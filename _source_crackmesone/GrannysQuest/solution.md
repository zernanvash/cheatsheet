# GrannysQuest Writeup

Challenge_URL: https://crackmes.one/crackme/699661243a36b6fb91ee893e

GRANNY'S QUEST — CRACKME WRITEUP BY KANKER1337
=================================

Day 1 asked for granny's birthday in ddmmyyyy format.
The validation function at RVA 0x2360 checks that the input is exactly 8 digits,
sums up their ASCII codes, XORs the result with 0x29A, rotates it left by 4 bits,
and multiplies by 5. I needed this to equal a specific target derived from the global variable.
After working out the math the target came out to 62240, and working backwards
I found the digit sum needed to be 16. 00700900 does the job.

    Calculation ( n = 122*2 = 244, 0x49 = 73 ):

        ((244^2 + 11^2) * 2026 - 120739968) / 2 - (244 + 73)
        = ((59536 + 121) * 2026 - 120739968) / 2 - 317
        = 125114 / 2 - 317
        = 62240

        5 * ROL4(digit_ascii_sum ^ 0x29A, 4) = 62240
        ROL4(digit_ascii_sum ^ 0x29A, 4) = 12448 (0x30A0)
        ROR4(0x000030A0, 4) = 0x0000030A = 778
        digit_ascii_sum ^ 0x29A = 778
        digit_ascii_sum = 778 ^ 666 = 400

        400 - 8 * 48 = 16  ->  digit sum = 16  ->  input: 00700900


--


Day 2 was simpler.
The program holds an encoded string "Dlyyov#Dsvvoh#Fmornrgvw" at RVA 0xC248,
initialized at startup in RVA 0x1000. The check at RVA 0x2490 applies Atbash cipher
to that string and compares it against the input. I set a breakpoint at RVA 0x24B7
in x64dbg to confirm the string, then just decoded it.

    Answer: Wobble-Wheels-Unlimited


--


Day 3 took a bit of back and forth.
The program asks for your name first, then a number code.
The function at RVA 0x2600 is recursive Fibonacci. For each letter of the name
it computes fib(letter - 'a') and concatenates the results into a string.
After a few wrong guesses about the accumulation logic I confirmed dynamically
that it's just a straight concatenation - no accumulation.

    Example for "Kanker":

        k -> fib(10) = 55
        a -> fib(0)  = 0
        n -> fib(13) = 233
        k -> fib(10) = 55
        e -> fib(4)  = 3
        r -> fib(17) = 1597

        Code: 5502335531597


--


Day 4 had three separate inputs: a launch code, coordinates, and a verification number.

The launch code validation at RVA 0x32C0 checks that the format is NNN-NNNNN-NNN
and that the ASCII sum of each numeric segment is divisible by 7.
Not the digit values — the ASCII codes. That tripped me up at first
since I assumed it was just a number divisibility check.

    003-00005-003:

        "003"   -> 48+48+51 = 147,  147 % 7 = 0  ok
        "00005" -> 48*4+53  = 245,  245 % 7 = 0  ok
        "003"   -> 48+48+51 = 147,  147 % 7 = 0  ok


The coordinates check at RVA 0x2F20 enforces the format XX.XXXX,XX.XXXX
with dots at positions 2 and 10, comma at position 7.
The actual coordinate values are computed at RVA 0x2820. That function looks
intimidating with all its trig and hashing, but after reading it carefully
I noticed all the intermediate calculations cancel out — v33 minus v33 is zero,
v16 minus v17 is zero, same with v19/v20 and a3/a3. The return value is just
the constant v34.

    a3 == 1  ->  40.8214  (latitude)
    a3 == 2  ->  14.4262  (longitude)

    Answer: 40.8214,14.4262


The verification number was the trickiest part.
The formula at RVA 0x34A0 hashes the launch code, multiplies by name length,
adds the XOR of the two coordinate doubles, normalizes the result,
then XORs with 0x309 times name length. My keygen implementation of the hash
kept hanging due to an infinite loop in the normalization. I set a breakpoint
at RVA 0x3638, right after the imul instruction, and read RAX directly.
It was 0x1236 for "Kanker", which means v7 — the value before the final XOR —
is always 0x8000000000000000. That's what the double XOR of 40.8214 and 14.4262
produces. So the verification number simplifies to:

    v8 = (0x309 * len(name)) ^ 0x8000000000000000
    interpreted as signed int64

    For "Kanker" (6 letters):  (0x309 * 6) ^ 0x8000000000000000 = -9223372036854771146