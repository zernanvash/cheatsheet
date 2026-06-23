# SelfKey Writeup

Step-by-step write-up

1) What the program does
- It prompts for a password and prints "Correct" or "Wrong."
- Input is normalized by removing spaces and dashes, so AB-CD equals ABCD.
- There are anti-debug, timing, and self-integrity checks before the password check.

2) Where the expected key comes from
- The function expectedForExe() computes the key.
- It takes the running exe’s file name (without extension), lowercases it, and hashes it.
- The result is encoded with a Base32-like alphabet and a 2-char checksum suffix.
- Therefore, the key depends on the exe name, not on the machine.

3) Input normalization
- Spaces and '-' are removed before comparison.
- Case is not normalized, so you must enter the exact characters.

4) Anti-debug / timing checks
- IsDebuggerPresent and CheckRemoteDebuggerPresent cause an early exit if a debugger is attached.
- A small timing loop exits if execution is "too slow."
- If you’re debugging, these can trigger early termination.

5) Actual verification flow
- expectedForExe(argv[0]) generates the expected key.
- User input is normalized.
- A constant-time comparison decides correct/incorrect.

6) Important detail: undefined behavior
- The key generator shifts a uint32_t by (i*3), which can exceed 31.
- That is undefined behavior in C++, so the generated key can vary by compiler.
- MSVC behavior (likely for the provided exe) yields a different key than some other compilers.

7) Correct key for crackme.exe
- With MSVC-style behavior, the correct key is:
  CWYZDVYNGWLKL2X8WKFAQQ

8) How to test
- Run from PowerShell:
  .\crackme.exe
- Enter:
  CWYZDVYNGWLKL2X8WKFAQQ
