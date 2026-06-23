(I stink at writing, AI sanity explanation)

# aj21h's Spaghetti

Crackme. UPX + custom VM. x86-64 Linux.

**TL;DR:** password is `in_the_beginning_there_was_the_flying_spaghetti_monster_and_it_was_delicious`, flag is `FLAG{the_flying_spaghetti_monster_would_be_proud}`. No patching — emulated the VM in Python and let Z3 chew on the input-dependent branches.

## Unpacking

`upx -d` got me a stripped dynamic ELF. I was on macOS so anything that needed to actually run went through Docker (`debian:stable-slim`). Static work was IDA 9.3 headless:

```bash
"/Applications/IDA Professional 9.3.app/Contents/MacOS/idat" \
  -A -c -ocrackme.i64 -Lida.log \
  -S"ida_dump.py ida_dump.txt" crackme.unpacked
```

First read of the unpacked binary made it obvious the "obfuscation" half of the description is a VM. There's a 0x1074cb-byte blob at `.data:0x6040` starting with the magic `HS->`, entry at `0xf959e`, dispatch loop at `sub_16F8`. The native side is a thin host — mode 1 reads a byte, mode 2 writes a byte, and that's basically it. All the logic is bytecode.

## VM

Stack machine. Pointers are 32 bits with the high byte as a segment id and the low 24 as an offset. The segments that matter:

- `1` — bytecode + static data
- `3` — local scratch
- `4` — heap-ish scratch where input lands

Wrote a disassembler and interpreter in Python. Opcode table I ended up with:

```
0x01        push imm
0x02/0x03   pick / poke
0x10-0x19   arith + unary
0x20-0x25   bitwise + shifts
0x30-0x39   compare
0x40-0x4f   direct VM call
0x50/0x51   skip if true / false
0x53        rel jump
0x57        ret
0x60-0x66   loads, stores, allocation
0x70/0x71   host read / write
```

Sanity check — does it actually run the program? The challenge hands you a pile of decoys to lean on:

```
test        -> This is not a test.
password    -> Hideous!
password123 -> You absolute donkey!
aj21h       -> Correct! Just kidding!
admin       -> This isn't that kind of challenge.
pasta       -> Warmer. Much warmer. Still wrong.
spaghetti   -> I'm not even mad. I'm just disappointed.
```

Author had fun with this one. Once my emulator was producing all of those from the right inputs, I trusted the interpreter and moved on.

## Finding the gate

Length fuzzing on non-decoy inputs surfaced two different rejection paths. Inputs with anything other than 76 bytes:

```
Wrong.
```

A 76-byte wrong input:

```
Wrong! You had one job. One!
```

So there's a length check gating the content check, and the password is 76 bytes long.

Traced a 76-byte run down to the success/failure split near VM `0xfc0bf`:

```
0xfc0bf: skip_if_true   ; true for my wrong input
0xfc0c0: jmp -> wrong
0xfc0c3: skip_if_true   ; false → falls into wrong
0xfc0c4: jmp -> wrong
0xfc0c7: success
```

The first condition was already true for my wrong 76-byte input. The second one was the real final content check; it also needs to be nonzero so the second `skip_if_true` skips the jump to the wrong path.

## Constraints

First instinct: point Z3 at the whole interpreter and walk away. That went about as well as you'd expect — VMs are not symbolic-execution friendly. Killed it and went concolic instead.

Run with a concrete 76 printable bytes. Keep Z3 bitvectors for those bytes propagated through every read/write into segment 4. In the Python emulator only, force the input-dependent branches that would otherwise reject toward "keep going," recording the symbolic constraint each forced branch implies. Hand the pile to Z3 at the end.

To be explicit on the rules: the forcing happens in my emulator so I can harvest the success-path constraints. The original packed binary stays untouched and is what ultimately verifies the answer.

Forced run produced 249 post-input branch conditions. Three were the length/newline checks I already knew about. The remaining 246 all had the same shape:

```
(((input[d] & 7) ^
  (((0xed6a3b68 * input[a] +
     0x622b7708 * input[b] +
     0x00611be8 * input[c] +
     input[d]) >> 16) & 7)) == target
```

Three bits of one byte XORed with three bits of a weighted sum of four bytes. Only bits 16..18 of the sum matter, only bits 0..2 of `input[d]` matter. Adding printable-ASCII bounds and reducing the model to 19-bit arithmetic made the solve effectively instant.

Z3 produced:

```
in_the_beginning_there_was_the_flying_spaghetti_monster_and_it_was_delicious
```

76 bytes. Right shape.

## Verifying against the original

```bash
printf '%s\n' 'in_the_beginning_there_was_the_flying_spaghetti_monster_and_it_was_delicious' \
  | docker run --rm --platform linux/amd64 -i \
      -v "$PWD":/challenge -w /challenge \
      debian:stable-slim ./crackme
```

```
Password:
Congrats. You found the meatball. Here's your flag. Respect.

FLAG{the_flying_spaghetti_monster_would_be_proud}
```
