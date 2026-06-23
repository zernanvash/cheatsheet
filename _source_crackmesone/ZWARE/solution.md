Challenge_URL: https://crackmes.one/crackme/69e2a353471059af19ad0951

Writeup: MAS's ZWARE - Custom VM Architecture Reversing
1. Challenge Overview
Platform: crackmes.one
Difficulty: Tier 4
Protection Mechanisms: Custom Virtual Machine (VM), Bytecode-based Instruction Set, STL Container Obfuscation (std::unordered_map).
2. Reverse Engineering Process
Phase 1: Entry Point & Target Extraction
Using Ghidra, I searched for the string "Enter The Flag : " to locate the main logic function at FUN_140002300.
Input Handling: The program reads user input via std::cin and stores it in a local buffer.
Ciphertext Recovery: Near the end of the function at label LAB_140002448, I identified a hardcoded 21-byte target array initialized as follows:
80 A8 D8 BC A4 84 4C 14 34 EC 00 14 38 D4 D4 14 58 EC 80 8C 9C (Little-Endian).
Phase 2: Deconstructing the VM Engine
Inside the core transformation function (the VM Interpreter), I analyzed the dispatch logic (switch-case style implemented via map lookups) and mapped the Instruction IDs to specific bitwise operations:
ID 0x7a ('z'): Executes a bitwise XOR 0x5A.
ID 0x70 ('p'): Executes a Rotate Right (ROR) 6 (implemented as >> 6 | << 2).
ID 0x6c ('l'): Executes a Rotate Right (ROR) 2 (implemented as >> 2 | << 6).
ID 0x75 ('u'): Triggers the final validation via memcmp. If successful, it prints "Correct".
Phase 3: Bytecode Script Recovery
I located the VM's instruction sequence in the .zplus data section (address 14000D000). The "script" consists of the following sequence:
7a (XOR) -> 70 (ROR6) -> 7a (XOR) -> 70 (ROR6) -> 7a (XOR) -> 6c (ROR2) -> 7a (XOR) -> 70 (ROR6) -> 7a (XOR) -> 6c (ROR2).
3. Algorithm Reversing (Keygen)
Since all VM instructions are reversible bitwise operations, the flag can be recovered by applying the inverse operations in reverse order to the target ciphertext.
The inverse of XOR 0x5A is XOR 0x5A.
The inverse of ROR N is ROL N (Rotate Left).
Solution Script (Python):
python
def rol(v, n): return ((v << n) & 0xFF) | (v >> (8 - n))

target = [0x80, 0xA8, 0xD8, 0xBC, 0xA4, 0x84, 0x4C, 0x14, 0x34, 0xEC, 
          0x00, 0x14, 0x38, 0xD4, 0xD4, 0x14, 0x58, 0xEC, 0x80, 0x8C, 0x9C]

def decrypt(b):
    # Reverse execution of the recovered bytecode script
    ops = ['rol2', 'xor', 'rol6', 'xor', 'rol2', 'xor', 'rol6', 'xor', 'rol6', 'xor']
    for op in ops:
        if op == 'xor': b ^= 0x5A
        elif op == 'rol2': b = rol(b, 2)
        elif op == 'rol6': b = rol(b, 6)
    return b

flag = "".join([chr(decrypt(x)) for x in target])
print(f"Decrypted Flag: {flag}")
请谨慎使用此类代码。
4. Conclusion
The flag is recovered as: zplus{I_WaZ_Too_Lazy}.
The challenge demonstrates a standard VM-based protection. While the use of C++ STL containers adds some noise to the disassembly, the underlying logic remains vulnerable to static analysis of the opcode-to-handler mapping.