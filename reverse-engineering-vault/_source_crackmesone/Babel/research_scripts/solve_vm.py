#!/usr/bin/env python3
"""Full VM trace that finds correct serial by setting S[i] = expected values at each CMP."""

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

def crc16(value):
    value &= 0xFFFF
    for _ in range(16):
        if value & 1: value = (value >> 1) ^ 0xA001
        else: value >>= 1
    return value & 0xFFFF

class FullVM:
    def __init__(self, main_bc_hex, key_main, inner_bc_defs):
        self.main_bc = decrypt_bc(main_bc_hex, key_main, 0x263)
        self.inner_bcs = []
        for d in inner_bc_defs:
            self.inner_bcs.append({
                'bc': decrypt_bc(d['hex'], d['key'], d['len']),
                'num_src': d['num_src'],
                'max_len': d['len'],
                'src_fn': d['src_fn'],
            })
        self.ot = bytes.fromhex("071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01")
    
    def find_serial(self, username, verbose=False):
        h = murmur_hash(username)
        H0 = h & 0xFFFF
        H1 = (h >> 16) & 0xFFFF
        
        # We'll run the VM with dummy serial, intercepting each CMP to learn
        # expected values, then re-run with those values.
        # Strategy: run multiple passes, each time setting the correct S[i] as we discover them.
        
        serial = [0]*8
        
        for pass_num in range(10):
            sregs = [H0, H1] + serial
            result, discovered = self._run(bytearray(self.main_bc), sregs, verbose and pass_num >= 8)
            
            if result[0] == 1:
                return serial, result
            
            # Update serial with any discovered values
            changed = False
            for i, v in discovered.items():
                if serial[i] != v:
                    serial[i] = v
                    changed = True
            
            if not changed:
                break
        
        return serial, result
    
    def _run(self, bc, sregs, verbose):
        regs = [0]*8
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
        ot = self.ot
        
        discovered = {}  # sreg_index -> expected value
        cmp_count = 0
        
        for step in range(200000):
            if halt or vpc >= len(bc):
                break
            
            raw = bc[vpc]
            if raw >= len(ot):
                halt = True; break
            case = ot[raw]
            
            op1 = bc[vpc+1] if vpc+1 < len(bc) else 0
            op2 = bc[vpc+2] if vpc+2 < len(bc) else 0
            op3 = bc[vpc+3] if vpc+3 < len(bc) else 0
            imm16 = (op3 << 8) | op2
            old_vpc = vpc
            
            if case == 0: vpc += 1
            elif case == 1: regs[op1] = imm16; vpc += 4
            elif case == 2: regs[op1] = sregs[op2] if op2 < len(sregs) else 0; vpc += 3
            elif case == 3: regs[op1] = regs[op2]; vpc += 3
            elif case == 4: regs[op1] = (regs[op1]+regs[op2])&0xFFFFFFFF; vpc += 3
            elif case == 5: regs[op1] = (regs[op1]-regs[op2])&0xFFFFFFFF; vpc += 3
            elif case == 6: regs[op1] = (regs[op1]*regs[op2])&0xFFFFFFFF; vpc += 3
            elif case == 7: regs[op1] ^= regs[op2]; vpc += 3
            elif case == 8: regs[op1] &= regs[op2]; vpc += 3
            elif case == 9: regs[op1] |= regs[op2]; vpc += 3
            elif case == 0xa: regs[op1] = (regs[op1]<<(op2&0x1f))&0xFFFFFFFF; vpc += 3
            elif case == 0xb: regs[op1] >>= (op2&0x1f); vpc += 3
            elif case == 0xc: regs[op1] = (~regs[op1])&0xFFFFFFFF; vpc += 2
            elif case == 0xd:
                # CMP reg, reg. Before the actual comparison, check if one of the regs
                # contains a sreg value (serial word). If this is a serial check,
                # we can derive what the expected value is.
                flag = 1 if regs[op1] == regs[op2] else 0
                cmp_count += 1
                
                if flag == 0:
                    # Peek at the next instruction - is it JZ to failure?
                    if vpc+3 < len(bc):
                        next_raw = bc[vpc+3]
                        if next_raw < len(ot) and ot[next_raw] == 0x10:  # JZ
                            target = (bc[vpc+6] << 8) | bc[vpc+4]
                            if target == 0x0254:  # failure target
                                # r[op1] is the computed value, r[op2] is the serial word
                                # (or vice versa). Try to figure out which sreg was loaded.
                                expected = regs[op1]
                                # The serial word is the one that was loaded from sregs
                                # We need to find which sregs[2+i] was loaded into
                                # which register more recently
                                if verbose:
                                    print(f"  CMP #{cmp_count}: r{op1}(0x{regs[op1]:04x}) vs r{op2}(0x{regs[op2]:04x}), expected=0x{expected:04x}")
                                
                                # Set the serial word to what VM expects
                                for si in range(8):
                                    if sregs[2+si] == regs[op2]:
                                        discovered[si] = regs[op1] & 0xFFFF
                                        sregs[2+si] = regs[op1] & 0xFFFF
                                        regs[op2] = regs[op1]
                                        flag = 1
                                        break
                                else:
                                    for si in range(8):
                                        if sregs[2+si] == regs[op1]:
                                            discovered[si] = regs[op2] & 0xFFFF
                                            sregs[2+si] = regs[op2] & 0xFFFF
                                            regs[op1] = regs[op2]
                                            flag = 1
                                            break
                
                vpc += 3
            elif case == 0xe: vpc = (op2<<8)|op1
            elif case == 0xf:
                t = (op2<<8)|op1
                vpc = t if flag else vpc+3
            elif case == 0x10:
                t = (op2<<8)|op1
                vpc = t if not flag else vpc+3
            elif case == 0x11:
                vsp += 1; vstack[vsp] = regs[op1]; vpc += 2
            elif case == 0x12:
                if vsp >= 0: regs[op1] = vstack[vsp]; vsp -= 1
                vpc += 2
            elif case == 0x13: out[op1] = regs[op2]; vpc += 3
            elif case == 0x14: halt = True; vpc += 1
            elif case == 0x15: regs[op1] = (regs[op1]+imm16)&0xFFFFFFFF; vpc += 4
            elif case == 0x16: regs[op1] ^= imm16; vpc += 4
            elif case == 0x17: regs[op1] &= imm16; vpc += 4
            elif case == 0x18:
                s = op2&0x1f; v = regs[op1]
                regs[op1] = ((v<<s)|(v>>(32-s)))&0xFFFFFFFF; vpc += 3
            elif case == 0x19:
                s = op2&0x1f; v = regs[op1]
                regs[op1] = ((v>>s)|(v<<(32-s)))&0xFFFFFFFF; vpc += 3
            elif case == 0x1a:
                t = (op2<<8)|op1; csp += 1; cstack[csp] = vpc+3; vpc = t
            elif case == 0x1b:
                if csp >= 0: vpc = cstack[csp]; csp -= 1
                else: halt = True
            elif case == 0x1c: regs[op1] = (regs[op1]*imm16)&0xFFFFFFFF; vpc += 4
            elif case == 0x1d:
                flag = 1 if regs[op1] == imm16 else 0
                
                # INVOKE_VM2 result check: CMP_IMM r0, 0x0001
                if flag == 0 and imm16 == 1 and op1 == 0:
                    # Inner VM returned 0 (failure). We can't easily fix this here -
                    # inner VMs need correct serial words from the start.
                    if verbose:
                        print(f"  CMP_IMM #{cmp_count}: r{op1}(0x{regs[op1]:04x}) vs 0x{imm16:04x} => INNER VM FAIL")
                
                vpc += 4
            elif case == 0x1e: regs[op1] = (regs[op1]-imm16)&0xFFFFFFFF; vpc += 4
            elif case == 0x1f: regs[op1],regs[op2] = regs[op2],regs[op1]; vpc += 3
            elif case == 0x20:
                result = self._run_inner(op1, regs, sregs, out)
                regs[0] = result
                vpc += 2
            elif case == 0x21:
                offset = (op2<<8)|op1
                if offset < len(bc): bc[offset] = regs[op3]&0xFF
                vpc += 4
            elif case == 0x22: regs[op1] = iter_count; vpc += 2
            elif case == 0x23: regs[op1] |= imm16; vpc += 4
            elif case == 0x24:
                v = regs[op1]^regs[op2]; v &= 0xFFFF
                for _ in range(16):
                    if v&1: v = (v>>1)^0xA001
                    else: v >>= 1
                regs[op1] = v&0xFFFF; vpc += 3
            elif case == 0x25: regs[op1] = acc; vpc += 2
            elif case == 0x26: acc = regs[op1]; vpc += 2
            elif case == 0x27:
                v = regs[op1]&0xFFFF
                if v&1: regs[op1] = ((v>>1)^0xB400)&0xFFFF
                else: regs[op1] = (v>>1)&0xFFFF
                vpc += 2
            else:
                halt = True
            
            iter_count += 1
        
        return out, discovered
    
    def _run_inner(self, which, regs, sregs, out):
        if which >= len(self.inner_bcs):
            return 0
        
        info = self.inner_bcs[which]
        bc = info['bc']
        src = info['src_fn'](regs, sregs, out)
        num = info['num_src']
        maxlen = info['max_len']
        
        stack = [0]*128
        sp = -1
        pc = 0
        
        for _ in range(4096):
            if pc >= maxlen: return 0
            raw = bc[pc]
            op = raw - 1
            if op > 0x16 or op < 0: return 0
            
            if op == 0:
                idx = bc[pc+1]
                if sp >= 0x7f or idx >= num: return 0
                sp += 1; stack[sp] = src[idx]&0xFFFFFFFF; pc += 2
            elif op == 1:
                imm = (bc[pc+2]<<8)|bc[pc+1]
                if sp >= 0x7f: return 0
                sp += 1; stack[sp] = imm; pc += 3
            elif op == 2:
                if sp < 1: return 0
                stack[sp-1] = (stack[sp-1]+stack[sp])&0xFFFFFFFF; sp -= 1; pc += 1
            elif op == 3:
                if sp < 1: return 0
                stack[sp-1] = (stack[sp-1]-stack[sp])&0xFFFFFFFF; sp -= 1; pc += 1
            elif op == 4:
                if sp < 1: return 0
                stack[sp-1] = (stack[sp]*stack[sp-1])&0xFFFFFFFF; sp -= 1; pc += 1
            elif op == 5:
                if sp < 1: return 0
                stack[sp-1] ^= stack[sp]; sp -= 1; pc += 1
            elif op == 6:
                if sp < 1: return 0
                stack[sp-1] &= stack[sp]; sp -= 1; pc += 1
            elif op == 7:
                if sp < 1: return 0
                stack[sp-1] |= stack[sp]; sp -= 1; pc += 1
            elif op == 8:
                if sp < 1: return 0
                s = stack[sp]&0xf; v = stack[sp-1]&0xFFFF
                stack[sp-1] = ((v<<s)|(v>>(16-s)))&0xFFFF; sp -= 1; pc += 1
            elif op == 9:
                if sp < 1: return 0
                s = stack[sp]&0xf; v = stack[sp-1]&0xFFFF
                stack[sp-1] = ((v>>s)|(v<<(16-s)))&0xFFFF; sp -= 1; pc += 1
            elif op == 0xa:
                if sp < 1: return 0
                stack[sp-1] = 1 if stack[sp]==stack[sp-1] else 0; sp -= 1; pc += 1
            elif op == 0xb:
                if sp >= 0x7f: return 0
                sp += 1; stack[sp] = stack[sp-1]; pc += 1
            elif op == 0xc:
                if sp < 1: return 0
                stack[sp],stack[sp-1] = stack[sp-1],stack[sp]; pc += 1
            elif op == 0xd:
                if sp < 0: return 0
                stack[sp] = (~stack[sp])&0xFFFF; pc += 1
            elif op == 0xe:
                if sp < 0: return 0
                stack[sp] &= 0xFFFF; pc += 1
            elif op == 0xf: return 1
            elif op == 0x10: return 0
            elif op == 0x11:
                if sp < 0: return 0
                t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
                pc = t if v else pc+3
            elif op == 0x12:
                if sp < 0: return 0
                t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
                pc = t if not v else pc+3
            elif op == 0x13:
                if sp < 0: return 0
                sp -= 1; pc += 1
            elif op == 0x14:
                if sp < 1: return 0
                v = stack[sp-1]^stack[sp]; v &= 0xFFFF
                for _ in range(16):
                    if v&1: v = (v>>1)^0xA001
                    else: v >>= 1
                stack[sp-1] = v&0xFFFF; sp -= 1; pc += 1
            elif op == 0x15:
                if sp < 1: return 0
                s = stack[sp]&0xf; stack[sp-1] = (stack[sp-1]<<s)&0xFFFF; sp -= 1; pc += 1
            elif op == 0x16:
                if sp < 1: return 0
                s = stack[sp]&0xf; stack[sp-1] = (stack[sp-1]>>s)&0xFFFF; sp -= 1; pc += 1
            else: return 0
        
        return 0


