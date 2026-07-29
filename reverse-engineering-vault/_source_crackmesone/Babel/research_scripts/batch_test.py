#!/usr/bin/env python3
"""Batch verification of keygen against the real babel_vm.exe binary."""

import subprocess, sys, time
sys.path.insert(0, r"c:\Users\hatem\Desktop\Challenges\Challenge03")
from keygen import keygen

BINARY = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"

test_users = [
    "test",
    "admin",
    "w33d",
    "BABEL_VM",
    "CrackMe2026",
    "hatem",
    "reverse_engineering_is_fun",
]

results = []
for user in test_users:
    t0 = time.time()
    serial_str, S, h = keygen(user)
    dt = time.time() - t0

    inp = f"{user}\n{serial_str}\n"
    r = subprocess.run([BINARY], input=inp, capture_output=True, text=True, timeout=15)
    ok = "Access Granted" in r.stdout or "Valid" in r.stdout

    # Also check for the success XOR-decoded message
    if not ok:
        # Look for any non-"Invalid" message
        lines = r.stdout.strip().split('\n')
        last = lines[-1].strip() if lines else ""
        if "Invalid" not in last and last:
            ok = True

    status = "PASS" if ok else "FAIL"
    results.append((user, serial_str, status, dt))
    print(f"  [{status}] {user:30s} -> {serial_str}  ({dt:.2f}s)")

print()
passed = sum(1 for _,_,s,_ in results if s=="PASS")
print(f"Results: {passed}/{len(results)} passed")
