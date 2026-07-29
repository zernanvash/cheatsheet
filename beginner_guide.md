# CTF Reverse Engineering: Starter Guide & Roadmap

Hey! Welcome to the reversing track. If you're coming from a defense or log monitoring background, diving into raw binaries might feel like a different world at first. Don't worry—everyone starts with the exact same confusion when looking at assembly or decompiled code for the first time!

This guide gives you the basic idea of how reversing works step-by-step, along with the best resources to dig deeper whenever you want to learn more.

---

## How to Think About Reversing

In defense, you're used to asking: *"What did this binary do on the network or disk?"* (looking at SIEM logs, process trees, or registry changes).

Reversing just shifts the camera angle to the inside: *"How does this binary decide what to do?"*

Since we rarely get source code in CTFs, we use disassemblers and debuggers to peek inside the compiled binary to see how it checks inputs, transforms keys, or hides the flag.

---

## Step 1: Quick Surface Recon (Outside Inspection)

**The Idea:** Before opening heavy reversing tools, take 30 seconds to inspect the file from the outside. You can check if it's 32-bit or 64-bit, search for plain-text hints (like error messages or flag formats), and watch what system calls it makes.

```bash
file challenge       # Check binary type and OS architecture
strings -n 8 challenge # Look for readable text hints
strace ./challenge    # Watch system calls live (like process logs)
```

> **Further Reading:**
> * Watch [LiveOverflow's Binary Recon Video](https://www.youtube.com/watch?v=3S_JSfw8j3c) for a visual walkthrough.
> * Check out the [Reversing CLI Tools Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) or search command flags live on [0xrefs Interactive Reference](https://zernanvash.dev/cheatsheet/0xrefs.html).

---

## Step 2: Reading the Code (Static Analysis)

**The Idea:** When plain-text `strings` doesn't give away the flag, we open the binary in a decompiler like **Ghidra** or **IDA**. Decompilers translate raw binary bytes back into pseudo-C code that humans can read.

```
Machine Bytes (0x89 0xE5) -> Assembly Instructions -> Decompiled Pseudo-C Code
```

You'll focus on three main things:
1. **Registers**: Think of registers (`RAX`, `EAX`) as temporary CPU variables or sticky notes.
2. **Control Flow**: Finding the `if/else` checks where the binary compares your input against the secret key.
3. **Functions**: Seeing where your input string gets passed.

> **Further Reading:**
> * Take [OST2's Free RE1001 Course](https://ost2.fyi/) to master x86-64 assembly fundamentals.
> * Watch [Low Level Learning's Assembly Shorts](https://www.youtube.com/@LowLevelLearning) for quick 5-minute explanations.
> * Check our online guides: [Ghidra Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/Ghidra%20Cheat%20Sheet.md) and [Reverse Engineering Blueprint](https://zernanvash.dev/cheatsheet/viewer.html?file=blueprints/Reverse%20Engineering%20Blueprint.md).

---

## Step 3: Stepping Through Execution (Dynamic Debugging)

**The Idea:** If decompiled code looks messy or obfuscated, don't strain your eyes guessing. Run the program inside a debugger (like **GDB** on Linux or **x64dbg** on Windows), set a **breakpoint** right before the password check, and pause execution to inspect variables live in memory.

> **Defender Connection:** Debugging is just like examining process memory or stack dumps during incident triage!

> **Further Reading:**
> * Play [Microcorruption](https://microcorruption.com/) — a fun browser game where you debug smart lock assembly line-by-line.
> * Watch [John Hammond's CTF Walkthroughs](https://www.youtube.com/@_JohnHammond) to see live GDB and Ghidra debugging in action.
> * Check our online debugging guides: [GDB Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/GDB%20Cheat%20Sheet.md) and [x64dbg Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/x64dbg%20Cheat%20Sheet.md).

---

## Step 4: Automating Math & Logic (Z3 Solver)

**The Idea:** Sometimes a binary checks your password against 15 complex math equations or byte XOR loops. Don't waste time doing algebra by hand! We use **Z3** (a Python library) to write constraints and let Python calculate the exact input for us.

```python
from z3 import *
a, b = Int('a'), Int('b')
s = Solver()
s.add(3 * a + 2 * b == 180, a - b == 10)
if s.check() == sat:
    print(s.model()) # Solves the exact values automatically!
```

> **Further Reading:**
> * Open our interactive browser app: [Z3 Interactive Practice](https://zernanvash.dev/cheatsheet/rev_source/z3_practice.html) to solve 20 decompiled code challenges right in your browser.
> * Grab Python script templates from the [REV Python Toolkit](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/REV%20Python%20Toolkit.md).

---

## Step 5: Independent Practice & Research

**The Idea:** Once you know how to inspect binaries, read decompiled C, use debuggers, and run Z3 solvers, you're ready to start solving real CTF challenges on your own!

> **Further Reading:**
> * [picoCTF Gym](https://play.picoctf.org/) — Beginner-friendly CTF challenges with helpful community hints.
> * [crackmes.one](https://crackmes.one/) — The biggest collection of downloadable puzzle binaries (filter by Easy).
> * [pwn.college](https://pwn.college/) — Free interactive Linux reversing courses.
> * Browse solved CTF writeups on [zernanvash.dev Writeup Browser](https://zernanvash.dev/cheatsheet/writeups.html) or check the main hub at [zernanvash.dev/cheatsheet](https://zernanvash.dev/cheatsheet/).

---

## Summary Cheatsheet

| Stage | Main Concept | Quick Tools | Learn More Link |
|---|---|---|---|
| 1. Recon | Inspect file headers & strings | `file`, `strings`, `strace` | [LiveOverflow Recon Video](https://www.youtube.com/watch?v=3S_JSfw8j3c) \| [CLI Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/Reversing%20CLI%20Tools%20Cheat%20Sheet.md) |
| 2. Static | Read decompiled C code | Ghidra, IDA Free | [OST2 RE1001 Course](https://ost2.fyi/) \| [Ghidra Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/Ghidra%20Cheat%20Sheet.md) |
| 3. Dynamic | Pause memory execution | GDB + GEF, x64dbg | [Microcorruption Game](https://microcorruption.com/) \| [GDB Cheat Sheet](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/GDB%20Cheat%20Sheet.md) |
| 4. Solver | Automate math with Python | Python 3 + Z3 | [Z3 Browser Game](https://zernanvash.dev/cheatsheet/rev_source/z3_practice.html) \| [Python Toolkit](https://zernanvash.dev/cheatsheet/viewer.html?file=tools/REV%20Python%20Toolkit.md) |
| 5. Self-Study | Solve real CTF targets | crackmes.one, picoCTF | [picoCTF Gym](https://play.picoctf.org/) \| [zernanvash.dev Main Hub](https://zernanvash.dev/cheatsheet/) |
