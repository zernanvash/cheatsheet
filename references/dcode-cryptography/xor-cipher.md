# XOR Cipher

> Source: [https://www.dcode.fr/xor-cipher](https://www.dcode.fr/xor-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the XOR cipher? (Definition)

XOR encryption is a symmetrical encryption/decryption method based on the use of the logical/binary operator XOR (also called Exclusive Or , symbolized by ⊕ ).

This technique consists of combining each bit of the message with a key bit, using the XOR operation.

The XOR operation takes 2 bits as input and returns one bit as output according to the following truth table : if the two bits are different, the result is 1, otherwise the result is 0.

## How to encrypt using XOR cipher?

XOR is applied on binary data, if the message is text, encoding (conversion to ASCII or Unicode ) must be performed.

Example: Encrypt the plain message 1001 with the key 10

Take the first bit of the plain text and the first bit of the key and multiply then using XOR operation to get the ciphered bit.

Example: 1 ⊕ 1 = 0

The operation is repeated with the second bit of the plaintext and the second bit of the key. At the end of the key, loop back to the first bit.

Example: Plain message 1001 Key (repeated) 1010 Encrypted message 0011

Plain message 1001 Key (repeated) 1010 Encrypted message 0011

## How to decrypt XOR cipher?

XOR Decryption (UnXOR/DeXOR) is identical to encryption because the XOR operation is symmetrical: A XOR B = C and C XOR B = A (reverse XOR = XOR ).

Example: 1001 ⊕ 1010 = 0011 and 0011 ⊕ 1010 = 1001

## How to convert a text into binary?

dCode manages the conversion automatically, but by default the ASCII encoding table for classic characters (letters of the alphabet or numbers) allows each character to be coded by a number between 0 and 127, which is then converted to base 2 (binary). For accented or less common characters (symbols, emojis, etc.) dCode uses UTF-8 ( Unicode ).

## What is the truth table for XOR?

The truth table of the 2-parameter XOR logic function is: A B A xor B 0 0 0 0 1 1 1 0 1 1 1 0

A B A xor B 0 0 0 0 1 1 1 0 1 1 1 0

## How to recognize XOR ciphertext?

A xored message ( XOR encrypted message) has the same length as the plaintext.

An encoded message may contain non-printable characters if it is represented in ASCII code . Therefore, its representation is usually in hexadecimal or binary (or other binary data interchange format such as Base64 ).

If the key is short and repeated while the text is long and has repetitions, then regular patterns may appear and be detected by tools like dCode.

Data in the form of a stream is well suited to XOR encoding.

## What are the pros and cons of XOR?

The XOR operation is one of the basics of logical computing. Computer processors can perform this type of calculation immediately, billions of times per second, which is therefore useful if computing resources are limited.

The XOR operation has the advantage of being reversible and above all symmetrical by applying the same algorithm, which further simplifies the calculations.

XOR encryption provides some cryptographic security when the key is as large as the original message, otherwise XOR is vulnerable to known-plaintext attacks.

## How to decipher XOR without the key?

Without the key, several attacks are possible to decrypt XOR :

— Frequency analysis and linguistic probability: compare the expected bit or character frequencies and analyze their distribution based on plausible key lengths

— Probable word attack: by knowing part of the plaintext, it is possible to deduce all or part of the key

— Dictionary attack: if the key is a password, testing common keys is possible

— Bruteforce attack: if the key is short and repeated, trying all combinations is a reasonably time-consuming solution

— Use of automated XOR decryption tools (such as dCode)

## What are the variants of the XOR cipher?

XOR is compatible with the principle of autoclave cipher.

XOR can be used as a One-Time Pad (OTP): a theoretically unbreakable version using a random key as long as the message, and never disclosed or reused.
