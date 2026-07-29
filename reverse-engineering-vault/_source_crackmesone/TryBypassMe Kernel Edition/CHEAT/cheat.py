import ctypes
from ctypes import wintypes
import psutil
import time


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


# ACCESS consts
PROCESS_ALL_ACCESS = 0x1FFFFF

# types for Windows x64
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

#  ReadProcessMemory
kernel32.ReadProcessMemory.argtypes = [
    wintypes.HANDLE,  # hProcess
    ctypes.c_void_p,  # lpBaseAddress
    ctypes.c_void_p,  # lpBuffer
    ctypes.c_size_t,  # nSize
    ctypes.POINTER(ctypes.c_size_t)  # lpNumberOfBytesRead
]
kernel32.ReadProcessMemory.restype = wintypes.BOOL

#  WriteProcessMemory
kernel32.WriteProcessMemory.argtypes = [
    wintypes.HANDLE,  # hProcess
    ctypes.c_void_p,  # lpBaseAddress
    ctypes.c_void_p,  # lpBuffer
    ctypes.c_size_t,  # nSize
    ctypes.POINTER(ctypes.c_size_t)  # lpNumberOfBytesWritten
]
kernel32.WriteProcessMemory.restype = wintypes.BOOL


def get_pid_and_image_base_by_name(process_name):
	for proc in psutil.process_iter(['pid', 'name']):
		try:
            # compare name
			if proc.info['name'].lower() == process_name.lower():
				#modules
				for m in proc.memory_maps(grouped=False):
					print()
					print()
					print(m)
        		# first region with exe — ImageBase
					if m.path == proc.exe():
						start_addr_str = m.addr.split('-')[0]
						return proc.info['pid'], int(start_addr_str, 16)

                
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return None, None




def read_process_memory(pid, address, length):
    
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())

    buffer = ctypes.create_string_buffer(length)
    bytes_read = ctypes.c_size_t(0)
    
    success = kernel32.ReadProcessMemory(
        process_handle, address, buffer, length, ctypes.byref(bytes_read)
    )
    
    kernel32.CloseHandle(process_handle)
    
    if not success:
        raise ctypes.WinError(ctypes.get_last_error())
        
    return buffer.raw  

def read_DWORD_fr_pointer(pid, pointer, image_base):
	addr = int.from_bytes(read_process_memory(pid, compute_addr(pointer, image_base), 8), byteorder='little')
	value = int.from_bytes(read_process_memory(pid, addr, 4), byteorder='little')
	return value, addr

def write_process_memory(pid, address, data):
    
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())

    # if str
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    length = len(data)
    # make buf
    c_data = ctypes.c_char_p(data)
    bytes_written = ctypes.c_size_t(0)
    
    success = kernel32.WriteProcessMemory(
        process_handle, address, data, length, ctypes.byref(bytes_written)
    )
    
    kernel32.CloseHandle(process_handle)
    
    if not success:
        raise ctypes.WinError(ctypes.get_last_error())
    
    return bytes_written.value


def compute_addr(addr_from_ida, image_base):
	IMAGE_BASE_IN_IDA = 0x7FF669B80000

	RVA = addr_from_ida - IMAGE_BASE_IN_IDA
	return image_base + RVA


def make_protected_value_buff(value, Qword_1_7FF669BF0888 = 0x00, Qword_2_7FF669BF07C0 = 0X00):
	assert(value < 2**32 +1)
	assert(Qword_1_7FF669BF0888 < 2**32 +1)
	assert(Qword_2_7FF669BF07C0 < 2**32 +1)
	assert(value >= 0)
	assert(Qword_1_7FF669BF0888 >= 0)
	assert(Qword_2_7FF669BF07C0 >= 0)
	
	protval = [0x00] * 0x78

	protval[0x00] = value ^ Qword_1_7FF669BF0888 
	protval[0x20] = 0xDEADC0DE
	protval[0x38] = 0xB16B00B5
	protval[0x68] = value ^ Qword_2_7FF669BF07C0

	PRMZH = value ^ Qword_1_7FF669BF0888 ^ Qword_2_7FF669BF07C0
	
	for iii in range(0x04, 0x20, 4):
		protval[iii] = ((PRMZH * 0X1000193) & 0XFFFFFFFF) ^ 0x811C9DC5
		PRMZH = protval[iii]

	for iii in range(0x24, 0x38, 4):
		protval[iii] = ((PRMZH * 0X1000193) & 0XFFFFFFFF) ^ 0x811C9DC5
		PRMZH = protval[iii]

	for iii in range(0x3C, 0x68, 4):
		protval[iii] = ((PRMZH * 0X1000193) & 0XFFFFFFFF) ^ 0x811C9DC5
		PRMZH = protval[iii] 

	for iii in range(0x6C, 0x78, 4):
		protval[iii] = ((PRMZH * 0X1000193) & 0XFFFFFFFF) ^ 0x811C9DC5
		PRMZH = protval[iii] 

	############# make bytes
	buf = b""

	for iii in range(0,len(protval),4):
		buf += protval[iii].to_bytes(4, byteorder='little') 

	return buf


