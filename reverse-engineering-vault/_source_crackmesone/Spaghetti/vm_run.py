#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from vm_disasm import DATA_FILE_OFF, CODE_OFF, BIN, decode


MASK = 0xFFFFFFFF


def u32(x: int) -> int:
    return x & MASK


def s32(x: int) -> int:
    x &= MASK
    return x - 0x100000000 if x & 0x80000000 else x


def trunc_div(a: int, b: int) -> int:
    a = s32(a)
    b = s32(b)
    return int(a / b)


def trunc_mod(a: int, b: int) -> int:
    a = s32(a)
    b = s32(b)
    return a - trunc_div(a, b) * b


@dataclass
class Frame:
    ret: int
    stack_base: int
    local_top: int


class VM:
    def __init__(
        self,
        inp: bytes,
        trace: bool = False,
        events: list | None = None,
        flip_branch: int | None = None,
        sym_inputs: list | None = None,
        force_branch=None,
    ):
        raw = BIN.read_bytes()
        self.blob_len = int.from_bytes(raw[DATA_FILE_OFF + 0x8 : DATA_FILE_OFF + 0xC], "little")
        self.entry = int.from_bytes(raw[DATA_FILE_OFF + 0xC : DATA_FILE_OFF + 0x10], "little")
        self.code = raw[DATA_FILE_OFF + CODE_OFF : DATA_FILE_OFF + CODE_OFF + self.blob_len]
        self.pc = self.entry
        self.stack: list[int] = []
        self.frames: list[Frame] = [Frame(0xFFFFFFFF, 0, 0)]
        self.halted = False
        self.exit_code = 0
        self.inp = inp
        self.inpos = 0
        self.output = bytearray()
        self.trace = trace
        self.events = events
        self.flip_branch = flip_branch
        self.force_branch = force_branch
        self.branch_counter = 0
        self.steps = 0

        # VM memory pointers use the top byte as a segment id and the low
        # 24 bits as a byte offset. Segment 1 is the bytecode/data blob,
        # segment 3 is stack-local scratch, and segment 4 is heap scratch.
        self.mem3 = bytearray(0x40000 * 4)
        self.mem4 = bytearray(0x100000)
        self.heap4 = 0
        self.sym_inputs = sym_inputs
        self.sym_enabled = sym_inputs is not None
        self.sstack: list = []
        self.smem: dict[tuple[int, int], object] = {}
        self.last_sym = None
        self.last_read_sym = None

    def bv(self, x: int):
        if not self.sym_enabled:
            return None
        import z3

        return z3.BitVecVal(x & MASK, 32)

    def zext8(self, x):
        if x is None:
            return None
        import z3

        return z3.ZeroExt(24, x) if x.size() == 8 else x

    def push(self, x: int, sx=None) -> None:
        if len(self.stack) >= 2048:
            self.trap(1)
            return
        self.stack.append(u32(x))
        if self.sym_enabled:
            self.sstack.append(sx)

    def pop(self) -> int:
        if not self.stack:
            self.trap(2)
            self.last_sym = None
            return 0
        if self.sym_enabled:
            self.last_sym = self.sstack.pop()
        return self.stack.pop()

    def trap(self, code: int) -> None:
        self.exit_code = code
        self.halted = True

    def mem_bytes(self, seg: int) -> bytearray | bytes | None:
        if seg == 1:
            return self.code
        if seg == 3:
            return self.mem3
        if seg == 4:
            return self.mem4
        return None

    def read_word_index(self, ptr_word: int) -> int:
        seg = (ptr_word >> 24) & 0xFF
        idx = ptr_word & 0xFFFFFF
        mem = self.mem_bytes(seg)
        if mem is None:
            self.trap(10 if seg == 0 else 11)
            return 0
        off = idx * 4
        if off + 4 > len(mem):
            self.trap(10 if seg == 0 else 11)
            return 0
        self.last_read_sym = self.read_sym_bytes(seg, off, 4, False)
        return int.from_bytes(mem[off : off + 4], "little")

    def write_word_index(self, ptr_word: int, value: int, svalue=None) -> None:
        seg = (ptr_word >> 24) & 0xFF
        idx = ptr_word & 0xFFFFFF
        mem = self.mem_bytes(seg)
        if mem is None or seg == 1:
            self.trap(9 if seg == 1 else 11)
            return
        off = idx * 4
        if off + 4 > len(mem):
            self.trap(11)
            return
        mem[off : off + 4] = u32(value).to_bytes(4, "little")
        self.write_sym_bytes(seg, off, 4, svalue)

    def read_bytes_value(self, ptr: int, size: int, signed: bool) -> int:
        seg = (ptr >> 24) & 0xFF
        off = ptr & 0xFFFFFF
        mem = self.mem_bytes(seg)
        if mem is None or off + size > len(mem):
            self.trap(10 if seg == 0 else 11)
            return 0
        if size > 4:
            size = 4
        val = int.from_bytes(mem[off : off + size], "little", signed=False)
        self.last_read_sym = self.read_sym_bytes(seg, off, size, signed)
        if signed and size < 4 and val & (1 << (8 * size - 1)):
            val |= (-1 << (8 * size))
        return u32(val)

    def write_bytes_value(self, ptr: int, value: int, size: int, svalue=None) -> None:
        seg = (ptr >> 24) & 0xFF
        off = ptr & 0xFFFFFF
        mem = self.mem_bytes(seg)
        if mem is None or seg == 1 or off + size > len(mem):
            self.trap(9 if seg == 1 else 11)
            return
        if size > 4:
            size = 4
        mem[off : off + size] = u32(value).to_bytes(4, "little")[:size]
        self.write_sym_bytes(seg, off, size, svalue)

    def read_sym_bytes(self, seg: int, off: int, size: int, signed: bool):
        if not self.sym_enabled:
            return None
        import z3

        bs = [self.smem.get((seg, off + i)) for i in range(size)]
        if not any(b is not None for b in bs):
            return None
        concrete = self.mem_bytes(seg)
        filled = []
        for i, b in enumerate(bs):
            if b is None:
                b = z3.BitVecVal(concrete[off + i], 8)
            filled.append(b)
        val = filled[0] if len(filled) == 1 else z3.Concat(*reversed(filled))
        if size < 4:
            val = z3.SignExt(32 - size * 8, val) if signed else z3.ZeroExt(32 - size * 8, val)
        return val

    def write_sym_bytes(self, seg: int, off: int, size: int, svalue) -> None:
        if not self.sym_enabled:
            return
        import z3

        for i in range(size):
            key = (seg, off + i)
            if svalue is None:
                self.smem.pop(key, None)
            else:
                self.smem[key] = z3.Extract(8 * i + 7, 8 * i, svalue)

    def effective_addr(self, indexed: int, size: int) -> int:
        if not indexed:
            return self.pop()
        idx = self.pop()
        base = self.pop()
        return (base & 0xFF000000) | ((base + idx * size) & 0xFFFFFF)

    def skip_one(self) -> None:
        if self.pc >= len(self.code):
            return
        _op, _name, _args, new_pc = decode(self.code, self.pc)
        self.pc = new_pc

    def alloc4(self, count: int, size: int) -> int:
        total = count * size
        off = (self.heap4 + size - 1) & -size if size in (1, 2, 4, 8) else (self.heap4 + 3) & -4
        if off + total > len(self.mem4):
            self.trap(12)
            return 0
        self.heap4 = (off + total + 3) & -4
        return 0x04000000 | off

    def step(self) -> None:
        old_pc = self.pc
        op, name, args, self.pc = decode(self.code, self.pc)
        self.steps += 1
        if self.trace and (0x40 <= op <= 0x4F or op in (0x50, 0x51, 0x53, 0x56, 0x57, 0x5F, 0x70, 0x71) or self.steps < 30):
            top = self.stack[-5:]
            print(f"{old_pc:06x} {name} {args} sp={len(self.stack)} top={[hex(x) for x in top]}")

        if 0x80 <= op <= 0x9F:
            self.push(op - 0x90)
        elif 0xA0 <= op <= 0xAF:
            idx = op - 0xA0
            if idx >= len(self.stack):
                self.trap(2)
            else:
                self.push(self.stack[-1 - idx], self.sstack[-1 - idx] if self.sym_enabled else None)
        elif 0xB0 <= op <= 0xBF:
            idx = op - 0xB0
            val = self.pop()
            sval = self.last_sym
            if not self.halted:
                if idx >= len(self.stack):
                    self.trap(2)
                else:
                    self.stack[-1 - idx] = val
                    if self.sym_enabled:
                        self.sstack[-1 - idx] = sval
        elif 0xC0 <= op <= 0xCF:
            n = op - 0xBF
            if len(self.stack) < n:
                self.trap(2)
            else:
                del self.stack[-n:]
                if self.sym_enabled:
                    del self.sstack[-n:]
        elif op == 0x01:
            self.push(args[0])
        elif op == 0x02:
            idx = args[0]
            if idx >= len(self.stack):
                self.trap(2)
            else:
                self.push(self.stack[-1 - idx], self.sstack[-1 - idx] if self.sym_enabled else None)
        elif op == 0x03:
            idx = args[0]
            val = self.pop()
            sval = self.last_sym
            if not self.halted:
                if idx >= len(self.stack):
                    self.trap(2)
                else:
                    self.stack[-1 - idx] = val
                    if self.sym_enabled:
                        self.sstack[-1 - idx] = sval
        elif op == 0x04:
            if not self.stack:
                self.trap(2)
            else:
                self.push(self.stack[-1], self.sstack[-1] if self.sym_enabled else None)
        elif op == 0x05:
            if len(self.stack) <= 1:
                self.trap(2)
            else:
                self.push(self.stack[-2], self.sstack[-2] if self.sym_enabled else None)
        elif op == 0x06:
            n = args[0]
            if len(self.stack) < n:
                self.trap(2)
            else:
                del self.stack[-n:]
                if self.sym_enabled:
                    del self.sstack[-n:]
        elif op == 0x07:
            if len(self.stack) < 2:
                self.trap(2)
            else:
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
                if self.sym_enabled:
                    self.sstack[-1], self.sstack[-2] = self.sstack[-2], self.sstack[-1]
        elif op == 0x08:
            self.push(0x01000000 | args[0])
        elif op in (0x10, 0x11, 0x12, 0x13, 0x14, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39):
            b = self.pop()
            sb = self.last_sym
            a = self.pop()
            sa = self.last_sym
            if self.halted:
                return
            if op == 0x10:
                r = a + b
            elif op == 0x11:
                r = a - b
            elif op == 0x12:
                r = a * b
            elif op == 0x13:
                if b == 0:
                    self.trap(6); return
                r = trunc_div(a, b)
            elif op == 0x14:
                if b == 0:
                    self.trap(6); return
                r = trunc_mod(a, b)
            elif op == 0x20:
                r = a & b
            elif op == 0x21:
                r = a | b
            elif op == 0x22:
                r = a ^ b
            elif op == 0x23:
                r = a << (b & 31)
            elif op in (0x24, 0x25):
                r = (a & MASK) >> (b & 31)
            elif op == 0x30:
                r = int(s32(a) == s32(b))
            elif op == 0x31:
                r = int(s32(a) != s32(b))
            elif op == 0x32:
                r = int(s32(b) > s32(a))
            elif op == 0x33:
                r = int(s32(b) >= s32(a))
            elif op == 0x34:
                r = int(s32(b) < s32(a))
            elif op == 0x35:
                r = int(s32(b) <= s32(a))
            elif op == 0x36:
                r = int((a & MASK) < (b & MASK))
            elif op == 0x37:
                r = int((b & MASK) >= (a & MASK))
            elif op == 0x38:
                r = int((b & MASK) < (a & MASK))
            elif op == 0x39:
                r = int((a & MASK) >= (b & MASK))
            if self.events is not None and 0x30 <= op <= 0x39:
                self.events.append(("cmp", old_pc, op, a, b, u32(r), self.inpos, len(self.output)))
            sr = None
            if self.sym_enabled and (sa is not None or sb is not None):
                import z3
                za = sa if sa is not None else self.bv(a)
                zb = sb if sb is not None else self.bv(b)
                if op == 0x10:
                    sr = za + zb
                elif op == 0x11:
                    sr = za - zb
                elif op == 0x12:
                    sr = za * zb
                elif op == 0x13:
                    sr = za / zb
                elif op == 0x14:
                    sr = za % zb
                elif op == 0x20:
                    sr = za & zb
                elif op == 0x21:
                    sr = za | zb
                elif op == 0x22:
                    sr = za ^ zb
                elif op == 0x23:
                    sr = za << (zb & self.bv(31))
                elif op in (0x24, 0x25):
                    sr = z3.LShR(za, zb & self.bv(31))
                elif op == 0x30:
                    sr = z3.If(za == zb, self.bv(1), self.bv(0))
                elif op == 0x31:
                    sr = z3.If(za != zb, self.bv(1), self.bv(0))
                elif op == 0x32:
                    sr = z3.If(zb > za, self.bv(1), self.bv(0))
                elif op == 0x33:
                    sr = z3.If(zb >= za, self.bv(1), self.bv(0))
                elif op == 0x34:
                    sr = z3.If(zb < za, self.bv(1), self.bv(0))
                elif op == 0x35:
                    sr = z3.If(zb <= za, self.bv(1), self.bv(0))
                elif op == 0x36:
                    sr = z3.If(z3.ULT(za, zb), self.bv(1), self.bv(0))
                elif op == 0x37:
                    sr = z3.If(z3.UGE(zb, za), self.bv(1), self.bv(0))
                elif op == 0x38:
                    sr = z3.If(z3.ULT(zb, za), self.bv(1), self.bv(0))
                elif op == 0x39:
                    sr = z3.If(z3.UGE(za, zb), self.bv(1), self.bv(0))
            self.push(r, sr)
        elif op == 0x15:
            v = self.pop(); sv = self.last_sym
            self.push(-v, -sv if self.sym_enabled and sv is not None else None)
        elif op == 0x16:
            v = self.pop(); sv = self.last_sym
            self.push(~v, ~sv if self.sym_enabled and sv is not None else None)
        elif op == 0x17:
            v = self.pop(); sv = self.last_sym
            sr = None
            if self.sym_enabled and sv is not None:
                import z3
                sr = z3.If(sv == self.bv(0), self.bv(1), self.bv(0))
            self.push(int(v == 0), sr)
        elif op == 0x18:
            v = self.pop(); sv = self.last_sym
            self.push(v + 1, sv + self.bv(1) if self.sym_enabled and sv is not None else None)
        elif op == 0x19:
            v = self.pop(); sv = self.last_sym
            self.push(v - 1, sv - self.bv(1) if self.sym_enabled and sv is not None else None)
        elif 0x40 <= op <= 0x4F:
            target = ((op >> 1) & 7) | ((args[-1] * 8) if (op & 1) else 0)
            if len(self.frames) >= 256:
                self.trap(3)
            else:
                self.frames.append(Frame(self.pc, 0, self.frames[-1].local_top if self.frames else 0))
                self.pc = target
        elif op == 0x50:
            cond = self.pop()
            taken = cond != 0 and not self.halted
            branch_id = self.branch_counter
            self.branch_counter += 1
            if self.flip_branch == branch_id:
                taken = not taken
            if self.force_branch is not None:
                forced = self.force_branch(self, old_pc, op, cond, taken, branch_id)
                if forced is not None:
                    taken = bool(forced)
            if self.events is not None:
                self.events.append(("branch", old_pc, op, cond, int(taken), self.inpos, len(self.output), self.pc, branch_id))
            if taken:
                self.skip_one()
        elif op == 0x51:
            cond = self.pop()
            taken = cond == 0 and not self.halted
            branch_id = self.branch_counter
            self.branch_counter += 1
            if self.flip_branch == branch_id:
                taken = not taken
            if self.force_branch is not None:
                forced = self.force_branch(self, old_pc, op, cond, taken, branch_id)
                if forced is not None:
                    taken = bool(forced)
            if self.events is not None:
                self.events.append(("branch", old_pc, op, cond, int(taken), self.inpos, len(self.output), self.pc, branch_id))
            if taken:
                self.skip_one()
        elif op == 0x53:
            self.pc = self.pc + args[0]
        elif op == 0x55:
            target = self.pop() & 0xFFFFFF
            if not self.halted:
                self.frames.append(Frame(self.pc, 0, self.frames[-1].local_top))
                self.pc = target
        elif op == 0x56:
            n = args[0]
            if len(self.stack) < n:
                self.trap(2)
            elif self.frames:
                self.frames[-1].stack_base = len(self.stack) - n
                self.frames[-1].local_top = self.frames[-1].local_top
        elif op == 0x57:
            if not self.frames:
                self.trap(4)
            else:
                fr = self.frames.pop()
                self.stack = self.stack[: fr.stack_base]
                if self.sym_enabled:
                    self.sstack = self.sstack[: fr.stack_base]
                if fr.ret == 0xFFFFFFFF:
                    self.halted = True
                    self.exit_code = 1
                else:
                    if self.frames:
                        self.frames[-1].local_top = fr.local_top
                    self.pc = fr.ret
        elif op == 0x5A:
            self.halted = True
            self.exit_code = 1
        elif op in (0x5B, 0x5C):
            pass
        elif op == 0x5D:
            self.trap(7)
        elif op == 0x5F:
            target = self.pc + args[0]
            cond = self.stack[-1] if self.stack else 0
            taken = bool(self.stack and self.stack[-1] != 0)
            branch_id = self.branch_counter
            self.branch_counter += 1
            if self.flip_branch == branch_id:
                taken = not taken
            if self.force_branch is not None:
                forced = self.force_branch(self, old_pc, op, cond, taken, branch_id)
                if forced is not None:
                    taken = bool(forced)
            if self.events is not None:
                self.events.append(("branch", old_pc, op, cond, int(taken), self.inpos, len(self.output), target, branch_id))
            if taken:
                self.pc = target
            else:
                self.pop()
        elif op == 0x60:
            ptr = self.pop()
            val = self.read_word_index(ptr)
            self.push(val, self.last_read_sym)
        elif op == 0x61:
            value = self.pop()
            svalue = self.last_sym
            ptr = self.pop()
            if not self.halted:
                self.write_word_index(ptr, value, svalue)
        elif op == 0x62:
            idx = self.pop()
            ptr = self.pop()
            val = self.read_word_index((ptr & 0xFF000000) | ((ptr + 4 * idx) & 0xFFFFFF))
            self.push(val, self.last_read_sym)
        elif op == 0x63:
            value = self.pop()
            svalue = self.last_sym
            idx = self.pop()
            ptr = self.pop()
            if not self.halted:
                self.write_word_index((ptr & 0xFF000000) | ((ptr + 4 * idx) & 0xFFFFFF), value, svalue)
        elif op == 0x64:
            sub = args[0]
            sizes = {1: 1, 2: 2, 3: 4, 4: 8}
            size = sizes.get((sub & 7), 4)
            if sub == 0x18:
                _ptr = self.pop()
            elif sub & 8:
                count = self.pop()
                if not self.halted:
                    self.push(self.alloc4(count, size))
            else:
                indexed = sub >> 7
                if sub & 0x40:
                    value = self.pop()
                    svalue = self.last_sym
                    ptr = self.effective_addr(indexed, size)
                    if not self.halted:
                        self.write_bytes_value(ptr, value, size, svalue)
                else:
                    ptr = self.effective_addr(indexed, size)
                    if not self.halted:
                        if sub & 0x10:
                            self.push(ptr)
                        else:
                            val = self.read_bytes_value(ptr, size, bool(sub & 0x20))
                            self.push(val, self.last_read_sym)
        elif op == 0x65:
            _ptr = self.pop()
        elif op == 0x66:
            size = self.pop()
            if not self.halted:
                fr = self.frames[-1]
                old = fr.local_top
                new = old + ((size + 3) & 0xFFFFFFFC)
                if new > len(self.mem3):
                    self.trap(12)
                else:
                    fr.local_top = new
                    self.push(0x03000000 | old)
        elif op == 0x70:
            mode = self.pop()
            ch = 0
            sx = None
            if mode == 1:
                if self.inpos < len(self.inp):
                    read_pos = self.inpos
                    ch = self.inp[self.inpos]
                    self.inpos += 1
                    if self.sym_enabled and read_pos < len(self.sym_inputs):
                        sx = self.zext8(self.sym_inputs[read_pos])
            if self.events is not None:
                self.events.append(("read", old_pc, mode, ch, self.inpos, len(self.output)))
            self.push(ch, sx)
        elif op == 0x71:
            val = self.pop()
            mode = self.pop()
            if mode == 2:
                self.output.append(val & 0xFF)
                if self.events is not None:
                    self.events.append(("write", old_pc, val & 0xFF, self.inpos, len(self.output)))
        else:
            self.trap(5)

    def run(self, max_steps: int = 10_000_000) -> bytes:
        while not self.halted and self.steps < max_steps:
            self.step()
        if self.steps >= max_steps:
            raise RuntimeError("step limit exceeded")
        return bytes(self.output)


def main() -> None:
    inp = (sys.argv[1] if len(sys.argv) > 1 else "").encode() + b"\n"
    vm = VM(inp, trace="--trace" in sys.argv)
    out = vm.run()
    sys.stdout.buffer.write(out)
    sys.stderr.write(f"\nsteps={vm.steps} exit={vm.exit_code} inpos={vm.inpos} sp={len(vm.stack)} frames={len(vm.frames)}\n")


if __name__ == "__main__":
    main()
