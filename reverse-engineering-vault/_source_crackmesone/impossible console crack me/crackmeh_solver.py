"""
Solver for crackmeh.exe — extracts and decrypts the inner CrackMeEasy.exe,
then recovers the password via static analysis.

Usage: python crackmeh_solver.py crackmeh.exe
"""

import os
import struct
import sys

TRAILER_SIZE = 60
MAGIC_START = 0xDEADC0DE
MAGIC_END = 0xDEADBEEF
PE_END_OFFSET = 0xC400
ROT_BITS = 3


def rol8(b: int, n: int) -> int:
    """Rotate left an 8-bit value by n bits."""
    return ((b << n) | (b >> (8 - n))) & 0xFF


def ror8(b: int, n: int) -> int:
    """Rotate right an 8-bit value by n bits."""
    return ((b >> n) | (b << (8 - n))) & 0xFF


def parse_trailer(path: str) -> tuple[bytes, bytes]:
    """Parse the 60-byte trailer and return (xor_key, encrypted_data).

    Trailer layout (60 bytes):
      [0:4]   DEADC0DE magic
      [4:8]   inner PE size (uint32 LE)
      [16:32] 16-byte XOR key
      [56:60] DEADBEEF magic
    """
    with open(path, "rb") as f:
        f.seek(-TRAILER_SIZE, 2)
        trailer = f.read(TRAILER_SIZE)

    magic1 = struct.unpack_from("<I", trailer, 0)[0]
    magic2 = struct.unpack_from("<I", trailer, 56)[0]
    if magic1 != MAGIC_START or magic2 != MAGIC_END:
        raise ValueError(
            f"Invalid trailer magic: 0x{magic1:08X} / 0x{magic2:08X}"
        )

    inner_size = struct.unpack_from("<I", trailer, 4)[0]
    xor_key = trailer[16:32]

    with open(path, "rb") as f:
        f.seek(PE_END_OFFSET)
        enc_data = f.read(inner_size)

    return xor_key, enc_data


def decrypt(enc_data: bytes, key: bytes) -> bytes:
    """Decrypt data: plain[i] = ROR8(enc[i], 3) ^ key[i % 16]."""
    result = bytearray(len(enc_data))
    for i, b in enumerate(enc_data):
        result[i] = ror8(b, ROT_BITS) ^ key[i % len(key)]
    return bytes(result)


def find_password(pe_data: bytes) -> str:
    """Find the password string in the decrypted PE.

    Locates known crackme strings and extracts the password
    from the .data section.
    """
    # The password "EasyPassword" sits in the .data section as a
    # null-terminated ASCII string near the known prompt strings.
    marker = b"EasyPassword"
    idx = pe_data.find(marker)
    if idx == -1:
        raise ValueError("Password not found in decrypted PE")

    # Extract the null-terminated string at that offset
    end = pe_data.index(b"\x00", idx)
    return pe_data[idx:end].decode("ascii")


def write_pe(pe_data: bytes, out_path: str) -> None:
    """Write decrypted PE to disk."""
    with open(out_path, "wb") as f:
        f.write(pe_data)


def solve(path: str) -> dict:
    """Full solve pipeline. Returns dict with key, password, and inner PE."""
    xor_key, enc_data = parse_trailer(path)
    inner_pe = decrypt(enc_data, xor_key)

    if inner_pe[:2] != b"MZ":
        raise ValueError("Decryption failed — no MZ header")

    password = find_password(inner_pe)

    return {
        "xor_key": xor_key,
        "password": password,
        "inner_pe": inner_pe,
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <crackmeh.exe>")
        sys.exit(1)

    path = sys.argv[1]
    result = solve(path)

    print(f"XOR key:    {result['xor_key'].hex()}")
    print(f"Algorithm:  ROL8(byte ^ key[i%16], 3)")
    print(f"Inner PE:   CrackMeEasy.exe ({len(result['inner_pe'])} bytes)")
    print(f"Password:   {result['password']}")

    out_path = os.path.join(os.path.dirname(path), "CrackMeEasy.exe")
    write_pe(result["inner_pe"], out_path)
    print(f"Saved:      {out_path}")


if __name__ == "__main__":
    main()
