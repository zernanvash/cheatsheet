#!/usr/bin/env python3
"""Sync selected vault Markdown files to Notion child pages.

Required environment:
  NOTION_TOKEN
  NOTION_PARENT_PAGE_ID

Optional environment:
  NOTION_MANIFEST              default: notion-sync-manifest.txt
  NOTION_TITLE_PREFIX          default: empty
  NOTION_DELETE_UNLISTED       default: false
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_BLOCKS_PER_REQUEST = 100
MAX_TEXT = 1900


class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def request(self, method: str, path: str, payload: dict | None = None) -> dict:
        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            f"{API_BASE}{path}",
            data=data,
            headers=headers,
            method=method,
        )

        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = resp.read().decode("utf-8")
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code == 429 and attempt < 4:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise RuntimeError(f"Notion API {method} {path} failed: {exc.code} {body}") from exc

        raise RuntimeError(f"Notion API {method} {path} failed after retries")

    def search_page_by_title(self, title: str) -> str | None:
        payload = {
            "query": title,
            "filter": {"property": "object", "value": "page"},
            "page_size": 10,
        }
        result = self.request("POST", "/search", payload)
        for page in result.get("results", []):
            page_title = extract_page_title(page)
            if page_title == title:
                return page["id"]
        return None

    def create_page(self, parent_page_id: str, title: str) -> str:
        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}},
        }
        return self.request("POST", "/pages", payload)["id"]

    def child_blocks(self, page_id: str) -> list[dict]:
        blocks: list[dict] = []
        cursor = None
        while True:
            query = f"?page_size=100"
            if cursor:
                query += f"&start_cursor={urllib.parse.quote(cursor)}"
            result = self.request("GET", f"/blocks/{page_id}/children{query}")
            blocks.extend(result.get("results", []))
            if not result.get("has_more"):
                return blocks
            cursor = result.get("next_cursor")

    def clear_children(self, page_id: str) -> None:
        for block in self.child_blocks(page_id):
            self.request("PATCH", f"/blocks/{block['id']}", {"archived": True})

    def append_children(self, page_id: str, blocks: list[dict]) -> None:
        for i in range(0, len(blocks), MAX_BLOCKS_PER_REQUEST):
            chunk = blocks[i : i + MAX_BLOCKS_PER_REQUEST]
            self.request("PATCH", f"/blocks/{page_id}/children", {"children": chunk})


def extract_page_title(page: dict) -> str:
    props = page.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            return "".join(item.get("plain_text", "") for item in prop.get("title", []))
    return ""


def read_manifest(path: Path) -> list[Path]:
    files: list[Path] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        files.append(Path(line))
    return files


def page_title_for(path: Path, prefix: str) -> str:
    title = path.stem
    return f"{prefix}{title}" if prefix else title


def rich_text(text: str) -> list[dict]:
    text = strip_markdown_links(text)
    if not text:
        text = " "
    parts = []
    for chunk in split_text(text, MAX_TEXT):
        parts.append({"type": "text", "text": {"content": chunk}})
    return parts


def strip_markdown_links(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)


def split_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks


def paragraph(text: str) -> dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text(text)}}


def heading(level: int, text: str) -> dict:
    block_type = f"heading_{min(level, 3)}"
    return {"object": "block", "type": block_type, block_type: {"rich_text": rich_text(text)}}


def bulleted(text: str) -> dict:
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rich_text(text)}}


def numbered(text: str) -> dict:
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": rich_text(text)}}


def code_block(code: str, language: str) -> dict:
    if language.lower() in {"powershell", "ps1"}:
        language = "powershell"
    elif language.lower() in {"bash", "sh", "shell"}:
        language = "shell"
    elif language.lower() in {"python", "py"}:
        language = "python"
    elif language.lower() in {"javascript", "js"}:
        language = "javascript"
    elif language.lower() in {"cmd", "batch", "bat", "text"}:
        language = "plain text"
    else:
        language = "plain text"

    blocks = []
    for chunk in split_text(code.rstrip() or " ", MAX_TEXT):
        blocks.append(
            {
                "object": "block",
                "type": "code",
                "code": {"rich_text": rich_text(chunk), "language": language},
            }
        )
    return blocks[0] if len(blocks) == 1 else paragraph(code.rstrip())


def markdown_to_blocks(markdown: str, source_path: Path) -> list[dict]:
    blocks: list[dict] = []
    lines = markdown.splitlines()
    in_code = False
    code_lang = "plain text"
    code_lines: list[str] = []

    for line in lines:
        fence = re.match(r"^```(\S*)", line)
        if fence:
            if in_code:
                blocks.append(code_block("\n".join(code_lines), code_lang))
                code_lines = []
                code_lang = "plain text"
                in_code = False
            else:
                in_code = True
                code_lang = fence.group(1) or "plain text"
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            continue

        h = re.match(r"^(#{1,6})\s+(.+)$", line)
        if h:
            blocks.append(heading(len(h.group(1)), h.group(2).strip()))
            continue

        b = re.match(r"^\s*[-*]\s+(.+)$", line)
        if b:
            blocks.append(bulleted(b.group(1).strip()))
            continue

        n = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if n:
            blocks.append(numbered(n.group(1).strip()))
            continue

        blocks.append(paragraph(line.strip()))

    if in_code:
        blocks.append(code_block("\n".join(code_lines), code_lang))

    blocks.append(paragraph(f"Source: {source_path.as_posix()}"))
    return blocks


def main() -> int:
    token = os.environ.get("NOTION_TOKEN")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID")
    manifest = Path(os.environ.get("NOTION_MANIFEST", "notion-sync-manifest.txt"))
    title_prefix = os.environ.get("NOTION_TITLE_PREFIX", "")

    if not token or not parent_page_id:
        print("NOTION_TOKEN and NOTION_PARENT_PAGE_ID are required.", file=sys.stderr)
        return 2
    if not manifest.exists():
        print(f"Manifest not found: {manifest}", file=sys.stderr)
        return 2

    client = NotionClient(token)
    for rel_path in read_manifest(manifest):
        if not rel_path.exists():
            print(f"skip missing: {rel_path}")
            continue
        title = page_title_for(rel_path, title_prefix)
        page_id = client.search_page_by_title(title)
        if page_id:
            print(f"update: {title}")
            client.clear_children(page_id)
        else:
            print(f"create: {title}")
            page_id = client.create_page(parent_page_id, title)

        markdown = rel_path.read_text(encoding="utf-8")
        blocks = markdown_to_blocks(markdown, rel_path)
        client.append_children(page_id, blocks)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
