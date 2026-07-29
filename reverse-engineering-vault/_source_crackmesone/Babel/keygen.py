#!/usr/bin/env python3
"""
BABEL_VM Keygen - CrackMe by w33d
===================================
Multi-layer VM architecture reverse engineered from babel_vm.exe.

Architecture:
  - Outer state machine drives multiple phases (hash, decrypt, VM exec, verify)
  - Primary VM: Register-based (8 GPRs, 10 source regs, flags, accumulator)
  - 3x Secondary VMs: Stack-based sub-programs invoked from the primary VM
  - XOR-encrypted bytecodes decrypted at runtime from magic constants

Serial format: XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
Username: 4-64 ASCII characters

S0-S4: derived by primary VM from username hash
S5-S7: derived by secondary stack VMs from hash + S0-S4
"""

import sys, subprocess

# ============================================================
# Crypto primitives (matching binary implementations)
# ============================================================

def murmur_hash(username):
    """Murmur-like hash with seed 0x42414245 ('BABE')."""
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
    """XOR-decrypt bytecode with 4-byte repeating key."""
    data = bytes.fromhex(data_hex)
    return bytearray(data[i] ^ key_bytes[i & 3] for i in range(length))


# ============================================================
# Encrypted bytecodes & opcode dispatch table
# ============================================================

MAIN_BC_HEX = (
    "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA8"
    "0E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB"
    "591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB6"
    "5A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A8"
    "0E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB"
    "591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB4"
    "5B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB4"
    "7C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B0"
    "5B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B4"
    "5813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB"
    "5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4B"
    "A511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5"
    "591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5"
    "551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD"
    "5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF93"
    "59116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB3"
    "5B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB0"
    "5D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB4"
    "5A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE95"
    "5B1BB5000000000000000000"
)
MAIN_KEY  = [0x5A, 0x1C, 0xBE, 0xB4]
MAIN_LEN  = 0x263

VM2_DEFS = [
    # VM2 #0: constrains S5 | src = [H0,H1,S0,S1,S3,S5]
    {"hex": "DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF",
     "key": [0xDE,0xAD,0xBE,0xEF], "len": 0x21, "num": 6,
     "src": lambda s: [s[0],s[1],s[2],s[3],s[5],s[7]]},
    # VM2 #1: constrains S6 | src = [H0,H1,S0..S5,S6]
    {"hex": "CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB",
     "key": [0xCA,0xFE,0xBA,0xBE], "len": 0x27, "num": 9,
     "src": lambda s: s[:9]},
    # VM2 #2: constrains S7 | src = [H0,H1,S0..S6,S7]
    {"hex": "1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02",
     "key": [0x13,0x37,0xC0,0xDE], "len": 0x29, "num": 10,
     "src": lambda s: s[:10]},
]

OT = bytes.fromhex(
    "071826171C2003220527211411040B02"
    "2423191B090A1D001F16120E10061A1E"
    "1513250F080D0C01"
)


# ============================================================
# Inner (stack-based) VM executor
# ============================================================

