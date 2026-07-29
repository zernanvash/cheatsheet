#!/usr/bin/env python3
"""
Patch code.flp so FlipVM starts at a small injected VM stub.

The stub directly loads the valid password into R0 just before the VM's
mutation/check routine.  The FLP header is then rebuilt so the loader accepts
our modified bytecode.

Usage:
    python3 patch.py code.flp patched.flp
"""

from pathlib import Path
import sys

# RSA-looking header parameters accepted by the VM loader.
# The challenge stores N and E in the file header, so we can rebuild a valid
# header for the patched bytecode.
P = 4013756539255022581843
Q = 4032658848359024928157
N = P * Q
E = 0x10001
HEADER_SIZE = 3 + 128 + 3 + 128 + 4
PASSWORD = b"$?$__LeT_Th#_h@ck!ng_b3g1n__$?$"


def fnv1a_hash(data: bytes) -> int:
    """FlipVM's slightly modified 64-bit FNV-like hash."""
    hash_val = 0x3140101438
    for byte in data:
        b = 0
        for j in range(8):
            b |= byte << (8 * j)
        hash_val = (hash_val * 8675309) ^ b
        hash_val &= 0xFFFFFFFFFFFFFFFF
    return hash_val


def build_header(code: bytes, entrypoint: int) -> bytes:
    h = fnv1a_hash(code)
    signature = pow(h, E, N)
    xor = (signature ^ entrypoint) & 0xFFFFFFFF
    return (
        b"FLP"
        + N.to_bytes(128, byteorder="little")
        + E.to_bytes(3, byteorder="little")
        + signature.to_bytes(128, byteorder="little")
        + xor.to_bytes(4, byteorder="little")
    )


def patch(in_path: Path, out_path: Path) -> None:
    data = in_path.read_bytes()
    if len(data) <= HEADER_SIZE or data[:3] != b"FLP":
        raise SystemExit("input is not a valid-looking FLP file")

    code = bytearray(data[HEADER_SIZE:])

    # VM mode switch: MODE 1 / big immediate mode.
    big_insn = b"\x58\x01\x01"

    # MOV R0, PASSWORD
    # The immediate is encoded little-endian in the VM bytecode.
    mov_insn = b"\x28\x88\x1f" + PASSWORD

    # Drop the injected block immediately before the mutation routine.
    mutate_offs = 0xFA1
    big_offs = mutate_offs - len(big_insn) - len(mov_insn)
    mov_offs = mutate_offs - len(mov_insn)

    if big_offs < 0 or mutate_offs > len(code):
        raise SystemExit("unexpected code.flp layout; offsets do not fit")

    code[big_offs : big_offs + len(big_insn)] = big_insn
    code[mov_offs : mov_offs + len(mov_insn)] = mov_insn

    entrypoint = big_offs
    out_path.write_bytes(build_header(code, entrypoint) + code)
    print(f"wrote {out_path}")
    print(f"entrypoint = 0x{entrypoint:x}")
    print(f"password   = {PASSWORD.decode()}")


def main(argv: list[str]) -> None:
    if len(argv) not in (2, 3):
        print(f"usage: {argv[0]} code.flp [patched.flp]")
        raise SystemExit(1)
    in_path = Path(argv[1])
    out_path = Path(argv[2]) if len(argv) == 3 else Path("patched.flp")
    patch(in_path, out_path)


if __name__ == "__main__":
    main(sys.argv)
