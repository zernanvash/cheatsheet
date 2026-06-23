# Monsignors Crackme Writeup

I approached solving the crackme using the following steps:

1. I first downloaded, extracted and ran the crackme (hello.exe); it prompted for a password and I entered one, 'hello', it prompted 'access denied'.
2. I opened Ghidra and loaded the executable into my project folder using the code browser tool.
3. Once the executable was loaded into the code browser tool, I then checked the .text section to see if I could find the main execution function (as per my knowledge on how C programs are compiled)
4. I managed to find the main function, and as per my initial guess, the argument passed from the command line was being compared against a raw string value ('secret') using the strcmp function from the string library in C.
5. I then ran the executable and entered the hardcoded passphrase 'secret', and the program printed 'access granted' via the command line.