# CrackMe.exe Reverse Engineering Writeup

Challenge_URL: https://crackmes.one/crackme/69c53f51f2d49d8512f64b7a

## Challenge Overview

We were given a single Windows executable file, `CrackMe.exe`, with the goal of reverse engineering its verification code algorithm, building a working keygen, and producing a valid verification code for the target machine.

- **File:** `CrackMe.exe` (164,864 bytes)
- **Architecture:** 32-bit x86 (`IMAGE_FILE_MACHINE_I386`)
- **Subsystem:** Windows Console (CUI)
- **Target:** Windows Reverse Engineering sandbox

---

## Phase 1: Initial Reconnaissance

### 1.1 File Discovery and Basic Properties

The first step was simply confirming the file existed and understanding its basic properties. A quick directory listing showed only `CrackMe.exe` and a Base64-encoded copy (`crackme.b64`).

We registered the sample with the Windows Reverse MCP sandbox, which assigned it the sample ID:
```
sha256:081685df00d1ada4760c94dc35605d17c66f30a0395ea7b92fca7aefa8372510
```

### 1.2 PE Structure Analysis

Using the sandbox's PE analysis tools, we extracted the following key facts:
- **Machine Type:** `IMAGE_FILE_MACHINE_I386` (32-bit)
- **Subsystem:** `WINDOWS_CUI` (console application)
- **Not packed:** Section entropy in `.text` was ~6.62, well within normal ranges.
- **Not .NET:** No CLR header present.
- **Key Imports:** `ADVAPI32.dll` (registry APIs) and `KERNEL32.dll`.

This immediately told us we were dealing with a native C/C++ console application, likely performing some system query and user input validation.

### 1.3 String Extraction

String analysis is always the lowest-hanging fruit in reverse engineering. We extracted all readable strings from the binary and found several critical clues:

```
SOFTWARE\Microsoft\Cryptography
MachineGuid
Enter Your Verification Code: 
Good Job Bro!
Error! Invalid Code!
0123456789abcdefghijklmnopqrstuvwxyz
```

**Key Observations:**
1. The binary reads `MachineGuid` from the Windows registry. This is a well-known unique identifier for Windows installations.
2. It prompts for a "Verification Code," suggesting a keygen-style challenge.
3. It contains a base36 alphabet string (`0123456789abcdefghijklmnopqrstuvwxyz`), which initially led us to hypothesize that the key might be encoded in base36 or a similar alphanumeric scheme.
4. The success/failure messages (`Good Job Bro!` / `Error! Invalid Code!`) gave us clear targets to search for in the disassembly.

---

## Phase 2: Capability and Behavior Triage

### 2.1 Static Capability Analysis

Running a capa-style static capability triage confirmed our hypotheses and added detail:
- **Registry Query:** Uses `RegOpenKeyExA` and `RegQueryValueExA`.
- **Debugger Check:** Calls `IsDebuggerPresent`.
- **Process Suspension:** Calls `Sleep` (likely to pause before exiting).
- **PE Parsing:** Identified a function at `0x4207376` that parses PE exports and resolves functions dynamically, indicating some runtime linking obfuscation or manual import resolution.

### 2.2 Sandbox Simulation

We ran the binary in safe simulation mode. The sandbox reported:
- **Risk Score:** 40 (Medium)
- **Inferred Capabilities:** Registry modification, defense evasion

More importantly, when we executed the binary locally without providing input, it immediately printed:
```
Enter Your Verification Code: Error! Invalid Code!
```

This confirmed that the program reads from `stdin` and expects a verification code. The immediate failure suggested it might be reading from a pipe or that `stdin` was empty.

---

## Phase 3: Attempts at Dynamic Analysis

### 3.1 Frida Instrumentation (Failed)

Our first attempt at dynamic analysis was to use Frida to hook the registry read and the comparison function. However, the Frida instrumentation failed on this system. This is not uncommon in sandboxed or restricted environments, so we pivoted back to static analysis.

### 3.2 PowerShell Redirect (Failed)

We attempted to run the binary via PowerShell with `Start-Process -RedirectStandardInput`, but this failed because the input file (`in.txt`) was missing. Rather than fighting the local execution environment, we decided to solve the challenge purely through static reverse engineering and then verify the result locally.

### 3.3 Reading the Local MachineGuid

Since the binary derives its key from the local `MachineGuid`, we read the registry value directly using PowerShell:
```powershell
(Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Cryptography').MachineGuid
```

Result:
```
abd69392-f237-4f68-97c4-53bfcb788278
```

This gave us the exact input that the binary would use on this machine, which would be essential for verifying our keygen later.

