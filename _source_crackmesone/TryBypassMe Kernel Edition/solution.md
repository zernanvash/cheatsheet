# TryBypassMe Kernel Edition Writeup

Challenge_URL: https://crackmes.one/crackme/69db34d6b38f9259eec7eb32

The game consists of three primary components: the game executable (TBM.exe), a watchdog, and a kernel-mode driver (TBMKD.sys).

The game implements many security mechanisms, including debugger checks, blacklisted process/window scanning, section hashing, IAT integrity checks, encrypted variables, handle stripping (driver-side), and remote thread blocking (driver-side).

To achieve the objective, the most efficient approach is as follows:
1. Disable handle stripping in the TBMKD.sys driver to allow the cheat to attach to the TBM.exe process and 2. modify HP and AMMO variables in VRAM. This requires utilizing the proprietary data format discovered during memory analysis to ensure the cheat.py script writes valid data structures.

=====================================
1. Disabling Handle Stripping in TBMKD.sys (Memory addresses are valid for the driver base address FFFFF8013B010000)

Handle stripping is performed within the callback function Sub_FFFFF8013B013070, registered via ObRegisterCallbacks. This function is triggered whenever a process attempts to obtain a handle to TBM.exe, subsequently stripping the following access rights:
PROCESS_SUSPEND_RESUME (0x0800)
PROCESS_DUP_HANDLE (0x0040)
PROCESS_VM_WRITE (0x0020)
PROCESS_VM_READ (0x0010)
PROCESS_VM_OPERATION (0x0008)
PROCESS_CREATE_THREAD (0x0002)
In certain scenarios, the requesting process is terminated. 

To disable this, the driver has been patched: the jz loc_FFFFF8013B01317C instruction was replaced with an unconditional jmp, effectively bypassing the access rights validation. This patch also resolves crashes reported by @0xGroot and @crackthiscrackthat. I suspect that in their specific system, the program was crashing because other applications (like antivirus or scanners) were trying to grab the handle. Now that this functionality is turned off, it won't terminate the program anymore.

Additionally, for easier driver debugging, the driver's self-integrity check was disabled by replacing the call Sub_FFFFF8013B0132BC at 0xFFFFF8013B013708 with NOP instructions. This function previously performed periodic checksum validation of the loaded driver sections.

===================================
2. Modifying HP and AMMO Values in TBM.exe RAM
(Memory addresses are valid for the base address 00007FF669B80000)

Code analysis revealed that the HP and AMMO values ​​are not stored in RAM as regular numbers. Instead, their values ​​are first encrypted by XORing with the variables at pointers 0x7FF669BF0888 and 0x7FF669BF07C0. Additionally, the buffer is filled with the CRC chain values ​​(FNV1) from these variables. The final block for storing the HP or AMMO value occupies 0x78 bytes each. The game periodically checks the validity of all these values. If they are invalid, the game displays a message and terminates. To generate a valid block containing the HP or AMMO value, the cherat.py script contains the function make_protected_value_buff(value, Qword_1_7FF669BF0888, Qword_2_7FF669BF07C0). You can examine this script contents in more detail to figure out the data storage format.

Additionally, the Qword_7FF669BF07F0_diff_HP_2_value_addr, Qword_7FF669BF0AC0_diff_AMMO_value_addr, Qword_7FF669BF0880_diff2_AMMO_value_addr, Qword_7FF669BF0988_diff3_AMMO_value_addr, 0x7FF669BF0B74, and 0x7FF669BF0FA4 pointers store XOR encrypted values ​​of the offsets from the initial values.
If any deviations occur in these values, the game terminates.

The cheat.py script has been developed to attach to the TBM.exe process and replace the HP and AMMO values ​​in its RAM.

======================================
Cheat Usage Guide:
1. Replace the original TBMKD.sys driver with the patched version provided in the Writeup.
2. Disable Driver Signature Enforcement (the patched driver is unsigned lol).
3. Run python cheat.py from an Administrator command prompt.
4. Requirements: Python 3 x64 and the psutil package (pip install psutil).

Launch TBM.exe as Administrator.

The script will attach to the TBM.exe process and reset the HP and AMMO values every 0.1 seconds using the analyzed data structures.