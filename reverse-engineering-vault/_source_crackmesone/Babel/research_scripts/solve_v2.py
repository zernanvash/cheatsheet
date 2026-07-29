#!/usr/bin/env python3
"""Robust VM serial solver using unique sentinel values."""

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

main_bc_hex = "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000"

def run_vm(bc_orig, sregs_in, inner_bcs, fix_cmps=True, trace=False):
    """Run primary VM. If fix_cmps=True, automatically fix CMP failures by patching sregs."""
    bc = bytearray(bc_orig)
    regs = [0]*8
    sregs = list(sregs_in)
    out = [0]*8
    flag = 0
    acc = 0xDEAD
    vpc = 0
    vstack = [0]*256
    vsp = -1
    cstack = [0]*32
    csp = -1
    halt = False
    iter_count = 0
    ot = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")
    
    # Track which LOAD_SREG loaded which sreg into which register
    last_sreg_load = {}  # reg_idx -> sreg_idx  (most recent)
    
    for step in range(200000):
        if halt or vpc >= len(bc): break
        raw = bc[vpc]
        if raw >= len(ot): halt = True; break
        case = ot[raw]
        op1 = bc[vpc+1] if vpc+1 < len(bc) else 0
        op2 = bc[vpc+2] if vpc+2 < len(bc) else 0
        op3 = bc[vpc+3] if vpc+3 < len(bc) else 0
        imm16 = (op3 << 8) | op2
        old_vpc = vpc
        
        if case == 0: vpc += 1
        elif case == 1: regs[op1] = imm16; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 2:
            regs[op1] = sregs[op2] if op2 < len(sregs) else 0
            last_sreg_load[op1] = op2  # Track this load
            vpc += 3
        elif case == 3: 
            regs[op1] = regs[op2]
            if op2 in last_sreg_load: last_sreg_load[op1] = last_sreg_load[op2]
            else: last_sreg_load.pop(op1, None)
            vpc += 3
        elif case == 4:
            regs[op1] = (regs[op1]+regs[op2])&0xFFFFFFFF
            last_sreg_load.pop(op1, None); vpc += 3
        elif case == 5: regs[op1] = (regs[op1]-regs[op2])&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 6: regs[op1] = (regs[op1]*regs[op2])&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 7: regs[op1] ^= regs[op2]; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 8: regs[op1] &= regs[op2]; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 9: regs[op1] |= regs[op2]; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0xa: regs[op1] = (regs[op1]<<(op2&0x1f))&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0xb: regs[op1] >>= (op2&0x1f); last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0xc: regs[op1] = (~regs[op1])&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 2
        elif case == 0xd:
            flag = 1 if regs[op1] == regs[op2] else 0
            
            if fix_cmps and flag == 0:
                # One of the two registers should contain a serial word loaded via LOAD_SREG
                # The other is the computed expected value
                r1_sreg = last_sreg_load.get(op1)
                r2_sreg = last_sreg_load.get(op2)
                
                if r2_sreg is not None and r2_sreg >= 2:
                    # r[op2] holds serial word, r[op1] is expected
                    expected = regs[op1] & 0xFFFF
                    si = r2_sreg - 2
                    sregs[r2_sreg] = expected
                    regs[op2] = expected
                    flag = 1
                    if trace: print(f"  FIX S{si}: 0x{expected:04x} (at vpc=0x{old_vpc:04x})")
                elif r1_sreg is not None and r1_sreg >= 2:
                    expected = regs[op2] & 0xFFFF
                    si = r1_sreg - 2
                    sregs[r1_sreg] = expected
                    regs[op1] = expected
                    flag = 1
                    if trace: print(f"  FIX S{si}: 0x{expected:04x} (at vpc=0x{old_vpc:04x})")
            
            vpc += 3
        elif case == 0xe: vpc = (op2<<8)|op1
        elif case == 0xf: t = (op2<<8)|op1; vpc = t if flag else vpc+3
        elif case == 0x10: t = (op2<<8)|op1; vpc = t if not flag else vpc+3
        elif case == 0x11: vsp += 1; vstack[vsp] = regs[op1]; vpc += 2
        elif case == 0x12:
            if vsp >= 0: regs[op1] = vstack[vsp]; vsp -= 1
            # After POP, the register no longer tracks a sreg
            last_sreg_load.pop(op1, None)
            vpc += 2
        elif case == 0x13: out[op1] = regs[op2]; vpc += 3
        elif case == 0x14: halt = True; vpc += 1
        elif case == 0x15: regs[op1] = (regs[op1]+imm16)&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x16: regs[op1] ^= imm16; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x17: regs[op1] &= imm16; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x18:
            s = op2&0x1f; v = regs[op1]; regs[op1] = ((v<<s)|(v>>(32-s)))&0xFFFFFFFF
            last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0x19:
            s = op2&0x1f; v = regs[op1]; regs[op1] = ((v>>s)|(v<<(32-s)))&0xFFFFFFFF
            last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0x1a: t = (op2<<8)|op1; csp += 1; cstack[csp] = vpc+3; vpc = t
        elif case == 0x1b:
            if csp >= 0: vpc = cstack[csp]; csp -= 1
            else: halt = True
        elif case == 0x1c: regs[op1] = (regs[op1]*imm16)&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x1d:
            flag = 1 if regs[op1] == imm16 else 0
            if fix_cmps and flag == 0 and imm16 == 1 and op1 == 0:
                # Inner VM returned 0 - this means prior serial words don't satisfy inner VM.
                # We can't auto-fix this - inner VMs need correct values upfront.
                if trace: print(f"  INNER VM FAIL at vpc=0x{old_vpc:04x}")
            vpc += 4
        elif case == 0x1e: regs[op1] = (regs[op1]-imm16)&0xFFFFFFFF; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x1f:
            regs[op1],regs[op2] = regs[op2],regs[op1]
            if op1 in last_sreg_load or op2 in last_sreg_load:
                s1 = last_sreg_load.pop(op1, None)
                s2 = last_sreg_load.pop(op2, None)
                if s1 is not None: last_sreg_load[op2] = s1
                if s2 is not None: last_sreg_load[op1] = s2
            vpc += 3
        elif case == 0x20:
            which = op1
            result = run_inner_vm(which, regs, sregs, out, inner_bcs)
            regs[0] = result
            last_sreg_load.pop(0, None)
            vpc += 2
        elif case == 0x21:
            offset = (op2<<8)|op1
            if offset < len(bc): bc[offset] = regs[op3]&0xFF
            vpc += 4
        elif case == 0x22: regs[op1] = iter_count; last_sreg_load.pop(op1, None); vpc += 2
        elif case == 0x23: regs[op1] |= imm16; last_sreg_load.pop(op1, None); vpc += 4
        elif case == 0x24:
            v = regs[op1]^regs[op2]; v &= 0xFFFF
            for _ in range(16):
                if v&1: v = (v>>1)^0xA001
                else: v >>= 1
            regs[op1] = v&0xFFFF; last_sreg_load.pop(op1, None); vpc += 3
        elif case == 0x25: regs[op1] = acc; last_sreg_load.pop(op1, None); vpc += 2
        elif case == 0x26: acc = regs[op1]; vpc += 2
        elif case == 0x27:
            v = regs[op1]&0xFFFF
            if v&1: regs[op1] = ((v>>1)^0xB400)&0xFFFF
            else: regs[op1] = (v>>1)&0xFFFF
            last_sreg_load.pop(op1, None); vpc += 2
        else: halt = True
        
        iter_count += 1
    
    return out, sregs

