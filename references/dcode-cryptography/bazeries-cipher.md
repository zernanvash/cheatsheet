# Bazeries Cipher

> Source: [https://www.dcode.fr/bazeries-cipher](https://www.dcode.fr/bazeries-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Bazeries cipher? (Definition)

The Bazeries cipher is an encryption system created by Étienne Bazeries that combines two Polybius grids (square arrays of letters) and a transposition supercipher based on a number or keyword.

## How to encrypt using Bazeries cipher?

Bazeries encryption uses a number N, and two identical grids (usually square grids of 25 distinct characters).

Bazeries suggested generating the second grid from the number N, number written in letters , but any keyword is fine too.

Example: To crypt DCODE with N=23, use a first grid, generated with the alphabet (one letter should be removed) and written in columns and the second grid generated with the keyword TWENTYTHREE (one could have took TWOTHREE ) Grid 1 Grid 2 \ 1 2 3 4 5 1 A F L Q V 2 B G M R W 3 C H N S X 4 D I O T Y 5 E K P U Z \ 1 2 3 4 5 1 T W E N Y 2 H R A B C 3 D F G I K 4 L M O P Q 5 S U V X Z

Grid 1 Grid 2 \ 1 2 3 4 5 1 A F L Q V 2 B G M R W 3 C H N S X 4 D I O T Y 5 E K P U Z \ 1 2 3 4 5 1 T W E N Y 2 H R A B C 3 D F G I K 4 L M O P Q 5 S U V X Z

\ 1 2 3 4 5 1 A F L Q V 2 B G M R W 3 C H N S X 4 D I O T Y 5 E K P U Z

\ 1 2 3 4 5 1 T W E N Y 2 H R A B C 3 D F G I K 4 L M O P Q 5 S U V X Z

The message is segmented by groups of letters with cardinality equals to each digit of N (repeated if necessary).

Example: The number 23 is made of the digits 2 and 3, so split in 2 then 3 letters: DC then ODE .

If the groups of letters are larger than 10, indicate the successive sizes, separating them with commas if necessary.

The groups are then written backward

Example: DC becomes CD and ODE becomes EDO

The letters are located in the grid 1 and replaced by the letter in the same position in grid 2. The encrypted message is the result obtained.

Example: C (row 3, column 1, grid 1) is replaced by D (row 3, column 1, grid 1) and so on. The final Bazeries ciphered message is DLSLO .

## How to decrypt Bazeries cipher?

Bazeries decryption requires a number N and two grids (or the keys to generate them).

Example: The cipher message is DLSLO , the number N=23 , grid 1 transposed (without key) is: \ 1 2 3 4 5 1 A F L Q V 2 B G M R W 3 C H N S X 4 D I O T Y 5 E K P U Z and grid 2 (key: TWENTYTHREE created from N) : \ 1 2 3 4 5 1 T W E N Y 2 H R A B C 3 D F G I K 4 L M O P Q 5 S U V X Z

\ 1 2 3 4 5 1 A F L Q V 2 B G M R W 3 C H N S X 4 D I O T Y 5 E K P U Z

\ 1 2 3 4 5 1 T W E N Y 2 H R A B C 3 D F G I K 4 L M O P Q 5 S U V X Z

The message is segmented by groups of letters with cardinality equals to each digit of N (repeated if necessary).

Example: 23 is made of the digits 2 and 3, let's split the message by 2 then 3 letters: DL and SLO .

Groups of letters are written backward

Example: DL becomes LD and SLO becomes OLS

Each letter is located in the second grid, and replaced by the letter with the same coordinate in the first grid.

Example: L (row 4, column 1, grid 2) is replaced by D (row 4, column 1, grid 1) and so on. The original plain text is DCODE .

## How to recognize a Bazeries ciphertext?

A Bazeries ciphered message has an index of coincidence close to the language of the plain text.

The presence of a number (usually at least 2 digits) is a clue.

## How to decipher Bazeries without key?

One can crack Bazeries using frequency analysis , as it is a substitution, but a manual analysis is then needed to find the key used and reverse segments of the message.

## What are the variants of the Bazeries cipher?

Grids can be written in rows or in columns, they also can be switched.

Bazeries is already considered a variant of the Polybius cipher .

## When was Bazeries cipher invented?

The Bazeries cipher was invented around 1890 by Étienne Bazeries , a French military cryptographer.
