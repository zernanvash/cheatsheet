# Frequency Analysis

> Source: [https://www.dcode.fr/frequency-analysis](https://www.dcode.fr/frequency-analysis)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is frequency analysis? (Definition)

Frequency analysis is the statistical study of the distribution (and counting) of symbols (most often letters, but also numbers or groups of letters) in a text.

It is widely used in cryptanalysis to break certain ciphers. Its principle is based on the fact that, in a given language, some symbols appear more frequently than others.

Example: In English, the letter E is generally the most common, while Z is rare.

By comparing the observed frequencies in a ciphertext with those known from the presumed language of the plaintext, it becomes possible to formulate hypotheses about the correspondence between ciphertext symbols and plaintext letters.

## How to use frequency analysis?

Frequency analysis generates a histogram that allows statistical distributions to be compared with those of a reference model (the plaintext language). This comparison can theoretically help decipher a text by comparing the frequencies of occurrence of letters in the encrypted message with the theoretical frequencies of occurrence of letters in the plaintext language.

Frequency analysis attack is particularly effective on monoalphabetic ciphers. These systems do not modify the statistical distribution of letters, which allows a correspondence to be established between the ciphertext and the plaintext.

To perform an alphabetic substitution using frequency analysis , the most frequent symbol must be replaced with the letter E (which is the most frequent letter in English), and the others deduced from this. This principle is only truly applicable if the cryptogram contains a large number of symbols so that the frequencies are statistically significant.

## How to use frequency analysis on ngrams?

Frequency analysis is not limited to individual letters but can also be applied to groups of letters (ngrams) for polygram ciphers.

Some ciphers are characterized by the presence or absence of repeated letters in a bigram or trigram .

For some ngrams analyzes, use the sliding window mode:

Example: ABCD has bigrams AB,CD (blocks mode)

Example: ABCD has bigrams AB,BC,CD (sliding window mode)

## When frequency analysis is useless?

Frequency analysis becomes ineffective when the text is too short, because statistical variations dominate and make the results unreliable.

Frequency analysis is also less relevant when the message has been encrypted with polyalphabetic encryption (which tends to randomize the frequency of the letters), or when the encryption is homophonic (several different encrypted characters for the same plain letter) or polygrammic (groups of characters replace each letter). In these cases, the analysis does not allow a decoding but allows to filter or find the type of encryption used.

## What are letter appearance frequencies in English language?

Letters by frequency of appearance in English: E 12.7 % M 2.4 % T 9.1 % W 2.4 % A 8.2 % F 2.2 % O 7.5 % G 2.0 % I 7.0 % Y 2.0 % N 6.7 % P 1.9 % S 6.3 % B 1.5 % H 6.1 % V 1.0 % R 6.0 % K 0.8 % L 4.0 % J 0.2 % D 4.3 % X 0.2 % C 2.8 % Q 0.1 % U 2.8 % Z 0.1 %

E 12.7 % M 2.4 % T 9.1 % W 2.4 % A 8.2 % F 2.2 % O 7.5 % G 2.0 % I 7.0 % Y 2.0 % N 6.7 % P 1.9 % S 6.3 % B 1.5 % H 6.1 % V 1.0 % R 6.0 % K 0.8 % L 4.0 % J 0.2 % D 4.3 % X 0.2 % C 2.8 % Q 0.1 % U 2.8 % Z 0.1 %

For comparison purposes, here are letters frequency in French: E 17.3 % P 3.0 % A 8.4 % G 1.3 % S 8.1 % V 1.3 % I 7.3 % B 1.1 % N 7.1 % F 1.1 % T 7.1 % Q 1.0 % R 6.6 % H 0.9 % L 6.0 % X 0.4 % U 5.7 % J 0.3 % O 5.3 % Y 0.3 % D 4.2 % K 0.1 % C 3.0 % W 0.1 % M 3.0 % Z 0.1 %

E 17.3 % P 3.0 % A 8.4 % G 1.3 % S 8.1 % V 1.3 % I 7.3 % B 1.1 % N 7.1 % F 1.1 % T 7.1 % Q 1.0 % R 6.6 % H 0.9 % L 6.0 % X 0.4 % U 5.7 % J 0.3 % O 5.3 % Y 0.3 % D 4.2 % K 0.1 % C 3.0 % W 0.1 % M 3.0 % Z 0.1 %

And in Spanish: A 12.3 % B 1.0 % C 4.5 % D 5.0 % E 13.7 % F 0.8 % G 1.0 % H 0.7 % I 7.8 % J 0.3 % K 0.1 % L 5.8 % M 2.8 % N 7.4 % O 8.7 % P 2.6 % Q 1.0 % R 6.4 % S 7.0 % T 4.8 % U 4.0 % V 1.0 % W 0.1 % X 0.2 % Y 0.6 % Z 0.3 %

A 12.3 % B 1.0 % C 4.5 % D 5.0 % E 13.7 % F 0.8 % G 1.0 % H 0.7 % I 7.8 % J 0.3 % K 0.1 % L 5.8 % M 2.8 % N 7.4 % O 8.7 % P 2.6 % Q 1.0 % R 6.4 % S 7.0 % T 4.8 % U 4.0 % V 1.0 % W 0.1 % X 0.2 % Y 0.6 % Z 0.3 %
