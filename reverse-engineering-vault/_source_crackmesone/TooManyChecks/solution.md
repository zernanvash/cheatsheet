# TooManyChecks Writeup

Challenge_URL: https://crackmes.one/crackme/69761202511e37b6d1f8ed43

From sub_140008090, the flag is constructed by taking characters from:

a1 + 280 (1 char, index 0)
a1 + 568 (1 char, index 0)
a1 + 184 (2 chars, index 0-1)
a1 + 344 (8 chars, index 0-7)
a1 + 408 (2 chars, index 0-1)
a1 + 472 (5 chars, index 0-4)

The structure at a1 contains vectors starting at offset 152 (from sub_1400038C0). Each vector entry is 32 bytes apart.
Let me calculate which string index each offset refers to:

184 = 152 + 32*1 = index 1 → "ag"
280 = 152 + 32*4 = index 4 → "Fdez"
344 = 152 + 32*6 = index 6 → "(ByP@$$_"
408 = 152 + 32*8 = index 8 → "a_)"
472 = 152 + 32*10 = index 10 → "B0$$)"
568 = 152 + 32*13 = index 13 → "l&"

So the flag construction is:

1 char from "Fdez" [0] = 'F'
1 char from "l&" [0] = 'l'
2 chars from "ag" [0-1] = 'ag'
8 chars from "(ByP@$$" [0-7] = '(ByP@$$'
2 chars from "a_)" [0-1] = 'a_'
5 chars from "B0$$)" [0-4] = 'B0$$)'

Flag: Flag(ByP@$$_a_B0$$)