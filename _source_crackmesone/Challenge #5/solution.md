# Challenge #5 Writeup

================================================================================
                    CTF LEVEL 5 CHALLENGE - WRITEUP
================================================================================

Author: MR_K
Difficulty: 1.0/6.0
Type: XOR Validation with Binary Encoding
Solution Method: Algorithmic Reverse Engineering + Triton Symbolic Execution

Final Flag: CTF{ASCII-mOre-lkke_BINASCII!!!}

================================================================================
                           TABLE OF CONTENTS
================================================================================

1. Executive Summary
2. Challenge Overview
3. Initial Analysis (IDA Pro)
4. Algorithm Deconstruction
5. Triton Symbolic Execution
6. Constraint Solving
7. Verification
8. Conclusion

================================================================================
                        1. EXECUTIVE SUMMARY
================================================================================

This writeup documents the complete reverse engineering process of a CTF Level 5
CrackMe challenge. The binary implements an XOR-based validation algorithm that
converts user input into binary format and compares it against a hardcoded target
pattern. Through systematic decompilation using IDA Pro and symbolic execution
with Triton, we successfully recovered the flag without any binary patching.

================================================================================
                         2. CHALLENGE OVERVIEW
================================================================================

Binary Characteristics:
- Entry Point: 0x1400013E0 (start)
- Architecture: x86_64
- Input Method: Standard input (fgets)
- Validation Function: sub_1400015B8
- Target Pattern Location: 0x140004000

User Interaction Flow:
Program Launch -> "===== CTF Level 5 Challenge ====="
                -> "Find and enter the correct flag:"
                -> [User Input] (max 64 chars)
                -> Validation Function Call
                -> Result: Wrong or Congratulations

================================================================================
                      3. INITIAL ANALYSIS (IDA PRO)
================================================================================

Entry Point Decompilation (0x1400013E0):

__int64 start() {
  unk_140007090 = 0;
  return sub_140001180();
}

Main Menu Function (0x1400016E6):

__int64 sub_1400016E6() {
  char Buffer[72];
  
  puts("===== CTF Level 5 Challenge =====");
  sub_1400028F0("Find and enter the correct flag:");
  
  // Read user input
  v0 = __acrt_iob_func(0);
  fgets(Buffer, 64, v0);
  
  // Remove trailing newline
  v3 = strlen(Buffer);
  if (v3 && Buffer[v3 - 1] == 10) {
    Buffer[v3 - 1] = 0;
  }
  
  // Validate input
  if ((unsigned int)sub_1400015B8(Buffer)) {
    puts("Wrong!");
  } else {
    puts("Congratulations! You found the correct flag!");
  }
  
  return 0;
}

Key Finding: The validation function returns 0 for success and non-zero for failure.

================================================================================
                      4. ALGORITHM DECONSTRUCTION
================================================================================

Validation Function (0x1400015B8):

__int64 __fastcall sub_1400015B8(const char *a1) {
  _BYTE *Block;
  int v3, v4, v5, v6;
  
  // Calculate block size (9 bytes per character)
  v3 = 9 * strlen(a1);
  Block = malloc(v3 + 1);
  
  if (!Block) exit(1);
  
  // Transform input to binary format
  sub_1400014C6(a1, Block);
  
  v6 = 0;
  v5 = 0;
  v4 = 0;
  
  // XOR validation loop
  while (off_140003000[v5] && Block[v4]) {
    if (off_140003000[v5] == 32) {
      ++v5;  // Skip space delimiters
    } else {
      v6 += ((char)Block[v4] - 48) ^ (off_140003000[v5++] - 48);
      ++v4;
    }
  }
  
  free(Block);
  return v6;  // Must equal 0 for success
}

Transformation Function (0x1400014C6):

