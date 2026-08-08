# Android Keyboard Long Press

> Source: [https://www.dcode.fr/keyboard-android-long-press](https://www.dcode.fr/keyboard-android-long-press)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is a long press on an Android keyboard (Gboard)? (Definition)

A long press on an Android keyboard like Gboard involves holding down a key for longer than a certain threshold (usually a few hundred milliseconds).

When this threshold is exceeded, the keyboard displays one or more alternative characters associated with the key.

## How do I encode a symbol using a long press on Gboard?

To encode a message using long presses, use a lookup table that associates each letter with a symbol accessible via a long press. Here is the lookup table for the default GBoard QWERTY keyboard:

A @ D $ G ^ J * M ¿ P ] S # V : Y _ B ; E ÷ H & K ( N ¡ Q + T / W x Z - C \" F % I > L ) O [ R = U < X '

A @ D $ G ^ J * M ¿ P ] S # V : Y _ B ; E ÷ H & K ( N ¡ Q + T / W x Z - C \" F % I > L ) O [ R = U < X '

Example: GBOARD translates to &;{@=$ ou &;914€

The key mappings depend on the user's keyboard layout; in QWERTY, the key mappings are not the same as in AZERTY.

Google may change these mappings in keyboard updates.

## How do I decode a symbol obtained by long-pressing on Gboard?

To decode a symbol (that is, to identify the originating key), consult the standard key assignment table (see above).

The decoded message is obtained by replacing each symbol with the corresponding letter in the table.

## How do I recognize the symbols associated with each key on Gboard?

The message is theoretically composed solely of special characters (among the most common):

@, ;, ", $, ÷, %, ^, &, =, >, *, (, ), ¿, ¡, [, ], +, #, /, <, :, >, ', _, -

## Why do some symbols change depending on whether the number line is activated or not?

The presence of the number row allows characters to be accessed by long-pressing because the virtual keyboard layout is adaptive.

A smartphone keyboard has limited display space. When the number row is activated, the numbers 0 through 9 occupy a dedicated row.

The keyboard can then rearrange the alternative characters across the 26 letters.

Conversely, if the number row is not displayed, the 10 digits become accessible by long-pressing the first row of keys.
