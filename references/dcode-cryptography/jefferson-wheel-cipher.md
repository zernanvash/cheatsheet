# Jefferson Wheel Cipher

> Source: [https://www.dcode.fr/jefferson-wheel-cipher](https://www.dcode.fr/jefferson-wheel-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Jefferson Wheel cipher? (Definition)

Jefferson's wheel is a polyalphabetical cipher that uses a cylinder made of several vertical rotating wheels. Each of the 26 letters of the alphabet are randomly written on the edge of each wheel.

## How to encrypt using Jefferson Wheel cipher?

To write a message, the author turns the wheels and aligns the letters of his message on the same line.

There are several versions of the cylinder, each with a different alphabet number (between 10 and 25), and different alphabets all in a possibly modifiable order.

Example: The original configuration uses this series of 25 alphabets whose 17th begins with ARMYOFTHEUS (imagine each line as a vertical wheel): 1 ABCEIGDJFVUYMHTQKZOLRXSPWN 2 ACDEHFIJKTLMOUVYGZNPQXRWSB 3 ADKOMJUBGEPHSCZINXFYQRTVWL 4 AEDCBIFGJHLKMRUOQVPTNWYXZS 5 AFNQUKDOPITJBRHCYSLWEMZVXG 6 AGPOCIXLURNDYZHWBJSQFKVMET 7 AHXJEZBNIKPVROGSYDULCFMQTW 8 AIHPJOBWKCVFZLQERYNSUMGTDX 9 AJDSKQOIVTZEFHGYUNLPMBXWCR 10 AKELBDFJGHONMTPRQSVZUXYWIC 11 ALTMSXVQPNOHUWDIZYCGKRFBEJ 12 AMNFLHQGCUJTBYPZKXISRDVEWO 13 ANCJILDHBMKGXUZTSWQYVORPFE 14 AODWPKJVIUQHZCTXBLEGNYRSMF 15 APBVHIYKSGUENTCXOWFQDRLJZM 16 AQJNUBTGIMWZRVLXCSHDEOKFPY 17 ARMYOFTHEUSZJXDPCWGQIBKLNV 18 ASDMCNEQBOZPLGVJRKYTFUIWXH 19 ATOJYLFXNGWHVCMIRBSEKUPDZQ 20 AUTRZXQLYIOVBPESNHJWMDGFCK 21 AVNKHRGOXEYBFSJMUDQCLZWTIP 22 AWVSFDLIEBHKNRJQZGMXPUCOTY 23 AXKWREVDTUFOYHMLSIQNJCPGBZ 24 AYJPXMVKBQWUGLOSTECHNZFRID 25 AZDNBUHYFWJLVGRCQMPSOEXTKI

1 ABCEIGDJFVUYMHTQKZOLRXSPWN 2 ACDEHFIJKTLMOUVYGZNPQXRWSB 3 ADKOMJUBGEPHSCZINXFYQRTVWL 4 AEDCBIFGJHLKMRUOQVPTNWYXZS 5 AFNQUKDOPITJBRHCYSLWEMZVXG 6 AGPOCIXLURNDYZHWBJSQFKVMET 7 AHXJEZBNIKPVROGSYDULCFMQTW 8 AIHPJOBWKCVFZLQERYNSUMGTDX 9 AJDSKQOIVTZEFHGYUNLPMBXWCR 10 AKELBDFJGHONMTPRQSVZUXYWIC 11 ALTMSXVQPNOHUWDIZYCGKRFBEJ 12 AMNFLHQGCUJTBYPZKXISRDVEWO 13 ANCJILDHBMKGXUZTSWQYVORPFE 14 AODWPKJVIUQHZCTXBLEGNYRSMF 15 APBVHIYKSGUENTCXOWFQDRLJZM 16 AQJNUBTGIMWZRVLXCSHDEOKFPY 17 ARMYOFTHEUSZJXDPCWGQIBKLNV 18 ASDMCNEQBOZPLGVJRKYTFUIWXH 19 ATOJYLFXNGWHVCMIRBSEKUPDZQ 20 AUTRZXQLYIOVBPESNHJWMDGFCK 21 AVNKHRGOXEYBFSJMUDQCLZWTIP 22 AWVSFDLIEBHKNRJQZGMXPUCOTY 23 AXKWREVDTUFOYHMLSIQNJCPGBZ 24 AYJPXMVKBQWUGLOSTECHNZFRID 25 AZDNBUHYFWJLVGRCQMPSOEXTKI

The encrypted message consists of any other cylinder line (usually the top line or the bottom line). If there are not enough wheels, encrypt the beginning of the message normally and start over / continue with the remaining letters.

Example: Code JEFFERSON with the cylinder described below. Locate the first letter J on the first wheel 1 ABCEIGDJFVUYMHTQKZOLRXSPWN and take the letter directly below (here beside) or F . Continue with the Nth letter and the Nth wheel. The encrypted message is: FHYGMNYBL

## How to decrypt Jefferson Wheel cipher?

The Jefferson Wheel decryption requires knowing the configuration of the cylinder of the transmitter.

Position the letters of the encrypted message on the wheels and read the line directly (or directly above depending on how the coding was done)

Example: Decode the message WWPATYZSZ by locating the Nth letter on the Nth wheel (using the configuration described above). W on the wheel 1 ABCEIGDJFVUYMHTQKZOLRXSPWN is preceded by the letter P , and so on. The plain message is PRESIDENT .

## How to recognize a Jefferson's Wheel ciphertext?

The message has a low coincidence score (0.04) due to the use of multiple alphabets.

In its usual versions, the message contains only letters.

Jefferson's cylinder is often confused with the cryptex popularized by the novel Da Vinci Code.

## What are the variants of the Jefferson's Wheel cipher?

Without being a variant, the cylinder can have multiple configurations, in number of wheels and according to their order. A wheel rotation key can be used to complicate the decryption.

## When was Jefferson's Disks invented?

The invention of the cylinder by Thomas Jefferson is estimated in 1793.
