#!/usr/bin/env python3
"""Disassemble the VM bytecodes for babel_vm.exe"""

# Primary VM (switch in main function) opcode semantics from decompiled code:
# case 0: NOP - vpc++
# case 1: LOAD_IMM reg, imm16 - reg[op1] = (op2 << 8 | op3); vpc += 4
# case 2: LOAD_SREG reg, sreg - reg[op1] = sreg_file[op2]; vpc += 3
# case 3: MOV reg_dst, reg_src - reg[op1|op2] = reg[op2]; vpc += 3 (seems wrong, re-check)
#   Actually: reg[op1] = reg[op2] where op1 and op2 are separate; vpc += 3
# case 4: ADD reg_dst, reg_src - reg[op1] += reg[op2]; vpc += 3
# case 5: SUB reg_dst, reg_src - reg[op1] -= reg[op2]; vpc += 3
# case 6: MUL reg_dst, reg_src - reg[op1] *= reg[op2]; vpc += 3
# case 7: XOR reg_dst, reg_src - reg[op1] ^= reg[op2]; vpc += 3
# case 8: AND reg_dst, reg_src - reg[op1] &= reg[op2]; vpc += 3
# case 9: OR  reg_dst, reg_src - reg[op1] |= reg[op2]; vpc += 3
# case 0xa: SHL reg, imm - reg[op1] <<= (op2 & 0x1f); vpc += 3
# case 0xb: SHR reg, imm - reg[op1] >>= (op2 & 0x1f); vpc += 3
# case 0xc: NOT reg - reg[op1] = ~reg[op1]; vpc += 2
# case 0xd: CMP reg1, reg2 - flag = (reg[op1] == reg[op2]); vpc += 3
# case 0xe: JMP imm16 - vpc = (op2 << 8 | op1); (unconditional jump)
# case 0xf: JZ imm16 - if flag==0: vpc = (op2<<8|op1) else vpc = (op1<<8|op2); 
#   Wait... let me re-read: if (local_e4 == 0) goto LAB_14000473c (vpc = uVar19+3)
#   else: vpc = (int)pFVar24 << 8 | (uint)bVar18  
#   Actually: case 0xf: if flag==0 -> vpc=op2<<8|op1; else -> vpc unchanged (vpc += 3)
#   Wait no. Let me re-read more carefully.
# case 0xf: JNZ - if (flag != 0): vpc = op2<<8|op1; else: goto LAB_14000473c (vpc = uVar19+3)
#   So: if flag: vpc = imm16; else: vpc += 3
# case 0x10: JZ - if (flag == 0): vpc = op2<<8|op1; else: goto LAB_14000473c (vpc = uVar19+3)  
#   Actually looking again: case 0x10 goes to LAB_14000473c if flag!=0, vice versa of 0xf
#   case 0xf: if flag==0 => LAB_14000473c (skip, vpc+=3); if flag!=0 => LAB_1400046ff (jump)
#   case 0x10: if flag==0 => LAB_1400046ff (jump); if flag!=0 => LAB_14000473c (skip, vpc+=3)
# case 0x11: PUSH reg - push reg[op1] onto vstack; vpc += 2
# case 0x12: POP reg - pop from vstack into reg[op1]; vpc += 2
# case 0x13: STORE_OUT reg_dst, reg_src - out_regs[op1] = reg[op2]; vpc += 3
# case 0x14: HALT - set halt flag; vpc += 1
# case 0x15: ADD_IMM reg, imm16 - reg[op1] += imm16; vpc += 4
# case 0x16: XOR_IMM reg, imm16 - reg[op1] ^= imm16; vpc += 4
# case 0x17: AND_IMM reg, imm16 - reg[op1] &= imm16; vpc += 4
# case 0x18: ROL reg, imm - reg[op1] = rotl32(reg[op1], op2&0x1f); vpc += 3
# case 0x19: ROR reg, imm - reg[op1] = rotr32(reg[op1], op2&0x1f); vpc += 3
# case 0x1a: CALL imm16 - push vpc+3 onto call stack; vpc = imm16
# case 0x1b: RET - pop from call stack into vpc
# case 0x1c: MUL_IMM reg, imm16 - reg[op1] *= imm16; vpc += 4
# case 0x1d: CMP_IMM reg, imm16 - flag = (reg[op1] == imm16); vpc += 4
# case 0x1e: SUB_IMM reg, imm16 - reg[op1] -= imm16; vpc += 4
# case 0x1f: SWAP reg1, reg2 - swap reg[op1] and reg[op2]; vpc += 3
# case 0x20: INVOKE_VM2 which - invoke secondary stack VM; vpc += 2
# case 0x21: STORE_BC offset, reg - bytecode[offset] = reg[op3] & 0xff; vpc += 4
# case 0x22: LOAD_ITER reg - reg[op1] = iteration_counter; vpc += 2
# case 0x23: OR_IMM reg, imm16 - reg[op1] |= imm16; vpc += 4
# case 0x24: CRC16 reg1, reg2 - reg[op1] = crc16(reg[op1] ^ reg[op2]); vpc += 3
# case 0x25: LOAD_ACC reg - reg[op1] = accumulator; vpc += 2
# case 0x26: STORE_ACC reg - accumulator = reg[op1]; vpc += 2
# case 0x27: LFSR reg - reg[op1] = lfsr_step(reg[op1]); vpc += 2

