# SirCrackaLot v2 Writeup

the main verification logic is in the function at image address 0xf4d0 (ghidra rebased 0x10f4d0)

the key parser in this function accepts four 4-hex groups split by dashes and maps them to 16 bit values
from the instruction flow and compare points, the groups end up in these roles:
first group in bp
second group in r13w
third group in r14w
fourth group in r12w

the important check region is around 0x10873 to 0x10f7d in the same function. there is anti debug noise generated before that, including a syscall plus rdtsc timing branch aat 0x107ed to 0x10837
constants 0xface and 0xdead are mixed into an internal value. (in a normal run this value is effectively 0)

- at 0x10ad4 and 0x10adb, ecx is computed as r13d * 0x7a69, then compared to the low 16 bits of local_160 stored at rsp+0x68
this gives the second seal relation:
  seal2 * 0x7a69 == local_160 mod 2^16
  inverse of 0x7a69 modulo 2^16 is 0xb5d9, so seal2 = local_160 * 0xb5d9 mod 2^16
- at 0x10f03, ax is compared with r14w. ( third check)
- at 0x10f1c, rcx is loaded with the table base at 0x5f60. then a crc--like chain of 16 bit table lookups and xor is executed, and at 0x10f79 si is compared with r12w. ( fourth seal check)

the table at 0x5f60 is present in rodata and is a 256 entry uint16 table.

there is also a check gate at 0x10e15 that depends on two earlier booleans tied to anti debug affected state and name derived state
for extraction while debugging, i forced normal run semantics for the anti debug influenced value and bypassed only this gate to read internal expected values.

---

Enter thy name, Aspirant: djd
Present thy sacred key: EA49-AD2D-7AB3-8828
Hail, worthy Knight! The Order welcomes thee!
