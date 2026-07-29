from unicorn import *
from unicorn.x86_const import *
import pefile
from collections import defaultdict

def count_iterations(inp):
	mu = Uc(UC_ARCH_X86, UC_MODE_64)

	mu.mem_map(0x140001000, 0x5000, UC_PROT_READ | UC_PROT_EXEC) # text
	mu.mem_map(0x1000, 0x2000, UC_PROT_READ | UC_PROT_WRITE) # stack
	mu.reg_write(UC_X86_REG_RSP, 0x2000)
	mu.reg_write(UC_X86_REG_RBP, 0)
	mu.mem_map(0x3000, 0x2000, UC_PROT_READ | UC_PROT_WRITE) # heap
	mu.mem_map(0x5000, 0x1000, UC_PROT_READ | UC_PROT_WRITE) # special buffer for input
	spec_buf = 0x5000
	mu.mem_map(0x140006000, 0x3000, UC_PROT_READ) # rdata
	mu.mem_map(0x140009000, 0x1000, UC_PROT_READ | UC_PROT_WRITE) # data


	pe = pefile.PE("crackme_very_hard.exe")
	for section in pe.sections:
		if section.Name[:5] == b'.text':
			mu.mem_write(0x140001000, section.get_data())
		elif section.Name[:6] == b'.rdata':
			mu.mem_write(0x140006000, section.get_data())
	pe.close()

	# .data section dumped by x64dbg at hardware breakpoint 14000419d with input VHARD{AAAAA-AAAAA-AAAAA}
	# this is just in case some important globals are initialized beforehand and used in the function
	with open("data.bin", "rb") as f:
		mu.mem_write(0x140009000, f.read())

	# the function we are emulating allocates a single buffer on the heap (see 140003d0a)
	# since this is the only heap allocation and we don't care where the memory goes, we replace
	# the allocating function with a dummy allocator that just returns the address to the beginning of the heap
	fake_malloc = b'\x48\xc7\xc0\x00\x30\x00\x00\xc3' # mov rax, 0x3000; ret
	mu.mem_write(0x140001000, fake_malloc)

	# the function also calls (external) memmove, which we replace with an actual implementation 
	memmove = b'\x57\x56\x48\x89\xCF\x48\x89\xD6\x4C\x89\xC1\xF3\xA4\x5E\x5F\xC3'
	mu.mem_write(0x140005486, memmove)

	# it also calls some functions that do nothing for our purposes, which we just replace with ret's
	ret_inst = b'\xc3'
	mu.mem_write(0x1400046d8, ret_inst) # atexit
	mu.mem_write(0x14000472c, ret_inst) # _Init_thread_foot
	mu.mem_write(0x140004930, ret_inst) # security_check_cookie

	# 140004798 does some thread stuff but it ultimately sets data at 140009178 to 0xffffffff
	# we thus patch 140004798 to do just that
	set_to_neg1 = b'\x50\x48\xb8\x78\x91\x00\x40\x01\x00\x00\x00\xc7\x00\xff\xff\xff\xff\x58\xc3'
	mu.mem_write(0x140004798, set_to_neg1)

	# the function also tries to read the ThreadLocalStoragePointer to check some condition
	# which (by my testing) always evaluates to true, and so I just patch the whole thing out
	# see instructions 14000343c-140003457
	gs_patch_len = 0x140003457 - 0x14000343c
	patched_inst = b'\xb8\x00\x00\x00\x80'
	patched_inst = patched_inst.ljust(gs_patch_len, b'\x90') # pad with noops
	mu.mem_write(0x14000343c, patched_inst)

	# sets arguments and calls the function 1400033c0, the one we're interested in
	# note that 140002000 is not used by the function we are emulating, and so we can overwrite it
	entry_code = b'\x48\xc7\xc1\x00\x50\x00\x00\xba\x35\x54\x61\x72\x49\xc7\xc0\x00\x00\x00\x00\xe8\xa8\x13\x00\x00\xcc'
	mu.mem_write(0x140002000, entry_code)
	end = 0x140002000 + len(entry_code) - 1

	# input std::string according to msvc
	# 8 byte pointer to actual chars
	# 8 byte padding
	# 8 byte size of string
	# 8 byte capacity
	# actual string
	assert(len(inp) == 17)
	input_string = f'VHARD{{{inp}}}'.encode()
	input_string_ptr = spec_buf + 32
	mu.mem_write(input_string_ptr, input_string)
	mu.mem_write(spec_buf, input_string_ptr.to_bytes(8, "little"))
	mu.mem_write(spec_buf + 16, (24).to_bytes(8, "little"))
	mu.mem_write(spec_buf + 24, (31).to_bytes(8, "little"))

	it_count = [0]
	def br_count(uc, address, size, count):
		count[0] += 1

	# 140003c3b is a jmp to the beginning of the loop
	# therefore the hook will count the number of iterations of the loop
	mu.hook_add(UC_HOOK_CODE, br_count, it_count, 0x140003c3b, 0x140003c3b)
	mu.emu_start(0x140002000, end)

	return it_count[0]


chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
correct = ""
for i in range(17):
	its_per_char = defaultdict(int)
	# bruteforce each possible char
	for char in chars:
		inp = correct + char + ("A" * (16 - len(correct)) )
		its_per_char[char] = count_iterations(inp) # record iterations for char

	# the character that had the highest iterations
	highest_its = max(its_per_char.items(), key=lambda x: x[1])

	# we expect the correct character to yield more iterations
	# than any other character
	lowest_its = min(its_per_char.items(), key=lambda x: x[1])
	assert(highest_its[1] > lowest_its[1])

	correct += highest_its[0]
	print(correct)

print(f"FLAG: VHARD{{{correct}}}")