# Babylonian Numerals

> Source: [https://www.dcode.fr/babylonian-numbers](https://www.dcode.fr/babylonian-numbers)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What are babylonian numbers? (Definition)

Babylonian numeration is a numbering system used by the ancient Babylonians/Sumerians in Mesopotamia to represent numbers. In mesopotamian/babylonian/sumerian number system, numbers are written in a cuneiform style with | (pipe or nail) and < (corner wedge or bracket), written in base 60 (sexagesimal).

## How to write babylonian numbers?

The number is written in base 60 , the 60 digits are broken down into vertical bars 𒐕 (often noted | ) which are worth one unit (1) and chevrons 𒌋 (often noted < ) which are worth ten (10) in base 10.

The power change of sixty ($ 60^1 = 60 $, $ 60^2 = 3600 $, $ 60^3 = 216000 $ etc.) is represented by an empty space.

Example: 23 is written with 2 tenths and 3 units so <<||| or

To convert a Babylonian number :

— Identify the positions (from right to left ). Each position represents a power of $ 60 $

— Multiply the value in each position by its power of $ 60 $

— Add the results to obtain the number in base $ 10 $

Example: A Babylonian number noted | |||| || (watch out for spaces), is broken down into || ($ 2 $) in the first position on the left, |||| ($ 4 $) in the second and | ($ 1 $) in the third is calculated as $ 2 \cdot 60^0 + 4 \cdot 60^1 + 1 \cdot 60^2 = 2 + 240 + 3600 = 3842 $

Since Unicode 5 (2006) cuneiform symbols can be represented on compatible browsers, here is the table of characters used by dCode: 𒐕 1 𒐖 2 𒐗 3 𒐘 4 𒐙 5 𒐚 6 𒐛 7 𒐜 8 𒐝 9 𒌋 10 𒎙 20 𒌍 30 𒐏 40 𒐐 50 NB: The double chevron character 𒎙 (20) has been forgotten in Unicode 5 (it existed as ⟪ ) and was added in Unicode 8 (2015) but may appear unknown (?) on some devices.

𒐕 1 𒐖 2 𒐗 3 𒐘 4 𒐙 5 𒐚 6 𒐛 7 𒐜 8 𒐝 9 𒌋 10 𒎙 20 𒌍 30 𒐏 40 𒐐 50

## How to write the number zero 0?

Babylonians did not use the zero (this concept had not been invented), but from the 3rd century in Babylon, they used the symbol (as a writing separator for numbers)

## How to convert babylonian numbers?

Converting is easy by counting symbols and considering it in base 60 to get numbers into classical Hindu-Arabic notation.

Example: <<||| is 2 < and 3 | so $ 2 \times 10 + 3 \times 1 = 23 $

Example: | | (note the space) is 1 | and then 1 | so $ 1 \times 60 + 1 = 61 $

## How to convert from base 10 to base 60?

To convert a number $ n $ from base $ 10 $ to base $ b=60 $ apply the algorithm::

— Divide the decimal number by $ 60 $ and note the whole quotient as well as the remainder

— Repeat the process with the quotient until it is equal to $ 0 $

— Read the remainders obtained in reverse order to obtain the representation in base $ 60 $

// pseudo-code function decimal_to_base60(n) { q = n b60 = [] while (q > 0) { r = q mod 60 b60 []= r q = q div 60 } return b60 }

Example: $$ q_0 = 100 \\ r_0 = 100 \mbox{ mod } 60 = 40 \;\;\; q_1 = 100 \mbox{ div } 60 = 1 \\ r_1 = 1 \mbox{ mod } 60 = 1 \;\;\; q_2 = 0 \\ \Rightarrow \{1,0,0\}_{(10)} = \{1, 40\}_{(60)} $$

## How to count using Babylonian numerals?

Babylonian numbers chart (base60) 0 (zero) 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59

0 (zero) 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59

For other numbers, use the form above.

## Why using the base 60?

60 has the advantage of having many divisors : 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, and 60.

Today the time system of hours still uses the numerotation in base sixty: 60 seconds = 1 minute, 60 minutes = 1 hour = 3600 seconds

## How to convert Babylonian numbers into roman numerals?

Convert the Babylonian numbers to Hindu-Arabic numerals (1,2,3,4,5,6,7,8,9,0), then use the Roman numeral converter of dCode.

## What traces remain of Babylonian numbers?

Clay tablets played a crucial role in understanding Babylonian numbers , as they were the medium on which the ancient Babylonians wrote their numerations. These tablets have survived through the centuries, providing a valuable source of information about the numerical and mathematical systems of this civilization.

## When are Babylonian numbers from?

Babylonian/Summerian numbers are thought to have been developed around 2000 BC.

## Reference Images

![char(66)](../dcode-images/babylonian-numbers-char-66-da1b32ce.png)
![char(51)](../dcode-images/babylonian-numbers-char-51-008682d9.png)
![char(48)](../dcode-images/babylonian-numbers-char-48-02ec43ef.png)
![char(49)](../dcode-images/babylonian-numbers-char-49-161887af.png)
![char(50)](../dcode-images/babylonian-numbers-char-50-348a94fc.png)
![char(52)](../dcode-images/babylonian-numbers-char-52-98f40962.png)
![char(53)](../dcode-images/babylonian-numbers-char-53-8b035918.png)
![char(54)](../dcode-images/babylonian-numbers-char-54-d1ad3537.png)
![char(55)](../dcode-images/babylonian-numbers-char-55-d50a725e.png)
![char(56)](../dcode-images/babylonian-numbers-char-56-4cd5d6d7.png)
![char(57)](../dcode-images/babylonian-numbers-char-57-de3a0d7d.png)
![char(65)](../dcode-images/babylonian-numbers-char-65-a0e0c4bd.png)
