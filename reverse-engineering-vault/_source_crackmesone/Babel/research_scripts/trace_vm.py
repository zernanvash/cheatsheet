#!/usr/bin/env python3
"""Detailed step trace of the primary VM to debug constraint equations."""

def murmur_hash(username):
    h = 0x42414245
    data = username.encode('ascii') if isinstance(username, str) else username
    length = len(data)
    for i in range(length):
        shift = (i & 3) << 3
        h ^= (data[i] << shift)
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 0x5BD1E995) & 0xFFFFFFFF
        h ^= (h >> 15)
    h = ((h ^ length) * 0xCC9E2D51) & 0xFFFFFFFF
    if ((h - (h >> 16)) & 0xFFFFFFFF) == 0:
        return 0x42424242
    return (h ^ (h >> 16)) & 0xFFFFFFFF

def decrypt_bc(data_hex, key_bytes, length):
    data = bytes.fromhex(data_hex)
    return bytearray(data[i] ^ key_bytes[i & 3] for i in range(length))

username = "test"
h = murmur_hash(username)
H0 = h & 0xFFFF
H1 = (h >> 16) & 0xFFFF
print(f"H0=0x{H0:04x}, H1=0x{H1:04x}")

main_bc = decrypt_bc(
    "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000",
    [0x5A, 0x1C, 0xBE, 0xB4], 0x263
)

opcode_table = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")
case_names = {0:"NOP",1:"LOAD_IMM",2:"LOAD_SREG",3:"MOV",4:"ADD",5:"SUB",
             6:"MUL",7:"XOR",8:"AND",9:"OR",0xa:"SHL",0xb:"SHR",0xc:"NOT",
             0xd:"CMP",0xe:"JMP",0xf:"JNZ",0x10:"JZ",0x11:"PUSH",0x12:"POP",
             0x13:"STORE_OUT",0x14:"HALT",0x15:"ADD_IMM",0x16:"XOR_IMM",
             0x17:"AND_IMM",0x18:"ROL",0x19:"ROR",0x1a:"CALL",0x1b:"RET",
             0x1c:"MUL_IMM",0x1d:"CMP_IMM",0x1e:"SUB_IMM",0x1f:"SWAP",
             0x20:"INVOKE_VM2",0x21:"STORE_BC",0x22:"LOAD_ITER",0x23:"OR_IMM",
             0x24:"CRC16",0x25:"LOAD_ACC",0x26:"STORE_ACC",0x27:"LFSR"}
case_sizes = {0:1,1:4,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:3,0xa:3,0xb:3,0xc:2,
             0xd:3,0xe:3,0xf:3,0x10:3,0x11:2,0x12:2,0x13:3,0x14:1,0x15:4,
             0x16:4,0x17:4,0x18:3,0x19:3,0x1a:3,0x1b:1,0x1c:4,0x1d:4,0x1e:4,
             0x1f:3,0x20:2,0x21:4,0x22:2,0x23:4,0x24:3,0x25:2,0x26:2,0x27:2}

regs = [0]*8
sregs = [H0, H1, 0xAAAA, 0xBBBB, 0xCCCC, 0xDDDD, 0xEEEE, 0xFFFF, 0x1111, 0x2222]
acc = 0xDEAD
flag = 0
vpc = 0

