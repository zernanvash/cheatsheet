# Prime Multiplication Cipher

> Source: [https://www.dcode.fr/prime-multiplication-cipher](https://www.dcode.fr/prime-multiplication-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## How to encrypt using prime multiplication cipher?

Modes 1 to 3

Associate with each letter its equivalent in prime number according to a correspondence table (the most basic one is the prime number substitution according to the alphabet: A (first letter of the alphabet) is coded by 2 (first prime number), and so on A=2 , B=3 , C=5 , …, Z=101 )

Mode 3: Multiplication only

A word, composed of letters, will then be coded by the multiplication of prime numbers corresponding to the letters constituting it. However, this poses some problems during decryption.

Example: AB is $ 2 \times 3 = 6 $ and BA is $ 3 \times 2 = 6 $ also. By default, with a multiplication only, the order of the letters is lost.

Mode 1: Letter power Position

In order not to lose the order of the letters, it is possible to multiply the value of the letters as many times as its position in the word. Thus, at decryption, the position of the letters may be retrieved.

Example: AB is then $ 2 \times ( 3 \times 3 ) = 2^1 \times 3^2 = 18 $ and BA is then $ 3 \times ( 2 \times 2 ) = 3^1 \times 2^2 = 12 $

However, if 2 identical letters are in the same word, then the exponents will add up. It is therefore recommended to cut the word when there is a repeating letter.

Example: DCODE = D(7) C(5) O(47) D(7) E(11) is coded $ 7^1 \times 5^2 \times 47^3 \times 7^4 \times 11^5 = 7^5 \times 5^2 \times 47^3 \times 11^5 $ which cannot be easily deciphered. Better to code DCO then DE : $ 7^1 \times 5^2 \times 47^3 $ followed by $ 7^1 \times 11^2 $

Mode 2: Multiplication of alphabetic ordered parts

By precutting the message with groups of letters having a predefined order (here alphabetical order), it is possible to avoid the use of exponents .

Example: DCODE is divided into D,CO,DE and is coded $ 7 \, 3 \times 47 = 141 \, 7 \times 11 = 77 $

Mode 4: Position power Letter

In this case, the letter is coded according to a correspondance table ( A1Z26 or ASCII or prime numbers subtitution are fine) but the position is coded by the prime numbers. Positions 1, 2 and 3 are respectively coded 2, 3 and 5..

Example: DCODE = D(4) C(3) O(15) D(4) E(5) is coded (with A1Z26 ) $ 2^4 \times 3^3 \times 5^15 \times 7^4 \times 11^5 = 30517741620 $

## How to decrypt prime multiplication cipher?

The first step is to factor the numbers of the encrypted message. This step is quick because only the prime factors present in the correspondence table are taken into account.

Multiplication alone or alphabetical portions

Substitute for each factor found, its corresponding letter / character in the table in order to form the original message.

Example: The numbers 2993,2627,1219,37,23,5,142,1081,43 are factorized 41×73,37×71,23×53,37,23,5,2×71,23×47,43 which corresponds to the letters MU,LT,IP,L,I,C,AT,IO,N

With exponents

The factorization must have the following form: $ a^1 \times b^2 \times c^3 \times \cdots \times n^m $ with $ {a\,\cdots\,n} $ prime numbers and $ m $ the number of letters in the word. The deciphered word is then composed of the letter corresponding to $ a $ in position $ 1 $, of the letter corresponding to $ b $ in position $ 2 $ etc.

Example: $ 55466476835 = 5^1 \times 47 ^ 2 \times 7^3 \times 11^4 $ and according to the table 5=C , 47=O , 7=D , 11=E so the word is CODE

## How to recognize a prime multiplication ciphertext?

The message is made up of numbers, sometimes very large, with an atypical decomposition into prime numbers (often $ a^1 \times b^2 \times c^3 \times \cdots \times n^m $)

If the message is in English, as the letter E is coded 11 , many of these numbers are multiple of 11 .

## Who did invent this cipher?

A web page dedicated to South African scouts included a message to decipher which used the same principle here

Over the net, some page called this method south african scout cipher , but please, avoid.
