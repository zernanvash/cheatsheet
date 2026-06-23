# CrackMe One Writeup

Challenge_URL: https://crackmes.one/crackme/6a1daa532b3df128c1df5d3f

## Metadata

- Target: `/Users/singularity/Downloads/crack/crackme.exe`
- SHA-256: `7439b0fdf55c3bd169fde2c888210a64826b9803774dc078a3538aa80188772b`
- Format: PE32+ console executable, x86-64, Windows
- Tools: IDA Pro MCP, `x86_64-w64-mingw32-objdump`, Wine, Python
- Goal: generate the correct 16-character serial for any accepted username

## Summary

The program asks for a username and a serial. The serial is not fixed; it is derived from the username by a deterministic 64-bit mixing routine. The expected serial is a 16-character hexadecimal string.

Example valid pairs:

```text
username: test
serial:   E7097F10E14820BB

username: admin
serial:   6F734C07FEBA5004
```

A standalone keygen is included as `keygen.py`:

```bash
python3 keygen.py admin
# admin: 6F734C07FEBA5004
```

## Triage

IDA identified the binary as a 64-bit PE console program with image base `0x140000000`. The main challenge logic is in `sub_140001180`.

Useful strings:

- `0x1400195a8`: `Username:`
- `0x1400195d8`: `Serial  :`
- `0x1400195e8`: `[X] %s`
- `0x1400195f0`: `[+] %s`

The program uses basic console APIs and anti-debug checks (`IsDebuggerPresent`, `CheckRemoteDebuggerPresent`), but the serial check itself is static and can be recovered without patching.

## Input Validation

At `sub_140001180`, after reading both fields:

- Username length must be from 4 to 32 bytes.
- Username characters must be letters, digits, `.`, `_`, or `-`.
- Serial length must be exactly 16.
- Serial characters must be hexadecimal digits.
- The serial text is parsed as a base-16 unsigned 64-bit integer.

The comparison occurs at:

```asm
140001709  call    sub_140001A40
140001715  cmp     rax, rsi
140001718  jne     invalid_serial
```

Here `rsi` is the parsed serial and `rax` is the expected value generated from the username.

## Algorithm

The program first mixes the username bytes:

```c
uint64_t a = 0x0123456789ABCDEF;
uint64_t b = 0xFEDCBA9876543210;

for (i = 0; i < username_len; i++) {
    uint8_t ch = username[i];

    b = ror64(b, 3) ^ ch;

    uint64_t x = (uint64_t)ch << ((i % 7) * 8);
    x = (x ^ a) * 0x100000001B3;

    b += x;
    a = b;
    b = ~b - 0x61C8864E7A143579;
    a ^= x;
}

uint64_t h = mix64(a ^ b);
```

Then it folds in character class counts:

```c
uint32_t letters = count_alpha(username);
uint32_t digits  = count_digits(username);
uint32_t other   = username_len - letters - digits;

uint64_t v = letters;
v = (v << 16) ^ digits;
v = (v << 16) ^ other;
v = (v << 16) ^ h;
v += username_len * 0x12345678;

serial = mix64(v);
```

`mix64()` is implemented at `sub_140001A40`. It substitutes each byte through the AES S-box table at `0x140019410`, then applies four 32-bit rotate/add/xor rounds. The exact recovered implementation is in the included `keygen.py`.

## Validation

The generated serial for `admin` was tested against the real binary under Wine:

```text
Username: admin
Serial  : 6F734C07FEBA5004

[+] Registration Successful!
```

No binary patching was required.

