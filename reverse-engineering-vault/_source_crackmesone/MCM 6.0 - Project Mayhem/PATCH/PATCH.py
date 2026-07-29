import sys
import argparse
from Ssub_7FF72A8B0000_smc_deXORed import get_checksum_and_MessageBuf0x40_from_key_sub_7FF72A8B000_smc_deXORed
from blobs import Unk_7FF72A8B54B0__HARDCODED_ORIG

new_VALID_MESSAGE = b"Success!\x00"   # should be 9 bytes long. To modify it patch code should be modified
assert(len(new_VALID_MESSAGE) == 9)   # should be 9 bytes long. To modify it make_shell should be modified


def hex_dump(data, size=16):
    for i in range(0, len(data), size):
        chunk = data[i:i + size]
        
        # 1. offset
        address = f"{i:08x}: "
        
        # 2.HEX
        hex_view = chunk.hex(' ').ljust(size * 3 - 1)
        
        # 3. ASCII
        ascii_view = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        
        print(f"{address} {hex_view}  |{ascii_view}|")


def compute_checksum_and_new_Unk_7FF72A8B54B0__HARDCODED(key, VALID_MESSAGE):
	# compute Unk_7FF72A8B54B0__HARDCODED for VALID_MESSAGE and the corresponding checksum (.smc:00007FF72A8B0828 398 xor     eax, 8EDA89A9h ) 

	_, buf0x40_for_zeroes = get_checksum_and_MessageBuf0x40_from_key_sub_7FF72A8B000_smc_deXORed(key, b'\x00'*0x40)  # compute mask for key
	
	# compute HARDCODED to get buf0x40 as VALID_MESSAGE
	new_Unk_7FF72A8B54B0__HARDCODED = bytearray(Unk_7FF72A8B54B0__HARDCODED_ORIG)
	for iii in range(len(VALID_MESSAGE)):
		new_Unk_7FF72A8B54B0__HARDCODED[iii] = buf0x40_for_zeroes[iii] ^ VALID_MESSAGE[iii]
	
	# compute new checksum for new new_Unk_7FF72A8B54B0__HARDCODED
	new_checksum, message = get_checksum_and_MessageBuf0x40_from_key_sub_7FF72A8B000_smc_deXORed(key, new_Unk_7FF72A8B54B0__HARDCODED)
	
	return new_checksum, new_Unk_7FF72A8B54B0__HARDCODED, message


def make_shell(new_checksum, new_Unk_7FF72A8B54B0__HARDCODED):
	
	_SUB_7FF72A8B0000_deXORed_START_ADDR = 0x7FF72A8B0000
	_OFF_FROM_RIP = 0x1724F1  #offset to .smc section
	_OFF_to_Unk_7FF72A8B54B0__HARDCODED = 0x4C87 - 0x4000 +0x3E00  # offset from checksum to Unk_7FF72A8B54B0__HARDCODED in image

	# generate shell for checksum modification
	_MASK = [0x4F, 0xAC, 0x08, 0x44]
	addr_checksum = 0x7FF72A8B0829
	checksum = bytearray(new_checksum.to_bytes(4, byteorder='little'))

	for iii in range(len(checksum)):
		checksum[iii] ^= _MASK[(addr_checksum + iii) % 4]  #.smc section is under XOR mask [0x4F, 0xAC, 0x08, 0x44]

	
	offset = _OFF_FROM_RIP + addr_checksum - _SUB_7FF72A8B0000_deXORed_START_ADDR

	shell =  b'\x48\x8D\x0D' +  offset.to_bytes(4, byteorder='little')                                # mov rcx, [rip+offset]
	shell += b'\xC7\x01' + checksum                                                                   # mov dword[rcx], checksum

	#  generate shell for checksum modification
	shell += b'\x48\x81\xC1' + _OFF_to_Unk_7FF72A8B54B0__HARDCODED.to_bytes(4, byteorder='little')    # add rcx, _OFF_to_Unk_7FF72A8B54B0__HARDCODED
	shell += b'\xC7\x01'     + new_Unk_7FF72A8B54B0__HARDCODED[:4]                                    # mov dword[rcx], new_Unk_7FF72A8B54B0__HARDCODED[:4]
	shell += b'\xC7\x41\x04' + new_Unk_7FF72A8B54B0__HARDCODED[4:8]                                   # mov dword[rcx+4], new_Unk_7FF72A8B54B0__HARDCODED[4:8]
	shell += b'\xC6\x41\x08' + new_Unk_7FF72A8B54B0__HARDCODED[8:9]                                     # mov byte[rcx+8], new_Unk_7FF72A8B54B0__HARDCODED[8]

	return shell


def patch(data, new_key):
	_START_SHELL_IN_MAIN_IMAGE = 0x1B2F08
	_END___SHELL_IN_MAIN_IMAGE = 0x1B2F3A
	assert(len(new_key) <=0x40)  # in crackme it could be longer but not implemented in my scripts
	assert(len(data) == 3392000)
	need_shell_len = _END___SHELL_IN_MAIN_IMAGE - _START_SHELL_IN_MAIN_IMAGE

	#compute new data to use it in patch
	new_checksum, new_Unk_7FF72A8B54B0__HARDCODED, message = compute_checksum_and_new_Unk_7FF72A8B54B0__HARDCODED(new_key, new_VALID_MESSAGE)
	
	new_Unk_7FF72A8B54B0__HARDCODED = new_Unk_7FF72A8B54B0__HARDCODED[:len(new_VALID_MESSAGE)]
	
	# make shell
	shell = make_shell(new_checksum, new_Unk_7FF72A8B54B0__HARDCODED)
	shell = shell + b'\x90'*(need_shell_len - len(shell))
	assert(len(shell) == need_shell_len)

	print("New checksum at .smc:00007FF72A8B0828 is", hex(new_checksum))
	print("New Unk_7FF72A8B54B0__HARDCODED is")
	hex_dump(new_Unk_7FF72A8B54B0__HARDCODED)
	print("\nNew message is")
	hex_dump(message)
	print(f"\nPatch shell to {hex(_START_SHELL_IN_MAIN_IMAGE)}:")
	hex_dump(shell)	

	#patch shell to image data
	rezult = data[:_START_SHELL_IN_MAIN_IMAGE] + shell + data[_END___SHELL_IN_MAIN_IMAGE:]  # Patch buffer
	assert(len(data) == len(rezult))

	return rezult

def main(filename, key):
	with open(filename, 'rb') as inf:
		data = inf.read()
		with open(f"{filename}_patch_for_key_{key.decode()}.exe", "wb") as outf:
			outf.write(patch(data, key))
			print("\nPATCHED!!")
			print(f"New file is {filename}_patch_for_key_{key.decode()}.exe")


def test(key):
	new_checksum, new_Unk_7FF72A8B54B0__HARDCODED, message = compute_checksum_and_new_Unk_7FF72A8B54B0__HARDCODED(key, new_VALID_MESSAGE)

	print("New checksum in at .smc:00007FF72A8B0828 is", hex(new_checksum))
	print("New Unk_7FF72A8B54B0__HARDCODED is", new_Unk_7FF72A8B54B0__HARDCODED)
	print("New message is", message)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Patch CrackMe.exe to make your key valid")

	parser.add_argument("new_key", type=lambda x: x.encode(), help="new valid key")
	parser.add_argument("-t", "--test", action="store_true", help="Test script for key")
	args = parser.parse_args()
	assert(len(args.new_key) <=0x40)  # in crackme it could be longer but not implemented in my scripts
	
	if args.test:
		test(args.new_key)
		sys.exit()
    
	main('CrackMe.exe', args.new_key)

	