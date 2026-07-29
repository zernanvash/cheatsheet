#!/usr/bin/env python3
"""
BABEL_VM Keygen - CrackMe by w33d
Reverse-engineered from babel_vm.exe

Architecture: Multi-layer VM with register-based primary VM and stack-based secondary VMs.
The constraints on serial words are computed sequentially from the username hash.
"""

import sys

# ============================================================
# Helper functions (matching binary implementations)
# ============================================================

def murmur_hash(username):
    """Murmur-like hash of username string. seed = 0x42414245 ('BABE')."""
    h = 0x42414245
    data = username.encode('ascii') if isinstance(username, str) else username
    length = len(data)
    
    for i in range(length):
        shift = (i & 3) << 3
        h ^= (data[i] << shift)
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 0x5bd1e995) & 0xFFFFFFFF
        h ^= (h >> 15)
    
    h = ((h ^ length) * 0xCC9E2D51) & 0xFFFFFFFF  # 0xCC9E2D51 = -0x3361D2AF mod 2^32
    
    if ((h - (h >> 16)) & 0xFFFFFFFF) == 0:
        return 0x42424242
    else:
        return (h ^ (h >> 16)) & 0xFFFFFFFF

def crc16(value):
    """CRC16 with polynomial 0xA001 (reflected CRC-16/ARC)."""
    value &= 0xFFFF
    for _ in range(16):
        if value & 1:
            value = (value >> 1) ^ 0xA001
        else:
            value >>= 1
    return value & 0xFFFF

def lfsr_step(val):
    """LFSR step with taps 0xB400."""
    val &= 0xFFFF
    if val & 1:
        return ((val >> 1) ^ 0xB400) & 0xFFFF
    else:
        return (val >> 1) & 0xFFFF

# ============================================================
# Constraint extraction from VM bytecode trace
# ============================================================
# 
# Register file layout:
#   sreg[0] = H0 = hash & 0xFFFF
#   sreg[1] = H1 = (hash >> 16) & 0xFFFF
#   sreg[2..9] = S0..S7 (serial words, each 16-bit)
#
# The VM processes 8 constraints sequentially. If all pass → "Access Granted"
# r7 tracks a running XOR checksum. acc tracks another running value.
#
# I'll trace each constraint block from the disassembly to compute S0..S7.

