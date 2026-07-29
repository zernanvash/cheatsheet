#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import struct
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


# recovered:
# target_dword[i] = BASE_DWORD[i] ^ exc_seed
# key bytes are target dwords serialized little-endian.
BASE_DWORDS = (
    0x6E2F1A3B,
    0xC4D85F92,
    0x1B7E3C6D,
    0xA09F4E21,
)

EXC_XOR_CONST = 0xABCDEF01

ADDR_EXC_SEED = 0x140030E08
ADDR_TARGETS = 0x140030B70


@dataclass
class RuntimeState:
    exc_seed: int
    targets: tuple[int, int, int, int]


def to_u32(v: int) -> int:
    return v & 0xFFFFFFFF


def key_dwords_from_exc_seed(exc_seed: int) -> tuple[int, int, int, int]:
    exc_seed = to_u32(exc_seed)
    return tuple(to_u32(x ^ exc_seed) for x in BASE_DWORDS)


def key_bytes_from_exc_seed(exc_seed: int) -> bytes:
    return b"".join(struct.pack("<I", x) for x in key_dwords_from_exc_seed(exc_seed))


def escape_bytes(bs: bytes) -> str:
    out = []
    for b in bs:
        if 32 <= b < 127 and b not in (0x5C,):  # printable except backslash
            out.append(chr(b))
        else:
            out.append(f"\\x{b:02x}")
    return "".join(out)


def read_u32_from_pid(pid: int, addr: int) -> int:
    with open(f"/proc/{pid}/mem", "rb", buffering=0) as f:
        f.seek(addr)
        b = f.read(4)
    if len(b) != 4:
        raise RuntimeError("short read")
    return struct.unpack("<I", b)[0]


def read_targets_from_pid(pid: int) -> tuple[int, int, int, int]:
    with open(f"/proc/{pid}/mem", "rb", buffering=0) as f:
        f.seek(ADDR_TARGETS)
        b = f.read(16)
    if len(b) != 16:
        raise RuntimeError("short read")
    return struct.unpack("<IIII", b)


def read_runtime_state(pid: int, timeout_s: float = 5.0) -> RuntimeState:
    deadline = time.time() + timeout_s
    last_err = None
    while time.time() < deadline:
        try:
            exc = read_u32_from_pid(pid, ADDR_EXC_SEED)
            targets = read_targets_from_pid(pid)
            if targets == (0, 0, 0, 0):
                raise RuntimeError("targets not  initialized yet ")
            return RuntimeState(exc_seed=exc, targets=targets)
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(0.01)
    raise RuntimeError(f"failed reading runtime state from pid {pid}: {last_err}")


def _read_ppid_map() -> dict[int, int]:
    out: dict[int, int] = {}
    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue
        pid = int(name)
        try:
            with open(f"/proc/{pid}/stat", "r", encoding="latin1") as f:
                s = f.read()
            # format: pid (comm) state ppid ...
            rparen = s.rfind(")")
            if rparen == -1:
                continue
            rest = s[rparen + 2 :].split()
            if len(rest) < 3:
                continue
            ppid = int(rest[1])
            out[pid] = ppid
        except Exception:
            continue
    return out


def _descendants(root_pid: int) -> set[int]:
    ppid_map = _read_ppid_map()
    children: dict[int, list[int]] = {}
    for pid, ppid in ppid_map.items():
        children.setdefault(ppid, []).append(pid)

    seen: set[int] = set()
    stack = [root_pid]
    while stack:
        cur = stack.pop()
        for ch in children.get(cur, []):
            if ch in seen:
                continue
            seen.add(ch)
            stack.append(ch)
    return seen


def _cmdline(pid: int) -> str:
    with open(f"/proc/{pid}/cmdline", "rb") as f:
        data = f.read()
    return data.replace(b"\x00", b" ").decode("latin1", "ignore").strip()


def resolve_target_pid(root_pid: int, exe_name: str, timeout_s: float = 5.0) -> int:
    exe_name = Path(exe_name).name
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        # try the root directly
        try:
            _ = read_u32_from_pid(root_pid, ADDR_EXC_SEED)
            return root_pid
        except Exception:
            pass

        # try descendants that look like the PE host process
        for pid in sorted(_descendants(root_pid)):
            try:
                cmd = _cmdline(pid)
                if exe_name not in cmd:
                    continue
                _ = read_u32_from_pid(pid, ADDR_EXC_SEED)
                return pid
            except Exception:
                continue
        time.sleep(0.01)
    raise RuntimeError(f"could not resolve target pid from root pid {root_pid}")


def print_key(exc_seed: int) -> None:
    d = key_dwords_from_exc_seed(exc_seed)
    k = b"".join(struct.pack("<I", x) for x in d)
    print(f"exc_seed: 0x{exc_seed:08x}")
    print("key_dwords:", " ".join(f"0x{x:08x}" for x in d))
    print("key_hex:", k.hex())
    print("key_escaped:", escape_bytes(k))


