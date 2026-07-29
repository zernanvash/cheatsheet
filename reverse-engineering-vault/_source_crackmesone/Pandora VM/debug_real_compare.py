import ctypes
import struct
from ctypes import wintypes


DEBUG_ONLY_THIS_PROCESS = 0x00000002
DBG_CONTINUE = 0x00010002
STARTF_USESTDHANDLES = 0x00000100
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
EXCEPTION_DEBUG_EVENT = 1
CREATE_PROCESS_DEBUG_EVENT = 3
EXIT_PROCESS_DEBUG_EVENT = 5
EXCEPTION_BREAKPOINT = 0x80000003
EXCEPTION_SINGLE_STEP = 0x80000004
CONTEXT_AMD64 = 0x00100000
CONTEXT_CONTROL = CONTEXT_AMD64 | 0x1
CONTEXT_INTEGER = CONTEXT_AMD64 | 0x2

BASE = 0x140000000
BP_VA = 0x14001AFB3


class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.c_void_p),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", ctypes.c_void_p),
        ("bInheritHandle", wintypes.BOOL),
    ]


class EXCEPTION_RECORD64(ctypes.Structure):
    _fields_ = [
        ("ExceptionCode", wintypes.DWORD),
        ("ExceptionFlags", wintypes.DWORD),
        ("ExceptionRecord", ctypes.c_ulonglong),
        ("ExceptionAddress", ctypes.c_ulonglong),
        ("NumberParameters", wintypes.DWORD),
        ("__unusedAlignment", wintypes.DWORD),
        ("ExceptionInformation", ctypes.c_ulonglong * 15),
    ]


class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [("ExceptionRecord", EXCEPTION_RECORD64), ("dwFirstChance", wintypes.DWORD)]


class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ("hFile", wintypes.HANDLE),
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("lpBaseOfImage", ctypes.c_void_p),
        ("dwDebugInfoFileOffset", wintypes.DWORD),
        ("nDebugInfoSize", wintypes.DWORD),
        ("lpThreadLocalBase", ctypes.c_void_p),
        ("lpStartAddress", ctypes.c_void_p),
        ("lpImageName", ctypes.c_void_p),
        ("fUnicode", wintypes.WORD),
    ]


class DEBUG_EVENT_UNION(ctypes.Union):
    _fields_ = [
        ("Exception", EXCEPTION_DEBUG_INFO),
        ("CreateProcessInfo", CREATE_PROCESS_DEBUG_INFO),
        ("raw", ctypes.c_byte * 160),
    ]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ("dwDebugEventCode", wintypes.DWORD),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
        ("u", DEBUG_EVENT_UNION),
    ]


class CONTEXT64(ctypes.Structure):
    _fields_ = [
        ("P1Home", ctypes.c_ulonglong),
        ("P2Home", ctypes.c_ulonglong),
        ("P3Home", ctypes.c_ulonglong),
        ("P4Home", ctypes.c_ulonglong),
        ("P5Home", ctypes.c_ulonglong),
        ("P6Home", ctypes.c_ulonglong),
        ("ContextFlags", wintypes.DWORD),
        ("MxCsr", wintypes.DWORD),
        ("SegCs", wintypes.WORD),
        ("SegDs", wintypes.WORD),
        ("SegEs", wintypes.WORD),
        ("SegFs", wintypes.WORD),
        ("SegGs", wintypes.WORD),
        ("SegSs", wintypes.WORD),
        ("EFlags", wintypes.DWORD),
        ("Dr0", ctypes.c_ulonglong),
        ("Dr1", ctypes.c_ulonglong),
        ("Dr2", ctypes.c_ulonglong),
        ("Dr3", ctypes.c_ulonglong),
        ("Dr6", ctypes.c_ulonglong),
        ("Dr7", ctypes.c_ulonglong),
        ("Rax", ctypes.c_ulonglong),
        ("Rcx", ctypes.c_ulonglong),
        ("Rdx", ctypes.c_ulonglong),
        ("Rbx", ctypes.c_ulonglong),
        ("Rsp", ctypes.c_ulonglong),
        ("Rbp", ctypes.c_ulonglong),
        ("Rsi", ctypes.c_ulonglong),
        ("Rdi", ctypes.c_ulonglong),
        ("R8", ctypes.c_ulonglong),
        ("R9", ctypes.c_ulonglong),
        ("R10", ctypes.c_ulonglong),
        ("R11", ctypes.c_ulonglong),
        ("R12", ctypes.c_ulonglong),
        ("R13", ctypes.c_ulonglong),
        ("R14", ctypes.c_ulonglong),
        ("R15", ctypes.c_ulonglong),
        ("Rip", ctypes.c_ulonglong),
        ("Padding", ctypes.c_byte * 2048),
    ]


k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.CreateProcessW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPWSTR,
    ctypes.c_void_p,
    ctypes.c_void_p,
    wintypes.BOOL,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.LPCWSTR,
    ctypes.POINTER(STARTUPINFO),
    ctypes.POINTER(PROCESS_INFORMATION),
]
k32.CreatePipe.argtypes = [ctypes.POINTER(wintypes.HANDLE), ctypes.POINTER(wintypes.HANDLE), ctypes.POINTER(SECURITY_ATTRIBUTES), wintypes.DWORD]
k32.WriteFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
k32.CloseHandle.argtypes = [wintypes.HANDLE]
k32.GetStdHandle.argtypes = [wintypes.DWORD]
k32.GetStdHandle.restype = wintypes.HANDLE
k32.WaitForDebugEvent.argtypes = [ctypes.POINTER(DEBUG_EVENT), wintypes.DWORD]
k32.ContinueDebugEvent.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
k32.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.WriteProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.FlushInstructionCache.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t]
k32.GetThreadContext.argtypes = [wintypes.HANDLE, ctypes.POINTER(CONTEXT64)]
k32.SetThreadContext.argtypes = [wintypes.HANDLE, ctypes.POINTER(CONTEXT64)]
k32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]


