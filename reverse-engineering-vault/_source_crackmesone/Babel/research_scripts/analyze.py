#!/usr/bin/env python3
"""Scratch analysis of babel_vm.exe data sections."""

# FUN_1400016d0 XORs each byte with 0x55 and prints it
# Let's decode the two result strings

# DAT_140007340 (failure, length 0xf = 15)
fail_hex = "1C3B2334393C3175193C36303B263000"
fail_bytes = bytes.fromhex(fail_hex)
fail_decoded = ''.join(chr(b ^ 0x55) for b in fail_bytes[:15])
print(f"Failure string: '{fail_decoded}'")

# DAT_140007350 (success, length 0xe = 14) 
success_hex = "143636302626751227343B2130310000"
success_bytes = bytes.fromhex(success_hex)
success_decoded = ''.join(chr(b ^ 0x55) for b in success_bytes[:14])
print(f"Success string: '{success_decoded}'")

# Opcode dispatch table at 1400076a0
# This maps raw bytecode bytes to switch case numbers
opcode_table_hex = "071826171C2003220527211411040B022423191B090A1D001F16120E10061A1E1513250F080D0C01"
opcode_table = bytes.fromhex(opcode_table_hex)
print(f"\nOpcode dispatch table ({len(opcode_table)} entries):")
for i, v in enumerate(opcode_table):
    print(f"  raw_byte 0x{i:02x} -> switch case {v}")

# Global data at 140006010 (XOR keys for bytecode decryption)
global_hex = "DEC03700CEFAEDFE13BEBAFE37133713CAEFBEADBEBAFECADE00000001000100B40000008EB10000BE00000013E067D21C000000EFBEADDE5A0000000000000070510040010000000000000000000000"
global_bytes = bytes.fromhex(global_hex)
print(f"\nGlobal data at 0x140006010:")
for i in range(0, len(global_bytes), 4):
    chunk = global_bytes[i:i+4]
    if len(chunk) == 4:
        val = int.from_bytes(chunk, 'little')
        print(f"  +0x{i:02x}: 0x{val:08x}")

# The XOR keys used for bytecode decryption
# In the code, the key is built from bytes at specific offsets:
# For bytecode at DAT_140007420 (main VM bytecode, 0x263 bytes):
#   key comes from uStack_b1c._4_4_ = CONCAT13(DAT_140006030, CONCAT12(DAT_140006038, CONCAT11(DAT_140006040, DAT_140006048)))
#   That's bytes: DAT_140006048, DAT_140006040, DAT_140006038, DAT_140006030

# Let me extract those individual byte offsets from global data
# 0x140006010 base
# DAT_140006048 = offset 0x38 from 0x140006010 = byte at 0x140006048
# DAT_140006040 = offset 0x30
# DAT_140006038 = offset 0x28
# DAT_140006030 = offset 0x20

print(f"\n--- XOR Key extraction ---")
print(f"DAT_140006010 byte: 0x{global_bytes[0x00]:02x}")
print(f"DAT_140006011 byte: 0x{global_bytes[0x01]:02x}")
print(f"DAT_140006012 byte: 0x{global_bytes[0x02]:02x}")
print(f"DAT_140006018 byte: 0x{global_bytes[0x08]:02x}")
print(f"DAT_140006019 byte: 0x{global_bytes[0x09]:02x}")
print(f"DAT_14000601a byte: 0x{global_bytes[0x0a]:02x}")
print(f"DAT_14000601b byte: 0x{global_bytes[0x0b]:02x}")
print(f"DAT_140006020 byte: 0x{global_bytes[0x10]:02x}")
print(f"DAT_140006021 byte: 0x{global_bytes[0x11]:02x}")
print(f"DAT_140006022 byte: 0x{global_bytes[0x12]:02x}")
print(f"DAT_140006023 byte: 0x{global_bytes[0x13]:02x}")
print(f"DAT_140006028 byte: 0x{global_bytes[0x18]:02x}")
print(f"DAT_140006030 byte: 0x{global_bytes[0x20]:02x}")
print(f"DAT_140006038 byte: 0x{global_bytes[0x28]:02x}")
print(f"DAT_140006040 byte: 0x{global_bytes[0x30]:02x}")
print(f"DAT_140006048 byte: 0x{global_bytes[0x38]:02x}")

