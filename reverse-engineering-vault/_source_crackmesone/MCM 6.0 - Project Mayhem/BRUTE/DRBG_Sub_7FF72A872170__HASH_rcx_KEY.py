from datetime import datetime
from hash_with_salt__Sub_7FF72A871B00 import hash_with_salt__Sub_7FF72A871B00
import cupy 
import numpy
import settings

array = numpy.zeros((0x200,settings.attempts_in_GPU), dtype=cupy.uint8)

def DRBG_Sub_7FF72A872170(key_attempts):
	SALT = b"MCM6_LWE_V2"

	#start = datetime.now()
	for column, hashh in enumerate(key_attempts):  #hashh = key
		#print(hashh)
		for count in range (0x400 // 0x20):
			#print(column, count)
			hashh = hash_with_salt__Sub_7FF72A871B00(hashh, SALT)
			#print(len(hashh), count)
			array[count*0x10 + 0,column] = hashh[0]
			#array[count*0x20 + 1] = hashh[1]
			array[count*0x10 + 1,column] = hashh[2]
			#array[count*0x20 + 3] = hashh[3]
			array[count*0x10 + 2,column] = hashh[4]
			#array[count*0x20 + 5] = hashh[5]
			array[count*0x10 + 0x3,column] = hashh[6]
			#array[count*0x20 + 7] = hashh[7]
	
			array[count*0x10 + 4,column] = hashh[8]
			#array[count*0x20 + 9] = hashh[9]
			array[count*0x10 + 5,column] = hashh[10]
			#array[count*0x20 + 11] = hashh[11]
			array[count*0x10 + 6,column] = hashh[12]
			#array[count*0x20 + 13] = hashh[13]
			array[count*0x10 + 7,column] = hashh[14]
			#array[count*0x20 + 15] = hashh[15]
	
			array[count*0x10 + 8,column] = hashh[16]
			#array[count*0x20 + 17] = hashh[17]
			array[count*0x10 + 9,column] = hashh[18]
			#array[count*0x20 + 19] = hashh[19]
			array[count*0x10 + 0xA,column] = hashh[20]
			#array[count*0x20 + 21] = hashh[21]
			array[count*0x10 + 0xB,column] = hashh[22]
			#array[count*0x20 + 23] = hashh[23]
	
			array[count*0x10 + 0xC,column] = hashh[24]
			#array[count*0x20 + 25] = hashh[25]
			array[count*0x10 + 0xD,column] = hashh[26]
			#array[count*0x20 + 27] = hashh[27]
			array[count*0x10 + 0xE,column] = hashh[28]
			#array[count*0x20 + 29] = hashh[29]
			array[count*0x10 + 0xF,column] = hashh[30]
			#array[count*0x20 + 31] = hashh[31]
			#key = hashh


	print("Hashes generated")
	return cupy.asarray(array)


	