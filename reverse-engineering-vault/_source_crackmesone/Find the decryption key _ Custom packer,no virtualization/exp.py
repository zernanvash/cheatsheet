#exp.py

cipher = bytes([
    0xD8, 0xCA, 0x7B, 0xDA, 0x48, 0x1C, 0xEA, 0xEE,
    0x42, 0xA4, 0xF4, 0xD3, 0xEE, 0xA6, 0xD1, 0x74,
    0xBC, 0x4D, 0xAA, 0xA5, 0x3E, 0xBF, 0xC1, 0x6A,
    0x57, 0x80, 0xB5, 0xA8, 0x3E, 0xF5, 0x5D, 0x20
])

def rol(x, n):
    x &= 0xFF
    return ((x << n) | (x >> (8 - n))) & 0xFF

def ror(x, n):
    x &= 0xFF
    return ((x >> n) | (x << (8 - n))) & 0xFF

def decrypt(key):
    key_bytes = key if isinstance(key, bytes) else key.encode()
    v19 = bytearray(32)
    v21 = 1
    while True:
        v6 = v21
        v7 = 27 * (v6 - 1)
        v8 = ((v6 - 1) & 3) + 1
        v9 = (v6 & 3) + 1
        v10 = -98 * (v6 - 1)
        v11 = 7 * (v6 - 1)
        # v19[v6-1]
        i = v6 - 1
        v19[i] = (cipher[i] ^ (v11 + ((v10 + 55) ^ rol(key_bytes[i % 5] ^ (v7 - 91), v8)))) & 0xFF
        # v19[v6]
        i = v6
        v19[i] = (cipher[i] ^ (v11 + ((v10 - 43) ^ rol(key_bytes[i % 5] ^ (v7 - 64), v9)) + 7)) & 0xFF
        # v19[v6+1]
        i = v6 + 1
        v14 = ((v6 + 1) & 3) + 1
        idx_key = (v6 - 1) - 5 * ((v6 + 1) // 5) + 2
        v19[i] = (cipher[i] ^ (v11 + ((v10 + 115) ^ rol(key_bytes[idx_key] ^ (v7 - 37), v14)) + 14)) & 0xFF
        # v19[v21+2]
        i = v21 + 2
        idx_key = (v21 - 1) - 5 * ((v21 + 2) // 5) + 3
        v19[i] = (cipher[i] ^ (7 * (v21 + 2) + ((17 - 98 * (v21 - 1)) ^ rol(key_bytes[idx_key] ^ (v7 - 10), ((v21 - 2) & 3) + 1)))) & 0xFF
        # v19[v21+3]
        i = v21 + 3
        idx_key = (v21 - 1) - 5 * ((v21 + 3) // 5) + 4
        v19[i] = (cipher[i] ^ (7 * (v21 + 3) + ((-81 - 98 * (v21 - 1)) ^ rol(key_bytes[idx_key] ^ (v7 + 17), v8)))) & 0xFF
        # v19[v21+4]
        i = v21 + 4
        t = (v21 + 4) // 5
        idx_key = v21 + 4 * (1 - t) - t
        v19[i] = (cipher[i] ^ (7 * (v21 + 4) + ((77 - 98 * (v21 - 1)) ^ rol(key_bytes[idx_key] ^ (v7 + 44), v9)))) & 0xFF
        # v19[v21+5]
        i = v21 + 5
        idx_key = (v21 - 1) - 5 * ((v21 + 5) // 5) + 6
        v19[i] = (cipher[i] ^ (7 * (v21 + 5) + ((-21 - 98 * (v21 - 1)) ^ rol(key_bytes[idx_key] ^ (v7 + 71), v14)))) & 0xFF
        # v19[v21+6]
        i = v21 + 6
        idx_key = (v21 - 1) - 5 * ((v21 + 6) // 5) + 7
        v19[i] = (cipher[i] ^ (7 * (v21 + 6) + ((-119 - 98 * (v21 - 1)) ^ rol(key_bytes[idx_key] ^ (v7 + 98), ((v21 - 2) & 3) + 1)))) & 0xFF
        
        v6 = v21 + 8
        v21 += 8
        if (v21 - 8) + 7 >= 32:  
            break
    return bytes(v19)

def recover_key_from_prefix(prefix):

    key = bytearray(5)

    

    i = 0
    expected = prefix[0]
    K0 = cipher[0] ^ expected
    # K0 = v11 + ((v10+55) ^ rol(key[0] ^ (v7-91), v8))  v11=0,v10=0,v7=0,v8=1
    # K0 = (55 ^ rol(key[0] ^ 165, 1))
    rol_val = 55 ^ K0
    # rol_val = rol(key[0] ^ 165, 1)
    key0_xor = ror(rol_val, 1)
    key[0] = key0_xor ^ 165
    

    i = 1
    expected = prefix[1]
    K1 = cipher[1] ^ expected
    # K1 = v11 + ((v10-43) ^ rol(key[1] ^ (v7-64), v9)) + 7 = (213 ^ rol(key[1]^192, 2)) + 7
    tmp = K1 - 7
    rol_val = 213 ^ tmp
    key1_xor = ror(rol_val, 2)
    key[1] = key1_xor ^ 192
    

    i = 2
    expected = prefix[2]
    K2 = cipher[2] ^ expected
    # K2 = v11 + ((v10+115) ^ rol(key[2]^ (v7-37), v14)) + 14 = (115 ^ rol(key[2]^219, 3)) + 14
    tmp = K2 - 14
    rol_val = 115 ^ tmp
    key2_xor = ror(rol_val, 3)
    key[2] = key2_xor ^ 219
    

    i = 3
    expected = prefix[3]
    K3 = cipher[3] ^ expected
    # K3 = 7*(v21+2) + ((17-98*(v21-1)) ^ rol(key[3]^(v7-10), ((v21-2)&3)+1)) = 21 + (17 ^ rol(key[3]^246, 4))
    tmp = K3 - 21
    rol_val = 17 ^ tmp
    key3_xor = ror(rol_val, 4)
    key[3] = key3_xor ^ 246
    

    i = 4
    expected = prefix[4]
    K4 = cipher[4] ^ expected
    # K4 = 7*(v21+3) + ((-81-98*(v21-1)) ^ rol(key[4]^(v7+17), v8)) = 28 + (175 ^ rol(key[4]^17, 1))
    tmp = K4 - 28
    rol_val = 175 ^ tmp
    key4_xor = ror(rol_val, 1)
    key[4] = key4_xor ^ 17
    
    return bytes(key)

def main():

    prefix = b'FLAG{'
    key = recover_key_from_prefix(prefix)
    print(f"Recovered key: {key.decode()}")
    flag = decrypt(key)

    flag_str = flag.decode('ascii', errors='ignore').rstrip('\x00')
    print(f"FLAG: {flag_str}")

if __name__ == '__main__':
    main()