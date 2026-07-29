"""
crackme3 keygen
===============
The crackme generates a 32-character key at startup using:
  seed = time(0) ^ GetTickCount()
  LCG:  seed = seed * 0x19660D + 0x3C6EF35F  (mod 2^32)
  char  = charset[seed % 62]
  charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

The generated chars are XOR'd with 0x5A and stored at address 0x466B80
in the crackme's memory (32 bytes).

Two modes:
  1) --read-memory  : attach to a running crackme3 process and read the
                      key directly from its memory (most reliable)
  2) --brute-time   : given approximate time & tick, brute-force the key
"""

import argparse
import ctypes
import ctypes.wintypes as wt
import struct
import sys
import time

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
KEY_TABLE_VA = 0x466B80
KEY_LEN = 32
XOR_BYTE = 0x5A

# ------------------------------------------------------------------ #
#  Mode 1: Read key from running process memory                       #
# ------------------------------------------------------------------ #
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

def read_key_from_process(pid: int) -> str:
    """Read the key table from a running crackme3 process."""
    kernel32 = ctypes.windll.kernel32

    hProcess = kernel32.OpenProcess(
        PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid
    )
    if not hProcess:
        print(f"Error: cannot open process {pid} (run as admin?)")
        sys.exit(1)

    buf = ctypes.create_string_buffer(KEY_LEN)
    bytesRead = ctypes.c_size_t(0)
    ok = kernel32.ReadProcessMemory(
        hProcess,
        ctypes.c_void_p(KEY_TABLE_VA),
        buf,
        KEY_LEN,
        ctypes.byref(bytesRead),
    )
    kernel32.CloseHandle(hProcess)

    if not ok or bytesRead.value != KEY_LEN:
        print("Error: ReadProcessMemory failed")
        sys.exit(1)

    raw = buf.raw
    key = "".join(chr(b ^ XOR_BYTE) for b in raw)
    return key


# ------------------------------------------------------------------ #
#  Mode 2: Brute-force key from approximate time & tick               #
# ------------------------------------------------------------------ #
def generate_key(seed: int) -> str:
    """Generate the 32-char key given the initial LCG seed."""
    s = seed & 0xFFFFFFFF
    key = []
    for _ in range(KEY_LEN):
        s = (s * 0x19660D + 0x3C6EF35F) & 0xFFFFFFFF
        idx = s % 62
        key.append(CHARSET[idx])
    return "".join(key)


def brute_force(approx_time: int, approx_tick: int, window: int = 5000):
    """
    Try seeds around the given approximate time and tick values.
    Since the crackme uses  seed = time(0) ^ GetTickCount(),
    and both change, we try combinations within a window.
    """
    print(f"Brute-forcing with time~{approx_time}, tick~{approx_tick}, window={window}")
    print("(this is a demo — use --read-memory for the real key)\n")

    # Show a few candidate keys
    for dt in range(-2, 3):
        for dtick in range(0, window, 100):
            t = approx_time + dt
            tick = approx_tick + dtick
            seed = t ^ tick
            key = generate_key(seed)
            if dt == 0 and dtick == 0:
                print(f"  seed=0x{seed:08X}  key={key}  (exact guess)")
    print("\n(only showing exact-guess key; real usage: read from memory)")


# ------------------------------------------------------------------ #
#  CLI                                                                #
# ------------------------------------------------------------------ #
def main():
    parser = argparse.ArgumentParser(description="crackme3 keygen")
    sub = parser.add_subparsers(dest="mode")

    p1 = sub.add_parser("read", help="Read key from running crackme3 process")
    p1.add_argument("pid", type=int, help="PID of crackme3_cracked.exe")

    p2 = sub.add_parser("generate", help="Generate key from a known seed")
    p2.add_argument("seed", type=lambda x: int(x, 0), help="LCG seed (hex or dec)")

    args = parser.parse_args()

    if args.mode == "read":
        key = read_key_from_process(args.pid)
        print(f"\n  Valid key: {key}\n")
    elif args.mode == "generate":
        key = generate_key(args.mode and args.seed)
        print(f"\n  Key for seed 0x{args.seed:08X}: {key}\n")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python keygen.py read 12345          # read key from process with PID 12345")
        print("  python keygen.py generate 0xDEADBEEF # generate key for a given seed")

if __name__ == "__main__":
    main()
