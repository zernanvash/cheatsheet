# Final logic
import argparse

import settings
import sys
import string
import secrets
import numpy
import cupy
from datetime import datetime
#import fnvhash
#import fnv_c
import fnv_hash_fast
#import fnvhash_c
from blobs import cupy_vec_from_buf100000, cupy_vec_0x800_7FF72A8B4CA0, HARDCODED
from DRBG_Sub_7FF72A872170__HASH_rcx_KEY import DRBG_Sub_7FF72A872170
from emulator import emulate_Sub_7FF72A870890

cupy_vec_0x800_7FF72A8B4CA0 = cupy_vec_0x800_7FF72A8B4CA0.reshape((-1,1))

######################
CHECKSUM_LOOKING_FOR = 0x8EDA89A9
#CHECKSUM_LOOKING_FOR = 0xb036d4fb     # for test ))))
######################

alphabet = string.ascii_letters + string.digits + string.punctuation + ' '
final_buf_0x40 = bytearray(0x40)

def hex_dump(data, size=16):
    for i in range(0, len(data), size):
        chunk = data[i:i + size]
        
        # 1. offset
        address = f"{i:08x}: "
        
        # 2. HEX
        hex_view = chunk.hex(' ').ljust(size * 3 - 1)
        
        # 3. ASCII 
        ascii_view = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        
        print(f"{address} {hex_view}  |{ascii_view}|")


def emulate(buf_x200):

	target_r10_xor_rsi_xor_r14 = bytearray.fromhex('BE 0D B9 34 81 3C 82 21 93 69 45 4F 95 16 9D 3B A9 46 F6 7F E5 27 13 10 07 14 14 1A 3E 1D 16 15')
	for iii in range(len(target_r10_xor_rsi_xor_r14)):
		# final byte compute in memory
		target_r10_xor_rsi_xor_r14[iii] ^= buf_x200[iii % len(buf_x200)];
	
	#hex_dump(target_r10_xor_rsi_xor_r14)
	return emulate_Sub_7FF72A870890(target_r10_xor_rsi_xor_r14, 0xD2)  ## .text:00007FF72A87C6D7 C28 mov     eax, dword ptr [rbp+0BE0h+var_B98] ; == 8e4545d2


def checksum_fr_buf_0x200(buf):
	#print("Start emulate")
	#input()
	emulated = emulate(buf.tobytes())
	"""
	if (emulated != 0):
		print('AAAAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!!!')
		input()	
	"""

	#print("End emulate")
	v39 = (((((fnv_hash_fast.fnv1a_32(buf.tobytes()) ^ emulated)* 0x9E3779B9)%(2**32))^ 0x31415926)+ 0x27182818)% (2**32) 

	#loc_7FF72A8B03A0:
	v39 = v39.to_bytes(4, byteorder='little')
	
	for i in range(0x40):
		final_buf_0x40[i] = v39[i%4] ^ buf[i] ^ HARDCODED[i]
	
	#00007FF72A8B0528
	rezult = fnv_hash_fast.fnv1a_32(bytes(final_buf_0x40))#.to_bytes(4, byteorder='little').hex(' ')
	return rezult

def get_checksums(key_attempts):
	print("Compute matrix")
	buf_0x200_x_attempts = (cupy_vec_0x800_7FF72A8B4CA0 - cupy.dot(cupy_vec_from_buf100000, DRBG_Sub_7FF72A872170(key_attempts))).get()  #.tobytes()  # maybe cupy.asnumpy
	print("Matrix computed")
	
	return map(checksum_fr_buf_0x200, numpy.nditer(buf_0x200_x_attempts, flags=['external_loop'], order='F'))		


def generate_attempts(pref =''):
	pref_MCM = "MCM6{"
	post = "}"
	pref = pref.upper()
	
	attempts = []
	for iii in range(0xFFFFFFFF+1 >> 4*len(pref)):
		attempts.append((pref_MCM + pref+ f"{iii:08X}"[len(pref):] + post).encode())
		if (len(attempts) == settings.attempts_in_GPU):
			yield attempts
			attempts = []

	if len(attempts) == 0:
		return	

	while len(attempts) < settings.attempts_in_GPU:
		attempts.append(b'MCM6{--__--__}')	

	yield attempts


#######################################################
def test():
	attempts = [
	(b'a1a2a3a4a5a6a7a8b1b2b3b4b5b6b7b8c1c2c3c4c5c6c7c8d1d2d3d4d5d6d7d8', 0xb9b1ee24),
	(b'11223344556677881122334455667788aabbccddeeffAAFFaabbccddeeff0102', 0xc941ca8a),
	(b'abcdefabcdef1234567890-=).,#@+*LIGDHCIUHWColijqwdacijqwc[jqapdc]', 0x1d1c6804),
	(b'bbcdefabcdef1234567890-=).,#@+*LIGDHCIUHWColijqwdacijqwc[jqapdc]', 0xc2279fde),
	(b'MCM6{000015AE}', 0x913f4e2e),
	(b'MCM6{E503DAF9}', 0xb036d4fb),
    (b'MCM6{0F044BCC}', 0x9f677f11),    ### With emulator (emulator rezult is 0x43d)
	(b'MCM6{031B46C3}', 0xDCE5AB88)      ### With emulator (emulator rezult is 0x3AC)
	]	

	#add checksums from file
	for line in open('test.txt'):
		attempts.append((line[:0x40].encode(), int(line[0x41:], 16)))

		if len(attempts) >= settings.attempts_in_GPU:
			break

	# if not enopugh for 1 cycle
	while len(attempts) < settings.attempts_in_GPU:
		attempts.append(attempts[0])

	
	# compute and check
	assert(len(attempts) == settings.attempts_in_GPU)  # key attempts for test should be equal to size of matrix in GPU 
	keys = [key for (key, _) in attempts]

	alll_checksums = get_checksums(keys)
	for iii, checksum_new_algo in enumerate(alll_checksums):
		if attempts[iii][1] != checksum_new_algo:
			print("New algo for key", attempts[iii][0], "DOES NOT MATCH OLD ALGO!!!!")
			print("Rezults", hex(checksum_new_algo), hex(attempts[iii][1]))
			return False
		print(attempts[iii][0].decode(), hex(checksum_new_algo), " PASSED !")

	return True

def writerezult(key, summ, prefix):
	with open(prefix+"  !!!BINGO!!.txt", "a") as bingo_f:
		bingo_f.write(key.decode() + " " + hex(summ) +"\r")
	

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Find key")
	parser.add_argument('-p', '--prefix', type=str, default='', help='prefix')
	args = parser.parse_args()

	print("START TEST.")
	if not test():
		print("TEST NOT PASSED. EXIT.........")
		sys.exit(0) 

	print("TEST PASSED. TRY TO BRUTE KEY")
	print("================================")
	#input()

	###############################################
	# BRUTE
	
	tries = 0
	start = datetime.now()
	for key_attempts in generate_attempts(args.prefix):
		tries +=  settings.attempts_in_GPU
		
		checksums = get_checksums(key_attempts)
		for iii, ch in enumerate(checksums):
			if  ch == CHECKSUM_LOOKING_FOR:
				print("BINGO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				print("Key is: ", key_attempts[iii])
				print("Key is: ", key_attempts[iii].decode("utf-8"))
				writerezult(key_attempts[iii], ch, args.prefix)
				input()
		
		passed = datetime.now() - start
		print(f"Attempt: {tries}. Time passed: {passed}. Check is {key_attempts[iii].decode("utf-8")} checksum is {hex(ch)}")








 