# Alberti Cipher

> Source: [https://www.dcode.fr/alberti-cipher](https://www.dcode.fr/alberti-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Alberti cipher? (Definition)

The Alberti cipher is a polyalphabetic cipher system that uses two mobile concentric disks which can rotate.

## How to encrypt using Alberti cipher?

Encryption uses a disk with two alphabets, one fixed (stabilis) one moving (mobilis). By rotating a disk, it shifts an alphabet to the next letter.

To encrypt, the disk is set in one position, the initial shift (which can be zero) corresponds to the number of letters shifted at the beginning.

Example: The disk is composed of ABCDEFGHIJKLMNOPQRSTUVWXYZ for the large outer ring, and abcdefghijklmnopqrstuvwxyz for the small inner ring. A is in line with a , B is inline with b , etc. Rotating a disk by 2, then A is in line with c , and the initial shift becomes 2 .

Each letter of the plain text found on the outer ring, is replaced by the corresponding one (the one aligned) in the inner ring.

By default, every 4 characters (4 = period), the disk is rotated clockwise of 1 letter (1 = periodic increment), this changes the substituting alphabet.

Example: Encrypt DCODE with the parameters: initial shift: 1, periodic increment: 2, period: 3. Alphabets are such as ABCDEFGHIJKLMNOPQRSTUVWXYZ is aligned with bcdefghijklmnopqrstuvwxyza . The period begins, D is coded by e , C by d , O by p , the period (length 3) ends, the disk is rotated by 2 letters. Alphabets are now aligned like this: ABCDEFGHIJKLMNOPQRSTUVWXYZ with defghijklmnopqrstuvwxyzabc , the new period begins, etc. The encrypted message is edpgh

## How to decrypt Alberti cipher?

Le decryption needs the disk (or the 2 alphabets) and the parameters: initial position, period and shift.

To cipher a message, the disk is set with the corresponding initial shift. Each letter is identified on the inner disk, and is coded by the letter aligned in the outer disk.

By default, every 4 characters (4 = period), the disk is rotated counter-clockwise of 1 letter (1 = periodic increment).

Example: The parameters are: initial shift: 1, periodic increment: 2, period: 3, and the cipher message edpgh . Alphabets are such as ABCDEFGHIJKLMNOPQRSTUVWXYZ is aligned with bcdefghijklmnopqrstuvwxyza The period begins, e is decoded by D , d by C , p by O , the period (length 3) ends, the disk is rotated by 2 letters. Alphabets are now aligned like this: ABCDEFGHIJKLMNOPQRSTUVWXYZ with defghijklmnopqrstuvwxyzabc , the new period begins, etc. The original plain text is DCODE

## How to recognize an Alberti ciphertext?

The ciphered message has a polyalphabetic index of coincidence .

In its original version, the message has only these letters: ABCDEFGHIKLMNOPQRSTVXYZ and & , no J , U or W

The mention of De Cifris refers to the treaty published by Alberti presenting his cipher.

## What are usual alphabets for Alberti's wheel?

The outer disk (stabilis) is usually ABCDEFGILMNOPQRSTVXZ1234 , but there is also ABCDEFGHIKLMNOPQRSTVXYZ2 or ABCDEFGHIKLMNOPQRSTVXYZ- (which are rarer).

The inner disc (mobilis) is less well defined and several versions coexist:

— usqomkhfdbacegilnprtxz&y (De componendis cifris - Archivio di Stato Venezia CCX VI 1, Ferraioli Ms. 360-1, Vaticanus Latinus 5118, Vaticanus Latinus 5357)

— vsqomkhfdbacegilnp-rtxz7 (De componendis cifris - Marcianus 4702)

— zyxuronmilhgedcba&qtpsfk (De componendis cifris - Chigi M II 49)

— xihcnzvrypagqldfts&moebk (De componendis cifris - Riccardianus 927)

— mqihfdbacegklnprtuz&xyso (English & Italian Wikipedia)

— c&bmdgpfznxyvtoskerlhaiq (Ars Cryptographica)

## How to decipher Alberti without period or shift?

One can crack Alberti by brute-forcing all combinations of period, initial shift and periodic increment. Use the 'Bruteforce attack' button.

## When was the Alberti cipher invented?

Leon Battista Alberti would have invented this wheel around 1460.
