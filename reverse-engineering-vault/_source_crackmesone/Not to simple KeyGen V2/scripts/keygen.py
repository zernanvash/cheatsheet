#!/usr/bin/env python3
import argparse
import struct
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API.*") # avoid spam on filter test run

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL, UC_HOOK_CODE
    from unicorn.x86_const import (
        UC_X86_REG_RAX,
        UC_X86_REG_RDI,
        UC_X86_REG_RDX,
        UC_X86_REG_RIP,
        UC_X86_REG_RSI,
        UC_X86_REG_RSP,
        UC_X86_REG_FS_BASE,
    )
except Exception as exc:  # ! testing on laptop - dep guard
    raise SystemExit(f"Unicorn is required for offline keygen: {exc}")


LOOP_INDEXES = [0, 3, 6, 9, 12, 15]


def s8(x: int) -> int:
    return x - 256 if x >= 128 else x


def escape_bytes(bs: bytes) -> str:
    out = []
    for b in bs:
        if 32 <= b <= 126 and b != 0x5C:
            out.append(chr(b))
        else:
            out.append(f"\\x{b:02x}")
    return "".join(out)


def serial_value(serial: bytearray, idx: int) -> int:
    if idx == 16:
        return 0
    return s8(serial[idx])


def cond1_is_true(serial: bytearray, i: int) -> bool:
    a = serial_value(serial, i)
    b = serial_value(serial, (i + 1) % 17)
    c = serial_value(serial, (i + 2) % 17)
    return (a + b) == (c << 3)


def force_cond1_false(serial: bytearray, i: int, locked_index: int) -> bool:
    if not cond1_is_true(serial, i):
        return True

    tune_positions = [i, (i + 1) % 17, (i + 2) % 17]
    trial_values = [0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x61, 0x62]

    for pos in tune_positions:
        if pos == 16 or pos == locked_index:
            continue
        old = serial[pos]
        for tv in trial_values:
            if tv in (0x00, 0x0A):
                continue
            serial[pos] = tv
            if not cond1_is_true(serial, i):
                return True
        serial[pos] = old
    return False


