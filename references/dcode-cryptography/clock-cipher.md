# Clock Cipher

> Source: [https://www.dcode.fr/clock-cipher](https://www.dcode.fr/clock-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Clock Cipher? (Definition)

A clock cipher is the name given to any type of encryption/code that associates the positions of the hands of an analog clock with letters of the alphabet.

A standard clock divided into 15-minute increments has 48 distinct positions (12 hours and 4 possible positions for the minutes: 00, 15, 30, 45). Since the Latin alphabet contains 26 letters, there are more positions than symbols to encode, and there is no standard correspondence between time and letters.

## How to encrypt using Clock cipher?

Clock code encoding involves associating a letter of the alphabet with a specific clock hand configuration.

To encode a message, the user must define a table that maps letters to times. Several methods are possible, for example:

Example: 00:00 = A , 01:00 = B , …, 11:00 = 'L, 00:30 = M , … 11:30 = X

Example: 01:00 = A , 02:00 = B , …, 11:00 = 'L, 00:30 = L , … 11:30 = W

Example: 00:00 = A , 00:15 = B , 00:30 = C , …

Example: 00:15 = A , 00:30 = B , 00:45 = C , …

The coded message is then represented in the form of needle clocks.

Example:

Often, it is not the absolute time that is important, but the position of the hands because 00:00 and 12:00 correspond to the same display.

## How to decrypt Clock cipher?

Decoding the clock code involves finding the letters associated with the hand configurations.

This operation requires knowledge of the lookup table used during encoding.

dCode automatically tests different correspondences (brute force). This approach consists of trying several plausible mappings between times and letters, then selecting the results that form a coherent text.

## How to recognize a Clock ciphertext?

A message using the clock code is generally recognizable by the presence of representations of analog clocks or schedules or any notion of time.

The characteristic clues are:

— drawings of clocks with two hands or times written in the format hh:mm

— values often limited to multiples of 15 minutes (ending in 00 , 15 , 30 , or 45 )

A variant is the clock semaphore code, where the classic semaphore symbols are replaced by clocks, the position of the hands simulating those of a human arm.

## Reference Images

![char(48)](../dcode-images/clock-cipher-char-48-910f2751.png)
![char(49)](../dcode-images/clock-cipher-char-49-37a18f3c.png)
![char(50)](../dcode-images/clock-cipher-char-50-e68600c1.png)
![char(51)](../dcode-images/clock-cipher-char-51-cc383d7e.png)
