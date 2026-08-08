# Hill Cipher

> Source: [https://www.dcode.fr/hill-cipher](https://www.dcode.fr/hill-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Hill cipher? (Definition)

The Hill cipher is a polyalphabetic and polygraphic cipher, using linear algebra and modular arithmetic . Unlike classical substitution ciphers that encrypt letters one by one, the Hill cipher deals with groups of letters called ngrams using a square numerical matrix as the encryption key.

## How to encrypt using Hill cipher?

Hill cipher encryption uses an alphabet and a square matrix $ M $ of size $ n $ made up of integers numbers and called encryption matrix.

Example: Encrypt the plain text DCODE with the latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ and the matrix $ M $ (size $ n=2 $): $$ M = \begin{bmatrix} 2 & 3 \\ 5 & 7 \end{bmatrix} $$

Split the text into $ n $-grams. Complete any final incomplete ngrams with random letters if necessary.

Example: The matrix $ M $ is a 2x2 matrix, DCODE , split in 2-grams, becomes DC,OD,EZ ( Z letter has been added to complete the last bigram )

Substitute the letters of the plain message by a value: their rank in the alphabet starting from $ 0 $.

Example: The alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ leads to A=0,B=1,…,Z=25 . Groups of letters DC , OD , EZ become the groups of values (3,2) , (14,3) , (4,25)

It is possible (but not recommended) to use ZABCDEFGHIJKLMNOPQRSTUVWXY in order to get A=1,B=2,…Y=25,Z=0 .

For each group of values $ P $ of the plain text (mathematically equivalent to a vector of size $ n $), compute the matrix product : $$ M.P \equiv C \mod 26 $$ where $ C $ is the calculated vector (a group) of ciphered values and $ 26 $ the alphabet length.

Example: $$ \begin{bmatrix} 2 & 3 \\ 5 & 7 \end{bmatrix} \cdot \begin{bmatrix} 3 \\ 2 \end{bmatrix} \equiv \begin{bmatrix} 12 \\ 3 \end{bmatrix} \mod 26 $$

From cipher values $ C $, retrieve cipher letters of the same rank in the alphabet .

Example: $ 12 $ is equal to M and $ 3 $ is equal to D . And so on, DCODEZ is encrypted MDLNFN .

## How to decrypt Hill cipher?

Hill cipher decryption needs the matrix and the alphabet used. Decryption involves matrix computations such as matrix inversion, and arithmetic calculations such as modular inverse .

To decrypt hill ciphertext, compute the matrix inverse modulo 26 (where 26 is the alphabet length), requiring the matrix to be invertible.

Example: Using the example matrix, compute the inverse matrix ( modulo 26 ) : $$ \begin{bmatrix} 2 & 3 \\ 5 & 7 \end{bmatrix}^{-1} \equiv \begin{bmatrix} -7 & 3 \\ 5 & -2 \end{bmatrix} \equiv \begin{bmatrix} 19 & 3 \\ 5 & 24 \end{bmatrix} \mod 26 $$

Decryption consists in encrypting the ciphertext with the inverse matrix .

Note that not all matrices can be adapted to hill cipher. The determinant of the matrix has to be coprime with 26.

## Why must the determinant of the Hill matrix be coprime with 26?

The determinant of the Hill matrix must be coprime to $ 26 $ for the matrix to be invertible modulo $ 26 $ (the value 26 comes from the length of the Latin alphabet, which has 26 letters).

Mathematically, this means that the determinant has a modular inverse modulo $26$. This property guarantees that the encryption is bijective: each ngram in the plaintext corresponds to a unique ciphertext ngram, and vice versa.

If the determinant shares a common factor with $ 26 $, then several different vectors can produce the same ciphertext. In this case, decryption becomes unambiguously impossible.

For a 2x2 matrix, the 4 numbers $ \{ a,b,c,d \} $ must satisfy the condition that $ ad-bc $ is coprime with 26.

## How to recognize Hill ciphertext?

The ciphered message has a small index of coincidence and similar ngrams can be coded using the same letters.

Any reference to an actual hill or mountain is a clue.

Sometimes the groups of letters are left visible (all of length n = 2, 3 or 4) which suggests that the matrix is of size n.

The Hill cipher is also vulnerable to known plaintext attacks: if enough plaintext/ciphertext pairs are known, it becomes possible to reconstruct the cipher matrix using linear algebra.

## How to decipher Hill without the key matrix?

dCode proposes to bruteforce test around 6000 combinations of 2x2 matrices (with digits between 1 and 9) and alphabets.

For matrices containing numbers $ >= 10 $ or larger size matrices, computation times become exponentially longer.

## What are the variants of the Hill cipher?

Hill is already a variant of Affine cipher . Few variants, except the use of large size matrices.

## When was the Hill cipher invented?

Hill cipher has been created in 1929 by Lester S. Hill
