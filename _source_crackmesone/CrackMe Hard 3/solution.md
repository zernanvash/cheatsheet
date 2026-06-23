# CrackMe Hard 3 Writeup

Main is located at 140003f90.
After decrypting some strings and printing them to the console it gets user input and runs the important functions:
- 140002f00. Checks if process is debugged and returns true if so
- 140003e9. Computes a checksum of the whole .text section to check for patches/breakpoints
- 140002960. Verifies that the input is of the correct format. from reversing this function it's easy to see that the format is VHARD{x}, where x is a 17 character long string composed of only capital letters, digits, and dashes.
- 1400033c0. Complicated function which returns true if the input matches the correct flag we are looking for. We will come back to this function.
- 140002d80. Computes a hash of the input string, which is later compared to the correct hash. this is an extra redundency check and the correct hash doesn't really help to recover the flag.

1400033c0 keeps a pretty complicated state and runs a loop where it calculates some checksum/hash on the current state and does a switch statement to either calculate some other stuff, return from the function, or, importantly, get the next character of the input (see 1400037af-1400037c4). Since the loop is a while(true) with return logic based on the current state, and the input characters are loaded one by one, my hope was that the number of iterations the loop does before returning is based on how many correct characters there are in the input, creating an oracle. That was indeed in the case.

The unicorn script bruteforces a single character of the input at a time, seeing whichever one increases the number of iterations of the loop, and proceeds onto the next one (see emulate.py).

The script finds VHARD{VMX-T1M3-L0CK-9F2}, which produces "ACCESS GRANTED" when inputted into the program.