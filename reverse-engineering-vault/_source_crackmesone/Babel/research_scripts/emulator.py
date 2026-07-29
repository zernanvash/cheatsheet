#!/usr/bin/env python3
"""Full emulation and keygen derivation for babel_vm.exe"""

# After thorough analysis of the decompiled code, here's the architecture:
#
# === ARCHITECTURE OVERVIEW ===
# 
# 1. Input: username (4-64 chars), serial (XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX)
#    Serial: 8 groups of 4 hex chars = 8 x 16-bit values = serial[0..7]
#
# 2. The main function is a STATE MACHINE (not a traditional loop), driven by
#    state variable iVar21 through these stages:
#
#    State 0xA7: Validate username length (4-64), init flags
#    State 0x21: CRC32 of serial string, then Murmur-like hash of username  
#    State 0x3C: Same Murmur hash (shared path)
#    State 0x5E: Decrypt 4 bytecode programs using XOR keys, compute CRC32 checksum
#    State 0x12: Set up primary VM context (registers, stack, etc.)
#    State 0xF1: Execute primary VM bytecode
#    State 0xE1: Dummy/trap operations (deceptive)
#    State 0xD3: Post-execution, check modexp parity constraint
#    State 0x99: Final verification - XOR checksum, CRC16 checksum
#
# 3. Two VM layers:
#    - Primary Register VM: 8 registers (r0-r7), VPC, flag, accumulator, output regs
#    - Secondary Stack VMs: 3 different programs invoked from primary VM
#
# === KEY DERIVATION ===
#
# From username:
#   hash_lo = murmur_like_hash(username) & 0xffff  (stored in local_8a8 low 16 bits)
#   hash_hi = (murmur_hash ^ murmur_hash >> 16) or 0x42424242 if zero result
#   serial_crc32 = crc32(serial_string)  
#
# Source registers for VM (sreg_file):
#   sreg[0] = hash_lo (lower 16 bits of username hash)
#   sreg[1] = hash_hi (upper 16 bits, set in state 0x99 after modexp)
#   sreg[2..9] = serial[0..7]  (the 8 serial groups as 16-bit values)
#
# The VM computes various checks on these values. If all pass, "Access Granted".
#
# Let me trace through the primary VM to extract the constraints:

def murmur_hash(username):
    """Murmur-like hash of username, as in the binary."""
    h = 0x42414245  # 'BABE'
    length = len(username)
    for i in range(length):
        byte_val = username[i] if isinstance(username[i], int) else ord(username[i])
        shift = (i & 3) << 3
        h ^= (byte_val << shift)
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 0x5bd1e995) & 0xFFFFFFFF
        h ^= (h >> 15)
    
    h = ((h ^ length) * 0xcc9e2d51) & 0xFFFFFFFF  # -0x3361d2af = 0xcc9e2d51
    
    if (h - (h >> 16)) & 0xFFFFFFFF == 0:
        result = 0x42424242
    else:
        result = h ^ (h >> 16)
    
    return result & 0xFFFFFFFF

def crc32_bytes(data):
    """CRC32 as implemented in the binary."""
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (-(crc & 1) & 0xEDB88320)
            crc &= 0xFFFFFFFF
    return (~crc) & 0xFFFFFFFF

def crc16(value):
    """CRC16 as implemented in the binary (16-bit, poly 0xA001)."""
    for _ in range(16):
        value = ((value >> 1) ^ (-(value & 1) & 0xA001)) & 0xFFFF
    return value

def lfsr_step(val):
    """LFSR step: case 0x27 in primary VM."""
    val &= 0xFFFF
    result = (val >> 1) & 0x7FFF
    result ^= (-(val & 1) & 0xB400)
    return result

# ============================================================
# Now let me trace the primary VM bytecode to extract constraints.
# The VM has:
#   r0-r7: general registers (32-bit but &0xffff often)
#   sreg[0..9]: source registers (read-only from VM perspective)
#   out[0..7]: output registers
#   flag: comparison flag
#   acc: accumulator
#   iter_counter: iteration counter
#
# sreg layout:
#   sreg[0] = hash_lo = username_hash & 0xFFFF
#   sreg[1] = hash_hi = username_hash >> 16
#   sreg[2] = serial[0]
#   sreg[3] = serial[1]
#   sreg[4] = serial[2]
#   sreg[5] = serial[3]
#   sreg[6] = serial[4]
#   sreg[7] = serial[5]
#   sreg[8] = serial[6]
#   sreg[9] = serial[7]
#
# The "LOAD_SREG r, idx" instruction: reg[r] = sreg[idx]
# But looking at the bytecode, I see "LOAD_SREG r0, r1" which is case 2
# In case 2: reg[op1] = local_12c[op2] where local_12c holds the sreg file
# So the second operand is an index into the sreg array, not a register.

