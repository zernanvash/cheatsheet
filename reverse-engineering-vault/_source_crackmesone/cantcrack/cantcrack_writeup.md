# CantCrack.exe

Challenge_URL: https://crackmes.one/crackme/6a30eab0a4b247348ae805c4

loaded it in ida. checked strings first cause thats always the easiest way. found the success and fail messages.

followed the xref from congratulations to the main function. decompiled it. pretty straightforward.

main func does this:
- copies "YYXVRsqswKSP" to a buffer
- reads your input
- calls another func to compare them
- prints win or lose based on result

the compare func is where all the meat is.

first it checks:
- input has to be 14 chars
- position 5 has to be '-'
- position 10 has to be '-'

so its XXXXX-XXXX-XXX format.

then it splits the hardcoded string into 3 parts and xors them with different keys, then compares each part to the input segments.

part 1 (first 5 chars):
take "YYXVR" xor with 0x37
- Y ^ 0x37 = n
- Y ^ 0x37 = n
- X ^ 0x37 = o
- V ^ 0x37 = a
- R ^ 0x37 = e
so "nnoae"

part 2 (next 4 chars, between the dashes):
take "sqsw" xor with 0x41
- s ^ 0x41 = 2
- q ^ 0x41 = 0
- s ^ 0x41 = 2
- w ^ 0x41 = 6
so "2026"

part 3 (last 3 chars):
take "KSP" xor with 0x23
- K ^ 0x23 = h
- S ^ 0x23 = p
- P ^ 0x23 = s
so "hps"

put it all together with dashes:
nnoae-2026-hps

thats it. ran it and it works.