def compute_serial(username):
    """Compute valid serial for the given username."""
    h = murmur_hash(username)
    H0 = h & 0xFFFF           # sreg[0]
    H1 = (h >> 16) & 0xFFFF   # sreg[1]
    
    # Initial state
    r7 = 0xDEAD   # running XOR checksum
    acc = 0xDEAD  # accumulator (local_58 initialized to 0xDEAD)
    
    # ============================================================
    # Block 1: Compute S0  (offset 0x000a - 0x003d)
    # ============================================================
    # r5 = 0x1234, r6 = 0x5678
    # r5 ^= r6  => r5 = 0x1234 ^ 0x5678 = 0x444C
    # NOT r5    => r5 = ~0x444C = 0xFFFFBBB3
    # AND r5, 0xFFFF => r5 = 0xBBB3
    # ADD_IMM r5, 0x0001 => r5 = 0xBBB4  (this is just -(0x444C) = 0xBBB4)
    # AND r5, 0xFFFF => r5 = 0xBBB4
    # CMP_IMM r5, 0x0000 => flag = (0xBBB4 == 0) = 0
    # JZ 0x0254 => flag==0, so NO jump (this is an integrity check, always passes)
    
    # (Skip the trap: it just verifies 0x1234 ^ 0x5678 + 1 != 0, which is always true)
    
    # Actual S0 computation:
    # r0 = sreg[0] = H0
    # r1 = sreg[1] = H1  
    # r0 ^= r1   => r0 = H0 ^ H1
    # MUL_IMM r0, 0x4E6B => r0 = (H0^H1) * 0x4E6B
    # r1 = sreg[0] = H0
    # MUL_IMM r1, 0x1337 => r1 = H0 * 0x1337
    # ADD r0, r1 => r0 += r1
    # AND r0, 0xFFFF => r0 &= 0xFFFF
    # r1 = sreg[2] = S0
    # CMP r0, r1 => flag = (r0 == S0)
    # JZ 0x0254 => if flag==0, jump to fail
    
    S0 = (((H0 ^ H1) * 0x4E6B) + (H0 * 0x1337)) & 0xFFFF
    
    # After successful check:
    # r7 ^= r1 (= S0)
    r7 ^= S0
    # LOAD_ACC r4 => r4 = acc (= 0xDEAD)
    r4 = acc
    # XOR r4, r1 => r4 ^= S0
    r4 ^= S0
    # ROR r4, 5 => rotate right 32-bit by 5
    r4 &= 0xFFFFFFFF
    r4 = ((r4 >> 5) | (r4 << 27)) & 0xFFFFFFFF
    # STORE_ACC r4
    acc = r4
    
    # ============================================================
    # Block 2: Compute S1  (offset ~0x0082 - 0x00C1)
    # ============================================================
    # Trap code: r3 = 0xFACE * 0x0B0B = some value (ignored, NOP follows)
    # 
    # r0 = sreg[1] = H1
    # MUL_IMM r0, 0x4E6B => r0 = H1 * 0x4E6B
    # r1 = sreg[0] = H0
    # MUL_IMM r1, 0x1337 => r1 = H0 * 0x1337
    # ADD r0, r1 => r0 += r1
    # r2 = sreg[0] = H0
    # r3 = sreg[1] = H1
    # XOR r2, r3 => r2 = H0 ^ H1
    # AND r2, 0xFFFF
    # ROL r2, 7 => r2 = rotl32(H0^H1, 7)
    # AND r2, 0xFFFF
    # MUL_IMM r2, 0x9A3F  
    # ADD r0, r2
    # AND r0, 0xFFFF
    # r1 = sreg[3] = S1
    # CMP r0, r1 => flag = (r0 == S1)
    
    xor_h = (H0 ^ H1) & 0xFFFF
    rol7 = ((xor_h << 7) | (xor_h >> (16 - 7))) & 0xFFFF  # 16-bit rotate
    # Wait... ROL in primary VM is 32-bit rotate. Let me reconsider:
    # ROL r2, 7 on a 32-bit value, then AND 0xFFFF
    xor_h_32 = (H0 ^ H1) & 0xFFFF  # already masked
    rol7_32 = ((xor_h_32 << 7) | (xor_h_32 >> (32 - 7))) & 0xFFFFFFFF
    rol7_16 = rol7_32 & 0xFFFF
    
    S1 = ((H1 * 0x4E6B) + (H0 * 0x1337) + (rol7_16 * 0x9A3F)) & 0xFFFF
    
    # After check:
    # r7 ^= S1
    r7 ^= S1
    # r4 = acc; r4 ^= S1; ROR r4, 5; acc = r4
    # Wait, looking at the disasm for block 2 (around 0x00C4):
    # 00c4: XOR r7, r1
    # 00c7: LOAD_ACC r4
    # 00c9: XOR r4, r1
    # 00cc: ROR r4, 5
    # 00cf: STORE_ACC r4
    r4 = acc ^ S1
    r4 = ((r4 >> 5) | (r4 << 27)) & 0xFFFFFFFF
    acc = r4
    
    # ============================================================
    # Block 3: Compute S2  (offset ~0x00D1 - 0x0114)
    # ============================================================
    # r0 = sreg[0]; r1 = sreg[1]; r0 ^= r1 (= H0^H1)
    # MUL_IMM r0, 0x3141
    # ADD_IMM r0, 0x5926
    # r1 = sreg[2] = S0 (note: loads the serial word we already know!)
    # MUL_IMM r1, 0xA5A5
    # ADD r0, r1
    # AND r0, 0xFFFF
    # r1 = sreg[4] = S2
    # CMP r0, r1
    
    S2 = (((H0 ^ H1) * 0x3141 + 0x5926) + (S0 * 0xA5A5)) & 0xFFFF
    
    # After:
    # r7 ^= S2
    r7 ^= S2
    # r4 = acc; ADD r4, S2; LFSR r4; acc = r4
    r4 = (acc + S2) & 0xFFFFFFFF
    r4 = lfsr_step(r4)
    acc = r4
    
    # ============================================================
    # Block 4: Compute S3  (offset ~0x011E - 0x016E)
    # ============================================================
    # Integrity trap: r5=0; NOT r5; AND 0xFFFF r5; ADD 1; AND 0xFFFF; CMP 0 -> never 0
    # 
    # r0 = sreg[2] = S0; r1 = sreg[3] = S1; ADD r0, r1 (r0 = S0+S1)
    # r1 = sreg[4] = S2; ADD r0, r1 (r0 = S0+S1+S2)
    # AND r0, 0xFFFF
    # r1 = sreg[0] = H0 (stored in r1)
    # MUL_IMM r1, 0x0F0F; AND 0xFFFF; r0 ^= r1
    # r1 = sreg[1] = H1
    # MUL_IMM r1, 0xF0F0; AND 0xFFFF; r0 ^= r1
    # r2 = sreg[2] = S0; r3 = sreg[3] = S1; r2 ^= r3; AND 0xFFFF
    # ROR r2, 3; AND 0xFFFF
    # ADD r0, r2; AND 0xFFFF
    # r1 = sreg[5] = S3
    # CMP r0, r1
    
    base = (S0 + S1 + S2) & 0xFFFF
    h0_term = (H0 * 0x0F0F) & 0xFFFF
    h1_term = (H1 * 0xF0F0) & 0xFFFF
    base ^= h0_term
    base ^= h1_term 
    
    s0_xor_s1 = (S0 ^ S1) & 0xFFFF
    # ROR 32-bit by 3, then AND 0xFFFF
    ror3 = ((s0_xor_s1 >> 3) | (s0_xor_s1 << (32 - 3))) & 0xFFFFFFFF
    ror3 &= 0xFFFF
    
    S3 = (base + ror3) & 0xFFFF
    
    # After:
    r7 ^= S3
    r4 = acc ^ S3
    r4 = ((r4 >> 7) | (r4 << 25)) & 0xFFFFFFFF  # Wait, the disasm shows ROR r4, #7 at 0x0106
    # Hmm, checking again... let me look at offset 0x0171-0x017A:
    # 0171: XOR r7, r1      ; r7 ^= S3
    # 0174: LOAD_ACC r4
    # 0176: XOR r4, r1       ; r4 = acc ^ S3
    # 0179: STORE_ACC r4
    # No ROR here for block 3! Let me re-check blocks...
    
    # Actually, block 3 (S3) the acc update at 0x0171-0x0179 is:
    # XOR r7, r1
    # LOAD_ACC r4
    # XOR r4, r1
    # STORE_ACC r4
    # So: acc ^= S3
    acc ^= S3
    r4 = acc
    
    # ============================================================
    # Block 5: Compute S4  (offset ~0x017B - 0x01B4)
    # ============================================================
    # r0 = sreg[2]=S0; r1 = sreg[3]=S1; r0 ^= r1
    # r1 = sreg[4]=S2; r0 ^= r1
    # r1 = sreg[5]=S3; r0 ^= r1
    # r1 = r0 (saved)
    # r2 = r1 (r2 = r0_val)
    # ADD r1, r2 => r1 = 2*r0_val
    # MUL_IMM r1, 0xDEAD
    # ADD r0, r1
    # r1 = sreg[4]=S2
    # MUL_IMM r1, 0x1111
    # ADD r0, r1
    # AND r0, 0xFFFF
    # r1 = sreg[6] = S4
    # CMP r0, r1
    
    xor_all = (S0 ^ S1 ^ S2 ^ S3) & 0xFFFF
    r0 = xor_all
    r1 = r0
    r2 = r1
    r1 = (r1 + r2) & 0xFFFFFFFF  # r1 = 2 * xor_all
    r1 = (r1 * 0xDEAD) & 0xFFFFFFFF
    r0 = (r0 + r1) & 0xFFFFFFFF
    r1 = (S2 * 0x1111) & 0xFFFFFFFF
    r0 = (r0 + r1) & 0xFFFFFFFF
    S4 = r0 & 0xFFFF
    
    # After:
    r7 ^= S4
    # 01b7: XOR r7, r1
    # 01ba: LOAD_ACC r4
    # 01bc: ADD r4, r1
    # 01bf: LFSR r4
    # 01c1: STORE_ACC r4
    r4 = (acc + S4) & 0xFFFFFFFF
    r4 = lfsr_step(r4)
    acc = r4
    
    # ============================================================
    # Block 6: S5 via Inner VM #0  (offset 0x01C3)
    # ============================================================
    # INVOKE_VM2 #0
    # The inner VM #0 is invoked with bVar18=0 (first program)
    # Source regs for VM2#0: sreg[0..5] = [H0, H1, S0, S1, S2, S3]
    #   (6 source regs: local_b90 = 6)
    # Bytecode = decrypted bytecode at local_615 (0x21 = 33 bytes)
    
    # Decrypted VM2#0 bytecode:
    # 01 40 01 41 05 4d 02 49 00 48 01 42 01 43 03 43 04 41 02 73 75 47 0f 44 0f 43 05 49 12 62 00 52 11
    # Hmm, but register indices like 0x40, 0x41 etc are way out of range (max 5 for 6 regs)
    # Something is wrong with my decryption of bytecode 2.
    
    # Let me re-check. The binary decrypts bytecode 2 (local_615) from DAT_1400073e0 
    # BUT the XOR key used comes from uStack_b1c._4_4_ which is set right before the loop:
    # 
    # For local_615 (bytecode invoked by bVar18==0, 0x21 bytes):
    # uStack_b1c._4_4_ = CONCAT31(CONCAT21(CONCAT11(DAT_140006021, DAT_140006022), DAT_140006023), DAT_140006028)
    # This is a 4-byte value assembled as:
    #   byte0 (lowest) = DAT_140006028 = 0xDE
    #   byte1 = DAT_140006021 = 0xEF  
    #   byte2 = DAT_140006022 = 0xBE
    #   byte3 (highest) = DAT_140006023 = 0xAD
    #
    # CONCAT31(abc, d) = abc << 8 | d  (result is 4 bytes)
    # So the 32-bit key = 0xADBEEFDE (as a little-endian value: DE EF BE AD)
    #
    # But the XOR loop uses: *(byte *)((longlong)auStack_b14 + ((ulonglong)((uint)lVar16 & 3) - 4))
    # auStack_b14 is right after uStack_b1c in memory layout.
    # The key bytes at offsets -4..-1 from auStack_b14 = uStack_b1c._4_4_ as bytes:
    # In little-endian: [0xDE, 0xEF, 0xBE, 0xAD]
    
    # So key = [0xDE, 0xEF, 0xBE, 0xAD] and I used that correctly: deefbead
    # But wait, the offset is ((uint)lVar16 & 3) - 4, which gives:
    #   when lVar16 & 3 == 0: offset -4 (byte 0 of key)
    #   when lVar16 & 3 == 1: offset -3 (byte 1 of key)
    #   when lVar16 & 3 == 2: offset -2 (byte 2 of key)
    #   when lVar16 & 3 == 3: offset -1 (byte 3 of key)
    # So key[i & 3] = auStack_b14[i&3 - 4] = uStack_b1c._4_4_ bytes in LE order
    # = [0xDE, 0xEF, 0xBE, 0xAD]
    # This matches my key_bc2 = deefbead, so decryption should be correct.
    
    # But register indices 0x40 = 64 are invalid (max 5). This suggests
    # the encoding is different for the inner VM. The inner VM's register indices
    # might be relative to some base. Looking at the decompiled inner VM case 0:
    #   idx = bc[pc+1]
    #   if sp >= 0x7f || idx >= local_b90: break (local_b90 = num_src_regs)
    #   stack[sp] = source_regs[idx]
    # 
    # So idx must be < num_src_regs (6 for #0, 9 for #1, 10 for #2)
    # But our decrypted byte at index 1 is 0x40 which is 64... that's wrong.
    
    # Let me re-examine the key construction. Maybe I have the wrong globals.
    # For case bVar18==0 in the INVOKE_VM2:
    #   local_b90 = 6
    #   iVar21 = 0x21 (bytecode length)
    #   pFVar24 = &local_615 (bytecode pointer)
    # But wait, the binary has iVar21=0x21 meaning max_len=33 for decrypted bc at local_615
    # And the source regs are arranged from local_b58:
    #   local_b58 = CONCAT44(local_12c[1], local_12c[0]) = (H1, H0)
    #   uStack_b50 = CONCAT44(local_12c[3], local_12c[2]) = (S1, S0)
    #   local_b48 = CONCAT44(local_110, local_118) = (S4, S2)
    #   pFVar24 = &local_615
    # Hmm, for bVar18==0: local_b48 = CONCAT44(local_110, local_118)
    # That's only 3 64-bit words = 6 32-bit values:
    #   idx 0: H0, idx 1: H1, idx 2: S0, idx 3: S1, idx 4: S2, idx 5: S4
    
    # Wait no. bVar18==0 path sets:
    #   local_b58 = CONCAT44(local_12c[1], local_12c[0])
    #   uStack_b50 = CONCAT44(local_12c[3], local_12c[2])
    #   local_b48 = CONCAT44(local_110, local_118)
    # BUT for bVar18==0 specifically:
    #   iVar21 = 0x21, local_b90 = 6
    #   pFVar24 = &local_615
    
    # So the source register array (local_b58) contains:
    # [local_12c[0], local_12c[1], local_12c[2], local_12c[3], local_118, local_110]
    # = [H0, H1, S0, S1, S2, S4]
    
    # Hmm, that gives S4 at index 5, not S3. But our S4 was just computed...
    # Actually local_118 = sreg[5] = serial[3] = S3 (not S2)
    # local_110 = sreg[7] = serial[5] = S5 ← but we're solving for S5 here!
    
    # Wait, local_12c and local_11c etc map to sreg indices:
    # local_12c[0] = hash_lo
    # local_12c[1] = hash_hi  
    # local_12c[2] = serial[0] = S0
    # local_12c[3] = serial[1] = S1
    # local_11c = serial[2] = S2
    # local_118 = serial[3] = S3
    # local_114 = serial[4] = S4
    # local_110 = serial[5] = S5
    # local_10c = serial[6] = S6
    # uStack_108 = serial[7] = S7
    
    # So for bVar18==0, source regs = [H0, H1, S0, S1, S3, S5]
    # local_b48 = CONCAT44(local_110, local_118) means:
    # low 32bits = local_118 = S3 (index 4), high 32bits = local_110 = S5 (index 5)
    
    # But S5 is what we're SOLVING for! This means S5 appears in a constraint.
    # The VM2 must compute some function and return 1 iff S5 satisfies the constraint.
    # We need to solve the inner VM equation for S5.
    
    # This changes the approach: S5 is determined by solving the inner VM #0 equation.
    # Let me analyze the decrypted inner VM #0 bytecode more carefully.
    
    # Let me re-decrypt with the corrected understanding and check if register indices make sense.
    # Actually, maybe my decryption is correct and the register indices ARE in range.
    # Let me re-check: decrypted_bc2 should have indices < 6.
    
    # Decrypted: 01 40 01 41 05 4d 02 49 00 48 01 42 01 43 03 43 04 41 02 73 75 47 0f 44 0f 43 05 49 12 62 00 52 11
    # First instruction: raw=0x01, opcode = 0x01-1 = 0 (PUSH_REG), next byte = 0x40 = 64
    # 64 >= 6, so this would FAIL.
    
    # This means my decryption key is WRONG. Let me re-check.
    
    # CRITICAL RE-EXAMINATION:
    # The decryption loops use the key like:
    #   for i in range(length):
    #     dest[i] = key_bytes[(i & 3)] ^ encrypted_data[i]
    # where key_bytes are from uStack_b1c._4_4_ which is set differently for each bytecode.
    
    # For local_615 (after local_878 which is 0x263 bytes of main VM code): 
    # uStack_b1c._4_4_ = CONCAT31(CONCAT21(CONCAT11(DAT_140006021, DAT_140006022), DAT_140006023), DAT_140006028)
    # 
    # CONCAT11(a,b) = (a << 8) | b (2 bytes)
    # CONCAT21(ab, c) = (ab << 8) | c (3 bytes)  
    # CONCAT31(abc, d) = (abc << 8) | d (4 bytes)
    #
    # So: CONCAT11(0xEF, 0xBE) = 0xEFBE
    #     CONCAT21(0xEFBE, 0xAD) = 0xEFBEAD
    #     CONCAT31(0xEFBEAD, 0xDE) = 0xEFBEADDE
    #
    # As a 32-bit value stored in little-endian: DE AD BE EF
    # So key_bytes = [0xDE, 0xAD, 0xBE, 0xEF]  (NOT [0xDE, 0xEF, 0xBE, 0xAD])!
    #
    # I had the byte order wrong! CONCAT31 puts the first arg in the HIGH bytes,
    # so 0xEFBEADDE stored in little-endian is DE AD BE EF.

    # Let me also fix the other keys:
    # For local_5d5 (bytecode for bVar18==1):
    # CONCAT31(CONCAT21(CONCAT11(DAT_140006019, DAT_14000601a), DAT_14000601b), DAT_140006020)
    # = CONCAT31(CONCAT21(CONCAT11(0xBE, 0xBA), 0xFE), 0xCA)
    # = CONCAT31(CONCAT21(0xBEBA, 0xFE), 0xCA)
    # = CONCAT31(0xBEBAFE, 0xCA)
    # = 0xBEBAFECA
    # LE bytes: CA FE BA BE
    
    # For local_595 (bytecode for bVar18==2):
    # CONCAT31(CONCAT21(CONCAT11(DAT_140006010, DAT_140006011), DAT_140006012), DAT_140006018)
    # = CONCAT31(CONCAT21(CONCAT11(0xDE, 0xC0), 0x37), 0x13)
    # = CONCAT31(CONCAT21(0xDEC0, 0x37), 0x13)
    # = CONCAT31(0xDEC037, 0x13)
    # = 0xDEC03713
    # LE bytes: 13 37 C0 DE
    
    # For local_878 (main 0x263-byte bytecode):
    # CONCAT13(DAT_140006030, CONCAT12(DAT_140006038, CONCAT11(DAT_140006040, DAT_140006048)))
    # CONCAT11(0x1C, 0x5A) = 0x1C5A
    # CONCAT12(0xBE, 0x1C5A) = 0xBE1C5A  (3 bytes: BE is high)
    # CONCAT13(0xB4, 0xBE1C5A) = 0xB4BE1C5A (4 bytes: B4 is highest)
    # LE bytes: 5A 1C BE B4
    # This matches my original key! Good.
    
    pass

