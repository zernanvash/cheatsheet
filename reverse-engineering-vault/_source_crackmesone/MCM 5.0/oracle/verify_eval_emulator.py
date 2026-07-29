#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass


MASK32 = 0xFFFFFFFF


def u32(x: int) -> int:
    return x & MASK32


def i32(x: int) -> int:
    x &= MASK32
    return x if x < 0x80000000 else x - 0x100000000


def sar32(x: int, sh: int) -> int:
    return u32(i32(x) >> (sh & 31))


INIT_DWORDS = [
    0xE41697A5,
    0xA2D0F306,
    0x8ACBD0A5,
    0xA5DDF10D,
    0xB743DBAB,
    0xA362EC59,
    0xD1B99AE2,
    0xA464EA4A,
]


def init_blob() -> bytearray:
    out = bytearray()
    for d in INIT_DWORDS:
        out.extend(d.to_bytes(4, "little"))
    return out


TABLE_14000F7F0 = bytes.fromhex(
    # 64 bytes at VA 0x14000f7f0 (file paddr 0x0000ebf0)
    "a5925ba8afe84ecfbbed5dabd7fe43c8"
    "b5e655a2b7e54bc3a2f44da4164b0796"
    "d38e45e881389c22417fdb6d05b217ad"
    "c8f654ff7f21a4333969e578f0aa26bc"
)


assert len(TABLE_14000F7F0) == 64


@dataclass
class EvalState:
    vm_ret: int
    mix_word: int
    total_sum: int
    eval_value: int


def vm_14001e870(bytecode: bytes, byte_65640: int = 0x0C, slow_xor: bool = False) -> int:
    regs = [0] * 0x21  # param_2[0..0x20]
    state = 0x4521
    steps = 0x2000
    u14 = 0
    dst = 0
    op = 0
    rs = 0
    rt = 0
    fl = 0

    while True:
        if steps == 0: # ok | non ok
            break

        if state < 0x7789:
            if state == 0x7788:
                sign = ((u14 >> 31) & 1) * 0x100000
                imm = (((u14 >> 11) & 0xFFC00) | (u14 & 0x100000)) >> 9
                imm |= (u14 & 0xFF000)
                imm |= sign
                imm = u32(imm | (0xFFE00000 if sign else 0))
                if dst != 0:
                    regs[dst] = u32(regs[0x20] + 4)
                regs[0x20] = u32(regs[0x20] + imm)

            elif state == 0x1122:
                imm = sar32(u14, 20)
                a = regs[rs]
                if op == 0:
                    v = u32((a | imm) * 2 - (a ^ imm))
                elif op == 4:
                    v = u32((a | imm) - (a & imm))
                elif op == 6:
                    v = u32((a - (a & imm)) + imm)
                elif op == 7: # inv 6 where | -> &
                    v = u32((a - (a | imm)) + imm)
                elif op == 1:
                    v = u32(a << (imm & 31))
                elif op == 5:
                    v = sar32(a, imm & 31) if (fl & 0x20) else u32(a >> (imm & 31))
                else:
                    v = 0
                if dst != 0:
                    regs[dst] = u32(v)
                regs[0x20] = u32(regs[0x20] + 4)

            elif state == 0x3344:
                a = regs[rs]
                b = regs[rt]
                if op == 0:
                    if (fl & 0x20) == 0:
                        v = u32((b | a) * 2 - (b ^ a))
                    else:
                        b2 = u32((~b | 1) * 2 - (~b ^ 1))
                        v = u32((b2 | a) * 2 - (b2 ^ a))
                elif op == 1:
                    v = u32(a << (b & 31))
                elif op == 2:
                    v = 1 if i32(a) < i32(b) else 0
                elif op == 3:
                    v = 1 if a < b else 0
                elif op == 4:
                    v = u32((b | a) - (b & a))
                elif op == 5:
                    v = sar32(a, b & 31) if (fl & 0x20) else u32(a >> (b & 31))
                elif op == 6:
                    v = u32((b - (b & a)) + a)
                elif op == 7:
                    v = u32((b - (b | a)) + a)
                else:
                    v = 0
                if dst != 0:
                    regs[dst] = u32(v)
                regs[0x20] = u32(regs[0x20] + 4)

            else:
                if state == 0x4521:
                    ip = regs[0x20]
                    if ip + 4 <= len(bytecode):
                        u14 = int.from_bytes(bytecode[ip:ip + 4], "little")
                        state = 0x89AB
                    else:
                        state = 0xFFFF
                elif state == 0x5566:
                    sign = ((u14 >> 31) & 1) * 0x1000
                    imm = (((u14 >> 13) & 0x3F000) | (u14 & 0xF00)) >> 7
                    imm |= ((u14 & 0x80) << 4)
                    imm |= sign
                    imm = u32(imm | (0xFFFFE000 if sign else 0))
                    a = regs[rs]
                    b = regs[rt]
                    if op == 0:
                        take = (a == b)
                    elif op == 1:
                        take = (a != b)
                    elif op == 4:
                        take = (i32(a) < i32(b))
                    elif op == 5:
                        take = (i32(b) <= i32(a))
                    elif op == 6:
                        take = (a < b)
                    elif op == 7:
                        take = (b <= a)
                    else:
                        take = False
                    regs[0x20] = u32(regs[0x20] + (imm if take else 4))
                else:
                    # invalid state -> return path
                    break

                # shared transition for 0x4521 / 0x5566 path
                steps -= 1
                continue

            state = 0x4521

        else:
            if state != 0x89AB:
                if state == 0x99AA:
                    imm = sar32(u14, 20)
                    if not ((op == 0) and (imm <= 1)):
                        regs[0x20] = u32(regs[0x20] + 4)
                        state = 0x4521
                        steps -= 1
                        continue
                break

            opcode = ((u14 & 0xFF) ^ byte_65640) & 0xFF
            dst = (u14 >> 7) & 0x1F
            fl = (u14 >> 25) & 0x7F
            op = (u14 >> 12) & 7
            rs = (u14 >> 15) & 0x1F
            rt = (u14 >> 20) & 0x1F

            op_u = opcode - 0x10
            if 0 <= op_u < 0x40 and ((0x8000000000040001 >> op_u) & 1):
                state = 0x1122
            elif opcode in (0x9A, 0x55, 0xAA):
                state = 0x3344
            elif opcode in (0xB2, 0x66):
                state = 0x5566
            elif opcode in (0xE5, 0x77):
                state = 0x7788
            elif opcode in (0x1C, 0x88, 0x99):
                state = 0x99AA
            else:
                state = 0xFFFF

            steps -= 1
            continue

        steps -= 1

    if slow_xor:
        regs[10] ^= 0xDEADBEEF
        regs[11] ^= 0x1337C0DE
    return u32(regs[10])


