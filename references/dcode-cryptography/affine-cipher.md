# Affine Cipher

> Source: [https://www.dcode.fr/affine-cipher](https://www.dcode.fr/affine-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Affine cipher? (Definition)

Affine cipher is a monoalphabetic substitution method where each letter of the plaintext is replaced by another letter according to an affine function of the form $ f(x) = A \times x + B \mod 26 $.

$ A $ and $ B $ are two integers that form the encryption key, and $ 26 $ corresponds to the length of the standard Latin alphabet.

## How to encrypt using the Affine cipher?

To encode a message using affine cipher :

1/ Assign each letter of the plaintext its numerical position $ x $ in the alphabet . By default, $ A=0, B=1, \dots, Z=25 $. It is possible (but not recommended) to use $ A=1, \dots, Y=25, Z=0 $ by using the alphabet ZABCDEFGHIJKLMNOPQRSTUVWXY .

2/ Apply the affine function $ y = (A \times x + B) \mod 26 $ to obtain the position $ y $ of the ciphertext letter.

3/ Replace each letter of the plaintext with the letter corresponding to $ y $ in the alphabet.

Example: Encrypt DCODE with the coefficients $ A=5, B=3 $, and the Latin/French alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ . Plain letter $ x $ $ y $ Cipher letter D $ 3 $ $ 5 \times 3 + 3 = 18 $ S C $ 2 $ $ 5 \times 2 + 3 = 13 $ N O $ 14 $ $ 5 \times 14 + 3 = 73 \equiv 21 \mod 26 $ V D $ 3 $ $ 18 $ S E $ 4 $ $ 5 \times 4 + 3 = 23 $ X DCODE is crypted SNVSX

Plain letter $ x $ $ y $ Cipher letter D $ 3 $ $ 5 \times 3 + 3 = 18 $ S C $ 2 $ $ 5 \times 2 + 3 = 13 $ N O $ 14 $ $ 5 \times 14 + 3 = 73 \equiv 21 \mod 26 $ V D $ 3 $ $ 18 $ S E $ 4 $ $ 5 \times 4 + 3 = 23 $ X

## How to decrypt the Affine cipher?

To decode a message encrypted using Affine :

1/ Calculate the modular inverse $ A' $ of $ A $ modulo $ 26 $

2/ For each ciphertext letter at position $ y $, calculate $ x = A' \times (y - B) \mod 26 $

3/ Replace each ciphertext letter with the letter corresponding to $ x $ in the alphabet.

Example: The message to decipher is SNVSX with the coefficients $ (A,B) = (5,3) $. A coefficient $ A' $ for $ A = 5 $ is $ 21 $ (since $ 5 \times 21 = 105 \equiv 1 \mod 26 $). For the letter S ($ y = 18 $), calculate the value $ x = A' \times (18-B) = 21 \times (18-3) = 315 \equiv 3 \mod 26 $, and the letter at position 3 is D . The plaintext message is DCODE .

## How to recognize an Affine ciphertext?

A message encrypted by Affine has a coincidence index close to the plain text language's one.

Any reference to an affine function (in a straight line), a graph, an abscissa or an ordinate is a clue (the function $ f(x) = ax + b $ can be represented in an orthonormal coordinate system like a classical affine function, it is therefore possible from a graph to find the slope coefficient $ a $ and the y-intercept $ b $).

## What are Affine cipher variants?

The affine ciphers in fact group together several ciphers which are special cases:

— The multiplicative cipher is a special case of the Affine cipher where B is 0.

— The Caesar cipher is a special case of the Affine cipher where A is 1 and B is the shift/offest.

The affine cipher is itself a special case of the Hill cipher, which uses an invertible matrix , rather than a straight-line equation, to generate the substitution alphabet.

## How to decipher Affine without coefficients A and B?

Without knowing the coefficients $ A $ and $ B $, a brute-force attack can be used. Assuming the alphabet has 26 characters, then the coefficient $ A $ can only take 12 values (numbers coprime to 26) and the coefficient $ B $ can only take 16 values, for a total of 312 combinations .

Knowing some letters from the plaintext, it is possible to plot the plaintext/ciphertext letters on a cartesian plane and deduce $ A $ (the slope) and $ B $ (the y-intercept ).

## How to compute the decryption function?

For an affine encryption with the function $ y = A x + B $, then the reciprocal/inverse decryption function is expressed $ y' = A' x + B $

## How to compute A' value?

Calculate the modular inverse of A, modulo the length of the alphabet (see below for pre-calculated values).

## How to compute B' value?

B' has the same value as B, for this reason, this variable should not be called B' but B.

## What are the A' values?

The value of A' depends on A but also on the alphabet's length, if it is a classic one, it is 26 characters long. The values of A' are then:

A = 1 A' = 1 A = 3 A' = 9 A = 5 A' = 21 A = 7 A' = 15 A = 9 A' = 3 A = 11 A' = 19 A = 15 A' = 7 A = 17 A' = 23 A = 19 A' = 11 A = 21 A' = 5 A = 23 A' = 17 A = 25 A' = 25

A = 1 A' = 1 A = 3 A' = 9 A = 5 A' = 21 A = 7 A' = 15 A = 9 A' = 3 A = 11 A' = 19 A = 15 A' = 7 A = 17 A' = 23 A = 19 A' = 11 A = 21 A' = 5 A = 23 A' = 17 A = 25 A' = 25

## Why is there a constraint on the value of A?

Bézout's theorem states that $ A' $ exists only if $ A $ and $ 26 $ (the length of the alphabet) are coprime . This restricts $ A $ to the values $ 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25 $.

## Is it possible to use a key A not coprime with 26?

Yes, but this makes decryption non-unique: the same ciphered letter can correspond to several plaintext letters.

## Does a negative value for A exist?

Yes, but every negative value of $ A $ has a positive equivalent modulo 26 .

Example: An encryption with a value of $ A = -1 $ is identical to an encryption with a value of $ A = 25 $ (because $ 25 \equiv -1 \mod 26 $)

## Is there a limitation on B value?

No, $ B $ can be any integer, but all values of $ B $ modulo 26 (the length of the alphabet) are equivalent. Thus, if $ B $ is negative, there exists an equivalent positive value of $ B $.

Example: An encryption with $ B = -1 $ is equivalent to an encryption with $ B = 25 $

## Why is this encryption so called affine?

In mathematics, an affine function is defined by addition and multiplication of the variable (often $ x $) and written $ f(x) = ax + b $. The affine cipher is similar to the $ f $ function as it uses the values $ a $ and $ b $ as a coefficient and the variable $ x $ is the letter to be encrypted.

An affine function is a linear function because its graph is a straight line.

## When was Affine invented?

Date and author are unknown, the affine cipher .
