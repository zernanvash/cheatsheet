# SimpleCrackMeForBeginners_ByKakao Writeup

Challenge_URL: https://crackmes.one/crackme/6a2471b2ee3223161ea298e9

## Summary

The correct key is an 8-byte non-printable byte string:

```text
64 54 16 B9 DA 78 AA 3F
```

In escaped shell form for Wine/bash:

```bash
$'dT\x16\u00b9\u00dax\u00aa?'
```

No patching is required. With the correct key, the original executable prints:

```text
ok
```

## Metadata

- File: `SimpleCrackMeForBeginners_ByKakao.exe`
- SHA-256: `5b29e05a326cbcb7d37be097322d2ac7e33b213f7b1b713a810757dc93983ec5`
- Format: PE32+ x86-64 console executable
- Platform: Windows x64
- Output strings: `usage: %s key`, `err`, `ok`

## Initial Behavior

The program expects one command-line argument:

```text
CrackMe.exe <key>
```

Running without arguments prints usage. Running with a wrong key prints `err`:

```bash
WINEDEBUG=-all MVK_CONFIG_LOG_LEVEL=0 wine SimpleCrackMeForBeginners_ByKakao.exe 1234
```

Output:

```text
err
```

## Unpacking

The executable has a decrypted-at-startup code section named `.NiTiNOL`. On disk this section does not disassemble cleanly. A pre-CRT stub locates the section, changes its protection with `VirtualProtect`, XOR-decrypts it, then restores execute/read protection.

The decrypt loop is:

```c
for (i = 0; i < section_size; i++)
    section[i] ^= key[i & 0x1f] ^ ((i * 0x6d) & 0xff);
```

The 32-byte key table is at virtual address `0x1401F79E0`. I used [unpack_simple_kakao.py](/Users/singularity/Documents/Codex/2026-06-08/i-like-to-reverse-engineer-apps/work/unpack_simple_kakao.py) to produce:

[SimpleCrackMeForBeginners_ByKakao.unpacked.exe](/Users/singularity/Documents/Codex/2026-06-08/i-like-to-reverse-engineer-apps/outputs/simple_kakao/SimpleCrackMeForBeginners_ByKakao.unpacked.exe)

The unpacked `main` at `0x1402064B0` sets up a context containing `argc`, `argv`, and a return slot, then calls the flattened checker at `0x140211420`.

## Checker Structure

The flattened checker uses a function-pointer table at `0x1401F79B0`. Important entries are:

```text
0x140210C00  anti-debug / PEB / timing check
0x140210D70  page-byte anti-patch check
0x140210F10  printf wrapper
0x140211030  key-processing wrapper
0x140211160  printf wrapper
0x140211270  printf wrapper
```

The message pointers are:

```text
0x1401F7998 -> usage: %s key
0x1401F79A0 -> ok
0x1401F79A8 -> err
```

The key-processing wrapper at `0x140211030` passes `argv[1]` to `sub_140206260`. That helper runs a small VM. The VM first checks that the key pointer is non-null, then measures the string length. The length comparison requires exactly 8 bytes.

## Digest Recovery

The first VM packs the 8 input bytes into a big-endian qword. For example:

```text
"ABCDEFGH" -> 0x4142434445464748
```

It then calls a second VM-backed mixer, `sub_140206000`, and compares the returned 64-bit digest against:

```text
0xF4D1A2C3B5E60718
```

Concrete traces confirmed:

```text
f(0x4142434445464748) = 0xBDDF043A64C94765
f(0x4141414141414141) = 0xFDF84335934547DC
```

I used a strict Unicorn harness, [emulate_simple_kakao_strict.py](/Users/singularity/Documents/Codex/2026-06-08/i-like-to-reverse-engineer-apps/work/emulate_simple_kakao_strict.py), to model the unpacked binary without skipping the actual checker helpers. It only stubs environmental edges such as `__alloca_probe`, internal printf, and anti-debug/timing helpers.

Then I used angr on only `sub_140206000(rcx)` with symbolic `rcx` and the constraint:

```text
return_value == 0xF4D1A2C3B5E60718
```

angr's model was checked against the Unicorn concrete traces above. Solving the target digest produced:

```text
0x645416B9DA78AA3F
```

As bytes:

```text
64 54 16 B9 DA 78 AA 3F
```

## Validation

The strict emulator validates the raw-byte key:

```text
645416b9da78aa3f ['ok\n'] 0x0
```

The original binary also validates under Wine. Because the key contains non-printable and non-ASCII bytes, I passed it through bash ANSI-C quoting using Unicode characters that MSVCRT converts back to the intended byte values:

```bash
WINEDEBUG=-all MVK_CONFIG_LOG_LEVEL=0 wine /Users/singularity/Downloads/SimpleCrackMeForBeginners_ByKakao.exe $'dT\x16\u00b9\u00dax\u00aa?'
```

Output:

```text
ok
```

## Final Answer

Submit the key as raw bytes:

```text
64 54 16 B9 DA 78 AA 3F
```

Escaped representation:

```text
dT\x16\xb9\xdax\xaa?
```