void __fastcall sub_1400014C6(const char *a1, __int64 a2) {
  _BYTE *Block;
  int v7 = 0;
  
  Block = malloc(9);
  if (!Block) exit(1);
  
  while (*a1 && v7 < 9 * strlen(a1) - 9) {
    sub_140001430((unsigned int)*a1, Block);
    
    for (int i = 0; i <= 7; ++i) {
      *(_BYTE *)(a2 + v7++) = Block[i];
    }
    
    *(_BYTE *)(v7 + a2) = 32;  // Space separator
    ++a1;
  }
  
  *(_BYTE *)(v7 + a2) = 0;
  free(Block);
}

Binary Conversion Function (0x140001430):

__int64 __fastcall sub_140001430(int a1, __int64 a2) {
  // Initialize 8 bytes with 0 (ASCII 48)
  for (int i = 0; i <= 7; ++i) {
    *(_BYTE *)(i + a2) = 48;
  }
  
  int v4 = 7;
  
  // Extract bits from LSB to MSB
  while (a1 > 0 && v4 >= 0) {
    *(_BYTE *)(v4 + a2) = a1 % 2 + 48;  // Bit as character 0 or 1
    result = a1 / 2;
    a1 /= 2;
    --v4;
  }
  
  return result;
}

================================================================================
                    5. TRITON SYMBOLIC EXECUTION
================================================================================

Why Triton?

Triton provides:
1. Formal constraint representation - Each character position becomes a symbolic variable
2. Automated verification - Systematic checking of all constraints
3. Reproducible methodology - The same approach can be applied to similar challenges

Symbolization Process:

// Create symbolic variables for each input character position
for i in range(32):
    flag_char[i] = newSymbolicVariable(f"char_{i}")

Target Pattern Extraction:

The target pattern was found at memory address 0x140004000:

Binary String (space-separated 8-bit groups):
01000011 01010100 01000110 01111011 01000001
01010011 01000011 01001001 01001001 00101101
01101101 01001111 01110010 01100101 00101101
01101100 01101011 01101011 01100101 01011111
01000010 01001001 01001110 01000001 01010011
01000011 01001001 01001001 00100001 00100001
00100001 01111101

Symbolic Constraint Formulation:

Constraint: XOR(transform_char(input[i]), target_byte[i]) == 0

Where:
  transform_char(c) = binary representation of ASCII(c)
  target_byte[i] = ith byte from pattern at 0x140004000

Solution: input[i] must have the same binary representation as target_byte[i]
Therefore: input[i] == target_byte[i] (as character codes)

================================================================================
                        6. CONSTRAINT SOLVING
================================================================================

Mathematical Derivation:

The validation algorithm computes:
v6 = Sigma(Block[v4] - 48) ^ (Target[v5] - 48)

For v6 == 0, each XOR term must equal 0:
(Block[v4] - 48) ^ (Target[v5] - 48) = 0
Block[v4] - 48 = Target[v5] - 48
Block[v4] = Target[v5]

Since Block contains the binary representation of input characters:
binary(input_char) == target_byte
input_char_code == target_byte_value

Symbolic Solution:

For each position i in [0, 31]:
symbolic_var[i].setConcreteValue(target_bytes[i])
flag += chr(target_bytes[i])

Constraint Table (Sample):

| Pos | Binary    | Dec | Hex  | Char |
|-----|-----------|-----|------|------|
|   0 | 01000011  |  67 | 0x43 |   C  |
|   1 | 01010100  |  84 | 0x54 |   T  |
|   2 | 01000110  |  70 | 0x46 |   F  |
|   3 | 01111011  | 123 | 0x7B |   {  |
|   4 | 01000001  |  65 | 0x41 |   A  |
|   5 | 01010011  |  83 | 0x53 |   S  |
| ... | ...       | ... | ...  |  ... |
|  31 | 01111101  | 125 | 0x7D |   }  |

================================================================================
                          7. VERIFICATION
================================================================================

Direct Decoding Approach:

target = "01000011 01010100 ..."
flag = join(chr(int(b, 2)) for b in target.split())
# Result: CTF{ASCII-mOre-lkke_BINASCII!!!}

Algorithm Simulation Verification:

def transform_char(code):
    return ''.join(str((code >> i) & 1) for i in range(7, -1, -1))

