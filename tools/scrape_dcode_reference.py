#!/usr/bin/env python3
"""Create a personal offline dCode cryptography reference (no solver code)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = "https://www.dcode.fr"
ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "references" / "dcode-cryptography"
IMAGES = ROOT / "references" / "dcode-images"
DATA = ROOT / "references" / "dcode-cryptography-data.js"
INDEX = ROOT / "references" / "dCode Cryptography Index.md"
UA = "H4G-personal-offline-reference/1.0"
CHROME_IMAGES = {"dcode.png", "share.png", "discord-logo.png"}
EXCLUDED_SECTION_WORDS = ("source code", "algorithm", "how to code", "programming language", "api")


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "reference"


def inline(node: Tag) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            text = inline(child)
            if child.name in {"code", "kbd"}:
                parts.append(f"`{clean(text)}`")
            elif child.name in {"b", "strong"}:
                parts.append(f"**{clean(text)}**")
            elif child.name == "a" and child.get("href"):
                parts.append(f"[{clean(text)}]({urljoin(BASE, child['href'])})")
            else:
                parts.append(text)
    return clean("".join(parts))


def listing(session: requests.Session) -> list[dict[str, str]]:
    response = session.get(f"{BASE}/tools-list", timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    start = next(h for h in soup.find_all("h3") if clean(h.get_text(" ")) == "Cryptography")
    category = "Other"
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for node in start.find_all_next(["h3", "h4", "a"]):
        if node.name == "h3":
            break
        if node.name == "h4":
            category = clean(node.get_text(" "))
        elif node.name == "a" and node.get("href"):
            url = urljoin(BASE, node["href"])
            title = clean(node.get_text(" ")).removeprefix("★ ")
            if title and urlparse(url).netloc == "www.dcode.fr" and url not in seen:
                records.append({"category": category, "title": title, "url": url})
                seen.add(url)
    return records


def save_image(session: requests.Session, src: str, page_slug: str) -> str | None:
    url = urljoin(BASE, src)
    parsed = urlparse(url)
    name = Path(parsed.path).name
    if parsed.netloc != "www.dcode.fr" or name in CHROME_IMAGES or name.startswith("flag-"):
        return None
    response = session.get(url, timeout=30)
    response.raise_for_status()
    if not response.headers.get("content-type", "").startswith("image/"):
        return None
    suffix = Path(parsed.path).suffix.lower() or ".img"
    filename = f"{page_slug}-{slug(Path(name).stem)}-{hashlib.sha1(url.encode()).hexdigest()[:8]}{suffix}"
    path = IMAGES / filename
    if not path.exists():
        path.write_bytes(response.content)
    return f"references/dcode-images/{filename}"


def extract(session: requests.Session, record: dict[str, str]) -> dict:
    response = session.get(record["url"], timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = clean((soup.find("h1") or soup.title).get_text(" "))
    page_slug = slug(urlparse(record["url"]).path.rsplit("/", 1)[-1])
    sections: list[dict[str, str]] = []
    faq = next((h for h in soup.find_all("h2") if "Answers to Questions" in clean(h.get_text(" "))), None)
    current = {"heading": "Overview", "text": ""}
    if faq:
        for node in faq.find_all_next(["h2", "h3", "h4", "p", "ul", "ol", "table"]):
            if node is not faq and node.name == "h2":
                break
            if node.find_parent(["ul", "ol", "table"]) and node.name not in {"ul", "ol", "table"}:
                continue
            if node.name in {"h3", "h4"}:
                if current["text"]:
                    if not any(word in current["heading"].lower() for word in EXCLUDED_SECTION_WORDS):
                        sections.append(current)
                current = {"heading": clean(node.get_text(" ")), "text": ""}
            else:
                text = clean(node.get_text(" "))
                if text and "Ask a new question" not in text:
                    current["text"] += ("\n\n" if current["text"] else "") + text
        if current["text"]:
            if not any(word in current["heading"].lower() for word in EXCLUDED_SECTION_WORDS):
                sections.append(current)

    images: list[dict[str, str]] = []
    seen: set[str] = set()
    # Symbol pages expose short visual samples like the cipher atlas shown on dCode.
    # Other categories mostly contain site chrome or generated solver imagery.
    image_nodes = soup.find_all("img") if record["category"] == "Symbol Substitution" else []
    for image in image_nodes:
        src = image.get("src") or image.get("data-src")
        if not src or src in seen:
            continue
        seen.add(src)
        try:
            local = save_image(session, src, page_slug)
        except requests.RequestException:
            local = None
        if local:
            images.append({"src": local, "alt": clean(image.get("alt", "")) or title})
        if len(images) >= 12:
            break

    markdown = [
        f"# {title}", "", f"> Source: [{record['url']}]({record['url']})",
        f"> Retrieved: {date.today().isoformat()}",
        "> Attribution: dCode.fr (CC BY notice on the source page).",
        "> Reference-only extract: no converter, solver, API, or implementation code.", "",
    ]
    for section in sections:
        markdown.extend([f"## {section['heading']}", "", section["text"], ""])
    if images:
        markdown.extend(["## Reference Images", ""])
        markdown.extend(f"![{item['alt']}](../dcode-images/{Path(item['src']).name})" for item in images)
    (PAGES / f"{page_slug}.md").write_text("\n".join(markdown).rstrip() + "\n", encoding="utf-8")
    return {**record, "title": title, "slug": page_slug, "sections": sections, "images": images}


def write_outputs(records: list[dict]) -> None:
    DATA.write_text(
        "/* Generated by tools/scrape_dcode_reference.py */\nwindow.DCODE_CRYPTO_DATA = "
        + json.dumps({"retrieved": date.today().isoformat(), "records": records}, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    lines = [
        "# dCode Cryptography Reference Index", "",
        "> Personal offline study extracts from [dCode.fr](https://www.dcode.fr/tools-list).",
        f"> Retrieved {date.today().isoformat()}; attributed to dCode under the CC BY notice on each page.",
        "> Converter interfaces, solvers, scripts, APIs, and implementation code are excluded.", "",
    ]
    current = ""
    for item in records:
        if item["category"] != current:
            current = item["category"]
            lines.extend([f"## {current}", ""])
        lines.append(f"- [{item['title']}](dcode-cryptography/{item['slug']}.md)")
    INDEX.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    PAGES.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = UA
    items = listing(session)
    if args.limit:
        items = items[:args.limit]
    records = []
    for number, item in enumerate(items, 1):
        try:
            records.append(extract(session, item))
            print(f"[{number}/{len(items)}] {item['title']}")
        except (requests.RequestException, OSError, ValueError) as error:
            print(f"[{number}/{len(items)}] ERROR {item['title']}: {error}")
        time.sleep(max(args.delay, 0))
    write_outputs(records)
    print(f"Saved {len(records)} pages with {sum(len(r['images']) for r in records)} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
