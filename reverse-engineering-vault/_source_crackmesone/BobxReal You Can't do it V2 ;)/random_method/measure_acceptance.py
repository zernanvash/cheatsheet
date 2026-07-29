#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys


def run_once(exe: str, password: str) -> bool:
    env = os.environ.copy()
    env["WINEDEBUG"] = "-all"
    proc = subprocess.run(
        ["wine", exe],
        input=(password + "\n").encode("utf-8", "ignore"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        timeout=20,
    )
    out = proc.stdout.decode("latin1", "ignore")
    return "Correct!" in out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="measure acceptance rate of bobxREAL.exe for 16-byte keys."
    )
    ap.add_argument("--exe", default="bobxREAL.exe")
    ap.add_argument("--trials", type=int, default=40)
    ap.add_argument(
        "--password",
        action="append",
        required=True,
        help="16-character password; pass multiple --password args to compare.",
    )
    args = ap.parse_args()

    if args.trials <= 0:
        print("error: --trials must be > 0", file=sys.stderr)
        return 2

    for pw in args.password:
        if len(pw) != 16:
            print(f"error: password must be exactly 16 chars.: {pw!r}", file=sys.stderr)
            return 2

    for pw in args.password:
        ok = 0
        for _ in range(args.trials):
            if run_once(args.exe, pw):
                ok += 1
        rate = (ok / args.trials) * 100.0
        print(f"{pw} -> {ok}/{args.trials} ({rate:.1f}%)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

