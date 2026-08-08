# Book Cipher

> Source: [https://www.dcode.fr/book-cipher](https://www.dcode.fr/book-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Book cipher? (Definition)

The book cipher is a substitution cipher that uses a book as a reference table/index, each letter is encoded by the position (or rank) of a word or a letter in a text/book.

The book is used as a reference to select words or letters that serve to encode the message.

dCode is limited to 1 number because it cannot manage the pagination and/or the exact position of a word in a formatted text.

## What are the variants of the book cipher?

A variant with 2 numbers uses the numbered pages of the book to no longer associate a single number but 2 numbers: the page number and the number of the word in the page.

Another 3-number variant for (page - line - word) or (page - word - letter) or (page - paragraph - word)

An alternative to 4 numbers for page - line - word - letter.

Beale has proposed three cryptograms, one of which (the second one, called the Beale cipher) is coded by this principle. It uses precisely as a dictionary the declaration of independence of the United States of America.

The Chappe code uses a reference dictionary where the words are already numbered.

## How to encrypt using Book cipher?

The Book cipher encryption consists of indexing a text by numbering from 1 to n each word. A letter (or a word) is coded by the number of the word beginning with that same letter (or the whole word).

Choose a well-defined text or book in order to have a precise word list and to facilitate decoding.

Example: Using the Declaration of Independence of the United States of America. To encode DCODE , therefore, the words DISSOLVE,COURSE,ONE,DECENT,EVENTS (with D,C,O,D,E as initials) can be taken (with their respective indexes 15,4,12,52,7 ) to describe a coded message.

The book cipher is easy to use, does not require specialized hardware, and can be used with any book or text. It can also be used creatively to hide messages in seemingly ordinary texts.

## How to decrypt a Book cipher?

Book cipher decryption consists in retrieving the word corresponding to the number and extracting the latter or only its first letter.

Example: For 221,132,136,305 the words are BY,OF,OF,KING or (take the first letters) BOOK .

## How are words counted?

Any sequence of 1 to n consecutive letters (or digits) (not interrupted by any other character) is considered as a word.

Example: ALICE'S ADVENTURES IN WONDERLAND contains 5 words: ALICE,S,ADVENTURES,IN,WONDERLAND

## How to recognize a Book ciphertext?

The message usually consists of several numbers, from a few tens to sometimes a thousand for the big books (but it is rare because it requires to count up to 1000 words of the book).

All references to books, pages, lines, words, even paper or a library are clues.

Some people call this book substutition ottendorf cipher .

## How to decipher a text without the book?

Without knowing the dictionary used it is impossible to decode this cipher.

Also, it is necessary to agree on the book but also its version, all the printed versions of the same book are not all identical.

## When was Book cipher invented?

The first traces of the book cipher are dated from the invention of printing, but could be considered on any paper medium.