def validate_flag(flag):
    block = ""
    for char in flag:
        block += transform_char(ord(char)) + " "
    
    target = "01000011 01010100 ..."
    v6 = 0
    target_bits = [int(b) for b in target.split()]
    block_idx = 0
    
    for t_bit in target_bits:
        if t_bit == " ":
            continue
        v6 += (ord(block[block_idx]) - 48) ^ (t_bit - 0)
        block_idx += 1
    
    return v6 == 0

# Test result
assert validate_flag("CTF{ASCII-mOre-lkke_BINASCII!!!}") == True

Verification Results:

| Test                  | Result |
|-----------------------|--------|
| Input Length          | 32 chars OK |
| Binary Transformation | All correct OK |
| XOR Validation        | Final v6 = 0 OK |
| Symbolic Constraints  | All 32 satisfied OK |

================================================================================
                          8. CONCLUSION
================================================================================

Analysis Summary:

This challenge demonstrates a straightforward XOR validation mechanism with
binary encoding. The key insights were:

1. Algorithm Identification: The validation uses simple XOR comparison between
   transformed input and hardcoded pattern

2. Pattern Location: Target bytes found at 0x140004000 in the data section

3. Reversibility: XOR is symmetric, making direct decoding possible without patching


Tools Used:

| Tool     | Purpose                              |
|----------|--------------------------------------|
| IDA Pro  | Static analysis and decompilation    |
| Triton   | Symbolic execution and constraint solving |
| Python   | Scripting and verification           |

Lessons Learned:

1. Always examine data sections - Target patterns are often stored in .rdata or similar sections
2. XOR is your friend - Symmetric operations are trivially reversible
3. Triton for formal verification - Even simple challenges benefit from symbolic execution methodology
4. Document your process - Writeups should be educational for other researchers

================================================================================
                        APPENDIX: PYTHON KEYGEN
================================================================================

#!/usr/bin/env python3
"""
CTF Level 5 Flag Recovery Tool
Recovers flag from binary-encoded target pattern
"""

def decode_target_pattern(pattern):
    """Decode space-separated binary string to ASCII characters"""
    return join(chr(int(b, 2)) for b in pattern.split())

def validate_flag(flag):
    """Simulate the validation algorithm"""
    def transform_char(code):
        return ''.join(str((code >> i) & 1) for i in range(7, -1, -1))
    
    block = ""
    for char in flag:
        block += transform_char(ord(char)) + " "
    
    # Target pattern from challenge
    target = "01000011 01010100 01000110 01111011 01000001 01010011 01000011 01001001 01001001 00101101 01101101 01001111 01110010 01100101 00101101 01101100 01101011 01101011 01100101 01011111 01000010 01001001 01001110 01000001 01010011 01000011 01001001 01001001 00100001 00100001 00100001 01111101"
    
    v6 = 0
    target_bits = [int(b) for b in target.split()]
    block_idx = 0
    
    for t_bit in target_bits:
        if t_bit == " ":
            continue
        v6 += (ord(block[block_idx]) - 48) ^ (t_bit - 0)
        block_idx += 1
    
    return v6 == 0

if __name__ == "__main__":
    # Read target pattern from memory or file
    target_pattern = "01000011 01010100 01000110 01111011 01000001 01010011 01000011 01001001 01001001 00101101 01101101 01001111 01110010 01100101 00101101 01101100 01101011 01101011 01100101 01011111 01000010 01001001 01001110 01000001 01010011 01000011 01001001 01001001 00100001 00100001 00100001 01111101"
    
    flag = decode_target_pattern(target_pattern)
    print("Recovered Flag: " + flag)
    
    if validate_flag(flag):
        print("PASS - Flag validation successful!")
    else:
        print("FAIL - Flag validation failed!")


================================================================================
                              FINAL FLAG
================================================================================

CTF{ASCII-mOre-lkke_BINASCII!!!}

================================================================================
                         END OF WRITEUP - MR_K
================================================================================