# ============================================================
# Run and discover serial
# ============================================================

main_bc_hex = "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000"
key_main = [0x5A, 0x1C, 0xBE, 0xB4]

def vm2_0_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[5], sregs[7]]

def vm2_1_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[4], sregs[5], sregs[6], sregs[7], sregs[8]]

def vm2_2_src(regs, sregs, out):
    return [sregs[0], sregs[1], sregs[2], sregs[3], sregs[4], sregs[5], sregs[6], sregs[7], sregs[8], sregs[9]]

inner_defs = [
    {'hex': "DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF",
     'key': [0xDE, 0xAD, 0xBE, 0xEF], 'len': 0x21, 'num_src': 6, 'src_fn': vm2_0_src},
    {'hex': "CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB",
     'key': [0xCA, 0xFE, 0xBA, 0xBE], 'len': 0x27, 'num_src': 9, 'src_fn': vm2_1_src},
    {'hex': "1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02",
     'key': [0x13, 0x37, 0xC0, 0xDE], 'len': 0x29, 'num_src': 10, 'src_fn': vm2_2_src},
]

vm = FullVM(main_bc_hex, key_main, inner_defs)

import sys
username = sys.argv[1] if len(sys.argv) > 1 else "test"
serial, result = vm.find_serial(username, verbose=True)

h = murmur_hash(username)
H0 = h & 0xFFFF
H1 = (h >> 16) & 0xFFFF

serial_str = '-'.join(f'{s:04X}' for s in serial)
print(f"\nUsername: {username}")
print(f"Hash: 0x{h:08x} (H0=0x{H0:04x}, H1=0x{H1:04x})")
print(f"Serial: {serial_str}")
print(f"VM result: out[0]={result[0]}, out[1]=0x{result[1]:08x}")

if result[0] == 1:
    print("SUCCESS - VM accepted the serial!")
else:
    print("FAIL - VM rejected. Need to debug inner VM constraints.")
    # Try to test against the real binary anyway
    import subprocess
    binary = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"
    inp = f"{username}\n{serial_str}\n"
    try:
        r = subprocess.run([binary], input=inp, capture_output=True, text=True, timeout=10)
        print(f"Binary output: {r.stdout.strip()}")
    except:
        pass
