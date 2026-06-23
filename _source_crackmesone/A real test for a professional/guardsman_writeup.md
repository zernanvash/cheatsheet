# guardsman.exe Writeup

Challenge_URL: https://crackmes.one/crackme/6a17349ed7ff92e1214c020d

## Overview

`guardsman.exe` is a 64-bit Windows crackme that asks for a password and prints
either `Correct password` or `Incorrect passord`. The password is not stored as
a simple plaintext string. Instead, the program derives it at runtime from a set
of bundled data files and then compares the generated value with the user's
input.

The valid password is:

```text
 eUIBPa98aIOJve647adsMKEWATq8qev 
```

Pay attention to the spaces: the password starts with `0x20` and ends with
`0x20`. Without those two spaces, the crackme rejects the input.

Target hash:

```text
SHA-256: 0B4C6853C3CE650A2B5F745A6C0648B648B4FD7D610693A756E5BB53B08FC31B
```

## Environment

I used Ghidra 11.4.2 for the static analysis. The binary is a PE32+ executable
compiled for `x86-64` Windows. It appears to be built with MinGW/libstdc++, so a
large part of the listing is C++ runtime and standard-library support code.

The crackme directory also contains several small binary files:

```text
a\a1      a\a1_H
a\a2      a\a2_H
a\a3      a\a3_H
a\b1      a\b1_H
a\b2      a\b2_H
a\b3      a\b3_H
a\c
b\a1      b\a2H
b\b1      b\b2H
b\c
c\data    c\hash
```

Those files are part of the validation logic, not leftover junk.

## Finding the Interesting Code

The first useful step was checking the defined strings. The following strings in
`.rdata` immediately stand out:

```text
1400e2088  7tguibjkTCYRs54s4rdtyvu()UY*978SE52p[xvzug876921frqfekmlRCTYlyu
1400e20c8  Enter the password:
1400e20de  \nCorrect password
1400e20f0  \nIncorrect passord
```

Cross-referencing `Enter the password:` leads to the main validation routine:

```text
1400db6e0  FUN_1400db6e0
```

There is also a small anti-debugging routine:

```c
void FUN_1400db6c0(void)
{
    if (IsDebuggerPresent() != 0) {
        exit(1);
    }
}
```

This check is simple and is not where the real protection lives. The useful
work is in `FUN_1400db6e0` and in a helper called from it, `FUN_14001a950`.

## Embedded File Names

Near `1400e203a`, the program stores a sequence of short strings. These strings
match the challenge's side-file layout:

```text
1400e203a  "a"
1400e203c  "a1"
1400e203f  "a1_H"
1400e2044  "a2"
1400e2047  "a2_H"
1400e204c  "a3"
1400e204f  "a3_H"
1400e2054  "b1"
1400e2057  "b1_H"
1400e205c  "b2"
1400e205f  "b2_H"
1400e2064  "b3"
1400e2067  "b3_H"
1400e206c  "c"
1400e206f  "data"
1400e2074  "hash"
1400e2079  "b"
1400e207b  "a2H"
1400e207f  "b2H"
```

The program builds paths from these fragments, reads the matching files, and
uses the hardcoded 63-byte string at `1400e2088` as an XOR key:

```text
7tguibjkTCYRs54s4rdtyvu()UY*978SE52p[xvzug876921frqfekmlRCTYlyu
```

## Understanding the Runtime Checks

Inside `FUN_1400db6e0`, the key string is copied into a local C++ string:

```c
FUN_1400c3ed0(&local_1e8, 0, 0,
    "7tguibjkTCYRs54s4rdtyvu()UY*978SE52p[xvzug876921frqfekmlRCTYlyu",
    0x3f);
```

The routine then reads data from the side files and applies an XOR transform.
Ghidra's output is noisy because of C++ string and filesystem wrappers, but the
core transform is straightforward:

```c
key_index = 0;
out_index = 0;

while (out_index < output_len) {
    b = output[out_index];

    if (b != '\n') {
        b ^= key[key_index];
        if (b != '\n') {
            output[out_index] = b;
        }
    }

    key_index++;
    out_index++;

    if (key_index == key_len) {
        key_index = 0;
    }
}
```

One intermediate result is compared against this ASCII value:

```text
16347830079011800400
```

In the decompiler this appears as little-endian constants followed by a
`memcmp`:

```c
*pppuVar7      = 0x3033383734333631;
pppuVar7[1]    = 0x3831313039393730;
*(uint *)(...) = 0x30343030;

if (local_710 == 0x14) {
    ok = memcmp(local_718, pppuVar7, local_710) == 0;
}
```

This confirms that the program is deriving values from the bundled data files
instead of simply comparing against a fixed plaintext string.

## Final Password Comparison

The final password is produced by `FUN_14001a950`:

```c
uVar9 = FUN_14001a950(&local_248, &local_8a8, local_428);
```

Immediately after this call:

```text
local_8a8 = pointer to expected password
local_8a0 = expected password length
local_888 = pointer to user input
local_880 = user input length
```

The important decompiled block is:

```c
FUN_1400d4b60(&cout, "Enter the password:  ", 0x15);
FUN_1400d6570(&cin, &local_888, delimiter);

if ((local_8a0 == local_880) &&
    ((local_8a0 == 0 ||
      memcmp(local_8a8, local_888, local_8a0) == 0))) {
    FUN_1400d4b60(&cout, "\nCorrect password", 0x11);
}
else {
    FUN_1400d4b60(&cout, "\nIncorrect passord", 0x12);
}
```

The corresponding disassembly makes the stack variables clear:

```text
1400dc2d8  mov r8, qword ptr [rsp + 0xa8]   ; expected length
1400dc2e0  cmp r8, qword ptr [rsp + 0xc8]   ; user input length

1400dc394  mov rdx, qword ptr [rsp + 0xc0]  ; user input pointer
1400dc39c  mov rcx, qword ptr [rsp + 0xa0]  ; expected password pointer
1400dc3a9  call memcmp

1400dc3b6  print "\nCorrect password"
```

At this point the protection is essentially solved. The program has already
calculated the expected password, and the final check is a normal length check
plus `memcmp`.

To recover the answer, break immediately before the final `memcmp`, for example
at `1400dc394`, and dump:

```text
qword ptr [rsp + 0xa0]  ; expected password buffer
qword ptr [rsp + 0xa8]  ; expected password length
```

The expected length is `0x21`, or 33 decimal. Dumping 33 bytes from the expected
password buffer gives:

```text
20 65 55 49 42 50 61 39 38 61 49 4f 4a 76 65 36
34 37 61 64 73 4d 4b 45 57 41 54 71 38 71 65 76
20
```

Converted to ASCII:

```text
 eUIBPa98aIOJve647adsMKEWATq8qev 
```

The first byte and the last byte are both `0x20`, which is why the password must
be entered with leading and trailing spaces.

## Verification

Correct input:

```text
 eUIBPa98aIOJve647adsMKEWATq8qev 
```

Expected output:

```text
Enter the password:
Correct password
```

Incorrect input without the spaces:

```text
eUIBPa98aIOJve647adsMKEWATq8qev
```

This fails because the length is 31 instead of 33, so the program reaches the
failure branch and prints:

```text
Incorrect passord
```

## Conclusion

The crackme hides the password by deriving it from several side files and a
hardcoded XOR key. The most efficient route is to identify the final comparison
instead of fully reimplementing every C++ filesystem and string operation. At
the final `memcmp`, the expected password is already present in memory, with
its length stored next to it on the stack.

Final password:

```text
 eUIBPa98aIOJve647adsMKEWATq8qev 
```
