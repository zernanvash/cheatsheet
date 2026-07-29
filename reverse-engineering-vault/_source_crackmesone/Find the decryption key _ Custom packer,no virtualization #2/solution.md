# Find the decryption key | Custom packer,no virtualization #2 Writeup

Challenge_URL: https://crackmes.one/crackme/6a00b3533fba64e45dceaa2d

Password:
x9K!7zPq4mNvR2bL

Flag:
FLAG{p3Wq8RnZmK4vYxT7Bc2J}


Step by step

1. First run

The program prints:

=== elevenpack crackme ===
Enter password:

With a wrong password, it prints:

[-] wrong password


2. Packer check

The binary is packed with ElevenPack. In x64dbg, the original entry point
starts inside the packer stub, not inside the real crackme code.

Debugging it directly also triggers anti-debug behavior, so instead of
fighting the protector at the entry point, I let the program unpack itself
normally.


3. Dumping the unpacked process

I executed the program normally and left it waiting at the password prompt.
At that point, the real code and data had already been unpacked in memory.

Then I dumped the process memory and searched for useful strings.

The unpacked strings included:

=== elevenpack crackme ===
Enter password:
[-] no input
[-] empty input
[+] %.*s
[-] internal: flag sentinel mismatch
[-] wrong password

This confirmed that the real crackme data was available in memory.


4. Finding the important data

Near the strings there was a data block containing:

- an encrypted flag blob
- data used to derive the expected password
- a visible sentinel:

11 22 33 44 55 66 77 88 99 AA BB CC

The sentinel was useful because the program checks it after decrypting the
flag.


5. Rebuilding the protected code

ElevenPack kept the real code in protected encrypted pages.

The loader had metadata for 23 pages. Each entry contained:

- the final page address
- the encrypted page address
- a 16-byte page key
- a page index

The page decrypt routine did this:

1. scramble the 16-byte key with a global seed
2. use the result as an RC4 key
3. decrypt the page back into the real image

I reproduced this logic in a script and rebuilt the real .text section.


6. Analyzing the password check

After rebuilding the real code, the main password routine was clear.

The routine:

1. reads the input
2. strips newline characters
3. requires exactly 16 bytes
4. generates the expected password using a ChaCha20 block and XOR
5. compares the generated value with the user input

The calculated password was:

x9K!7zPq4mNvR2bL


7. Decrypting the flag

After the password check passes, the same password is used as the RC4 key
to decrypt the encrypted flag blob.

The decrypted flag is:

FLAG{p3Wq8RnZmK4vYxT7Bc2J}


8. Final test

Input:

x9K!7zPq4mNvR2bL

Output:

=== elevenpack crackme ===
Enter password: [+] FLAG{p3Wq8RnZmK4vYxT7Bc2J}


Conclusion

The crackme was protected with ElevenPack. The solution was to dump the
process after unpacking, rebuild the encrypted code pages, analyze the real
password check, calculate the expected 16-byte password, and use it to
decrypt the flag.

Final password:
x9K!7zPq4mNvR2bL

Final flag:
FLAG{p3Wq8RnZmK4vYxT7Bc2J}
