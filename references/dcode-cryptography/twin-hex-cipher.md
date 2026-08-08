# Twin Hex Cipher

> Source: [https://www.dcode.fr/twin-hex-cipher](https://www.dcode.fr/twin-hex-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Twin Hex cipher? (Definition)

Twin Hex cipher is an encryption algorithm that uses ASCII bigrams/character pairs to convert them into alphanumeric trigrams .

## How to encrypt using Twin Hex cipher?

The Twin Hex encryption process only works on printable ASCII characters (codes 32 to 127).

Example: Encrypt the dCode message

Each pair of characters ( bigram ) is then indexed according to its rank among possible bigrams (the first bigram with codes 32,32 has the value $0$, then 32,33 has the index $1$, up to '127,127 ' which has a value of $9216). If the message is odd in length, complete with a space.

Example: dC has index $ 6563 $, od has index $ 7652 $ and e (a space has been added) has index $ 6624 $.

The index is then converted to base36 (symbols 0123456789abcdefghijklmnopqrstuvwxyz ) optionally supplemented by spaces (on the right) to obtain a trigram .

Example: $ 6563_{(10)} = \texttt{52b}_{(36)} $ (see the page dedicated to base n conversion )

The concatenation of the trigrams obtained forms the encrypted message.

Example: dCode is encrypted in Twin Hex as 52b5wk540

## How to decrypt Twin Hex cipher?

To decipher Twin Hex ciphertext, the decryption process begins by breaking the text into trigrams .

Example: Decrypt the message 3x35gu14 56g

Each trigram is then considered as a base36 number whose decimal value corresponds to an index among the possible ASCII bigrams .

Example: $ \texttt{3x3}_{(36)} = 5079_{(10)} $ and $ 5079 $ corresponds to the bigram Tw $ \texttt{5gu}_{(36)} = 7086_{(10)} $ and $ 7086 $ matches the bigram in , etc.

The plain message consists of the concatenation of the bigrams obtained.

Example: The original message is ' Twin Hex '

## How to recognize a Twin Hex ciphertext? (Identification)

Twin Hex is made up of lowercase alphanumeric characters a-z0-9 (default).

The indication twin or jumeau is a clue.

Mike Brockington's site here seems to be the original source but the form does not work correctly, use with caution.
