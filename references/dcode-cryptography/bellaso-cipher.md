# Bellaso Cipher

> Source: [https://www.dcode.fr/bellaso-cipher](https://www.dcode.fr/bellaso-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Bellaso cipher? (Definition)

Bellaso cipher created by Giovan Battista Bellaso is a cryptographic poly-alphabetic process using one or two keys and adapted to the italian alphabet.

## How to encrypt using Bellaso cipher?

Bellaso encryption uses an alphabet, a key to generate N alphabets from the first one and a cipher key.

The original author used the italian alphabet with 20 letters ABCDEFGHILMNOPQRSTVX , please adapt it to the current Latin alphabet (26 letters) ABCDEFGHIJKLMNOPQRSTUVWXYZ to encrypt texts containing missing letters.

Example: Encrypt DCODE BELLASO with the alphabet ABCDEFGHILMNOPQRSTVX , the generation key CHIAVEALFABETICA for 5 alphabets and GIOVAN the ciphering key.

The first step is to generate reversible alphabets (see below).

Then go through the words in the message. For the nth word of the message, get the nth letter of the key (modulo key length) and substitute using the alphabet for the nth letter.

Example: Word 1: DCODE , Word 2 = BELLASO 1st letter of the key: G , alphabet for G = CHIAVDGMNO/LFBTPQRSXE , so the word DCODE becomes QLEQO 2nd letter of the key: I , alphabet for I = CHIAVDFGMN/XELPBTOQRS , so the word BELLASO becomes HNOOPGL The message is encrypted QLEQO HNOOPGL

## How to decrypt Bellaso cipher?

Bellaso decryption is identical to encryption, thanks to the alphabet generation method, the substitutions are self-reversing.

## How to generate Bellaso alphabets?

To generate Bellaso alphabets for encryption/decryption, follow these steps:

— Split the key word: take the distinct letters of the generating key and split them into two groups.

Example: the key word CHIAVEALPHABET becomes CHIAVELFBT , which splits into CHIAV and ELFBT

— Complete the alphabet: fill each portion with the remaining letters of the full alphabet in order.

Example: The remaining letters are DFGMNOQRSX, so the parts are filled CHIAVDFGMN/ELFBTPQRSX

— Generate subsequent alphabets: for each following alphabet i , keep the first half of the alphabet and shift the second part by n×i characters, where i is the alphabet number and n is an integer (usually 1). Repeat this process until you have N alphabets (usually N=5).

Example: For the second alphabet (i=1, n=1), shift ELFBTPQRSX by 1, resulting in LFBTPQRSXE . For the third alphabet (i=2, n=1), shift ELFBTPQRSX by 2, resulting in FBTPQRSXEL , etc.

— Associate Letters with Alphabets: number the alphabets from 1 to N and assign letters to each alphabet in sequence from alphabet 1. The first letter is associated with the alphabet 1 , the second with the alphabet 2 , etc. Continue this pattern until all letters are associated with an alphabet.

Example: With 5 alphabets, the sequence would be: C→1,H→2,I→3,A→4,V→5,D→1,G→2,M→3,N→4,O→5,E→1,L→2,F→3,B→4,T→5,P→1,Q→2,R→3,S→4,X→5 The 5 alphabets are: C,D,E,P CHIAVDGMNO ELFBTPQRSX H,G,L,Q CHIAVDGMNO LFBTPQRSXE I,M,F,R CHIAVDGMNO FBTPQRSXEL A,N,B,S CHIAVDGMNO BTPQRSXELF V,O,T,X CHIAVDGMNO TPQRSXELFB

C,D,E,P CHIAVDGMNO ELFBTPQRSX H,G,L,Q CHIAVDGMNO LFBTPQRSXE I,M,F,R CHIAVDGMNO FBTPQRSXEL A,N,B,S CHIAVDGMNO BTPQRSXELF V,O,T,X CHIAVDGMNO TPQRSXELFB

## How to recognize an Bellaso ciphertext?

The ciphered message has a smaller index of coincidence than to the language of the plaintext.

In its original version, only 20 characters are used (italian alphabet, U=V )

In its original version, the message use a word-separator (space).

Clues on Italy or Vigenere are not to be neglected.

## How to decipher Bellaso without key?

It is possible to find the number N of alphabet by analyzing frequency of one word out of N.

Each word is a monoalphabetic substitution , vulnerable to a word pattern search (dCode has a desubstitution tool).

Every k×Nth word is substituted with the same alphabet, if the text is long enough, the monoalphabetical substitution tool should be able to decrypt such subtext (constituted of each k×Nth word)

## When was Bellaso cipher invented?

A book from Giovanni Battista Bellaso describing the process is dated 1553.
