# RSA Cipher

> Source: [https://www.dcode.fr/rsa-cipher](https://www.dcode.fr/rsa-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the RSA cipher? (Definition)

RSA encryption (named after the initials of its creators Rivest, Shamir, and Adleman) is the most widely used asymmetric cryptography algorithm. Based on mathematical and arithmetic principles of prime numbers, it uses large numbers, a public key and a private key, to secure data exchanges on the Internet.

## How to encrypt using RSA cipher?

RSA encryption is purely mathematical, any message must first be encoded by integers (any encoding works: ASCII , Unicode , even A1Z26 ). To encrypt, RSA needs the numbers $ n $ and $ e $ called the public keys. The message $ M $ (numeric) is encrypted by the formula $$ C \equiv M^{e}{\pmod {n}} $$

Example: Encrypt the message R,S,A (encoded 0x525341 in ASCII or 5395265 in decimal) with the public key $ n = 6199931 $ and $ e = 101 $ or $ C = 5395265^{101} \mod 6199931 = 4331034 $, so the encrypted message is 4331034 .

If $ M $ is greater than $ n $ then the message is broken down into numbers (blocks smaller than $ n $)

## How to decrypt a RSA cipher?

Decryption requires knowing the private key $ d $ and the public key $ n $. For any (numeric) encrypted message $ C $, the plain (numeric) message $ M $ is computed: $$ M \equiv C^{d} \pmod{n} $$

Example: Decrypt the message C=4331034 with the public key $ n = 1022117 $ and the private key $ d = 5029565 $, that is $ M = 4331034^{5029565} \mod 1022117 = 5395265 $, 5395265 is the plain message (ie. 0x525341 in hexadecimal or the letters R,S,A in ASCII )

## How to generate RSA keys?

RSA needs a public key (consisting of 2 numbers $ (n, e) $) and a private key (only 1 number $ d $).

— Select 2 distinct prime numbers $ p $ and $ q $ (the larger they are and the stronger the encryption will be)

— Calculate $ n = p \times q $

— Calculate the indicator of Euler $ \phi(n) = (p-1)(q-1) $

— Select an integer $ e \in \mathbb{N} $, prime with $ \phi(n) $ such that $ e < \phi(n) $

— Calculate the modular inverse $ d \in \mathbb{N} $, ie. $ d \equiv e^{-1} \mod \phi(n) $ (via the extended Euclidean algorithm )

With these numbers, the pair $ (n, e) $ is called the public key and the number $ d $ is the private key.

Example: $ p = 1009 $ and $ q = 1013 $ so $ n = pq = 1022117 $ and $ \phi(n) = 1020096 $. The numbers $ e = 101 $ and $ \phi(n) $ are prime between them and $ d = 767597 $.

The keys are renewed regularly to avoid any risk of disclosure of the private key. It is essential never to use the same value of p or q several times to avoid attacks by searching for GCD .

Using identical $ p $ and $ q $ is a very bad idea, because the factorization becomes trivial $ n = p^2 $, but in this particular case, note that $ phi $ is calculated $ phi = p(p-1) $

## How to recognize RSA ciphertext?

The message is fully digital and is normally accompanied by at least one key (also digital).

In practice, the keys are sometimes displayed in hexadecimal , or stored in a certificate (encoded in base64 ).

The length of depends on the complexity of the RSA implemented (1024 or 2048 are common)

RSA encryption is used in the HTTPS protocol

## What are possible RSA attacks?

Method 1: Prime numbers factorization of $ n $ to find $ p $ and $ q $.

The RSA cipher is based on the assumption that it is not possible to quickly find the values $ p $ and $ q $, which is why the value $ n $ is public. To find the private key, a hacker must be able to perform the prime factorization of the number $ n $ to find its 2 factors $ p $ and $ q $. In practice, this decomposition is only possible for small values, i.e. a key $ n $ comprising less than 30 digits (for current algorithms and computers), between 30 and 100 digits, counting several minutes or hours, and beyond, calculation can take several years. With $ p $ and $ q $ the private key $ d $ can be calculated and the messages can be deciphered.

Method 2: Find the common factor to several public keys $ n $

Key generation is random but it is not unlikely that a factor $ p $ (or $ q $) could be used to calculate the values of 2 different public keys $ n $. By calculating the GCD of 2 keys, if the value found is different from 1, then the GCD is a first factor of $ n $ (therefore $ p $ or $ q $), by dividing $ n $ by the gcd is the second factor ($ p $ or $ q $).

Method 3: Chosen ciphertext attack

Given a published key ($ n $, $ e $) and a known encrypted message $ c \equiv m^e \pmod{n} $, it is possible to ask the correspondent to decrypt a chosen encrypted message $ c' $. Based on the property $ m_1^e m_2^e \equiv (m_1 m_2)^e \pmod{n} $, the decryption of a message $ c' \equiv c \times r^e \pmod{n} $ with $ r $ a chosen number (invertible modulo $ n $) will return the value $ m \times r \pmod{n} $. By calculating $ m \times r \times r^{-1} \pmod{n} $ (with $ r^{-1} $ the modular inverse ) is found $ m $ the original message.

Method 4: Problem with short messages with small exponent $ e $

For a small exponent ($ e = 3 $) and a short message $ m $ (less than $ n^{1/e} $) then the encrypted message $ c = m^e $ is less than $ n $, so the calculation of the modulo has no effect and it is possible to find the message $ m $ by calculating $ c^{1/e} $ ($ e $-th root).

Method 5: Wiener's attack for private keys $ d $ too small

If the private key $ d $ is small compared to the message $ n $ and such that $ d < \frac{1}{3} n^{\frac{1}{4}} $ and that $ p $ and $ q $ are close $ q < p < 2q $, then by calculating approximations of $ n/e $ using continued fractions , it is possible to find the value of $ p $ and $ q $ and therefore the value of $ d $.

## How to decrypt RSA without the private key?

To find the private key, a hacker must be able to realize the prime factor decomposition of the number $ n $ to find its 2 factors $ p $ and $ q $. For small values (up to a million or a billion), it's quite fast with current algorithms and computers, but beyond that, when the numbers $ p $ and $ q $ have several hundred digits, the decomposition requires on average several hundreds or thousands of years of calculation. There are databases listing factorizations like here

With the numbers $ p $ and $ q $ the private key $ d $ can be computed and the messages can be decrypted.

## Why using the number e=65537 for RSA?

The value $ e=65537 $ comes from a cost-effectiveness compromise.

A value of $ e $ that is too large increases the calculation times. A value of $ e $ that is too small increases the possibilities of attack.

$ 65357 $ is a Fermat number $ 65357 = 2^{2^4} + 1 $ which allows a simplification in the generation of prime numbers.

This value has become a standard, it is not recommended to change it in the context of secure exchanges.

## How to decrypt a number into plaintext?

The number found is an integer representing the decimal value of the plaintext content.

Generally, this number can be transcribed according to the character encoding used (such as ASCII or Unicode ).

Example: The whole number 431164974181 has hexadecimal writing 64,63,6F,64,65 i.e. the characters D,C,O,D,E (in ASCII code )

## What is an RSA certificate?

An RSA certificate is a text file containing the data useful for a cryptographic exchange by RSA .

There are 2 types of certificate:

— the public certificate, which begins with -----BEGIN PUBLIC KEY----- and which contains the values of the public keys $ N $ and $ e $.

— the private certificate, which starts with -----BEGIN RSA PRIVATE KEY----- and which contains all the values: $ N $, $ e $, $ d $, $ q $ and $ p $. This file is usually kept safe and should never be disclosed.

## When was RSA invented?

Ronald Rivest, Adi Shamir and Leonard Adleman described the algorithm in 1977 and then patented it in 1983.
