# Morbit Cipher

> Source: [https://www.dcode.fr/morbit-cipher](https://www.dcode.fr/morbit-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Morbit cipher? (Definition)

The Morbit cipher is an encryption method based on Morse code . It involves converting a message into Morse code and then dividing it into groups of two symbols (dots, dashes, or separators) called bigrams .

These bigrams are then replaced by digits from 1 to 9 in an order determined by a key. It is therefore a super-encryption of Morse code that combines fractionalization and polygrammatic substitution.

## How to encrypt using Morbit cipher?

Morbit encryption uses a numeric index (from 1 to 9) associated with pairs of morse characters indexed like this: 1 2 3 4 5 6 7 8 9 .. .- ./ -. -- -/ /. /- //

1 2 3 4 5 6 7 8 9 .. .- ./ -. -- -/ /. /- //

The key is used to mix the index according to the alphabetical order of its letters.

Example: The keyword MORSECODE is associated with the code 568931724 by sorting the letters alphabetically CDEEMOORS and matching them to 1234567879 as: Letters M O R S E C O D E Order 5 6 8 9 3 1 7 2 4 Bigrams .. .- ./ -. -- -/ /. /- //

Letters M O R S E C O D E Order 5 6 8 9 3 1 7 2 4 Bigrams .. .- ./ -. -- -/ /. /- //

The first step of encryption is to encode the original message in Morse code , the characters are separated by a slash / and the words are separated by double slash // .

Example: The message MORE BITS is encoded in Morse --/---/.-././/-.../../-/...

The second part of the encryption consists in splitting the Morse message into couples of 2 characters and to associate the corresponding digit in the numeric index made with the key.

Example: -- /- -- /. -. /. // -. .. /. ./ -/ .. ./ 3 2 3 7 9 7 4 9 5 7 8 1 5 8

-- /- -- /. -. /. // -. .. /. ./ -/ .. ./ 3 2 3 7 9 7 4 9 5 7 8 1 5 8

The encrypted message is therefore 32379749578158 .

## How to decrypt using Morbit cipher?

Morbit decryption requires knowing the key in order to generate the numerical index associated with morse character pairs.

Example: The key ALPHABETS gives the following index: Letters A L P H A B E T S Order 1 6 7 5 2 3 4 9 8 Bigrams .. .- ./ -. -- -/ /. /- //

Letters A L P H A B E T S Order 1 6 7 5 2 3 4 9 8 Bigrams .. .- ./ -. -- -/ /. /- //

The first step in decryption is to replace each digit with its morse bigram equivalent.

Example: The message 2924591719 corresponds to the morse code --/---/.-./-.../../- : 2 9 2 4 5 9 1 7 1 9 -- /- -- /. -. /- .. ./ .. /-

2 9 2 4 5 9 1 7 1 9 -- /- -- /. -. /- .. ./ .. /-

The morse code obtained only needs to be translated via the classic Morse code to get the plain message.

Example: -- / --- / .-. / -... / .. / - translates to MORBIT

## How to recognize a Morbit ciphertext?

A Morbit encrypted message uses only digits from 1 (one) to 9 (nine).

The Morbit message is between 50% and 100% longer (approximately) than the original message.

The presence of a 9-letter word that can serve as a key is an important clue.

The adjective morbid is a paronym that can be a clue.

The distribution of figures tends towards a relatively homogeneous distribution.

## How to decipher Morbit without key?

The key is an important element because it allows $ 9! = 362880 $ combinations of the numerical index.

A way to reduce this number of combinations is to know a part of the plain text in order to deduce the numerical index and the correspondence with the morse bigrams .

Also, several assumptions about the message can reduce the possibilities of the key:

— the appearance of 3 consecutive // 'is unlikely

— any word of more than 10 Morse characters (without / spacer) is unlikely

— any sequence of more than 4 consecutive identical digits is unlikely

The corresponding combinations can be reasonably eliminated.

## What are the variants of the Morbit cipher?

Morbit is closer to the Fractionated Morse Code which is a kind of over-encryption.
