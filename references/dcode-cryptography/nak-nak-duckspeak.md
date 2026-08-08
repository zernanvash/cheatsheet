# Nak Nak (Duckspeak)

> Source: [https://www.dcode.fr/nak-nak-duckspeak](https://www.dcode.fr/nak-nak-duckspeak)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using Nak-Nak cipher?

Nak-Nak encryption uses the base 16 hexadecimal to encode messages themselves encoded with the ASCII table .

Example: Encode the DUCK message, start by encoding it in ASCII ( hexadecimal ) i.e. 44,75,63,6B then, for each digit, replace it with its corresponding one in the following table:

0 = Nak 1 = Nanak 2 = Nananak 3 = Nanananak 4 = Nak? 5 = nak? 6 = Naknak 7 = Naknaknak 8 = Nak. 9 = Naknak . A (10) = Naknaknaknak B (11) = nanak C (12) naknak D (13) nak! E (14) nak. F (15) naknaknak

0 = Nak 1 = Nanak 2 = Nananak 3 = Nanananak 4 = Nak? 5 = nak? 6 = Naknak 7 = Naknaknak 8 = Nak. 9 = Naknak . A (10) = Naknaknaknak B (11) = nanak C (12) naknak D (13) nak! E (14) nak. F (15) naknaknak

Example: DUCK ('44,75,63,6B 'in ASCII ) is coded as 4=Nak? 4=Nak? 7=Naknaknak 5=nak? and so on: Nak? Nak? Naknaknak nak? Naknak Nanananak Naknak nanak

The case ( upper and lower case ) is taken into account as are the characters . and ?

## How to decrypt Nak-Nak cipher?

The decryption of the Nak-Nak begins with the substitution of the different words Nak by the associated number in the table.

Example: Naknak Nak? Nak? Nanananak Naknak naknaknak Naknak Nak? Naknak nak? is constituted of Naknak =6 , Nak?=4 etc. so 6,4,4,3,6,F,6,4,6,5

The resulting code is the ASCII code in hexadecimal format of the original message.

Example: 64,43,6F,64,65 is decoded d,C,o,d,e in ASCII code . dCode is the clear starting message.

## How to recognize a Nak-Nak ciphertext?

The message consists of the sometimes repeated syllables Nak and Na . All words start with N and end with k .

Any reference to a duck or duckspeak are clues.

## What is the Coink/Couink variant?

According to the preferences of some, ducks rather make Coin than Nak , this variant modifies Na in Coin or Couin .
