# Rust Crackme Easy - Dynamic Analysis Writeup

Challenge_URL: https://crackmes.one/crackme/69ceb8986793d479be018f3f

**Difficulty:** Beginner
**Platform:** Windows x64
**Language:** Rust
**Tools Used:** x64dbg, PE_Analyzer (Custom Tool)

---

## 1. Introduction
This writeup documents the reverse engineering of a Rust-based crackme. The application validates a username and a password. The goal was to extract the hardcoded credentials through dynamic analysis.

---

## 2. Initial Analysis
Using my custom **PE_Analyzer**, I performed a quick check of the binary:
* **Architecture:** x64
* **Subsystem:** Console
* **Entropy:** Normal (not packed).
* **Language:** Identified as Rust due to specific memory management and string handling patterns in the imports.

---

## 3. Dynamic Analysis & Credential Extraction

### 3.1 Locating the Validation Logic
I loaded the binary in **x64dbg** and searched for string references. After finding the prompt `"Please enter your password:"`, I set a breakpoint on the subsequent logic.

### 3.2 Register Inspection
Rust often optimizes string comparisons by loading small strings directly into 64-bit registers. By stepping through the execution to the final comparison instruction at `0x7FF6AD6E111A`, I monitored the registers.

**Found in Registers:**
* **RCX:** `746E756873736170`
* **R8:** `7372656B63617263`



### 3.3 Decoding Hex to ASCII
Converting the Little-endian hex values to ASCII revealed the hardcoded strings:
* `746E756873736170` -> **passhunt**
* `7372656B63617263` -> **crackers**

---

## 4. Execution Demo
Testing the recovered credentials against the original binary:

```text
Please enter your username:
crackers
Please enter your password:
passhunt

Correct!!!
```

---

## 5. Conclusion
The challenge was a great example of how Rust handles string comparisons in `x64` architecture. Instead of traditional string functions, the compiler utilized direct 64-bit register comparisons for speed. By intercepting the execution at the right moment, the credentials were easily recovered from the CPU state.
