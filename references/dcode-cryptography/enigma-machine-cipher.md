# Enigma Machine

> Source: [https://www.dcode.fr/enigma-machine-cipher](https://www.dcode.fr/enigma-machine-cipher)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is the Enigma Machine? (Definition)

The Enigma Machine was an electromechanical encryption device used by the German armed forces during World War II to encrypt their communications.

## How to encrypt using Enigma cipher?

The Enigma Machine uses a system of rotating wheels (rotors) and electrical wiring to encrypt messages by polyalphabetic substitution.

The basic Enigma machine includes 1 wiring board, 3 rotors and 1 reflector, each element configurable independently (machine settings changing daily).

When a key is pressed by the user, the rotor(s) rotate one notch then an electrical signal leaves the keyboard, passes through the board, then the rotors from right to left , then the reflector, then the rotors from left to right, then the table again. At each stage, the wiring of the elements transforms the value of the letter into another. At the end, the number letter lights up on the top of the machine.

## How to decrypt using Enigma cipher?

The decryption process is the same as encryption. For a given setting, typing a letter L1 lights a letter L2, and conversely typing the letter L2 lights the letter L1.

## What is rotor order (Walzenlage)?

A rotor is a cylinder with a toothed wheel equipped with a set of internal electrical contacts allowing the letters of the alphabet to be permuted.

Example: The rotor named I has the wiring EKMFLGDQVZNTOWYHXUSPAIBRCJ , so the letter A ( position 1 in the alphabet ) would be transformed into E (position 1 of the rotor), the letter B (position 2) would be transformed into K etc.

The rotor configuration was called Walzenlage and described the order of the rotors from left to right. In fact, the user could insert several rotors into the machine, in any order.

Example: 'VI - II - III' indicates that the right rotor is III , then the middle one is II and the left one is VI .

dCode accepts the following rotors: Name Alphabet/Wiring Notch(es) I EKMFLGDQVZNTOWYHXUSPAIBRCJ Q II AJDKSIRUXBLHWTMCQGZNPYFVOE E III BDFHJLCPRTXVZNYEIWGAKMUSQO V IV ESOVPZJAYQUIRHXLNFTGKDCMWB J V VZBRGITYUPSDNHLXAWMJQOFECK Z VI JPGVOUMFYQBENHZRDKASXLICTW M,Z VII NZJHGRCXMYSWBOUFAIVLPEKQDT M,Z VIII FKQHTLXOCBJSPDZRAMEWNIUYGV M,Z BETA LEYJVCNIXWPBQMDRTAKZGFUHOS - GAMMA FSOKANUERHMBTIYCWLQPZXVGJD - IC EKMFLGDQVZNTOWYHXUSPAIBRCJ A,B,C,E,F,G,I,K,L,O,P,Q,S,U,V,W,Z IIC HQZGPJTMOBLNCIFDYAWVEUSRKX A,C,D,F,G,H,K,M,N,Q,S,T,V,Y,Z IIIC UQNTLSZFMREHDPXKIBVYGJCWOA A,E,F,H,K,M,N,R,U,W,X IR JGDQOXUSCAMIFRVTPNEWKBLZYH N IIR NTZPSFBOKMWRCJDIVLAEYUXHGQ E IIIR JVIUBHTCDYAKEQZPOSGXNRMWFL Y IK PEZUOHXSCVFMTBGLRINQJWAYDK Y IIK ZOUESYDKFWPCIQXHMVBLGNJRAT E IIIK EHRVXGAOBQUSIMZFLYNWKTPDJC N

Name Alphabet/Wiring Notch(es) I EKMFLGDQVZNTOWYHXUSPAIBRCJ Q II AJDKSIRUXBLHWTMCQGZNPYFVOE E III BDFHJLCPRTXVZNYEIWGAKMUSQO V IV ESOVPZJAYQUIRHXLNFTGKDCMWB J V VZBRGITYUPSDNHLXAWMJQOFECK Z VI JPGVOUMFYQBENHZRDKASXLICTW M,Z VII NZJHGRCXMYSWBOUFAIVLPEKQDT M,Z VIII FKQHTLXOCBJSPDZRAMEWNIUYGV M,Z BETA LEYJVCNIXWPBQMDRTAKZGFUHOS - GAMMA FSOKANUERHMBTIYCWLQPZXVGJD - IC EKMFLGDQVZNTOWYHXUSPAIBRCJ A,B,C,E,F,G,I,K,L,O,P,Q,S,U,V,W,Z IIC HQZGPJTMOBLNCIFDYAWVEUSRKX A,C,D,F,G,H,K,M,N,Q,S,T,V,Y,Z IIIC UQNTLSZFMREHDPXKIBVYGJCWOA A,E,F,H,K,M,N,R,U,W,X IR JGDQOXUSCAMIFRVTPNEWKBLZYH N IIR NTZPSFBOKMWRCJDIVLAEYUXHGQ E IIIR JVIUBHTCDYAKEQZPOSGXNRMWFL Y IK PEZUOHXSCVFMTBGLRINQJWAYDK Y IIK ZOUESYDKFWPCIQXHMVBLGNJRAT E IIIK EHRVXGAOBQUSIMZFLYNWKTPDJC N

## What is the reflector (Umkehrwalze)?

The Enigma reflector is a static component of the machine, located after the rotors (left). Its internal wiring achieves a reciprocal/symmetric permutation of the letters of the alphabet. Its role is to change the value of the letter and send the electric current back to the rotors for a second pass.

Example: The Cthin reflector has RDOBJNTKVEHMLFCWZAXGYIPSUQ wiring, so the letter A ( position 1 in the alphabet ) would be transformed into R (position 1 of the rotor) and reciprocally the letter R would be transformed into ' HAS'.

dCode accepts the following reflectors: Name Alphabet/Wiring A EJMZALYXVBWFCRQUONTSPIKHGD B YRUHQSLDPXNGOKMIEBFZCWVJAT C FVPJIAOYEDRZXWGCTKUQSBNMHL BTHIN ENKQAUYWJICOPBLMDXZVFTHRGS CTHIN RDOBJNTKVEHMLFCWZAXGYIPSUQ UKWR QYHOGNECVPUZTFDJAXWMKISRBL UKWK IMETCGFRAYSQBZXWLHKDVUPOJN

Name Alphabet/Wiring A EJMZALYXVBWFCRQUONTSPIKHGD B YRUHQSLDPXNGOKMIEBFZCWVJAT C FVPJIAOYEDRZXWGCTKUQSBNMHL BTHIN ENKQAUYWJICOPBLMDXZVFTHRGS CTHIN RDOBJNTKVEHMLFCWZAXGYIPSUQ UKWR QYHOGNECVPUZTFDJAXWMKISRBL UKWK IMETCGFRAYSQBZXWLHKDVUPOJN

## What is the position of the rings (Ringstellung)?

Wheel rings are adjustable elements located on the rotors. They made it possible to define an additional offset between the letters and their position on the rotor (the wheel is not fixed and can be offset relative to the rotor).

Example: 13-20-03 is a possible configuration for 3 rotors (from left to right). The numbers refer to those written on the rotors (numbered 01 to 26).

Sometimes the positions are noted in letters the equivalent is given by A=01, B=02, Z=26 ( A1Z26 coding).

## What is the rotor position (Grundstellung)?

The Grundstellung ( base position in German) refers to the initial configuration of the Enigma Machine's rotors before beginning to encrypt a message. The position is usually noted with a group of 3 letters. The letters refer to the position of the rotors (visible on top of the machine)

Example: EXS is a possible configuration for 3 rotors (from left to right E,X,S ).

When you change the key, the rightmost rotor turns one notch. A notch system makes it possible to drive the following rotors (like an odometer).

The Enigma machine had a particularity (anomaly?) for the rotation of the third rotor: double stepping. The central rotor thus rotates twice during the rotation of the left rotor, once before and once at the same time. The fourth rotor, when it exists, never turns.

## What is the plugboard (Steckverbindungen)?

The plugboard (or connection panel) is located at the front of the machine and is made up of sockets and cables. It allows you to reconfigure the connections between the letters of the alphabet.

The user could plug cables between the different sockets to swap correspondences between letters.

Example: By connecting the socket marked A to the one marked B , each time the machine encoded (or decoded) the letter A , it would be transformed into B and vice versa.

There are therefore a maximum of 13 possible connections (the 26 letters of the alphabet are grouped into 13 pairs).

## What are the different Enigma machines?

The first Enigma machines were sold by the Chiffriermaschinen Aktien-Gesellschaft company from 1923 in Germany.

The first commercial version included 3 disks named IC , IIC , and IIIC , they did not include a board or reflector and therefore had to switch from encryption mode to decryption mode.

In 1930, the German navy adopted the M3 version (known as Funkschlüssel) comprising a reflector (among B or C ) and a connection panel and 3 rotors among 5 available ( I , II , III , IV and V )

In 1938 and 1939, 3 new rotors were added to the M3 version ( VI , VII and VIII )

In 1942, the navy adopted a version M4 modified the M3 to replace the reflector with a 4th rotor (thinner) to choose from BETA or GAMMA and a reflector (thinner) to choose from 'BTHIN or CTHIN .

A Swiss version named K offered 3 rotors including IK , IIK , IIIK and a UKWK reflector

A Railway version named R offered 3 rotors including IR , IIR , IIIR and a UKWR reflector

## How to recognize Enigma ciphertext?

The encrypted message consists only of letters (the keyboard being limited to the 26 letters of the alphabet), no punctuation, no numbers, no symbols. Any numbers are written in letters.

A letter is never encoded with itself (no plain letter is identical to its cipher letter).

## Why can't a letter be coded by itself?

The crucial point that prevents a letter from being encrypted by itself is the reflector. The reflector connects pairs of electrical contacts, but never allows a contact to be connected to itself. So if a letter A is typed, the current will pass through the wiring board, rotors, arrive at the reflector and be sent back through the rotors and wiring board. But since the reflector cannot return the current to the same place from where it came, the letter A cannot be coded as A .

This feature of the Enigma was actually a weakness that was exploited by Allied cryptanalysts to help break the Enigma code. By knowing that a letter could not be encrypted by itself, and by knowing or assuming part of the known message, they could eliminate certain possibilities when trying to decrypt messages, reducing the number of configurations to test .

## How many possible combinations are there for Enigma?

It all depends on the machine used, but taking the general case at $ r $ rotors to choose from $ n $ rotor models and a wiring board with $ w $ wires.

— Walzenlage: The $ r $ rotors among $ n $ represent $ \binom{n}{r} = \frac{n!}{(n-r)!} $ combinations

— Ringstellung: The $ r $ rotors can be positioned independently in 26 positions, i.e. $ 26^r $ combinations

— Steckerverbindungen: The $ w $ wires connect $ 2w $ letters among the 26 of the alphabet, i.e. $ \frac{26!}{(26-2w)! \times 2^w \times w!} $ combinations .

Thus, the Enigma machine has $ \frac{n!}{(n-r)!} \times 26^r \times \frac{26!}{(26-2w)! \times 2^w \times w!} $ combinations .

Example: For the Enigma M3 machine (with $ r = 3 $, $ n = 5 $, $ w = 10 $), this represents $ 158962555217826360000 \approx 1.59 \cdot 10^{20} $ combinations .

## What are the changes following the dCode 2024 update?

The update of the Enigma simulator by dCode in 2024 corrected 3 elements:

— The order of the rotors, previously dCode recorded the rotors from right to left , now it is from left to right (same for positions and rings).

— The connection board only worked if there were no hyphens between pairs of letters.

— The double stepping anomaly sometimes created an inappropriate lag.

## When was Enigma invented?

Enigma was invented by the German Arthur Scherbius, taking over a patent from the Dutchman Hugo Koch, dating from 1919.
