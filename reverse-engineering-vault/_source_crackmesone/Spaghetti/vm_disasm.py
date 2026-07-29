#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


BIN = Path("/Users/chris/Documents/Game/crackme-analysis/crackme.unpacked")
DATA_VA = 0x6040
DATA_FILE_OFF = 0x5040
CODE_OFF = 0x80


NAMES = {
    0x01: "push_i",
    0x02: "pick",
    0x03: "poke",
    0x04: "dup",
    0x05: "over",
    0x06: "dropn",
    0x07: "swap",
    0x08: "push_addr",
    0x10: "add",
    0x11: "sub",
    0x12: "mul",
    0x13: "div",
    0x14: "mod",
    0x15: "neg",
    0x16: "not_bits",
    0x17: "not_bool",
    0x18: "inc",
    0x19: "dec",
    0x20: "and",
    0x21: "or",
    0x22: "xor",
    0x23: "shl",
    0x24: "shr_log",
    0x25: "shr_arith",
    0x30: "eq",
    0x31: "ne",
    0x32: "gt_s",
    0x33: "ge_s",
    0x34: "lt_s",
    0x35: "le_s",
    0x36: "lt_u",
    0x37: "ge_u",
    0x38: "lt_f?",
    0x39: "ge_f?",
    0x50: "skip_if_true",
    0x51: "skip_if_false",
    0x53: "jmp",
    0x54: "br_table?",
    0x55: "call_ind?",
    0x56: "call",
    0x57: "ret",
    0x5A: "halt",
    0x5B: "nop",
    0x5C: "nop2",
    0x5D: "trap",
    0x5F: "jmp_if_true",
    0x60: "load32",
    0x61: "store32",
    0x62: "load32_idx",
    0x63: "store32_idx",
    0x64: "memop",
    0x65: "free?",
    0x66: "alloca?",
    0x70: "host_read",
    0x71: "host_write",
}


def uleb(data: bytes, pc: int) -> tuple[int, int]:
    shift = 0
    out = 0
    while True:
        b = data[pc]
        pc += 1
        out |= (b & 0x7F) << shift
        if b < 0x80:
            return out, pc
        shift += 7


def sleb(data: bytes, pc: int) -> tuple[int, int]:
    shift = 0
    out = 0
    while True:
        b = data[pc]
        pc += 1
        out |= (b & 0x7F) << shift
        shift += 7
        if b < 0x80 or shift == 35:
            if b & 0x40:
                out |= -1 << shift
            return out & 0xFFFFFFFF, pc


def signed32(x: int) -> int:
    x &= 0xFFFFFFFF
    return x - 0x100000000 if x & 0x80000000 else x


def decode(data: bytes, pc: int) -> tuple[int, str, list[int], int]:
    start = pc
    op = data[pc]
    pc += 1
    args: list[int] = []
    if op in (0x02, 0x03, 0x06, 0x08, 0x54, 0x56):
        v, pc = uleb(data, pc)
        args.append(v)
    elif op in (0x01, 0x53, 0x5F):
        v, pc = sleb(data, pc)
        args.append(signed32(v))
    elif 0x40 <= op <= 0x4F and (op & 1):
        v, pc = uleb(data, pc)
        args.append(v)
    elif op == 0x64:
        args.append(data[pc])
        pc += 1
    name = NAMES.get(op, f"op_{op:02x}")
    if 0x80 <= op <= 0x9F:
        name = "push_small"
        args = [op - 0x90]
    elif 0xA0 <= op <= 0xAF:
        name = "pick_small"
        args = [op - 0xA0]
    elif 0xB0 <= op <= 0xBF:
        name = "poke_small"
        args = [op - 0xB0]
    elif 0xC0 <= op <= 0xCF:
        name = "drop_small"
        args = [op - 0xBF]
    elif 0x40 <= op <= 0x4F:
        name = "enter/call"
        args.insert(0, (op >> 1) & 7)
    return op, name, args, pc


def main() -> None:
    raw = BIN.read_bytes()
    blob_len = int.from_bytes(raw[DATA_FILE_OFF + 0x8 : DATA_FILE_OFF + 0xC], "little")
    entry = int.from_bytes(raw[DATA_FILE_OFF + 0xC : DATA_FILE_OFF + 0x10], "little")
    code = raw[DATA_FILE_OFF + CODE_OFF : DATA_FILE_OFF + CODE_OFF + blob_len]
    start = int(sys.argv[1], 0) if len(sys.argv) > 1 else entry
    count = int(sys.argv[2], 0) if len(sys.argv) > 2 else 200
    pc = start
    for _ in range(count):
        old = pc
        op, name, args, pc = decode(code, pc)
        b = code[old:pc].hex(" ")
        extra = ""
        if name in ("jmp", "jmp_if_true"):
            extra = f" -> {pc + args[0]:06x}"
        if name == "host_write":
            extra = " ; write(pop2, pop1)"
        if name == "host_read":
            extra = " ; read(pop1)"
        print(f"{old:06x}: {b:<18} {name:<14} {', '.join(map(str,args))}{extra}")


if __name__ == "__main__":
    main()