def run_inner(which, sregs):
    """Execute secondary stack VM. Returns 1 on success, 0 on failure."""
    d   = VM2_DEFS[which]
    bc  = decrypt_bc(d["hex"], d["key"], d["len"])
    src = d["src"](sregs)
    num = d["num"];  maxlen = d["len"]
    stk = [0]*128;   sp = -1;  pc = 0

    for _ in range(4096):
        if pc >= maxlen: return 0
        op = bc[pc] - 1
        if op > 0x16 or op < 0: return 0

        if   op == 0x00:                                       # PUSH_REG
            idx = bc[pc+1]
            if sp >= 0x7f or idx >= num: return 0
            sp += 1;  stk[sp] = src[idx] & 0xFFFFFFFF;  pc += 2
        elif op == 0x01:                                       # PUSH_IMM16
            sp += 1;  stk[sp] = (bc[pc+2]<<8)|bc[pc+1];  pc += 3
        elif op == 0x02:                                       # ADD
            stk[sp-1] = (stk[sp-1]+stk[sp])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 0x03:                                       # SUB
            stk[sp-1] = (stk[sp-1]-stk[sp])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 0x04:                                       # MUL
            stk[sp-1] = (stk[sp]*stk[sp-1])&0xFFFFFFFF; sp -= 1; pc += 1
        elif op == 0x05:                                       # XOR
            stk[sp-1] ^= stk[sp];                      sp -= 1; pc += 1
        elif op == 0x06:                                       # AND
            stk[sp-1] &= stk[sp];                      sp -= 1; pc += 1
        elif op == 0x07:                                       # OR
            stk[sp-1] |= stk[sp];                      sp -= 1; pc += 1
        elif op == 0x08:                                       # ROL16
            s = stk[sp]&0xf; v = stk[sp-1]&0xFFFF
            stk[sp-1] = ((v<<s)|(v>>(16-s)))&0xFFFF;   sp -= 1; pc += 1
        elif op == 0x09:                                       # ROR16
            s = stk[sp]&0xf; v = stk[sp-1]&0xFFFF
            stk[sp-1] = ((v>>s)|(v<<(16-s)))&0xFFFF;   sp -= 1; pc += 1
        elif op == 0x0a:                                       # EQ
            stk[sp-1] = 1 if stk[sp]==stk[sp-1] else 0; sp -= 1; pc += 1
        elif op == 0x0b:                                       # DUP
            sp += 1; stk[sp] = stk[sp-1]; pc += 1
        elif op == 0x0c:                                       # SWAP
            stk[sp],stk[sp-1] = stk[sp-1],stk[sp]; pc += 1
        elif op == 0x0d:                                       # NOT16
            stk[sp] = (~stk[sp])&0xFFFF; pc += 1
        elif op == 0x0e:                                       # TRUNC16
            stk[sp] &= 0xFFFF; pc += 1
        elif op == 0x0f: return 1                              # DONE_TRUE
        elif op == 0x10: return 0                              # DONE_FALSE
        elif op == 0x11:                                       # JZ
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stk[sp]; sp -= 1
            pc = t if not v else pc+3
        elif op == 0x12:                                       # JNZ
            t = (bc[pc+2]<<8)|bc[pc+1]; v = stk[sp]; sp -= 1
            pc = t if v else pc+3
        elif op == 0x13:  sp -= 1; pc += 1                    # DROP
        elif op == 0x14:                                       # CRC16
            v = stk[sp-1]^stk[sp]; v &= 0xFFFF
            for _ in range(16):
                v = (v>>1)^0xA001 if v&1 else v>>1
            stk[sp-1] = v&0xFFFF; sp -= 1; pc += 1
        elif op == 0x15:                                       # SHL16
            s = stk[sp]&0xf
            stk[sp-1] = (stk[sp-1]<<s)&0xFFFF; sp -= 1; pc += 1
        elif op == 0x16:                                       # SHR16
            s = stk[sp]&0xf
            stk[sp-1] = (stk[sp-1]>>s)&0xFFFF; sp -= 1; pc += 1
        else: return 0
    return 0


# ============================================================
# Primary (register-based) VM executor  --  auto-discovery mode
# ============================================================

