# CrackMe.obf.exe Writeup

Challenge_URL: https://crackmes.one/crackme/69b1ff67ddd6176826ae8960

## Initial Triage

The first pass in IDA was intentionally misleading:

- imports were effectively hidden,
- early functions disassembled as garbage,
- normal string searches mostly returned CRT/runtime noise.

The real entry point is a small loader stub. After following the PE entry and the `start` routine, I found that the program decrypts a large region of its own code before transferring control to the real program logic.

### Self-decryption stub

At `0x1400AB562`, the loader walks a single decryption descriptor and XOR-decrypts the code region:

- start: `0x140001000`
- size: `0x59906`
- multiplier: `0x9BDDC5AF`
- seed: `0xE512BC01`

The algorithm is:

```c
state = seed;
for (i = 0; i < size; i++) {
    buf[i] ^= state & 0xFF;
    state = (seed + multiplier * state) & 0xFFFFFFFF;
}
```

I reproduced that directly in IDA with a script, patched the decrypted bytes back into the database, undefined the previously wrong items, and let IDA reanalyze the region. After that, the code became readable again.

## Finding the User-Facing Logic

Once the decrypted region was analyzed, the program flow became much clearer.

I located a family of short string-decryption stubs around `0x14009FA31` through `0x1400A34C5`. These routines all use the same pattern:

- decode a short encrypted string once,
- cache it,
- jump into a normal caller.

The most useful strings were:

- `0x14009FD79` -> `Enter Password: `
- `0x14009FE05` -> `Correct`
- `0x14009FE91` -> `Incorrect`

Those three functions lead directly into the password handling logic around `0x14000AA80`.

## The Validation Loop

The important code is the loop around `0x14000AB8B`.

The program reads the input into a `std::string`-like buffer, then iterates over the user-supplied bytes. During each iteration it only uses:

- the current input byte,
- the low byte of a qword from a table at `0x14005B000`,
- the low byte of a qword from a table at `0x14005B0B0`.

The core check is effectively:

```c
acc = 0;
for (i = 0; i < input_len; i++) {
    acc |= input[i] ^ table1[i % 21] ^ table2[i];
}

if (acc == 0)
    print("Correct");
else
    print("Incorrect");
```

The slightly ugly arithmetic in the loop is just a compiler-generated way to compute `i % 21`.

### Table bytes

Extracting only the low bytes from the first table gives:

```text
53 c4 ea 6f 91 4d d9 4a 1f dd f3 b2 20 fb 2d cc d3 d4 71 f2 17
```

Extracting the low bytes from the second stream and XORing them against the first table produces the expected password characters.

## Recovering the Password

Running the XOR recovery gives the printable candidate:

```text
Y38GH3bJKSmbD3pijZ1h1oNAWCVQydPG
```

That string works as the full password.

## Important Bug: Prefixes Also Pass

The crackme has a logic bug: it never enforces the intended length.

The loop only checks the bytes that were actually provided. If the user enters a correct prefix, the accumulator still stays zero and the program prints `Correct`.

That means all non-empty valid prefixes are accepted, including the shortest one:

```text
Y
```

So:

- intended full password: `Y38GH3bJKSmbD3pijZ1h1oNAWCVQydPG`
- shortest accepted input due to the bug: `Y`

## Runtime Confirmation

After solving it statically, I confirmed the result under CrossOver (without using a debugger):

- `Y38GH3bJKSmbD3pijZ1h1oNAWCVQydPG` -> `Correct`
- `Y` -> `Correct`
- `wrong` -> `Incorrect`

This matched the static analysis exactly.

## Optional Easy Goal: Always Print `Correct`

If the patching goal is desired, the easiest patch is to redirect the failure branch to the success string routine:

- failure path jumps to `0x14009FE91` (`Incorrect`)
- success path jumps to `0x14009FE05` (`Correct`)

The branch site is around `0x14000AC84`.

## Final Answer

Full recovered password:

```text
Y38GH3bJKSmbD3pijZ1h1oNAWCVQydPG
```

Shortest accepted prefix because of the bug:

```text
Y
```
