#!/usr/bin/env python3
"""Build a static, attributed NTHW reader snapshot from an upstream checkout."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

UPSTREAM = "https://github.com/notthehiddenwiki/NTHW.git"
BRANCH = "nthw"
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ALLOWED_SCHEMES = {"http", "https", "mailto"}


def git(*args: str, cwd: Path | None = None) -> str:
    command = ["git"]
    if cwd:
        command += ["-c", f"safe.directory={cwd.resolve()}"]
    return subprocess.run(
        [*command, *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def acquire(source: Path | None) -> tuple[Path, tempfile.TemporaryDirectory | None]:
    if source:
        return source.resolve(), None
    temp = tempfile.TemporaryDirectory(prefix="nthw-")
    checkout = Path(temp.name) / "NTHW"
    git("clone", "--depth", "1", "--branch", BRANCH, UPSTREAM, str(checkout))
    return checkout, temp


def category_for(relative: Path) -> str:
    return " / ".join(relative.parts[:-1]) or "Root"


def parse(checkout: Path) -> tuple[list[dict], int]:
    entries: list[dict] = []
    rejected = 0
    for file in sorted(checkout.rglob("*.md")):
        relative = file.relative_to(checkout)
        if relative.parts[0] == ".github" or relative.name in {
            "LICENSE.md", "CONTRIBUTING.md", "HoF.md", "acknowledgements.md"
        }:
            continue
        text = file.read_text(encoding="utf-8", errors="replace")
        heading = ""
        for line_number, raw in enumerate(text.splitlines(), 1):
            stripped = raw.strip()
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
            for match in LINK_RE.finditer(raw):
                label, url = match.group(1).strip(), match.group(2).strip()
                scheme = urlparse(url).scheme.lower()
                if scheme not in ALLOWED_SCHEMES:
                    rejected += 1
                    continue
                prefix = raw[: match.start()].strip().lstrip("-* ").strip()
                description = re.sub(r"\s*[-–—:]\s*$", "", prefix).strip()
                entries.append({
                    "id": f"{relative.as_posix()}:{line_number}:{len(entries)}",
                    "category": category_for(relative),
                    "type": relative.stem.replace("_", " ").replace("-", " ").title(),
                    "heading": heading,
                    "description": description or label,
                    "label": label,
                    "url": url,
                    "source": relative.as_posix(),
                    "line": line_number,
                    "original": raw,
                })
    return entries, rejected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Existing NTHW checkout; otherwise clone upstream")
    parser.add_argument("--output", type=Path, default=Path("nthw/data.json"))
    args = parser.parse_args()
    checkout, temp = acquire(args.source)
    try:
        commit = git("rev-parse", "HEAD", cwd=checkout)
        entries, rejected = parse(checkout)
        if len(entries) < 1000:
            raise RuntimeError(f"Validation failed: only {len(entries)} publishable links found")
        payload = {
            "schema": 1,
            "upstream": "https://github.com/notthehiddenwiki/NTHW",
            "branch": BRANCH,
            "commit": commit,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "license": "CC BY-NC-ND 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "count": len(entries),
            "rejected_links": rejected,
            "entries": entries,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        staged = args.output.with_suffix(".json.tmp")
        staged.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        json.loads(staged.read_text(encoding="utf-8"))
        staged.replace(args.output)
        shutil.copyfile(checkout / "LICENSE.md", args.output.parent / "LICENSE-NTHW.md")
        print(f"Published {len(entries)} links from {commit}; rejected {rejected} unsupported links")
    finally:
        if temp:
            temp.cleanup()


if __name__ == "__main__":
    main()
