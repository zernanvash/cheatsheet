# NeuroVault Crackme Write-Up

Challenge_URL: https://crackmes.one/crackme/6a0368f48fab7bbca2730160

## Entry Point and Runtime Setup

The apparent entry point only performs CRT/runtime initialization and then eventually reaches the program controller.

The important transition is:

```asm
start
  -> sub_7FF78DAA1020
  -> sub_7FF78DAA4160
```

The first meaningful function is:

```asm
sub_7FF78DAA4160
```

This function performs anti-tamper setup, initializes encoded data, and dispatches several logic stages through a function pointer table.

## Dispatcher

The main logic uses a function pointer table at `off_7FF78DAA6060`:

```asm
dq offset sub_7FF78DAA1A20
dq offset sub_7FF78DAA1DB0
dq offset sub_7FF78DAA2010
dq offset sub_7FF78DAA2290
```

These functions roughly correspond to:

| Function           | Purpose                          |
| ------------------ | -------------------------------- |
| `sub_7FF78DAA1A20` | Print intro/prompt text          |
| `sub_7FF78DAA1DB0` | Read user input and uppercase it |
| `sub_7FF78DAA2010` | Decoy serial check               |
| `sub_7FF78DAA2290` | Real VM-based serial check       |

The program passes a shared input buffer and a stop flag into each function. If the stop flag is set, later stages are skipped.

## Decoy Check

`sub_7FF78DAA2010` checks for this format:

```text
NV-XXXXXXXX-VAULT
```

where `XXXXXXXX` must be eight hexadecimal characters.

It then sums the eight hex nibbles and applies this condition:

```asm
imul    eax, ecx, 0FEFEFEFFh
add     eax, 37373737h
cmp     eax, 1010100h
ja      fail
```

For valid hex nibble sums, this condition is satisfied only when the sum is:

```text
55
```

A decoy-valid serial would therefore be:

```text
NV-77777776-VAULT
```

because:

```text
7 + 7 + 7 + 7 + 7 + 7 + 7 + 6 = 55
```

However, this is not the real solution. If this check passes, it sets the stop flag, preventing the real validator from running.

## Real Validator

The real check is implemented in `sub_7FF78DAA2290`.

It again expects the same serial format:

```text
NV-XXXXXXXX-VAULT
```

The eight hex characters are decoded into four bytes:

```text
XXXXXXXX -> b0 b1 b2 b3
```

Then a small stack-based VM evaluates a bytecode program. The relevant bytecode was recovered as:

```text
05 00 05 01 02 01 A4 06
05 02 05 03 03 01 01 06 07
05 00 01 04 04 01 E4 06 07
05 01 05 02 09 01 20 06 07
05 03 05 00 0B 01 E3 06 07
08
```

The VM opcodes include operations such as:

| Opcode | Meaning         |
| -----: | --------------- |
|   `01` | Push immediate  |
|   `02` | Add             |
|   `03` | XOR             |
|   `04` | ROL             |
|   `05` | Push input byte |
|   `06` | Equal           |
|   `07` | AND             |
|   `08` | End/check       |
|   `09` | Multiply        |
|   `0B` | Subtract        |

The bytecode translates into these constraints:

```text
b0 + b1      == 0xA4
b2 ^ b3      == 0x01
ROL8(b0, 4)  == 0xE4
b1 * b2      == 0x20
b3 - b0      == 0xE3
```

Solving them gives:

```text
b0 = 0x4E
b1 = 0x56
b2 = 0x30
b3 = 0x31
```

As an eight-character hex string:

```text
4E563031
```

## Final Serial

Putting the solved hex block back into the required format gives:

```text
NV-4E563031-VAULT
```

This serial avoids the decoy path and satisfies the VM-based real validator.
