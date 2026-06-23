# SimpleCrackme.exe - Reverse Engineering Writeup

Challenge_URL: https://crackmes.one/crackme/69b33ffcddd6176826ae8975

**Difficulty:** 1.0 (Beginner)
**Platform:** Windows PE32
**Language:** C++
**Tools Used:** Static Analysis (hex dump, disassembly), Dynamic Testing

---

## 1. Introduction

This writeup documents my approach to solving "SimpleCrackme.exe", a beginner-level crackme challenge. The goal was to find the correct password that makes the program output `[+] Access Granted!` without patching the binary.

---

## 2. Initial Reconnaissance

### 2.1 File Identification

First, I identified the target binary:

```
Filename: SimpleCrackme.exe
Size: 20,992 bytes
Type: PE32 executable (console) for MS Windows
Architecture: 32-bit x86
```

### 2.2 Basic Execution Test

Running the program with a test password:

```
Enter password: test
[-] Wrong password!
```

This confirmed the program accepts user input and validates it against some internal logic.

---

## 3. Static Analysis

### 3.1 PE Structure Analysis

Using a hex editor and PE analysis tools, I examined the file structure:

| Section | Virtual Address | Raw Offset | Purpose |
|---------|----------------|------------|---------|
| .text | 0x1000 | 0x400 | Executable code |
| .rdata | 0x4000 | 0x3000 | Read-only data (strings) |
| .data | 0x5000 | 0x3600 | Initialized data |
| .rsrc | 0x6000 | 0x3800 | Resources |
| .reloc | 0x7000 | 0x3a00 | Relocations |

### 3.2 String Search

I searched the `.rdata` section for readable strings. Instead of finding a single complete password, I discovered **12 string fragments**:

| Address (VA) | String |
|--------------|--------|
| 0x404278 | `succ` |
| 0x404280 | `ess` |
| 0x404284 | `good` |
| 0x40428c | `try` |
| 0x404290 | `but` |
| 0x404294 | `you` |
| 0x404298 | `are` |
| 0x40429c | `found` |
| 0x4042a4 | `at` |
| 0x4042a8 | `ry` |
| 0x4042ac | `pass` |
| 0x4042b4 | `01` |

This was a key insight: the password is **constructed dynamically** from multiple fragments, not stored as a single static string.

### 3.3 Understanding the Construction Logic

The presence of these fragments suggested the program uses `std::string` concatenation in C++. A typical pattern would be:

```cpp
std::string password = std::string("succ") + "ess" + "good" + "try" +
                       "but" + "you" + "are" + "found" +
                       "at" + "ry" + "pass" + "01";
```

By concatenating all fragments in the order they appear in memory:

```
succ + ess + good + try + but + you + are + found + at + ry + pass + 01
```

This yields the candidate password:

```
successgoodtrybutyouarefoundatrypass01
```

---

## 4. Verification

### 4.1 Testing the Candidate Password

I tested the constructed password against the **original, unmodified executable**:

```bash
echo "successgoodtrybutyouarefoundatrypass01" | SimpleCrackme.exe
```

**Output:**
```
Enter password:
[+] Access Granted!
```

### 4.2 Success Confirmation

The program accepted the password and displayed the success message, confirming our analysis was correct.

---

## 5. Technical Details

### 5.1 Why Fragment Storage?

This technique of storing the password in fragments serves as a basic obfuscation method:

1. **Prevents simple string searches** - Tools like `strings` won't find the complete password
2. **Complicates static analysis** - Analysts must understand the construction logic
3. **Increases analysis time** - More effort required than finding a plaintext password

### 5.2 Anti-Debugging Note

During analysis, I noticed the binary contains an `IsDebuggerPresent` check, which is a common anti-debugging technique. However, for this simple crackme, static analysis was sufficient to extract the password without needing to bypass this protection.

---

## 6. Alternative Approach: Binary Patching (For Educational Purposes)

While the challenge goal was to find the real password (not to patch), I also explored the patching approach for learning purposes.

### 6.1 Identifying the Check Logic

Through disassembly analysis, I identified two conditional jumps that lead to the "Wrong password" message:

| File Offset | Original Bytes | Instruction | Purpose |
|-------------|----------------|-------------|---------|
| 0xC80 | `75 6A` | `JNE +0x6A` | Jump if password doesn't match |
| 0xCE3 | `74 07` | `JE +0x07` | Jump to failure path |

### 6.2 NOP Sled Patching

By replacing these conditional jumps with NOP instructions (`90 90`), the program accepts any input:

```
Offset 0xC80: 75 6A → 90 90
Offset 0xCE3: 74 07 → 90 90
```

**Note:** This approach violates the spirit of most crackme challenges. The proper solution is to find the actual password, which we accomplished through string fragment analysis.

---

## 7. Conclusion

### 7.1 Solution Summary

- **Password:** `successgoodtrybutyouarefoundatrypass01`
- **Method:** Static analysis of `.rdata` section to find string fragments
- **Key Insight:** Password constructed via string concatenation, not stored as plaintext

### 7.2 Lessons Learned

1. **Always check for fragmented strings** - Not all passwords are stored as complete strings
2. **Memory layout matters** - Strings in `.rdata` often appear in construction order
3. **Verify on original binary** - Always test solutions against unmodified executables
4. **Understand the why, not just the what** - Knowing how the protection works is more valuable than just having the password

---

## 8. Tools Reference

| Tool | Purpose |
|------|---------|
| Hex Editor | Examine raw binary data and PE structure |
| `strings` | Extract readable strings from binary |
| Disassembler | Analyze x86 assembly code |
| Command Line | Test password input |

---

## 9. Final Verification Screenshot

```
C:\>echo successgoodtrybutyouarefoundatrypass01 | SimpleCrackme.exe
Enter password:
[+] Access Granted!
```

---

**Author:** Reverse Engineering Enthusiast
**Date:** March 2026
**Challenge:** SimpleCrackme.exe (Difficulty 1.0)
