#!/usr/bin/env python3
from __future__ import annotations

import sys
from vm_run import VM


def run(s: str):
    events = []
    vm = VM(s.encode() + b"\n", events=events)
    out = vm.run()
    return out.decode("latin1", errors="replace"), events, vm


def main() -> None:
    inputs = sys.argv[1:] or ["wrong", "test", "pasta", "spaghetti", "aj21h", "password"]
    runs = {}
    for s in inputs:
        out, events, vm = run(s)
        runs[s] = (out, events, vm)
        last = out.splitlines()[-1] if out.splitlines() else ""
        print(f"{s!r}: {last!r} events={len(events)} steps={vm.steps} reads={vm.inpos}")

    base_name = inputs[0]
    base_events = [e for e in runs[base_name][1] if e[0] in ("branch", "cmp")]
    for other in inputs[1:]:
        other_events = [e for e in runs[other][1] if e[0] in ("branch", "cmp")]
        print(f"\nfirst diffs {base_name!r} vs {other!r}")
        shown = 0
        for i, (a, b) in enumerate(zip(base_events, other_events)):
            if a != b:
                print(f"#{i}: {a} != {b}")
                shown += 1
                if shown >= 20:
                    break
        print(f"cmp/branch lens: {len(base_events)} vs {len(other_events)}")


if __name__ == "__main__":
    main()
