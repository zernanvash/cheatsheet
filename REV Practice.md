# REV Practice — crackmes.one CTF 2026

Progression-based checklist for the [crackmes.one CTF 2026](https://github.com/crackmesone/ctf-2026-challenges-public) reverse engineering challenges. Arranged from easiest to hardest so you build skills incrementally.

> **Local repo:** `_source_crackmesone/` — each challenge has a `Handout/` or `handout/` folder with the binary.

---

## 🟢 Tier 1 — Warm-Up (Beginner)

These challenges introduce core RE concepts: basic string analysis, patching, and simple input validation.

### 1. `wallpaper`
- [ ] **Solved**
- **Binary:** `wallpaper/handout/wallpaper` (ELF, Linux)
- **Description:** A tiny Linux binary that asks for a password. The validation logic is a straightforward comparison — a great first target for `strings`, `ltrace`, or stepping through in GDB.
- **Skills:** String analysis, basic disassembly, input tracing.
- [Show Hint](#hint-wallpaper)

### 2. `cryptpad`
- [ ] **Solved**
- **Binary:** `cryptpad/handout/cryptpad.exe` + `flag.enc` (PE, Windows)
- **Description:** An old machine left behind an encrypted flag file. Reverse the small Windows executable to understand the encryption and decrypt `flag.enc`.
- **Skills:** Small PE analysis, basic crypto reversing, file I/O tracing.
- [Show Hint](#hint-cryptpad)

### 3. `Fatmike_02` (RecordPlayer)
- [ ] **Solved**
- **Binary:** `Fatmike_02/Handout/RecordPlayer.exe` (PE x64, Windows)
- **Description:** A record player application with a broken play button. Find the button handler and apply two small patches to fix playback — the flag appears while the song plays.
- **Skills:** GUI binary analysis, finding event handlers, byte patching (`mov dl,1` → `mov dl,0`).
- [Show Hint](#hint-fatmike02)

---

## 🟡 Tier 2 — Intermediate

Encrypted flags, anti-analysis tricks, obfuscation layers, and multi-file challenges.

### 4. `httpd`
- [ ] **Solved**
- **Binary:** `httpd/handout/httpd` (ELF, Linux, ~12MB Go binary)
- **Description:** A suspicious binary found on an infected host. Figure out what it does. This is a large Go binary — navigate the bloated symbol table and find the meaningful logic.
- **Skills:** Go binary reversing, large binary navigation, identifying malicious behavior.
- [Show Hint](#hint-httpd)

### 5. `Fatmike` (Crackme)
- [ ] **Solved**
- **Binary:** `Fatmike/Handout/Crackme.exe` (PE x86, Windows)
- **Description:** Find the valid serial key to unlock the flag. The binary uses JIT decryption combined with nanomites (child process debugging tricks) to protect the validation.
- **Skills:** Anti-debug awareness, JIT decryption, nanomite bypassing, serial key validation.
- [Show Hint](#hint-fatmike)

### 6. `FLRSCRNSVR`
- [ ] **Solved**
- **Binary:** `FLRSCRNSVR/handout/FLRSCRNSVR.zip` (PE, Windows screensaver `.SCR`, password: `flare`)
- **Description:** A Windows screensaver with light anti-analysis components. The configuration mode (`/c`) writes a registry value (the flag) that is decoded during normal screensaver execution. Reverse the custom encoding algorithm.
- **Skills:** Windows screensaver internals, registry analysis, custom encoding reversal, anti-analysis bypass.
- [Show Hint](#hint-flrscrnsvr)

### 7. `moment`
- [ ] **Solved**
- **Binary:** `moment/handout/moment.exe.bin` (PE, Windows — rename to `.exe`, run in isolated env)
- **Description:** A Windows binary requiring a mixed RE approach. Circumvent various anti-tamper mechanisms to find the flag. Should be straightforward once you complete initial RE.
- **Skills:** Anti-tamper bypass, mixed static + dynamic analysis, x64dbg usage.
- [Show Hint](#hint-moment)

---

## 🟠 Tier 3 — Advanced

Multi-layer obfuscation, network simulation, crypto, and timestamp brute-forcing.

### 8. `A_MatterOfTime`
- [ ] **Solved**
- **Binary:** `A_MatterOfTime/Handout/a_matter_of_time.zip` (PE x64, Windows)
- **Description:** The flag is encrypted with AES-CBC-128. The key is a discoverable username and the IV is derived from UNIX timestamps. You need educated brute force with the right timestamp format. The binary is also obfuscated with a custom bin2bin obfuscator.
- **Skills:** AES-CBC-128 key/IV recovery, timestamp brute-forcing, deobfuscation.
- [Show Hint](#hint-amatteroftime)

### 9. `What did you type`
- [ ] **Solved**
- **Binary:** `What did you type/Handout/chall.zip` + `PbWE.txt` (large ~42MB archive)
- **Description:** Your garage was breached. Analyze captured agent logs to find out what was taken. This is a forensic-flavored RE challenge — decode the captured data.
- **Skills:** Log/keylog analysis, data reconstruction, forensic mindset.
- [Show Hint](#hint-whatdidyoutype)

### 10. `Matryoshka v2`
- [ ] **Solved**
- **Binary:** `Matryoshka v2/Handout/LicenseChecker.exe` + `Doll.dll` (~68MB DLL, PE, Windows)
- **Description:** Like nested Russian dolls — the deeper you dig, the more layers you uncover. A license checker backed by a massive DLL with hidden layers.
- **Skills:** DLL analysis, multi-layer unpacking, persistence through deep nesting.
- [Show Hint](#hint-matryoshka)

---

## 🔴 Tier 4 — Expert

Custom virtual machines, custom crypto, and network protocol reversing.

### 11. `connected`
- [ ] **Solved**
- **Binary:** `connected/handout/connected` (ELF, Linux)
- **Description:** A simulated network of 10 virtual PCs. The user sends packets through the network and specific PCs perform validation steps (length checking, hashing, XOR cipher, even-char checks). You must reverse the network protocol, discover IP addresses, and craft the right input to extract the flag from PC1.
- **Skills:** Network protocol RE, multi-component analysis, custom hash/XOR logic, packet crafting.
- [Show Hint](#hint-connected)

### 12. `FlipVM`
- [ ] **Solved**
- **Binary:** `FlipVM/Handout/FlipVM` + `code.flp` (ELF, Linux, custom VM)
- **Description:** A fully custom virtual machine with its own bytecode format (`.flp`). The VM executes virtual code that validates your input through mutation functions and decrypts the flag using a modified Kuznyechik cipher with non-standard S-boxes and GF(256) polynomial. This is the boss challenge.
- **Skills:** VM architecture reversing, custom bytecode lifting, opcode identification, modified Kuznyechik cipher, mutation inversion.
- [Show Hint](#hint-flipvm)

---

## Progress Tracker

| Tier | Solved | Total |
|---|---|---|
| 🟢 Warm-Up | ☐☐☐ | 3 |
| 🟡 Intermediate | ☐☐☐☐ | 4 |
| 🟠 Advanced | ☐☐☐ | 3 |
| 🔴 Expert | ☐☐ | 2 |
| **Total** | **0** | **12** |

---

## Hints

Scroll down only when you need them. Each hint gives you a starting direction without spoiling the solve.

---

<a id="hint-wallpaper"></a>
### 💡 wallpaper
> The binary is written in x86 assembly. Run `strings` first. If that doesn't work, try `ltrace ./wallpaper` with a test input — the comparison might be visible. For a deeper look, disassemble with `objdump -d` and trace the comparison loop. The password is a numeric string.

[↑ Back to challenge](#1-wallpaper)

---

<a id="hint-cryptpad"></a>
### 💡 cryptpad
> The executable is very small (11KB). Open it in Ghidra or IDA and look at `main`. Find where it reads `flag.enc`, what algorithm it uses to decrypt, and where the key comes from. The key may be embedded or derived from a simple source.

[↑ Back to challenge](#2-cryptpad)

---

<a id="hint-fatmike02"></a>
### 💡 Fatmike_02
> Open in x64dbg. Search for string references to find UI-related code. Locate the play button's click handler. You're looking for two `mov dl, 1` instructions right before specific function calls — patching both to `mov dl, 0` fixes the player.

[↑ Back to challenge](#3-fatmike_02-recordplayer)

---

<a id="hint-httpd"></a>
### 💡 httpd
> Go binaries are huge but the custom logic is small. In Ghidra, filter the function list for `main.` prefixed functions. Ignore the Go runtime. Focus on what the binary does with HTTP requests and where it hides its payload or C2 logic.

[↑ Back to challenge](#4-httpd)

---

<a id="hint-fatmike"></a>
### 💡 Fatmike
> The binary spawns child processes (nanomites). Watch for `CreateProcess` / `DEBUG_PROCESS` flags. The serial format is `XXXX-XXXX-XXXX-XXXX`. JIT decryption means code is decrypted at runtime — set breakpoints after the decryption routines complete to see the real validation logic.

[↑ Back to challenge](#5-fatmike-crackme)

---

<a id="hint-flrscrnsvr"></a>
### 💡 FLRSCRNSVR
> Extract with password `flare`. Remember `.SCR` files are just renamed `.exe` files. Run it with `/c` flag to trigger configuration mode. Look for registry writes (`RegSetValueEx`). The flag is encoded with a custom algorithm before being stored — reverse the encoder.

[↑ Back to challenge](#6-flrscrnsvr)

---

<a id="hint-moment"></a>
### 💡 moment
> Rename `.exe.bin` to `.exe` and run in an isolated VM. The binary has anti-tamper checks. Use x64dbg with ScyllaHide to bypass debugger detection. Once past the anti-tamper, the core logic should be visible in the decompiler.

[↑ Back to challenge](#7-moment)

---

<a id="hint-amatteroftime"></a>
### 💡 A_MatterOfTime
> Find the username first — it's the AES key. The IV comes from UNIX timestamps. You need to brute-force the timestamp within a reasonable range using the correct format (think about what precision the timestamp uses). The bin2bin obfuscation adds junk instructions — look past them.

[↑ Back to challenge](#8-a_matteroftime)

---

<a id="hint-whatdidyoutype"></a>
### 💡 What did you type
> The `PbWE.txt` file contains captured data. Think about what kind of agent could capture "what you typed." Analyze the data format and reconstruct the original input from the logs.

[↑ Back to challenge](#9-what-did-you-type)

---

<a id="hint-matryoshka"></a>
### 💡 Matryoshka v2
> The 68MB `Doll.dll` has nested layers. Start with `LicenseChecker.exe` and trace how it loads and calls into the DLL. Each layer may unpack or decrypt the next one. The password hint is in the description: `5Ecrets_WiThIn_Rus$14N_DOL1s`.

[↑ Back to challenge](#10-matryoshka-v2)

---

<a id="hint-connected"></a>
### 💡 connected
> Start by reversing how the network is simulated. Find how PCs are addressed (IP format). The user sends to a target PC, which distributes validation across PC3 (length=8), PC4 (hash), PC7 (even + printable chars via XOR on PC9). Craft input that passes all three checks. You can also talk directly to helper PCs for clues.

[↑ Back to challenge](#11-connected)

---

<a id="hint-flipvm"></a>
### 💡 FlipVM
> First, reverse the VM's instruction set by analyzing `FlipVM`. Map out the opcodes, registers, and memory model. Then disassemble `code.flp` into readable virtual instructions. The input is mutated before validation — find the mutation function and write its inverse. The flag is decrypted with a modified Kuznyechik cipher. The easiest path: patch `code.flp` to bypass the check entirely (see the solution's `patch.py` approach).

[↑ Back to challenge](#12-flipvm)

---

## Related

- [Reverse Engineering Playbook](Reverse%20Engineering%20Playbook.md)
- [IDA Pro Cheat Sheet](tools/IDA%20Pro%20Cheat%20Sheet.md)
- [Ghidra Cheat Sheet](tools/Ghidra%20Cheat%20Sheet.md)
- [x64dbg Cheat Sheet](tools/x64dbg%20Cheat%20Sheet.md)
- [GDB (gef) Cheat Sheet](tools/GDB%20Cheat%20Sheet.md)
- [REV Python Toolkit](tools/REV%20Python%20Toolkit.md)
