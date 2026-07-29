# all addreses valid for base of image(unpacked image)	00007FF72A850000

import sys
import numpy
import fnv_hash_fast
from blobs import numpy_matrix_from_buf100000, numpy_vec_0x800_7FF72A8B4CA0, buf_addr_7FF72A8B6CE0, Unk_7FF72A8B54B0__HARDCODED_ORIG
from DRBG_Sub_7FF72A872170__HASH_rcx_KEY import DRBG_Sub_7FF72A872170
from emulator import emulate_Sub_7FF72A870890


def emulate(buf_x200):
	#loc_7FF72A8B0120
	target_r10_RISC_code = bytearray(buf_addr_7FF72A8B6CE0)  # 
	rsi = bytes.fromhex("9fea235a7c6a4fb4")[::-1]
	r14 = bytes.fromhex("b3e192f8a4d5c6b7")[::-1]
	
	for iii in range(len(target_r10_RISC_code)):

		k1 = rsi[iii % 8];
		k2 = r14[iii % 8];
	
		target_r10_RISC_code[iii] ^= (k1 ^ k2 ^ buf_x200[iii % len(buf_x200)]);  #.smc:00007FF72A8B0172  mov     [r10+r9], cl    
	
	return emulate_Sub_7FF72A870890(target_r10_RISC_code, 0xD2)  ## .text:00007FF72A87C6D7 C28 mov     eax, dword ptr [rbp+0BE0h+var_B98] ; == 8e4545[d2]


def get_Buf0x200_from_key_Sub_7FF72A872480(key_attempt):
	#Computing matrix
	#.text:00007FF72A872540
	buf_0x200 = (numpy_vec_0x800_7FF72A8B4CA0 - numpy.dot(numpy_matrix_from_buf100000, DRBG_Sub_7FF72A872170(key_attempt))).tobytes()  #.text:00007FF72A8725BB 868 sub     cl, al
	
	return buf_0x200


def get_checksum_and_MessageBuf0x40_from_key_sub_7FF72A8B000_smc_deXORed(key, hardcoded_mask = Unk_7FF72A8B54B0__HARDCODED_ORIG):
	final_buf_0x40 = bytearray(0x40)

	buf0x200 = get_Buf0x200_from_key_Sub_7FF72A872480(key)

	emulated = emulate(buf0x200)
	
	#loc_7FF72A8B0354
	v39 = (((((fnv_hash_fast.fnv1a_32(buf0x200) ^ emulated)* 0x9E3779B9)%(2**32))^ 0x31415926)+ 0x27182818)% (2**32) 

	#loc_7FF72A8B03A0:
	v39 = v39.to_bytes(4, byteorder='little')
	
	for i in range(0x40):
		final_buf_0x40[i] = v39[i%4] ^ buf0x200[i] ^ hardcoded_mask[i]  #.smc:00007FF72A8B03DF 398 mov     byte ptr [rbp+r10+290h+var_2D0__BUF_40h__REZULT+1], al ..............  
	
	#00007FF72A8B0528
	rezult_checksum = fnv_hash_fast.fnv1a_32(bytes(final_buf_0x40))
	return (rezult_checksum, final_buf_0x40)
		

############### TEST
def test():
	attempts = [
	(b'a1a2a3a4a5a6a7a8b1b2b3b4b5b6b7b8c1c2c3c4c5c6c7c8d1d2d3d4d5d6d7d8', 0xb9b1ee24),
	(b'11223344556677881122334455667788aabbccddeeffAAFFaabbccddeeff0102', 0xc941ca8a),
	(b'abcdefabcdef1234567890-=).,#@+*LIGDHCIUHWColijqwdacijqwc[jqapdc]', 0x1d1c6804),
	(b'bbcdefabcdef1234567890-=).,#@+*LIGDHCIUHWColijqwdacijqwc[jqapdc]', 0xc2279fde),
	(b'MCM6{000015AE}', 0x913f4e2e),
	(b'MCM6{E503DAF9}', 0xb036d4fb),
    (b'MCM6{0F044BCC}', 0x9f677f11),    ### With emulator (emulator rezult is 0x43d)
	(b'MCM6{031B46C3}', 0xDCE5AB88)     ### With emulator (emulator rezult is 0x3AC)
	]	

	for iii, (key, test_checksum) in enumerate(attempts):
		checksum_rezult, buf_0x40 = get_checksum_and_MessageBuf0x40_from_key_sub_7FF72A8B000_smc_deXORed(key)
		if checksum_rezult != test_checksum:
			print(f"Test {iii} for key {key} failed.")
			sys.exit()
		
	print("Checksums test success!")
	compute_checksum_and_new_Unk_7FF72A8B54B0__HARDCODED(b"SuperSecretPassword", b'Success!\x00')

if __name__ == "__main__":
	test()








 