# Opcode dispatch table maps raw bytecodes to case numbers
opcode_table = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")

# Build reverse map: raw_byte -> case_number
raw_to_case = {i: opcode_table[i] for i in range(len(opcode_table))}

# Case name map
case_names = {
    0: "NOP",
    1: "LOAD_IMM",     # reg, imm16 (4 bytes)
    2: "LOAD_SREG",    # reg, sreg_idx (3 bytes)
    3: "MOV",          # dst, src (3 bytes)
    4: "ADD",          # dst, src (3 bytes)
    5: "SUB",          # dst, src (3 bytes)
    6: "MUL",          # dst, src (3 bytes)
    7: "XOR",          # dst, src (3 bytes)
    8: "AND",          # dst, src (3 bytes)
    9: "OR",           # dst, src (3 bytes)
    0xa: "SHL",        # reg, imm (3 bytes)
    0xb: "SHR",        # reg, imm (3 bytes)
    0xc: "NOT",        # reg (2 bytes)
    0xd: "CMP",        # reg1, reg2 (3 bytes)
    0xe: "JMP",        # imm16 (3 bytes)
    0xf: "JNZ",        # imm16 (3 bytes) - jump if flag != 0
    0x10: "JZ",        # imm16 (3 bytes) - jump if flag == 0
    0x11: "PUSH",      # reg (2 bytes)
    0x12: "POP",       # reg (2 bytes)
    0x13: "STORE_OUT", # dst, src (3 bytes)
    0x14: "HALT",      # (1 byte)
    0x15: "ADD_IMM",   # reg, imm16 (4 bytes)
    0x16: "XOR_IMM",   # reg, imm16 (4 bytes)
    0x17: "AND_IMM",   # reg, imm16 (4 bytes)
    0x18: "ROL",       # reg, imm (3 bytes)
    0x19: "ROR",       # reg, imm (3 bytes)
    0x1a: "CALL",      # imm16 (3 bytes)
    0x1b: "RET",       # (1 byte)
    0x1c: "MUL_IMM",   # reg, imm16 (4 bytes)
    0x1d: "CMP_IMM",   # reg, imm16 (4 bytes)
    0x1e: "SUB_IMM",   # reg, imm16 (4 bytes)
    0x1f: "SWAP",      # reg1, reg2 (3 bytes)
    0x20: "INVOKE_VM2",# which (2 bytes)
    0x21: "STORE_BC",  # offset16, reg (4 bytes)
    0x22: "LOAD_ITER", # reg (2 bytes)
    0x23: "OR_IMM",    # reg, imm16 (4 bytes)
    0x24: "CRC16",     # reg1, reg2 (3 bytes)
    0x25: "LOAD_ACC",  # reg (2 bytes)
    0x26: "STORE_ACC", # reg (2 bytes)
    0x27: "LFSR",      # reg (2 bytes)
}