---

## Phase 4: Deep Static Analysis with Ghidra

### 4.1 Launching Ghidra Analysis

With dynamic analysis blocked, we launched a deep Ghidra analysis job on the sandbox:
- **Job ID:** `3b734152-75d2-401f-bd97-c5a6ff6e9f56`
- **Estimated Time:** ~30 minutes
- **Actual Time:** ~42 seconds

Ghidra successfully analyzed the binary and extracted **886 functions**, making the function index, decompiler, and CFG workflows available.

### 4.2 Finding the Verification Function

Using the sandbox's `code_functions_search` tool, we searched for functions referencing our key strings:

**Search 1: "Enter Your Verification Code:"**
- **Match:** `FUN_00403310` at address `0x00403310`

**Search 2: "Error! Invalid Code!"**
- **Match:** `FUN_00403310` at address `0x00403310`

**Search 3: "Good Job Bro!"**
- **Match:** `FUN_00403310` at address `0x00403310`

All three strings were referenced from the same function, confirming that `0x00403310` is the main verification routine.

### 4.3 Decompiling the Registry Reader

Before diving into the main verification function, we decompiled `FUN_00402c60`, which was called at the very beginning of `FUN_00403310`. This function:
1. Opens `HKLM\SOFTWARE\Microsoft\Cryptography` with `RegOpenKeyExA`.
2. Queries the `MachineGuid` value with `RegQueryValueExA`.
3. **Removes all `-` characters** from the GUID string using a manual character-shifting loop.
4. Returns the cleaned GUID string to the caller.

This was a critical finding: the algorithm operates on the **dash-free, lowercase GUID**.

### 4.4 Decompiling the Main Verification Routine

Decompiling `FUN_00403310` revealed a large but logically straightforward function. The pseudocode was verbose due to C++ `std::string` internals (small-string optimization, heap allocations, reference counting), but the core algorithm was discernible through careful analysis.

We traced the data flow step by step:

#### Step A: Character Transformation Loop
The function iterates over each character of the dash-free GUID:
- If the character is alphabetic (`_isalpha`), it converts it to lowercase (`_tolower`) and computes `c - 'a' + 1`.
- If the character is a digit, it is appended as-is.

For our target GUID `abd69392f2374f6897c453bfcb788278`, this produced:
```
12469392623746689734532632788278
```

#### Step B: Big-Integer Division by 5
The transformed string is a 32-digit decimal number, far exceeding the 64-bit integer limit. The binary implements a **string-based long division** algorithm:
- It walks the string left-to-right.
- For each digit, it computes `value = digit + carry * 10`.
- It computes `quotient_digit = value / 5` (C-style truncation toward zero).
- It updates `carry = value % 5` (C-style modulo).
- It appends the quotient digit to a result string.

For our example, the quotient was:
```
2493878524749337946906526557655
```

#### Step C: Strip Leading Zeros
The quotient string has its leading zeros stripped. In our case, there were none to strip.

#### Step D: Big-Integer Multiplication by 2
The quotient is then multiplied by 2 using another string-based algorithm:
- It walks the string right-to-left.
- For each digit, it computes `value = digit * 2 + carry`.
- It appends `value % 10` to the result and updates `carry = value / 10`.
- If there's a final carry, it is prepended.

Result:
```
4987757049498675893813053115310
```

#### Step E: Digit-to-Letter Mapping
Finally, the function maps each decimal digit to a fixed lowercase letter:
- `0 -> x`
- `1 -> a`
- `2 -> b`
- `3 -> c`
- `4 -> d`
- `5 -> e`
- `6 -> f`
- `7 -> g`
- `8 -> h`
- `9 -> i`

This produced the final verification code:
```
dihggegxdidihfgehichacxecaaecax
```

#### Step F: Comparison
The binary then prompts the user for input, reads a line from `stdin`, and performs a standard string comparison against the generated code. If they match, it prints `Good Job Bro!` and sleeps for 3 seconds; otherwise, it prints `Error! Invalid Code!` and sleeps for 3 seconds.

---

## Phase 5: Keygen Implementation

