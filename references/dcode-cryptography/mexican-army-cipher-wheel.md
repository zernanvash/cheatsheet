# Mexican Army Cipher Wheel

> Source: [https://www.dcode.fr/mexican-army-cipher-wheel](https://www.dcode.fr/mexican-army-cipher-wheel)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Mexican Army Wheel? (Definition)

The wheel of the Mexican army is in fact made up of 5 rotating concentric discs (also called wheels, or stages), whose position can be adjusted. Generally the outer wheel is fixed (the letters wheel) with the A at the top, so there are only 4 disks that are swiveling and adjustable.

The 4 disks are made of numbers from 00 to 99 as follows:

Disk 1 01,02,03,…,24,25,26 Disk 2 27,28,29,…,50,51,52 Disk 3 53,54,55,…,76,77,78 Disk 4 79,80,81,…,98,99,00,-,-,-,-

Disk 1 01,02,03,…,24,25,26 Disk 2 27,28,29,…,50,51,52 Disk 3 53,54,55,…,76,77,78 Disk 4 79,80,81,…,98,99,00,-,-,-,-

The fourth disc is composed of the numbers from 79 to 99 , followed by 00 (for 100) and 4 empty slots (which may be called 101 , 102 , 103 and 104 ).

## How to define the position (cipher key) of the wheel?

The position of the disks is the encryption key. The key (the position of the disks on each stage) is defined according to two methods:

— by a set of 4 numbers, those situated under the A

Example: 01,27,53,79

— by a set of 4 letters, those above (on the outer disk) of the numbers 01 , 27 , 53 and 79 (which are the smallest numbers of each disc)

Example: A,A,A,A

## How to encrypt using the Mexican Army Cipher Wheel?

At each letter of the plain message, the transmitter marks it on the outer dial and associates a two-digit (random) code among the 4 located directly below the letter.

Example: Given a dial positioned at stage 1 on 01 , at stage 2 on 27 , at stage 3 on 53 and at stage 4 on 79 (which is the default position, therefore associated with the 4 letters AAAA ).

Example: To encrypt DCODE , the transmitter locates the letter D and can choose either 04 , 30 , 56 or 82 to encrypt the first letter. For the C , the numbers 03 , 29 , 55 or 81 are possible. In the end, DCODE can be encrypted 8281670405 or 5629938257 or other.

## How to decrypt using the Mexican Army Cipher Wheel?

Decryption requires knowing the encryption key (the positions of the disks), usually 4 numbers or 4 letters, which make it possible to adjust the positions of the discs of the wheel.

To decrypt, the message is decomposed in pairs of 2 digits in order to retrieve, for each 2-digit number / code, the letter at the top (on the outer disk) of the number in the wheel and thus reconstitute the plain message.

Example: The encrypted message is 5681158231 , so 56 corresponds to D , 81 is located under C , etc. The plaintext is DCODE .

## How to select the position of the wheel?

The position of the 4 discs can be defined by 4 letters, any word or acronym can be used.

It is also possible to use the 4 2-digit numbers (the 1-digit numbers must be completed by an initial zero) or 8 digits.

## How to recognize a Mexican Army ciphertext?

The message consists only of digits and there is an even number (since the encrypted message consists of pairs of 2 digits). Any reference to Mexico, Mayan, fajitas, tequila etc. is a clue.

## What are variants of the Mexican Army wheel?

The Youtuber Michael Stevens (Vsauce, Ding) presented a very similar encrypted wheel sold under the name of INQ Cipher Wheel in his Curiosity Box VIII here

The numbers are represented there with the code of the mirror digits and the values 101,102,103,104 are replaced by V1, V2, V3 and a drawing of an octopus (named Inq)

## How to decipher Mexican Army cipher without wheel?

The cipher wheel of the Mexican Army is actually a polyalphabetic cipher with 4 alphabets per shift.

To find the 4 offsets, it is necessary to analyze the frequencies of the numbers between 01 and 26, the same for the numbers between 27 and 52, then 53 and 78 and 79 to 99.

Thus, the most used number between 01 and 26 will probably be an E , the position of the first wheel is then deduced therefrom. The same can be done for other discs.
