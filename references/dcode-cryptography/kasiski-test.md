# Kasiski's Test

> Source: [https://www.dcode.fr/kasiski-test](https://www.dcode.fr/kasiski-test)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Kasiski examination? (Definition)

The Kasiski examination is a classical cryptanalysis method published by Friedrich Kasiski in 1863.

The purpose of the test is to estimate the period P of the cipher, that is, the probable length of the key used in a periodic polyalphabetic cipher such as the Vigenère cipher .

Once P has been estimated, the ciphertext can be divided into P subtexts. Each subtext then corresponds to the same alphabetic shift and can be analysed as an independent Caesar cipher .

The method relies on searching for repetitions in the ciphertext in order to recover clues about the periodicity of the key.

The technique had also been discovered independently by Charles Babbage around 1854, without any official publication at that time.

## What is the principle behind the Kasiski examination?

The test relies on a periodicity property of the Vigenère cipher . If the same n-gram from the plaintext appears several times and is encrypted with the same position in the key, then the resulting encrypted n-gram will be identical.

The distance between these repetitions in the ciphertext is then often a multiple of the period P.

The principle consists of identifying repeated sequences in the ciphertext, measuring the distances between them, then searching for common factors likely to correspond to P.

Some repetitions may nevertheless appear by chance, which introduces noise into the analysis and can produce false candidates.

## How is the Kasiski examination applied?

The Kasiski examination is generally applied in several steps:

— identify repeated sequences in the ciphertext

Example: In ABCDEFABCGHIJ , ABC is repeated twice (position 1 and position 7)

— measure the distances between these repetitions

— factorise these distances

Example: The distance between 2 ABC is 6, the factors of 6 are 2 and 3

— identify the factors that appear most frequently

The most frequent factors constitute plausible candidates for the period P.

The result must then be confirmed using other methods, particularly the index of coincidence .

The principle consists of dividing the ciphertext into P subtexts and then calculating the index of coincidence for each one. If the obtained values approach those of a natural language, then the tested period becomes more credible.

## What are the limitations of the test?

The Kasiski examination becomes unreliable when exploitable repetitions are rare or absent. Several situations strongly limit its effectiveness:

— a key that is long relative to the size of the message, or even as long as the text itself (one-time pad)

— the autokey Vigenère cipher , whose key is not periodic

— texts that are too short to produce enough repetitions

## What role did the Kasiski examination play in the history of cryptanalysis?

The Kasiski examination marked a major milestone in the history of cryptanalysis.

Before this method, the Vigenère cipher was sometimes considered indecipherable.

Kasiski 's work demonstrated that a periodic polyalphabetic cipher could be attacked systematically through the analysis of repetitions.

This discovery contributed to the development of modern statistical cryptanalysis and deeply influenced the methods used until the 20th century.
