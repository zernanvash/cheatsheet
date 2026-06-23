# CrackIt;) Writeup

Challenge_URL: https://crackmes.one/crackme/697e6957e04ca145cd9d13b4

# Writeup of crackit;)

Open the binary with hexdump in cli.

Found a section containing string:

hexdump -C crackit
[...]
00002090  00 43 54 46 7b 00 4d 79  5f 00 53 33 63 00 72 33  |.CTF{.My_.S3c.r3|
000020a0  74 5f 00 46 6c 34 67 00  7d 57 30 57 00 59 30 75  |t_.Fl4g.}W0W.Y0u|
000020b0  00 46 30 75 6e 64 00 4d  33 00 7b 30 72 20 00 4e  |.F0und.M3.{0r .N|
000020c0  30 74 7d 00 01 1b 03 3b  58 00 00 00 0a 00 00 00  |0t}....;X.......|
[...]

The flag appear.

run crackit binary with the flag:

./crackit "CTF{My_S3cr3t_Fl4g}W0WY0uF0undM3{0r N0t}"
You cracked me!

Thx for this crackme.
