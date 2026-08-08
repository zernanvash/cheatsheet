# Ubchi Cipher

> Source: [https://www.dcode.fr/ubchi-cipher](https://www.dcode.fr/ubchi-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Ubchi cipher? (Definition)

Übchi is a double transposition cipher (with the same permutation key) used by the Germans during the First World War.

## How to encrypt using Ubchi cipher?

Ubchi consists of a columnar transposition , the addition of null letters, then a second columnar transposition .

Example: Encrypt SECRET with the key UBER

Step 1 - Write the message in a grid of width N with N the size of the key.

Example: The key UBER has 4 letters so U B E R S E C R E T

U B E R S E C R E T

Step 2 - Sort the key alphabetically and swap the columns of the table accordingly

Example: B E R U E C R S T E

B E R U E C R S T E

Step 3 - Read the table in columns from top to bottom and from left to right in order to get a new message

Example: Intermediate message: ETCRSE

Step 4 - Add null letters , any letter. Without this, the encryption is a classical double transposition , the addition of a single letter is enough to obfuscate the transposition method.

Example: Intermediate message: ETCRSEX (letter X added, it is preferable to add common letters to confuse the code breakers)

Step 5 - Repeat steps 1 to 3 a second time, the result is the final encrypted message.

Example: 1bis) U B E R E T C R S E X 2bis) B E R U T C R E E X S 3bis) Final message TECXRES

U B E R E T C R S E X

B E R U T C R E E X S

## How to decrypt Ubchi cipher?

Decryption begins by determining the form of the grid used during encryption. Count the number of characters in the encrypted message and the permutation key, in order to deduce the number of columns and thus, rows.

Example: Decipher TECXRES (7 letters) with the key UBER (4 letters), knowing there is 1 null letter, the table will have the form U B E R X X X X X X X

U B E R X X X X X X X

Step 1 - Sort the key in alphabetical order and fill in the grid in columns with the encrypted message.

Example: The grid fills up B E R U T C R E E X S

B E R U T C R E E X S

Step 2 - Swap the columns of the grid to find the letters of the key in the correct order.

Example: The grid is swapped U B E R E T C R S E X

U B E R E T C R S E X

Step 3 - Read the grid in lines from left to right then from top to bottom in order to get the message

Example: Intermediate message: ETCRSEX

Step 4 - Remove the null letters (found at the end of the message found)

Example: Intermediate message: ETCRSE (1 letter deleted, the letter X )

Step 5 - Repeat steps 1 to 3 a second time, the result is the original plain message.

Example: 1bis) B E R U E C R S T E 2bis) U B E R S E C R E T 3bis) Original plain message is SECRET

B E R U E C R S T E

U B E R S E C R E T

## How to recognize a Ubchi ciphertext?

Any message encrypted by Ubchi is a transposition of the characters of the original message, so the analysis of the frequency of the letters and the index of coincidence are the same as those of the plain message.

The cipher was abandoned by the Germans following an article in the French newspaper Le Matin in November 1914, which praised the success of the decryption by the French. Any reference to German coded messages or to the newspaper Le Matin is a clue.

## How to decipher Ubchi without key?

Attempting permutations by brute force is possible as long as the key is not too large (the number of possible permutations is equal to N! With N the size of the key).

The number of null letters is generally limited to 1 or 2. According to some sources, the number of null letters corresponded to the number of words in the permutation key.

## What are the variants of the Ubchi cipher?

The Ubchi figure could be made more complex by repeating the transposition several times or by performing a double transposition by modifying the key the second time.

## When Ubchi was invented?

The Ubchi cipher was used at the start of the First World War.

The principle of encryption by transposition dates from well before.
