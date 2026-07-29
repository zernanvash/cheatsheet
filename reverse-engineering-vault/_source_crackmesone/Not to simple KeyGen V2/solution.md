# Not to simple KeyGen V2 Writeup

Challenge_URL: https://crackmes.one/crackme/69a1f44218b5d7ee4709351d

i traced input handling and then focused on the branch near the end of main

0x401996  cmp rax, 0x10
0x40199a  jne 0x401a08

this forces serial length = 16

after that, the loop starts around 0x4019ab and iterates with i = 0, 3, 6, 9, 12, 15


important branch
0x4019f2  cmp r11d, esi
0x4019f5  je 0x401aa4

targets
- 0x401a08 <-- failure path
- 0x401aa4 <-- success path

inside each loop step, two checks exist:

1) first relation on serial bytes only:
   s[(i+1)%17] + s[i] == (s[(i+2)%17] << 3)

2) only if check 1 is false, it compares:
   s[(i+3)%17] == (h[i] << 2)

if check 2 is true, code jumps directly to 0x401aa4 (success)

the logic is weak because success depends on hitting one specific equality, not on passing a strict full validation of all positions



the custom hash routine is at 0x401d80

main calls it three times
- h_name  = hash401d80(name)
- h_email = hash401d80(email)
- h_mix   = hash401d80(h_name || h_email)

validation uses bytes from h_mix (for example h[i] for i in 0,3,6,9,12,15)

for some name/email pairs, no valid serial exists because compared serial byte is signed (-128..127), while (h[i] << 2) can be outside this range
if all six candidate positions are out of range, the pair is unsat




keygen emulates 0x401d80 with unicorn, h_mix, then builds a 16-byte serial

- choose i in {0,3,6,9,12,15} with reachable target t = int8(h[i]) * 4
- set serial[(i+3)%17] = t
- force check 1 to be false for that i
- keep serial length 16 and avoid 0x00/0x0a in payload bytes

---------


Hello! Welcome to Howo's not to simple Keygen CTF!


Welcome back to the NTSK Hotel!

Please insert your full name: djd
Please insert your best email: djd@email.gov
Please insert your serial: AAAAAAdAAAAAAAAA
Very nice work man!!!
Get your flag: CTF{Giant-binary!=Secure-binary---Look-to-validation-and-boom}
