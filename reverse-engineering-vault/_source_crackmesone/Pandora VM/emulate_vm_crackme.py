import struct

import pefile
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from unicorn import (
    UC_ARCH_X86,
    UC_HOOK_CODE,
    UC_HOOK_MEM_READ,
    UC_HOOK_MEM_WRITE,
    UC_MEM_WRITE,
    UC_MODE_64,
    UC_PROT_ALL,
    Uc,
    UcError,
)
from unicorn.x86_const import *


BASE = 0x140000000
EXE = "vm_crackme.exe"
PAGE = 0x1000
STACK = 0x700000000000
STACK_SIZE = 0x400000
FAKE = 0x180000000
HOOK_PRINT = 0x140001000


def align_up(value):
    return (value + PAGE - 1) & ~(PAGE - 1)


def read_cstr(uc, addr, limit=4096):
    data = []
    for i in range(limit):
        b = uc.mem_read(addr + i, 1)[0]
        if b == 0:
            break
        data.append(b)
    return bytes(data).decode("utf-8", "replace")


pe = pefile.PE(EXE)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

imports = []
if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
    idx = 0
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode(errors="ignore")
        for imp in entry.imports:
            name = (imp.name or b"").decode(errors="ignore")
            imports.append((imp.address, FAKE + idx * 0x100, dll, name))
            idx += 1

fake_by_addr = {fake: (iat, dll, name) for iat, fake, dll, name in imports}

branch_insns = {}
cpuid_insns = set()
xgetbv_insns = set()
for sec in pe.sections:
    if not (sec.Characteristics & 0x20000000):
        continue
    start = BASE + sec.VirtualAddress
    for ins in md.disasm(sec.get_data(), start):
        if ins.mnemonic.startswith("j") and ins.mnemonic != "jmp":
            branch_insns[ins.address] = (ins.mnemonic, ins.op_str)
        elif ins.mnemonic == "cpuid":
            cpuid_insns.add(ins.address)
        elif ins.mnemonic == "xgetbv":
            xgetbv_insns.add(ins.address)


class Stop(Exception):
    pass


def make_uc(import_overrides=None):
    import_overrides = import_overrides or {}
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(BASE, align_up(pe.OPTIONAL_HEADER.SizeOfImage), UC_PROT_ALL)
    with open(EXE, "rb") as f:
        image = f.read()
    uc.mem_write(BASE, image[: pe.OPTIONAL_HEADER.SizeOfHeaders])
    for sec in pe.sections:
        raw = sec.get_data()
        size = max(sec.Misc_VirtualSize, len(raw))
        uc.mem_write(BASE + sec.VirtualAddress, raw + b"\0" * (size - len(raw)))

    uc.mem_map(FAKE, align_up(len(imports) * 0x100 + PAGE), UC_PROT_ALL)
    for iat, fake, _dll, name in imports:
        uc.mem_write(iat, struct.pack("<Q", import_overrides.get(name, fake)))
        uc.mem_write(fake, b"\xC3")

    uc.mem_map(STACK - STACK_SIZE, STACK_SIZE, UC_PROT_ALL)
    rsp = STACK - 0x1000
    uc.reg_write(UC_X86_REG_RSP, rsp)
    uc.mem_write(rsp, struct.pack("<Q", 0))
    uc.reg_write(UC_X86_REG_RCX, 1)
    uc.reg_write(UC_X86_REG_RDX, 0)
    uc.reg_write(UC_X86_REG_R8, 0)
    uc.reg_write(UC_X86_REG_R9, 0)
    return uc


def ret_to(uc, value=0):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)
    uc.reg_write(UC_X86_REG_RAX, value & 0xFFFFFFFFFFFFFFFF)
    if ret == 0:
        raise Stop()
    uc.reg_write(UC_X86_REG_RIP, ret)


