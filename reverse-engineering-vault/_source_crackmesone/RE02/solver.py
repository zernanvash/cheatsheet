from z3 import *

# 1. The perfectly aligned integers we extracted from Ghidra.
targets = [
    0x72, 0x87, 0x565, 0x39, 0xEE, 0x8D7, 0x82, 0xA5, 
    0x83F, 0x6F, 0xBF, 0x95E, 0x32, 0xB8, 0xAB0, 0x74, 
    0x7D, 0x50B, 0x42, 0xF9, 0xB9D, 0x7D, 0xE5, 0xB6C, 
    0x7B, 0xB6, 0x5CF, 0x86, 0xC2, 0x58F, 0x5BB, 0x18CE, 
    0xA97E, 0x6B00, 0xDA17, 0x892B4, 0x12F064, 0x24859, 0x24A29, 0x3E7, 
    0xA50C7, 0x8BEF, 0x36D, 0x133, 0x2CF, 0x1A1, 0x38, 0x33, 
    0x66, 0x35, 0x32, 0x31, 0x34, 0x34
]

# 2. Create 49 8-bit variables for the flag characters
flag = [BitVec(f"c_{i}", 8) for i in range(49)]

s = Solver()

# 3. Constrain the flag to printable ASCII characters
for c in flag:
    s.add(c >= 32, c <= 126)


# 4. ALL 54 equations
s.add(flag[1] + (flag[0] % 19) == targets[0])
s.add(flag[2] + flag[0] + 19 == targets[1])
s.add(flag[3] + (19 * flag[0]) == targets[2])
s.add(flag[5] + (flag[4] % 20) == targets[3])
s.add(flag[4] + flag[6] + 20 == targets[4])
s.add(flag[7] + 20 * flag[4] == targets[5])
s.add(flag[9] + (flag[8] % 21) == targets[6])
s.add(flag[8] + flag[10] + 21 == targets[7])
s.add(flag[11] + 21 * flag[8] == targets[8])
s.add(flag[13] + (flag[12] % 22) == targets[9])
s.add(flag[12] + flag[14] + 22 == targets[10])
s.add(flag[15] + 22 * flag[12] == targets[11])
s.add(flag[17] + (flag[16] % 23) == targets[12])
s.add(flag[18] + flag[16] + 23 == targets[13])
s.add(flag[19] + 23 * flag[16] == targets[14])
s.add(flag[21] + (flag[20] % 24) == targets[15])
s.add(flag[20] + flag[22] + 24 == targets[16])
s.add(flag[23] + 24 * flag[20] == targets[17])
s.add(flag[25] + (flag[24] % 25) == targets[18])
s.add(flag[24] + flag[26] + 25 == targets[19])
s.add(flag[27] + 25 * flag[24] == targets[20])
s.add(flag[29] + (flag[28] % 26) == targets[21])
s.add(flag[28] + flag[30] + 26 == targets[22])
s.add(flag[31] + 26 * flag[28] == targets[23])
s.add(flag[33] + (flag[32] % 27) == targets[24])
s.add(flag[34] + flag[32] + 27 == targets[25])
s.add(flag[35] + 27 * flag[32] == targets[26])
s.add(flag[37] + (flag[36] % 28) == targets[27])
s.add(flag[36] + flag[38] + 28 == targets[28])
s.add(flag[39] + 28 * flag[36] == targets[29])
s.add(flag[40] + 28 * flag[36] == targets[30])