def run_inner_vm(which, regs, sregs, out, inner_bcs):
    if which >= len(inner_bcs): return 0
    info = inner_bcs[which]
    bc = info['bc']; src = info['src_fn'](regs, sregs, out)
    num = info['num_src']; maxlen = info['max_len']
    stack = [0]*128; sp = -1; pc = 0
    for _ in range(4096):
        if pc >= maxlen: return 0
        raw = bc[pc]; op = raw - 1
        if op > 0x16 or op < 0: return 0
        if op == 0:
            idx = bc[pc+1]
            if sp >= 0x7f or idx >= num: return 0
            sp += 1; stack[sp] = src[idx]&0xFFFFFFFF; pc += 2
        elif op == 1:
            imm = (bc[pc+2]<<8)|bc[pc+1]
            if sp >= 0x7f: return 0
            sp += 1; stack[sp] = imm; pc += 3
        elif op == 2: stack[sp-1] = (stack[sp-1]+stack[sp])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 3: stack[sp-1] = (stack[sp-1]-stack[sp])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 4: stack[sp-1] = (stack[sp]*stack[sp-1])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 5: stack[sp-1] ^= stack[sp]; sp -= 1; pc += 1
        elif op == 6: stack[sp-1] &= stack[sp]; sp -= 1; pc += 1
        elif op == 7: stack[sp-1] |= stack[sp]; sp -= 1; pc += 1
        elif op == 8:
            s = stack[sp]&0xf; v = stack[sp-1]&0xFFFF
            stack[sp-1] = ((v<<s)|(v>>(16-s)))&0xFFFF; sp -= 1; pc += 1
        elif op == 9:
            s = stack[sp]&0xf; v = stack[sp-1]&0xFFFF
            stack[sp-1] = ((v>>s)|(v<<(16-s)))&0xFFFF; sp -= 1; pc += 1
        elif op == 0xa: stack[sp-1] = 1 if stack[sp]==stack[sp-1] else 0; sp -= 1; pc += 1
        elif op == 0xb: sp += 1; stack[sp] = stack[sp-1]; pc += 1
        elif op == 0xc: stack[sp],stack[sp-1] = stack[sp-1],stack[sp]; pc += 1
        elif op == 0xd: stack[sp] = (~stack[sp])&0xFFFF; pc += 1
        elif op == 0xe: stack[sp] &= 0xFFFF; pc += 1
        elif op == 0xf: return 1
        elif op == 0x10: return 0
        elif op == 0x11:
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
            pc = t if v else pc+3
        elif op == 0x12:
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
            pc = t if not v else pc+3
        elif op == 0x13: sp -= 1; pc += 1
        elif op == 0x14:
            v = stack[sp-1]^stack[sp]; v &= 0xFFFF
            for _ in range(16):
                if v&1: v = (v>>1)^0xA001
                else: v >>= 1
            stack[sp-1] = v&0xFFFF; sp -= 1; pc += 1
        elif op == 0x15: s = stack[sp]&0xf; stack[sp-1] = (stack[sp-1]<<s)&0xFFFF; sp -= 1; pc += 1
        elif op == 0x16: s = stack[sp]&0xf; stack[sp-1] = (stack[sp-1]>>s)&0xFFFF; sp -= 1; pc += 1
        else: return 0
    return 0

