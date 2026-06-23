# leet_echo_chamber - writeup

so this one's the followup to whatever the author's previous crackme was. the description says "find the elite superior number that will reflect itself into the result" which is just a fancy way of saying "find a fixed point of this hash". echo chamber, input == output. simple to state.

answer up front in case you don't want to read the rest: **`133742069`**.

## first look

64-bit windows PE, around 64KB, 155 functions. nothing weird about the section names, no obvious packer or protector, all the section permissions are normal. compiled with msvc, normal ucrt imports. tossed it into ida and let auto-analysis settle.

main lives at `0x1400089c0` and is 3.6KB which is already a lot for a "type a number, get a number" challenge. so something nontrivial is going on.

string-wise there's basically nothing interesting:

```
"Enter activation number:\n"
"result: %u\n"
```

both xref from main exactly once. the rest of the strings are CRT plumbing. the `.data` segment starts with sixteen `0x09` bytes which ida labels as a tab-string but it's really just a seed table for the init code.

## what input does it want

before doing anything clever I checked the input parser, since "find a number" challenges are very sensitive to input format. parser is at `sub_140004AB0`, and underneath it `sub_140004630` does the actual digit work:

```c
if (*a1 == '0') return 0;          // no leading zero
for (int i = 0; i < 9; ++i) {       // exactly 9 digits
    char c = a1[i];
    if (c < '0' || c > '9') return 0;
    v5 = 10 * v5 + (c - '0');
}
```

so the input has to be exactly 9 digits and can't start with zero. the example in the task description ("input 133, output 133") is just illustrative because the binary itself would reject a 3-digit input. real range is `100000000` to `999999999`, which is 900 million possible inputs.

ran a few of them through to see what the output looks like:

```
100000000 -> 1530092063
123456789 -> 2604172925
133713371 ->  695859664
999999999 ->  468757550
987654321 -> 2757081589
```

outputs span the full uint32 range and look uniformly distributed. since the output is 32-bit and the input is effectively 30-bit, you'd expect roughly 0.2 fixed points on average if the hash is well-mixed. so there might or might not be one in this particular instance, but the description guarantees there is, so we're looking for it.

## the rabbit hole

main does, in order:

