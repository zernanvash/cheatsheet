# [Write-up] BABEL_VM CrackMe by w33d

Challenge_URL: https://crackmes.one/crackme/69ca6a30f2d49d8512f64bcc

## 1. Challenge Overview
**Target:** `babel_vm.exe`  
**Difficulty:** Level 3-4 (Medium/Hard)  
**Objective:** Reverse engineer the custom multi-layer VM architecture and implement a functional Python keygen.

The binary is a classic VM-protected CrackMe. It takes a username (4-64 chars) and a serial in the format `XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX`. Validation is performed across several layers of custom virtual machines.

---

## 2. Analysis Environment
To ensure a safe and consistent analysis environment, the binary was analyzed inside a **VirtualBox Virtual Machine** running **Windows 10 (Flare-VM)**. 

Using a VM allowed for:
- **System Isolation**: Protecting the host machine from any potential malicious behavior or system-level changes caused by the CrackMe.
- **Snapshotting**: The ability to save the system state before running the binary, allowing for easy reverts during dynamic analysis.
- **Tool Integration**: Using a pre-configured environment with all necessary debuggers and decompilers ready to go.

---

## 3. Tools Used
- **VirtualBox**: For hosting the isolated analysis environment.
- **Ghidra**: Static analysis and decompilation of the protected binary.
- **Python**: To write the custom VM emulator, bytecode extractors, and the final keygen.
- **x64dbg / Process Hacker**: To monitor memory allocations and verify that the bytecode was being decrypted correctly in real-time.

---

## 3. Analysis Phase

### 3.1 Input and Hashing
The crackme starts by reading the username and calculating a custom **Murmur-like hash** with a seed of `0x42414245` ("BABE"). This 32-bit hash is split into two 16-bit words (`H0` and `H1`), which serve as the foundation for all subsequent serial checks.

### 3.2 The Outer State Machine
Instead of a straight-line validation, the binary uses an **Outer State Machine** dispatcher. Different phases of validation (hashing, decryption, VM execution) are triggered by state codes like `0xA7`, `0x21`, `0x5E`, and `0xF1`.

### 3.3 The Virtual Machine Layer (The "Babel" Architecture)
The core validation happens in `Phase 0xF1`, which starts a complex, multi-layered VM environment.

#### The Primary VM (Register-based)
- **Registers:** 8 general-purpose 32-bit registers (r0-r7).
- **Source Registers:** A special array containing `[H0, H1, S0, S1, S2, S3, S4, S5, S6, S7]`.
- **Bytecode:** XOR-encrypted bytecode (`Key: 5A 1C BE B4`) that is decrypted into memory at runtime.
- **Opcodes:** ~40 unique instructions (ADD, XOR, ROL, CMP, LOAD_SREG, etc.).
- **Trick:** The VM uses a `STORE_BC` instruction, meaning the VM bytecodes can **self-modify** during execution to thwart static analysis.

#### The Secondary VMs (Stack-based)
Within the Primary VM, there is an `INVOKE_VM2` opcode. This pauses the primary VM and starts one of three **secondary stack VMs**.
- Each secondary VM has its own XOR key and bytecode.
- They are used specifically to validate the last three words of the serial (`S5`, `S6`, and `S7`).
- **The Trap:** In the secondary VMs, opcodes `0x11` (JZ) and `0x12` (JNZ) have **inverted logic**. If you assume `0x11` is JNZ, your solver will fail.

### 3.4 The Red Herrings
The author included a **Modular Exponentiation** check (`pow(serial, 0x10001, 0xB18ED267E013)`). However, the final check against the result is a mathematical tautology (`x*(x+1) % 2 == 0`) which **always passes**. This is a distraction to lead reverse engineers down an RSA-reversing hole.

---

## 4. Solving Strategy: The Self-Solving Emulator

Because the VM uses self-modifying code and complex branch dependencies, manual derivation of the serial formula is extremely tedious. 

**My approach:** 
1. **Emulate:** Build a complete Python-based emulator for both the Primary and Secondary VMs.
2. **Cheat:** Since we control the emulator, we can "interpose" on the `CMP` (Compare) instructions. 
   - For `S0-S4`: If the VM compares a register holding our serial word against a target value, we simply patch our serial word in memory with the expected target.
   - For `S5-S7`: Since these are checked by the stack VMs independently, we simply **brute-force** the 16-bit range (`0x0000 - 0xFFFF`) for each word until the VM returns `True`.

This hybrid "interception + brute-force" approach generates a valid serial for any username in under 2 seconds.

---

## 5. Keygen Implementation (Python)
The keygen logic involves replicating the hashing algorithm and running the emulation layers to find all 8 serial segments. The final product is a standalone Python script `keygen.py`.

---

## 6. Lessons Learned
- **Don't trust the names:** Always verify branch logic (JZ/JNZ) in custom VMs.
- **Emulation is King:** When dealing with self-modifying code or multi-stage obfuscation, building an emulator is often faster than static reversing.
- **Identify Tautologies:** Mathematical "RSA-style" checks at the end of a CrackMe are often red herrings if the final comparison result is always true.