def find_target_process():
	
	while True:
		print("Try find TBM.exe process")
		pid, image_base = get_pid_and_image_base_by_name("TBM.exe")

		if pid:
			break
		print("waiting...")
		time.sleep(1)

	print(f'Found process. PID={pid} ImageBase={hex(image_base)}')
	return pid, image_base


def cheat_HP(pid, image_base):
	HP_addr_in_IDA = 0x7FF669BF0990
	HP_NEW_VALUE = 100

	qw1_value, _ = read_DWORD_fr_pointer(pid, 0x7FF669BF0888, image_base)
			
	qw2_value, _ = read_DWORD_fr_pointer(pid, 0x7FF669BF07C0, image_base)
			
	#### cheat HP value buffer
	print("cheat HP", HP_NEW_VALUE)
	HP_value_buffer = make_protected_value_buff(HP_NEW_VALUE, qw1_value, qw2_value)
			
	#print(hex(compute_addr(HP_addr_in_IDA, image_base)))
	#hex_dump(HP_value_buffer)
	
	write_process_memory(pid, compute_addr(HP_addr_in_IDA, image_base), HP_value_buffer)
			
	#### cheat HP diff  >>>>>>>>.text:00007FF669BD1F70<<<<<<<<<<
	print("cheat HP diff")
	Qword_7FF669BF07C8_diff_HP_1_xor_1_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07C8, image_base)
	Qword_7FF669BF07F0_diff_HP_2_value_value, Qword_7FF669BF07F0_diff_HP_2_value_addr = read_DWORD_fr_pointer(pid, 0x7FF669BF07F0, image_base)
	Qword_7FF669BF07D8_diff_HP_3_xor_2_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07D8, image_base)
			
	#print("Qword_7FF669BF07C8_diff_HP_1_xor_1", hex(Qword_7FF669BF07C8_diff_HP_1_xor_1_value))
	#print("Qword_7FF669BF07F0_diff_HP_2_value", hex(Qword_7FF669BF07F0_diff_HP_2_value_value))
	#print("Qword_7FF669BF07D8_diff_HP_3_xor_2", hex(Qword_7FF669BF07D8_diff_HP_3_xor_2_value))

	# write XORED zero diff to two memory locations   
	write_process_memory(pid, Qword_7FF669BF07F0_diff_HP_2_value_addr    , Qword_7FF669BF07C8_diff_HP_1_xor_1_value.to_bytes(4, byteorder='little') )
	write_process_memory(pid, Qword_7FF669BF07F0_diff_HP_2_value_addr + 4, Qword_7FF669BF07D8_diff_HP_3_xor_2_value.to_bytes(4, byteorder='little') )


