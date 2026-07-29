#!/usr/bin/env python3
from __future__ import annotations

import glob
import os
import random
import re
import string
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
BIN = str(HERE / "live_cap_allargs_eval2.bin")
HOOK = str(HERE / "hook_watch_eval_state.so")
TARGET_SUM = 0x18FC
CHARS = string.ascii_letters + string.digits + "_-.!@#$%^&*"
LOG_GLOB = "/tmp/hook_watch_eval_state_*.log"


def q(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def parse_eval_from_log(path: str) -> int | None:
    txt = Path(path).read_text(errors="ignore")
    vals = [int(m.group(1), 16) for m in re.finditer(r"arg5=0338578a.*eval=([0-9a-fA-F]+)", txt)]
    if not vals:
        return None
    return vals[-1]  # !!! IMPORTANT !! !!! last observed eval for this process


def run_eval(candidate: str, timeout_s: int = 12) -> int | None:
    for p in glob.glob(LOG_GLOB):
        try:
            os.unlink(p)
        except OSError:
            pass

    cmd = (
        f"printf '%s\\n\\n' {q(candidate)} | "
        f"LD_PRELOAD={q(HOOK)} timeout {timeout_s}s wine {q(BIN)} --type=utility "
        f">/tmp/oracle_final_run.out 2>/tmp/oracle_final_run.err"
    )
    subprocess.run(cmd, shell=True, check=False)

    # Prefer newest process log that actually contains the target call
    found: list[tuple[float, str, int]] = []
    for p in glob.glob(LOG_GLOB):
        try:
            ev = parse_eval_from_log(p)
            if ev is None:
                continue
            mt = os.path.getmtime(p)
            found.append((mt, p, ev))
        except OSError:
            continue
    if not found:
        return None
    found.sort(key=lambda x: x[0])
    return found[-1][2]


def score(ev: int) -> int:
    sm = ev ^ TARGET_SUM
    return abs(sm - TARGET_SUM)


def run_eval_multi(candidate: str, rounds: int) -> tuple[list[int], int]:
    vals: list[int] = []
    for _ in range(rounds):
        ev = run_eval(candidate)
        if ev is not None:
            vals.append(ev)
    if not vals:
        return vals, 1 << 30
    # minimize worst observed distance
    return vals, max(score(v) for v in vals)


def mutate(s: str) -> str:
    # fixed length search (64 chars) to avoid OOB read nondeterminism in verifier
    mode = random.random()
    b = list(s)
    if mode < 0.85:
        i = random.randrange(len(b))
        b[i] = random.choice(CHARS)
    else: # COND
        i = random.randrange(len(b))
        j = random.randrange(len(b))
        b[i], b[j] = b[j], b[i]
    return "".join(b)


def main() -> int:
    random.seed(int(time.time()))
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    seeds = [
        "A" * 64,
        "B" * 64,
        "C" * 64,
        ("PassQW9or2dCr2ckM3ByPwn" + "X" * 64)[:64], # decoy?? idk
        "".join(random.choice(CHARS) for _ in range(64)),
    ]

    best_s = None
    best_ev = None
    best_d = None
    cur_s = None
    cur_ev = None
    cur_d = None

    for s in seeds:
        vals, d = run_eval_multi(s, rounds)
        if not vals:
            continue
        ev = vals[-1]
        print(f"SEED d={d:5d} ev_last=0x{ev:08x} vals={[hex(v) for v in vals]} s={s}", flush=True)
        if best_d is None or d < best_d:
            best_d, best_s, best_ev = d, s, ev
        if cur_d is None or d < cur_d:
            cur_d, cur_s, cur_ev = d, s, ev
        if all(v == 0 for v in vals):
            print(f"FOUND {s}", flush=True)
            return 0

    if cur_s is None:
        print("no usable seed")
        return 1

    for step in range(budget):
        cand = mutate(cur_s)
        vals, d = run_eval_multi(cand, rounds)
        if not vals:
            continue
        ev = vals[-1]

        accept = d <= cur_d or random.random() < 0.03
        if accept:
            cur_s, cur_ev, cur_d = cand, ev, d

        if d < best_d:
            best_s, best_ev, best_d = cand, ev, d
            print(f"BEST step={step:5d} d={d:5d} ev_last=0x{ev:08x} vals={[hex(v) for v in vals]} s={cand}", flush=True)

        if step % 25 == 0:
            print(
                f"STEP {step:5d} cur_d={cur_d:5d} cur_ev=0x{cur_ev:08x} "
                f"best_d={best_d:5d} best_ev=0x{best_ev:08x}",
                flush=True,
            )

        if all(v == 0 for v in vals):
            print(f"FOUND {cand}", flush=True)
            return 0

    print(f"DONE best_d={best_d} best_ev=0x{best_ev:08x} best={best_s}") #fi
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