# Let me re-read specific parts of the VM trace and build the constraint equations.

# From the disassembly, here's the VM logic (simplified):
# All arithmetic is mod 0x10000 (16-bit) due to AND_IMM r, 0xffff masks

# Symbols:
#   H0 = hash_lo (sreg[0])
#   H1 = hash_hi (sreg[1])  
#   S0..S7 = serial[0..7] (sreg[2..9])

# Block 1 (offset 0x0000-0x007e): Check serial[0]
# r7 = 0xDEAD
# r0 = H0 ^ H1 (from LOAD_SREG and operations)
# Check: result == S0
# ... (complex chain of operations)

# Actually, let me just write a full VM emulator to extract constraints symbolically.
# That's the most reliable approach.

# First, let me create a concrete emulator to verify with known values,
# then derive the inverse.

class PrimaryVM:
    def __init__(self, bytecode, sregs):
        self.bc = bytecode
        self.regs = [0] * 8       # r0-r7
        self.sregs = sregs         # source register file (10 entries)
        self.out = [0] * 8         # output registers
        self.flag = 0              # comparison flag
        self.acc = 0               # accumulator (local_58 = 0xDEAD initially)
        self.vpc = 0               # virtual program counter
        self.vstack = []           # virtual stack
        self.vsp = -1              # virtual stack pointer (starts at -1 = 0xffffffff)
        self.call_stack = []       # call stack
        self.csp = -1              # call stack pointer
        self.halt = False
        self.iter_counter = 0      # iteration counter (uStack_54)
        
        # Inner VM bytecodes (decrypted)
        self.inner_vms = []
        
    def set_inner_vms(self, vms):
        self.inner_vms = vms
    
    def run(self, max_steps=100000):
        step = 0
        while not self.halt and step < max_steps:
            if self.vpc >= len(self.bc):
                break
            self._step()
            step += 1
            self.iter_counter += 1
        return self.out
    
    def _read_byte(self, offset):
        if offset < len(self.bc):
            return self.bc[offset]
        return 0
    
    def _step(self):
        # Opcode dispatch table
        opcode_table = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")
        
        raw = self._read_byte(self.vpc)
        if raw >= len(opcode_table):
            self.halt = True
            return
        
        case = opcode_table[raw]
        
        op1 = self._read_byte(self.vpc + 1)
        op2 = self._read_byte(self.vpc + 2)
        op3 = self._read_byte(self.vpc + 3)
        imm16 = (op3 << 8) | op2
        
        if case == 0:  # NOP
            self.vpc += 1
        elif case == 1:  # LOAD_IMM reg, imm16
            self.regs[op1] = imm16
            self.vpc += 4
        elif case == 2:  # LOAD_SREG reg, idx
            self.regs[op1] = self.sregs[op2] if op2 < len(self.sregs) else 0
            self.vpc += 3
        elif case == 3:  # MOV dst, src
            # From decompiled: reg[op1] = reg[op2 (via or logic)]
            # Actually the decompiled shows: reg[op1|op2] = reg[op2]
            # But that makes no sense. Let me re-check.
            # case 3: bVar18 = op1; bVar8 = op2; bVar18 = bVar18 | bVar8
            # reg[op1] = reg[bVar18]
            # So: reg[op1] = reg[op1 | op2]
            # Actually NO. Looking again at the decompiled:
            # (local_554)[pFVar24] = (local_554)[bVar8]
            # where pFVar24 = op1, bVar8 = op1 | op2 (wait)
            # bVar18 = op1; bVar8 = op2; bVar18 = bVar18 | bVar8
            # reg[pFVar24] = reg[bVar18] 
            # where pFVar24 is original op1 (before OR), bVar18 is op1 | op2
            # Hmm, that's a weird encoding. For MOV: reg[op1] = reg[op1|op2]
            # But typical usage: if op1=0, op2=5 => reg[0] = reg[5]
            # If op1=1, op2=2 => reg[1] = reg[3]?? That's weird.
            # Let me look at the actual bytecode: all MOV-like ops seem to have
            # operands where one is 0xff (like 03 00 ff ff which I parsed as AND_IMM)
            # Let me check: raw_byte 0x06 -> case 3
            # In the disassembly I don't see raw byte 0x06 much...
            # Actually raw 0x06 = case 3. In bytecode the AND_IMM raw byte would be 
            # different. Let me re-map.
            
            # OK I think the OR of op1|op2 is a validation check - if result > 7, 
            # it fails. This is just ensuring both are valid register indices.
            # The actual semantics: reg[op1_original] = reg[op2]
            # Because pFVar24 stores the original op1 before the OR.
            # Wait no: pFVar24 = (FILE *)(ulonglong)bVar18 is set BEFORE the OR, 
            # to original op1 value. Then bVar8 is op2. Then bVar18 = bVar18 | bVar8
            # used only for validation (if > 7, fail).
            # So reg[original_op1] = reg[op2]
            # Wait that doesn't match either. Let me look more carefully:
            # (local_554)[(longlong)pFVar24] = (local_554)[bVar8];
            # pFVar24 = original bVar18 = op1
            # bVar8 = op1 | op2 -- NO!
            # Actually:
            # bVar18 = bytecode[vpc+1]  (= op1)
            # pFVar24 = bVar18  (saved)
            # bVar8 = bytecode[vpc+2]  (= op2)
            # bVar18 = bVar18 | bVar8  (validation)
            # reg[pFVar24] = reg[bVar8]
            # So: reg[op1] = reg[op2]  !!!  Simple MOV!
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
        elif case == 0xa:  # SHL
            self.regs[op1] = (self.regs[op1] << (op2 & 0x1f)) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0xb:  # SHR
            self.regs[op1] = (self.regs[op1] >> (op2 & 0x1f)) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0xc:  # NOT
            self.regs[op1] = (~self.regs[op1]) & 0xFFFFFFFF
            self.vpc += 2
        elif case == 0xd:  # CMP
            self.flag = 1 if self.regs[op1] == self.regs[op2] else 0
            self.vpc += 3
        elif case == 0xe:  # JMP
            self.vpc = (op2 << 8) | op1
        elif case == 0xf:  # JNZ
            target = (op2 << 8) | op1
            if self.flag != 0:
                self.vpc = target
            else:
                self.vpc += 3
        elif case == 0x10:  # JZ
            target = (op2 << 8) | op1
            if self.flag == 0:
                self.vpc = target
            else:
                self.vpc += 3
        elif case == 0x11:  # PUSH
            self.vsp += 1
            if self.vsp < 256:
                while len(self.vstack) <= self.vsp:
                    self.vstack.append(0)
                self.vstack[self.vsp] = self.regs[op1]
            self.vpc += 2
        elif case == 0x12:  # POP
            if self.vsp >= 0:
                self.regs[op1] = self.vstack[self.vsp]
                self.vsp -= 1
            self.vpc += 2
        elif case == 0x13:  # STORE_OUT
            self.out[op1] = self.regs[op2]
            self.vpc += 3
        elif case == 0x14:  # HALT
            self.halt = True
            self.vpc += 1
        elif case == 0x15:  # ADD_IMM
            self.regs[op1] = (self.regs[op1] + imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x16:  # CMP_IMM
            self.flag = 1 if self.regs[op1] == imm16 else 0
            self.vpc += 4
        elif case == 0x17:  # AND_IMM
            self.regs[op1] &= imm16
            self.vpc += 4
        elif case == 0x18:  # ROL
            shift = op2 & 0x1f
            val = self.regs[op1] & 0xFFFFFFFF
            self.regs[op1] = ((val << shift) | (val >> (32 - shift))) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0x19:  # ROR
            shift = op2 & 0x1f
            val = self.regs[op1] & 0xFFFFFFFF
            self.regs[op1] = ((val >> shift) | (val << (32 - shift))) & 0xFFFFFFFF
            self.vpc += 3
        elif case == 0x1a:  # CALL
            target = (op2 << 8) | op1
            self.csp += 1
            while len(self.call_stack) <= self.csp:
                self.call_stack.append(0)
            self.call_stack[self.csp] = self.vpc + 3
            self.vpc = target
        elif case == 0x1b:  # RET
            if self.csp >= 0:
                self.vpc = self.call_stack[self.csp]
                self.csp -= 1
            else:
                self.halt = True
        elif case == 0x1c:  # MUL_IMM
            self.regs[op1] = (self.regs[op1] * imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x1d:  # CMP_IMM with imm16 
            self.flag = 1 if self.regs[op1] == imm16 else 0
            self.vpc += 4
        elif case == 0x1e:  # SUB_IMM
            self.regs[op1] = (self.regs[op1] - imm16) & 0xFFFFFFFF
            self.vpc += 4
        elif case == 0x1f:  # SWAP
            self.regs[op1], self.regs[op2] = self.regs[op2], self.regs[op1]
            self.vpc += 3
        elif case == 0x20:  # INVOKE_VM2
            which = op1
            result = self._run_inner_vm(which)
            self.regs[0] = result
            self.vpc += 2
        elif case == 0x21:  # STORE_BC
            offset = (op2 << 8) | op1
            if offset < len(self.bc):
                self.bc[offset] = self.regs[op3] & 0xFF
            self.vpc += 4
        elif case == 0x22:  # LOAD_ITER
            self.regs[op1] = self.iter_counter
            self.vpc += 2
        elif case == 0x23:  # OR_IMM
            self.regs[op1] |= imm16
            self.vpc += 4
        elif case == 0x24:  # CRC16
            val = self.regs[op1] ^ self.regs[op2]
            for _ in range(16):
                val = ((val >> 1) ^ (-(val & 1) & 0xA001)) & 0xFFFF
            self.regs[op1] = val & 0xFFFF
            self.vpc += 3
        elif case == 0x25:  # LOAD_ACC
            self.regs[op1] = self.acc
            self.vpc += 2
        elif case == 0x26:  # STORE_ACC
            self.regs[op1] = self.regs[op1]  # already in regs
            self.acc = self.regs[op1]
            self.vpc += 2
        elif case == 0x27:  # LFSR
            val = self.regs[op1] & 0xFFFF
            result = (val >> 1) & 0x7FFF
            result ^= (-(val & 1) & 0xB400)
            self.regs[op1] = result
            self.vpc += 2
        else:
            self.halt = True
    
    def _run_inner_vm(self, which):
        """Execute a secondary stack VM."""
        if which >= len(self.inner_vms):
            return 0
        
        vm_info = self.inner_vms[which]
        bc = vm_info['bytecode']
        src_regs = vm_info['src_regs']  # list of uint values
        num_src = vm_info['num_src']
        max_len = vm_info['max_len']
        
        stack = []
        sp = -1  # 0xffffffff initially in binary
        pc = 0
        count = 0
        result = -1  # -1 = running, 0 = false, 1 = true
        
        while count < 4096 and pc < max_len:
            raw = bc[pc]
            opcode = raw - 1
            count += 1
            
            if opcode > 0x16:
                result = -1
                break
            
            if opcode == 0:  # PUSH_REG
                if pc + 1 >= max_len:
                    break
                idx = bc[pc + 1]
                if sp >= 0x7f or idx >= num_src:
                    break
                sp += 1
                while len(stack) <= sp:
                    stack.append(0)
                stack[sp] = src_regs[idx] & 0xFFFFFFFF
                pc += 2
                
            elif opcode == 1:  # PUSH_IMM16
                if pc + 2 >= max_len:
                    break
                lo = bc[pc + 1]
                hi = bc[pc + 2]
                imm = (hi << 8) | lo
                if sp >= 0x7f:
                    break
                sp += 1
                while len(stack) <= sp:
                    stack.append(0)
                stack[sp] = imm
                pc += 3
            
            elif opcode == 2:  # ADD
                if sp < 1:
                    break
                stack[sp - 1] = (stack[sp - 1] + stack[sp]) & 0xFFFFFFFF
                sp -= 1
                pc += 1
            
            elif opcode == 3:  # SUB
                if sp < 1:
                    break
                stack[sp - 1] = (stack[sp - 1] - stack[sp]) & 0xFFFFFFFF
                sp -= 1
                pc += 1
            
            elif opcode == 4:  # MUL
                if sp < 1:
                    break
                stack[sp - 1] = (stack[sp] * stack[sp - 1]) & 0xFFFFFFFF
                sp -= 1
                pc += 1
            
            elif opcode == 5:  # XOR
                if sp < 1:
                    break
                stack[sp - 1] ^= stack[sp]
                sp -= 1
                pc += 1
            
            elif opcode == 6:  # AND
                if sp < 1:
                    break
                stack[sp - 1] &= stack[sp]
                sp -= 1
                pc += 1
            
            elif opcode == 7:  # OR
                if sp < 1:
                    break
                stack[sp - 1] |= stack[sp]
                sp -= 1
                pc += 1
            
            elif opcode == 8:  # ROL (16-bit rotate left)
                if sp < 1:
                    break
                shift_amt = stack[sp] & 0xf
                val = stack[sp - 1] & 0xFFFF
                rotated = ((val << shift_amt) | (val >> (16 - shift_amt))) & 0xFFFF
                sp -= 1
                stack[sp] = rotated
                pc += 1
            
            elif opcode == 9:  # ROR (16-bit rotate right)
                if sp < 1:
                    break
                shift_amt = stack[sp] & 0xf
                val = stack[sp - 1] & 0xFFFF
                rotated = ((val >> shift_amt) | (val << (16 - shift_amt))) & 0xFFFF
                sp -= 1
                stack[sp] = rotated
                pc += 1
            
            elif opcode == 0xa:  # EQ
                if sp < 1:
                    break
                stack[sp - 1] = 1 if stack[sp] == stack[sp - 1] else 0
                sp -= 1
                pc += 1
            
            elif opcode == 0xb:  # DUP
                if sp >= 0x7f:
                    break
                sp += 1
                while len(stack) <= sp:
                    stack.append(0)
                stack[sp] = stack[sp - 1]
                pc += 1
            
            elif opcode == 0xc:  # SWAP
                if sp < 1:
                    break
                stack[sp], stack[sp-1] = stack[sp-1], stack[sp]
                pc += 1
            
            elif opcode == 0xd:  # NOT16
                if sp < 0:
                    break
                stack[sp] = (~stack[sp]) & 0xFFFF
                pc += 1
            
            elif opcode == 0xe:  # TRUNC16
                if sp < 0:
                    break
                stack[sp] = stack[sp] & 0xFFFF
                pc += 1
            
            elif opcode == 0xf:  # DONE_TRUE
                result = 1
                break
            
            elif opcode == 0x10:  # DONE_FALSE
                result = 0
                break
            
            elif opcode == 0x11:  # JNZ
                if pc + 2 >= max_len or sp < 0:
                    break
                target = (bc[pc + 2] << 8) | bc[pc + 1]
                if stack[sp] != 0:
                    pc = target
                else:
                    pc += 3
                sp -= 1
            
            elif opcode == 0x12:  # JZ
                if pc + 2 >= max_len or sp < 0:
                    break
                target = (bc[pc + 2] << 8) | bc[pc + 1]
                if stack[sp] != 0:
                    pc += 3
                else:
                    pc = target
                sp -= 1
            
            elif opcode == 0x13:  # DROP
                if sp < 0:
                    break
                sp -= 1
                pc += 1
            
            elif opcode == 0x14:  # CRC16
                if sp < 1:
                    break
                val = stack[sp - 1] ^ stack[sp]
                for _ in range(16):
                    val = ((val >> 1) ^ (-(val & 1) & 0xA001)) & 0xFFFF
                stack[sp - 1] = val
                sp -= 1
                pc += 1
            
            elif opcode == 0x15:  # SHL
                if sp < 1:
                    break
                shift_amt = stack[sp] & 0xf
                stack[sp - 1] = (stack[sp - 1] << shift_amt) & 0xFFFF
                sp -= 1
                pc += 1
            
            elif opcode == 0x16:  # SHR
                if sp < 1:
                    break
                shift_amt = stack[sp] & 0xf
                stack[sp - 1] = (stack[sp - 1] >> shift_amt) & 0xFFFF
                sp -= 1
                pc += 1
            
            else:
                break
        
        return 1 if result == 1 else 0


def decrypt_bc(data, key, length):
    result = bytearray()
    for i in range(length):
        result.append(data[i] ^ key[i & 3])
    return result


def compute_serial(username):
    """Compute a valid serial for the given username."""
    # Step 1: Compute username hash
    h = murmur_hash(username)
    hash_lo = h & 0xFFFF
    hash_hi = (h >> 16) & 0xFFFF
    
    print(f"Username: {username}")
    print(f"Hash: 0x{h:08x}")
    print(f"hash_lo (H0 = sreg[0]): 0x{hash_lo:04x}")
    print(f"hash_hi (H1 = sreg[1]): 0x{hash_hi:04x}")
    
    # Step 2: Brute-force approach using the VM emulator
    # We need to find S0..S7 such that the VM outputs out[0]=1
    # 
    # From the VM trace, the constraints are sequential:
    # Each serial word is computed from the previous ones and the hash.
    # Let me trace the VM to extract each constraint forward:
    
    # I'll trace step by step through the bytecodes to derive each serial word.
    # Looking at the disassembly, the pattern is:
    #   Compute expected value for serial[i] from hash + previous serials
    #   Compare with actual serial[i]
    #   If mismatch, jump to failure (0x0254)
    
    # Let me trace through manually to extract the constraint for each S[i]:
    
    # === Constraint 1: S0 ===
    # 0x0000: LOAD_IMM r7, 0xDEAD     ; r7 = 0xDEAD (running checksum)
    # 0x0004: LOAD_SREG r7, r5        ; Wait, this is wrong mapping
    # Actually looking at the hex: 02 07 27 05
    # raw 0x02 -> case 0x26 = STORE_ACC => STORE_ACC r7
    # raw 0x27 -> case 0x01 = LOAD_IMM => LOAD_IMM r5, ...
    # Let me re-check my opcode table mapping!
    
    # opcode_table[0x27] = 0x01 = LOAD_IMM
    # opcode_table[0x02] = 0x26 = STORE_ACC  (actually 38 = 0x26)
    # Wait: opcode_table hex = "071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01"
    # Index 2: 0x26 = 38... no that's 0x26 in hex not decimal
    # opcode_table[2] = 0x26 which in my case_names is STORE_ACC
    # But 0x26 in the case_names is... let me check: 0x26 = 38 decimal
    # I only defined cases up to 0x27 = 39
    
    # Actually case 0x26: STORE_ACC reg
    # ok that's right
    
    # So the bytecode starts:
    # 27 07 ad de -> LOAD_IMM r7, 0xDEAD  (raw 0x27 = case 1)
    # 02 07      -> STORE_ACC r7           (raw 0x02 = case 0x26)
    # 27 05 34 12 -> LOAD_IMM r5, 0x1234
    # 27 06 78 56 -> LOAD_IMM r6, 0x5678
    # 00 05 06   -> XOR r5, r6             (raw 0x00 = case 7)
    
    # Wait, case 7 = XOR? Let me recheck.
    # opcode_table[0x00] = 0x07. Case 0x07 = XOR. Yes!
    
    # Let me just run the emulator with known test values and check.
    # But I need to also handle CMP_IMM vs CMP properly.
    
    # Looking at my case mapping:
    # case 0x16 -> I mapped to CMP_IMM but in the switch statement,
    # case 0x15: ADD_IMM, case 0x16: XOR_IMM
    # Wait, these are DIFFERENT cases to the ones I listed.
    # Let me re-verify from the decompiled code:
    # case 0x15: reg[op1] += imm16  -> ADD_IMM
    # case 0x16: reg[op1] ^= imm16 -> XOR_IMM
    # case 0x17: reg[op1] &= imm16 -> AND_IMM
    # case 0x1d: flag = reg[op1] == imm16 -> CMP_IMM
    
    # In my _step, I have case 0x16 mapped to CMP_IMM - that's WRONG!
    # Let me check: At line "elif case == 0x16:  # CMP_IMM"
    # But case 0x16 should be XOR_IMM from the decompiled code!
    # I think I have a bug in my emulator. Let me fix and re-verify.
    
    # Actually looking at my emulator code more carefully, I see I have BOTH
    # case 0x16 as CMP_IMM AND case 0x1d as CMP_IMM. That's wrong.
    # case 0x16 should be XOR_IMM.
    pass

# Quick test
username = "test"
h = murmur_hash(username)
print(f"murmur_hash('test') = 0x{h:08x}")

username = "admin"
h = murmur_hash(username)
print(f"murmur_hash('admin') = 0x{h:08x}")
