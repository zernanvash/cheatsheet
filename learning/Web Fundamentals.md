# Web Fundamentals

Use this before the web exploitation blueprint. The goal is to understand what a web app is, how HTTP works, and which parts of a request or response can become security-relevant.

Sources summarized:

- Esther7171 TryHackMe walkthrough: [Web Application Basics](https://github.com/Esther7171/TryHackMe-Walkthroughs/blob/main/Room/Web_Application_Basics/readme.md)
- Local offline PDF: [Web Exploitation.pdf](../references/Web%20Exploitation.pdf)

## Web Application Model

- Front end: HTML, CSS, and JavaScript running in the browser.
- Back end: web server, application server, database, storage, and supporting services.
- Database: stores and retrieves application data.
- WAF: optional filtering layer that may block suspicious requests.

Study question: when you see a web page, ask which logic is client-side and which must be server-side.

## URL Anatomy

Example:

```text
https://user@example.com:443/path/page.php?id=10#section
```

- Scheme: `http` or `https`.
- User info: rarely used now; unsafe for secrets.
- Host/domain: target web name.
- Port: service endpoint, such as `80`, `443`, `8080`.
- Path: resource location.
- Query string: key/value input after `?`.
- Fragment: browser-side anchor after `#`.

Security link: paths and query strings are common places for IDOR, traversal, SQLi, XSS, and parameter tampering.

## HTTP Request

HTTP requests trigger actions on the web application.

```http
GET /login HTTP/1.1
Host: target.local
User-Agent: Mozilla/5.0
Cookie: session=abc
```

Request line:

- Method: action such as `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`.
- Path: resource requested.
- Version: HTTP protocol version.

Important request headers:

- `Host`: target virtual host.
- `User-Agent`: client identity.
- `Referer`: source page.
- `Cookie`: client-side state sent back to server.
- `Content-Type`: body format.

Request body formats:

- `application/x-www-form-urlencoded`: `key=value&key2=value2`.
- `multipart/form-data`: file uploads and mixed form fields.
- `application/json`: API data.
- `application/xml`: XML/SOAP-style data.

## HTTP Response

HTTP responses return status, headers, and body content.

Status classes:

- `100-199`: informational.
- `200-299`: success.
- `300-399`: redirect.
- `400-499`: client/request problem.
- `500-599`: server-side problem.

Common status codes:

- `200 OK`: request worked.
- `301 Moved Permanently`: resource moved.
- `302 Found`: temporary redirect.
- `401 Unauthorized`: authentication required.
- `403 Forbidden`: authenticated or not, access denied.
- `404 Not Found`: resource not found.
- `500 Internal Server Error`: application/server failure.

Response headers to recognize:

- `Server`: software/version leak.
- `Set-Cookie`: session or state issued to browser.
- `Location`: redirect target.
- `Content-Type`: response format.
- `Cache-Control`: cache behavior.

## Security Headers

- `Content-Security-Policy`: restricts where scripts, styles, and other resources can load from.
- `Strict-Transport-Security`: forces HTTPS for future requests.
- `X-Content-Type-Options: nosniff`: prevents MIME sniffing.
- `Referrer-Policy`: controls referrer leakage.
- Cookie flags: `Secure`, `HttpOnly`, and `SameSite`.

## Practice Checklist

- Capture a request and identify method, path, headers, cookies, and body.
- Change one harmless parameter and observe the response.
- Compare status code, redirect location, response length, and body content.
- Run `OPTIONS` only in a lab to learn supported methods.

## When To Jump To Blueprints

- You understand requests/responses and need an attack workflow -> [Web Exploit Blueprint](../blueprints/Web%20Exploit%20Blueprint.md).
- You found a file parameter -> [LFI And Directory Traversal](../blueprints/machine-attacks/LFI%20And%20Directory%20Traversal.md).
- You found an upload -> [Web Upload To Shell](../blueprints/machine-attacks/Web%20Upload%20To%20Shell.md).
- You found XML -> [XXE To File Read](../blueprints/machine-attacks/XXE%20To%20File%20Read.md).
