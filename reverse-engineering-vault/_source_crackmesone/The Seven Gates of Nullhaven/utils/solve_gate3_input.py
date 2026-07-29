#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

TARGET_VA = 0x49CE20
NIBBLE_TABLE_VA = 0x49CE40
BIN_BASE_VA = 0x400000


def rol8(x: int, r: int) -> int:
    r &= 7
    return ((x << r) | (x >> (8 - r))) & 0xFF


def ror8(x: int, r: int) -> int:
    r &= 7
    return ((x >> r) | (x << (8 - r))) & 0xFF


def fib_bytes(n: int) -> bytes:
    # binary register update order
    # store edx, then ecx = ecx + edx, then edx = old ecx
    ecx, edx = 1, 1
    out = bytearray()
    for _ in range(n):
        out.append(edx & 0xFF)
        esi = ecx
        ecx = (ecx + edx) & 0xFFFFFFFF
        edx = esi
    return bytes(out)


def main() -> int:
    blob = Path("nullhaven").read_bytes()

    target_off = TARGET_VA - BIN_BASE_VA
    table_off = NIBBLE_TABLE_VA - BIN_BASE_VA
    target = bytearray(blob[target_off : target_off + 32])
    sbox = list(blob[table_off : table_off + 16])

    inv = [0] * 16
    for i, v in enumerate(sbox):
        inv[v] = i

    # undo stage 3: byte rotation by ((idx % 7) + 1).
    for i in range(32):
        target[i] = ror8(target[i], (i % 7) + 1)

    # undo stage 2: nibble substitution
    for i in range(32):
        hi = (target[i] >> 4) & 0xF
        lo = target[i] & 0xF
        target[i] = ((inv[hi] << 4) | inv[lo]) & 0xFF

    # undo stage 1: rolling XOR with fibonacci bytes
    fib = fib_bytes(32)
    plain = bytes(target[i] ^ fib[i] for i in range(32))

    print("input hex:", plain.hex())
    print("input ascii:", plain.decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
