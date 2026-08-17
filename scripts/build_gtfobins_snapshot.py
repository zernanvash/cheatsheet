#!/usr/bin/env python3
"""Build a static GTFOBins data snapshot from an upstream checkout."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError as error:
    raise SystemExit("PyYAML is required to refresh this snapshot: python3 -m pip install PyYAML") from error

UPSTREAM = "https://github.com/GTFOBins/gtfobins.github.io.git"


def git(*args: str, cwd: Path | None = None) -> str:
    command = ["git"]
    if cwd:
        command += ["-c", f"safe.directory={cwd.resolve()}"]
    return subprocess.run([*command, *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def acquire(source: Path | None) -> tuple[Path, tempfile.TemporaryDirectory | None]:
    if source:
        return source.resolve(), None
    temporary = tempfile.TemporaryDirectory(prefix="gtfobins-")
    checkout = Path(temporary.name) / "gtfobins"
    git("clone", "--depth", "1", UPSTREAM, str(checkout))
    return checkout, temporary


def merge_documents(checkout: Path, relative: str) -> dict:
    merged: dict = {}
    for document in yaml.safe_load_all(git("show", f"HEAD:{relative}", cwd=checkout)):
        if isinstance(document, dict):
            merged.update(document)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Existing GTFOBins checkout; otherwise clone upstream")
    parser.add_argument("--output", type=Path, default=Path("gtfobins/data.json"))
    args = parser.parse_args()
    checkout, temporary = acquire(args.source)
    try:
        commit = git("rev-parse", "HEAD", cwd=checkout)
        functions = yaml.safe_load((checkout / "_data" / "functions.yml").read_text(encoding="utf-8"))
        contexts = yaml.safe_load((checkout / "_data" / "contexts.yml").read_text(encoding="utf-8"))
        bins = []
        paths = git("ls-tree", "-r", "--name-only", "HEAD", "_gtfobins", cwd=checkout).splitlines()
        for relative in sorted(paths, key=str.casefold):
            name = relative.rsplit("/", 1)[-1]
            value = merge_documents(checkout, relative)
            entries = value.get("functions", {})
            if not isinstance(entries, dict):
                entries = {}
            aliases = value.get("alias", [])
            if isinstance(aliases, str):
                aliases = [aliases]
            bins.append({"name": name, "aliases": aliases or [], "comment": value.get("comment", ""), "functions": entries})
        if len(bins) < 400:
            raise RuntimeError(f"Validation failed: only {len(bins)} executable definitions found")
        payload = {"schema": 1, "upstream": "https://github.com/GTFOBins/gtfobins.github.io", "commit": commit, "generated_at": datetime.now(timezone.utc).isoformat(), "license": "GPL-3.0", "count": len(bins), "function_definitions": functions, "context_definitions": contexts, "bins": bins}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        staged = args.output.with_suffix(".json.tmp")
        staged.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        json.loads(staged.read_text(encoding="utf-8"))
        staged.replace(args.output)
        (args.output.parent / "LICENSE-GTFOBINS.txt").write_text(git("show", "HEAD:LICENSE", cwd=checkout) + "\n", encoding="utf-8")
        print(f"Published {len(bins)} GTFOBins definitions from {commit}")
    finally:
        if temporary:
            temporary.cleanup()


if __name__ == "__main__":
    main()
