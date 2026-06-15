# x64dbg Cheat Sheet

A comprehensive, production-grade x64dbg reference tailored for reverse engineers, malware analysts, and CTF players performing user-mode dynamic analysis on Windows PE binaries.

---

## 1. Essential UI & Execution Controls
These are the core keys you will use to run, step, and navigate through binaries interactively.

| Shortcut | Action | Strategic Use Case |
|---|---|---|
| **F9** | Run (Resume) | Resume execution of the program until a breakpoint is hit or it exits. |
| **F8** | Step Over | Execute the current instruction; if it is a call, execute the entire subroutine and stop at the next instruction. |
| **F7** | Step Into | Execute the current instruction; if it is a call, jump to the first instruction of the subroutine. |
| **Ctrl + F9** | Execute till Return | Run until the current subroutine reaches its `RET` instruction (useful for stepping out of a function). |
| **Alt + F9** | Execute till User Code | Run until execution returns to the main module (extremely useful when lost in system DLL code). |
| **F2** | Toggle Software Breakpoint | Set a breakpoint at the current instruction line. |
| **Ctrl + G** | Jump to Expression / Address | Navigate disassembly or dump view to a specific address, API (e.g., `VirtualAlloc`), or register. |
| **Spacebar** | Assemble | Modify the instruction at the current cursor line by typing assembly on the fly. |
| **Asterisk (\*)** | Center on EIP / RIP | Instantly focus the CPU disassembly view back onto the current instruction pointer. |
| **Minus (-)** | Go Back | Navigate backward in your viewing history. |
| **Plus (+)** | Go Forward | Navigate forward in your viewing history. |

---

## 2. Memory & Dump Inspection
Analyzing data layouts, stack buffers, and dynamically allocated memory blocks.

* **Right-click $\rightarrow$ Follow in Dump**:
  * Select an address in the Disassembler or a register value, right-click, and select **Follow in Dump** to load that memory area in the Hex Dump pane.
* **Right-click $\rightarrow$ Follow in Stack**:
  * View local variables, function arguments, or saved return addresses.
* **Hex Dump Format Options**:
  * Right-click inside the Hex Dump panel to toggle presentation mode between **Hex**, **ASCII**, **Integer**, **Float**, **Structure**, or **Disassembly**.
* **Memory Map Tab**:
  * View all allocated memory blocks, their base addresses, sizes, protections (ERW), and allocation types. Useful for finding decrypted malware payloads in memory.

---

## 3. Tracking Data & Control Flow
Locating code targets, finding hardcoded resources, and mapping functions.

### Finding References & Searches
* **Search for String References**:
  * Right-click in the CPU Disassembly view $\rightarrow$ **Search for** $\rightarrow$ **All Modules** (or **Current Module**) $\rightarrow$ **String references**. Essential for locating flag strings, validation prompts, or system APIs.
* **Search for Intermodular Calls**:
  * Right-click $\rightarrow$ **Search for** $\rightarrow$ **All Modules** (or **Current Module**) $\rightarrow$ **Intermodular calls**. Lists all external APIs called by the binary (e.g., `RegOpenKeyExA`, `CreateFileW`).
* **Find References to Command/Address**:
  * Right-click an instruction $\rightarrow$ **Find References to** $\rightarrow$ **Selected Command** (or **Address**). Lists all locations in the binary referencing that instruction or location.

---

## 4. Modifying & Patching (Runtime & Binary Disk Patches)
Bypassing license checks, patching anti-debug conditions, or forcing program branches.

### Patching Instructions & Bytes
1. **Spacebar**: Select the instruction (e.g., `JZ 0x00402010`) and press Spacebar. Type the new instruction (e.g., `JMP 0x00402010` or `NOP` to remove the check) and click **OK**.
2. **Binary Edit**: In the Hex Dump pane, select bytes, right-click $\rightarrow$ **Binary** $\rightarrow$ **Edit** (or press **Ctrl + E**). Enter the new hex bytes directly.
3. **Fill with NOPs**: In the disassembly view, select a range of lines, right-click $\rightarrow$ **Binary** $\rightarrow$ **Fill with NOPs** to erase multiple checks at once.

### Exporting Patches to Disk
1. Press **Ctrl + P** (or click the Patch icon on the toolbar) to open the **Patches** window.
2. Verify the list of modified addresses.
3. Click **Patch File** to save the modified database changes into a new standalone executable file on disk.

### Modifying Register & Flag Values
* Double-click any value in the Registers pane (right side) to modify its value (e.g., changing `EAX` from `0` to `1` to fake a validation success).
* Double-click flag bits (e.g., changing `ZF` from `0` to `1` to force a jump on a conditional branch without modifying the code).

---

## 5. Advanced Breakpoints & Malware Unpacking

### Breakpoint Types
* **Software Breakpoints (F2)**: Replaces target byte with a `0xCC` (INT 3) instruction. Best for general code logic.
* **Hardware Breakpoints**: Right-click an address $\rightarrow$ **Breakpoint** $\rightarrow$ **Hardware, Access / Write / Execute**. Uses CPU debug registers (DR0-DR3). Does not alter binary bytes. Perfect for spotting when a decrypted payload is written to memory, or hitting code when software breakpoints are blocked.
* **Conditional Breakpoints**: Right-click an address $\rightarrow$ **Breakpoint** $\rightarrow$ **Conditional Breakpoint**. Enter an expression (e.g., `EAX == 0x1337` or `[ESP+4] == 0x0`).

### 💡 Unpacking Malware with Scylla
Most packed malware decrypts its original code into memory and jumps to it.
1. Run the malware in x64dbg until it reaches the **Original Entry Point (OEP)** (often spotted by a tail jump: `JMP EAX` or `PUSH / RET` to a newly allocated memory block).
2. Go to **Plugins $\rightarrow$ Scylla** to open the Scylla import reconstruction tool.
3. Click **IAT Autosearch** to automatically locate the Import Address Table in memory.
4. Click **Get Imports** to resolve the API function names.
5. Click **Dump** to save the unpacked process memory as a raw PE file.
6. Click **Fix Dump** and select the dumped PE file to write the reconstructed IAT back into the file headers. This makes the dumped binary runnable!

### 💡 Hiding from Anti-Debugging
Many malware files call `IsDebuggerPresent`, `NtQueryInformationProcess`, or read the PEB directly.
* Use the **ScyllaHide** plugin (`Plugins -> ScyllaHide`).
* Configure it to hook and spoof debugger signals.
* Alternatively, command line commands: `bp IsDebuggerPresent` $\rightarrow$ run until hit $\rightarrow$ set `EAX = 0` $\rightarrow$ continue.

---

## Related Links
* [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
* [IDA Pro Cheat Sheet](IDA%20Pro%20Cheat%20Sheet.md)
* [Ghidra Cheat Sheet](Ghidra%20Cheat%20Sheet.md)
* [GDB Cheat Sheet](GDB%20Cheat%20Sheet.md)
