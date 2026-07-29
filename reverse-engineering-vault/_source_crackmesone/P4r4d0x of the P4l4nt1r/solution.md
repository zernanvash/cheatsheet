# summary

Challenge_URL: https://crackmes.one/crackme/6a148dd62b3df128c1df5c9e

the target is `p0tp.exe`, a pe64 crackme with a custom vm. i found an accepted pair of byte-string keys that makes the unmodified program print the success line and the flag buffer. the path i used is not a binary patch. it uses the fact that two later vm bytecode blocks are decrypted from the two 32-bit input hashes.

the final keys are byte strings, not normal printable text.

key 1 hex:

```text
50414c414e54495241414141414141f020ff0f
```

key 2 hex:

```text
bf2af2687c41414141414141414141414164ab23ae
```

the stdin file used for validation is `solution_stdin_palantir.bin`.

# target identifiers

file: `p0tp.exe`

sha256:

```text
f0791256f2035b2fe4d4fadc207d1e739211d29549e44fb4cd1f1ac8596dbb50
```

sha1:

```text
5c1042461c8783b2b990e48ed5bbd8fff36c21ce
```

md5:

```text
f106474d052340895c77433b1fe235b0
```

the binary is a 64-bit windows pe built with the microsoft c and c++ runtime.

# static triage

i started with hashes, file metadata, die, capa, floss, radare2, lief, and ghidra. ghidra gave the most useful view after import. the important code was a vm interpreter that decrypts bytecode before running it.

the vm bytecode decrypt has three regions:

```text
offset < 0x19a: xor with 0x4b3a8f25, selected by offset mod 4
0x19a through 0x1a6: xor with hash1 ^ 0x7e9d3f1e
offset >= 0x1a7: xor with hash2 ^ 0x3f6a8d2e
```

the input hash routine is:

```text
state starts at 0x1337 for key 1 or 0xdead for key 2
state = low64(state * state)
state = state + input_byte
state = low64(state * 0x19e3779b9)
state = state >> 32
```

the normal intended hashes are:

```text
hash1 = 0x5ce4f560
hash2 = 0x9bcf98e6
```

# validation notes

the early vm code checks the first four bytes of key 1. solving that gives the byte sequence:

```text
50 41 4c 41
```

the lattice opcode uses a generated 16 by 8 system modulo 257. translating the decompiler exactly mattered because the matrix values are written through 16-bit truncation. solving the system gives the first eight bytes of key 1:

```text
50 41 4c 41 4e 54 49 52
```

those are the uppercase ascii bytes for the word palantir.

the key 2 math check gives this first-four-byte sequence:

```text
4e 42 47 59
```

i also checked the elliptic-curve branch. it uses the two 32-bit hashes, not extra input bytes, and it matches the intended hash pair above.

# false trail

because the hashes are only 32-bit, it is easy to make short colliding strings. for example, the earlier shortest printable-style collisions reached the intended hashes but decrypted the output to junk. this showed that the hash checks alone are not enough. the first capped bytes are also part of the output transform state.

# bytecode steering

the useful weakness is that the vm decrypts part of its own bytecode with the two input hashes. after offset `0x19a`, changing selected hash bytes changes the opcodes. no binary patch is needed.

for key 1, i chose the capped prefix:

```text
50 41 4c 41 4e 54 49 52 41 41 41 41 41 41 41
```

then i searched for four nonzero suffix bytes that make `hash1 ^ 0x7e9d3f1e` decrypt the bytes at vm offset `0x19a` as:

```text
99 0b
```

this jumps over the normal `p`, `r`, and `t` validation opcodes.

the suffix found was:

```text
f0 20 ff 0f
```

that gives:

```text
hash1 = 0x5fe4e2b1
```

for key 2, i chose the first 17 bytes:

```text
bf 2a f2 68 7c 41 41 41 41 41 41 41 41 41 41 41 41
```

the first five bytes were selected by inverting opcode `0x65` so that the output begins with the five success-check bytes:

```text
46 4c 41 47 7b
```

then i searched for four suffix bytes that make `hash2 ^ 0x3f6a8d2e` decrypt vm offset `0x1a7` as:

```text
65 70
```

that runs the key 2 output transform and then the print opcode.

the suffix found was:

```text
64 ab 23 ae
```

that gives:

```text
hash2 = 0x67cd649a
```

# validation run

i wrote this stdin file:

```text
50414c414e54495241414141414141f020ff0f0a
bf2af2687c41414141414141414141414164ab23ae0a
```

running the original executable with that stdin returns exit code 0 and prints the success line.

the bytes after the flag label are:

```text
46 4c 41 47 7b 0b 68 48 6c 3b 11 96 23 a2 56 a3 a8 d2 0d 0a 81 ed 6c 66 1f 8b e5 0d 0a 9c ca 28 f9 ec 08 96 f4 32 ce c9 1f 88 a6 7d dd db f8 98 0e 19 4c 6d 3e 82 32 78 18 8d a8
```

the buffer is not fully printable because the success opcode only checks the first five bytes before printing the whole buffer raw.

# reproduction steps

1. save the two key byte strings with a newline after each one.
2. run `p0tp.exe` with that file redirected to stdin.
3. check for the success line and the flag label.
4. if the terminal hides control bytes, redirect stdout and inspect the output as hex.

# unresolved notes

i recovered the stronger intended prefixes from the math checks, especially the first eight key 1 bytes. the full intended printable flag path still resists the simple array-based z3 model because the output preimage goes through the custom ksa and arx transforms. the submitted pair above is an unpatched accepted input path that reaches the success print by steering the hash-decrypted vm bytecode.
