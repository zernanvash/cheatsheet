# Mono-alphabetic Substitution

> Source: [https://www.dcode.fr/monoalphabetic-substitution](https://www.dcode.fr/monoalphabetic-substitution)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a (mono-)alphabetical substitution? (Definition)

An alphabetic substitution is a substitution cipher where the letters of the alphabet are replaced by others according to a 1-1 correspondence (a plain letter always corresponds to the same cipher letter).

The substitution is said to be monoalphabetic because it uses only one alphabet, this alphabet is said to be disordered.

## How to encrypt using an alphabetical substitution?

The monoalphabetical substitution consists in using a mixed alphabet (with the letters in an unusual order) and replacing the letters of the alphabet normal by it.

Example: BYKWASLFXOCZTDHJUMIGPVENQR is a totally random alphabet with the 26 letters of the Latin alphabet.

To understand, write the alphabet over the classic alphabet: Plain alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Substitution alphabet BYKWASLFXOCZTDHJUMIGPVENQR

Plain alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Substitution alphabet BYKWASLFXOCZTDHJUMIGPVENQR

The substitution involves a replacement in the plaintext of all the letters of the first row with the letters associated with the second row.

Example: All A become N , all the B remain B , all the C become A , etc.

Example: With this substitution DCODE is encrypted as WKHWA .

Any deranged alphabet can be used to create a mono alphabetic substitution provided it respects the criterion of an alphabet: not containing the same letter several times.

## What do K1, K2, K3, K4 mean?

The K1, K2, K3, and K4 classifications are used by the ACA to describe the use of keywords in encryption alphabets.

— K1: The key is inserted into the substitution alphabet, usually at the beginning and then the rest of the letters follow in alphabetical order.

Example: Default CODEABFGHIJKLMNPQRSTUVWXYZ but an offset is possible XYZCODEABFGHIJKLMNPQRSTUVW

— K2: The key is inserted into the substitution (reciprocal) coded alphabet ⇅.

— K3: The key is used in both plaintext and coded alphabets.

— K4: Two different keys are used: one for the substitution alphabet and another for the coded alphabet.

## How to decrypt using an alphabetical substitution?

Decryption requires knowing the alphabet mixed used and the inverse substitution encryption.

Substitution Alphabet NBAJYFOWLZMPXIKUVCDEGRQSTH Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ

Substitution Alphabet NBAJYFOWLZMPXIKUVCDEGRQSTH Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ

The substitution involves replacing in the ciphertext all the letters of the first row with the letters associated with the second row.

Example: The encrypted message JAKJY has for plain message DCODE .

## How to recognize a mono alphabetical substituted text?

The ciphered message has an index of coincidence identical to the language of the plain text.

English speakers call this encryption aristocrat (if there are spaces) or patristocrat (if there are no spaces between words).

## How to decipher a substitution without the alphabet?

The MCMC technique (used by dCode) is one of the most effective for finding the most probable plain text and proposing a replacement alphabet.

dCode additionally adds an interactive tool to manually decrypt substitution-encrypted messages.

Another possibility, the known plaintext attack that makes possible to deduce some letters of the alphabet via the knowledge or the preliminary guess of certain portions of the plain text.

Example: The most common alphabets used for substitutions are: QWERTYUIOPASDFGHJKLZXCVBNM MNBVCXZLKJHGFDSAPOIUYTREWQ QAZWSXEDCRFVTGBYHNUJMIKOLP AZERTYUIOPQSDFGHJKLMWXCVBN NBVCXWMLKJHGFDSQPOIUYTREZA AQWZSXEDCRFVTGBYHNUJIKOLPM ZYXWVUTSRQPONMLKJIHGFEDCBA AEIOUYBCDFGHJKLMNPQRSTVWXZ' Pangrams can also be used as an alphabet (by removing redundant letters).

## What is the MCMC technique?

MCMC ( Markov Chain Monte Carlo) is the name given to a statistical method that applies very well to mono-alphabetical substitutions.

1 - Initialization: use a random substitution alphabet (but it is possible to carry out an analysis of letter frequencies to obtain a first plain alphabet - encrypted alphabet mapping table).

2 - Evaluation: calculation of the probability that the current substitution alphabet produces plain text (score generally based on the frequencies of appearance of bigrams in the target language).

3 - Modification of the alphabet: randomly exchange certain plain letter-cipher letter correspondences

4 - Repeat steps 2 and 3 as long as the plausibility score of the message obtained increases and the alphabet selected offers the most probable plain message.

Source: here Diaconis, Persi. (2009). The Markov Chain Monte Carlo Revolution. Bulletin of the American Mathematical Society. 46. 179-205. 10.1090/S0273-0979-08-01238-X.

## What are the variants of the substitution cipher?

First, some substitution use specific alphabets, such as Atbash that takes the alphabet backwards ZYXWVUTSRQPONMLKJIHGFEDCBA or the Caesar cipher which uses a shifted alphabet DEFGHIJKLMNOPQRSTUVWXYZABC that is shifted by 3.

There are also substitutions that use several alphabets, alphabet that changes depending on an algorithm defined by encryption (e.g. Vigenere uses 26 alphabets).

In game-play journals, substitution games / exercises are often called cryptograms.