class Hash401d80Emu:
    # static addrs
    FUNC_ADDR = 0x401D80
    MALLOC_ADDR = 0x41B7D0
    STACK_FAIL_ADDR = 0x44CDA0

    IMAGE_BASE = 0x400000
    STACK_BASE = 0x70000000
    STACK_SIZE = 0x200000
    HEAP_BASE = 0x60000000
    HEAP_SIZE = 0x400000
    FS_BASE = 0x71000000
    RET_ADDR = 0x72000000

    INPUT_ADDR = HEAP_BASE + 0x200000
    HEAP_START = HEAP_BASE + 0x1000

    def __init__(self, binary_path: str) -> None:
        self.binary_path = binary_path
        data = bytearray(Path(binary_path).read_bytes())
        self._patch_endbr64(data)

        image_size = (len(data) + 0xFFF) & ~0xFFF
        self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        self.mu.mem_map(self.IMAGE_BASE, image_size, UC_PROT_ALL)
        self.mu.mem_write(self.IMAGE_BASE, bytes(data) + b"\x00" * (image_size - len(data)))

        self.mu.mem_map(self.STACK_BASE, self.STACK_SIZE, UC_PROT_ALL)
        self.mu.mem_map(self.HEAP_BASE, self.HEAP_SIZE, UC_PROT_ALL)
        self.mu.mem_map(self.FS_BASE, 0x1000, UC_PROT_ALL)
        self.mu.mem_map(self.RET_ADDR & ~0xFFF, 0x1000, UC_PROT_ALL)
        self.mu.mem_write(self.RET_ADDR, b"\x90")

        # canary expected by the function prologue/epilogue
        self.mu.reg_write(UC_X86_REG_FS_BASE, self.FS_BASE)
        self.mu.mem_write(self.FS_BASE + 0x28, struct.pack("<Q", 0x1234567887654321))

        self.heap_ptr = self.HEAP_START
        self.mu.hook_add(UC_HOOK_CODE, self._code_hook)

    @staticmethod
    def _patch_endbr64(blob: bytearray) -> None:
        sig = b"\xF3\x0F\x1E\xFA"
        i = 0
        while True:
            i = blob.find(sig, i)
            if i < 0:
                break
            blob[i : i + 4] = b"\x90\x90\x90\x90"
            i += 4

    @staticmethod
    def _u64(raw: bytes) -> int:
        return struct.unpack("<Q", raw)[0]

    def _malloc(self, size: int) -> int:
        if size <= 0:
            size = 1
        ptr = (self.heap_ptr + 0xF) & ~0xF
        nxt = ptr + size
        if nxt >= self.HEAP_BASE + self.HEAP_SIZE:
            raise RuntimeError("emulator heap exhausted")
        self.heap_ptr = nxt
        return ptr

    def _code_hook(self, uc: Uc, address: int, _size: int, _user_data: object = None) -> None:
        if address == self.MALLOC_ADDR:
            sz = uc.reg_read(UC_X86_REG_RDI)
            ptr = self._malloc(sz)
            uc.reg_write(UC_X86_REG_RAX, ptr)
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = self._u64(bytes(uc.mem_read(rsp, 8)))
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RIP, ret)
            return

        if address == self.STACK_FAIL_ADDR:
            raise RuntimeError("stack canary check failed in emulator")

        if address == self.RET_ADDR:
            uc.emu_stop()

    def hash_401d80(self, msg: bytes) -> bytes:
        self.heap_ptr = self.HEAP_START

        if msg:
            self.mu.mem_write(self.INPUT_ADDR, msg)

        sp = self.STACK_BASE + self.STACK_SIZE - 0x100
        sp -= 8
        self.mu.mem_write(sp, struct.pack("<Q", self.RET_ADDR))

        self.mu.reg_write(UC_X86_REG_RSP, sp)
        self.mu.reg_write(UC_X86_REG_RDI, self.INPUT_ADDR)
        self.mu.reg_write(UC_X86_REG_RSI, len(msg))
        self.mu.reg_write(UC_X86_REG_RIP, self.FUNC_ADDR)

        self.mu.emu_start(self.FUNC_ADDR, self.RET_ADDR)

        out_ptr = self.mu.reg_read(UC_X86_REG_RAX)
        out_len = self.mu.reg_read(UC_X86_REG_RDX)
        return bytes(self.mu.mem_read(out_ptr, out_len))


def build_candidate_from_hash(hash_bytes: bytes) -> Optional[Tuple[int, bytes]]:
    candidates: List[Tuple[int, bytes]] = []

    for i in LOOP_INDEXES:
        target = s8(hash_bytes[i]) * 4
        if target < -128 or target > 127:
            continue

        target_b = target & 0xFF
        if target_b in (0x00, 0x0A):
            continue

        j = (i + 3) % 17
        if j == 16:
            continue

        serial = bytearray(b"A" * 16)
        serial[j] = target_b
        if not force_cond1_false(serial, i, j):
            continue
        if any(b in (0x00, 0x0A) for b in serial):
            continue

        # try to get better serials if more than one works
        printable_score = sum(32 <= b <= 126 for b in serial)
        candidates.append((printable_score, i, bytes(serial)))

    if not candidates:
        return None

    candidates.sort(key=lambda x: (-x[0], x[1]))
    _, idx, serial = candidates[0]
    return idx, serial


def main() -> int:
    parser = argparse.ArgumentParser(description=" keygen howo-not-to-simple-keygen")
    parser.add_argument("name", help="full name")
    parser.add_argument("email", help="email")
    parser.add_argument("--binary", default="./howo-not-to-simple-keygen", help="path to binary")
    args = parser.parse_args()

    emu = Hash401d80Emu(args.binary)

    h_name = emu.hash_401d80(args.name.encode("utf-8"))
    h_email = emu.hash_401d80(args.email.encode("utf-8"))
    h_mix = emu.hash_401d80(h_name + h_email)

    result = build_candidate_from_hash(h_mix)
    if result is None:
        print("no valid serial exists for this name/email pair")
        return 1

    idx, serial = result
    print(f"Chosen looop index: {idx}")
    print(f"Serial hex: {serial.hex()}")
    print(f"Serial escaped: {escape_bytes(serial)}")
    if all(32 <= b <= 126 for b in serial):
        print(f"Serial ascii: {serial.decode('ascii')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