# XOR key for main bytecode (DAT_140007420, 0x263 bytes):
# CONCAT13(DAT_140006030, CONCAT12(DAT_140006038, CONCAT11(DAT_140006040, DAT_140006048)))
# This is [DAT_140006048, DAT_140006040, DAT_140006038, DAT_140006030] as a 4-byte key
key_main = bytes([global_bytes[0x38], global_bytes[0x30], global_bytes[0x28], global_bytes[0x20]])
print(f"\nKey for main bytecode (0x140007420): {key_main.hex()}")

# XOR key for bytecode 2 (DAT_1400073e0, 0x21 bytes):
# CONCAT31(CONCAT21(CONCAT11(DAT_140006021, DAT_140006022), DAT_140006023), DAT_140006028)
# = [DAT_140006028, DAT_140006021, DAT_140006022, DAT_140006023]
key_bc2 = bytes([global_bytes[0x18], global_bytes[0x11], global_bytes[0x12], global_bytes[0x13]])
print(f"Key for bytecode 2 (0x1400073e0): {key_bc2.hex()}")

# XOR key for bytecode 3 (DAT_1400073a0, 0x27 bytes):
# CONCAT31(CONCAT21(CONCAT11(DAT_140006019, DAT_14000601a), DAT_14000601b), DAT_140006020)
# = [DAT_140006020, DAT_140006019, DAT_14000601a, DAT_14000601b]
key_bc3 = bytes([global_bytes[0x10], global_bytes[0x09], global_bytes[0x0a], global_bytes[0x0b]])
print(f"Key for bytecode 3 (0x1400073a0): {key_bc3.hex()}")

# XOR key for bytecode 4 (DAT_140007360, 0x29 bytes):
# CONCAT31(CONCAT21(CONCAT11(DAT_140006010, DAT_140006011), DAT_140006012), DAT_140006018)
# = [DAT_140006018, DAT_140006010, DAT_140006011, DAT_140006012]
key_bc4 = bytes([global_bytes[0x08], global_bytes[0x00], global_bytes[0x01], global_bytes[0x02]])
print(f"Key for bytecode 4 (0x140007360): {key_bc4.hex()}")

# Now decrypt the bytecodes
main_bc_hex = "7D1B136A581B99B16E0E99B2224ABEB15C10BBA55F1DBEB75F1DBEA25F1DBEA80E1EA4B1551CBEB85A18BE892513BFB5561DBAB5CB36B3B45B13BCB4541EBDBB591DABB75F1FBD4BA51CBCB75E1E59A8571CBCB75AE341BB5B1E9BB45B00EAB65A1BBF965E1CBAB55B18BDB65E06BFAE5A0735B47D1F510A5A1FBEA259E274A80E1E99B794E6BAB75117A9BB5A1DBAB43152B1B55A18BF834911BEB5551EBEBB591DBEB6591FBC4BA51DBCB3591E414B5E1E812E571CBCB75AE341BB5B1F9BB45B00EAB65A1BBF965E1CBAB54818BBB65E13BEB4551DBFB45A1DBAB41B2D9EB47C45B1B55818BF11FF11BEB5591C414B551DBA915A1DA2E0581CB9B57818B3B05B15BAB65E3BBBB45A3ABBB75FE341945F1DBEB75FE341A25F1CBEA80E1EB1B45813BFB7571CBFBB5B18B3B45B1FBE4BA513BFB45E1DB1BB591D414B5A1CBFBB5B1DBAB5AAECBDB5A5E3BEB45B13BCB6551FBDB4581FBDB6A5E3ACB6591FBC4BA511BEB6591C414B551DBB915A1DA2E0581CB9B57818BEB05B1EBABB5A1EB1B5591CBEB5551DBAB45A1DB1B55F1CBEB5551DBEBB581DB3B55818BF198411BEB5551DBAB05B0DAFB95A1DBDB4A5E3B1B55C39BEB54648BCB45D1D9CB05718BFBD5E1EBAB15A0ABEB55A00EAB6551DB9B45D1D9CB05A18BFA65E1BBCB041EEBF9359116EB0592BADAD59F300A2595EBEA80E1EBBB54C1CBFB44648BCBB5B14BEB35B3EBAB95E1DBCB05F1EA8B45B1CA2E05813BFBD5A1BBF965E1CBAB55318BCB05D1999B25A1C9BB15C14BBB25419B1B75F1DBEA25F1CBEA80E1EBFB35F13BEB45A1BBEBB5A1DB3B35A3BBEB55A3DBEB47B1DB9BF7D1CBEB47B1CBE935D1CBE955B1BB5000000000000000000"
main_bc = bytes.fromhex(main_bc_hex)

