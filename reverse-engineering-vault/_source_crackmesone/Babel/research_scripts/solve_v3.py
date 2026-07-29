#!/usr/bin/env python3
"""
Correct multi-phase, iterative VM solver for babel_vm.exe keygen.
Phase 1: Discover S0-S4 via primary VM CMP interception
Phase 2: Brute-force S5 via inner VM #0
Phase 3: Brute-force S6 via inner VM #1  
Phase 4: Brute-force S7 via inner VM #2
Phase 5: Final verification pass with all values
"""

import sys, subprocess

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

main_bc_template = decrypt_bc(main_bc_hex, [0x5A, 0x1C, 0xBE, 0xB4], 0x263)

ot = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")

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


def run_inner(which, sregs):
    """Run inner VM with given source registers."""
    info = inner_bcs[which]
    bc = info['bc']
    src = info['src_fn'](None, sregs, None)
    num = info['num_src']
    maxlen = info['max_len']
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
        elif op == 0x11:  # JZ: jump if TOS == 0
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
            pc = t if not v else pc+3
        elif op == 0x12:  # JNZ: jump if TOS != 0
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
            pc = t if v else pc+3
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


def run_primary_discover(bc, sregs_in):
    """Run primary VM, auto-fixing CMP reg,reg failures. Returns (discovered_sregs, ok)."""
    bc = bytearray(bc)
    regs = [0]*8; sregs = list(sregs_in); out = [0]*8
    flag = 0; acc = 0xDEAD; vpc = 0
    vstack = [0]*256; vsp = -1; cstack = [0]*32; csp = -1
    halt = False; iter_count = 0
    last_sreg = {}  # tracks which reg was most recently loaded from which sreg
    
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
        
        def clear_sr(r): last_sreg.pop(r, None)
        
        if case == 0: vpc += 1
        elif case == 1: regs[op1] = imm16; clear_sr(op1); vpc += 4
        elif case == 2:
            regs[op1] = sregs[op2] if op2 < len(sregs) else 0
            last_sreg[op1] = op2; vpc += 3
        elif case == 3:
            regs[op1] = regs[op2]
            if op2 in last_sreg: last_sreg[op1] = last_sreg[op2]
            else: clear_sr(op1)
            vpc += 3
        elif case == 4: regs[op1] = (regs[op1]+regs[op2])&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 5: regs[op1] = (regs[op1]-regs[op2])&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 6: regs[op1] = (regs[op1]*regs[op2])&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 7: regs[op1] ^= regs[op2]; clear_sr(op1); vpc += 3
        elif case == 8: regs[op1] &= regs[op2]; clear_sr(op1); vpc += 3
        elif case == 9: regs[op1] |= regs[op2]; clear_sr(op1); vpc += 3
        elif case == 0xa: regs[op1] = (regs[op1]<<(op2&0x1f))&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 0xb: regs[op1] >>= (op2&0x1f); clear_sr(op1); vpc += 3
        elif case == 0xc: regs[op1] = (~regs[op1])&0xFFFFFFFF; clear_sr(op1); vpc += 2
        elif case == 0xd:
            flag = 1 if regs[op1] == regs[op2] else 0
            if flag == 0:
                # Try to fix: which register holds the sreg?
                r1s = last_sreg.get(op1)
                r2s = last_sreg.get(op2)
                if r2s is not None and r2s >= 2:
                    # r[op2] is serial word, r[op1] is expected
                    sregs[r2s] = regs[op1] & 0xFFFF
                    regs[op2] = regs[op1]
                    flag = 1
                elif r1s is not None and r1s >= 2:
                    sregs[r1s] = regs[op2] & 0xFFFF
                    regs[op1] = regs[op2]
                    flag = 1
            vpc += 3
        elif case == 0xe: vpc = (op2<<8)|op1
        elif case == 0xf: t = (op2<<8)|op1; vpc = t if flag else vpc+3
        elif case == 0x10: t = (op2<<8)|op1; vpc = t if not flag else vpc+3
        elif case == 0x11: vsp += 1; vstack[vsp] = regs[op1]; vpc += 2
        elif case == 0x12:
            if vsp >= 0: regs[op1] = vstack[vsp]; vsp -= 1
            clear_sr(op1); vpc += 2
        elif case == 0x13: out[op1] = regs[op2]; vpc += 3
        elif case == 0x14: halt = True; vpc += 1
        elif case == 0x15: regs[op1] = (regs[op1]+imm16)&0xFFFFFFFF; clear_sr(op1); vpc += 4
        elif case == 0x16: regs[op1] ^= imm16; clear_sr(op1); vpc += 4
        elif case == 0x17: regs[op1] &= imm16; clear_sr(op1); vpc += 4
        elif case == 0x18:
            s = op2&0x1f; v = regs[op1]
            regs[op1] = ((v<<s)|(v>>(32-s)))&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 0x19:
            s = op2&0x1f; v = regs[op1]
            regs[op1] = ((v>>s)|(v<<(32-s)))&0xFFFFFFFF; clear_sr(op1); vpc += 3
        elif case == 0x1a: t = (op2<<8)|op1; csp += 1; cstack[csp] = vpc+3; vpc = t
        elif case == 0x1b:
            if csp >= 0: vpc = cstack[csp]; csp -= 1
            else: halt = True
        elif case == 0x1c: regs[op1] = (regs[op1]*imm16)&0xFFFFFFFF; clear_sr(op1); vpc += 4
        elif case == 0x1d:
            flag = 1 if regs[op1] == imm16 else 0
            # DON'T fix CMP_IMM - this is for inner VM results
            vpc += 4
        elif case == 0x1e: regs[op1] = (regs[op1]-imm16)&0xFFFFFFFF; clear_sr(op1); vpc += 4
        elif case == 0x1f:
            regs[op1],regs[op2] = regs[op2],regs[op1]
            s1 = last_sreg.pop(op1, None); s2 = last_sreg.pop(op2, None)
            if s1 is not None: last_sreg[op2] = s1
            if s2 is not None: last_sreg[op1] = s2
            vpc += 3
        elif case == 0x20:
            # Inner VM - run with current sregs
            result = run_inner(op1, sregs)
            regs[0] = result; clear_sr(0); vpc += 2
        elif case == 0x21:
            offset = (op2<<8)|op1
            if offset < len(bc): bc[offset] = regs[op3]&0xFF
            vpc += 4
        elif case == 0x22: regs[op1] = iter_count; clear_sr(op1); vpc += 2
        elif case == 0x23: regs[op1] |= imm16; clear_sr(op1); vpc += 4
        elif case == 0x24:
            v = regs[op1]^regs[op2]; v &= 0xFFFF
            for _ in range(16):
                if v&1: v = (v>>1)^0xA001
                else: v >>= 1
            regs[op1] = v&0xFFFF; clear_sr(op1); vpc += 3
        elif case == 0x25: regs[op1] = acc; clear_sr(op1); vpc += 2
        elif case == 0x26: acc = regs[op1]; vpc += 2
        elif case == 0x27:
            v = regs[op1]&0xFFFF
            if v&1: regs[op1] = ((v>>1)^0xB400)&0xFFFF
            else: regs[op1] = (v>>1)&0xFFFF
            clear_sr(op1); vpc += 2
        else: halt = True
        iter_count += 1
    
    return sregs, out


