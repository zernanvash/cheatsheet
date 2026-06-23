# c Writeup

Torontos's c

Tools:
OS: Arch Linux
Kernel Linux 6.18.9-arch1-2
Terminal: kitty 0.45.0
Dissasember: Ghidra

Dissasembed using standard options.

So first thing that i found myself in is what decoded as FUN_001010c0(void)

PTR_s_5368616b652069742c206261627921_00104118

Ghidra names pointers using hex
s_ hex _ addr in this format:
so taking that and decoding it
5368616b652069742c206261627921

becomes

Shake it, baby!

Happy Cracking,

Tballer801
