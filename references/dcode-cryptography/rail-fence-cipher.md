# Rail Fence (Zig-Zag) Cipher

> Source: [https://www.dcode.fr/rail-fence-cipher](https://www.dcode.fr/rail-fence-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Rail Fence cipher? (Definition)

The Rail Fence (or zig-zag ) cipher is a transposition cipher that involves writing text in a wave pattern across multiple lines and reading it line by line to obtain the encrypted message.

## How to encrypt using Rail Fence cipher?

The Rail Fence cipher follows these steps:

— Define a number of levels N (or rows or floors), this number is sometimes called the cipher key.

— Write the message following a sawtooth pattern (alternating up and down) along a path of N levels/floors.

Example: Encode DCODEZIGZAG with N=3 : D---E---Z-- -C-D-Z-G-A- --O---I---G

D---E---Z-- -C-D-Z-G-A- --O---I---G

— Read the message line by line to obtain the encrypted text.

Example: The encrypted message is DEZCDZGAOIG

## How to decrypt Rail Fence cipher?

Deciphering Rail Fence requires knowing the number of levels N and is broken down into three steps:

Example: Decipher the message DEZCDZGAOIG and N=3

— Reconstruct the zigzag pattern with the expected number of levels.

Example: X---X---X-- -X-X-X-X-X- --X---X---X

X---X---X-- -X-X-X-X-X- --X---X---X

— Write the numbered letters in the pattern, line by line.

Example: D---E---Z-- -C-D-Z-G-A- --O---I---G

D---E---Z-- -C-D-Z-G-A- --O---I---G

— Read the letters along the zigzag path to reconstruct the original message.

Example: The plain text is DCODEZIGZAG .

## How to recognize Rail Fence ciphertext? (Identification)

A message encoded by Rail-Fence has an index of coincidence equal to that of the language of the original text.

Frequency analysis reveals usual occurrences of common letters similar to a plain text.

All references to zig-zag , sawtooth, up and down, uphill and downhill, path/track/route, wave, etc. are clues.

Anything in the shape of bumps can also be a clue: camel, speed bump, etc.

The word rail can be the target of puns about trains, railroads, railway tracks, cocaine/coke, etc.

## How to decipher Rail Fence without the number of levels?

If the number of levels is unknown, several approaches exist:

— Automatic brute force: Test different levels and search for readable text (dCode uses this method).

— Manual detection: Try to find possible words using the letters in the text and deduce the key.

## What are the variants of the Rail Fence cipher?

There are several variations:

— The fence pattern may begin with a peak or a hollow (up or down).

Example: (↘↗ hollow) A---E -B-D- --C--

Example: (↗↘ peak) --C-- -B-D- A---E

— The first letter is not necessarily the base of the peak or hollow, the zig zag can start in the middle with an offset (equivalent to add spaces at the beginning)

Example: (Offset of +1) ----D- -A-C-E --B---

— It is possible to allow spaces and punctuation, which shifts the characters.

— It is possible to encrypt a message by applying the decryption steps. dCode denotes this variant with the symbol ⁻¹ .

## What happens if the key is greater than or equal to the length of the text?

If the value of the number of levels is greater than or equal to the size of the text, then the text undergoes no encryption (no change).

## What is the difference between Rail Fence and ZigZag?

None, Rail Fence is the original word, ZigZag is the mnemonic term.

Sometimes Zig-Zag is the name given to a reading method. The message is hidden in a written grid, as with Rail Fence , but the empty spaces in the grid are then filled with neutral letters.

Example: ( Zig-zag reading of ABCDE ) AxyzE xByDz wxCyz

## When Rail-Fence was invented?

Rail-Fence is a basic transposition , no date or creator is recognized.
