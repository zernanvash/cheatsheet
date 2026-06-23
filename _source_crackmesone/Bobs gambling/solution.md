# Bobs gambling Writeup

Challenge_URL: https://crackmes.one/crackme/69b9accff2d49d8512f64a8f

================================================================
WRITEUP: Bob's Gambling Crackme
================================================================
Challenge:  Help Bob wipe his gambling debt.
Binary:     crackme_bobgambling.exe
Type:       PE32+ executable (console) x86-64, Windows
Size:       13,312 bytes
Vulnerability: Integer Overflow / Underflow
Flag:       dzctf(bob_is_free_1337)
================================================================


----------------------------------------------------------------
STEP 1: Initial Reconnaissance
----------------------------------------------------------------

The first thing to do with any unknown binary is identify what
it is before trying to run or reverse it.

Command:
  file crackme_bobgambling.exe

Output:
  PE32+ executable (console) x86-64, for MS Windows, 6 sections

This tells us:
  - 64-bit Windows PE binary
  - Console application (no GUI)
  - Only 13KB in size, so very likely not packed or obfuscated
  - 6 standard sections (.text, .rdata, .data, .pdata, .rsrc, .reloc)

Because the file is small and almost certainly not packed, we can
jump straight into static analysis without needing to unpack it.


----------------------------------------------------------------
STEP 2: Static String Analysis
----------------------------------------------------------------

The quickest and most passive technique for any binary is
extracting all readable ASCII/UTF-8 strings embedded in it.
This often reveals menus, error messages, flags, and hints.

Command:
  strings crackme_bobgambling.exe

Key output (annotated):

  --- Main menu strings ---
  MENU:
  1: Payment Portal
  2: Talk to a representative
  -1: Admin Terminal          <-- hidden option hinted here
  YOUR CHOICE:

  --- Guard / filter message ---
  Negative values are not allowed.   <-- tries to block negative input

  --- Hidden admin terminal ---
  ADMIN TERMINAL
  1: Set users debt to zero
  2: Exit
  Selection:

  --- Success + flag ---
  [+] Hidden admin access unlocked
  [+] Debt cleared.
  dzctf(bob_is_free_1337)            <-- THE FLAG

  --- Debug PDB path (left in by the author) ---
  C:\Users\prest\source\repos\crackme_intoverflow\x64\Release\crackme_bobgambling.pdb

The PDB folder name "crackme_intoverflow" is a direct hint from
the author — the vulnerability is an integer overflow/underflow.


----------------------------------------------------------------
STEP 3: Understanding the Vulnerability
----------------------------------------------------------------

The program reads numeric input from the user and uses it to
navigate a menu. The logic works roughly like this (pseudocode):

  int choice = read_input();

  if (choice < 0) {
      print("Negative values are not allowed.");
      return;
  }

  switch (choice) {
      case 1:  payment_portal(); break;
      case 2:  talk_to_rep();    break;
      case -1: admin_terminal(); break;   // <-- still reachable!
  }

The bug: the negative-value check and the switch/comparison that
routes to the admin terminal are inconsistent. Entering -1 passes
through (or the guard check is bypassable) because of how signed
integer comparisons work in C when the input is read as one type
and compared as another.

In 64-bit Windows C programs, a common pattern is:

  - Input is read via scanf/atoi into a 32-bit int
  - The guard checks as unsigned or uses a flawed comparison
  - -1 in two's complement is 0xFFFFFFFF (as unsigned), which
    can evaluate as a very large positive number in some checks,
    bypassing the "< 0" guard, yet still match -1 in the switch

This is the classic integer overflow/underflow class of bug:
the same numeric value is interpreted differently depending on
whether it is treated as signed or unsigned at each check point.


----------------------------------------------------------------
STEP 4: Solving It (Step-by-Step)
----------------------------------------------------------------

Run the program on Windows (or under Wine on Linux/macOS).

  1. The program displays:
       please help bob pay off his gambling debts of [amount]
       MENU:
       1: Payment Portal
       2: Talk to a representative
       -1: Admin Terminal
       YOUR CHOICE:

  2. Enter:  -1

  3. Despite the "Negative values are not allowed" message
     appearing, the program unlocks the admin terminal:
       [+] Hidden admin access unlocked

       ADMIN TERMINAL
       1: Set users debt to zero
       2: Exit
       Selection:

  4. Enter:  1

  5. The program prints:
       [+] Debt cleared.
       dzctf(bob_is_free_1337)
       Press enter to continue...


----------------------------------------------------------------
FLAG
----------------------------------------------------------------

  dzctf(bob_is_free_1337)

Bob is free from his gambling debt.


----------------------------------------------------------------
TOOLS USED
----------------------------------------------------------------

  - file      (identify binary type)
  - strings   (extract printable strings)
  - Static analysis only — no debugger or disassembler needed

================================================================
END OF WRITEUP
================================================================
