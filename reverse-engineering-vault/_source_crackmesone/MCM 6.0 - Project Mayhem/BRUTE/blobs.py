import numpy
import cupy
import settings

with open("DMP_in_00007FF72A872516_addr_RBP(BUF_100000h).bin", "rb") as f_00007FF72A872516:
	#BUF_100000 = f_00007FF72A872516.read()
	vec_from_buf100000 = numpy.zeros((0x200, 0x200), dtype=cupy.uint8)
	for iii in range(0x200):
		dwords_line = f_00007FF72A872516.read(0x800)
		for jjj in range(0x200):
			vec_from_buf100000[iii][jjj] = dwords_line[jjj*4]

	cupy_vec_from_buf100000 = cupy.asarray(vec_from_buf100000)
	
	#ones = cupy.ones((settings.attempts_in_GPU, 1))
	#cupy_vec_0x800_7FF72A8B4CA0 = np.transpose(ones @ cupy_vec_0x800_7FF72A8B4CA0.reshape(1,-1))  ## mb remove np.transpose(		

with open("Dword_7FF72A8B4CA0_dump_orig_fr_exe.bin", "rb") as f_7FF72A8B4CA0:
	BUF_0x800_7FF72A8B4CA0 = f_7FF72A8B4CA0.read()
	vec_0x800_7FF72A8B4CA0 = numpy.zeros(0x200, dtype=numpy.uint8)
	for iii in range(0x200):
		vec_0x800_7FF72A8B4CA0[iii] = BUF_0x800_7FF72A8B4CA0[iii*4]


	cupy_vec_0x800_7FF72A8B4CA0 = cupy.asarray(vec_0x800_7FF72A8B4CA0)


HARDCODED = bytes.fromhex("""
46 F6 FD F2 71 A9 CD B3  75 AA DA E4 16 97 D2 A9
4F 85 E9 E0 52 A0 EB 8F  6D 84 E9 E5 E9 32 A4 D8
3D EC CD A6 7C 58 08 77  8B 39 4F 08 EA D2 9B EE
0E B6 E1 B7 BC 4E 2D 6D  EE 24 63 13 36 D4 94 C8
""")

REZULT_SSSub_7FF72A870890_VM = 0   # evaluated with any key