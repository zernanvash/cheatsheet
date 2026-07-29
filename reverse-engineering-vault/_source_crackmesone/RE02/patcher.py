import sys

# 1. Target file
FILE_PATH = "RE02.exe"

# 2. Search boundaries
START_OFFSET = 0x8d4
END_OFFSET = 0x14cf

# 3. The byte signatures to search for (corrected 'al' to 'a1')
# b"\xe8" = CALL, b"\xe9" = JMP, b"\x90" = NOP
PATTERN_1 = b"\xe8\x64\xa1\x30\x00"
PATTERN_2 = b"\xe9\x64\xa1\x30\x00"

def patch_binary():
    try:
        with open(FILE_PATH, 'r+b') as f:
            # Read the entire file into a mutable byte array
            data = bytearray(f.read())
            patch_count = 0
            
            # --- Search and Patch Pattern 1 (E8) ---
            index = data.find(PATTERN_1, START_OFFSET, END_OFFSET + len(PATTERN_1))
            
            while index != -1 and index <= END_OFFSET:
                data[index] = 0x90  # Overwrite just the E8 byte with NOP
                print(f"[*] Patched E8 -> 90 at offset: {hex(index)}")
                patch_count += 1
                # Find the next occurrence starting from the next byte
                index = data.find(PATTERN_1, index + 1, END_OFFSET + len(PATTERN_1))
                
            # --- Search and Patch Pattern 2 (E9) ---
            index = data.find(PATTERN_2, START_OFFSET, END_OFFSET + len(PATTERN_2))
            
            while index != -1 and index <= END_OFFSET:
                data[index] = 0x90  # Overwrite just the E9 byte with NOP
                print(f"[*] Patched E9 -> 90 at offset: {hex(index)}")
                patch_count += 1
                # Find the next occurrence
                index = data.find(PATTERN_2, index + 1, END_OFFSET + len(PATTERN_2))
                
            # If patches were made, write the modified array back to disk
            if patch_count > 0:
                f.seek(0)
                f.write(data)
                print(f"[+] Successfully applied {patch_count} patches.")
            else:
                print("[-] No patterns found in the specified range. Verify your offsets.")
                
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    patch_binary()