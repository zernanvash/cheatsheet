# VIC Cipher

> Source: [https://www.dcode.fr/vic-cipher](https://www.dcode.fr/vic-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Vic cipher? (Definition)

The VIC cipher is a substitution cipher with an overencryption using transposition , named after a spy called Victor .

## How to encrypt using Vic cipher?

Vic encryption starts with the creation of a grid called Straddling Checkerboard generated from a deranged alphabet (see below on how to create it)

Example: The following grid (with the numbers 2 and 6 and an upside-down deranged alphabet complemented by . and / ) \ 0 1 2 3 4 5 6 7 8 9 . / ␣ Z Y X ␣ W V U 2 T S R Q P O N M L K 6 J I H G F E D C B A

\ 0 1 2 3 4 5 6 7 8 9 . / ␣ Z Y X ␣ W V U 2 T S R Q P O N M L K 6 J I H G F E D C B A

Each character is then associated with its coordinates (row, column), so the plain message can then be coded numerically by following these associations.

Example: The text VICTOR is coded 8,61,67,20,25,22 or 86167202522 (by concatenation)

The Vic cipher may end there, but an over-encryption is possible by using a numeric key that will be added, digit after digit, modulo 10 .

Example: The key 0248 is used, the over-encrypted code becomes 88547240546 via the calculation: Cipher message 8 6 1 6 7 2 0 2 5 2 2 Key (repeated) 0 2 4 8 0 2 4 8 0 2 4 Addition (mod 10) 8 8 5 4 7 4 4 0 5 4 6

Cipher message 8 6 1 6 7 2 0 2 5 2 2 Key (repeated) 0 2 4 8 0 2 4 8 0 2 4 Addition (mod 10) 8 8 5 4 7 4 4 0 5 4 6

A final step, optional, is to convert the numbers obtained into letters, via the checkerboard / grid.

If the last digit corresponds to a row identifier of the grid, then add another digit randomly to make this last step possible. The consequence is that the decoded message will have a superfluous extra letter.

Example: 8 => V , 5 => X , etc. (the last digit 6 does not exist, but, for example, 60 exists) to get the final message VVXYWYY.XYJ

## How to decrypt Vic cipher?

The Vic decryption requires to know the grid (or checkerboard) used during the encryption.

Example: \ 0 1 2 3 4 5 6 7 8 9 P ␣ I A ␣ B C D E F 1 G H J K L M N O Q R 4 S T U V W X Y Z . /

\ 0 1 2 3 4 5 6 7 8 9 P ␣ I A ␣ B C D E F 1 G H J K L M N O Q R 4 S T U V W X Y Z . /

The encrypted message may be in numeric or alphabetic form (depending on the optional steps selected during encryption).

If the message is alphabetic, then convert it to numeric via the grid (row, column coordinates) otherwise skip this step

Example: The message DMPBDBFEU is then translated to 71505759842

If the encryption used a numeric key, then subtract it digit after digit, via a subtraction modulo 10 .

Example: The key 314 was used, the result of the subtraction is then 40247328417 via the calculation: Cipher message 7 1 5 0 5 7 5 9 8 4 8 Key (repeated) 3 1 4 3 1 4 3 1 4 3 1 Subtraction (mod 10) 4 0 1 7 4 3 2 8 4 1 7

Cipher message 7 1 5 0 5 7 5 9 8 4 8 Key (repeated) 3 1 4 3 1 4 3 1 4 3 1 Subtraction (mod 10) 4 0 1 7 4 3 2 8 4 1 7

Transcribe the numeric code into letters via the grid using the coordinates (row, column) to get the plain message.

Example: 40 => S , 17 => O , 43 => V , 2 => I , 8 => E , 41 => T , 7 => D soit SOVIET (+ D , the last letter is a residue)

## How to generate the Vic grid/checkerboard?

The grid / checkerboard contains an alphabet of 28 characters over 3 rows and 10 columns marked with numerical coordinates. By default, the 28 characters are ABCDEFGHIJKLMNOPQRSTUVWXYZ and the characters . (dot) and / (slash) in a random or predefined order (refer to the generation of deranged alphabets ). The column coordinates ranges from 0 to 9 ( 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ) and the coordinates of the rows ranges from 0 to 2 ( 0 , 1 , 2 ), but it is common not to display the 0 and to use 2 others numbers instead of 1 and 2 to make encryption more complex. The grid is filled with the 28 characters, that is 1 character per box except for the coordinates 0,1 and 0,2 (where '0, x' are the figures chosen previously for the row numbers).

Example: The alphabet AZERTYUIOPQSDFGHJKLMWXCVBN./ combined with the numbers 3 and 7 make it possible to create the grid \ 0 1 2 3 4 5 6 7 8 9 A Z E ␣ R T Y ␣ U I 3 O P Q S D F G H J K 7 L M W X C V B N . /

\ 0 1 2 3 4 5 6 7 8 9 A Z E ␣ R T Y ␣ U I 3 O P Q S D F G H J K 7 L M W X C V B N . /

This grid makes it possible to generate associations between numbers (coordinate row, column) and characters, these associations are used for the encryption and the decryption.

Example: Z is associated with 1 (the characters of the first row are associated with a number), B is associated with 76 (the characters of the other rows have 2 digits)

## How to recognize a Vic ciphertext?

A message encrypted by Vic is either numeric or alphabetic (+ the two characters . and / ).

If the message is numeric and without a key, it contains 2 digits that have a higher occurrence frequency than the others (the 2 digits of the grid).

If the message is alphabetical, it contains 8 characters with a frequency higher than the others (those of the first row of the grid).

The story of this cipher is in part linked to a microfilm found in a coin by a Brooklyn newspapers' boy who had never been deciphered until a Russian spy, named Reino Häyhänen, described its encryption system to the FBI. Any reference to a microfilm, New York or a newspaper delivery man is a clue.

## How to decipher Vic without the grid?

The knowledge of the grid is almost indispensable, the number of grid possibilities is of the order of 10^30. Brute force attack is therefore deprecated, unless the grid is generated from a single common keyword.

## How to decipher Vic without the key?

The key can be bruteforced if it is short, the number of attempts is 10^(key size).

## What are the variants of the Vic cipher?

The Vic cipher has several optional steps, depending on their application, the results may be different.

The Vic cipher being of Russian origin, it is often associated with the nihilist cipher of which it is itself considered as a variant.

## When was Vic cipher invented?

The use of Vic cipher was established in the 1950s, its first traces date back to 1953 where US intelligence associated it with the Russian (Soviet Union) spy Reino Häyhänen, known as Victor .
