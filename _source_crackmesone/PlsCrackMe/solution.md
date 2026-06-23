# PlsCrackMe Writeup

---------- INTRODUCTION ----------

When we open the program with IDA, we are directly greeted by the main function, and we see that a simple license check is being performed here.
Pseudocode View (F5):

int __fastcall main(int argc, const char **argv, const char **envp)
{
  char Str[13]; // [rsp+23h] [rbp-Dh] BYREF

  _main();
  _mingw_printf("Please enter the password : ");
  _mingw_scanf("%s", Str);
  while ( !Checker(Str) )
  {
    if ( strlen(Str) > 0xD )
      puts_0("Way 2 Big!");
    _mingw_printf("Please Try again : ");
    _mingw_scanf("%s", Str);
  }
  puts_0("Good job, You Really Cracked it!");
  Sleep(0x3E8u);
  return 0;
}

Here we see that our input is checked by the Checker function. 
As long as our password is not correct, it allows us to make attempts in an infinite loop; 
if our password is longer than 0xD in hexadecimal (13 in decimal), it gives an error, 
from which we understand that the password must be 13 characters long.

---------- Checker Analysis ----------

At the bottom, we see the boolean value returned by the function: return v8 == 3 && v7 == 3 && v6 == 3 && v5 == 4;

v8 == 3
v7 == 3
v6 == 3
v5 == 4

All of them must be satisfied at the same time; at the beginning of the function these variables are set to 0.
Adding them together and seeing that the result is 13 also allows us to understand once again how many characters the password should be.

Now we can start analyzing this function with pseudocode view:

The initial for-loop iterates over each character of the string.
The character being processed is copied into v2:

  v3 = strlen(a1);
  for ( i = 0; i < v3; ++i )
  {
    v2 = a1[i];

First, it is checked whether the character is less than or equal to 47 or greater than 57.

  if ( v2 <= 47 || v2 > 57 )

In ASCII, the range between these two numbers corresponds to digits (0–9), so here it is checking whether the character is a digit.
If this is true, v8 is incremented and the loop returns to the beginning; otherwise, the loop proceeds to the following check:

  if ( (v2 <= 32 || v2 > 47) && (v2 <= 57 || v2 > 64) && (v2 <= 90 || v2 > 96) && (v2 <= 122 || a1[i] == 127) )

The ASCII range between 33 and 47:
! " # $ % & ' ( ) * + , - . /
So here it checks that the character is not one of these symbols.
Let’s call this chars1.

The ASCII range between 58 and 64:
: ; < = > ? @
Here it is also checking that the character is not one of these symbols; let’s call this chars2.

The ASCII range between 91 and 96:
`[ \ ] ^ _ ``
This checks that the character is not one of these either; let’s call this chars3.

The ASCII range between 122 and 126:
{ | } ~
Here, all printable characters except these symbols and DEL (a non-printable special character) are accepted.
Let’s call this chars4.

The simplified form of the condition is: if (chars1 && chars2 && chars3 && chars4)
In short, this checks whether the character is a special symbol; if it is not, the loop continues, and if it is, v7 is incremented:
  ...
  else {
    ++v7;
Now we continue analyze the loop from where we left off.

  if ( v2 <= 64 || v2 > 91 )

The ASCII range between 65 and 91 covers all uppercase letters (A–Z), so here it checks whether the character is an uppercase letter.
If it is an uppercase letter, the condition fails and v6 is incremented; otherwise, it proceeds to the next check:
  ...
  else {
    ++v6;

The other and final condition:

  if ( v2 > 96 && v2 <= 122 )
    ++v5;

The ASCII range between 97 and 122 covers all lowercase letters (a–z); if the character is a lowercase letter, v5 is incremented.

---------- Solution ----------

Now we know according to what our control variables are incremented:
v5 = lowercase letters | v6 = uppercase letters | v7 = special symbols | v8 = digits
Therefore, the password expected by the program is as follows:

4 lowercase letters + 3 uppercase letters + 3 symbols + 3 digits.

Now we can generate and test various passwords to see whether we have correctly solved the algorithm:

Please enter the password : aaaaAAA+++999
Good job, You Really Cracked it!

Please enter the password : a0+7bfxY[Z]P6
Good job, You Really Cracked it!







  











