# deo's High cortisol

Challenge_URL: https://crackmes.one/crackme/6a25ae31e13aafcf3f84fa7b

## summary

the key is:

```text
xQ9_vP4_tK2_mZ8
```

running the program with that key prints:

```text
>>> MBB <<<
[!] Enter The Key : DECRYPTED FLAG: FLAG{78hm4352rg425g08u,jk43f178yhn2376bfrt}
```

## target

file: `mbb.exe`

sha256:

```text
dd0a85b1c5d8e3b38af1298bf1c7fd7fb28be3947d06bfe5e618ee81c6e88f40
```

the file is a 64 bit windows console pe. the first static pass showed no normal import table, high entropy sections, and a small loader style entry point, so i treated it as packed and avoided starting with a full decompiler view.

## first look

i started with basic file triage, then opened the sample in rizin. the original entry point was not the real program. it used manual mapping, page protection changes, and a lot of opaque arithmetic using values like `0xdeadbeef`, `0xcafebabe`, and `rdtsc`.

the useful moment was after unpacking. with a runtime trace on `virtualprotect`, i dumped the pages when the program made them readable or executable. the important recovered ranges were:

```text
0x140001000  code
0x140034000  strings and runtime pointers
0x140049000  later payload data
```

i rebuilt those dumped ranges into a flat image at base `0x140000000` and used that as the main static target.

## finding the real code

the recovered image had the visible strings:

```text
0x1400343e0  >>> MBB <<<
0x1400343f0  [!] Enter The Key :
0x140034430  DECRYPTED FLAG:
```

the prompt is referenced at `0x140005636`. the success string is referenced at `0x140025773`.

wrong input reached several repeated state-machine blocks and then stopped before the final print. tracing checkpoints showed the input bytes appear in the state around `0x140017bcc`, and the last useful wrong-key block was near `0x14002186a`.

that block allocates memory, copies `0x607` bytes from `0x140049000`, and later uses it as executable code. that copied blob was the cleanest part of the challenge.

## unpacking the copied payload

the copied payload begins with a decoder:

```asm
lea rdi, [rip+0x29]      ; 0x140049039
mov ecx, 0x5ce
mov r8b, 0xaa
mov r9b, 0x55
decode:
    xor byte ptr [rdi], r8b
    add r8b, r9b
    xor r9b, 0x13
    inc rdi
    dec rcx
    jne decode
```

after applying that, the payload turns into a small vm interpreter. the interpreter then decodes its bytecode at `0x14004939a`:

```asm
lea rdi, [0x14004939a]
mov ecx, 0x26d
mov r8b, 0x55
decode2:
    xor byte ptr [rdi], r8b
    add r8b, 0x13
    xor r8b, 0x37
    inc rdi
    dec rcx
    jne decode2
```

the decoded vm bytecode starts like this:

```text
03 02 24 00 00 00
01 03 00 02 00 00 00 00 00 00
07 00 02 03
08 0a 00 00 00
0e 24 02 00 00 49 00 00 00 aa
00
```

translated, that is:

```text
r2 = bytecode + 0x24
r3 = 0x200
compare r0, r2, r3
if compare failed, skip 0x0a bytes
xor-decode stage at bytecode+0x224, length 0x49, key 0xaa
halt
```

so the vm first compares a 512 byte derived buffer against a 512 byte constant. if the compare passes, it decodes a second bytecode stage.

the second stage is:

```text
r0 = bytecode + 0x1d
r2 = bytecode + 0x1d
r3 = 0x2c
rc4(dst=r0, src=r2, len=r3, key=r1, key_len=r4)
halt
```

that means the user key itself is later used as the rc4 key for the flag ciphertext, but before that the outer program has to pass the 512 byte comparison.

## the rsa check

right after the vm payload there is a public rsa key blob:

```text
0x140049610  rsa1
bit length   0x1000
exponent     00 00 00 03
modulus len  0x200
```

the exponent is `3`. the 512 byte value used by the vm compare is almost all zero. only the last 45 bytes are nonzero:

```text
1a93aed762ce27c214d1878e84b0b724964ff5edc032f27fe352d69c5cdd1367f272c1b85a201ceff6fe4e2e00
```

because the value is tiny compared with the 4096 bit modulus, the rsa operation did not wrap modulo n. that means:

```text
c = key^3
```

so the key can be recovered with an exact integer cube root.

the cube root is:

```text
7851395f7650345f744b325f6d5a38
```

as ascii, that is:

```text
xQ9_vP4_tK2_mZ8
```

## small recovery script

this is the important part of the script i used after dumping and decoding the vm bytecode:

```python
with open("mbb_blob_decoded2.bin", "rb") as f:
    data = f.read()

bytecode = data[0x39a:0x39a + 0x26d]

c = int.from_bytes(bytecode[0x24:0x224], "big")

def iroot3(n):
    lo, hi = 0, 1
    while hi ** 3 <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo

key_int = iroot3(c)
assert key_int ** 3 == c

key = key_int.to_bytes((key_int.bit_length() + 7) // 8, "big")
print(key)
```

output:

```text
b'xQ9_vP4_tK2_mZ8'
```

## validation

final run:

```text
mbb.exe
>>> MBB <<<
[!] Enter The Key : xQ9_vP4_tK2_mZ8
DECRYPTED FLAG: FLAG{78hm4352rg425g08u,jk43f178yhn2376bfrt}
```

## notes

the main trick was not to fight the flattened outer state machine forever. the copied payload at `0x140049000` was much smaller and explained the whole design:

```text
packed outer program
  -> derives a 512 byte rsa result from the input
  -> vm compares that result against a constant
  -> if it matches, vm uses the input as an rc4 key
  -> rc4 decrypts the flag string
```

the weak point is the rsa exponent. since `e = 3` and the target value is smaller than the modulus, the correct input is just the exact cube root.