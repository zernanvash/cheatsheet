# Reverse Engineering Tool Workflow

Decision workflow for CTF/crackme reverse engineering when your main lab is Kali Linux and your Windows host is used for Windows PE challenges.

Source tool catalogs:

- [NTHW Reverse Engineering tools](https://github.com/notthehiddenwiki/NTHW/blob/nthw/Blue%20Team/Reverse%20Engineering/tools.md)
- [Awesome Reversing](https://github.com/tylerha97/awesome-reversing/blob/master/README.md)

---

## Lab Split

Use **Kali** for safe first-pass triage, scripting, ELF analysis, Android unpacking, bytecode work, and solver development.

Use **Windows host or Windows VM** for PE GUI behavior, Windows API behavior, .NET tooling, x64dbg, PE-Bear, Process Hacker, and FLARE tooling. Prefer a Windows VM or snapshot when running unknown files.

| Situation | Use Kali | Use Windows |
| --- | --- | --- |
| Unknown file | `file`, `sha256sum`, `strings`, `binwalk`, `xxd`, `rabin2`, `rizin/r2` | PE-Bear, Detect It Easy, PEStudio, CFF Explorer |
| ELF binary | Ghidra, Cutter, radare2/Rizin, GDB/gef, Qiling, Z3 | Usually not needed |
| Windows PE native | Ghidra/IDA/Cutter static review, `pefile`, FLOSS | PE-Bear, x64dbg, Process Hacker, dnSpy only if .NET |
| .NET binary | Basic strings/hash only | dnSpy, AvaloniaILSpy, ILSpy-style decompilers |
| Python EXE | `pyinstxtractor`, `python-exe-unpacker`, `pycdc` | Run only if needed in VM |
| Android APK | `apk.sh`, Apktool, ReverseAPK, jadx if installed | Usually not needed |
| Obfuscated script/document | Python helpers, Synchrony for JS, batch deobfuscator, oletools | Script host testing in VM if required |
| Packed/anti-debug PE | Static triage, entropy/import review | x64dbg, PE-Bear, Process Hacker, snapshots |
| Crypto/check constraints | Python, Z3, angr if available | Verify original binary only |

---

## Phase 0 - Intake Rules

1. Copy the challenge into a case folder:

```bash
mkdir -p cases/challenge_name/{orig,work,notes}
cp challenge_file cases/challenge_name/orig/
sha256sum cases/challenge_name/orig/* | tee cases/challenge_name/notes/hashes.txt
```

2. Do not run unknown Windows PE files on the bare host unless the challenge is trusted and intentionally benign. Use a Windows VM/snapshot for dynamic work.

3. Keep the original untouched. Patch copies only.

---

## Phase 1 - Fast Triage

Run this before choosing heavy tools.

```bash
file ./target
sha256sum ./target
strings -a -n 5 ./target | head -80
strings -a -el ./target | head -80
```

If available:

```bash
rabin2 -I ./target
rabin2 -z ./target
rizin -qq -c 'iI; iz; ii; iS' ./target
```

Choose the branch:

| Evidence                                                        | Branch                                                      |
| --------------------------------------------------------------- | ----------------------------------------------------------- |
| `PE32`, `PE32+`, `.exe`, `.dll[Windows PE](#windows-pe-native)` | [Windows PE](#windows-pe-native)                            |
| `Mono/.Net`, `mscoree.dll`, `BSJB`, readable C# names           | [.NET](#net-pe)                                             |
| `ELF`                                                           | [Linux ELF](#linux-elf)                                     |
| `PyInstaller`, `PYZ`, Python DLL/imports                        | [Python EXE](#python-exe-or-bytecode)                       |
| `.apk`, `AndroidManifest.xml`, `classes.dex`                    | [Android APK](#android-apk)                                 |
| `.doc`, `.docm`, `.xls`, `.xlsm`, `.pdf`, macro strings         | [Document or Macro](#document-or-macro)                     |
| high entropy, tiny imports, UPX/packer strings                  | [Packed or Obfuscated](#packed-or-obfuscated-native-binary) |
| encrypted data file plus small checker                          | [Crypto/Data Transform](#crypto-or-data-transform)          |
| asks for serial/password                                        | [Crackme Validation](#password-or-serial-crackme)           |

---

## Windows PE Native

Use this when the target is a normal C/C++/Delphi/Go/Rust PE.

### Static First

1. **PE-Bear**, **Detect It Easy**, **PEStudio**, **CFF Explorer**, or **PPEE** on Windows:
   - Check architecture, subsystem, sections, imports, resources.
   - Suspicious signs: high entropy `.text`, RWX section, weird entry point, very few imports.
   - Use CFF Explorer/PPEE when you need a deeper PE header, directory, import, export, or resource view.

2. **Ghidra or IDA Pro**:
   - Find `main`, `WinMain`, dialog procedures, button handlers, and validation functions.
   - Search strings for `flag`, `serial`, `wrong`, `correct`, `GetDlgItemText`, `MessageBox`, `CreateFile`, `ReadFile`, `WriteFile`.

3. **FLOSS**:

```powershell
floss.exe target.exe
```

Use FLOSS when normal `strings` is weak or you suspect decoded strings.

### Dynamic When Needed

Use **x64dbg** when static analysis shows a branch you need to observe or patch.

Common breakpoints:

| Goal | Break on |
| --- | --- |
| Password input | `GetDlgItemTextA/W`, `ReadFile`, `fgets`, `scanf`, `GetCommandLineA/W` |
| Success/fail message | `MessageBoxA/W`, string references, branch before message |
| File crypto | `CreateFileA/W`, `ReadFile`, `WriteFile` |
| Anti-debug | `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess` |
| Process tricks | `CreateProcessA/W`, `DebugActiveProcess`, `WaitForDebugEvent` |

Use **Process Hacker** or **Process Explorer** when the challenge creates child processes, checks handles, injects, or spawns helper binaries.

Use **ProcMon** when you need filesystem, registry, process, or DLL-load evidence without stepping through every call.

Use **API Monitor** when the key behavior is a Windows API sequence and x64dbg is too low-level for the question.

Use **FakeNet-NG**, **iNetSim**, or **Wireshark** when the binary phones home, resolves domains, waits for a server, or implements a custom protocol.

Use **WinDbg** instead of x64dbg when the challenge needs lower-level Windows debugging, exception-heavy behavior, driver/kernel context, or better insight into Windows internals.

Use **GhidraX64Dbg** or x64dbg scripts when you want Ghidra labels/comments to guide dynamic debugging.

---

## .NET PE

Evidence: `mscoree.dll`, `.NET` metadata, `BSJB`, readable class/method names.

Use **dnSpy** first if you need debugging or patching. Use **AvaloniaILSpy** for cross-platform decompilation/read-only review.

Workflow:

1. Open in dnSpy.
2. Search for `flag`, `password`, `serial`, `Check`, `Validate`, `Button_Click`.
3. Read the validation method as C#.
4. If logic is direct, write a Python solver.
5. If the program hides values at runtime, debug in dnSpy and watch locals.
6. Patch only a copy if the challenge asks for patching.

Do not waste time in Ghidra for normal .NET unless native stubs or packers are involved.

---

## Linux ELF

Use Kali as the main environment.

Static:

```bash
file ./target
checksec --file=./target
strings -a ./target | less
rabin2 -I ./target
rabin2 -z ./target
```

Use **Ghidra**, **Cutter**, **radare2/Rizin**, or **IDA Free/Pro** for disassembly/decompilation.

Dynamic:

```bash
gdb ./target
```

Good breakpoints:

| Goal | Break on |
| --- | --- |
| Password compare | `strcmp`, `strncmp`, `memcmp` |
| Input | `fgets`, `scanf`, `read` |
| Crypto loop | suspected transform function |
| Exit before success | conditional branch before fail path |

Use **Qiling** if you want to emulate a binary or hook APIs without fully running it on your system. Use **QBDI**, **Pin**, or **PANDA** only when coverage/instrumentation matters; they are heavier than GDB.

---

## Python EXE or Bytecode

Evidence: PyInstaller strings, `PYZ`, bundled `python*.dll`, `.pyc`, `__main__`.

Use Kali:

```bash
python pyinstxtractor.py target.exe
python python-exe-unpacker.py target.exe
pycdc extracted_file.pyc > recovered.py
```

Then read the recovered Python and solve normally. If decompilation is messy, disassemble bytecode and reconstruct only the validation or decryption path.

---

## Android APK

Use this when the challenge gives an `.apk` or `classes.dex`.

Tools from the NTHW list:

| Tool | Use when |
| --- | --- |
| `apk.sh` | One-command unpacking and baseline analysis |
| Apktool | Resources, manifest, smali, patch/rebuild |
| ReverseAPK | Quick APK analysis pipeline |
| Sixo Online APK Analyzer | Quick external read-only check if allowed |

Workflow:

```bash
apktool d app.apk -o app_dec
```

Then inspect:

```bash
grep -R "flag\\|password\\|serial\\|check\\|validate" -n app_dec
```

Use jadx if available for Java-like source. Use Apktool/smali when Java decompilation lies or the check is in bytecode details.

---

## Obfuscated Script

| File type | First tool | Then |
| --- | --- | --- |
| JavaScript | Synchrony | Beautifier, manual rename, Node sandbox |
| Batch | batch_deobfuscator | Manual variable expansion |
| VBA macro | Vba2Graph | oletools/VBA extraction if installed |
| Python | `pycdc`, `dis`, manual cleanup | Run functions with controlled inputs |

Rule: deobfuscate into a readable copy, then identify inputs, transforms, constants, and final comparison.

---

## Document or Macro

Use this when the challenge is an Office document, macro-enabled file, PDF, or embedded script container.

| File type | First tool | Then |
| --- | --- | --- |
| Office macro | oletools, Vba2Graph | Extract VBA, graph calls, deobfuscate strings |
| PDF | Didier Stevens PDF tools, Origami | Inspect objects, streams, JavaScript, embedded files |
| Unknown container | `file`, `binwalk`, ImHex | Extract embedded payloads |

Workflow:

```bash
olevba sample.docm
```

For PDFs, inspect before opening in a reader:

```bash
pdfid.py sample.pdf
pdf-parser.py sample.pdf
```

Escalate to a Windows VM only if the document must execute to reveal behavior.

---

## Packed or Obfuscated Native Binary

Signs:

- Very few imports.
- High entropy sections.
- Entry point outside normal `.text`.
- UPX or custom packer strings.
- Normal strings missing, but UI or behavior suggests hidden text.
- x64dbg reaches lots of junk code or anti-debug checks.

Workflow:

1. **PE-Bear**, **Detect It Easy**, or **PEStudio**: section entropy, entry point, imports, packer hints.
2. **FLOSS**: decoded strings.
3. **Ghidra/IDA**: identify unpacking stub and real code references.
4. **x64dbg**: run to original entry point if needed, dump memory after unpacking.
5. **Scylla**, **ImpRec**, or **LordPE**: reconstruct imports after a runtime dump if the unpacked PE does not run cleanly.
6. **NoVmp/Stadeo/msynth** only when the evidence matches:
   - NoVmp: VMProtect x64 3.x style virtualization.
   - Stadeo: control-flow flattening/string obfuscation.
   - msynth: mixed Boolean-arithmetic expressions.

Avoid advanced deobfuscators until you have evidence. Most CTF packers are solved faster by finding the unpacked code or runtime strings.

---

## Crypto or Data Transform

Use this when the target reads a file, decrypts something, or validates input through math.

1. Find I/O calls:
   - PE: `CreateFile`, `ReadFile`, `WriteFile`.
   - ELF: `open`, `read`, `fread`, `write`.
2. Find constants:
   - XOR keys, S-boxes, rotations, magic values, base64 alphabets.
3. Reimplement the transform in Python.
4. Use **Z3** when input bytes are constrained by equations, bitwise relations, modulo arithmetic, or multiple checks.

Z3 skeleton:

```python
from z3 import *

n = 16
xs = [BitVec(f"x{i}", 8) for i in range(n)]
s = Solver()

for x in xs:
    s.add(x >= 0x20, x <= 0x7e)

# Add recovered constraints here.

if s.check() == sat:
    m = s.model()
    print(bytes([m[x].as_long() for x in xs]))
```

Use **ImHex**, **rehex**, or **hexedit** when you need to inspect binary structures or patch bytes precisely.

---

## Password or Serial Crackme

Fast path:

1. Search strings for success/failure text.
2. Cross-reference those strings in Ghidra/IDA/Cutter.
3. Find the branch deciding success.
4. Work backward to the validation function.
5. Decide:
   - Direct compare: recover constant or observe `strcmp`.
   - Transform then compare: reimplement transform.
   - Many arithmetic constraints: use Z3.
   - GUI-only path: use x64dbg breakpoints on input/message APIs.
   - Patch challenge: flip conditional branch or force return value.

Do not begin by patching unless the objective is patching. For most CTF reverse challenges, extracting the actual key/flag is more valuable.

---

## Firmware or Embedded

Use this only when the file looks like firmware, raw blobs, bare-metal ARM/MIPS, or memory images.

Tools:

| Tool | Use |
| --- | --- |
| ghidra-firmware-utils | Loader/helpers for firmware blobs |
| SVD-Loader-Ghidra | Bare-metal ARM peripheral/register context |
| binwalk | Extract filesystems and embedded payloads |
| Ghidra | Main static analysis |
| ImHex | Structure inspection |

Workflow:

```bash
binwalk -e firmware.bin
strings -a firmware.bin | less
```

Then identify architecture, base address, reset vector, and memory map before decompiling deeply.

---

## Malware-Style Challenge

For malware analysis exercises only, prefer isolation.

Use:

- **FLARE VM** on a Windows VM for Windows malware-style PE challenges.
- **Limon** for Linux malware sandboxing.
- **Qu1cksc0pe** for quick all-in-one static triage.
- **ProcMon**, **Process Explorer**, **API Monitor**, **FakeNet-NG**, and **Wireshark** for controlled Windows behavior tracing.
- **DRAKVUF Sandbox**, **Freki**, **Aleph**, or **PANDA** only for heavier dynamic pipelines.
- **Awesome Malware Analysis** as a tool index when the challenge moves outside normal CTF reversing.

Never use live malware sample repositories such as theZoo or vx-underground collections on your host OS.

---

## Tool Choice Cheat Sheet

| Current challenge situation | Tool to use now | Why |
| --- | --- | --- |
| I do not know what this file is | `file`, `strings`, `rabin2`, Detect It Easy, PE-Bear | Fast identification |
| I need PE headers/resources/imports | PE-Bear, CFF Explorer, PEStudio, PPEE | Format-level inspection |
| Windows EXE with GUI | PE-Bear + Ghidra, then x64dbg | Static structure plus event-handler debugging |
| Windows EXE asks for serial | Ghidra/IDA + x64dbg | Find validation and observe branches |
| Windows EXE has no useful strings | FLOSS, x64dbg runtime breakpoints | Strings may be decoded at runtime |
| Windows EXE creates another process | x64dbg + Process Hacker/Process Explorer | See process/debug tricks |
| Windows EXE touches files/registry | ProcMon | Trace behavior quickly |
| Windows EXE calls many APIs | API Monitor | Observe API sequence without instruction stepping |
| Windows EXE waits for network | FakeNet-NG/iNetSim + Wireshark | Simulate services and capture traffic |
| Unpacked PE will not run | Scylla, ImpRec, LordPE | Rebuild imports after dumping |
| PE imports `mscoree.dll` | dnSpy or AvaloniaILSpy | It is probably .NET |
| Python-packed EXE | pyinstxtractor + pycdc | Recover source/bytecode |
| ELF asks for password | Ghidra/Cutter + GDB | Decompile then verify dynamically |
| Decompiled code is equation-heavy | Z3 | Solve constraints instead of brute forcing |
| Code is branch-obfuscated | Ghidra/IDA graph, Stadeo if applicable | Recover control flow |
| Code has MBA expressions | msynth | Simplify mixed Boolean arithmetic |
| VMProtect-like x64 virtualization | NoVmp, manual tracing | Specialized case |
| Need byte patching | ImHex, hexedit, PE-Bear, x64dbg patch | Precise edits |
| Need API-level emulation | Qiling | Hook calls without full native execution |
| Need coverage/instrumentation | QBDI, Pin, PANDA | Dynamic instrumentation |
| APK challenge | apk.sh, Apktool, ReverseAPK, jadx | Android-specific unpack/decompile |
| VBA macro challenge | Vba2Graph | Macro call graph |
| Office/PDF document challenge | oletools, Didier Stevens PDF tools, Origami | Extract macro/script/object content |
| JavaScript obfuscation | Synchrony | JS deobfuscation |

---

## Minimal Default Workflow

Use this when you are unsure.

1. Triage with `file`, `strings`, hash, and PE-Bear if PE.
2. Open in Ghidra or Cutter.
3. Search strings and imports.
4. Find success/failure branch.
5. Rebuild the validation in Python.
6. Use x64dbg/GDB only to confirm unknown runtime values.
7. Use Z3 when the validation is constraints rather than a simple transform.
8. Patch only after you understand the decision point.
