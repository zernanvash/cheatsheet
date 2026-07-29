#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys


def run_once(exe: str, password: str, suppress_wine_debug: bool = True) -> tuple[bool, str]:
    env = os.environ.copy()
    if suppress_wine_debug:
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
    return ("Correct!" in out), out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="exploit bobxREAL.exe randomized validator. retry a 16-byte key until success."
    )
    ap.add_argument("--exe", default="bobxREAL.exe")
    ap.add_argument("--password", default="AAAAAAAAAAAAAAAA")
    ap.add_argument("--max-attempts", type=int, default=200)
    args = ap.parse_args()

    if len(args.password) != 16:
        print("error: password must be exactly 16 characters", file=sys.stderr)
        return 2

    for i in range(1, args.max_attempts + 1):
        ok, out = run_once(args.exe, args.password)
        if ok:
            print(f"[+] success on attempt {i} with key: {args.password!r}")
            # Show the final two lines from the program for quick proof.
            lines = [ln for ln in out.splitlines() if ln.strip()]
            for ln in lines[-2:]:
                print(ln)
            return 0
        print(f"[-] attempt {i}: Wrong.")

    print(f"[!] no success after {args.max_attempts} attempts", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
