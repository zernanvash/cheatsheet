#!/usr/bin/env python3
"""
Prometheora reliable runner.

Uses the recovered valid key and retries launch/submit until the binary
hits the timing window and returns the success banner.

Usage:
    python3 prometheora_runner.py
"""

from __future__ import annotations

import os
import pty
import select
import subprocess
import time

KEY = "PR0M3TH30R_F1R3_UNL34SH_2027\n"
SUCCESS_MARKER = "Congratulations"


def run_once(timeout_s: float = 4.0) -> tuple[bool, str, int]:
    env = [
        "env",
        "-i",
        f"HOME={os.environ.get('HOME', '')}",
        "PATH=/usr/bin:/bin",
        "TERM=xterm-256color",
    ]

    master, slave = pty.openpty()
    proc = subprocess.Popen(
        env + ["./prometheora"],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        close_fds=True,
    )
    os.close(slave)

    buf = b""

    # Wait until prompt appears.
    end = time.time() + timeout_s
    while time.time() < end:
        r, _, _ = select.select([master], [], [], 0.05)
        if master in r:
            try:
                d = os.read(master, 4096)
            except OSError:
                break
            if not d:
                break
            buf += d
            if b"Enter key:" in buf:
                break

    # Submit key in one write (best observed success rate).
    try:
        os.write(master, KEY.encode())
    except OSError:
        pass

    # Drain output.
    end = time.time() + timeout_s
    while time.time() < end and proc.poll() is None:
        r, _, _ = select.select([master], [], [], 0.05)
        if master in r:
            try:
                d = os.read(master, 4096)
            except OSError:
                break
            if not d:
                break
            buf += d

    try:
        proc.wait(timeout=0.2)
    except Exception:
        proc.kill()
        proc.wait()

    try:
        os.close(master)
    except OSError:
        pass

    out = buf.decode(errors="ignore")
    return (SUCCESS_MARKER in out, out, proc.returncode)


def main() -> int:
    print("[*] Trying recovered key until success window hits...")
    for attempt in range(1, 301):
        ok, out, rc = run_once()
        if ok:
            print(f"[+] Success on attempt {attempt} (exit={rc})")
            print("-" * 80)
            print(out)
            print("-" * 80)
            return 0
        if attempt % 25 == 0:
            print(f"[.] attempts: {attempt}")

    print("[-] No success hit within retry budget.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
