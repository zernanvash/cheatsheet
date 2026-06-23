## Overview
When the executable is launched, it prompts the user for a password. Entering an incorrect password results in an error message and the application immediately terminates.
## Analysis

![Wrong Password]({34FBCD10-AA22-4107-9040-7FF8DD34C13C}.png)
The challenge description hints that the executable is a .NET application, making tools such as dnSpy ideal for analysis. Upon opening the binary in dnSpy abd navigating through the decompiled source, it becomes clear that the application simply compares the user's input against a hardcoded password. The relevant code can be inspected to recover the expected password without requiring any debugging or dynamic analysis.

![Code]({C394B256-3332-4BEF-9845-604504CF8CC3}.png)
## Solution
After identifying the hardcoded password in dnSpy, enter the password `TihiyOmut_Secret_2026` into the application when prompted. The program accepts the password and displays the success message shown below: 

![Correct Password]({72A4F8F6-CC6F-4A7F-8483-E9733015FEEF}.png)
## Conclusion
This crackme serves as a basic introduction to .NET reverse engineering. Because the binary is not obfuscated, the password can be recovered quickly through static analysis alone using dnSpy.