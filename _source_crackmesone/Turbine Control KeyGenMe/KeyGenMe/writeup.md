# Write-up: TurbineControl.exe KeyGenMe

Challenge_URL: https://crackmes.one/crackme/69bd737bf2d49d8512f64adc

## 1. Challenge Overview
The `TurbineControl.exe` challenge is a Windows KeyGenMe centered around an industrial SCADA/monitoring theme. Upon execution, the program generates a dynamic 5-character Hardware ID (HWID) and requires a 16-character license key in the format `XXXX-YYYY-ZZZZ-WWWW`.

Through reverse engineering, we identified that the license key is not static but is mathematically derived from the HWID.

## 2. Initial Analysis
Static analysis of the entry point revealed two decoy keys (`TCAL-DIAG-MSTR-2024` and `ADMN-ROOT-PASS-9999`). While these keys pass initial format checks, they trigger a "CRITICAL UNAUTHORIZED ACCESS" message because they fail a second-stage validation that checks the key against the dynamic HWID.

The core validation logic resides in a function that splits the input key into four 4-character blocks and validates each block sequentially.

## 3. Reversing the Validation Logic

### Part 1: XXXX (HWID-Based Mapping)
The first block is derived directly from the 5-character HWID.
- Each of the first 4 bytes of the HWID is transformed: `(HWID[i] + 3) XOR HWID[4] XOR 0x1F`.
- The result is taken modulo 93 and mapped to the printable ASCII range starting at `0x21`.
- The character `-` (0x2D) is explicitly skipped by incrementing the result if it falls on or after that value.

### Part 2: YYYY (Chained Substitution)
The second block uses a 256-character lookup table (substitution cipher) found at a fixed offset in the binary.
- The first character is `table[sum_of_part1_bytes % 256]`.
- Subsequent characters are "chained": `char[i] = table[(char[i-1] + sum_of_part1_bytes) % 256]`.

### Part 3: ZZZZ (Arithmetic Constraints)
This block must satisfy two specific arithmetic conditions:
1.  `ord(char[0]) * ord(char[1]) == 5040`.
2.  `ord(char[2]) + ord(char[3]) == 150`.
Our KeyGen satisfies these by selecting printable, typeable characters (e.g., `(/!u`).

### Part 4: WWWW (Polynomial Hash)
The final block is a verification hash of the first three blocks.
- It uses a polynomial hash with base 31: `hash = (hash * 31) + byte`.
- The final result is `hash % 10000`, formatted as a 4-digit zero-padded string (e.g., `4422`).

## 4. KeyGen Implementation
The solution script `keygen.py` automates this process:
1.  Extracts the HWID.
2.  Computes Part 1 via XOR/Modulo.
3.  Performs the chained lookup for Part 2.
4.  Selects valid characters for Part 3.
5.  Hashes the results to generate Part 4.

## 5. Conclusion
By reversing the relationship between the HWID and the key blocks, we can generate a valid license for any machine. Entering the correct key unlocks the "Diagnostic and Calibration Suite," which in this binary is represented by a successful diagnostic message loop.