1. seven init functions (deterministic, don't depend on input)
2. read line, parse, store input integer in `dword_14000D2CC`, scatter input digits and derivatives into a bunch of state bytes
3. 32-iteration loop calling `sub_140005AB0(i)` with the round number
4. ~200 lines of post-loop XOR / rotate / mod-9 stuff
5. compute `v35` and printf it

`sub_140005AB0` is the per-round hash and it is rough. like 200 local variables when decompiled, four-entry function pointer dispatch table that gets indexed by round state, three different places that can call into `sub_140003CA0` (which I figured out was a state-mutation panic function), pieces that read from D248, D250, D258, D260, D264, the 32-byte D278 array, the 8-dword D298 array, D2A4..D2B4, the 16-byte D2B8 array. basically every state byte in the data section gets touched.

I started reading this carefully and gave up after maybe ten minutes. it's all rotations, XORs, mod-9 arithmetic on permutation tables, and conditional jumps based on round state. there's no obvious linear structure to invert.

at this point the options were:

- **brute force**: 9e8 inputs, ~50ms per process spawn, that's around 14 months on a single core. no.
- **reimplement in C**: copy the decompilation, fix it up, compile. probably half a day of work and very easy to introduce a single off-by-one that makes the whole thing return the wrong number forever. not great.
- **z3 / symbolic**: maybe, but the dispatch table makes the path explosion ugly.
- **find a static shortcut**: ideal if it exists.

I went looking for the shortcut.

## the constant

scrolling through main's tail end I hit this:

```c
v40 = sub_140001A10();
v34 = v59 + ~v40 + 1;
```

`v59` is `dword_14000D2CC`, the input integer. `~x + 1` is just `-x`. so `v34 = input - v40`. what's `v40`?

```c
__int64 sub_140001A10() {
    return 133742069;
}
```

four bytes of code, no parameters, no state, no nothing. just returns a constant. and the constant is `133742069`, which reads as `1337` followed by `42069`. leet plus the other internet number. that's the "elite superior number" the description was advertising.

I had a strong suspicion right there but I wanted to actually understand why it works before testing. partly because guessing feels bad and partly because I wanted to know what would happen if you pick a number that's NOT the magic one - is the binary going to claim some other thing is correct? is there a second fixed point I'd miss?

## the math

after `v34` gets computed, main does:

```c
v60 = rol(v34,  9) ^ v34;
v37 = rol(v34, 21) ^ v60;
```

`v37` is just `rol(v34, 21) ^ rol(v34, 9) ^ v34`, an XOR of three rotations. for `v34 == 0` it's obviously zero; otherwise the rotation kernel is trivial so it's nonzero. so:

```
v37 == 0    iff    v34 == 0    iff    input == 133742069
```

a couple lines later:

```c
v39 = nz(v37) & MASK | v37 | v63;
v65 = nz(v39);
v35 = v65 & (X + 73244475) ^ (v64 * v39 + v40);
```

`nz` here is `sub_140004440`:

```c
return -((-a | a) >> 31);
```

which is the standard "is x nonzero" idiom: returns 0 for `x == 0` and `0xFFFFFFFF` otherwise.

so if `v39 == 0`, then `v65 == 0` too, and the final formula collapses:

```
v35 = 0 & (X + 73244475) ^ (v64 * 0 + v40)
    = 0 ^ v40
    = v40
    = 133742069
```

every single thing those 32 hash rounds did to the state - all the rotations, all the table lookups, all the integrity checks - gets multiplied by zero and disappears. all that remains is the constant. which equals the input, by hypothesis. fixed point.

so the question becomes: when is `v39 == 0`?

```c
v39 = nz(v37) & (v62 | v61 | v58^0xE0C | v57^0x6F3 | v38) | v37 | v63;
```

three OR'd terms, all need to be zero. the `nz(v37) & ...` term is zero whenever `v37 == 0` (because `nz(0) == 0`). the `v37` term is zero by the same condition. so the only one we need to think about is `v63`:

```c
v63 = word_14000D268[7] & 0x8000 ^ 0x8000;
```

operator precedence: that's `(D268[7] & 0x8000) ^ 0x8000`. it's zero when bit 15 of `D268[7]` is set, otherwise it's `0x8000`.

`D268[7]` starts at zero. the only place I could find that sets bit 15 is inside `sub_140003CA0`:

```c
word_14000D268[5] += ... & 0x3F;
if ((word_14000D268[5] & 0x1FF) > 0xC0)
    word_14000D268[7] |= 0x8000;
```

`sub_140003CA0` is the panic function the per-round hash calls when its various integrity checks (like `sub_140004470` returning false, or the soft consistency checks at the start of `sub_1400035A0`) detect "weird" state. each call bumps `D268[5]` by some chunk of state bits, and once it crosses 0xC0 the bit gets latched in.

so the question of whether the crack works for input `133742069` reduces to: does feeding that specific input cause enough panic calls during the 32 rounds to push `D268[5]` past 0xC0?

I could chase this through the round logic statically but at this point the hypothesis was strong enough that paying for one process spawn felt cheaper than another hour of reading mod-9 arithmetic.

## the test

```
PS> echo 133742069 | .\Leet_Echo_Chamber.exe
Enter activation number:
result: 133742069
```

done. it echoes. that's the answer.

just to make sure I wasn't accidentally hitting `v35 = 133742069` through some other arithmetic coincidence I checked the neighbours:

```
133742068 -> 1879068099  (something else)
133742070 ->  516123772  (something else)
133742069 ->  133742069  (echo)
```

only 133742069 is a fixed point. clean result.

## the joke

the bit-15 condition is the part of this challenge that I think is genuinely cute. the win formula needs `v63 == 0`, which needs the panic counter to overflow, which needs the integrity checks to fail enough times during the 32 hash rounds. so the binary's anti-tamper machinery is what enables the crack to land.

if you had hooked or patched out the panic function (which is a totally normal first move when you see something called "anti-cheat" in a crackme), `D268[5]` would never increment, bit 15 would never set, `v63` would stay at `0x8000`, `v39` would land on `0x8000`, and the formula would not collapse. you'd get some other 32-bit value as output and conclude "huh, even 133742069 isn't a fixed point, must be some other number" and go off looking for it forever.

so the trap is: if you assume the anti-cheat is fighting you and disable it, the win condition silently evaporates. if you just leave the binary alone and trust the constant, it works on the first try. it's a static-analysis-friendly design that punishes overzealous dynamic hacking. nice.

## stuff I didn't do

- didn't reverse the actual hash. would have taken hours and was completely unnecessary.
- didn't brute force. would have taken ~14 months single-threaded.
- didn't reimplement anything in C / python.
- didn't even attach a debugger.

the lesson, for the nth time: when you have a function with a `result == input` win condition, the very first thing to do is grep for tiny zero-arg functions that return a single constant. they're almost always either the answer directly or one xor away from it. ida's function listing sorted by size puts them at the top. takes thirty seconds.

`sub_140001A10` was 4 bytes long. that was the entire challenge.

## reference

useful addresses if you're following along in ida:

- `0x1400089C0` - main
- `0x140004AB0` - input parser
- `0x140004630` - the strict 9-digit reader
- `0x140003B70` - isspace clone
- `0x140005990` - rol32 helper, called everywhere
- `0x140004440` - the `nz()` indicator, key to the collapse
- `0x140001A10` - returns the magic constant
- `0x140005AB0` - per-round hash, can be ignored
- `0x140003CA0` - panic / state mutator, sets bit 15 indirectly
- `0x140004470` - the validity check whose failure triggers the panic

answer: `133742069`
