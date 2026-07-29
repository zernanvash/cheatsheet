# Fixed Easy Crackme Writeup

Challenge_URL: https://crackmes.one/crackme/698d2206e2ba6023bfacaa4f

Writeup: Kanax01's Fixed Easy Crackme
Author: Lazex

Challenge Date: 2026-02-13

Difficulty: 1.0 (Easy)

Platform: Windows x86-64

1. Challenge Overview
This challenge is a basic Windows binary written in C/C++. According to the author, it is a beginner-level "crackme" designed to test fundamental reverse engineering skills. The objective is to identify the correct password required to trigger the "Success" code path.

2. Static Analysis (IDA Free)
Upon loading the binary into IDA, I analyzed the main function. The program logic is straightforward, consisting of four primary functional blocks:

Input Collection: The binary prompts the user for string input.

Length Validation: The input length is calculated and compared against a constant.

String Comparison: The input is compared against a hardcoded value stored in memory.

Branching: The program prints a "Success" or "Failure" message based on the comparison result.

The Length Check
The first validation step involves a length check. In the disassembly, the input length is compared to 0x0C (12 in decimal).

Note: If the user input does not consist of exactly 12 characters, the program immediately branches to the "Failed" block.

The Comparison Logic (memcmp)
The core validation is handled by a memcmp function. By inspecting the function arguments, I observed that it compares the user input to a data structure labeled "Block".

By performing a Cross-Reference (XREF) on the "Block" address, the hardcoded password was clearly visible in the data section.

3. The Solution
The program performs a direct memory comparison between the user's 12-character input and the following string:

Password: EasyPassword

String: EasyPassword

Hex Length: 0x0C (12 characters), which satisfies the initial length requirement.

4. Conclusion
Analysis in IDA reveals that the binary employs no encryption, obfuscation, or packing. The password validation relies on a simple plaintext comparison, making it a perfect introductory challenge for static analysis.

Final Password: EasyPassword