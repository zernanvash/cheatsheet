# RC4 Cipher

> Source: [https://www.dcode.fr/rc4-cipher](https://www.dcode.fr/rc4-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is RC4? (Definition)

RC4 (Rivest Cipher 4) is a symmetric encryption algorithm, designed by Ronald Rivest in 1987. RC4 has been used in protocols like TLS and WEP, but it is now considered cryptographically weak.

## How to encrypt using RC4 cipher?

The RC4 digit uses a key that can initialize an array of 256 boxes.

The algorithm that allows to initialize the array with the key key is:

// Pseudocode for i = 0 -> 255 { t[i] = i } j = 0 k = length(cle) for i = 0 -> 255 { j = (j + t[i] + key[i % k]) % 256 swap t[i] <-> t[j] }

The array t can then be used to generate a stream by moving values and XOR operation.

The RC4 algorithm is then: // Pseudocode a = b = 0 j = length(string) codes = [] for i = 0 -> j { a = (a + 1) % 256 b = (b + t[a]) % 256 swap t[a] <-> t[b] codes []= ( t[ (t[a] + t[b]) % 256] ) XOR string[i] } print codes

The codes are values between 0 and 255.

Example: dCode ( 64,43,6F,64,65 in hexadecimal ) encrypted with the key RC4 ( 52,43,34 in hexadecimal ) is coded 2B,7F,DA,B6,1D ( hexadecimal ) Identically 2B,7F,DA,B6,1D (in hexadecimal ) decrypted with the same key RC4 ( 52,43,34 in hex) becomes 64,43,6F,64,65 ( dCode in ASCII )

## How to decrypt RC4 cipher?

Decryption is exactly the same as encryption.

## How to recognize a RC4 ciphertext?

An RC4 cipher produces bytes between 0 and 255, often represented in hexadecimal .

The generated stream is pseudo-random, but RC4 exhibits known statistical biases (particularly in the first few bytes of the stream). These biases are difficult to detect in small messages but exploitable on a large scale.

The code is also called RCfour, ARCFour, ARC4, Alleged RC4 or Ron's Code 4.

Any reference to WEP or TLS protocols is a clue.

## When was RC4 invented?

RC4 was invented by Ronald Rivest (one of the inventors of RSA encryption) in 1987.

The algorithm remained secret for several years before being anonymously leaked on the internet in 1994. This leak contributed to its widespread adoption in numerous software programs and protocols.
