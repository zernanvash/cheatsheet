# Multiplicative Cipher

> Source: [https://www.dcode.fr/multiplicative-cipher](https://www.dcode.fr/multiplicative-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Multiplicative Cipher? (Definition)

The multiplicative cipher is a special case of the affine cipher . In an affine cipher , each letter is transformed by the function $ ax + b $, where $ x $ is the position of the letter in the alphabet (usually starting at $ 0 $), and the calculation is performed modulo the size of the alphabet. The multiplicative cipher corresponds to the situation where the shift $ b $ is zero ($ b = 0 $). It therefore reduces to a simple multiplication of the position by an integer key $ a $, followed by a reduction modulo $ 26 $ (for the standard Latin alphabet of $ 26 $ letters).

## How to encrypt using Multiplicative cipher?

Multiplicative encryption uses a key $ k $ (an integer) and an alphabet.

Example: Encrypt DCODE with the key $ k = 17 $ and the 26-letter alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ

Each letter is associated with its rank $ c $ in the alphabet (starting from 0).

Example: D =3, C =2, O =14, D =3, E =4

For each character of the plain message, apply the following calculation:

$$ c \times k \mod 26 $$

($ 26 $ being the number of letters in the alphabet)

The number obtained indicates the rank in the alphabet of the corresponding numbered letter.

Example: D = 3, so $ 3 \times 17 \mod 26 \equiv 25 $ and the letter at rank 25 is Z . So on for each letter, the final encrypted message is ZIEZQ .

## How to decrypt Multiplicative cipher?

Decryption can be done in 2 ways:

— Mathematically, calculate the modular inverse $ k^{-1} $ of the key modulo 26 and apply the calculation for each letter:

$$ c \times k^{-1} \mod 26 $$

Example: The key $ 17 $ has the inverse modulo 26 of the value $ 23 $ so Z (index 25) becomes $ 25 \times 23 \mod 26 \equiv 3 $ and 3 corresponds to D in the alphabet.

— By substitution, in fact, during encryption each letter is associated with only one other, by calculating all the possible associations (by encrypting the 26 letters of the alphabet) then it is possible to deduce an alphabet substitution that will serve as a decryption table.

## What are the possible key values?

For multiplicative encryption to be reversible (i.e., for an encrypted message to be decrypted unambiguously), it is necessary that the key $ k $ be first with the size of the alphabet (denoted $ m $). In the case of the standard Latin alphabet of $ 26 $ letters, $ m = 26 $. The prime condition with $ 26 $ means that $ k $ and $ 26 $ have no common divisors other than $ 1 $. The integers that satisfy this property are the numbers $ k $ such that $ \operatorname{gcd}(k, 26) = 1 $.

Due to reduction modulo $ 26 $, two keys that differ by a multiple of $ 26 $ produce exactly the same encryption. Therefore, the set of distinct keys is limited to residues modulo $ 26 $ that are coprime with $ 26 $. The number of such distinct keys is given by Euler's totient function $ \varphi(26) = 12 $. These $ 12 $ values are: $ 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25 $.

The key $ 1 $ leaves the message unchanged (trivial encryption).

The key $ 25 $ is equivalent to $ -1 \mod 26 $ and produces an encryption that reverses the order of the alphabet (A→Z, B→Y, C→X, etc.).

The other $ 11 $ values (excluding $ 1 $) constitute the effective keys of non-trivial multiplicative encryption.

## How to recognize a Multiplicative ciphertext? (Identification)

The message is a monoalphabetic substitution : each letter of the plaintext is replaced by a single encrypted letter, and this correspondence is fixed for the duration of the message.

The analysis of the frequencies of the letters remains possible and the coincidence index of the ciphertext is identical to that of the plaintext (the distribution of frequencies is simply swapped).

A very telling clue is that the letter A is always numbered in A . Indeed, since the rank of A is $ 0 $, the calculation $ 0 \times k \mod 26 $ systematically gives $ 0 $, regardless of the key $ k $.

## How to decipher Multiplicative cipher without key? (Attacks)

For a given alphabet, there are only a few possible keys.

The 26-letter Latin alphabet allows only 11 keys: 3 , 5 , 7 , 9 , 11 , 15 , 17 , 19 , 21 , 23 and 25 (these are coprime numbers with 26).

Key Substitution Alphabet 3 ADGJMPSVYBEHKNQTWZCFILORUX 5 AFKPUZEJOTYDINSXCHMRWBGLQV 7 AHOVCJQXELSZGNUBIPWDKRYFMT 9 AJSBKTCLUDMVENWFOXGPYHQZIR 11 ALWHSDOZKVGRCNYJUFQBMXITEP 15 APETIXMBQFUJYNCRGVKZODSHWL 17 ARIZQHYPGXOFWNEVMDULCTKBSJ 19 ATMFYRKDWPIBUNGZSLEXQJCVOH 21 AVQLGBWRMHCXSNIDYTOJEZUPKF 23 AXUROLIFCZWTQNKHEBYVSPMJGD 25 AZYXWVUTSRQPONMLKJIHGFEDCB

Key Substitution Alphabet 3 ADGJMPSVYBEHKNQTWZCFILORUX 5 AFKPUZEJOTYDINSXCHMRWBGLQV 7 AHOVCJQXELSZGNUBIPWDKRYFMT 9 AJSBKTCLUDMVENWFOXGPYHQZIR 11 ALWHSDOZKVGRCNYJUFQBMXITEP 15 APETIXMBQFUJYNCRGVKZODSHWL 17 ARIZQHYPGXOFWNEVMDULCTKBSJ 19 ATMFYRKDWPIBUNGZSLEXQJCVOH 21 AVQLGBWRMHCXSNIDYTOJEZUPKF 23 AXUROLIFCZWTQNKHEBYVSPMJGD 25 AZYXWVUTSRQPONMLKJIHGFEDCB

There are other numbers co-prime with 26 (which are greater than 26) but they give alphabets identical to those above.

## What are the variants of the Multiplicative cipher?

The multiplicative cipher is a simplification of the Affine cipher .

The multiplicative cipher has little interest, but it is often used for learning computer science and ciphers.
