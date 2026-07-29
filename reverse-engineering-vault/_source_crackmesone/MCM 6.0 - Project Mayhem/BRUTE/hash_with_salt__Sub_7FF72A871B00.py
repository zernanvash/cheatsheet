import hashlib

def hash_with_salt__Sub_7FF72A871B00(key, salt = b"MCM6_LWE_V2"):
	KEY_LEN = 0x40
	MASK1 = 0x36
	MASK2 = 0x5C
	assert(len(key) <= KEY_LEN)  # looks like the key may be longer, but this option has not been tested.

	key_40 = key.ljust(KEY_LEN, b'\x00')
		

	hash1 = hashlib.sha256(bytes(b ^ MASK1 for b in key_40) + salt).digest()
	hash_rezult = hashlib.sha256(bytes(b ^ MASK2 for b in key_40) + hash1).digest()
	
	return hash_rezult


if __name__ == "__main__":
	key1 = b'a1a2a3a4a5a6a7a8b1b2b3b4b5b6b7b8c1c2c3c4c5c6c7c8d1d2d3d4d5d6d7d8'
	test_hash1 = '2845ebe50f62017051a6a7252a6c20c1c54b9c684cbbd84fbc9df9c4ee910530'
	
	rez_hash1 = hash_with_salt__Sub_7FF72A871B00(key1)
	print("test1", rez_hash1.hex(), rez_hash1.hex() == test_hash1)


	#####
	key2 = b'a1a2a3a4a5a6a7a8b1b2b3b4b5b6b7b8'
	test_hash2 = '611acdb021af6ea96aad8837d02b66012de370e99a64fe206a4d09f5a1b2f50c'

	rez_hash2 = hash_with_salt__Sub_7FF72A871B00(key2)
	print("test2", rez_hash2.hex(), rez_hash2.hex() == test_hash2)