def mode_from_exc(args: argparse.Namespace) -> int:
    print_key(to_u32(args.exc_seed))
    return 0


def mode_from_tick_pid(args: argparse.Namespace) -> int:
    exc = to_u32(args.tick ^ args.pid ^ EXC_XOR_CONST)
    print(f"tick: 0x{args.tick & 0xFFFFFFFF:08x}")
    print(f"pid:  0x{args.pid & 0xFFFFFFFF:08x}")
    print(f"exc = tick ^ pid ^ 0x{EXC_XOR_CONST:08x}")
    print_key(exc)
    return 0


def mode_from_pid(args: argparse.Namespace) -> int:
    target_pid = args.pid
    if not args.no_resolve:
        target_pid = resolve_target_pid(args.pid, args.exe_name, timeout_s=args.timeout)
    st = read_runtime_state(target_pid, timeout_s=args.timeout)
    print(f"pid: {target_pid}")
    print_key(st.exc_seed)
    if args.show_targets:
        print("targets:", " ".join(f"0x{x:08x}" for x in st.targets))
    return 0


def mode_launch(args: argparse.Namespace) -> int:
    env = os.environ.copy()
    if not args.no_quiet_wine:
        env["WINEDEBUG"] = "-all"

    for attempt in range(1, args.attempts + 1):
        proc = subprocess.Popen(
            [args.wine, args.exe],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
        try:
            target_pid = resolve_target_pid(proc.pid, args.exe, timeout_s=args.timeout)
            st = read_runtime_state(target_pid, timeout_s=args.timeout)
            key = key_bytes_from_exc_seed(st.exc_seed)

            if proc.stdin is None:
                raise RuntimeError("stdin pipe unavailable")
            # ssecond newline satisfies the "Press any key to continue..." prompt
            proc.stdin.write(key + b"\n\n")
            proc.stdin.flush()

            out = proc.communicate(timeout=args.proc_timeout)[0]
            text = out.decode("latin1", "ignore")
            pw_line = ""
            for ln in text.splitlines():
                if ln.startswith("Password:"):
                    pw_line = ln

            print(
                f"[{attempt}] pid={target_pid} root_pid={proc.pid} "
                f"exc=0x{st.exc_seed:08x} key={key.hex()} msg={pw_line!r}"
            )

            if ("Correct!" in pw_line) or ("FLAG{" in pw_line):
                print("[+] success")
                return 0
        except subprocess.TimeoutExpired:
            proc.kill()
            print(f"[{attempt}] timeout")
        except Exception as e:  # noqa: BLE001
            proc.kill()
            print(f"[{attempt}] error: {e}")

    print("[!] no successful run in allotted attempts", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "keygen for bobxREAL.exe --- derive per-run 16-byte key"
        )
    )
    sp = p.add_subparsers(dest="mode", required=True)

    p_exc = sp.add_parser("from-exc", help="Generate key from exc_seed (u32).")
    p_exc.add_argument("--exc-seed", required=True, type=lambda x: int(x, 0))
    p_exc.set_defaults(func=mode_from_exc)

    p_tp = sp.add_parser("from-tick-pid", help="Generate key from tick and pid.")
    p_tp.add_argument("--tick", required=True, type=lambda x: int(x, 0))
    p_tp.add_argument("--pid", required=True, type=lambda x: int(x, 0))
    p_tp.set_defaults(func=mode_from_tick_pid)

    p_pid = sp.add_parser(
        "from-pid",
        help="Read exc_seed from /proc/<pid>/mem annd generate key.",
    )
    p_pid.add_argument("--pid", required=True, type=int)
    p_pid.add_argument("--timeout", type=float, default=5.0)
    p_pid.add_argument("--exe-name", default="bobxREAL.exe")
    p_pid.add_argument("--no-resolve", action="store_true")
    p_pid.add_argument("--show-targets", action="store_true")
    p_pid.set_defaults(func=mode_from_pid)

    p_launch = sp.add_parser(
        "launch",
        help=(
            "launch target, extract live exc_seed, generate real key, feed it automatically. "
            "Multiple attempts handle the crackme's randomized outer state machine."
        ),
    )
    p_launch.add_argument("--exe", default="bobxREAL.exe")
    p_launch.add_argument("--wine", default="wine")
    p_launch.add_argument("--attempts", type=int, default=20)
    p_launch.add_argument("--timeout", type=float, default=5.0, help="Seed-read timeout per attempt.")
    p_launch.add_argument("--proc-timeout", type=float, default=20.0, help="Process completion timeout.")
    p_launch.add_argument("--no-quiet-wine", action="store_true")
    p_launch.set_defaults(func=mode_launch)

    return p


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
