# JustTry crackme Writeup

Challenge_URL: https://crackmes.one/crackme/69e8918b643676f8bb961dd5

JustTry.exe Solution Writeup

JustTry.exe is a small 32-bit Windows crackme with a dialog-based UI. The goal was to understand how the input is validated and then patch the binary so it always reaches the success path.

1. Initial triage

The first step was basic profiling of the file:

PE32 executable
x86 (Machine = 0x14C)
small size, about 18.5 KB
native code, not .NET
imports included DialogBoxParamA, GetWindowTextA, and MessageBoxA
That already suggested a classic Win32 dialog crackme: read text from edit controls, process it, and show a success or failure message.

2. Looking at strings

The most useful strings were:

"Congratulations, you found it!"
"Nope, that's not it!"
"VM initialization failed!"
The success string was especially helpful, because it gave us an anchor into the validation logic.

3. Opening it in IDA

Since this is a 32-bit binary, the correct debugger choice is x32dbg, not x64dbg.

In IDA, following the success string led straight into the dialog handler. The relevant logic was inside DialogFunc.

The important sequence was:

call GetDlgItem
call GetWindowTextA twice
call sub_401050 on the first input
convert 8 output bytes to hex using "%.2x"
compare the generated string with the second input
if equal: show "Congratulations, you found it!"
otherwise: show "Nope, that's not it!"
So the crackme uses two fields:

field 1 = name/input
field 2 = serial
4. Recovering the serial algorithm

The function sub_401050 computes 8 output bytes from the first input.

Inside that function, IDA showed two XMM constants loaded from .data, which correspond to the byte coefficients:

B5 BF C1 C5 C7 D3 DF E3

Then the loop performs, for each i from 0 to 7:

serial[i] = (coeff[i] * name[i % len(name)] * (i + 1)) & 0xFF;
After that, the 8 bytes are formatted as lowercase hex with "%.2x", producing a 16-character serial.

So the final serial is:

for (i = 0; i < 8; i++)
    out[i] = (coeff[i] * name[i % len(name)] * (i + 1)) & 0xFF;
serial = hex(out[0]) + ... + hex(out[7]);
For example, for the name test, the generated serial is:

04b61910dc7a3be0
5. Validation branch

The comparison result is normalized into EAX:

EAX = 0 on success
EAX = 1 on failure
Then the code does:

test eax, eax
jnz  short fail_branch
In the file, that conditional jump is located at offset 0x7A9 and originally contains:

75 3E
That is the jump to the failure path.

6. Patch

The minimal patch is to remove that jump:

original bytes at 0x7A9: 75 3E
patched bytes: 90 90
So the patched region becomes:

07A0: 05 1B C0 83 C8 01 53 85 C0 90 90 FF 15 80 30 40
With this change, execution always falls through into the success path and displays:

Congratulations, you found it!
7. Result

There are really two valid solution paths here:

Reverse the serial algorithm and generate correct serials.
Patch the conditional jump and force the success branch.
Both are straightforward once the dialog handler is identified.

Conclusion

This was a nice beginner-friendly Win32 crackme:

simple PE triage
useful strings
easy import clues
short validation routine
clean branch to patch
The main trick was recognizing that the program reads two edit controls, computes 8 bytes from the first one, turns them into a 16-character lowercase hex string, and compares the result against the second field.