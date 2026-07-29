# IDA Pro Cheat Sheet

A comprehensive, production-grade IDA Pro reference tailored for reverse engineers, malware analysts, and CTF players. Organized by workflow to help you find your bearings, navigate complex binaries, and unmask obscured logic efficiently.

---

## 1. Essential UI & Navigation Controls
These are the core keys you will use to navigate through basic blocks, graphs, and linear disassembly.

| Shortcut | Action | Strategic Use Case |
|---|---|---|
| **Spacebar** | Toggle Graph $\leftrightarrow$ Text View | Switch between visual basic block flows and linear memory address listings. |
| **G** | Jump to Address / Symbol / Offset | Instantly teleport to a specific address (e.g., `0x00401040`) or named API. |
| **Esc** | Jump Backward | Acts like a web browser's "Back" button; untrace your steps after following a pointer. |
| **Ctrl + Enter** | Jump Forward | Redo a backward jump step. |
| **F5** | Decompile Function | Converts the active assembly routine into C-like pseudo-code (requires Hex-Rays). |
| **Double Click** | Follow Identifier | Follow jumps, variables, function targets, or memory references in disassembly. |
| **Alt + T** | Search Text | Find a string or pattern within the disassembly or decompiler output. |
| **Ctrl + T** | Search Next Text | Find the next occurrence of the text searched via Alt+T. |
| **Alt + B** | Search Bytes | Search for specific hex byte sequences in the binary (e.g., shellcode signatures). |

---

## 2. Tracking Data & Control Flow
Finding where data lives and how functions link together is the core of static analysis.

### Cross-References (XREFs)
* **X (on a variable/function)**: Opens the Cross-References window. Use this to find every function that reads from, writes to, or calls your selection.
* **Ctrl + X**: Opens cross-references to the current position.

### Sub-view Windows
Access these through the top menu `View -> Open Subviews` if closed.

| Shortcut | Window | Strategic Use Case |
|---|---|---|
| **Shift + F12** | Strings Window | Scans the binary for plain-text strings. Essential for finding hardcoded keys, flags, URLs, and registry paths. |
| **Ctrl + P** | Functions Window | Displays a searchable list of all discovered subroutines inside the database. |
| **Ctrl + I** | Imports Window | Lists external API functions imported from third-party DLLs (e.g., `IsDebuggerPresent`, `VirtualAlloc`). Very useful for identifying structural capabilities. |
| **Ctrl + E** | Exports Window | Lists functions exposed by this binary (mostly DLLs/shared objects) for external use. |
| **Shift + F4** | Names Window | Lists all auto-generated and user-defined symbols and labels in the database. |

---

## 3. Modifying & Refactoring Code (Cleaning the Workspace)
Compilers shuffle names and properties. Your job is to rename and type variables until the code reads like original source code.

* **N (Rename)**: Rename any generic label (e.g., changing `sub_401040` to `check_validation_key`). This updates globally across IDA.
* **Y (Set Type)**: Modify a function signature, variable type, or argument definition (e.g., changing `int *this` to `char *input_string`).
* **; (Semicolon)**: Add a repeatable comment. This comment will appear next to the instruction and everywhere else that memory address is referenced.
* **: (Colon)**: Add a non-repeatable comment that only appears at that specific address line.
* **U (Undefine)**: Strips away IDA’s analytical assumptions, converting code/data blocks back into raw byte listings.
* **C (Code)**: Forces IDA to interpret an undefined block of raw bytes explicitly as executable assembly instructions.
* **D (Data)**: Rotates raw byte definitions through data types: `byte` $\rightarrow$ `word` $\rightarrow$ `dword` $\rightarrow$ `qword`.
* **A (ASCII)**: Directs IDA to interpret the raw bytes at the current address as a null-terminated ASCII string.
* **H (Hexadecimal)**: Toggle the representation of an immediate operand between decimal and hex (e.g., change `65535` to `0xFFFF`).
* **_ (Underscore)**: Toggle the representation of an immediate operand to an enum or offset.

---

## 4. Advanced Data & Object Structures
When a binary handles objects, network packets, or scattered text arrays, you need to tell IDA how the data layouts are configured.

### Defining Structures (Shift + F9)
1. Press **Shift + F9** to open the Structures tab.
2. Press **Insert** to declare a brand-new custom template object (e.g., `struct CustomKey`).
3. Press **D** inside the structure block to add a field, then use **N** to label it.
4. Press **Y** on a structure field to explicitly define its type (e.g., `char[32]`).

### Applying Structures to Disassembly
* **T (Structure Offset)**: Select an operand variable matching an array pattern (like `[eax + 14h]`) and press **T**. Select your custom structure template to automatically turn the raw math offset into a readable structure field lookup (e.g., `input_key->fourth_chunk`).

---

## 5. Pro-Tips for CTFs and Malware Analysis

### 💡 Tip 1: The Magic Transformation
If you see an optimized array loop casting strings using multi-byte integers (`_DWORD`), click the function header, press **Y**, and explicitly overwrite the variable parameter to `char *`. The decompiler will instantly drop register middleware variables and output human-readable index offsets like `&input[16]`.

### 💡 Tip 2: Color Coding
Right-click the header of a visual block node in Graph View to give it a custom background color.
* Mark **Success Paths** in **Green**.
* Mark **Verification Failure Paths** in **Red**.
* Mark **Suspicious Cryptographic Looping Sequences** in **Yellow** to visually map out major binaries.

### 💡 Tip 3: Patching Bytes & Instructions
If you need to bypass a license check or an anti-debugger:
1. Go to the instruction you want to patch (e.g., change a `jz` to `jnz` or a `jnz` to `jmp`/`nop`).
2. Go to `Edit -> Patch program -> Assemble...` to rewrite assembly instruction directly.
3. Or go to `Edit -> Patch program -> Change byte...` to patch raw bytes (e.g., `90 90` for NOPs).
4. Apply the patches to the actual binary file on disk via `Edit -> Patch program -> Apply patches to input file...`.

### 💡 Tip 4: Quick IDAPython Scripting
Access the Python command line at the bottom of the screen. Useful commands:
* `print(hex(idc.get_screen_ea()))` - Print the current selected address.
* `idc.patch_byte(0x401050, 0x90)` - Patch a byte via script.
* `print(idc.generate_disasm_line(idc.get_screen_ea(), 0))` - Print current assembly line.
* Iterate instructions:
  ```python
  import idautils
  import idc
  for addr in idautils.Heads(idc.get_screen_ea(), idc.get_func_attr(idc.get_screen_ea(), idc.FUNCATTR_END)):
      print(f"{hex(addr)}: {idc.generate_disasm_line(addr, 0)}")
  ```

---

## Related Links
* [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
* [Ghidra Cheat Sheet](Ghidra%20Cheat%20Sheet.md)
* [x64dbg Cheat Sheet](x64dbg%20Cheat%20Sheet.md)
* [GDB Cheat Sheet](GDB%20Cheat%20Sheet.md)
