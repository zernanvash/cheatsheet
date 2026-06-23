Join my telegram channel - t.me/dimension59 for more reverse stuffs.
Write-up for 
-
Coder_90's Crack It!
-
Сollecting_initial_data() {

    Operation system: Windows(95)[I386, 32-bit, GUI]
    Compiler: Borland C++(Builder)[Enterprise]
    Linker: Turbo Linker(5.0)[GUI32]
    Total entropy level 6.61916

} 

Brief overview() {

The file is quite large, containing thousands of functions unrelated to cracking, 99% noise, and 1% crackme due to Borland C++ Builder.
The verification logic contains 129-bit RSA. Author likely intentionally chose 129-bit because it's the sweet spot for an interesting crackme. 
It can't be brute-forced, but it's weak enough for factorization by a modern processor.

}

Analyze() {
Main function starts at 9398 + base address
[maingraph.png]  
Looks big
[GetText.png]
the place where the key is collected

Let's scroll down the graph a little. We see three blocks where long, strange strings are loaded. This is the "heart" of the cracks.
First block [blockone.png]
Second block [secondblock.png]
Third block [thirdblock.png]

First one is Module N. Second one is standard RSA exponent. Third one is Ciphertext C

Look below, after loading all three numbers.
[PowModcall.png]
Address 0x40A9CB: Calling sub_402C4C(PowMod). Our numbers are transmitted into it.
[Check.png]

Address `0x40AA9C`: Branch (Rhombus on graph).

    Green arrow leads to a block with PlaySoundW ("SystemHand") and MessageBoxW ("Invalid Key"). This is the failure path.
    Red arrow leads to a block with MessageBoxW ("ACCESS GRANTED").

    Logic - 
        Input is taken.
        65537 is taken (E).
        2630492240428669223384232383096338562137 is taken (N).
        RSA encryption of the input.
        The result is compared with 1601640017009476007754247816372425531056 (C).

    To get "ACCESS GRANTED," we need to find an Input that, when raised to the power 65537 modulo N, yields C.


here is python script to calcule that input [solve.py]

The resulting number 89309538283792098316791637877157732692 was converted to HEX and then to text ASCII.
Flag: C0d3r_9O_Crack!T


}