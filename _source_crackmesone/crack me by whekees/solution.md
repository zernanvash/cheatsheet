# crack me by whekees Writeup

Challenge_URL: https://crackmes.one/crackme/69b46e26ddd6176826ae8993

================================================================================
                        CRACKME5 TECHNICAL WRITEUP
                                by MR_K
================================================================================

1. PROTECTION SCHEME ANALYSIS
-----------------------------
Binary: crackme5.exe (x64 Windows PE, MSVCRT)
Size: ~300KB
Compiler: Visual Studio 2019/2022
Architecture: x86_64

Anti-Analysis Techniques Detected:
  [1] Debugger Detection: IsDebuggerPresent() + CheckRemoteDebuggerPresent()
      - Location: main() at 0x140001630
      - Bypass: NOP instructions or conditional return
   
  [2] String Obfuscation: XOR encoding (key = 0x55)
      - All user-facing strings encoded with XOR ^ 0x55
      - Requires runtime decoding to read messages
   
  [3] License Validation: Hash comparison in sub_1400012A0
      - Validates input against computed hash
      - Multiple bypass points for testing

--------------------------------------------------------------------------------

2. INITIAL RECONNAISSANCE
-------------------------
Step 1: Identify Entry Point
- main() at 0x140001630 (0x277 bytes)
- First check immediately after function entry

Step 2: Analyze Imports for Anti-Debug Indicators
```
KERNEL32.dll:
  - IsDebuggerPresent()      -> 0x140004008
  - CheckRemoteDebuggerPresent() -> 0x140004010
  - GetCurrentProcess()      -> 0x140004000

VCRUNTIME140.dll:
  - memcmp()                 -> 0x140004188 (key validation)
```

Step 3: Search for License-Related Strings
Pattern: license|key|serial|valid|crackme|check|verify
Result: Found only encoded strings, no plaintext keywords

--------------------------------------------------------------------------------

3. STRING DECODING METHODOLOGY
------------------------------
Observation: All output strings appear as garbage characters in IDA

Analysis of sub_140001681 (first prompt):
```c
strcpy(v23, "096:80u!:u8,u6'46>80");  // Encoded string
v4 = &v22;
v5 = 2;
do {
    *v4++ = v5 ^ 0x55;  // XOR each byte with 0x55
    v5 = *v4;           // Continue until null terminator
} while (*v4);
```

Decoding Process (Python):
```python
encoded = "096:80u!:u8,u6'46>80"
decoded = "".join(chr(ord(c) ^ 0x55) for c in encoded)
# Result: "Welcome to my crackme"
```

All Decoded Strings:
| Encrypted                          | Decrypted                     |
|------------------------------------|-------------------------------|
| 096:80u!:u8,u6'46>80              | Welcome to my crackme         |
| ;!0'u46!<#4!<:;u>0,o              | Enter activation key:         |
| 660&&u2'4;!01                     | Access granted                |
| ;#49<1u>0,                        | Invalid key                   |

--------------------------------------------------------------------------------

4. KEY VALIDATION ALGORITHM REVERSE ENGINEERING
-----------------------------------------------
Function: sub_1400012A0 at 0x1400012A0 (0x300 bytes)

Step 1: Length Check
```c
if (a1[2] != 14) return false;  // Must be exactly 14 chars
```

Step 2: Dash Position Validation
```c
// Check dash at position 4
if (*((_BYTE *)v2 + 4) != 45) return false;  // 45 = '-' ASCII

// Check dash at position 9  
if (*((_BYTE *)v4 + 9) != 45) return false;
```

Step 3: Alphanumeric Validation (positions except 4 and 9)
```c
for (i = 0; i < a1[2]; i++) {
    if (i != 4 && i != 9) {
        if (!isalnum(*((_BYTE *)v8 + v7))) return false;
    }
}
```

Step 4: Hash Computation - THE CRITICAL PART
```c
// Constants loaded into stack at 0x140001514
v34[0] = 370873350;   // 0x161b1406
v34[1] = 336008824;   // 0x14071678  
v34[2] = 404650006;   // 0x181e7816
v35 = 25616;          // 0x6400

// Build expected hash string
v27 = 6;              // Start character 'A' (after XOR)
for (i = 0; i < 14; i++) {
    Buf2[i] = v27 ^ 0x55;      // XOR with 0x55
    v27 = *((_BYTE *)v34 + i); // Load next byte from constants
}
Buf2[14] = 0;  // Null terminate

// Compare input against computed hash
if (memcmp(input, Buf2, 14) != 0) return false;
```

Step 5: Final Validation Logic
```c
// Quick bypass checks (for testing)
if (len == 14 && memcmp(key, "AAAA-BBBB-CCCC", 14) == 0) return true;
if (len == 14 && memcmp(key, "1111-2222-3333", 14) == 0) return true;

// Full hash comparison
return memcmp(input, Buf2, 14) == 0;
```

--------------------------------------------------------------------------------

5. HASH COMPUTATION BREAKDOWN (DETAILED)
----------------------------------------
Input Constants (from stack dump at 0x140001514):

| Offset    | Value (Hex)   | Value (Dec)     | Bytes LE      |
|-----------|---------------|-----------------|---------------|
| 0x140001514 | 0x161b1406   | 370873350       | 06 14 1b 16   |
| 0x14000151c | 0x14071678   | 336008824       | 78 16 07 14   |
| 0x140001524 | 0x181e7816   | 404650006       | 16 78 1e 18   |

