#!/usr/bin/env python3
"""stdin byte-stream that solves all 7 gates"""

from __future__ import annotations

import argparse
from pathlib import Path


GATE3_INPUT = b"SOLVETHEPUZZLEOFNULLHAVEN12345XX"
GATE4_SERIAL = b"0001-C033-2EF2-822B"
GATE5_PATH = b"UDLD"
GATE6_KEY = b"VEIL_LIFTED"
GATE7_KEY = b"LwbsZVbFY9QZbCJ1qn-WkXpRuHgVE5iYZ5BsM7zOir_LWDFzN.WeRuan"


def gate1_payload_64() -> bytes:
    payload = bytearray(41)
    # CRC bytes in positions 30..31
    payload[30] = 0x86
    payload[31] = 0x67
    payload[32:36] = b"ETAG"
    payload[36:40] = (0x0000B00F).to_bytes(4, "little")
    payload[40] = 0x01
    return bytes(payload) + b"A" * (64 - len(payload))


def gate2_room1_64() -> bytes:
    return (
        b"B" * 32
        + (0xDECADE42).to_bytes(4, "little")
        + (0x50484153).to_bytes(4, "little")
        + b"C" * (64 - 40)
    )


def gate2_room2_64() -> bytes:
    v = (0xDECADE42 ^ 0xCAFEBABE) & 0xFFFFFFFF
    return (
        b"D" * 32
        + (0x4F50454E).to_bytes(4, "little")
        + v.to_bytes(4, "little")
        + b"E" * (64 - 40)
    )


def build_stream() -> bytes:
    # !! Gate 1 + Gate 2 use raw fixed-size readers + no newline
    return (
        b"1\n"
        + gate1_payload_64()
        + b"2\n"
        + gate2_room1_64()
        + gate2_room2_64()
        + b"3\n"
        + GATE3_INPUT
        + b"\n4\n"
        + GATE4_SERIAL
        + b"\n5\n"
        + GATE5_PATH
        + b"\n6\n"
        + GATE6_KEY
        + b"\n7\n"
        + GATE7_KEY
        + b"\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        default="solution_stream.bin",
        help="out path for the binary in  stream (default: %(default)s)",
    )
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = build_stream()
    out_path.write_bytes(data)
    print(f"wrote {len(data)} bytes -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