# Let me re-decrypt with corrected keys and verify
def decrypt_bc(data_hex, key_bytes, length):
    data = bytes.fromhex(data_hex)
    result = bytearray()
    for i in range(length):
        result.append(data[i] ^ key_bytes[i & 3])
    return result

# Re-decrypt inner VM bytecodes with CORRECT key byte orders
# VM2 #0 (local_615, 0x21 bytes): key = DE AD BE EF
bc2_data = "DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF"
key2 = [0xDE, 0xAD, 0xBE, 0xEF]
dec_bc2 = decrypt_bc(bc2_data, key2, 0x21)
print("VM2 #0 (corrected):", ' '.join(f'{b:02x}' for b in dec_bc2))

# VM2 #1 (local_5d5, 0x27 bytes): key = CA FE BA BE
bc3_data = "CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB"
key3 = [0xCA, 0xFE, 0xBA, 0xBE]
dec_bc3 = decrypt_bc(bc3_data, key3, 0x27)
print("VM2 #1 (corrected):", ' '.join(f'{b:02x}' for b in dec_bc3))

# VM2 #2 (local_595, 0x29 bytes): key = 13 37 C0 DE
bc4_data = "1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02"
key4 = [0x13, 0x37, 0xC0, 0xDE]
dec_bc4 = decrypt_bc(bc4_data, key4, 0x29)
print("VM2 #2 (corrected):", ' '.join(f'{b:02x}' for b in dec_bc4))

# Verify main bytecode key: 5A 1C BE B4
main_data = "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4"
key_main = [0x5A, 0x1C, 0xBE, 0xB4]
dec_main = decrypt_bc(main_data, key_main, 17)
print("Main BC first 17 bytes:", ' '.join(f'{b:02x}' for b in dec_main))