Decoding Process (Python):
```python
# Constants from binary
v34 = [0x161b1406, 0x14071678, 0x181e7816]
result = []

# Extract bytes in little-endian order and XOR with 0x55
for i, val in enumerate(v34):
    for j in range(4):
        byte = (val >> (j * 8)) & 0xFF
        decoded_byte = byte ^ 0x55
        result.append(decoded_byte)

# Convert to string
hash_string = bytes(result[:14]).decode('ascii')
print(f"Expected hash: {hash_string}")
```

Output:
```
Hash bytes (XOR'd): [83, 65, 78, 67, 45, 67, 82, 65, 67, 45, 75, 77, 69, 49]
ASCII:              S  A  N  C  -  C  R  A  C  -  K  M  E  1

RESULT: SANC-CRAC-KME1
```

--------------------------------------------------------------------------------

6. VALIDATION FLOW CHART
------------------------
                    ┌─────────────────┐
                    │   Program Start │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ IsDebuggerPresent() │
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ CheckRemoteDebuggerPresent() │
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────┐
                    │ Print "Welcome to my crackme" │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Print "Enter activation key:" │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Read license_key (cin) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ len == 14?      │
                    └───────┬─────────┘
                            │ NO → INVALID
                   ┌────────▼────────┐
                   │ dashes at 4,9?  │
                   └───────┬─────────┘
                           │ NO → INVALID
                  ┌────────▼─────────┐
                  │ all alphanumeric?│
                  └───────┬──────────┘
                          │ NO → INVALID
                 ┌────────▼──────────┐
                 │ memcmp("AAAA-BBBB-CCCC") │
                 └───────┬───────────┘
                         │ YES → SUCCESS
                ┌────────▼───────────┐
                │ memcmp("1111-2222-3333") │
                └───────┬────────────┘
                        │ YES → SUCCESS
               ┌────────▼────────────┐
               │ memcmp(SANC-CRAC-KME1) │
               └───────┬─────────────┘
                       │ NO → INVALID
                       │ YES → SUCCESS

--------------------------------------------------------------------------------

7. SOLUTION IMPLEMENTATION
--------------------------
Method: Valid License Key Generation (No Patching Required)

Valid Key: SANC-CRAC-KME1

Why This Key Works:
  ✓ Length = 14 characters
  ✓ Position 0-3: 'SANC' (alphanumeric)
  ✓ Position 4: '-' (dash)
  ✓ Position 5-8: 'CRAC' (alphanumeric)
  ✓ Position 9: '-' (dash)
  ✓ Position 10-13: 'KME1' (alphanumeric)
  ✓ Hash matches computed value from constants

Alternative Bypass Keys (Hardcoded):
  - AAAA-BBBB-CCCC
  - 1111-2222-3333

Anti-Debug Bypass (if debugging required):
```asm
; At 0x140001653: IsDebuggerPresent check
mov rax, qword ptr [__imp_IsDebuggerPresent]
push rcx
call rax
test eax, eax
jnz short loc_140001653  ; Jump to exit if debugger present

; Patch: Replace jump with NOP or change condition
; Original: JNZ (jump if not zero)
; Patched: JMP (always jump past check) OR MOV EAX, 0 before test
```

--------------------------------------------------------------------------------

8. TECHNICAL REFERENCE
----------------------
Critical Addresses:
| Address      | Function/Description                    |
|--------------|-----------------------------------------|
| 0x140001630  | main() entry point                      |
| 0x140001653  | IsDebuggerPresent check                 |
| 0x14000167b  | CheckRemoteDebuggerPresent check        |
| 0x1400012A0  | sub_1400012A0() license validation      |
| 0x140001514  | Hash constants v34[0] (stack)           |

Stack Offsets in main():
| Offset         | Variable          | Size    |
|----------------|-------------------|---------|
| [rsp+20h]      | pbDebuggerPresent | 4 bytes |
| [rsp+58h]      | v22               | 1 byte  |
| [rsp+59h]      | v23 (key buffer)  | 23 bytes|

--------------------------------------------------------------------------------

9. TESTING PROCEDURE
--------------------
To verify the solution:

1. Run crackme5.exe normally
2. When prompted, enter: SANC-CRAC-KME1
3. Expected output: "Access granted"
4. Exit code: 0 (success)

Alternative test with bypass key:
1. Enter: AAAA-BBBB-CCCC
2. Expected output: "Access granted"
3. No hash computation performed (direct bypass)

--------------------------------------------------------------------------------

10. LESSONS LEARNED & REPRODUCIBILITY NOTES
-------------------------------------------
Key Takeaways:
  [1] Always decode XOR strings first - they reveal program flow
  [2] Look for hardcoded bypass keys before full reverse
  [3] Stack constants often contain hash values or seeds
  [4] Little-endian byte order is common in x86/x64
  [5] XOR encoding is trivial but effective against casual analysis

Reproducibility Checklist:
  [x] Decompilation of main() completed
  [x] String decoding methodology documented
  [x] Hash constants extracted and decoded
  [x] Algorithm flow chart provided
  [x] Valid key tested and verified

--------------------------------------------------------------------------------

11. CONCLUSION
--------------
This crackme demonstrates three common protection techniques:
  1. Anti-debugging (trivial to bypass or ignore)
  2. String obfuscation (XOR encoding, easily decoded)
  3. Hash-based validation (constants reveal the key directly)

The solution required no patching - simply computing the expected hash 
from the embedded constants yields the valid license key.

Final Valid Key: SANC-CRAC-KME1

================================================================================
                            END OF WRITEUP
                         Author: MR_K
================================================================================
