import sys
from typing import List, Tuple

DATA_HEX = "4f000000d000000051010000d201000053020000d402000055030000d603000057000000d800000059010000da0100005b020000dc0200005d030000de0300005f000000e000000061010000e201000063020000e402000065030000e603000067000000e800000069010000ea0100006b020000ec0200006d030000ee0300006f000000f000000071010000f201000073020000f402000075030000f603000077000000f800000079010000fa0100007b020000fc0200007d030000fe0300007f000000000100008101000002020000830200000403000085030000060000008700000008010000890100000a0200008b0200000c0300008d0300000e000000"
# DAT_140035310 (from FUN_140001000)
BLOB_HEX = "48d9ed8a1dff9a7bb0d1e57c15f7927388e9ddbb2dcfaa4b80e1d5b325c7a243" #
# child mask (anti-debug constant XOR parent-forced RAX value)
MASK = 0xB3E192F8A4D5C6B7 ^ 0x9F2D38B17C6A4E5F


def build_matrices(inp: bytes) -> Tuple[List[int], List[int]]: # high
    # 4096 x uint10 generated from fixed LCG
    high = [0] * 4096
    u = 0xDEADBEEF
    idx = 0
    for _ in range(0x40):
        for _ in range(4):
            for _ in range(16):
                u = (u * 0x19660D + 0x3C6EF35F) & 0xFFFFFFFF
                high[idx] = u & 0x3FF
                idx += 1

    # low matrix: 4 rows x 16 columns loaded from password bytes
    low = [0] * 64
    for row in range(4):
        for col in range(16):
            ix = row * 16 + col
            low[ix] = inp[ix] if ix < len(inp) else 0

    return high, low


def gen_key(inp: bytes) -> List[int]:
    high, low = build_matrices(inp)
    data = bytes.fromhex(DATA_HEX)
    key = []

    for n in range(64):
        edx = 0
        for j in range(4):
            start1 = (n * 4 + j) * 16
            start2 = j * 16
            dot = 0
            for k in range(16):
                dot = (dot + (high[start1 + k] * low[start2 + k])) & 0xFFFFFFFF
            edx = (edx + dot) & 0x3FF
        source_byte = data[n * 4]
        key.append((source_byte - (edx & 0xFF)) & 0xFF)

    return key


def decode_blob(key: List[int]) -> bytes:
    blob = bytes.fromhex(BLOB_HEX)
    mask_bytes = MASK.to_bytes(8, "little")
    out = bytearray()
    for i, b in enumerate(blob):
        out.append(b ^ mask_bytes[i & 7] ^ key[i])
    return bytes(out)


def parse_instrs(decoded: bytes) -> List[Tuple[int, int, int, int]]:
    instrs = []
    ptr = 0
    # vm loader in main uses chunks of 11 bytes, starting at +0 effectively for first instruction
    while ptr + 11 <= len(decoded):
        op = decoded[ptr]
        r1 = decoded[ptr + 1]
        r2 = decoded[ptr + 2]
        imm = int.from_bytes(decoded[ptr + 3:ptr + 11], "little")
        instrs.append((op, r1, r2, imm))
        ptr += 11
        if len(instrs) >= 2:
            break
    return instrs


def main() -> None:
    if len(sys.argv) < 2:
        print("emulate_vm_key.py <password>")
        return

    pw = sys.argv[1].encode("latin-1")
    key = gen_key(pw)
    decoded = decode_blob(key)
    instrs = parse_instrs(decoded)

    print("password:", sys.argv[1])
    print("key[0:16]:", ''.join(f"{x:02x}" for x in key[:16]))
    print("decoded[0:32]:", decoded.hex()) #
    for i, (op, r1, r2, imm) in enumerate(instrs):
        print(f"ins[{i}] op=0x{op:02x} r1=0x{r1:02x} r2=0x{r2:02x} imm=0x{imm:016x}")


if __name__ == "__main__":
    main()