# Decrypt: XOR each byte with key[i & 3]
def decrypt_bc(data, key, length):
    result = bytearray()
    for i in range(length):
        result.append(data[i] ^ key[i & 3])
    return bytes(result)

decrypted_main = decrypt_bc(main_bc, key_main, 0x263)
print(f"\nDecrypted main bytecode ({len(decrypted_main)} bytes):")
print(' '.join(f'{b:02x}' for b in decrypted_main))

# Decrypt bytecode 2 (DAT_1400073e0, 0x21 bytes)
bc2_hex = "DFAFBFECDBA2BCE4DEA7BFEFDFACBDEEDAAEBCDEABA8B1E9D1ACBBE4CC8DBEFFCF"
bc2 = bytes.fromhex(bc2_hex)
decrypted_bc2 = decrypt_bc(bc2, key_bc2, 0x21)
print(f"\nDecrypted bytecode 2 ({len(decrypted_bc2)} bytes):")
print(' '.join(f'{b:02x}' for b in decrypted_bc2))

# Decrypt bytecode 3 (DAT_1400073a0, 0x27 bytes)
bc3_hex = "CBFCBBBDC9FFBEBDCBFBB9BFCCFDBBB9C9F1B85BE6FBB5BFCAFFBBBBC5F8B5BFC2F5A898CAEEAB"
bc3 = bytes.fromhex(bc3_hex)
decrypted_bc3 = decrypt_bc(bc3, key_bc3, 0x27)
print(f"\nDecrypted bytecode 3 ({len(decrypted_bc3)} bytes):")
print(' '.join(f'{b:02x}' for b in decrypted_bc3))

# Decrypt bytecode 4 (DAT_140007360, 0x29 bytes)
bc4_hex = "1235C1DD1536C4D81232C6DF1531C1D91536C8D81237D5DF1222C1DE1236C3D81C36C9D5011FC0CE02"
bc4 = bytes.fromhex(bc4_hex)
decrypted_bc4 = decrypt_bc(bc4, key_bc4, 0x29)
print(f"\nDecrypted bytecode 4 ({len(decrypted_bc4)} bytes):")
print(' '.join(f'{b:02x}' for b in decrypted_bc4))

# Now analyze the modexp constants
# DAT_14000602c (4 bytes LE) = exponent
# DAT_140006034 = ?
# DAT_14000603c = modulus?
print(f"\n--- Modular exponentiation constants ---")
# From the hex at 14000602c: 01000100 B4000000 8EB10000 BE000000 13E067D2 1C000000 EFBEADDE 5A000000
# DAT_14000602c = 0x00010001 (little endian) -- That's 65537! RSA public exponent
exp_val = int.from_bytes(bytes.fromhex("01000100"), 'little')
print(f"DAT_14000602c (exponent): {exp_val} (0x{exp_val:x})")

