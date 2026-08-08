# Word Desubstitution/Pattern

> Source: [https://www.dcode.fr/word-desubstitution](https://www.dcode.fr/word-desubstitution)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a mono-alphabetic substitution of a word? (Definition)

A mono-alphabetical word substitution is an encryption method where each letter of the original word is replaced by a single letter in the encrypted word.

Example: If MESSAGE is encrypted TUNNIZU , then the letter E is always replaced by the letter U

## How to desubstitute a word ciphered by mono-alphabetical substitution?

To desubstitute an encrypted word by mono-alphabetic substitution , the user can use various techniques, including frequency analysis of letters, comparison with known words, or even the use of context if available.

The desubstitution of a single word, without a clue, must be based on the distribution of letters in the cipher word, specifically repeated and distinct letters in order to make a fingerprint/pattern.

Example: XYX is decomposed: one letter, then a second letter distinct from the first one, then the first letter again

With a fingerprint (idiomorph), it is possible to search in a dictionary for words with the same fingerprint and thus corresponding to a mono-alphabetic substitution .

Example: BOB , EVE or SMS can fit, but not CAB .

dCode can not find any result if the substitution is not monoalphabetic (ie it uses a unique alphabet, such a deranged alphabet ) or if the word is not present in the dictionary.

## What are the most favorable cases?

The fingerprint (or pattern) of the word must be specific, for example, include repetitions of letters. Indeed, if there are no repeated letters, then many words can match.

## Why limiting to 2 words?

The number of combinations of words is exponential and beyond the computation times exceed the minute. There are faster heuristics but they do not guarantee a result, dCode prefers to guarantee a result rather than not displaying it. To decipher a sentence, the monoalphabetic substitution tool is much faster.