def run(
    input_num,
    max_insn=20_000_000,
    trace=False,
    branch_trace=False,
    watch_input=False,
    watch_stack=False,
    snapshot_addrs=None,
    trace_input_flow=False,
    patch_writes=None,
    cpuid_map=None,
    xcr0=None,
    import_overrides=None,
):
    uc = make_uc(import_overrides=import_overrides)
    output = []
    calls = []
    steps = [0]
    last_rips = []
    branches = []
    input_addr = [None]
    mem_events = []
    snapshots = []
    snapshot_addrs = set(snapshot_addrs or [])
    input_flow = []
    input_flow_active = [False]
    patch_writes = dict(patch_writes or {})
    pending_patches = []
    cpuid_map = dict(cpuid_map or {})

    def hook_code(uc, address, size, _user):
        if pending_patches:
            for patch_addr, patch_size, patched in pending_patches:
                uc.mem_write(patch_addr, patched.to_bytes(patch_size, "little"))
            pending_patches.clear()
        steps[0] += 1
        if len(last_rips) >= 32:
            last_rips.pop(0)
        last_rips.append(address)
        if steps[0] > max_insn:
            raise Stop()

        if address in cpuid_insns and cpuid_map:
            leaf = uc.reg_read(UC_X86_REG_EAX) & 0xFFFFFFFF
            subleaf = uc.reg_read(UC_X86_REG_ECX) & 0xFFFFFFFF
            eax, ebx, ecx, edx = cpuid_map.get((leaf, subleaf), cpuid_map.get((leaf, 0), (0, 0, 0, 0)))
            uc.reg_write(UC_X86_REG_EAX, eax)
            uc.reg_write(UC_X86_REG_EBX, ebx)
            uc.reg_write(UC_X86_REG_ECX, ecx)
            uc.reg_write(UC_X86_REG_EDX, edx)
            uc.reg_write(UC_X86_REG_RIP, address + size)
            return

        if address in xgetbv_insns and xcr0 is not None:
            value = xcr0 & 0xFFFFFFFFFFFFFFFF
            uc.reg_write(UC_X86_REG_EAX, value & 0xFFFFFFFF)
            uc.reg_write(UC_X86_REG_EDX, value >> 32)
            uc.reg_write(UC_X86_REG_RIP, address + size)
            return

        if address in snapshot_addrs:
            snapshots.append(
                (
                    steps[0],
                    address,
                    uc.reg_read(UC_X86_REG_RAX),
                    uc.reg_read(UC_X86_REG_RBX),
                    uc.reg_read(UC_X86_REG_RCX),
                    uc.reg_read(UC_X86_REG_RDX),
                    uc.reg_read(UC_X86_REG_RSI),
                    uc.reg_read(UC_X86_REG_RDI),
                    uc.reg_read(UC_X86_REG_R8),
                    uc.reg_read(UC_X86_REG_R9),
                    uc.reg_read(UC_X86_REG_R10),
                    uc.reg_read(UC_X86_REG_R11),
                    uc.reg_read(UC_X86_REG_R12),
                    uc.reg_read(UC_X86_REG_R13),
                    uc.reg_read(UC_X86_REG_R14),
                    uc.reg_read(UC_X86_REG_R15),
                    uc.reg_read(UC_X86_REG_RSP),
                    uc.reg_read(UC_X86_REG_EFLAGS),
                )
            )

        if (
            trace_input_flow
            and address == 0x1400219A6
            and input_addr[0] is not None
            and uc.reg_read(UC_X86_REG_R13) == input_addr[0]
        ):
            input_flow_active[0] = True

        if input_flow_active[0]:
            try:
                ins = next(md.disasm(uc.mem_read(address, size), address))
                input_flow.append(
                    (
                        steps[0],
                        address,
                        ins.mnemonic,
                        ins.op_str,
                        uc.reg_read(UC_X86_REG_RAX),
                        uc.reg_read(UC_X86_REG_RBX),
                        uc.reg_read(UC_X86_REG_RCX),
                        uc.reg_read(UC_X86_REG_RDX),
                        uc.reg_read(UC_X86_REG_RSI),
                        uc.reg_read(UC_X86_REG_RDI),
                        uc.reg_read(UC_X86_REG_R8),
                        uc.reg_read(UC_X86_REG_R9),
                        uc.reg_read(UC_X86_REG_R10),
                        uc.reg_read(UC_X86_REG_R11),
                        uc.reg_read(UC_X86_REG_R12),
                        uc.reg_read(UC_X86_REG_R13),
                        uc.reg_read(UC_X86_REG_R14),
                        uc.reg_read(UC_X86_REG_R15),
                        uc.reg_read(UC_X86_REG_RSP),
                        uc.reg_read(UC_X86_REG_EFLAGS),
                    )
                )
            except Exception:
                pass

        if address == HOOK_PRINT:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            rdx = uc.reg_read(UC_X86_REG_RDX)
            s = read_cstr(uc, rdx)
            output.append(s)
            calls.append(("print", hex(rdx), s))
            if input_flow_active[0] and rdx != 0x1400034D0:
                input_flow_active[0] = False
            ret_to(uc, rcx)
            return

        if address in fake_by_addr:
            _iat, _dll, name = fake_by_addr[address]
            rcx = uc.reg_read(UC_X86_REG_RCX)
            rdx = uc.reg_read(UC_X86_REG_RDX)
            r8 = uc.reg_read(UC_X86_REG_R8)
            r9 = uc.reg_read(UC_X86_REG_R9)
            calls.append(("import", name, hex(rcx), hex(rdx), hex(r8), hex(r9)))

            if "basic_istream" in name and "AEA_K" in name:
                input_addr[0] = rdx
                uc.mem_write(rdx, struct.pack("<Q", input_num))
                ret_to(uc, rcx)
            elif name == "strlen":
                ret_to(uc, len(read_cstr(uc, rcx)))
            elif name == "system":
                ret_to(uc, 0)
            elif name in ("exit", "_exit"):
                raise Stop()
            else:
                ret_to(uc, rcx)
            return

        if branch_trace:
            branch = branch_insns.get(address)
            if branch:
                branches.append(
                    (
                        address,
                        branch[0],
                        branch[1],
                        uc.reg_read(UC_X86_REG_EFLAGS),
                        uc.reg_read(UC_X86_REG_RAX),
                        uc.reg_read(UC_X86_REG_RBX),
                        uc.reg_read(UC_X86_REG_RCX),
                        uc.reg_read(UC_X86_REG_RDX),
                        uc.reg_read(UC_X86_REG_R8),
                        uc.reg_read(UC_X86_REG_R9),
                        uc.reg_read(UC_X86_REG_R10),
                        uc.reg_read(UC_X86_REG_R11),
                        uc.reg_read(UC_X86_REG_R12),
                        uc.reg_read(UC_X86_REG_R13),
                        uc.reg_read(UC_X86_REG_R14),
                        uc.reg_read(UC_X86_REG_R15),
                    )
                )

        if trace and steps[0] < 5000:
            try:
                ins = next(md.disasm(uc.mem_read(address, size), address))
                print(f"{steps[0]:07d} {address:016x}: {ins.mnemonic} {ins.op_str}")
            except Exception:
                pass

    uc.hook_add(UC_HOOK_CODE, hook_code)
    if watch_input or watch_stack or patch_writes:
        def hook_mem(uc, access, address, size, value, _user):
            base = input_addr[0]
            if watch_input and base is not None and address < base + 8 and address + size > base:
                mem_events.append((access, uc.reg_read(UC_X86_REG_RIP), address, size, value))
            if watch_stack and STACK - STACK_SIZE <= address < STACK:
                mem_events.append(
                    (
                        access,
                        uc.reg_read(UC_X86_REG_RIP),
                        address,
                        size,
                        value,
                        steps[0],
                        uc.reg_read(UC_X86_REG_RSI),
                        uc.reg_read(UC_X86_REG_RSP),
                    )
                )
            if access == UC_MEM_WRITE and patch_writes:
                key = (uc.reg_read(UC_X86_REG_RIP), address, size)
                if key in patch_writes:
                    patched = patch_writes[key] & ((1 << (size * 8)) - 1)
                    pending_patches.append((address, size, patched))

        uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, hook_mem)
    try:
        uc.emu_start(0x140001900, 0, count=max_insn)
    except Stop:
        pass
    except UcError as e:
        rip = uc.reg_read(UC_X86_REG_RIP)
        print(f"UCERR {e} rip={rip:#x} steps={steps[0]}")
        try:
            ins = next(md.disasm(uc.mem_read(rip, 16), rip))
            print(f"  {ins.mnemonic} {ins.op_str}")
        except Exception:
            pass
    return "".join(output), calls, steps[0], last_rips, branches, mem_events, snapshots, input_flow


if __name__ == "__main__":
    for value in [0, 1, 1234, 1337, 0x41414141, 0xFFFFFFFFFFFFFFFF]:
        out, calls, steps, rips, _branches, _mem_events, _snapshots, _input_flow = run(value)
        print(f"input={value} steps={steps} output={out!r}")
        print("last calls:", calls[-8:])
        print("last rips:", [hex(x) for x in rips[-8:]])
