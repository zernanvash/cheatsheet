# The Alchemist's Lock Writeup

Challenge_URL: https://crackmes.one/crackme/69adaa15fbfe0ef21de946bd

Хорошо, переводю:

---

**CodeBrewBeans's The Alchemist's Lock**
https://crackmes.one/crackme/69adaa15fbfe0ef21de946bd

**Tools used:** x64dbg with Scylla plugin, IDA Pro, Detect-It-Easy

Using Detect-It-Easy, we determine that the binary is packed. The packer name could not be identified.

We open x64dbg and search for the OEP, which is found at `00007FF76ACC1D47`. Using Scylla, we dump the unpacked binary.

We begin analysis in IDA Pro. Most of the function calls handle string output and user input (name and password). At the end of the main logic, we find a conditional jump `jz short loc_7FF76ACC22F7` following the comparison `cmp rax, [rbp+260h+var_A8]`, which leads to the flag output. This means the function above is responsible for processing the password.

We launch the debugger using "Tom" as the name and "1111" as the password:

```
00007FF756B12279  call  7FF756B117DC        ; computes a value from name and password
00007FF756B1227E  mov   [rbp+1C0], rax      ; result stored on stack
00007FF756B12285  mov   rax, 52E85B18B8EFE7A6  ; magic constant loaded
00007FF756B1228F  mov   [rbp+1B8], rax      ; constant stored on stack
00007FF756B12296  mov   rax, [rbp+1C0]      ; function result back into rax
00007FF756B1229D  xor   rax, [rbp+1B8]      ; XOR with magic constant
00007FF756B122A4  mov   [rbp+1B0], rax      ; XOR result stored
00007FF756B122AB  mov   rax, [rbp+1C0]      ; function result back into rax
00007FF756B122B2  cmp   rax, [rbp+1B8]      ; compare against 52E85B18B8EFE7A6
```

If they are equal, the flag is printed as-is. Otherwise, the program corrupts it. Dynamic analysis confirmed that `[rbp+1B0]` — the XOR result — is used as the encryption key for the flag. Therefore, only the return value of `7FF756B117DC` matters.

By analyzing function `7FF756B117DC`, we can reconstruct its logic in Python:

```python
def rol(x, k):
    k %= 64
    return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

def compute_magic(name, password):
    acc = 0
    res = 0
    for s in (name, password):
        L = len(s)
        for _ in range(L):
            for c in s:
                acc = (acc + ord(c)) & 0xFFFFFFFFFFFFFFFF
            acc = rol(acc, 15)
            acc = (acc * 139) & 0xFFFFFFFFFFFFFFFF
            acc = (acc >> 2) + 4
            acc &= 0xFFFFFFFFFFFFFFFF
            res = (res + acc) & 0xFFFFFFFFFFFFFFFF
    return res
```

The reconstruction was verified against multiple name/password pairs using the debugger — all results matched.

However, the function is not analytically invertible. The only remaining option is brute force. After an hour of brute-forcing with no result on a low-end machine, this approach was abandoned.

The crackme was solved by patching the conditional jump from `jz short loc_7FF76ACC22F7` to `jnz short loc_7FF76ACC22F7`, which forces execution to always take the success branch regardless of input.

**FLAG_R3v3rs3d**