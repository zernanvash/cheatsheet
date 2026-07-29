#!/usr/bin/env python3

from __future__ import annotations

TARGET_LOW16 = 0x9857


def gate1_crc(data: bytes) -> int:
    # fcn 0x402096:
    #   init eax = 0xffffffff
    #   per byte: eax ^= (byte << 8)
    #   8 rounds: if signbit(ax) set -> ((eax << 1) ^ 0x1021), else (eax << 1)
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= (b & 0xFF) << 8
        for _ in range(8):
            shifted = (crc << 1) & 0xFFFFFFFF
            if crc & 0x8000:
                crc = shifted ^ 0x1021
            else:
                crc = shifted
    return crc


def main() -> int:
    buf = bytearray(41)
    buf[32:36] = b"ETAG"
    buf[36:40] = (0x0000B00F).to_bytes(4, "little")
    buf[40] = 0x01

    solutions: list[tuple[int, int]] = []
    for x in range(256):
        buf[30] = x
        for y in range(256):
            buf[31] = y
            if gate1_crc(buf) & 0xFFFF == TARGET_LOW16:
                solutions.append((x, y))

    if not solutions:
        print("no solution found")
        return 1

    x0, y0 = solutions[0]
    print(f"solutions found: {len(solutions)}")
    print(f"first pair: b[30]=0x{x0:02x}, b[31]=0x{y0:02x}")

    # temp determ. replay - test
    xr, yr = 0x86, 0x67
    buf[30], buf[31] = xr, yr
    ok = (gate1_crc(buf) & 0xFFFF) == TARGET_LOW16
    print(f"replay pair (0x86,0x67) valid: {str(ok).lower()}")
    print(f"replay payload41 hex: {bytes(buf).hex()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
