# Triliteral Cipher

> Source: [https://www.dcode.fr/triliteral-cipher](https://www.dcode.fr/triliteral-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a Triliteral cipher? (Definition)

A triliteral cipher (also called ternary or trifid ) is a substitution cipher where each letter or symbol in the plaintext message is replaced by a triplet of symbols.

The term triliteral means that the cipher uses three elements (3 letters) to represent a unit of information.

## How to encrypt using Triliteral cipher?

To encode with a triliteral cipher, follow these steps:

— Define a substitution alphabet (see below) so that each letter of the plaintext is associated with a triplet of symbols.

— Encode DCODE with the alphabet A=AAA , B=AAB , C=AAC , D=ABA , etc.

— Replace each letter of the plaintext with its corresponding triplet.

— The message is encrypted as: ABA AAC BBC ABA ABB

## What are the most common triliteral alphabets?

Base 3 (space ⌴ at the end = CCC ): A AAA B AAB C AAC D ABA E ABB F ABC G ACA H ACB I ACC J BAA K BAB L BAC M BBA N BBB O BBC P BCA Q BCB R BCC S CAA T CAB U CAC V CBA W CBB X CBC Y CCA Z CCB ⌴ CCC

A AAA B AAB C AAC D ABA E ABB F ABC G ACA H ACB I ACC J BAA K BAB L BAC M BBA N BBB O BBC P BCA Q BCB R BCC S CAA T CAB U CAC V CBA W CBB X CBC Y CCA Z CCB ⌴ CCC

Base 3 (space ⌴ at the beginning = AAA ): ⌴ AAA A AAB B AAC C ABA D ABB E ABC F ACA G ACB H ACC I BAA J BAB K BAC L BBA M BBB N BBC O BCA P BCB Q BCC R CAA S CAB T CAC U CBA V CBB W CBC X CCA Y CCB Z CCC

⌴ AAA A AAB B AAC C ABA D ABB E ABC F ACA G ACB H ACC I BAA J BAB K BAC L BBA M BBB N BBC O BCA P BCB Q BCC R CAA S CAB T CAC U CBA V CBB W CBC X CCA Y CCB Z CCC

Frederici: A AAB B AAC C ABA D ABB E ABC F ACA G ACB H ACC I BBA J BBA K BBC L BAB M BAA N BAC O BCB P BCA Q BCC R CCA S CCB T CAC U CAA V CAA W CAB X CBC Y CBA Z CBB

A AAB B AAC C ABA D ABB E ABC F ACA G ACB H ACC I BBA J BBA K BBC L BAB M BAA N BAC O BCB P BCA Q BCC R CCA S CCB T CAC U CAA V CAA W CAB X CBC Y CBA Z CBB

Cardan : A AAC B AAB C ACA D ACC E ACB F ABA G ABC H CAC I ABB J ABB K CAB L CAA M CCA N CCB O CBA P CBC Q CBB R BAA S CCC T BAC U BAB V BAB W BAB X BCA Y BCC Z BCB

A AAC B AAB C ACA D ACC E ACB F ABA G ABC H CAC I ABB J ABB K CAB L CAA M CCA N CCB O CBA P CBC Q CBB R BAA S CCC T BAC U BAB V BAB W BAB X BCA Y BCC Z BCB

Vigenere : A BBA B BAA C BAC D AAA E AAC F AAB G ACA H ACC I ACB J ACB K ABA L ABC M ABB N CCC O CCA P CCB Q CAA R CAC S CAB T CBA U CBC V CBC W CBC X CBB Y BBB Z BCB

A BBA B BAA C BAC D AAA E AAC F AAB G ACA H ACC I ACB J ACB K ABA L ABC M ABB N CCC O CCA P CCB Q CAA R CAC S CAB T CBA U CBC V CBC W CBC X CBB Y BBB Z BCB

Wilkins: A AAA B AAB C AAC D BAA E BBA F BBB G BBC H CAA I CCA J CCA K CCB L CCC M ABA N ABB O ABC P ACA Q ACB R ACC S BCA T BCB U BCC V BCC W BAB X CBA Y CBB Z CBC

A AAA B AAB C AAC D BAA E BBA F BBB G BBC H CAA I CCA J CCA K CCB L CCC M ABA N ABB O ABC P ACA Q ACB R ACC S BCA T BCB U BCC V BCC W BAB X CBA Y CBB Z CBC

Some sources present Wilkins' alphabet with different trigrams .

## How to decrypt Triliteral cipher?

To decode a triliteral ciphertext:

— Segment the ciphertext into triplets of 3 characters

Example: The message to be decrypted ABAAACBBCABAABB is segmented into ABA,AAC,BBC,ABA,ABB

— Replace each triplet with its corresponding letter in the substitution alphabet to reconstruct the plaintext

Example: Using the alphabet A=AAA , B=AAB , C=AAC , D=ABA , etc. The plaintext is DCODE .

## How to decipher Triliteral without knowing the alphabet?

If the substitution alphabet is unknown, it is possible to transform the ciphertext into a monoalphabetic substitution by grouping triplets and analyzing their frequency.

The ciphertext then becomes a monoalphabetic substitution , and if the ciphertext is long enough, decryption is possible.

## How to recognize triliteral ciphertext?

The ciphered message has 3 distinct characters equally distributed. It is usually the 3 letters A , B and C but it can be 3 numbers, or 3 different things.

Like a Bacon cipher, it is possible to hide a Triliteral cipher in a text, for example by alternating 3 fonts, or variations of letters: uppercase, lowercase , bold, italic, underlined, etc.

All notions of triplet, number 3, triple, words trifid , triliteral , tricode, triletter, tridigital, etc. are clues.

## What are the 27 combinations of the Triliteral Alphabet?

The list of permutations with repetition of 3 characters A , B and C is: AAA, AAB, AAC, ABA, ABB, ABC, ACA, ACB, ACC, BAA, BAB, BAC, BBA, BBB, BBC, BCA, BCB, BCC, CAA, CAB, CAC, CBA, CBB, CBC, CCA, CCB, CCC

These combinations allow for the representation of up to 27 different characters.

## When was the Triliteral cipher invented?

The first triliteral alphabet appeared between 1550 and 1650.
