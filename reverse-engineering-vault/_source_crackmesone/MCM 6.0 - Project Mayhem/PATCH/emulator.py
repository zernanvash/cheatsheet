
import ctypes
from ctypes import wintypes
from blobs import shell_emulator_7FF72A870890

# Setting up types for a 64-bit system 
kernel32 = ctypes.windll.kernel32
kernel32.VirtualAlloc.restype = ctypes.c_void_p  # Чтобы возвращался 64-битный указатель


VirtualFree = ctypes.windll.kernel32.VirtualFree

VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.wintypes.DWORD]

VirtualFree.restype = ctypes.wintypes.BOOL
###################
ctypes.memmove.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
ctypes.memmove.restype = ctypes.c_void_p

ctypes.memset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
ctypes.memset.restype = ctypes.c_void_p




shellcode_bytes = shell_emulator_7FF72A870890

# Allocate executable memory Windows for emulator code from crackme
addr = ctypes.windll.kernel32.VirtualAlloc(None, len(shellcode_bytes), 0x3000, 0x40)
#print(hex(addr))
ctypes.memmove(addr, shellcode_bytes, len(shellcode_bytes))

# Allocate buffers for emulator context
buf_RISC_context = ctypes.create_string_buffer(0x84)
buf_RISC_commands = ctypes.create_string_buffer(0x20)

# Struct with RISC commands addreses
class MemoryPair(ctypes.Structure):
    _fields_ = [
        ("address_start", ctypes.c_void_p),
        ("address_end", ctypes.c_void_p)
    ]
bytecode_start_end = MemoryPair(address_start=ctypes.addressof(buf_RISC_commands), address_end=ctypes.addressof(buf_RISC_commands) + 0x20)



# Set up function type
proto = ctypes.CFUNCTYPE(
    ctypes.c_longlong,    # RAX
    ctypes.c_void_p,      # RCX
    ctypes.c_void_p,      # RDX
    ctypes.c_ubyte        # R8B
)
native_func = proto(addr)

def emulate_Sub_7FF72A870890(commands, val_for_r8b):
	assert(len(commands) == 0x20)
	# copy commands to buf_RISC_commands
	ctypes.memmove(buf_RISC_commands, bytes(commands), len(commands)) # or ctypes.addressof(buf_RISC_commands)   ###### (ctypes.c_ubyte * len(commands)).from_buffer(commands)
	# zeroing buf_RISC_context
	ctypes.memset(buf_RISC_context, 0, ctypes.sizeof(buf_RISC_context))
	
	#start emulator
	#print('before')
	result = native_func(
    	ctypes.addressof(bytecode_start_end), 
    	ctypes.addressof(buf_RISC_context), 
    	val_for_r8b
	)
	#print('after')
	
	return result


