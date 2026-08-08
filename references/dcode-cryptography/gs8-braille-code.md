# GS8 Braille Code

> Source: [https://www.dcode.fr/gs8-braille-code](https://www.dcode.fr/gs8-braille-code)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is GS8 Braille? (Definition)

Gardner–Salinas 8-dot braille (GS8) is an 8-dot variant of braille , primarily used in computing and scientific contexts.

Unlike traditional 6-dot braille , historically designed for tactile reading, GS8 expands the braille cell to 8 dots arranged in two columns of 4 dots, allowing for up to 256 distinct combinations .

This expansion facilitates the direct representation of lowercase letters, uppercase letters, numbers, mathematical symbols, and special characters without the need for contextual prefixes.

## How to encrypt using Gardner–Salinas 8 Braille?

The general principle is the same as that of standard braille : each character corresponds to a specific configuration of raised dots.

GS8's innovation lies in the use of two additional dots (points 7 and 8), allowing for the direct encoding of capital letters, mathematical symbols, or computer symbols without prior indicators.

a ⠁ b ⠃ c ⠉ d ⠙ e ⠑ f ⠋ g ⠛ h ⠓ i ⠊ j ⠚ k ⠅ l ⠇ m ⠍ n ⠝ o ⠕ p ⠏ q ⠟ r ⠗ s ⠎ t ⠞ u ⠥ v ⠧ w ⠺ x ⠭ y ⠽ z ⠵ A ⡁ B ⡃ C ⡉ D ⡙ E ⡑ F ⡋ G ⡛ H ⡓ I ⡊ J ⡚ K ⡅ L ⡇ M ⡍ N ⡝ O ⡕ P ⡏ Q ⡟ R ⡗ S ⡎ T ⡞ U ⡥ V ⡧ W ⡺ X ⡭ Y ⡽ Z ⡵

a ⠁ b ⠃ c ⠉ d ⠙ e ⠑ f ⠋ g ⠛ h ⠓ i ⠊ j ⠚ k ⠅ l ⠇ m ⠍ n ⠝ o ⠕ p ⠏ q ⠟ r ⠗ s ⠎ t ⠞ u ⠥ v ⠧ w ⠺ x ⠭ y ⠽ z ⠵ A ⡁ B ⡃ C ⡉ D ⡙ E ⡑ F ⡋ G ⡛ H ⡓ I ⡊ J ⡚ K ⡅ L ⡇ M ⡍ N ⡝ O ⡕ P ⡏ Q ⡟ R ⡗ S ⡎ T ⡞ U ⡥ V ⡧ W ⡺ X ⡭ Y ⡽ Z ⡵

Example: ' Braille ' is written ⡃⠗⠁⠊⠇⠇⠑

Lowercase letters are identical to those of standard 6-dot braille . Capital letters are represented using an additional dot, usually point 7 (bottom left).

## How to decrypt Gardner–Salinas 8 Braille?

Identify the lines of braille , and separate each character so that it has 2 columns of 4 dots (at most, it can be less).

Replace each Braille character with the corresponding character in the GS8 Braille alphabet.

## How to recognize a Braille GS8 message?

The text is composed of vertical rectangular cells of 2 columns by 4 rows of dots, unlike classic braille which is limited to 2x3.

All references to visual impairment (visually impaired, blind person, etc.) are clues.

GS8 is supported by Unicode in the U+2800 to U+28FF block.

## What is the numbering of the dots in GS8 Braille?

The GS8 braille display uses a numbering system backward compatible with braille .

Points 1 to 3 are located in the upper left corner, points 4 to 6 in the upper right corner, point 7 in the lower left corner, and point 8 in the lower right corner.