def check(ok, msg):
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error(), msg)


def read_qword(process, addr):
    buf = ctypes.create_string_buffer(8)
    got = ctypes.c_size_t()
    check(k32.ReadProcessMemory(process, ctypes.c_void_p(addr), buf, 8, ctypes.byref(got)), "ReadProcessMemory")
    return struct.unpack("<Q", buf.raw)[0]


def write_byte(process, addr, value):
    buf = ctypes.create_string_buffer(bytes([value]))
    wrote = ctypes.c_size_t()
    check(k32.WriteProcessMemory(process, ctypes.c_void_p(addr), buf, 1, ctypes.byref(wrote)), "WriteProcessMemory")
    k32.FlushInstructionCache(process, ctypes.c_void_p(addr), 1)


sa = SECURITY_ATTRIBUTES()
sa.nLength = ctypes.sizeof(sa)
sa.bInheritHandle = True
stdin_r = wintypes.HANDLE()
stdin_w = wintypes.HANDLE()
check(k32.CreatePipe(ctypes.byref(stdin_r), ctypes.byref(stdin_w), ctypes.byref(sa), 0), "CreatePipe")
payload = b"0\n"
written = wintypes.DWORD()
check(k32.WriteFile(stdin_w, payload, len(payload), ctypes.byref(written), None), "WriteFile")
k32.CloseHandle(stdin_w)

si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
si.dwFlags = STARTF_USESTDHANDLES
si.hStdInput = stdin_r
si.hStdOutput = k32.GetStdHandle(STD_OUTPUT_HANDLE)
si.hStdError = k32.GetStdHandle(STD_ERROR_HANDLE)
pi = PROCESS_INFORMATION()
cmd = ctypes.create_unicode_buffer("vm_crackme.exe")
check(
    k32.CreateProcessW(
        None,
        cmd,
        None,
        None,
        True,
        DEBUG_ONLY_THIS_PROCESS,
        None,
        ".",
        ctypes.byref(si),
        ctypes.byref(pi),
    ),
    "CreateProcessW",
)

base = BASE
bp_addr = BP_VA
orig_byte = None
patched = False
stepping = False
hit_count = 0

while True:
    ev = DEBUG_EVENT()
    check(k32.WaitForDebugEvent(ctypes.byref(ev), 10000), "WaitForDebugEvent")
    code = ev.dwDebugEventCode
    status = DBG_CONTINUE

    if code == CREATE_PROCESS_DEBUG_EVENT:
        base = int(ev.u.CreateProcessInfo.lpBaseOfImage)
        bp_addr = base + (BP_VA - BASE)
        orig_byte = read_qword(pi.hProcess, bp_addr) & 0xFF
        write_byte(pi.hProcess, bp_addr, 0xCC)
        patched = True
        print(f"base={base:#x} bp={bp_addr:#x} orig={orig_byte:#x}")

    elif code == EXCEPTION_DEBUG_EVENT:
        ex = ev.u.Exception.ExceptionRecord
        if ex.ExceptionCode == EXCEPTION_BREAKPOINT and patched and int(ex.ExceptionAddress) == bp_addr:
            ctx = CONTEXT64()
            ctx.ContextFlags = CONTEXT_CONTROL | CONTEXT_INTEGER
            check(k32.GetThreadContext(pi.hThread, ctypes.byref(ctx)), "GetThreadContext")
            hit_count += 1
            stack_flags = read_qword(pi.hProcess, ctx.Rsp)
            slot0 = read_qword(pi.hProcess, ctx.Rsi)
            slot1 = read_qword(pi.hProcess, ctx.Rsi + 8)
            print(
                f"hit {hit_count}: rip={ctx.Rip:#x} r15={ctx.R15:#x} "
                f"rsi={ctx.Rsi:#x} rbx={ctx.Rbx:#x} r9={ctx.R9:#x} flags={stack_flags:#x}"
            )
            if ctx.R15 == base + 0x261E3:
                print(f"decisive hit: rsp={ctx.Rsp:#x} eflags={ctx.EFlags:#x}")
                print(f"[rsi]={slot0:#x} [rsi+8]={slot1:#x}")
                print(f"derived_key={(~ctx.Rbx + 1) & 0xffffffffffffffff:#x} {((~ctx.Rbx + 1) & 0xffffffffffffffff)}")
                k32.TerminateProcess(pi.hProcess, 0)
                break

            write_byte(pi.hProcess, bp_addr, orig_byte)
            ctx.Rip = bp_addr
            ctx.EFlags |= 0x100
            check(k32.SetThreadContext(pi.hThread, ctypes.byref(ctx)), "SetThreadContext")
            stepping = True

        elif ex.ExceptionCode == EXCEPTION_SINGLE_STEP and stepping:
            write_byte(pi.hProcess, bp_addr, 0xCC)
            stepping = False

    elif code == EXIT_PROCESS_DEBUG_EVENT:
        print("process exited before breakpoint")
        break

    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, status)
class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", ctypes.c_void_p),
        ("bInheritHandle", wintypes.BOOL),
    ]
