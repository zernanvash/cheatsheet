# Alphagrams

> Source: [https://www.dcode.fr/alphagrams](https://www.dcode.fr/alphagrams)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is an alphagram? (Definition)

An alphagram is a word or phrase whose letters have been rearranged alphabetically.

Example: ALPHABET is sorted as AABEHLPT !

All words with the same alphagram are anagrams of each other.

## How to encrypt using Alphabet Derangement cipher?

The text is first segmented according to the rule: as long as the next letter is after the previous one in alphabetical order, then continue, otherwise create a new segment.

Example: ALPHABET becomes ALP,H,ABET

Then each segment is mixed/shuffled either randomly ( ABC becomes BAC or BCA ) or by inverting the letters ( ABC becomes CBA )

Example: ALP,H,ABET is coded PLA,H,TEBA

## How to decrypt Alphabet Derangement cipher?

Each segment is alphagrammed ( sorted by alphabetical order ), then read the text (which no longer has space).

Example: 'PLA, H, TEBA' becomes 'ALP, H, ABET'

If the text is not segmented and the segments have been reversed, it is possible to find them by looking at the letters that follow in the anti-alphabetical order. If the segments were mixed randomly, then there is no magic method, at best looking for the most plausible bigrams .

## How to recognize an Alphabetical disordered ciphertext?

It is a transposition cipher: no letter is modified, only the order changes.

The coincidence index is equal to that of the language used.

The text has many separation symbols (usually spaces).