# Step through first ~100 instructions, printing each
for step in range(200):
    if vpc >= len(main_bc):
        break
    raw = main_bc[vpc]
    if raw >= len(opcode_table):
        break
    case = opcode_table[raw]
    cn = case_names.get(case, f"?{case}")
    sz = case_sizes.get(case, 1)
    
    op1 = main_bc[vpc+1] if vpc+1 < len(main_bc) else 0
    op2 = main_bc[vpc+2] if vpc+2 < len(main_bc) else 0
    op3 = main_bc[vpc+3] if vpc+3 < len(main_bc) else 0
    imm16 = (op3 << 8) | op2
    
    hexbytes = ' '.join(f'{main_bc[vpc+i]:02x}' for i in range(min(sz, len(main_bc)-vpc)))
    
    # Execute
    old_regs = list(regs)
    old_vpc = vpc
    
    if case == 0: vpc += 1
    elif case == 1: regs[op1] = imm16; vpc += 4
    elif case == 2: regs[op1] = sregs[op2] if op2 < len(sregs) else 0; vpc += 3
    elif case == 3: regs[op1] = regs[op2]; vpc += 3
    elif case == 4: regs[op1] = (regs[op1] + regs[op2]) & 0xFFFFFFFF; vpc += 3
    elif case == 5: regs[op1] = (regs[op1] - regs[op2]) & 0xFFFFFFFF; vpc += 3
    elif case == 6: regs[op1] = (regs[op1] * regs[op2]) & 0xFFFFFFFF; vpc += 3
    elif case == 7: regs[op1] ^= regs[op2]; vpc += 3
    elif case == 8: regs[op1] &= regs[op2]; vpc += 3
    elif case == 9: regs[op1] |= regs[op2]; vpc += 3
    elif case == 0xa: regs[op1] = (regs[op1] << (op2&0x1f)) & 0xFFFFFFFF; vpc += 3
    elif case == 0xb: regs[op1] >>= (op2&0x1f); vpc += 3
    elif case == 0xc: regs[op1] = (~regs[op1]) & 0xFFFFFFFF; vpc += 2
    elif case == 0xd: flag = 1 if regs[op1]==regs[op2] else 0; vpc += 3
    elif case == 0xe: vpc = (op2<<8)|op1
    elif case == 0xf:
        t = (op2<<8)|op1
        vpc = t if flag else vpc+3
    elif case == 0x10:
        t = (op2<<8)|op1
        vpc = t if not flag else vpc+3
    elif case == 0x14: break  # HALT
    elif case == 0x15: regs[op1] = (regs[op1]+imm16)&0xFFFFFFFF; vpc += 4
    elif case == 0x16: regs[op1] ^= imm16; vpc += 4
    elif case == 0x17: regs[op1] &= imm16; vpc += 4
    elif case == 0x18:
        s = op2&0x1f; v = regs[op1]&0xFFFFFFFF
        regs[op1] = ((v<<s)|(v>>(32-s)))&0xFFFFFFFF; vpc += 3
    elif case == 0x19:
        s = op2&0x1f; v = regs[op1]&0xFFFFFFFF
        regs[op1] = ((v>>s)|(v<<(32-s)))&0xFFFFFFFF; vpc += 3
    elif case == 0x1c: regs[op1] = (regs[op1]*imm16)&0xFFFFFFFF; vpc += 4
    elif case == 0x1d: flag = 1 if regs[op1]==imm16 else 0; vpc += 4
    elif case == 0x1e: regs[op1] = (regs[op1]-imm16)&0xFFFFFFFF; vpc += 4
    elif case == 0x1f: regs[op1],regs[op2] = regs[op2],regs[op1]; vpc += 3
    elif case == 0x22: regs[op1] = step; vpc += 2
    elif case == 0x25: regs[op1] = acc; vpc += 2
    elif case == 0x26: acc = regs[op1]; vpc += 2
    elif case == 0x27:
        v = regs[op1]&0xFFFF
        if v&1: regs[op1] = ((v>>1)^0xB400)&0xFFFF
        else: regs[op1] = (v>>1)&0xFFFF
        vpc += 2
    elif case == 0x24:
        v = regs[op1]^regs[op2]; v &= 0xFFFF
        for _ in range(16):
            if v&1: v = (v>>1)^0xA001
            else: v >>= 1
        regs[op1] = v&0xFFFF; vpc += 3
    else:
        print(f"  {old_vpc:04x}: {hexbytes:16s} {cn} -- UNHANDLED, stopping")
        break
    
    # Print
    reg_changes = []
    for i in range(8):
        if regs[i] != old_regs[i]:
            reg_changes.append(f"r{i}=0x{regs[i]:08x}")
    changes = ', '.join(reg_changes) if reg_changes else ""
    if case == 0xd:
        changes += f" flag={flag}"
    elif case == 0x1d:
        changes += f" flag={flag}"
    
    print(f"  {old_vpc:04x}: {hexbytes:16s} {cn:12s} {changes}")
    
    # Stop at failure jump
    if case in (0xf, 0x10) and vpc == 0x0254:
        print(f"  *** JUMP TO FAILURE at vpc=0x0254 ***")
        break