# DAT_140006034 
val_6034 = int.from_bytes(bytes.fromhex("B4000000"), 'little')
print(f"DAT_140006030+4 (DAT_140006034): {val_6034} (0x{val_6034:x})")

# DAT_14000603c
val_603c = int.from_bytes(bytes.fromhex("8EB10000"), 'little')
print(f"DAT_140006038+4 (DAT_14000603c): {val_603c} (0x{val_603c:x})")

# Actually let me re-read the structure more carefully
# 14000602c: 01 00 01 00  => uint32 LE = 0x00010001 = 65537 (this is DAT_14000602c)
# 140006030: B4 00 00 00  => uint32 LE = 0xB4 = 180
# 140006034: 8E B1 00 00  => uint32 LE = 0xB18E = 45454
# 140006038: BE 00 00 00  => uint32 LE = 0xBE = 190
# 14000603c: 13 E0 67 D2  => uint32 LE = 0xD267E013
# 140006040: 1C 00 00 00  => uint32 LE = 0x1C = 28

print(f"\n--- Re-reading modexp carefully ---")
modexp_hex = "01000100B40000008EB10000BE00000013E067D21C000000EFBEADDE5A000000"
modexp_bytes = bytes.fromhex(modexp_hex)
for i in range(0, len(modexp_bytes), 4):
    val = int.from_bytes(modexp_bytes[i:i+4], 'little')
    addr = 0x14000602c + i
    print(f"  0x{addr:09x}: 0x{val:08x} ({val})")

# In the code:
# pFVar11 = DAT_14000602c (exponent)
# param_4 = CONCAT44(DAT_140006034, DAT_14000603c) -- this creates a 64-bit modulus
# But the code says: param_4 = (FILE *)CONCAT44(DAT_140006034, DAT_14000603c)
# CONCAT44 puts first arg in high 32 bits: (DAT_140006034 << 32) | DAT_14000603c
# Wait, in Ghidra CONCAT44(a,b) = (a << 32) | b, so:
# modulus = (DAT_140006034 << 32) | DAT_14000603c

# But looking at the data layout at 0x14000602c:
# +0: 0x00010001 = DAT_14000602c (exponent)  
# +4: 0x000000B4 = ? 
# +8: 0x0000B18E = ?
# +12: 0x000000BE = ?
# +16: 0xD267E013 = ?
# +20: 0x0000001C = ?
# +24: 0xDEADBEEF = ?
# +28: 0x0000005A = ?

# Wait, the addresses are specific globals, not necessarily contiguous in reading order.
# Let me look at the decompiled code again:
# pFVar11 = (FILE *)(ulonglong)DAT_14000602c;   -- exponent
# param_4 = (FILE *)CONCAT44(DAT_140006034, DAT_14000603c);  -- modulus (64-bit)
# if (param_4 == 0) param_4 = 1;

# So exponent = DAT_14000602c = value at address 0x14000602c
# modulus = (DAT_140006034 << 32) | DAT_14000603c

# From the hex dump starting at 0x14000602c:
# 01 00 01 00  -> at 0x14000602c -> 0x00010001 = 65537
# The next 4 bytes at 0x140006030: B4 00 00 00 -> NOT DAT_140006034
# DAT_140006034 is at address 0x140006034: 8E B1 00 00 -> 0x0000B18E = 45454
# DAT_14000603c is at address 0x14000603c: 13 E0 67 D2 -> 0xD267E013

# So modulus = (45454 << 32) | 0xD267E013 = 0x0000B18ED267E013

modulus = (0x0000B18E << 32) | 0xD267E013
exponent = 0x00010001
print(f"\nRSA-like modexp:")
print(f"  exponent e = {exponent} (0x{exponent:x})")
print(f"  modulus  n = {modulus} (0x{modulus:x})")