With the algorithm fully understood, we implemented a Python keygen (`keygen.py`) that replicates the exact logic, including the C-style integer division and modulo operations (which differ from Python's floor division for negative numbers, though they were not triggered in this specific case).

### Keygen Algorithm (Python)

```python
import math

def c_div(a, b):
    return int(math.trunc(a / b))

def c_mod(a, b):
    return a - c_div(a, b) * b

def generate_code(guid):
    # Step 1: Remove dashes and map letters to 1-based positions
    s = guid.lower().replace("-", "")
    transformed = "".join(
        str(ord(c) - ord("a") + 1) if c.isalpha() else c
        for c in s
    )

    # Step 2: Divide by 5 (string-based long division)
    quotient = ""
    carry = 0
    for c in transformed:
        val = (ord(c) - ord("0")) + carry * 10
        q = c_div(val, 5)
        carry = c_mod(val, 5)
        quotient += chr(q + ord("0"))
    quotient = quotient.lstrip("0") or "0"

    # Step 3: Multiply by 2 (string-based big-int multiplication)
    result = ""
    carry = 0
    for c in reversed(quotient):
        val = (ord(c) - ord("0")) * 2 + carry
        q = c_div(val, 10)
        r = c_mod(val, 10)
        result = chr(r + ord("0")) + result
        carry = q
    if carry:
        result = chr(carry + ord("0")) + result

    # Step 4: Map digits to custom alphabet
    mapping = {
        "0": "x", "1": "a", "2": "b", "3": "c", "4": "d",
        "5": "e", "6": "f", "7": "g", "8": "h", "9": "i",
    }
    return "".join(mapping[c] for c in result)
```

### Keygen Features
- **Auto-detects local MachineGuid** from the Windows registry using `winreg`.
- **Accepts GUID as CLI argument** for offline code generation.

---

## Phase 6: Verification

### 6.1 Offline Test

We ran the keygen against the known MachineGuid:
```bash
python keygen.py abd69392-f237-4f68-97c4-53bfcb788278
```

Output:
```
MachineGuid: abd69392-f237-4f68-97c4-53bfcb788278
Verification Code: dihggegxdidihfgehichacxecaaecax
```

### 6.2 Live Binary Verification

We piped the generated code into `CrackMe.exe`:
```bash
python -c "import keygen; print(keygen.generate_code(keygen.get_machineguid()))" | .\CrackMe.exe
```

Output:
```
Enter Your Verification Code: Good Job Bro!
```

The binary accepted the code, confirming that our reverse engineering was 100% accurate.

---

## Phase 7: Dead Ends and Lessons Learned

### 7.1 The Base36 Red Herring

The presence of the string `0123456789abcdefghijklmnopqrstuvwxyz` at offset `120676` initially led us to believe the key might be a base36 encoding of the GUID or a hash thereof. We even tested a direct base36 conversion of the full GUID hex value, but the resulting code was not accepted by the binary. This string was likely a leftover from a different encoding path or a standard library string, not part of the active verification algorithm.

**Lesson:** Not every interesting string in a binary is actively used. Always trace references before building hypotheses.

### 7.2 Dynamic Analysis Blockage

Our attempts to use Frida and PowerShell redirection both failed. While frustrating, this forced us to rely on high-quality static analysis, which ultimately provided a more complete understanding of the algorithm than dynamic tracing would have.

**Lesson:** When dynamic analysis is blocked, deep static analysis (especially with Ghidra) is often sufficient for unstripped native binaries.

### 7.3 Recognizing Hand-Written Big-Integer Arithmetic

The most time-consuming part of the decompilation was recognizing that the long, loop-heavy string manipulation code was actually implementing `÷5` and `×2` on arbitrarily large decimal integers. In Ghidra's pseudocode, this was obscured by C++ `std::string` boilerplate (small-string optimization checks, heap allocation, `memcpy`-like helpers).

**Lesson:** When you see loops walking digit strings with carries and remainders, think "hand-written big-integer arithmetic," especially when the input is a long decimal string derived from a GUID.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| **Windows Reverse MCP Sandbox** | Sample ingestion, PE analysis, string extraction, capability triage, sandbox simulation |
| **Ghidra** | Deep static analysis, function recovery, decompilation of the verification routine |
| **Rizin** | Quick function listing and cross-reference inspection |
| **Python** | Keygen implementation, algorithm verification, big-integer simulation |
| **PowerShell** | Local registry inspection (`MachineGuid` extraction) and binary testing |

---

## Conclusion

`CrackMe.exe` is a straightforward but well-constructed keygen challenge. Its difficulty lies not in obfuscation or anti-analysis, but in the careful reconstruction of a custom, hand-written big-integer transformation algorithm hidden inside C++ string manipulation boilerplate.

The final algorithm is:
1. Read `MachineGuid` and remove dashes.
2. Map letters to alphabet positions, keep digits.
3. Divide the resulting decimal string by 5.
4. Multiply the quotient by 2.
5. Map digits `0-9` to `x, a-i`.

The working keygen (`keygen.py`) and this writeup fully document the solution.
