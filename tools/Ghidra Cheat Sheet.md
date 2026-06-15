# Ghidra Cheat Sheet

A comprehensive, production-grade Ghidra reference tailored for reverse engineers, malware analysts, and CTF players. Organized by workflow to help you find your bearings, navigate complex binaries, and unmask obscured logic efficiently.

---

## 1. Essential UI & Navigation Controls
These are the core keys you will use to navigate through basic blocks, graphs, and linear disassembly.

| Shortcut | Action | Strategic Use Case |
|---|---|---|
| **G** | Goto / Jump to Address | Teleport directly to a hex address (e.g., `0x00401040`), function name, or symbol. |
| **Alt + Left Arrow** | Navigation Back | Move backward to your previous location (untrace a jump). |
| **Alt + Right Arrow** | Navigation Forward | Redo a forward navigation step. |
| **F** | Find Text | Search for a specific string inside the current program listing. |
| **Ctrl + Shift + E** | Search Memory | Scan the binary for specific byte patterns, hex values, or text globally. |
| **F3** | Edit Function Signature | Opens the signature editor to modify return type, parameters, and calling convention. |
| **Spacebar / Graph Icon**| Graph View Toggle | Ghidra uses the "Function Graph" window. Toggle it via `Window -> Function Graph`. |
| **Double Click** | Follow target | Double-click any address, label, or call target to jump to it. |

---

## 2. Tracking Data & Control Flow
Finding where data lives and how functions link together is the core of static analysis.

### Cross-References (XREFs)
* **Ctrl + Shift + F (on a symbol or variable)**: Opens the **References to...** window. Use this to find all occurrences of code or data that read, write, or call your selection.
* **Right-click $\rightarrow$ References $\rightarrow$ Show References to**: Alternate way to trigger the XREF window.

### Sub-view Windows
Access these through the top menu `Window` if closed.

| Window | Path | Strategic Use Case |
|---|---|---|
| **Defined Strings** | `Window -> Defined Strings` | Searchable table of all ASCII/Unicode strings discovered in the binary. |
| **Functions** | `Window -> Functions` | View and filter all discovered functions/subroutines in the program database. |
| **Symbol Tree** | `Window -> Symbol Tree` | Expandable view of Imports (DLL APIs), Exports, Labels, and Functions. |
| **Data Type Manager** | `Window -> Data Type Manager` | List and search all loaded data types, structures, and headers. |
| **Decompiler** | `Window -> Decompiler` | Real-time C-like pseudo-code representation of the currently selected disassembly block. |

---

## 3. Modifying & Refactoring Code (Cleaning the Workspace)
Compilers shuffle names and properties. Your job is to rename and type variables until the code reads like original source code.

* **L (Rename)**: Rename any variable, parameter, local label, or function name globally.
* **T (Set Type)**: Modify the data type of a variable or signature parameter (e.g., changing type to `char *`, `int`, or a custom struct).
* **; (Semicolon)**: Add a comment. Opens the comments box with tabs for:
  * *EOL*: End of line comment.
  * *Pre / Post*: Appended before or after the instruction.
  * *Plate*: Top of block header comment.
  * *Repeatable*: Comment that propagates to cross-referenced lines.
* **C (Clear)**: Undefine the current area, turning assembly code or data back into raw bytes (equivalent to **U** in IDA).
* **D (Disassemble)**: Force interpretation of raw bytes at the current address as executable assembly instructions (equivalent to **C** in IDA).
* **Data Type Shortcuts**:
  * **b**: Define as a `Byte`.
  * **w**: Define as a `Word`.
  * **d**: Define as a `Double Word` (DWord).
  * **q**: Define as a `Quad Word` (QWord).
  * **Shift + D**: Opens a search dialog to pick any other data type.

> [!NOTE]
> **IDA vs. Ghidra Shortcut differences:**
> * Undefining code: IDA uses **U**, Ghidra uses **C** (Clear).
> * Disassembling code: IDA uses **C** (Code), Ghidra uses **D** (Disassemble).
> * Retyping variable: IDA uses **Y** (Set Type), Ghidra uses **T** (Type).

---

## 4. Advanced Data & Object Structures
When a binary handles objects, network packets, or scattered text arrays, you need to tell Ghidra how the data layouts are configured.

### Defining Structures
1. Open the **Data Type Manager** (`Window -> Data Type Manager`).
2. Right-click your project archive folder (or `ghidra` root folder) and select **New $\rightarrow$ Structure**.
3. In the Structure Editor, press **+** to add fields, define their types (e.g., `char[16]`, `int`, `void*`), and name them.
4. Save the structure (Ctrl+S or click the floppy disk icon).

### Applying Structures to Disassembly/Decompiler
* **T (Type)**: Select a variable in either the assembly Listing or the Decompiler view, press **T**, and search for your custom structure template.
* Alternatively, right-click the variable in the Decompiler view and select **Retype Variable** to type your structure.

---

## 5. Pro-Tips for CTFs and Malware Analysis

### 💡 Tip 1: The Magic Transformation
Optimized compilers often convert string lookups into multi-byte integer assignments (like `*(undefined4 *)(param_1 + 0x10) = 0x616c6667;`). To clean this up:
1. Select the parameter or pointer in the Decompiler.
2. Press **T** (or right-click $\rightarrow$ **Retype Variable**).
3. Overwrite the type with `char *`.
4. The Decompiler will immediately clean up the register expressions and display readable array indexing (e.g., `param_1[16] = 'g';`).

### 💡 Tip 2: Node Color Coding
To visually map pathways in the visual block graph:
1. Open the **Function Graph** (`Window -> Function Graph`).
2. Right-click the header of a block node in the graph layout.
3. Select **Color Panel** and pick a color:
   * **Green** for successful verification blocks.
   * **Red** for error / bail-out / exit blocks.
   * **Yellow** for loops, decryption, or hashing routines.

### 💡 Tip 3: Patching Instructions
If you need to patch a branch condition or remove a debugger check:
1. Select the instruction line in the disassembly Listing.
2. Right-click and select **Patch Instruction** (or press **Ctrl + Shift + G** / **Ctrl + G** on some configurations).
3. Type the new instruction directly (e.g., changing `JZ LAB_00401030` to `JMP LAB_00401030` or typing `NOP`).
4. Press **Enter** to compile the instruction and overwrite the database bytes.
5. Save the modified binary via `File -> Export Program -> Format: Original File` to export the patched binary to disk.

### 💡 Tip 4: Ghidra scripting (Python)
Ghidra has a built-in Jython shell:
1. Open the **Script Manager** (`Window -> Script Manager`).
2. Click **New Script** (the green circle plus icon), name it, and select **Python**.
3. Use the Ghidra API to query and modify state. Useful commands:
   ```python
   # Print current cursor address
   print("Current Address: {}".format(currentAddress))
   
   # Patch a byte at current address
   setByte(currentAddress, 0x90)
   
   # Read a byte
   b = getByte(currentAddress)
   
   # Disassemble at address
   disassemble(currentAddress)
   ```

---

## Related Links
* [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
* [IDA Pro Cheat Sheet](IDA%20Pro%20Cheat%20Sheet.md)
* [x64dbg Cheat Sheet](x64dbg%20Cheat%20Sheet.md)
* [GDB Cheat Sheet](GDB%20Cheat%20Sheet.md)