# ============================================================
# Main keygen
# ============================================================

username = sys.argv[1] if len(sys.argv) > 1 else "test"
h = murmur_hash(username)
H0 = h & 0xFFFF
H1 = (h >> 16) & 0xFFFF

print(f"Username: {username}")
print(f"Hash: 0x{h:08x} (H0=0x{H0:04x}, H1=0x{H1:04x})")

# Phase 1: Discover S0-S4
# Use sentinel values unlikely to collide with computed values
sentinels = [0xFE01, 0xFE02, 0xFE03, 0xFE04, 0xFE05, 0xFE06, 0xFE07, 0xFE08]
sregs_init = [H0, H1] + sentinels

sregs_after, out1 = run_primary_discover(main_bc_template, sregs_init)

S = [sregs_after[2+i] for i in range(8)]
print(f"\nPhase 1 (S0-S4 from primary VM CMPs):")
for i in range(5):
    changed = S[i] != sentinels[i]
    print(f"  S{i} = 0x{S[i]:04X} {'(discovered)' if changed else '(unchanged!)'}")

# Phase 2: Brute-force S5 via inner VM #0
# VM2 #0 src = [H0, H1, S0, S1, S3, S5]
print(f"\nPhase 2: Brute-forcing S5...")
found_s5 = False
for s5 in range(0x10000):
    S[5] = s5
    sregs_test = [H0, H1] + S
    if run_inner(0, sregs_test) == 1:
        print(f"  S5 = 0x{s5:04X}")
        found_s5 = True
        break
if not found_s5:
    print("  S5 NOT FOUND! (trying extended search)")

# Phase 3: Brute-force S6 via inner VM #1
# VM2 #1 src = [H0, H1, S0, S1, S2, S3, S4, S5, S6]
print(f"\nPhase 3: Brute-forcing S6...")
found_s6 = False
for s6 in range(0x10000):
    S[6] = s6
    sregs_test = [H0, H1] + S
    if run_inner(1, sregs_test) == 1:
        print(f"  S6 = 0x{s6:04X}")
        found_s6 = True
        break
if not found_s6:
    print("  S6 NOT FOUND!")

# Phase 4: Brute-force S7 via inner VM #2
# VM2 #2 src = [H0, H1, S0, S1, S2, S3, S4, S5, S6, S7]
print(f"\nPhase 4: Brute-forcing S7...")
found_s7 = False
for s7 in range(0x10000):
    S[7] = s7
    sregs_test = [H0, H1] + S
    if run_inner(2, sregs_test) == 1:
        print(f"  S7 = 0x{s7:04X}")
        found_s7 = True
        break
if not found_s7:
    print("  S7 NOT FOUND!")

serial_str = '-'.join(f'{s:04X}' for s in S)
print(f"\nSerial: {serial_str}")

# Test against binary
print(f"\nTesting against binary...")
binary = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"
inp = f"{username}\n{serial_str}\n"
try:
    r = subprocess.run([binary], input=inp, capture_output=True, text=True, timeout=10)
    if "Access Granted" in r.stdout:
        print("RESULT: Access Granted!")
    elif "Invalid" in r.stdout:
        print("RESULT: Invalid License :(")
    else:
        lines = r.stdout.strip().split('\n')
        print(f"RESULT: {lines[-1].strip()}")
except Exception as e:
    print(f"Error: {e}")