# The complex block algebra mappings
s.add(flag[43] + flag[47] + flag[42] + flag[46] + flag[41] + flag[45] + flag[44] + flag[48] + (flag[33] ^ flag[34]) * (flag[38] + flag[39] + flag[36] + flag[37] + flag[40] + flag[35]) == targets[31])
s.add(flag[43] + flag[47] + flag[42] + flag[46] + flag[41] + flag[45] + flag[44] + flag[48] + (flag[33] ^ flag[35] ^ flag[34]) * (flag[38] + flag[39] + flag[36] + flag[37] + flag[40]) == targets[32])
s.add((flag[33] + flag[34] + flag[35]) * (flag[39] ^ flag[38] ^ flag[36] ^ flag[40] ^ flag[37]) - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[33])
s.add(flag[43] + flag[47] + flag[42] + flag[46] + flag[41] + flag[45] + flag[44] + flag[48] + (flag[26] ^ flag[25]) * (flag[29] + flag[32] + flag[27] + flag[30] + flag[31] + flag[28]) == targets[34])
s.add(flag[29] + flag[28] + (flag[27] ^ flag[26] ^ flag[25]) + flag[32] * flag[30] * flag[31] - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[35])
s.add(flag[26] + flag[27] + flag[25] + (flag[32] ^ flag[31] ^ (flag[29] * flag[30] * flag[28])) - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[36])
s.add(flag[17] * flag[18] * flag[19] + (flag[23] ^ flag[22] ^ flag[20] ^ flag[24] ^ flag[21]) - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[37])
s.add(flag[43] + flag[47] + flag[20] + flag[42] + flag[46] + flag[41] + flag[45] + flag[44] + flag[48] + flag[17] * flag[18] * flag[19] - flag[24] - flag[21] - flag[23] - flag[22] == targets[38])
s.add(flag[22] + flag[23] + flag[43] + flag[47] + flag[20] + flag[42] + flag[46] + flag[21] + flag[24] + flag[41] + flag[45] + flag[44] + flag[48] + (flag[17] ^ flag[19] ^ flag[18]) == targets[39])
s.add(flag[10] * flag[11] * flag[9] + (flag[16] ^ flag[13] ^ flag[15] ^ flag[14] ^ flag[12]) - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[40])
s.add((flag[10] + flag[9]) * (flag[16] ^ flag[13] ^ flag[15] ^ flag[14] ^ (flag[11] + flag[12])) - flag[48] - flag[44] - flag[45] - flag[41] - flag[46] - flag[42] - flag[47] - flag[43] == targets[41])
s.add(flag[13] + flag[16] + flag[43] + flag[47] + flag[10] + flag[42] + flag[46] + flag[15] + flag[41] + flag[45] + flag[9] + flag[12] + flag[44] + flag[48] - flag[14] - flag[11] == targets[42])
s.add(flag[43] + flag[47] + flag[42] + flag[46] + flag[2] + flag[41] + flag[45] + flag[44] + flag[48] - (flag[7] ^ flag[6] ^ flag[4] ^ flag[8] ^ flag[5] ^ flag[3]) - flag[1] == targets[43])
s.add(flag[1] + flag[6] + flag[7] + flag[4] + flag[5] + flag[8] + flag[3] + (flag[47] ^ flag[43] ^ flag[46] ^ flag[42] ^ flag[45] ^ flag[41] ^ flag[48] ^ flag[44]) - flag[2] == targets[44])
s.add(flag[1] + flag[43] + flag[47] + flag[42] + flag[46] + flag[41] + flag[45] + flag[44] + flag[48] - (flag[7] ^ flag[6] ^ flag[4] ^ flag[8] ^ flag[5] ^ flag[3]) - flag[2] == targets[45])

# Hardcoded ending string check
s.add(flag[41] == targets[46])
s.add(flag[42] == targets[47])
s.add(flag[43] == targets[48])
s.add(flag[44] == targets[49])
s.add(flag[45] == targets[50])
s.add(flag[46] == targets[51])
s.add(flag[47] == targets[52])
s.add(flag[48] == targets[53])


# 5. Evaluate
print("[*] Solving...")
if s.check() == sat:
    model = s.model()
    solved_flag = "".join([chr(model[flag[i]].as_long()) for i in range(49)])
    print(f"[+] Flag found: {solved_flag}")
else:
    print("[-] UNSAT. Your equations are wrong.")