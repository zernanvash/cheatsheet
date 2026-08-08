# Multi-tap Phone (SMS)

> Source: [https://www.dcode.fr/multitap-abc-cipher](https://www.dcode.fr/multitap-abc-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Multitap code? (Definition)

Multi-tap coding is a historical text input technique used on early mobile phones with keypads (before touchscreens and predictive text input like T9 ).

The keypad typically has 12 keys arranged in a 3x4 grid. The letters of the alphabet are distributed across keys 2 through 9. Each key corresponds to several letters.

To type a letter, the user must press the same key repeatedly until the desired letter is reached.

The distribution of letters across the keys is defined by ITU-T Recommendation E.161.

## How to encrypt using Multitap cipher?

Encoding a message using multi-tap code involves replacing each letter with the repetition of the number corresponding to the key on the telephone keypad. Each key contains several letters. The number of presses indicates the letter's position on that key. Here is the standard alphabet correspondence table: A 2 N 66 B 22 O 666 C 222 P 7 D 3 Q 77 E 33 R 777 F 333 S 7777 G 4 T 8 H 44 U 88 I 444 V 888 J 5 W 9 K 55 X 99 L 555 Y 999 M 6 Z 9999

A 2 N 66 B 22 O 666 C 222 P 7 D 3 Q 77 E 33 R 777 F 333 S 7777 G 4 T 8 H 44 U 88 I 444 V 888 J 5 W 9 K 55 X 99 L 555 Y 999 M 6 Z 9999

Example: DCODE becomes 3 222 666 3 33 or without separator 3222666333

The ITU-T E.161 standard only defines the letter-to-number correspondence. Other elements (spaces, numbers, punctuation, or uppercase/lowercase distinction) depend on the phone's implementation and are not universally standardized.

## How to decrypt Multitap cipher?

Decoding a multi-tap message involves replacing each group of identical numbers with the corresponding letter.

Each group represents a letter; when the letters are separated by spaces, decoding is straightforward.

Example: 22 22 translates to BB

However, if no separator is present, several interpretations are possible because the string of numbers can be split in different ways. Decoding then consists of testing all possible segmentations and then selecting plausible words (dCode uses a dictionary).

Example: 2222 can be translated to AAAA or AAB or ABA or AC or BAA or BB or CA

## How to recognize Multitap ciphertext?

A message encoded with the multi-tap code has several recognizable characteristics:

— the message consists of numbers that often appear consecutively

— the groups contain between 1 and 4 identical digits

— the digits 2 through 9 are very frequent, while the digits 0 and 1 rarely or never appear, and are seldom repeated

In addition , references to old mobile phones (SMS, texting, Nokia 3310, Bi-Bop, etc.), old rotary dial phones, or any device with a keypad (beep) may indicate the use of this type of encoding.

On many phones the Multitap mode was indicated as named ABC .

## What are the variants of the Multi-tap cipher?

Several variations of multi-tap can appear in puzzles or simplified coding systems.

— Variation in the notation of the number of taps: instead of writing a repetition of the digit, the number of taps can be explicitly indicated.

Example: The code 222 can be written as 2*3 , 2^3 , or even 23 (digit followed by the number of taps).

— Over-encryption: a multi-tap message can be re-encoded a second time using a different method.

Example: PHONE = 7446666633 = PGGMMMMMDD

— Mixing with predictive text: the T9 code is often linked to the multi-tap code.

## When Multi-tap was invented?

The first patent is from 1985. It has since been used in the majority of mobile phones keypad (numpad), had its heyday with the Nokia GSM, and then disappeared with touch screens and smartphones like iPhone.

## How many strokes are typically needed to write a letter?

If all 26 letters had an equal probability of appearing, the keystroke per character (KSPC) would be a little over 2.15 taps per letter.

By weighting the frequency of letter occurrence in English, MacKenzie calculated a KSPC of 2.034. here

## Why do some keys contain 3 letters and others 4?

The telephone keypad must accommodate the two letters of the alphabet on 8 keys (from 2 to 9). If each key contained 3 letters, it would only be possible to fit 8 × 3 = 24. Two additional letters must therefore be added.
