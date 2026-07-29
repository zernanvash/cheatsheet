#!/usr/bin/env python3

from __future__ import annotations

import struct
from collections import deque
from pathlib import Path

TABLE_VA = 0x49CEA0
BIN_BASE_VA = 0x400000
TABLE_WORDS = 64
STATES = 16
XOR_MASK = 0xDEADBEEF
MOVES = "RULD"
START_STATE = 0
TARGET_STATE = 0xDEADBEE2 ^ XOR_MASK  # 13


def main() -> int:
    blob = Path("nullhaven").read_bytes()
    off = TABLE_VA - BIN_BASE_VA

    words = struct.unpack_from("<" + "I" * TABLE_WORDS, blob, off)

    edges = {s: [] for s in range(STATES)}
    for s in range(STATES):
        for i, m in enumerate(MOVES):
            raw = words[s * 4 + i]
            nxt = raw ^ XOR_MASK
            if 0 <= nxt < STATES:
                edges[s].append((nxt, m))

    q = deque([(START_STATE, "")])
    seen = {START_STATE}

    while q:
        s, path = q.popleft()
        if s == TARGET_STATE:
            print("path:", path)
            return 0
        for nxt, m in edges[s]:
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + m))

    print("no path found")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
