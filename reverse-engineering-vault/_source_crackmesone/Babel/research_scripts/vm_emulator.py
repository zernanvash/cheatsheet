#!/usr/bin/env python3
"""Full VM emulator for babel_vm.exe to trace and debug constraint equations."""

import subprocess

# ============================================================
# Crypto helpers
# ============================================================

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

def crc16(value):
    value &= 0xFFFF
    for _ in range(16):
        if value & 1:
            value = (value >> 1) ^ 0xA001
        else:
            value >>= 1
    return value & 0xFFFF

def decrypt_bc(data_hex, key_bytes, length):
    data = bytes.fromhex(data_hex)
    return bytearray(data[i] ^ key_bytes[i & 3] for i in range(length))

# ============================================================
# Primary VM Emulator
# ============================================================

class PrimaryVM:
    def __init__(self, bytecode, sregs):
        self.bc = bytearray(bytecode)
        self.regs = [0] * 8
        self.sregs = list(sregs)
        self.out = [0] * 8
        self.flag = 0
        self.acc = 0xDEAD
        self.vpc = 0
        self.vstack = [0] * 256
        self.vsp = -1
        self.call_stack = [0] * 32
        self.csp = -1
        self.halt = False
        self.iter_count = 0
        self.inner_vms = []
        
        self.opcode_table = bytes.fromhex(
            "071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01"
        )
        
        self.trace_enabled = False
    
    def set_inner_vms(self, vms):
        self.inner_vms = vms
    
    def run(self, max_steps=200000):
        step = 0
        while not self.halt and step < max_steps and self.vpc < len(self.bc):
            self._step()
            step += 1
            self.iter_count += 1
        return self.out
    
    def _step(self):
        raw = self.bc[self.vpc]
        if raw >= len(self.opcode_table):
            self.halt = True; return
        
        case = self.opcode_table[raw]
        op1 = self.bc[self.vpc+1] if self.vpc+1 < len(self.bc) else 0
        op2 = self.bc[self.vpc+2] if self.vpc+2 < len(self.bc) else 0
        op3 = self.bc[self.vpc+3] if self.vpc+3 < len(self.bc) else 0
        imm16 = (op3 << 8) | op2
        
        old_vpc = self.vpc
        
        if case == 0:    # NOP
            self.vpc += 1
        elif case == 1:  # LOAD_IMM reg, imm16
            self.regs[op1] = imm16
            self.vpc += 4
        elif case == 2:  # LOAD_SREG reg, idx
            self.regs[op1] = self.sregs[op2] if op2 < len(self.sregs) else 0
            self.vpc += 3
        elif case == 3:  # MOV dst, src (reg[op1] = reg[op2])
            # bVar18=op1, pFVar24=op1(saved), bVar8=op2, validation: op1|op2 <=7
            # reg[pFVar24] = reg[bVar8] => reg[op1] = reg[op2]
            # Wait, re-read: case 3 in decompiled:
            # bVar18 = bc[vpc+1]; pFVar24 = bVar18; bVar8 = bc[vpc+2]; 
            # bVar18 = bVar18|bVar8; if >7 fail;
            # reg[pFVar24] = reg[bVar8]  
            # So: reg[op1] = reg[op2]. BUT which is "op2"? 
            # In the code: (local_554)[(longlong)pFVar24] = (local_554)[bVar8]
            # pFVar24 = original op1, bVar8 = validataed combined value?
            # No: bVar8 is set to bc[vpc+2], then bVar18 = op1 | bVar8 for validation.
            # (local_554)[pFVar24] = (local_554)[bVar8] where bVar8 = bc[vpc+2]
            # WAIT. Let me re-read the decompiled code for case 3 very carefully:
            # bVar18 = bc[vpc+1]    // op1
            # pFVar24 = bVar18      // save op1  
            # bVar8 = bc[vpc+2]     // op2
            # bVar18 = bVar18 | bVar8  // validation only
            # if bVar18 > 7 goto fail
            # reg[pFVar24] = reg[bVar8]  // reg[op1] = reg[op2]
            # YES, it's reg[op1] = reg[op2]
            self.regs[op1] = self.regs[op2]
            self.vpc += 3
        elif case == 4:  # ADD
            self.regs[op1] = (self.regs[op1] + self.regs[op2]) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 5:  # SUB
            self.regs[op1] = (self.regs[op1] - self.regs[op2]) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 6:  # MUL
            self.regs[op1] = (self.regs[op1] * self.regs[op2]) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 7:  # XOR
            self.regs[op1] ^= self.regs[op2]
            self.vpc += 3
        elif case == 8:  # AND
            self.regs[op1] &= self.regs[op2]
            self.vpc += 3
        elif case == 9:  # OR
            self.regs[op1] |= self.regs[op2]
            self.vpc += 3
        elif case == 0xa: # SHL
            self.regs[op1] = (self.regs[op1] << (op2 & 0x1f)) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0xb: # SHR
            self.regs[op1] = (self.regs[op1] >> (op2 & 0x1f)) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0xc: # NOT
            self.regs[op1] = (~self.regs[op1]) & 0xFFFFFFFF
            self.vpc += 2
        elif case == 0xd: # CMP reg1, reg2
            self.flag = 1 if self.regs[op1] == self.regs[op2] else 0
            self.vpc += 3
        elif case == 0xe: # JMP
            self.vpc = (op2 << 8) | op1
        elif case == 0xf: # JNZ
            target = (op2 << 8) | op1
            if self.flag != 0:
                self.vpc = target
            else:
                self.vpc += 3
        elif case == 0x10: # JZ
            target = (op2 << 8) | op1
            if self.flag == 0:
                self.vpc = target
            else:
                self.vpc += 3
        elif case == 0x11: # PUSH
            self.vsp += 1
            if self.vsp < 256:
                self.vstack[self.vsp] = self.regs[op1]
            self.vpc += 2
        elif case == 0x12: # POP
            if self.vsp >= 0:
                self.regs[op1] = self.vstack[self.vsp]
                self.vsp -= 1
            self.vpc += 2
        elif case == 0x13: # STORE_OUT
            self.out[op1] = self.regs[op2]
            self.vpc += 3
        elif case == 0x14: # HALT
            self.halt = True
            self.vpc += 1
        elif case == 0x15: # ADD_IMM
            self.regs[op1] = (self.regs[op1] + imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x16: # XOR_IMM
            self.regs[op1] ^= imm16
            self.vpc += 4
        elif case == 0x17: # AND_IMM
            self.regs[op1] &= imm16
            self.vpc += 4
        elif case == 0x18: # ROL
            shift = op2 & 0x1f
            val = self.regs[op1] & 0xFFFFFFFF
            self.regs[op1] = ((val << shift) | (val >> (32 - shift))) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0x19: # ROR
            shift = op2 & 0x1f
            val = self.regs[op1] & 0xFFFFFFFF
            self.regs[op1] = ((val >> shift) | (val << (32 - shift))) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0x1a: # CALL
            target = (op2 << 8) | op1
            self.csp += 1
            self.call_stack[self.csp] = self.vpc + 3
            self.vpc = target
        elif case == 0x1b: # RET
            if self.csp >= 0:
                self.vpc = self.call_stack[self.csp]
                self.csp -= 1
            else:
                self.halt = True
        elif case == 0x1c: # MUL_IMM
            self.regs[op1] = (self.regs[op1] * imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x1d: # CMP_IMM
            self.flag = 1 if self.regs[op1] == imm16 else 0
            self.vpc += 4
        elif case == 0x1e: # SUB_IMM
            self.regs[op1] = (self.regs[op1] - imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x1f: # SWAP
            self.regs[op1], self.regs[op2] = self.regs[op2], self.regs[op1]
            self.vpc += 3
        elif case == 0x20: # INVOKE_VM2
            result = self._run_inner_vm(op1)
            self.regs[0] = result
            self.vpc += 2
        elif case == 0x21: # STORE_BC [offset], reg
            offset = (op2 << 8) | op1
            if offset < len(self.bc):
                self.bc[offset] = self.regs[op3] & 0xFF
            self.vpc += 4
        elif case == 0x22: # LOAD_ITER
            self.regs[op1] = self.iter_count
            self.vpc += 2
        elif case == 0x23: # OR_IMM
            self.regs[op1] |= imm16
            self.vpc += 4
        elif case == 0x24: # CRC16 reg1, reg2
            val = self.regs[op1] ^ self.regs[op2]
            val &= 0xFFFF
            for _ in range(16):
                if val & 1:
                    val = (val >> 1) ^ 0xA001
                else:
                    val >>= 1
            self.regs[op1] = val & 0xFFFF
            self.vpc += 3
        elif case == 0x25: # LOAD_ACC
            self.regs[op1] = self.acc
            self.vpc += 2
        elif case == 0x26: # STORE_ACC
            self.acc = self.regs[op1]
            self.vpc += 2
        elif case == 0x27: # LFSR
            val = self.regs[op1] & 0xFFFF
            if val & 1:
                result = ((val >> 1) ^ 0xB400) & 0xFFFF
            else:
                result = (val >> 1) & 0xFFFF
            self.regs[op1] = result
            self.vpc += 2
        else:
            self.halt = True
        
        if self.trace_enabled:
            case_names = {0:"NOP",1:"LOAD_IMM",2:"LOAD_SREG",3:"MOV",4:"ADD",5:"SUB",
                         6:"MUL",7:"XOR",8:"AND",9:"OR",0xa:"SHL",0xb:"SHR",0xc:"NOT",
                         0xd:"CMP",0xe:"JMP",0xf:"JNZ",0x10:"JZ",0x11:"PUSH",0x12:"POP",
                         0x13:"STORE_OUT",0x14:"HALT",0x15:"ADD_IMM",0x16:"XOR_IMM",
                         0x17:"AND_IMM",0x18:"ROL",0x19:"ROR",0x1a:"CALL",0x1b:"RET",
                         0x1c:"MUL_IMM",0x1d:"CMP_IMM",0x1e:"SUB_IMM",0x1f:"SWAP",
                         0x20:"INVOKE_VM2",0x21:"STORE_BC",0x22:"LOAD_ITER",0x23:"OR_IMM",
                         0x24:"CRC16",0x25:"LOAD_ACC",0x26:"STORE_ACC",0x27:"LFSR"}
            cn = case_names.get(case, f"?{case}")
            if case == 0xd:
                print(f"  VM[{old_vpc:04x}] {cn:12s} r{op1}({self.regs[op1]:08x}) r{op2}({self.regs[op2]:08x}) -> flag={self.flag}")
            elif case == 0x1d:
                print(f"  VM[{old_vpc:04x}] {cn:12s} r{op1}({self.regs[op1]:08x}) 0x{imm16:04x} -> flag={self.flag}")
            elif case == 0x20:
                print(f"  VM[{old_vpc:04x}] {cn:12s} #{op1} -> r0={self.regs[0]:08x}")
            elif case == 0x10 or case == 0xf:
                target = (op2 << 8) | op1
                print(f"  VM[{old_vpc:04x}] {cn:12s} 0x{target:04x}, flag={1 if case==0xf else 0}, vpc->{self.vpc:04x}")
    
    def _run_inner_vm(self, which):
        if which >= len(self.inner_vms):
            return 0
        
        vm = self.inner_vms[which]
        bc = vm['bytecode']
        src = vm['src_regs_fn'](self.regs, self.sregs, self.out)
        num = vm['num_src']
        maxlen = vm['max_len']
        
        stack = [0] * 128
        sp = -1
        pc = 0
        count = 0
        
        while count < 4096 and pc < maxlen:
            raw = bc[pc]
            op = raw - 1
            count += 1
            
            if op > 0x16 or op < 0:
                return 0
            
            if op == 0:  # PUSH_REG
                idx = bc[pc+1]
                if sp >= 0x7f or idx >= num:
                    return 0
                sp += 1
                stack[sp] = src[idx] & 0xFFFFFFFF
                pc += 2
            elif op == 1:  # PUSH_IMM16
                imm = (bc[pc+2] << 8) | bc[pc+1]
                if sp >= 0x7f:
                    return 0
                sp += 1
                stack[sp] = imm
                pc += 3
            elif op == 2:  # ADD
                if sp < 1: return 0
                stack[sp-1] = (stack[sp-1] + stack[sp]) & 0xFFFFFFFF
                sp -= 1; pc += 1
            elif op == 3:  # SUB
                if sp < 1: return 0
                stack[sp-1] = (stack[sp-1] - stack[sp]) & 0xFFFFFFFF
                sp -= 1; pc += 1
            elif op == 4:  # MUL
                if sp < 1: return 0
                stack[sp-1] = (stack[sp] * stack[sp-1]) & 0xFFFFFFFF
                sp -= 1; pc += 1
            elif op == 5:  # XOR
                if sp < 1: return 0
                stack[sp-1] ^= stack[sp]
                sp -= 1; pc += 1
            elif op == 6:  # AND
                if sp < 1: return 0
                stack[sp-1] &= stack[sp]
                sp -= 1; pc += 1
            elif op == 7:  # OR
                if sp < 1: return 0
                stack[sp-1] |= stack[sp]
                sp -= 1; pc += 1
            elif op == 8:  # ROL16
                if sp < 1: return 0
                shift = stack[sp] & 0xf
                val = stack[sp-1] & 0xFFFF
                stack[sp-1] = ((val << shift) | (val >> (16 - shift))) & 0xFFFF
                sp -= 1; pc += 1
            elif op == 9:  # ROR16
                if sp < 1: return 0
                shift = stack[sp] & 0xf
                val = stack[sp-1] & 0xFFFF
                stack[sp-1] = ((val >> shift) | (val << (16 - shift))) & 0xFFFF
                sp -= 1; pc += 1
            elif op == 0xa:  # EQ
                if sp < 1: return 0
                stack[sp-1] = 1 if stack[sp] == stack[sp-1] else 0
                sp -= 1; pc += 1
            elif op == 0xb:  # DUP
                if sp >= 0x7f: return 0
                sp += 1; stack[sp] = stack[sp-1]; pc += 1
            elif op == 0xc:  # SWAP
                if sp < 1: return 0
                stack[sp], stack[sp-1] = stack[sp-1], stack[sp]; pc += 1
            elif op == 0xd:  # NOT16
                if sp < 0: return 0
                stack[sp] = (~stack[sp]) & 0xFFFF; pc += 1
            elif op == 0xe:  # TRUNC16
                if sp < 0: return 0
                stack[sp] = stack[sp] & 0xFFFF; pc += 1
            elif op == 0xf:  # DONE_TRUE
                return 1
            elif op == 0x10: # DONE_FALSE
                return 0
            elif op == 0x11: # JNZ
                if sp < 0: return 0
                target = (bc[pc+2] << 8) | bc[pc+1]
                val = stack[sp]; sp -= 1
                if val != 0:
                    pc = target
                else:
                    pc += 3
            elif op == 0x12: # JZ
                if sp < 0: return 0
                target = (bc[pc+2] << 8) | bc[pc+1]
                val = stack[sp]; sp -= 1
                if val == 0:
                    pc = target
                else:
                    pc += 3
            elif op == 0x13: # DROP
                if sp < 0: return 0
                sp -= 1; pc += 1
            elif op == 0x14: # CRC16
                if sp < 1: return 0
                v = stack[sp-1] ^ stack[sp]
                v &= 0xFFFF
                for _ in range(16):
                    if v & 1: v = (v >> 1) ^ 0xA001
                    else: v >>= 1
                stack[sp-1] = v & 0xFFFF
                sp -= 1; pc += 1
            elif op == 0x15: # SHL16
                if sp < 1: return 0
                shift = stack[sp] & 0xf
                stack[sp-1] = (stack[sp-1] << shift) & 0xFFFF
                sp -= 1; pc += 1
            elif op == 0x16: # SHR16
                if sp < 1: return 0
                shift = stack[sp] & 0xf
                stack[sp-1] = (stack[sp-1] >> shift) & 0xFFFF
                sp -= 1; pc += 1
            else:
                return 0
        
        return 0

# ============================================================
# Run test
# ============================================================

username = "test"
h = murmur_hash(username)
H0 = h & 0xFFFF
H1 = (h >> 16) & 0xFFFF
print(f"Username: {username}, Hash: 0x{h:08x}, H0=0x{H0:04x}, H1=0x{H1:04x}")

# Test serial
S = [0x247E, 0x322B, 0x4819, 0xE41F, 0xF52A, 0x718B, 0x670A, 0x2D42]

# Source registers
sregs = [H0, H1] + S

# Decrypt main bytecode
main_bc = decrypt_bc(
    "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000",
    [0x5A, 0x1C, 0xBE, 0xB4], 0x263
)

# Inner VMs
bc_vm2_0 = decrypt_bc("DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF",
                       [0xDE, 0xAD, 0xBE, 0xEF], 0x21)
bc_vm2_1 = decrypt_bc("CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB",
                       [0xCA, 0xFE, 0xBA, 0xBE], 0x27)
bc_vm2_2 = decrypt_bc("1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02",
                       [0x13, 0x37, 0xC0, 0xDE], 0x29)

# Source reg builders for inner VMs:
# VM2 #0 (bVar18==0): [H0,H1,S0,S1,S3,S5] - 6 regs, maxlen=0x21
# local_b58 = CONCAT44(local_12c[1], local_12c[0]) -> [H0, H1]  (idx 0,1)
# uStack_b50 = CONCAT44(local_12c[3], local_12c[2]) -> [S0, S1]  (idx 2,3)
# local_b48 = CONCAT44(local_110, local_118)
#   For bVar18==0: only local_b48 is set (not b40, b38)
#   = [local_118, local_110] = [S3, S5]  (idx 4,5)

def vm2_0_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[5], sregs[7]]
    # H0, H1, S0, S1, S3, S5

# VM2 #1 (bVar18==1): [H0,H1,S0,S1,S2,S3,S4,S5,S6] - 9 regs, maxlen=0x27
# local_b48 = CONCAT44(local_118, local_11c) -> [S2, S3]
# uStack_b40 = CONCAT44(local_110, local_114) -> [S4, S5]
# local_b38 = CONCAT44(local_b38._4_4_, local_10c) -> [S6, ?]
# Wait, let me re-read the decompiled code for bVar18==1:
#   local_b90 = 9
#   local_b38 = CONCAT44(local_b38._4_4_, local_10c)
#   local_b48 = CONCAT44(local_118, local_11c)
#   uStack_b40 = CONCAT44(local_110, local_114)
# Note local_b38._4_4_ is set from the PREVIOUS assignment before the switch.
# Before bVar18 check: local_b58 and uStack_b50 are always [H0,H1,S0,S1].
# Then for bVar18==1:
#   idx 4 = local_11c = S2
#   idx 5 = local_118 = S3  
#   idx 6 = local_114 = S4
#   idx 7 = local_110 = S5
#   idx 8 = local_10c = S6

def vm2_1_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[4], sregs[5], sregs[6], sregs[7], sregs[8]]
    # H0, H1, S0, S1, S2, S3, S4, S5, S6

# VM2 #2 (bVar18==2): [H0,H1,S0,S1,S2,S3,S4,S5,S6,S7] - 10 regs, maxlen=0x29
# local_b38 = CONCAT44(uStack_108, local_10c) -> [S6, S7]
# local_b48 = CONCAT44(local_118, local_11c) -> [S2, S3]
# uStack_b40 = CONCAT44(local_110, local_114) -> [S4, S5]

def vm2_2_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[4], sregs[5], sregs[6], sregs[7], sregs[8], sregs[9]]