def discover_serial(H0, H1):
    """Run the primary VM with CMP auto-patching to discover S0-S4,
       then brute-force S5/S6/S7 through the inner VMs."""

    bc   = decrypt_bc(MAIN_BC_HEX, MAIN_KEY, MAIN_LEN)
    regs = [0]*8
    sentinels = [0xFE01+i for i in range(8)]
    sregs = [H0, H1] + sentinels
    out  = [0]*8
    flag = 0;  acc = 0xDEAD;  vpc = 0
    vstk = [0]*256;  vsp = -1
    cstk = [0]*32;   csp = -1
    icount = 0
    last_sr = {}                        # reg -> sreg index tracking

    for _ in range(200_000):
        if vpc >= len(bc): break
        raw = bc[vpc]
        if raw >= len(OT): break
        c = OT[raw]
        o1 = bc[vpc+1] if vpc+1<len(bc) else 0
        o2 = bc[vpc+2] if vpc+2<len(bc) else 0
        o3 = bc[vpc+3] if vpc+3<len(bc) else 0
        imm = (o3<<8)|o2
        clr = lambda r: last_sr.pop(r, None)

        if   c==0x00: vpc+=1
        elif c==0x01: regs[o1]=imm; clr(o1); vpc+=4
        elif c==0x02: regs[o1]=sregs[o2] if o2<len(sregs) else 0; last_sr[o1]=o2; vpc+=3
        elif c==0x03:
            regs[o1]=regs[o2]
            if o2 in last_sr: last_sr[o1]=last_sr[o2]
            else: clr(o1)
            vpc+=3
        elif c==0x04: regs[o1]=(regs[o1]+regs[o2])&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x05: regs[o1]=(regs[o1]-regs[o2])&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x06: regs[o1]=(regs[o1]*regs[o2])&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x07: regs[o1]^=regs[o2]; clr(o1); vpc+=3
        elif c==0x08: regs[o1]&=regs[o2]; clr(o1); vpc+=3
        elif c==0x09: regs[o1]|=regs[o2]; clr(o1); vpc+=3
        elif c==0x0a: regs[o1]=(regs[o1]<<(o2&0x1f))&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x0b: regs[o1]>>=o2&0x1f; clr(o1); vpc+=3
        elif c==0x0c: regs[o1]=(~regs[o1])&0xFFFFFFFF; clr(o1); vpc+=2
        elif c==0x0d:                                          # CMP reg,reg
            flag = 1 if regs[o1]==regs[o2] else 0
            if not flag:
                r1s,r2s = last_sr.get(o1), last_sr.get(o2)
                if r2s is not None and r2s>=2:
                    sregs[r2s]=regs[o1]&0xFFFF; regs[o2]=regs[o1]; flag=1
                elif r1s is not None and r1s>=2:
                    sregs[r1s]=regs[o2]&0xFFFF; regs[o1]=regs[o2]; flag=1
            vpc+=3
        elif c==0x0e: vpc=(o2<<8)|o1
        elif c==0x0f: t=(o2<<8)|o1; vpc=t if flag else vpc+3
        elif c==0x10: t=(o2<<8)|o1; vpc=t if not flag else vpc+3
        elif c==0x11: vsp+=1; vstk[vsp]=regs[o1]; vpc+=2
        elif c==0x12:
            if vsp>=0: regs[o1]=vstk[vsp]; vsp-=1
            clr(o1); vpc+=2
        elif c==0x13: out[o1]=regs[o2]; vpc+=3
        elif c==0x14: break                                    # HALT
        elif c==0x15: regs[o1]=(regs[o1]+imm)&0xFFFFFFFF; clr(o1); vpc+=4
        elif c==0x16: regs[o1]^=imm; clr(o1); vpc+=4
        elif c==0x17: regs[o1]&=imm; clr(o1); vpc+=4
        elif c==0x18:
            s=o2&0x1f; v=regs[o1]
            regs[o1]=((v<<s)|(v>>(32-s)))&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x19:
            s=o2&0x1f; v=regs[o1]
            regs[o1]=((v>>s)|(v<<(32-s)))&0xFFFFFFFF; clr(o1); vpc+=3
        elif c==0x1a: t=(o2<<8)|o1; csp+=1; cstk[csp]=vpc+3; vpc=t
        elif c==0x1b:
            if csp>=0: vpc=cstk[csp]; csp-=1
            else: break
        elif c==0x1c: regs[o1]=(regs[o1]*imm)&0xFFFFFFFF; clr(o1); vpc+=4
        elif c==0x1d: flag=1 if regs[o1]==imm else 0; vpc+=4
        elif c==0x1e: regs[o1]=(regs[o1]-imm)&0xFFFFFFFF; clr(o1); vpc+=4
        elif c==0x1f:
            regs[o1],regs[o2]=regs[o2],regs[o1]
            s1=last_sr.pop(o1,None); s2=last_sr.pop(o2,None)
            if s1 is not None: last_sr[o2]=s1
            if s2 is not None: last_sr[o1]=s2
            vpc+=3
        elif c==0x20:
            regs[0]=run_inner(o1, sregs); clr(0); vpc+=2
        elif c==0x21:
            off=(o2<<8)|o1
            if off<len(bc): bc[off]=regs[o3]&0xFF
            vpc+=4
        elif c==0x22: regs[o1]=icount; clr(o1); vpc+=2
        elif c==0x23: regs[o1]|=imm; clr(o1); vpc+=4
        elif c==0x24:
            v=regs[o1]^regs[o2]; v&=0xFFFF
            for _ in range(16): v=(v>>1)^0xA001 if v&1 else v>>1
            regs[o1]=v&0xFFFF; clr(o1); vpc+=3
        elif c==0x25: regs[o1]=acc; clr(o1); vpc+=2
        elif c==0x26: acc=regs[o1]; vpc+=2
        elif c==0x27:
            v=regs[o1]&0xFFFF
            regs[o1]=((v>>1)^0xB400)&0xFFFF if v&1 else (v>>1)&0xFFFF
            clr(o1); vpc+=2
        else: break
        icount+=1

    S = [sregs[2+i] for i in range(8)]

    # --- Brute-force S5, S6, S7 through inner VMs ---
    for vm_idx, si in [(0,5), (1,6), (2,7)]:
        for candidate in range(0x10000):
            S[si] = candidate
            if run_inner(vm_idx, [H0, H1] + S) == 1:
                break
        else:
            S[si] = 0  # fallback (should never happen)

    return S


# ============================================================
# Public API
# ============================================================

def keygen(username):
    """Generate a valid serial for the given username."""
    h  = murmur_hash(username)
    H0 = h & 0xFFFF
    H1 = (h >> 16) & 0xFFFF
    S  = discover_serial(H0, H1)
    return '-'.join(f'{w:04X}' for w in S), S, h


def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username (4-64 chars): ").strip()

    if len(username) < 4 or len(username) > 64:
        print(f"Error: Username must be 4-64 characters (got {len(username)})")
        sys.exit(1)

    serial_str, S, h = keygen(username)
    H0, H1 = h & 0xFFFF, (h >> 16) & 0xFFFF

    print()
    print("  " + "=" * 54)
    print("   BABEL_VM Keygen - CrackMe by w33d")
    print("  " + "=" * 54)
    print(f"   Username : {username}")
    print(f"   Hash     : 0x{h:08X}  (H0=0x{H0:04X}, H1=0x{H1:04X})")
    print(f"   Serial   : {serial_str}")
    print("  " + "=" * 54)


if __name__ == "__main__":
    main()
