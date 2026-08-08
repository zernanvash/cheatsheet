# Index of Coincidence

> Source: [https://www.dcode.fr/index-coincidence](https://www.dcode.fr/index-coincidence)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the index of coincidence? (Definition)

The index of coincidence (IC or IoC) is an indicator used in cryptanalysis which makes it possible to evaluate the global distribution of letters in an encrypted message for a given alphabet.

A text written in the English language has an index of coincidence of 0.0667. The use of certain ciphers on a message in English will tend to modify this value which can allow them to be recognized. See dCode's cipher identifier .

## How to calculate a coincidence index?

Index of coincidence uses the formula:

$$ IC = \sum_{i=A}^{i=Z} \frac{n_{i}(n_{i}-1)}{N(N-1)} $$

with $ n_i $ the number of occurrences of the letter $ i $ in the text and $ N $ the total number of letters.

This index was probably invented by William F. Friedman.

## How to use an Index of Coincidence?

For a given ciphered message, the value for the IoC allows to filter the list of ciphering methods to use. It is one of the first cryptanalysis techniques.

If the Index of coincidence is high (close to $ 0.070 $), i.e. similar to plain text, then the message has probably been encrypted using a transposition cipher (letters were shuffled) or a monoalphabetic substitution (a letter can be replaced by only one other).

If the Index of coincidence is low (close to $ 0.0385 $), i.e. similar to a random text, then the message has probably been encrypted using a polyalphabetic cipher (a letter can be replaced by multiple other ones).

The more the coincidence count is low, the more alphabets have been used.

Example: Vigenere cipher with a key of length 4 to 8 letters have an IC of about $ 0.045 \pm 0.005 $

## What are values of IC among languages?

For an unencrypted text, coincidence indexes are English 0.0667 French 0.0778 German 0.0762 Spanish 0.0770 Italian 0.0738 Russian 0.0529

English 0.0667 French 0.0778 German 0.0762 Spanish 0.0770 Italian 0.0738 Russian 0.0529

## What is a random text?

A text where each letter has the same probability of appearance than another, IC is then of $ 1/N $ (where $ N $ is the number of letters in the alphabet)

Example: $ IC = 0.0385 $ for $ N=26 $

## How to calculate a key size from the IC?

In the case where multiple alphabets are used and the key size determines the number of alphabets (as for the Vigenere cipher ), by denoting $ n $ the total number of letters in the message and $ m $ the key size, a new coincidence index can be calculated by the formula:

$$ IC = \frac{n-m}{m(n-1)}} \cdot IC_{\text{lang}}} + \frac{n(m-1)}{(n-1)m} \cdot 0.0385 $$