inner_vms = [
    {'bytecode': bc_vm2_0, 'src_regs_fn': vm2_0_src, 'num_src': 6, 'max_len': 0x21},
    {'bytecode': bc_vm2_1, 'src_regs_fn': vm2_1_src, 'num_src': 9, 'max_len': 0x27},
    {'bytecode': bc_vm2_2, 'src_regs_fn': vm2_2_src, 'num_src': 10, 'max_len': 0x29},
]

vm = PrimaryVM(main_bc, sregs)
vm.set_inner_vms(inner_vms)
vm.trace_enabled = True

print("\n--- Running VM with trace ---")
result = vm.run()
print(f"\nVM finished. out[0]={result[0]}, out[1]=0x{result[1]:08x}")
print(f"Halt={vm.halt}, VPC=0x{vm.vpc:04x}")

# Now let's brute-force one word at a time using the emulator
# to find where our constraints diverge

print("\n\n--- Constraint verification by brute-force search ---")

# Test S0 independently 
def test_s0():
    for s0 in range(0x10000):
        S_test = [s0, 0, 0, 0, 0, 0, 0, 0]
        sr = [H0, H1] + S_test
        v = PrimaryVM(bytearray(main_bc), sr)
        v.set_inner_vms(inner_vms)
        # Run just until the first CMP (or a few hundred steps)
        for _ in range(200):
            if v.halt or v.vpc >= len(v.bc):
                break
            # Check if we hit the first CMP at 0x003d offset
            raw = v.bc[v.vpc]
            case = v.opcode_table[raw] if raw < len(v.opcode_table) else 99
            if case == 0xd and v.vpc > 0x30:  # First CMP reg,reg
                # Check what would happen
                op1 = v.bc[v.vpc+1]
                op2 = v.bc[v.vpc+2]
                if v.regs[op1] == v.regs[op2]:
                    print(f"  S0 found by brute force: 0x{s0:04x}")
                    return s0
                break
            v._step()
            v.iter_count += 1
    print("  S0 brute force failed!")
    return None

expected_s0 = (((H0 ^ H1) * 0x4E6B) + (H0 * 0x1337)) & 0xFFFF
print(f"  Computed S0: 0x{expected_s0:04x}")

# Run the VM step by step up to first CMP and print register state
print("\n--- Step-by-step trace to first CMP ---")
v2 = PrimaryVM(bytearray(main_bc), [H0, H1, expected_s0, 0, 0, 0, 0, 0, 0, 0])
v2.set_inner_vms(inner_vms)
v2.trace_enabled = True
v2.run(max_steps=500)
