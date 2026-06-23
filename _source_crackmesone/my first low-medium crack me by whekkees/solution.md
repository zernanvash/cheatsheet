# my first low-medium crack me by whekkees Writeup

---------------------
1 - Overview
---------------------
First, to do static analysis, we open our program in IDA. When we reach the main function,
we press the F5 key to open the pseudocode view.

The texts found in the program:

"Hello my friend its my two crack me"
"Please enter ur login"

If our login is correct:
"Please enter ur password"
If entered wrong:
"bad"
If entered correctly:
"good"

---------------------
2- Anti-Debug Checks
---------------------
At the beginning of the program, there are two anti-debug checks:

if ( IsDebuggerPresent()
  || (pbDebuggerPresent[0] = 0,
      CurrentProcess = GetCurrentProcess(),
      CheckRemoteDebuggerPresent(CurrentProcess, pbDebuggerPresent),
      pbDebuggerPresent[0]) )
{
  exit(0);
}

If a debugger is detected, it calls exit to close the program, but we won’t be affected by these because we are doing static analysis.
---------------------
3- Login Check
---------------------

The login check is done in this code:

qmemcpy(pbDebuggerPresent, "&06'0!", 6);

The program checks each character entered by the user like this:

(input_char ^ 0x55) == expected_char

So, the actual input value can be found using this formula:

----------------------------------
3.5- How does XOR encryption work?
----------------------------------

Exclusive OR is a bit operation where the result is 1 if the two bits are different, and 0 if they are the same.

A	B    A XOR B
0	0	0
0	1	1
1	0	1
1	1	0

An important feature of XOR is that if you apply XOR with the same value again, the data returns to its original form.

A ^ B ^ B = A

For this reason, the same operation is used for both encryption and decryption.

Now, using this information, let’s find the correct password.

Expected value: &06'0! 
When we apply the XOR operation with 0x55, we get: secret
So we have found the correct login.

---------------------
4- Password Check
---------------------
When we enter the login correctly, the program also asks us for a password.

qmemcpy(pbDebuggerPresent, "71='9?", 6);

And the password is expected in a value XORed with 0x55; we apply the same method we learned:

Expected value: 71='9?
When we apply XOR with 0x55, we get: bdhrlj

This gives us the correct password.

---------------------
5- Solution
---------------------
Now let's test our login and password without running any debugger.
(Because the program does not use _getch, it closes after entering the input. Run it from cmd to see the result.)

C:\Users\...\Desktop>crackme2.exe
Hello my friend its my two crack me
Please enter ur login
secret
Please enter ur password
bdhrlj
good











