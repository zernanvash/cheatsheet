# MCM 6.0 - Project Mayhem Writeup

Challenge_URL: https://crackmes.one/crackme/69a95101fbfe0ef21de94652

Having analyzed and fully restored the algorithm, I realized that calculating the key mathematically is impossible.
(You can examine the key verification algorithm in detail within my brute-force or program patching scripts.)

Schematically (with many simplifications), the algorithm looks as follows:

0. First, the image is unpacked, projected into memory, followed by a jump to OEP, process creation under a debugger, etc.
1. Applying a mask to the key.
2. Generating a SHA256 hash chain from the masked key (using the "MCM6_LWE_V2" salt).
3. The resulting hash chain, treated as a vector, is multiplied by a pre-generated 0x200×0x200 matrix (DMP_in_00007FF72A872516_addr_RBP(BUF_100000h).bin).
4. The resulting vector is subtracted from a 0x200-element vector hardcoded in the program. 4-byte matrix calculations are reduced to a vector with 1-byte elements, resulting in a 0x200-byte buffer.   #buf_0x200 = (numpy_vec_0x800_7FF72A8B4CA0 - numpy.dot(numpy_matrix_from_buf100000, DRBG_Sub_7FF72A872170(key_attempt))).tobytes()
5. The 0x200-byte buffer is used as a base for generating bytecode for the RISC emulator. Also, an fnv1a_32 checksum is taken from the buffer.
6. The emulator output, the checksum, and a set of constants are used to create a XOR mask.  #v39 = (((((fnv_hash_fast.fnv1a_32(buf0x200) ^ emulated)* 0x9E3779B9)%(2**32))^ 0x31415926)+ 0x27182818)% (2**32) 
7. The resulting XOR mask, together with the hardcoded gamma (Unk_7FF72A8B54B0__HARDCODED_ORIG), is applied to the first 0x40 bytes of the 0x200 buffer.
8. If the fnv1a_32 checksum of the resulting 0x40 bytes equals 0x8EDA89A9, this 0x40-byte buffer is interpreted as the crackme success message and displayed in green.

=================
I am certainly no great expert in cryptography or mathematical statistics, but I was guided by the following reasoning. 
Since sha256 is used at the very beginning of the algorithm, it is not possible to precisely recover the original key corresponding to the target 0x8EDA89A9 checksum.
However, we can try to find collisions via brute-force (since the final check is reduced to a comparison with only a 32-bit number).

I wrote a Python script to bruteforce key. Although Python is slow, I used hashlib for efficient sha256 generation and cupy for matrix calculations on CUDA cores. 
After checking all options from MCM6{00000000} to MCM6{FFFFFFFF}, I found no collisions. Most likely, collisions are distributed non-uniformly due to the use of the emulator.

Furthermore, even if a collision were found, the resulting 0x40-byte buffer would contain garbage characters, and the success message would appear as an unreadable set of 
strange symbols. In my brute-force attempt, I assumed the keys follow the 'MCM6{%08X}' format. This assumption came from a hardcoded fake message: "\n[+] SUCCESS BUT NOT! Flag: MCM6{%08X}",
where a random rdtsc value is inserted as parameter every time.
=================

The brute-force script (see BRUTE\main_Ssub_7FF72A860000.py) iterates through variants from MCM6{00000000} to MCM6{FFFFFFFF}. To speed things up on multi-core CPUs, you can run multiple 
instances of this script with a specific prefix. For example: <python main_Ssub_7FF72A860000.py -p A>, and it will brute-force variants from MCM6{A0000000} to MCM6{AFFFFFFF}.

To accelerate calculations on CUDA cores, passwords are checked in batches of 100,000 per cycle. To achieve this, some changes were made to the original algorithm regarding matrix calculations
and data structures. Also, please excuse the messy code; it was written in a hurry and contains many rewrites, redundancies, naming inaccuracies, and possibly artifacts from previous versions.
If you are interested in a more detailed study of the original key transformation algorithm, you can find it in the program patch script (PATCH folder). 

You can also try to find the key yourself. By slightly modifying the script, you can change the format of the key. Maybe you'll get lucky!))

===================

Based on the fact that collisions are non-uniformly distributed, the key was not found, and even with a collision, the success message would be unreadable, I decided that the only way is 
to patch the program for a key of my choice.

To patch the program, we need to use a script with our custom key to perform the same calculations as the crackme and get the fnv1a_32 checksum (step 8). This checksum must be written over
the 0x8EDA89A9 value. But that's not enough. The 0x40-byte success message buffer will contain garbage. To transform this garbage into readable text after all calculations, the hardcoded 
crackme gamma (Unk_7FF72A8B54B0__HARDCODED_ORIG) must be modified. I chose "Success!\x00" as the success message.

Apparently, the program checks the image checksum after unpacking. Therefore, I decided not to modify the program directly, but to inject shellcode that patches the unpacked image before 
it is projected into memory and jumped to OEP.

The patching script is in the PATCH folder. 
To patch the program, run <python PATCH.py any_key_you_wish>. This will create a modified program that accepts the key you created.

====================

Final Notes

Emulator: I did not perform a deep analysis or a manual implementation of the emulator code. Instead, I dumped the emulator bytecode and run it from my scripts. To correctly insert the emulator 
bytecode in the Python context, I modified only a few instructions responsible for parameter input and temporary stack storage of the rdtsc result.

Constants: The 0x200×0x200 matrix (matrix_from_buf100000) inside the crackme is re-calculated every time. However, it is independent of the key and remains constant, so I simply dumped it. 
numpy_vec_0x800_7FF72A8B4CA0, buf_addr_7FF72A8B6CE0, and Unk_7FF72A8B54B0__HARDCODED_ORIG, along with other constants, were also dumped from the program. I tried to ensure they weren't corrupted
by the various anti-debugging and anti-emulation tricks this crackme is packed with!))))
The validity of all these constants is confirmed by the correct operation of the patch I created (all algorithms there are implemented exactly as in the original).

In the key-search script (BRUTE/main_Ssub_7FF72A860000.py), there are algorithm checks against pre-calculated values at the start, so there is some delay. 

====================

Thanks to the author for such an exciting challenge! It was very interesting for me.)