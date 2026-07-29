#!/usr/bin/env python3
"""Debug inner VM #0 to understand why it accepts S5=0."""

def decrypt_bc(data_hex, key_bytes, length):
    data = bytes.fromhex(data_hex)
    return bytearray(data[i] ^ key_bytes[i & 3] for i in range(length))

bc_vm0 = decrypt_bc("DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF",
                     [0xDE, 0xAD, 0xBE, 0xEF], 0x21)

print("VM2 #0 bytecode:", ' '.join(f'{b:02x}' for b in bc_vm0))

# src = [H0, H1, S0, S1, S3, S5]
H0, H1 = 0xaa39, 0xcd44
S0, S1, S3, S5 = 0x44aa, 0x322b, 0xb7ad, 0x0000
src = [H0, H1, S0, S1, S3, S5]

bc = bc_vm0
num = 6
maxlen = 0x21

op_names = {0:"PUSH_REG",1:"PUSH_IMM",2:"ADD",3:"SUB",4:"MUL",5:"XOR",
            6:"AND",7:"OR",8:"ROL16",9:"ROR16",0xa:"EQ",0xb:"DUP",
            0xc:"SWAP",0xd:"NOT16",0xe:"TRUNC16",0xf:"DONE_TRUE",
            0x10:"DONE_FALSE",0x11:"JNZ",0x12:"JZ",0x13:"DROP",
            0x14:"CRC16",0x15:"SHL16",0x16:"SHR16"}

stack = [0]*128; sp = -1; pc = 0
for iter in range(100):
    if pc >= maxlen:
        print(f"  ** OUT OF BOUNDS pc={pc}")
        break
    raw = bc[pc]; op = raw - 1
    if op > 0x16 or op < 0:
        print(f"  [{pc:02x}] raw={raw:02x} op={op} INVALID")
        break
    
    name = op_names.get(op, f"?{op}")
    
    if op == 0:
        idx = bc[pc+1]
        if sp >= 0x7f or idx >= num:
            print(f"  [{pc:02x}] PUSH_REG idx={idx} OVERFLOW (sp={sp}, num={num})"); break
        sp += 1; stack[sp] = src[idx]&0xFFFFFFFF
        src_names = ["H0","H1","S0","S1","S3","S5"]
        print(f"  [{pc:02x}] PUSH_REG {src_names[idx]}={src[idx]:04x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 2
    elif op == 1:
        imm = (bc[pc+2]<<8)|bc[pc+1]
        sp += 1; stack[sp] = imm
        print(f"  [{pc:02x}] PUSH_IMM 0x{imm:04x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 3
    elif op == 2:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = (a+b)&0xFFFFFFFF; sp -= 1
        print(f"  [{pc:02x}] ADD 0x{a:x}+0x{b:x}=0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 3:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = (a-b)&0xFFFFFFFF; sp -= 1
        print(f"  [{pc:02x}] SUB 0x{a:x}-0x{b:x}=0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 4:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = (b*a)&0xFFFFFFFF; sp -= 1
        print(f"  [{pc:02x}] MUL 0x{b:x}*0x{a:x}=0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 5:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = a^b; sp -= 1
        print(f"  [{pc:02x}] XOR 0x{a:x}^0x{b:x}=0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 6:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = a&b; sp -= 1
        print(f"  [{pc:02x}] AND 0x{a:x}&0x{b:x}=0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 9:
        s_val = stack[sp]&0xf; v = stack[sp-1]&0xFFFF
        r = ((v>>s_val)|(v<<(16-s_val)))&0xFFFF
        sp -= 1; stack[sp] = r
        print(f"  [{pc:02x}] ROR16 0x{v:04x} >> {s_val} = 0x{r:04x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 0xa:
        a,b = stack[sp-1], stack[sp]
        stack[sp-1] = 1 if b==a else 0; sp -= 1
        print(f"  [{pc:02x}] EQ 0x{b:x}==0x{a:x} => {stack[sp]}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 0xe:
        old = stack[sp]; stack[sp] &= 0xFFFF
        print(f"  [{pc:02x}] TRUNC16 0x{old:x} => 0x{stack[sp]:x}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc += 1
    elif op == 0xf:
        print(f"  [{pc:02x}] DONE_TRUE")
        break
    elif op == 0x10:
        print(f"  [{pc:02x}] DONE_FALSE")
        break
    elif op == 0x12:
        t = (bc[pc+2]<<8)|bc[pc+1]; v = stack[sp]; sp -= 1
        jumped = not v
        print(f"  [{pc:02x}] JZ {t:04x} (top={v}) => {'JUMP' if jumped else 'SKIP'}  stack:{[f'{stack[i]:x}' for i in range(sp+1)]}")
        pc = t if jumped else pc+3
    else:
        print(f"  [{pc:02x}] {name} -- NOT TRACED")
        break
