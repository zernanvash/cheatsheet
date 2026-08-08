# Caesar Cipher

> Source: [https://www.dcode.fr/caesar-cipher](https://www.dcode.fr/caesar-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Caesar cipher? (Definition)

The Caesar cipher (or Caesar code ) is a monoalphabetic substitution cipher, where each letter is replaced by another letter located a little further in the alphabet (therefore shifted but always the same for given cipher message).

The shift distance is chosen by a number called the offset, which can be right (A to B) or left (B to A).

For every shift to the right (of +N), there is an equivalent shift to the left (of 26-N) because the alphabet rotates on itself, the Caesar code is therefore sometimes called a rotation cipher .

## How to encrypt using Caesar cipher?

Encryption with Caesar code is based on an alphabet shift. The most commonly used shift/offset is by 3 letters such that A becomes D .

Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Caesar Alphabet (🠜3) DEFGHIJKLMNOPQRSTUVWXYZABC

Plain Alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ Caesar Alphabet (🠜3) DEFGHIJKLMNOPQRSTUVWXYZABC

Example: Crypt DCODEX with a shift of 3 . To encrypt D , take the alphabet and look 3 letters after: G . So D is encrypted with G . To encrypt X , loop the alphabet: after X : Y , after Y : Z , after Z : A . So X is coded A . DCODEX is coded GFRGHA

Another way to crypt , more mathematical, is to encode any letter x by (x+3) mod 26 .

Note A=0 , B=1 , …, Z=25 , and add a constant (the shift), then the result modulo 26 (alphabet length) is the coded text.

Example: To crypt D (of value 3 ), add the shift 3 : 3+3=6 and find the letter for 6 : 6=G , so D is crypted with G . To encrypt X=23 , 23+3=26 and 26 mod 26 = 0 , 0=A , so X is encrypted with A , etc. DCODEX is coded GFRGHA

## How to decrypt Caesar cipher?

Caesar code decryption replaces a letter another with an inverse alphabet shift: a previous letter in the alphabet.

Example: Decrypt GFRGHA with a shift of 3. To decrypt G , take the alphabet and look 3 letters before: D . So G is decrypted with D . To decrypt X , loop the alphabet: before A : Z , before Z : Y , before Y : X . So A is decrypted X . GFRGHA is decrypted DCODEX .

Another way to decrypt, more mathematical, note A=0 , B=1 , …, Z=25 , subtracts a constant (the shift), then the result modulo 26 (alphabet length) is the plain text.

Example: Take G=6 , subtract the shift 6-3=3 and 3=D , so G is decrypted with D Take A=0 , 0-3=-3 and -3 mod 26 = 23 , 23=X , so A is decrypted with X , etc. GFRGHA is decrypted DCODEX

## How to recognize Caesar ciphertext?

A message encoded with the Caesar cipher has constant shifts for each letter, so its frequency analysis diagram is shifted (by a number of letters equal to the shift).

The index of coincidence is equal to that of the plaintext (as with any substitution cipher).

Any reference to Caesar, general and emperor of Rome, his contemporaries (Cicero, Brutus, Cleopatra), or more generally to antiquity and the Roman Empire are clues.

Also, the presence of keywords like Julius (Iulius/Ivlivs), Ave, Augustus, or a (Caesar) salad can remind us of the Caesar imperator.

The English pronunciation of Caesar is close to seizure .

## How to decipher Caesar without knowing the shift?

It is possible to decipher a text encoded with the Caesar cipher even without knowing the shift used. Here are the main methods:

— Brute force attack (try all possible keys): there are only 25 possible shifts (since shifting by 26 returns to the original text). The correct offset can be identified by testing them one by one until you get a consistent text.

— Frequency analysis (identify the most common letters): languages ​​have characteristic letter frequencies. The letter E is the most common. If another letter appears very frequently in the ciphertext, it is probably a shifted E . By calculating the difference between this letter and the E , it is possible to determine the shift.

Example: If the letter X is the most frequent. Since X is 19 places after E in the alphabet, this means that the text was probably encrypted with an offset of 19.

— Use dCode, which applies these methods automatically

## Is the Caesar Cipher secure?

No, Caesar Cipher is not secure. This is an easy cipher to break. With a 26-letter alphabet, there are only 25 possible keys, making brute-force attacks very easy. dCode automatically decrypts any Caesar Cipher message in less than a second.

## What are the variants of the Caesar cipher?

Caesar cipher is best known with a shift of 3, all other shifts are possible. Some shifts are known with other cipher names.

Another variant changes the alphabet and introduces digits for example.

A Caesar cipher with an offset of N corresponds to an Affine cipher Ax+B with A=1 and B=N .

Caesar is sometimes written Cesar (in French) or Ceaser (bad typography).

## How to encrypt digits and numbers using Caesar cipher?

Caesar cipher is applicable only to letters of the alphabet. There are, however, several solutions to crypt numbers:

— Write the numbers in Roman numerals , the numbers becoming letters, it is enough to encode them normally

Example: Nine becomes IX which becomes LA with a shift of 3.

— Shift the numbers with the same shift as the letters.

Example: 9 becomes 12 (shift of +3)

— Integrate numbers in the alphabet.

Example: With the alphabet ABCDEF123 , 21 becomes BA with an offset of 3.

## Why the name Caesar Cipher?

Caesar (Caius Iulius Caesar) used this technique for some correspondences, especially military, for example with Cicerone (shift of 3).

However, it is possible that other civilizations also used it independently.

## What is August Cipher?

August Cipher is sometimes the name given to Caesar Cipher with a shift of 1.

## What are other Caesar Cipher names?

Caesar cipher is also known as Shift Cipher. This shifting property can be hidden in the name of Caesar variants, eg.:

CD code, C = D, the shift is 1

Hello (LO) code, L = O, the shift is 3

Jail (JL) code, J = L, the shift is 2

Ellen (LN) code, L = N, the shift is 2

Cutie (QT) code, Q = T, the shift is 3

Eiffel (FL) code, F = L, the shift is 6

WC code, W = C, the shift is 6

Empty (MT) code, M = T, the shift is 7

Baden Powell (scoutism founder), B = P, the shift is 14

Any (NE) code, N = E, the shift is 17

See You (CU) code, C = U, the shift is 18

I See (IC) code, I = C, the shift is 20

Easy (EZ) code, E = Z, the shift is 21

CEASAR (with a wrong spelling) where E=A or A=E, the shift is either +4 or -4 (=22)

Any 2-letter code that can give an association between a crypted char and the plain one (see gramograms)

ROT13 code, the shift is 13 and reversible

ROT5 code for digits, the shift is 5 and reversible

ROT47 code for ASCII printable characters, the shift is 47 and reversible

More generally ROT-N with N the shift, if N < 26 then the Latin alphabet is used, else it can be any other custom alphabet .

## How to cipher CAESAR with the Caesar code?

The 25 ways to cipher Caesar by itself: DBFTBS, ECGUCT, FDHVDU, GEIWEV, HFJXFW, IGKYGX, JHLZHY, KIMAIZ, LJNBJA, MKOCKB, NLPDLC, OMQEMD, PNRFNE, QOSGOF, RPTHPG, SQUIQH, TRVJRI, USWKSJ, VTXLTK, WUYMUL, XVZNVM, YWAOWN, ZXBPXO, AYCQYP, BZDRZQ

## How to write Caesar Cipher in pseudo-code?

For N from 1 to Text Length Do

Take C = Nth character of Text

Calculate R = the rank of C in the alphabet

Calculate R2 = (R + Shift) Modulo 26

Write the letter with rank R2 in the alphabet

End For Loop

## When Caesar Cipher was invented?

The code was named after Julius Caesar who was born in 100 BCE the first man which has testimonies (like Suetonius) proving that he used this type of substitution to protect his military communications.

The exact date of creation and its real author are unknown.
