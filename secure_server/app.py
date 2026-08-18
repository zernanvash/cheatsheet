"""FastAPI entry point for the password-protected H4G vault."""

from __future__ import annotations

import asyncio
import hashlib
import html
import mimetypes
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

import httpx
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response, StreamingResponse
from starlette.background import BackgroundTask
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .auth import new_token, safe_next, token_digest, user_agent_digest
from .database import Database
from .paths import PathDenied, resolve_vault_path
from .settings import Settings


SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "Cross-Origin-Opener-Policy": "same-origin",
}
CSP = (
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; "
    "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
)


def create_app(settings: Settings | None = None, *, clock=None, delay=asyncio.sleep) -> FastAPI:
    config = settings or Settings.from_env()
    database = Database(config.database_path, clock=clock) if clock else Database(config.database_path)
    verifier = PasswordHasher()
    verify_gate = asyncio.Semaphore(2)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        database.cleanup()
        async def periodic_cleanup():
            while True:
                await asyncio.sleep(300)
                database.cleanup()

        cleanup_task = asyncio.create_task(periodic_cleanup())
        try:
            yield
        finally:
            cleanup_task.cancel()
            database.connection.close()

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["ch.zernanvash.dev", "localhost", "127.0.0.1", "testserver"])
    app.state.settings = config
    app.state.database = database

    @app.middleware("http")
    async def headers(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception:
            response = JSONResponse({"error": "Internal server error"}, status_code=500)
        for name, value in SECURITY_HEADERS.items():
            response.headers[name] = value
        response.headers["Content-Security-Policy"] = CSP
        return response

    def cookie_token(request: Request) -> str | None:
        token = request.cookies.get(config.cookie_name)
        return token if token and 20 <= len(token) <= 128 else None

    def authenticated(request: Request):
        token = cookie_token(request)
        return database.session(token_digest(token)) if token else None

    def set_cookie(response: Response, token: str) -> None:
        response.set_cookie(
            config.cookie_name, token, max_age=config.session_seconds, path="/",
            secure=True, httponly=True, samesite="strict",
        )

    def clear_cookie(response: Response) -> None:
        response.delete_cookie(
            config.cookie_name, path="/", secure=True, httponly=True, samesite="strict",
        )

    def valid_origin(request: Request) -> bool:
        origin = request.headers.get("origin")
        if origin:
            return origin == config.origin
        return request.headers.get("sec-fetch-site") == "same-origin"

    def client_ip(request: Request) -> str:
        peer = request.client.host if request.client else "unknown"
        if config.trust_proxy and peer in {"127.0.0.1", "::1", "testclient"}:
            return request.headers.get("x-forwarded-for", peer).split(",")[0].strip()[:64]
        return peer[:64]

    def login_page(next_path: str, error: bool = False) -> HTMLResponse:
        template = (Path(__file__).parent / "templates" / "login.html").read_text(encoding="utf-8")
        body = template.replace("{{NEXT}}", html.escape(safe_next(next_path), quote=True))
        body = body.replace("{{ERROR}}", "Invalid passphrase or login temporarily unavailable." if error else "")
        return HTMLResponse(body, headers={"Cache-Control": "no-store"})

    @app.get("/login")
    async def login(request: Request, next: str = "/"):
        if authenticated(request):
            return RedirectResponse(safe_next(next), status_code=303)
        return login_page(next)

    @app.get("/_auth-static/login.css")
    async def login_css():
        return FileResponse(Path(__file__).parent / "static" / "login.css", media_type="text/css")

    @app.post("/auth/login")
    async def auth_login(request: Request):
        if not valid_origin(request):
            return JSONResponse({"error": "Forbidden"}, status_code=403)
        if request.headers.get("content-type", "").split(";", 1)[0] != "application/x-www-form-urlencoded":
            return JSONResponse({"error": "Unsupported media type"}, status_code=415)
        form = await request.form()
        passphrase, next_path = str(form.get("passphrase", "")), safe_next(str(form.get("next", "/")))
        database.cleanup()
        ip = client_ip(request)
        failures = database.failure_count(ip)
        if failures > 10:
            return JSONResponse({"error": "Invalid passphrase or login temporarily unavailable."}, status_code=429, headers={"Retry-After": "900", "Cache-Control": "no-store"})
        if failures >= 5:
            await delay(2)
        try:
            async with verify_gate:
                await asyncio.to_thread(verifier.verify, config.passphrase_hash, passphrase)
            valid = True
        except (VerifyMismatchError, InvalidHashError, VerificationError):
            valid = False
        if not valid:
            count = database.record_failure(ip)
            status = 429 if count > 10 else 401
            headers_out = {"Retry-After": "900"} if status == 429 else {}
            response = login_page(next_path, error=True)
            response.status_code = status
            response.headers.update(headers_out)
            return response
        old = cookie_token(request)
        if old:
            database.delete_session(token_digest(old))
        database.reset_failures(ip)
        token = new_token()
        database.create_session(token_digest(token), config.session_seconds, user_agent_digest(request.headers.get("user-agent", "")))
        response = RedirectResponse(next_path, status_code=303)
        set_cookie(response, token)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/auth/status")
    async def auth_status(request: Request):
        row = authenticated(request)
        if not row:
            response = JSONResponse({"authenticated": False}, status_code=401)
            clear_cookie(response)
            return response
        return JSONResponse({"authenticated": True, "expires_at": row["expires_at"]}, headers={"Cache-Control": "no-store"})

    @app.post("/auth/heartbeat")
    async def heartbeat(request: Request):
        if not valid_origin(request):
            return JSONResponse({"error": "Forbidden"}, status_code=403)
        database.cleanup()
        token = cookie_token(request)
        expires = database.renew_session(token_digest(token), config.session_seconds) if token else None
        if not expires:
            response = JSONResponse({"authenticated": False}, status_code=401)
            clear_cookie(response)
            return response
        response = JSONResponse({"authenticated": True, "expires_at": expires}, headers={"Cache-Control": "no-store"})
        set_cookie(response, token)
        return response

    @app.post("/auth/logout")
    async def logout(request: Request):
        if not valid_origin(request):
            return JSONResponse({"error": "Forbidden"}, status_code=403)
        token = cookie_token(request)
        if token and database.session(token_digest(token)):
            database.delete_session(token_digest(token))
        response = Response(status_code=204, headers={"Cache-Control": "no-store"})
        clear_cookie(response)
        return response

    async def proxy_api(request: Request, upstream: str) -> Response:
        client = httpx.AsyncClient(timeout=httpx.Timeout(60, read=None))
        target = f"{upstream}{request.url.path}"
        if request.url.query:
            target += f"?{request.url.query}"
        headers_in = {key: value for key, value in request.headers.items() if key.lower() not in {"host", "cookie", "content-length", "connection"}}
        headers_in["x-forwarded-for"] = client_ip(request)
        upstream_request = client.build_request(request.method, target, headers=headers_in, content=request.stream())
        try:
            upstream_response = await client.send(upstream_request, stream=True)
        except httpx.HTTPError:
            await client.aclose()
            return JSONResponse({"error": "Vault service unavailable"}, status_code=502)
        headers_out = {
            key: value for key, value in upstream_response.headers.items()
            if key.lower() not in {"connection", "content-length", "content-encoding", "transfer-encoding", "server"}
        }
        return StreamingResponse(
            upstream_response.aiter_raw(), status_code=upstream_response.status_code,
            headers=headers_out, background=BackgroundTask(client.aclose),
        )

    @app.api_route("/api/{api_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def protected_api(api_path: str, request: Request):
        if not authenticated(request):
            return JSONResponse({"authenticated": False}, status_code=401, headers={"Cache-Control": "no-store"})
        if request.method in {"POST", "PUT", "DELETE"} and not valid_origin(request):
            return JSONResponse({"error": "Forbidden"}, status_code=403)
        if api_path.startswith("cipher-identify"):
            return await proxy_api(request, config.cipher_api)
        if api_path.startswith("zen-notes"):
            return await proxy_api(request, config.zen_notes_api)
        if api_path.startswith("fileshare"):
            return await proxy_api(request, config.fileshare_api)
        return JSONResponse({"error": "Not found"}, status_code=404)

    @app.get("/_auth/session-lease.js")
    async def lease_script(request: Request):
        if not authenticated(request):
            return JSONResponse({"authenticated": False}, status_code=401)
        return FileResponse(Path(__file__).parent / "static" / "session-lease.js", media_type="text/javascript", headers={"Cache-Control": "private, max-age=3600"})

    @app.get("/{vault_path:path}")
    async def vault_file(vault_path: str, request: Request):
        if not authenticated(request):
            next_path = request.url.path + (f"?{request.url.query}" if request.url.query else "")
            return RedirectResponse(f"/login?next={quote(safe_next(next_path), safe='')}", status_code=303, headers={"Cache-Control": "no-store"})
        try:
            path = resolve_vault_path(config.vault_root, request.scope.get("raw_path", request.url.path.encode()))
        except (PathDenied, FileNotFoundError, OSError):
            return JSONResponse({"error": "Not found"}, status_code=404)
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix.casefold() == ".md":
            media_type = "text/markdown; charset=utf-8"
        if path.suffix.casefold() == ".js":
            media_type = "text/javascript; charset=utf-8"
        if path.suffix.casefold() in {".html", ".htm"}:
            body = path.read_text(encoding="utf-8", errors="replace")
            loader = '<script src="/_auth/session-lease.js" defer></script>'
            body = body.replace("</head>", f"  {loader}\n</head>", 1)
            return HTMLResponse(body, headers={"Cache-Control": "no-store"})
        disposition = "attachment" if path.suffix.casefold() in {".zip", ".pdf", ".docx"} else None
        cache = "no-store" if path.suffix.casefold() in {".md", ".json"} else "private, max-age=3600"
        return FileResponse(path, media_type=media_type, filename=path.name if disposition else None, content_disposition_type=disposition or "inline", headers={"Cache-Control": cache})

    return app


app = create_app()
