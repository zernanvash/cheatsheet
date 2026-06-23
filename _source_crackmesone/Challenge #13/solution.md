# Challenge #13 Writeup

the prompt string is referenced from fcn.1400caec0, which is the main challenge function

...
0x1400caf32      call fcn.140001920
0x1400caf3d      call fcn.140001570
0x1400caf47      cmp  r8, qword [var_48h]
0x1400caf4c      je   0x1400cafac
...
0x1400caf5e      lea  rcx, str.Wrong__n
0x1400caf65      call fcn.14000ff30
...
0x1400cafbb      call sub.api_ms_win_crt_private_l1_1_0.dll_memcmp
0x1400cafc2      jne  0x1400caf4e
...
0x1400cafe0      lea  rdx, str.Correct_Flag_
0x1400cafe7      call qword [sym.imp.USER32.dll_MessageBoxW]

- build reference buffer with fcn.140001920
- transform user input with fcn.140001570
- compare length
- compare bytes with memcmp
- print Wrong! on mismatch
- show Correct Flag! on success



fcn.140001640 (anti-debug ) is called while building the reference buffer


0x14000164e      call rbx        ; IsDebuggerPresent
0x140001652      jne  0x1400016a4
...
0x140001669      call rsi        ; CheckRemoteDebuggerPresent
0x14000166d      jne  0x1400016b8



fcn.140001570 walks the input string and calls fcn.1400014b0 for every byte after subtracting 0x30

0x1400015b0      lea  edx, [rax - 0x30]
0x1400015b9      call fcn.1400014b0


fcn.1400014b0 converts an integer into ascii bits in lsb-first order

0x1400014e0      mov  byte [rax + r12], bpl
0x1400014e7      sar  esi, 1
...
0x140001501      and  ebp, 1
0x140001504      add  ebp, 0x30

so for user input
- take one character c
- compute ord(c) - 0x30
- write its binary digits as '0' and '1'
- least significant bit first

example
- '6' --> 0x36 - 0x30 = 6
- 6 in binary is 110
- lsb-first ascii bits --> 011



fcn.140001920 (reference buffer transform) builds three weird overlapped strings, then runs each one through another transform

first chunk setup
0x140001971      movabs rdx, 0x6161686164626161   ; 'aabdahaa'
0x14000197e      movabs rax, 0x6261626464646161   ; 'aadddbab'
0x140001995      movabs rdx, 0x61616261616461     ; 'adaabaa'
0x1400019a4      movabs rax, 0x6164616461616861   ; 'ahaadada'

the writes overlap on purpose, so you cannot just read the immediates in order and be done

after reconstructing the actual in-memory bytes, the three chunks are
- aadddbabaabdahaahaadadaadaabaa
- ddddddgudggdaddddaddddgdddggdd
- fffeecfcfeffffoffoffcfcffcffefc

then fcn.1400016c0 transforms each chunk
0x1400016d7      lea  edi, [r8 + 0xc]
...
0x140001710      movzx edx, al
0x140001716      xor  edx, edi
0x140001718      call fcn.1400014b0

- take one chunk byte b
- xor it with seed + 0x0c
- convert the result to lsb-first ascii bits

the seeds used by fcn.140001920 are
- first chunk --> 0x54
- second chunk --> 0x59
- third chunk --> 0x5b

this produces one long bitstring
that final bitstring is what gets compared against the transformed user input

recovering the flag - invert the user-side transform against the final reference bitstring

the user encoding is not prefix-free
different printable strings can map to the same final bitstream if you split the bits differently

but we know that the flag format is CTF{...}

inversion:
1. reconstruct the 3 overlapped literal chunks exactly as they exist in memory
2. rebuild the final reference bitstream with the same xor + lsb-first logic
3. anchor the parse with CTF{ and }
4. consume the middle by taking the longest reasonable printable match

CTF{aaILLn_Jlike_b4maaIL41}