# Instruction sizes by case
case_sizes = {
    0: 1,   # NOP
    1: 4,   # LOAD_IMM
    2: 3,   # LOAD_SREG
    3: 3,   # MOV
    4: 3,   # ADD
    5: 3,   # SUB
    6: 3,   # MUL
    7: 3,   # XOR
    8: 3,   # AND
    9: 3,   # OR
    0xa: 3, # SHL
    0xb: 3, # SHR
    0xc: 2, # NOT
    0xd: 3, # CMP
    0xe: 3, # JMP
    0xf: 3, # JNZ
    0x10: 3,# JZ
    0x11: 2,# PUSH
    0x12: 2,# POP
    0x13: 3,# STORE_OUT
    0x14: 1,# HALT
    0x15: 4,# ADD_IMM
    0x16: 4,# XOR_IMM
    0x17: 4,# AND_IMM
    0x18: 3,# ROL
    0x19: 3,# ROR
    0x1a: 3,# CALL
    0x1b: 1,# RET
    0x1c: 4,# MUL_IMM
    0x1d: 4,# CMP_IMM
    0x1e: 4,# SUB_IMM
    0x1f: 3,# SWAP
    0x20: 2,# INVOKE_VM2
    0x21: 4,# STORE_BC
    0x22: 2,# LOAD_ITER
    0x23: 4,# OR_IMM
    0x24: 3,# CRC16
    0x25: 2,# LOAD_ACC
    0x26: 2,# STORE_ACC
    0x27: 2,# LFSR
}

def disasm_primary(bytecode, label=""):
    """Disassemble primary VM bytecode."""
    pc = 0
    print(f"\n=== Disassembly: {label} ({len(bytecode)} bytes) ===")
    while pc < len(bytecode):
        raw = bytecode[pc]
        if raw >= len(opcode_table):
            print(f"  {pc:04x}: INVALID raw_byte={raw:02x}")
            pc += 1
            continue
        case = opcode_table[raw]
        name = case_names.get(case, f"UNK_{case:02x}")
        size = case_sizes.get(case, 1)
        
        if pc + size > len(bytecode):
            print(f"  {pc:04x}: {name} (truncated)")
            break
        
        raw_bytes = bytecode[pc:pc+size]
        hex_str = ' '.join(f'{b:02x}' for b in raw_bytes)
        
        if size == 1:
            print(f"  {pc:04x}: {hex_str:12s} {name}")
        elif size == 2:
            op1 = bytecode[pc+1]
            if case in (0x11, 0x12, 0xc, 0x22, 0x25, 0x26, 0x27):
                print(f"  {pc:04x}: {hex_str:12s} {name} r{op1}")
            elif case == 0x20:
                print(f"  {pc:04x}: {hex_str:12s} {name} #{op1}")
            else:
                print(f"  {pc:04x}: {hex_str:12s} {name} {op1}")
        elif size == 3:
            op1 = bytecode[pc+1]
            op2 = bytecode[pc+2]
            if case in (0xe, 0xf, 0x10):
                target = (op2 << 8) | op1
                print(f"  {pc:04x}: {hex_str:12s} {name} 0x{target:04x}")
            elif case in (0xa, 0xb, 0x18, 0x19):
                print(f"  {pc:04x}: {hex_str:12s} {name} r{op1}, #{op2}")
            elif case == 0x1a:
                target = (op2 << 8) | op1
                print(f"  {pc:04x}: {hex_str:12s} {name} 0x{target:04x}")
            elif case == 0x24:
                print(f"  {pc:04x}: {hex_str:12s} {name} r{op1}, r{op2}")
            else:
                print(f"  {pc:04x}: {hex_str:12s} {name} r{op1}, r{op2}")
        elif size == 4:
            op1 = bytecode[pc+1]
            op2 = bytecode[pc+2]
            op3 = bytecode[pc+3]
            imm16 = (op3 << 8) | op2
            if case == 0x21:
                offset = (op2 << 8) | op1
                print(f"  {pc:04x}: {hex_str:12s} {name} [0x{offset:04x}], r{op3}")
            else:
                print(f"  {pc:04x}: {hex_str:12s} {name} r{op1}, 0x{imm16:04x}")
        
        pc += size

# Decrypt bytecodes
def decrypt_bc(data, key, length):
    result = bytearray()
    for i in range(length):
        result.append(data[i] ^ key[i & 3])
    return bytes(result)

# Main VM bytecode
main_bc_hex = "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000"
main_bc = bytes.fromhex(main_bc_hex)
key_main = bytes([0x5a, 0x1c, 0xbe, 0xb4])
decrypted_main = decrypt_bc(main_bc, key_main, 0x263)
disasm_primary(decrypted_main, "Main VM Bytecode")

