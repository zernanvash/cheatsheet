"""Constrained OpenCode explanation layer for deterministic cipher rankings."""

from __future__ import annotations

import json
import os
import subprocess
from typing import Any


def _extract_text(events: str) -> str:
    """Extract assistant text from OpenCode JSON events, tolerating CLI versions."""
    chunks: list[str] = []
    for line in events.splitlines():
        try: event = json.loads(line)
        except json.JSONDecodeError: continue
        for key in ("text", "content", "response"):
            value = event.get(key)
            if isinstance(value, str): chunks.append(value)
        part = event.get("part")
        if isinstance(part, dict) and isinstance(part.get("text"), str): chunks.append(part["text"])
    return "\n".join(chunks).strip() or events.strip()


def _json_object(text: str) -> dict[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start: raise ValueError("OpenCode returned no JSON object")
    return json.loads(text[start:end + 1])


def advise(ciphertext: str, deterministic: dict) -> dict:
    candidates = deterministic["candidates"][:5]
    allowed = {item["id"] for item in candidates}
    if not allowed: return {"status": "skipped", "reason": "No deterministic candidates."}
    prompt = {
        "role": "You are a constrained cipher-analysis reviewer. The algorithmic engine is authoritative.",
        "rules": [
            "Use only candidate IDs supplied below; never invent a cipher.",
            "Do not claim certainty or claim decryption.",
            "Evidence must refer only to supplied computed evidence or visible ciphertext structure.",
            "Return JSON only with keys ranking, explanation, questions.",
            "ranking is an ordered array containing zero or more allowed candidate IDs.",
            "explanation is at most 500 characters; questions is an array of at most 3 short strings."
        ],
        "features": deterministic["features"],
        "candidates": [{"id": x["id"], "score": x["score"], "evidence": x["evidence"]} for x in candidates],
        "ciphertext_sample": ciphertext[:2000],
    }
    command = [os.getenv("OPENCODE_BIN", "opencode"), "run", "--format", "json"]
    model = os.getenv("OPENCODE_MODEL", "").strip()
    if model: command += ["--model", model]
    command.append(json.dumps(prompt, ensure_ascii=False, separators=(",", ":")))
    completed = subprocess.run(command, capture_output=True, text=True, timeout=int(os.getenv("OPENCODE_TIMEOUT", "25")), check=False)
    if completed.returncode: raise RuntimeError((completed.stderr or "OpenCode failed")[-500:])
    payload = _json_object(_extract_text(completed.stdout))
    ranking = payload.get("ranking", [])
    if not isinstance(ranking, list) or any(item not in allowed for item in ranking): raise ValueError("OpenCode ranking violated candidate allowlist")
    explanation = payload.get("explanation", "")
    questions = payload.get("questions", [])
    if not isinstance(explanation, str) or len(explanation) > 500: raise ValueError("Invalid OpenCode explanation")
    if not isinstance(questions, list) or len(questions) > 3 or any(not isinstance(x, str) or len(x) > 180 for x in questions): raise ValueError("Invalid OpenCode questions")
    return {"status": "ok", "ranking": ranking, "explanation": explanation, "questions": questions}


def safe_advise(ciphertext: str, deterministic: dict) -> dict:
    if os.getenv("CIPHER_AI_ENABLED", "0").lower() not in {"1", "true", "yes"}:
        return {"status": "disabled", "reason": "AI review is disabled on this server."}
    try: return advise(ciphertext, deterministic)
    except subprocess.TimeoutExpired: return {"status": "unavailable", "reason": "OpenCode timed out; deterministic results remain valid."}
    except Exception as error: return {"status": "unavailable", "reason": f"AI review rejected: {str(error)[:180]}"}