# Setup
def vm2_0_src(r, s, o): return [s[0], s[1], s[2], s[3], s[5], s[7]]
def vm2_1_src(r, s, o): return [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]]
def vm2_2_src(r, s, o): return [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9]]

inner_bcs = [
    {'bc': decrypt_bc("DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF", [0xDE,0xAD,0xBE,0xEF], 0x21),
     'num_src': 6, 'max_len': 0x21, 'src_fn': vm2_0_src},
    {'bc': decrypt_bc("CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB", [0xCA,0xFE,0xBA,0xBE], 0x27),
     'num_src': 9, 'max_len': 0x27, 'src_fn': vm2_1_src},
    {'bc': decrypt_bc("1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02", [0x13,0x37,0xC0,0xDE], 0x29),
     'num_src': 10, 'max_len': 0x29, 'src_fn': vm2_2_src},
]

main_bc = decrypt_bc(main_bc_hex, [0x5A, 0x1C, 0xBE, 0xB4], 0x263)

import sys, subprocess
username = sys.argv[1] if len(sys.argv) > 1 else "test"
h = murmur_hash(username)
H0 = h & 0xFFFF
H1 = (h >> 16) & 0xFFFF

# Phase 1: Discover S0-S4 (from primary VM CMP reg, reg)
sregs_init = [H0, H1] + [0xBAD0 + i for i in range(8)]  # unique sentinels
out, sregs_after = run_vm(main_bc, sregs_init, inner_bcs, fix_cmps=True, trace=True)

