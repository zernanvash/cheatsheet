# Reverse Engineering Fundamentals

Use this before the reversing blueprint when you are still learning what files, strings, assembly, and debuggers are telling you.

## What Reversing Means In CTFs

Reverse engineering is reading a program or artifact to understand how it validates input, transforms data, hides a flag, or crashes.

Common CTF reversing targets:

- ELF Linux binaries.
- PE Windows binaries.
- Python source or bytecode.
- Java/JAR/APK.
- WebAssembly modules.
- pwn/buffer overflow binaries.

## First Questions

```bash
file challenge
strings -n 8 challenge
sha256sum challenge
```

Ask:

- What file type is it?
- Can it run locally?
- Does it ask for input?
- Are there readable strings?
- Is it source code, bytecode, or native binary?
- Does long input crash it?

## Core Concepts

- Static analysis: read without running.
- Dynamic analysis: run/debug and observe behavior.
- Strings: readable byte sequences.
- Disassembly: machine code converted to assembly.
- Registers: CPU storage used during execution.
- Stack: memory region for calls, local data, and return addresses.
- Control flow: branches, jumps, calls, and returns.

## Safe Beginner Workflow

1. Work in a lab VM or disposable folder.
2. Run `file` and `strings`.
3. Execute once only if safe and expected.
4. Use GDB/x64dbg for input checks.
5. Rebuild transforms in Python.
6. If it crashes after long input, switch to buffer overflow workflow.

## When To Jump To Blueprints

- General reversing -> [Reverse Engineering Blueprint](../blueprints/Reverse%20Engineering%20Blueprint.md).
- Native crash or pwn -> [Buffer Overflow Blueprint](../blueprints/Buffer%20Overflow%20Blueprint.md).
- Python helper scripts -> [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md).
- Examples -> [picoCTF Web and REV Patterns](../guides/picoCTF%20Web%20and%20REV%20Patterns.md).
