# Vigenere Cipher

> Source: [https://www.dcode.fr/vigenere-cipher](https://www.dcode.fr/vigenere-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Vigenere cipher? (Definition)

The Vigenère cipher (sometimes written Viginere) is a polyalphabetic encryption method using a keyword to encode a message.

Invented by the French cryptologist Blaise de Vigenère in the 16th century, it is based on the use of a grid/table called a Vigenère square which allows for shifts of the letters according to the keyword.

## How to encrypt using Vigenere cipher?

Vigenere cipher uses a key (and an alphabet).

Example: Encode plaintext DCODE with key CLE and Latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ .

Vigenère can be described by 2 encryption methods (which arrive at the same result)

METHOD 1: Vigenere cipher by adding letters

Vigenère cipher consists of adding the key to the plaintext.

— Map, for each letter, the value of its rank in the alphabet , starting from 0: A=0,B=1,…,Z=25 . The following letter addition calculations are actually number additions (the values of the letters are added).

— Perform the calculation (plain letter + keyword letter) ( modulo 26 ). NB: if the result is greater than or equal to 26, subtract 26 from the result (where 26 is the length of the alphabet).

— Repeat the calculation for the following letters, if necessary, match the length of the text to the key, this is repeated infinitely: CLECLECLEC..

Example: Take the first letters of the message D (=3) and the key K (=10) and add them 3+10= 13 . Note the value and continue with the next letter of the message C (=2) and the next letter of the key E (=4): 2+4= 6 etc. When you reach the end of the key, start again at the beginning of it.

— For each number obtained (which must be a value between 0 and 25), match the letter with the same rank in the alphabet . The encrypted message is composed of the sequence of letters obtained.

Example: D C O D E plain message 3 2 14 3 4 values for each letter K E Y K E key (repeated) 10 4 24 10 4 letter values for the key 13 6 12 13 8 result of the addition ( modulo 26 ) N G M N I ciphered message

D C O D E plain message 3 2 14 3 4 values for each letter K E Y K E key (repeated) 10 4 24 10 4 letter values for the key 13 6 12 13 8 result of the addition ( modulo 26 ) N G M N I ciphered message

METHOD 2: Vigenere encryption with a table

To encrypt with Vigenere via a two-input table, use the following grid/matrix (case where the alphabet is ABCDEFGHIJKLMNOPQRSTUVWXYZ ):

— Locate the column corresponding to the letter of the plain text and the row corresponding to the letter of the key, the intersection of the row and the column returns the encrypted letter.

Example: The intersection of column D (4th column), and row K (10th row) gives the encrypted letter N .

— Repeat with the next letter of the message and the next letter of the key, when you reach the end of the key, start again at the beginning of it.

Example: NGMNI is the encrypted message.

## How to decrypt Vigenere cipher?

Vigenere decryption requires a key (and an alphabet).

Example: Decrypt the message NGMNI with the key KEY and the Latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ

Vigenère can be described by 2 decryption methods (which arrive at the same result)

METHOD 1: Vigenere decryption by letter subtraction

Vigenère decryption consists in subtracting the key from the ciphertext.

— Match, for each letter, the value of its rank in the alphabet , starting from 0: 0=A,1=B,…,25=Z . The following letter subtraction calculations are in fact number subtractions (the values ​​of the letters are subtracted).

— Perform the calculation (encrypted letter - keyword letter) ( modulo 26 ). NB: if the result is negative (less than 0), add 26 to the result (where 26 is the length of the alphabet).

— Repeat the calculation for the following letters, if necessary, match the length of the text to the key, this is repeated infinitely: KEYKEYK..

Example: Take the first letters of the message N (=13) and the key K (=10) and subtract them (13-10=3), the letter of rank 3 is D .

— For each number obtained (which must be a value between 0 and 25), match the letter having the same rank in the alphabet . The plain message is composed of the sequence of letters obtained.

Example: N G M N I ciphered message 13 6 12 13 8 values for each letter K E Y K E key (repeated) 10 4 24 10 4 letter values for the key 3 2 14 3 4 result of the subtraction ( modulo 26 ) D C O D E plain original message

N G M N I ciphered message 13 6 12 13 8 values for each letter K E Y K E key (repeated) 10 4 24 10 4 letter values for the key 3 2 14 3 4 result of the subtraction ( modulo 26 ) D C O D E plain original message

METHOD 2: Vigenere decryption with a table

To decrypt with Vigenere via a square table with two entries, use the following grid/matrix (case where the alphabet is ABCDEFGHIJKLMNOPQRSTUVWXYZ ):

— Locate the row of the key letter (left column) and go through the row until you find the first letter of the encrypted message. Then, go up the column to read the corresponding plain letter (at the very top).

Example: The letter K corresponds to row 10, go through the row until you find N , and the name of this column is D , it is the first letter of the plain message.

— Repeat with the next letter of the message and the next letter of the key, when you reach the end of the key, start again at the beginning of it.

Example: DCODE is the original plain text.

## How to recognize Vigenere ciphertext?

Following a Vigenere encryption, the message has a coincidence index which decreases between 0.05 and 0.04 depending on the length of the key, it decreases towards 0.04 the longer the key is.

Any connection with France or the French nationality of Blaise de Vigenere is a clue.

Le chiffre indéchiffrable ( unbreakable cipher ) is an alternative name for the Vigenère cipher .

Tabula Recta is the latin name given to the Vigenère grid.

## How to break Vigenere without knowing the key?

Vigenère 's keyless decryption techniques begin with statistical methods that allow the length of the key to be found, then a frequency analysis allows each letter of the key to be found.

KASISKI TEST

The Kasiski Test (developed by Friedrich Kasiski in 1863) allows the length of the key used for encryption to be identified. It is based on the observation that, in a ciphertext with a repeated key, any sequence of letters appearing several times in the plaintext message has a probability of being encrypted with the same portion of the key, thus creating the same sequence of encrypted letters in the encoded message.

The Kasiski test consists of identifying repetitions of letters in the ciphertext and calculating the distance (in number of characters) between its occurrences. The common divisors of the distances obtained correspond to possible lengths for the key.

Example: ABC appears three times in the message ABCXYZABCKLMNOPQRSABC . The positions of ABC are 0, 6 and 18. The gaps between two identical sequence redundancies are 6, 12 and 18 (they are probably multiples of the key length). The most common divisors of these numbers are 2, 3 and 6, so the key has a high probability of being of length 2, 3 or 6.

CALCULATION OF THE COINCIDENCE INDEX

The coincidence index test consists of taking one letter out of N in the message, and measuring the coincidence index of the message obtained. The closer the coincidence index is to that of the supposed language of the plaintext, the higher the probability that N is the length of the key used.

Indeed, taking a letter out of N when N is the length of the key is equivalent to taking a series of encrypted letters always encrypted with the same offset (equivalent to a mono-alphabetic substitution ), the coincidence index is therefore equal to that of the plain text.

FREQUENCY ANALYSIS

Once the length of the key is determined, it is possible to break the Vigenère cipher using frequency analysis . This method is based on the predictable distribution of letters in a given language (such as the high frequency of the letters E , A , T or S in French or English).

— Divide the coded text into several subtexts, each subtext corresponding to the same offset according to the cycle of the key. (If the key has a length of N, this amounts to grouping all the letters located at positions multiples of N).

— Analyze each subtext independently: each subtext is encrypted with a shift cipher (or Caesar cipher )

— Calculate the frequency of letters in the subtext (count how many times each letter appears) and compare these frequencies with the frequencies of letters in the target language. The goal is therefore to find the shift applied to each subtext and to deduce the letter corresponding to the shift.

— Once the shift of each subtext is determined, deduce the key or apply the inverse shift (in negative) to the coded text.

## How to find the key when having both cipher and plaintext?

When encrypting, the key is added to the plain text to get encrypted text. So, from the encrypted text, subtract the plain text to get the key.

NB: This is equivalent to decrypting the encrypted text with the plain text as key. The key will then appear repeated.

Example: The cipher text is NGMNI and the corresponding plaintext is DCODE . Use DCODE as key to decrypt NGMNI and find as plaintext KEYKE which is in fact the key KEY (repeated).

## What are the variants of the Vigenere cipher?

The Vigenère cipher has inspired several variants:

— The Beaufort cipher: a variant of the Vigenère cipher where encryption consists of subtracting the plaintext from the key.

— The Gronsfeld cipher: a variant where the key is directly numeric (composed only of digits 0-9).

— The Vernam cipher or One-Time Pad (or single-key): the Vigenère cipher is applied, but the key is random and as long as the plaintext and is never reused (only one use to guarantee security).

— An autoclave Vigenère cipher (or common-key): rather than repeating a fixed key, at the end of the key, it is the plaintext (or ciphertext) that is used as the key. This makes the system less susceptible to statistical attacks.

— Vigenère cipher with disordered alphabet : the alphabet used in the Vigenère square can be modified to not follow the order ABCD..XYZ but can be derived from a keyword or completely random.

— Vigenère cipher with custom alphabet : other character sets, or symbols or numbers are used.

— Vigenère cipher with dynamic key: the key can change dynamically after certain characters or according to predefined rules.

— Saint-Cyr ruler: identical to Vigenère , the mechanical ruler uses two movable alphabet strips to facilitate encryption and decryption operations.

## How to choose the encryption key?

In order to make Vigenere resistant to attacks, the coder must determine the most secure encryption key possible. All attacks are based on detections of key repetitions, so to avoid this pitfall, it is necessary to use a key as long as possible so that it does not repeat itself, it must be random and of a length greater than or equal to the size of the text to be encrypted. This is the case of the Vernam cipher (One-Time Pad).

For even greater security, it is necessary that the key is not used to encrypt 2 different messages, because a second use of the key is equivalent to a repetition which would make it lose its security.

## What is the running key vigenere cipher?

The variant by running key uses a key length at least equal to that of the text. This technique makes it possible to secure Vigénère 's cipher as Kasiski 's attack is no longer valid.

To get a long enough key, it is common to use a long book or other message. The use of this kind of key then opens the possibility of other attacks, by probable word and / or by analysis of the frequencies of the characters if the message is long enough.

In the particular case where the entire key is made up of random characters (see Vernam one time pad), then the message becomes completely unbreakable by any method of cryptanalysis (unconditional security).

## What is the keyed vigenere cipher?

By using a disordered alphabet , or a key that allows the classical Latin alphabet to be modified, then the frequency analysis is more complex and the cipher is more resistant to classical attacks.

## What are the advantages of the Vigenere cipher versus Caesar Cipher?

Caesar cipher is in fact a Vigenere cipher with a 1-letter long key. Vigenere code uses longer keys that allows the letters to be crypted in multiple ways. The frequency analysis is no more enough to break a code.

## What is a Saint-Cyr slide?

Saint-Cyr slide is a rule-shaped instrument, a tool that simplifies manual encryption and decryption of a message encrypted with Vigenere . Its fixed part consists of the alphabet, and its sliding mobile part is a double alphabet.

To encrypt a letter, move the slider so that the A of the fixed part matches the letter of the key. Then look at the letter of the mobile part directly below the letter of the plain message written on the fixed part.

## Why the name Vigenere?

The Vigenère cipher is named after Blaise de Vigenère , a 16th-century French diplomat and cryptographer (1523–1596).

Although he did not invent this method of encryption, he popularized it by improving and describing it in his 1586 work Treatise on Ciphers, or Secret Ways to Write available here (affiliate link)

The method was originally proposed by Giovan Battista Bellaso , an Italian cryptographer, in 1553. However, Vigenère 's more comprehensive and detailed work helped to associate his name with the system.

## When Vigenere was invented?

Blaise de Vigenère wrote a treatise describing this cipher in 1586. A full reedition is available here (affiliate link) However another treatise from 1553 by Giovan Battista Bellaso already described a very similar system.
