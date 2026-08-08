# Circular Bit Shift

> Source: [https://www.dcode.fr/circular-bit-shift](https://www.dcode.fr/circular-bit-shift)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Circular Bit Shift cipher?

The Circular Bit Shift encryption uses data in binary format, such as the ASCII encoding .

Example: DCODE is coded in binary ASCII 01000100 01000011 01001111 01000100 01000101 or 44 43 44 45 4F in hexadecimal .

The encryption starts by cutting the binary data into blocks of size B bits (if B=8 then the shift is applied to each byte) and for each block, making it undergo a circular rotation of N bits (+1 = shift left, -1 = shift right).

Example: 01000100 shifted by N=-1 becomes 00100010 (the right bit is moved on the left). The message DCODE split into 8bits blocks and shifted by N=-1 becomes 00100010 10100001 10100111 00100010 10100010 or 22 A1 A7 22 A2 in hexadecimal .

For a block size B, an offset of -X or B-X is identical (modulo B).

## How to decrypt Circular Bit Shift cipher?

Decryption requires knowing the settings (block size and offset) used. It is identical to encryption except for the offset N which takes the opposite value (encryption with N = 1 is equivalent to decryption with N = -1).

Example: The binary message 00100010 10100001 10100111 00100010 10100010 encrypted with an offset of 1 bit. 00100010 is shifted by N=1 as 01000100 (the left bit is moved on the right). The message becomes 01000100 01000011 01001111 01000100 01000101 that is ASCII values for DCODE .

## How to recognize a Circular Bit Shift ciphertext?

The message is usually presented in a raw format or at best in hexadecimal or binary format, as the characters resulting from the processing are not always printable characters.

## How to decipher Circular shifting without the shift?

Test all possible block sizes and offsets and keep those that show ASCII values of alphanumeric characters.

dCode attempts common sizes (binary numbers from 2 to 10 bits, multiples of 4 up to 40, multiples of 32 up to 128 bits) at all their shifts and displays most probable results.