# Now disassemble secondary VM bytecodes
# The secondary VMs use a stack-based architecture with different instruction encoding
# From the switch at 0x14000427e (inner VM)
# The inner VM opcodes are (byte value - 1):
# 0: PUSH_REG sreg_idx (2 bytes)
# 1: PUSH_IMM16 (3 bytes) 
# 2: ADD (1 byte)
# 3: SUB (1 byte)
# 4: MUL (1 byte)
# 5: XOR (1 byte)
# 6: AND (1 byte)
# 7: OR (1 byte)
# 8: ROL (1 byte)
# 9: ROR (1 byte)
# 0xa: EQ (1 byte) 
# 0xb: DUP (1 byte)
# 0xc: SWAP (1 byte)
# 0xd: NOT16 (1 byte)
# 0xe: TRUNC16 (1 byte)
# 0xf: RESULT_TRUE / DONE_OK (1 byte)
# 0x10: RESULT_FALSE / DONE_FAIL (1 byte)
# 0x11: JNZ imm16 (3 bytes)
# 0x12: JZ imm16 (3 bytes)
# 0x13: DROP (1 byte)
# 0x14: CRC16 (1 byte)
# 0x15: SHL (1 byte)
# 0x16: SHR (1 byte)

vm2_names = {
    0: "PUSH_REG", 1: "PUSH_IMM16", 2: "ADD", 3: "SUB", 4: "MUL", 5: "XOR",
    6: "AND", 7: "OR", 8: "ROL", 9: "ROR", 0xa: "EQ", 0xb: "DUP", 0xc: "SWAP",
    0xd: "NOT16", 0xe: "TRUNC16", 0xf: "DONE_TRUE", 0x10: "DONE_FALSE",
    0x11: "JNZ", 0x12: "JZ", 0x13: "DROP", 0x14: "CRC16", 0x15: "SHL", 0x16: "SHR"
}

def disasm_vm2(bytecode, label="", num_regs=0):
    """Disassemble secondary stack VM bytecode."""
    pc = 0
    print(f"\n=== Disassembly (Stack VM): {label} ({len(bytecode)} bytes) ===")
    while pc < len(bytecode):
        raw = bytecode[pc]
        opcode = raw - 1
        if opcode < 0 or opcode > 0x16:
            print(f"  {pc:04x}: {raw:02x}       INVALID")
            pc += 1
            continue
        
        name = vm2_names.get(opcode, f"UNK_{opcode:02x}")
        
        if opcode == 0:
            if pc + 1 < len(bytecode):
                reg = bytecode[pc+1]
                r_name = f"sreg{reg}" if reg < num_regs else f"s{reg}"
                print(f"  {pc:04x}: {raw:02x} {reg:02x}    {name} {r_name}")
                pc += 2
            else: break
        elif opcode == 1:
            if pc + 2 < len(bytecode):
                lo = bytecode[pc+1]
                hi = bytecode[pc+2]
                imm = (hi << 8) | lo
                print(f"  {pc:04x}: {raw:02x} {lo:02x} {hi:02x} {name} 0x{imm:04x}")
                pc += 3
            else: break
        elif opcode in (0x11, 0x12):
            if pc + 2 < len(bytecode):
                lo = bytecode[pc+1]
                hi = bytecode[pc+2]
                target = (hi << 8) | lo
                print(f"  {pc:04x}: {raw:02x} {lo:02x} {hi:02x} {name} 0x{target:04x}")
                pc += 3
            else: break
        else:
            print(f"  {pc:04x}: {raw:02x}       {name}")
            pc += 1


# Bytecode 2 - invoked with bVar18==0 (first set of 6 source regs)
key_bc2 = bytes([0xde, 0xef, 0xbe, 0xad])
bc2 = bytes.fromhex("DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF")
decrypted_bc2 = decrypt_bc(bc2, key_bc2, 0x21)
disasm_vm2(decrypted_bc2, "VM2 Bytecode #0 (bVar18=0)", 6)

# Bytecode 3 - invoked with bVar18==1
key_bc3 = bytes([0xca, 0xbe, 0xba, 0xfe])
bc3 = bytes.fromhex("CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB")
decrypted_bc3 = decrypt_bc(bc3, key_bc3, 0x27)
disasm_vm2(decrypted_bc3, "VM2 Bytecode #1 (bVar18=1)", 9)

# Bytecode 4 - invoked with bVar18==2  
key_bc4 = bytes([0x13, 0xde, 0xc0, 0x37])
bc4 = bytes.fromhex("1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02")
decrypted_bc4 = decrypt_bc(bc4, key_bc4, 0x29)
disasm_vm2(decrypted_bc4, "VM2 Bytecode #2 (bVar18=2)", 10)