serial_phase1 = [sregs_after[2+i] for i in range(8)]
print(f"\nPhase 1 serial: {'-'.join(f'{s:04X}' for s in serial_phase1)}")
print(f"Phase 1 result: out[0]={out[0]}")

# Phase 2: Re-run with discovered S0-S4. The inner VMs should now get correct inputs.
# Inner VMs determine S5, S6, S7.
# We need to brute-force S5 through VM2#0, S6 through VM2#1, S7 through VM2#2.

# But first, let's see if phase 1 found all of them
if out[0] == 1:
    serial_str = '-'.join(f'{s:04X}' for s in serial_phase1)
    print(f"\nFull serial found: {serial_str}")
else:
    # Inner VMs failed. We need to brute-force S5, S6, S7.
    print("\nPhase 2: Brute-forcing inner VM constraints...")
    
    S = list(serial_phase1)
    
    # VM2 #0 determines S5
    # src = [H0, H1, S0, S1, S3, S5]
    # Brute-force S5:
    print("  Brute-forcing S5 via VM2 #0...")
    for s5 in range(0x10000):
        S[5] = s5
        sregs_test = [H0, H1] + S
        src = vm2_0_src(None, sregs_test, None)
        result = run_inner_vm(0, None, sregs_test, None, inner_bcs)
        if result == 1:
            print(f"  Found S5 = 0x{s5:04x}")
            break
    else:
        print("  S5 not found!")
    
    # VM2 #1 determines S6
    # src = [H0, H1, S0, S1, S2, S3, S4, S5, S6]
    print("  Brute-forcing S6 via VM2 #1...")
    for s6 in range(0x10000):
        S[6] = s6
        sregs_test = [H0, H1] + S
        result = run_inner_vm(1, None, sregs_test, None, inner_bcs)
        if result == 1:
            print(f"  Found S6 = 0x{s6:04x}")
            break
    else:
        print("  S6 not found!")
    
    # VM2 #2 determines S7
    print("  Brute-forcing S7 via VM2 #2...")
    for s7 in range(0x10000):
        S[7] = s7
        sregs_test = [H0, H1] + S
        result = run_inner_vm(2, None, sregs_test, None, inner_bcs)
        if result == 1:
            print(f"  Found S7 = 0x{s7:04x}")
            break
    else:
        print("  S7 not found!")
    
    # Final verification
    sregs_final = [H0, H1] + S
    out_final, _ = run_vm(bytearray(main_bc), sregs_final, inner_bcs, fix_cmps=False, trace=False)
    serial_str = '-'.join(f'{s:04X}' for s in S)
    print(f"\nFinal serial: {serial_str}")
    print(f"VM result: out[0]={out_final[0]}")
    
    # Test against binary
    binary = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"
    inp = f"{username}\n{serial_str}\n"
    try:
        r = subprocess.run([binary], input=inp, capture_output=True, text=True, timeout=10)
        if "Access Granted" in r.stdout:
            print("BINARY: Access Granted!")
        elif "Invalid" in r.stdout:
            print("BINARY: Invalid License")
        else:
            print(f"BINARY: {r.stdout.strip()[-50:]}")
    except Exception as e:
        print(f"BINARY test error: {e}")