def cheat_AMMO(pid, image_base):
	AMMO_addr_in_IDA = 0x7FF669BF0910
	AMMO_NEW_VALUE = 30

	qw1_value, _ = read_DWORD_fr_pointer(pid, 0x7FF669BF0888, image_base)
			
	qw2_value, _ = read_DWORD_fr_pointer(pid, 0x7FF669BF07C0, image_base)
			
	#### cheat AMMO value buffer
	print("cheat AMMO", AMMO_NEW_VALUE)
	AMMO_value_buffer = make_protected_value_buff(AMMO_NEW_VALUE, qw1_value, qw2_value)
			
	#print(hex(compute_addr(AMMO_addr_in_IDA, image_base)))
	
	
	write_process_memory(pid, compute_addr(AMMO_addr_in_IDA, image_base), AMMO_value_buffer)
			
	#### cheat AMMO diff   >>>>>>>>.text:00007FF669BD4371<<<<<<<<<<
	print("cheat AMMO diff Qword_7FF669BF0AC0_diff")
	Qword_7FF669BF07C8_diff_HP_1_xor_1_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07C8, image_base)
	Qword_7FF669BF0AC0_diff_AMMO_value_value, Qword_7FF669BF0AC0_diff_AMMO_value_addr = read_DWORD_fr_pointer(pid, 0x7FF669BF0AC0, image_base)
	Qword_7FF669BF07D8_diff_HP_3_xor_2_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07D8, image_base)

	# write XORED zero diff to two memory locations      
	write_process_memory(pid, Qword_7FF669BF0AC0_diff_AMMO_value_addr    , Qword_7FF669BF07C8_diff_HP_1_xor_1_value.to_bytes(4, byteorder='little') )
	write_process_memory(pid, Qword_7FF669BF0AC0_diff_AMMO_value_addr + 4, Qword_7FF669BF07D8_diff_HP_3_xor_2_value.to_bytes(4, byteorder='little') )

	#### cheat AMMO diff 2  >>>>>>>>.text:00007FF669BD258E<<<<<<<<<<
	print("cheat AMMO diff2 Qword_7FF669BF0880")
	Qword_7FF669BF07C8_diff_HP_1_xor_1_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07C8, image_base)
	Qword_7FF669BF0880_diff2_AMMO_value_value, Qword_7FF669BF0880_diff2_AMMO_value_addr = read_DWORD_fr_pointer(pid, 0x7FF669BF0880, image_base)
	Qword_7FF669BF07D8_diff_HP_3_xor_2_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07D8, image_base)

	# write XORED zero diff to two memory locations      
	write_process_memory(pid, Qword_7FF669BF0880_diff2_AMMO_value_addr    , Qword_7FF669BF07C8_diff_HP_1_xor_1_value.to_bytes(4, byteorder='little') )
	write_process_memory(pid, Qword_7FF669BF0880_diff2_AMMO_value_addr + 4, Qword_7FF669BF07D8_diff_HP_3_xor_2_value.to_bytes(4, byteorder='little') )


	#### cheat AMMO diff 3  >>>>>>>>.text:00007FF669BB3D25<<<<<<<<<<
	print("cheat AMMO diff3 Qword_7FF669BF0988")
	Qword_7FF669BF07C8_diff_HP_1_xor_1_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07C8, image_base)
	Qword_7FF669BF0988_diff3_AMMO_value_value, Qword_7FF669BF0988_diff3_AMMO_value_addr = read_DWORD_fr_pointer(pid, 0x7FF669BF0988, image_base)
	Qword_7FF669BF07D8_diff_HP_3_xor_2_value, _                                       = read_DWORD_fr_pointer(pid, 0x7FF669BF07D8, image_base)

	# write XORED zero diff to two memory locations      
	write_process_memory(pid, Qword_7FF669BF0988_diff3_AMMO_value_addr    , Qword_7FF669BF07C8_diff_HP_1_xor_1_value.to_bytes(4, byteorder='little') )
	write_process_memory(pid, Qword_7FF669BF0988_diff3_AMMO_value_addr + 4, Qword_7FF669BF07D8_diff_HP_3_xor_2_value.to_bytes(4, byteorder='little') )
	
	#write zero to byte_7FF669BF0B74 and dword_7FF669BF0FA4

	write_process_memory(pid, compute_addr(0x7FF669BF0B74, image_base), int(0).to_bytes(1, byteorder='little') )
	write_process_memory(pid, compute_addr(0x7FF669BF0FA4, image_base), int(0).to_bytes(4, byteorder='little') )


if __name__ == "__main__":
	CHEAT_DELAY = 0.1	

	pid, image_base = find_target_process()

	while True:
		cheat_HP(pid, image_base)
		cheat_AMMO(pid, image_base)
		
		time.sleep(CHEAT_DELAY)

