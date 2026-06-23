# X-0-R by [steve_maxwell](https://crackmes.one/user/steve_maxwell) - [\[url\]](https://crackmes.one/crackme/6976041d9bf7b8997653a6cf)

Difficulty: 2.0

Language: Python (claimed C/C++)

Platform: Unix/linux

Arch: x86-64

---

Description:

Every byte has been nudged in the same way. Reversing the process is easier than
it looks.

---

Files:

- [chall](./files/challenge/chall)
- [flag.txt.enc](./files/challenge/flag.txt.enc) - the flag (encrypted)

---

## Running the Executable

```sh
> ./chall
Usage: python chall <filename>

> echo "test test test" > test
> ./chall test
Encrypted file saved as: test.enc
```

Clearly the program does some sort of encryption.

```sh
> cat test test.enc
─────┬──────
     │ File: test
─────┼──────
   1 │  test test test
─────┴─────
─────┬─────
     │ File: test.enc
─────┼─────
   1 │ sbts'sbts'sbts
─────┴─────
```

This looks like a static substitution cypher (e.g. XOR encryption with a single
byte, static key).

We are also provided the `flag.txt.enc`, so it's reasonable to assume that it is
an encrypted flag which we would need to decrypt.

Knowing the properties of bitwise XOR with a static key, it is a fair assumption
that this encryption program could also act as a decryption program, since:

`msg_enc ^ key ^ key = msg_enc ^ (key ^ key) = msg_enc ^ 0 = msg_enc`

Hence, running the same script on the encrypted flag file might decrypt it, if
a static key was indeed used:

```sh
> ./chall flag.txt.enc
Encrypted file saved as: flag.txt.enc.enc

> mv flag.txt.enc.enc flag.txt.dec
> cat flag.txt.dec
─────┬─────
     │ File: flag.txt.dec
─────┼─────
   1 │ CTFLearn{y0u_x0r3d_th3_c0d3}
─────┴─────
```

And there is our flag, without any need to even disassemble the program!

---

## Program Analysis

`Note: Pyinstxtractor and pycdc tools were used to decompile the program`

Disassembled, this program contains a lot of functions and calls that suggest
this binary is a python script, packaged using PyInstaller.

e.g.

```asm
lea     rdi, aPyiLinuxProces ; "_PYI_LINUX_PROCESS_NAME"
mov     rsi, r12
call    sub_409A50
jmp     loc_405365


[...]

lea     rdi, aCouldNotSideLo ; "Could not side-load PyInstaller's PKG a"...
mov     rsi, r13
mov     ebp, 0FFFFFFFFh
call    sub_4044F0
jmp     loc_4055ED
```

```sh
> strings chall | grep -i "pyinstaller"

Could not load PyInstaller's embedded PKG archive from the executable (%s)
Could not side-load PyInstaller's PKG archive from external file (%s)
PYINSTALLER_SUPPRESS_SPLASH_SCREEN
PYINSTALLER_STRICT_UNPACK_MODE
PYINSTALLER_RESET_ENVIRONMENT
_pyinstaller_pyz
```

This makes it harder to make sense of the program in a tool like IDA Pro, due to
the amount of irrelevant PyInstaller-generated code mixed in with the actual
encryption code. However, since it is essentially an archive, we can try to
extract it using tools like [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor.git):

```sh
> pyi_extractor chall
[+] Processing chall
[...]
[+] Successfully extracted pyinstaller archive: chall
```

Now that we have `chall.pyc`, we can decompile it into a pretty accurate
original python code, using a tool like [pycdc](https://github.com/zrax/pycdc?tab=readme-ov-file)
or a web decompiler like [PyLingual](https://pylingual.io/):

```sh
> pyc_decompiler chall.pyc > chall.py
```

Analysing the `chall.py`, the first relevant function appears to convert an
array of numbers (bytes) to an ASCII string:

```py
def __s(seq):
    r = []
    for c in seq:
        r.append(chr(c))
    return ''.join(r)
```

The next relevant function is the actual XOR encryption function:

```py
def __x(data, key):

    def __f(b = None):
        return b ^ key

    return bytes(map(__f, data))
```

This confirms that the program is performing a simple static XOR cypher against
some key.

The following function appears to be the main function for this program:

```py
def __c(arg):
    key = __k()
    h = __op(arg, 'rb')
    d = h.read()
    h.close()
    o = __x(d, key)
    out = __m(arg)
    h2 = __op(out, 'wb')
    h2.write(o)
    h2.close()
    __pt(f'''Encrypted file saved as: {out}''')
```

Pretty unambiguously it reads the provided file, calls `__x` (encryption
function) and then write the encrypted text to the output file.

The key here is retrieved from some `__k` function:

```py
    key = __k()
```

```py
def __k():
    return 7
```

This confirms that the key is just a constant 1-byte value (7 decimal).

## Program Summary

The program reads the file, provided as a command line argument, and encrypts its
contents statically against a key (7 decimal), using XOR encryption. The
encrypted text is then saved in a separate file with `.enc` extension.

## Solution

Now that we know how the program works, we can write a simple decryption script by
XORing the encrypted flag against the same key as the encryption program.

`Note: Hence, the provided binary is the decryption script itself. However, I
wrote the solution in C, for practice sake.`

```c
#include <stdio.h>

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");

    for (char c = fgetc(f); c != EOF; c = fgetc(f))
        putchar(c ^ 7);

    fclose(f);

    return 0;
}
```

```sh
> gcc solution.c -o solution

> ./solution ./files/challenge/flag.txt.enc
CTFLearn{y0u_x0r3d_th3_c0d3}
```

And there is our flag!

---

[Back to home](./../crackmes.md)
