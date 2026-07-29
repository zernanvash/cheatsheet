# FlipVM crackme writeup

Challenge_URL: https://crackmes.one/crackme/69dc3b32b38f9259eec7eb56

## Result

Password:

```text
$?$__LeT_Th#_h@ck!ng_b3g1n__$?$
```

Flag:

```text
CMO{<-~~-~~~~-.1'm++In.-~~~~-~~ ->}
```

## Files

The challenge contains a tiny custom loader/interpreter and a bytecode file named `code.flp`.
The bytecode file begins with an `FLP` header:

```text
magic  : 3 bytes, "FLP"
N      : 128 bytes, little endian
E      : 3 bytes, little endian
sig    : 128 bytes, little endian
xor    : 4 bytes, little endian
code   : remaining bytes
```

The native executable is intentionally minimal and maps/dispatches a custom VM.  The interesting logic is in the `.flp` bytecode rather than in normal x86-64 functions.

## VM level idea

The program prints a banner and reaches a password check implemented inside the VM.  The check does not compare the plaintext directly.  Instead, it mutates the password through a 0x100-round reversible transform.

Each round uses the next low byte from a huge constant called here `atlas`:

1. expand that byte across a 20-byte XOR word
2. XOR it into the low part of the current 31-byte password integer
3. rotate the 31-byte integer right by one bit
4. shift the atlas to the next byte

The inverse does the opposite order:

1. pre-extract the 0x100 atlas bytes
2. rotate the 31-byte integer left by one bit
3. XOR with the atlas byte in reverse order

This is implemented in `keygen.py` as `mutate()` and `restore()`.

## Keygen

Run:

```bash
python3 keygen.py
```

Expected output includes:

```text
password : $?$__LeT_Th#_h@ck!ng_b3g1n__$?$
flag     : CMO{<-~~-~~~~-.1'm++In.-~~~~-~~ ->}
check    : PASS
```

## Patch

The patcher modifies `code.flp`, not the native VM binary.  It injects a small VM stub immediately before the mutation/check routine:

```text
MODE 1
MOV R0, "$?$__LeT_Th#_h@ck!ng_b3g1n__$?$"
```

Then it sets the FLP entrypoint to the injected block and rebuilds the header using the VM's modified FNV-like hash/signature scheme.

Run:

```bash
python3 patch.py code.flp patched.flp
./FlipVM patched.flp
```

The patched bytecode should skip manual password entry by preloading the correct value into the VM register used by the checker.

## Why this works

The protection is split into two layers:

1. encryption/verification at rest in the `.flp` container
2. password mutation inside the VM

Once the VM bytecode format is understood, the challenge is not about brute force.  The mutation is reversible, and the header can be rebuilt after patching.  The valid password is therefore recovered and can also be injected directly into the VM state.