def compute_eval(password: bytes, p3: int, p4: int, slow_xor: bool = False) -> EvalState:
    if len(password) == 0:
        raise ValueError("password must not be empty")

    # stage1 mutate 32-byte blob with password + p3/p4 streams
    bc = init_blob()
    plen = len(password)
    for i in range(len(bc)):
        sh = (i & 7) * 8
        x = (p3 >> sh) & 0xFF
        x ^= password[i % plen]
        x ^= (p4 >> sh) & 0xFF
        bc[i] ^= x

    vm_ret = vm_14001e870(bytes(bc), byte_65640=0x0C, slow_xor=slow_xor)

    # stag2 hash password bytes
    h = 0
    for b in password:
        h = u32((h * 0x21) + b)
    h = u32((h ^ vm_ret) * u32(-0x61C88647))
    h = u32((h | 0x31415926) - (h & 0x31415926))
    mix = u32((h | 0x27182818) * 2 - (h ^ 0x27182818))
    b0 = mix & 0xFF
    b1 = (mix >> 8) & 0xFF
    b2 = (mix >> 16) & 0xFF
    b3 = (mix >> 24) & 0xFF

    # stage3 build 64-byte block from first 64 password bytes
    if len(password) < 64:
        raise ValueError("password must be >= 64 bytes for  eval")
    arr = [0] * 64
    for base in (0, 16, 32, 48):
        arr[base + 0] = TABLE_14000F7F0[base + 0] ^ password[base + 0] ^ b0
        arr[base + 1] = TABLE_14000F7F0[base + 1] ^ password[base + 1] ^ b1
        arr[base + 2] = TABLE_14000F7F0[base + 2] ^ password[base + 2] ^ b2
        arr[base + 3] = TABLE_14000F7F0[base + 3] ^ password[base + 3] ^ b3
        arr[base + 4] = TABLE_14000F7F0[base + 4] ^ password[base + 4] ^ b0
        arr[base + 5] = TABLE_14000F7F0[base + 5] ^ password[base + 5] ^ b1
        arr[base + 6] = TABLE_14000F7F0[base + 6] ^ password[base + 6] ^ b2
        arr[base + 7] = TABLE_14000F7F0[base + 7] ^ password[base + 7] ^ b3
        arr[base + 8] = TABLE_14000F7F0[base + 8] ^ password[base + 8] ^ b0
        arr[base + 9] = TABLE_14000F7F0[base + 9] ^ password[base + 9] ^ b1
        arr[base + 10] = TABLE_14000F7F0[base + 10] ^ password[base + 10] ^ b2
        arr[base + 11] = TABLE_14000F7F0[base + 11] ^ password[base + 11] ^ b3
        arr[base + 12] = TABLE_14000F7F0[base + 12] ^ password[base + 12] ^ b0
        arr[base + 13] = TABLE_14000F7F0[base + 13] ^ password[base + 13] ^ b1
        arr[base + 14] = TABLE_14000F7F0[base + 14] ^ password[base + 14] ^ b2
        arr[base + 15] = TABLE_14000F7F0[base + 15] ^ password[base + 15] ^ b3

    total = sum(x & 0xFF for x in arr)
    ev = total ^ 0x18FC
    return EvalState(vm_ret=vm_ret, mix_word=mix, total_sum=total, eval_value=ev)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("password", help="ascii password")
    ap.add_argument("--p3", default="1e8670be7c6a5450")
    ap.add_argument("--p4", default="b3e192f8a4d5c6b7")
    ap.add_argument("--slow-xor", action="store_true") # test
    args = ap.parse_args()

    pw = args.password.encode("latin1", "ignore")
    st = compute_eval(pw, int(args.p3, 16), int(args.p4, 16), slow_xor=args.slow_xor)
    print(f"len={len(pw)} vm_ret=0x{st.vm_ret:08x} mix=0x{st.mix_word:08x} sum={st.total_sum} eval=0x{st.eval_value:08x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
