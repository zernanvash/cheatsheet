# Shannon Index

> Source: [https://www.dcode.fr/shannon-index](https://www.dcode.fr/shannon-index)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Shannon's Entropy Index? (Definition)

Shannon 's entropy index is a measure of the entropy, that applies to any numerical data, developed by Claude Shannon in the 1940s. It measures the frequencies of appearance of the items, and the more they are different, the more difficult it will be to predict the content (thus a greater uncertainty, more randomness, and thus a greater entropy).

## How to calculate Shannon's Entropy? (Formula)

Entropy is calculated from a list of elements: in a text, the elements will be the characters and in an array of numeric values, the elements will be the numbers.

For a string of characters with $ N $ items with $ k $ distinct, each element $ i $ having a number of occurence $ n_i $ and a frequency of appearance $ p_i ( = n_i/N ) $. The entropy of Shannon $ H $ is calculated according to the formula $$ H = -\sum_{i=1}^k p_i \log_2 (p_i) $$

Example: DCODE has 5 characters (4 distinct), the letter D appears 2 times (frequency: 2/5), and the 3 letters C , O and E each appear 1 time (frequency: 1/5), the calculation is: $ H = -\left( \frac{2}{5} \log_2(\frac{2}{5}) + 3 \times \frac{1}{5} \log_2(\frac{1}{5}) \right) \approx 1.921928 $

The value is always positive, the logarithms of numbers less than 1 are always negative, their sum too, the sign - makes it possible to obtain a positive result.

## What is the Shannon index for?

From the Shannon index, the optimal encoding of a string can be deduced. If the Shannon index of a string is 3.5, then it will take 4 bits (rounded up) by characters to encode it optimally. The Shannon index can then be useful for evaluating a compression ratio, the higher the entropy, the better the compression.

## What is Shannon's unit of entropy?

Shannon 's entropy is measured in bits.
