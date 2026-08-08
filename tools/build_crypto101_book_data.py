#!/usr/bin/env python3
"""Build the offline Crypto 101 reader data from the preserved Markdown archive."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "Crypto101 Full Text Archive.md"
OUTPUT = ROOT / "references" / "crypto101-book-data.js"


def clean_text(lines: list[str]) -> str:
    cleaned: list[str] = []
    for line in lines:
        line = line.replace("\x00", "").strip()
        if re.fullmatch(r"\d+", line):
            continue
        if line in {"Building blocks", "Complete cryptosystems", "Appendices"}:
            continue
        cleaned.append(line)

    paragraphs: list[str] = []
    current: list[str] = []
    for line in cleaned + [""]:
        if not line:
            if current:
                text = " ".join(current)
                text = re.sub(r"(?<=\w)- (?=[a-z])", "", text)
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    paragraphs.append(text)
                current = []
            continue
        if line.startswith(("- ", "* ")):
            if current:
                paragraphs.append(re.sub(r"\s+", " ", " ".join(current)).strip())
                current = []
            paragraphs.append(line)
        else:
            current.append(line)
    return "\n\n".join(paragraphs)


def slug(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def parse_book(markdown: str) -> list[dict[str, object]]:
    lines = markdown.splitlines()
    chapters: list[dict[str, object]] = []
    part = "Front matter"
    chapter: dict[str, object] | None = None
    subsection: dict[str, object] | None = None

    def finish_subsection() -> None:
        nonlocal subsection
        if chapter is not None and subsection is not None:
            subsection["text"] = clean_text(subsection.pop("lines"))
            if subsection["text"]:
                chapter["sections"].append(subsection)
        subsection = None

    def finish_chapter() -> None:
        nonlocal chapter
        finish_subsection()
        if chapter is not None:
            intro = clean_text(chapter.pop("lines"))
            if intro:
                chapter["intro"] = intro
            chapters.append(chapter)
        chapter = None

    for line in lines:
        if line.startswith("# Part "):
            finish_chapter()
            part = line[2:].strip()
            if "Glossary" in part or "References" in part:
                title = part.split(":", 1)[-1].strip()
                chapter = {"id": slug(title), "part": part, "title": title, "lines": [], "sections": []}
            continue
        if line.startswith("## Chapter ") or line.startswith("## Appendix "):
            finish_chapter()
            title = line[3:].strip()
            chapter = {"id": slug(title), "part": part, "title": title, "lines": [], "sections": []}
            continue
        if line.startswith("### ") and chapter is not None:
            finish_subsection()
            title = line[4:].strip()
            subsection = {"id": slug(title), "title": title, "lines": []}
            continue
        if line.startswith("## ") and chapter is not None and chapter["title"] in {"Glossary", "References"}:
            finish_subsection()
            title = line[3:].strip()
            subsection = {"id": slug(title), "title": title, "lines": []}
            continue
        if chapter is not None:
            target = subsection["lines"] if subsection is not None else chapter["lines"]
            target.append(line)

    finish_chapter()
    return chapters


def main() -> None:
    chapters = parse_book(SOURCE.read_text(encoding="utf-8"))
    payload = {
        "title": "Crypto 101",
        "author": "Laurens Van Houtven (lvh)",
        "version": "0.6.0-95-g64e8ccf",
        "license": "CC BY-NC 4.0",
        "chapters": chapters,
    }
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    OUTPUT.write_text(f"window.CRYPTO101_BOOK = {encoded};\n", encoding="utf-8")
    section_count = sum(len(chapter["sections"]) for chapter in chapters)
    print(f"Wrote {len(chapters)} chapters and {section_count} sections to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
