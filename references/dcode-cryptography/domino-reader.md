# Dominos in Digits

> Source: [https://www.dcode.fr/domino-reader](https://www.dcode.fr/domino-reader)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a domino? (Definition)

A domino is a rectangular tile divided into two ends, each bearing a numerical value represented by spots (called pips).

In standard game sets known as double-six, each half takes an integer value between 0 and 6 , generating a total of 28 unique tiles.

## How to encode a domino pair in textual notation?

To encode a domino in textual notation, the user can represent each tile as an ordered pair (a,b) , where a and b are the values of the two ends.

Example: A domino with the values 1 and 2 is written 12 or (1,2) or 1/2 .

By convention, the order can be ignored (undirected domino ), which implies that 1,2 is equivalent to 2,1

## How to encode a domino as a Unicode drawing?

The Unicode standard provides a set of glyphs/symbols for their visual display.

Dominoes are represented horizontally:

🀱🀲🀳🀴🀵🀶🀷🀸🀹🀺🀻🀼🀽🀾🀿🁀🁁🁂🁃🁄🁅🁆🁇🁈🁉🁊🁋🁌🁍🁎🁏🁐🁑🁒🁓🁔🁕🁖🁗🁘🁙🁚🁛🁜🁝🁞🁟🁠🁡🀰

and vertically:

🁣🁤🁥🁦🁧🁨🁩🁪🁫🁬🁭🁮🁯🁰🁱🁲🁳🁴🁵🁶🁷🁸🁹🁺🁻🁼🁽🁾🁿🂀🂁🂂🂃🂄🂅🂆🂇🂈🂉🂊🂋🂌🂍🂎🂏🂐🂑🂒🂓🁢

## How to decode a textual domino notation into a visual representation?

To decode a textual notation, the user must extract each pair a,b from the string.

Each pair is then interpreted as a domino whose two ends bear the values a and b respectively.

The visual representation then consists of associating these values with a corresponding graphical domino tile, possibly respecting the orientation if defined.

## Are there standardized formats for representing dominoes in computing?

There is no single universal standard for representing dominoes in computing, but several conventions exist depending on the context.

— Textual representation: (a,b) or (a,b)(c,d) for a sequence of dominoes.

— Unicode : there is a specific block of characters in Unicode (U+1F030 to U+1F09F), allowing for a 2D graphical representation.
