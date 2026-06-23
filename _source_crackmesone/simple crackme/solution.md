# Simple Crackme by [marco007](https://crackmes.one/user/marco007) - [\[url\]](https://crackmes.one/crackme/698a6214fb46458f1ef6cef5)

Challenge_URL: https://crackmes.one/crackme/69b33ffcddd6176826ae8975

Difficulty: 1.5

Language: C/C++

Platform: Unix/linux

Arch: x86-64

---

Description:

Password validation with basic obfuscation

---

Files:

- [crackme](./files/crackme)

---

### Running the Executable

Trying to execute the program on x86-64 Linux machine, we see the following:

```sh
> ./crackme
./crackme: CPU ISA level is lower than required
```

This indicates ISA incompatibility, let's confirm the executable architecture:

```sh
> file crackme

crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a257f02aa427d3ad6559eef6d547657a5953f898, for GNU/Linux 6.1.0, not stripped
```

```sh
> lscpu

Architecture:                x86_64
  CPU op-mode(s):            32-bit, 64-bit
  Address sizes:             46 bits physical, 48 bits virtual
  Byte Order:                Little Endian
```

The architecture seems to match, so let's check ELF metadata of the executable:

```sh
> readelf -n crackme

Displaying notes found in: .note.gnu.property
  Owner                Data size    Description
  GNU                  0x00000030   NT_GNU_PROPERTY_TYPE_0
      Properties: x86 ISA needed: x86-64-baseline, x86-64-v2, x86-64-v3, x86-64-v4
    x86 feature used: x86
    x86 ISA used: x86-64-baseline
```

These notes suggest the program needs x86-64-v4 to run (AVX-512 - 512-bit SIMD
instructions for x86 ISAs). From `lscpu` flags we know that our CPU only
supports v3, hence the problem. However, `x86 ISA used: x86-64-baseline`
indicates that we don't actually need these extensions to execute the binary,
hence we can patch this issue by simply removing the ELF metadata header:

```sh
> cp crackme crackme.patched
> objcopy --remove-section .note.gnu.property crackme.patched
```

This removes the problematic ELF metadata section - `note.gnu.property`.

---

### Program Analysis

`Note: IDA Pro was used to deassemble the program`

The first relevant section of the program is the main function entry:

```asm
public main
main proc near

var_1D= byte ptr -1Dh
var_1C= dword ptr -1Ch
var_18= dword ptr -18h
s1= byte ptr -14h
var_8= qword ptr -8

; __unwind {
push    rbp
mov     rbp, rsp
sub     rsp, 20h
mov     rax, fs:28h
mov     [rbp+var_8], rax
xor     eax, eax
mov     [rbp+var_1C], 0
jmp     short loc_11E7
```

This is clearly the function prologue (stack setup):

```asm
push    rbp
mov     rbp, rsp
```

This looks like a typical stack canary (corruption protection):

```asm

mov     rax, fs:28h
mov     [rbp+var_8], rax

xor     eax, eax ; clear eax register, idk why
```

The following looks like a typical loop setup:

```asm
mov     [rbp+var_1C], 0
jmp     short loc_11E7
```

We set the stack variable at `stack base - 28` to zero and then perform an
unconditional jump to the next section of the program - the loop condition:

```asm
loc_11E7:
mov     eax, [rbp+var_1C]
cmp     eax, 0Ah
jbe     short loc_11B9
```

`rbp+var_1C` variable appears to act as a loop counter here, so I will refer to
it as `i` from here on.

So the loop condition compares the variable `i` (loop counter) with 0x0A (10
decimal). We can assume that means that the loop will run 11 times (loop
condition is `i <= 10`).

`jbe` is `jump below or equal` instruction, so the jump occurs whenever `i`
variable is less than or equal to 10. So the `loc_11B9` address is most likely
the loop body, and hence I will refer to it as such from now on:

```asm
loop_body:
mov     eax, [rbp+i]
cdqe
lea     rdx, enc_msg    ; "'(\",-6:'(\","
movzx   edx, byte ptr [rax+rdx]
movzx   eax, cs:key
mov     ecx, edx
xor     ecx, eax
mov     eax, [rbp+i]
cdqe
lea     rdx, enc_msg    ; "'(\",-6:'(\","
mov     [rax+rdx], cl
add     [rbp+i], 1
```

These lines simply load the `i` into eax register and extend it to rax (64-bit):

```asm
mov     eax, [rbp+i]
cdqe
```

Then the `enc_msg` (pretty self explanatory) address is loaded into the rdx
register:

```asm
lea     rdx, enc_msg    ; "'(\",-6:'(\","
```

Then what appears to be a decryption process begins:

```asm
movzx   edx, byte ptr [rax+rdx]
```

copies a byte from the `enc_msg + i` address to the edx register.

Some `key` value (0x69 or 105 decimal) is then loaded to eax:

```asm
movzx   eax, cs:key
```

The values are then XORed together:

```asm
mov     ecx, edx
xor     ecx, eax
```

The resulting value is then moved back to its location (indexed by the `i`
variable):

```asm
mov     eax, [rbp+i]
cdqe
lea     rdx, enc_msg    ; "'(\",-6:'(\","
mov     [rax+rdx], cl
```

Finally, we increment the `i` variable at the end of the loop:

```asm
add     [rbp+i], 1
```

So essentially this loop performs a bitwise XOR on some encrypted string. This
is likely the password that we are looking for.

The next section of code is pretty straight-forward - its the start of the
password-checking loop:

```asm
mov     eax, cs:multiplier
mov     edx, eax
mov     eax, cs:offset
xor     eax, edx
mov     [rbp+var_1D], al
lea     rax, s          ; "You must enter a password to access thi"...
mov     rdi, rax        ; s
call    _puts
lea     rax, [rbp+s1]
lea     rdx, aS         ; "%s"
mov     rsi, rax
mov     rdi, rdx
mov     eax, 0
call    ___isoc23_scanf
jmp     short loc_125D
```

The following section appears to XOR two constants - `multiplier` (0xBB or 187
decimal) and `offset` (3), storing the result (0xB8 or 184 decimal) into the
`var_1D` variable on stack:

```asm
mov     eax, cs:multiplier
mov     edx, eax
mov     eax, cs:offset
xor     eax, edx
mov     [rbp+var_1D], al
```

This is likely some sort of key to be used later in the program.

Then the user input request string is printed using `_puts` function (first
argument in x86-64 UNIX is typically supplied in RDI register):

```asm
lea     rax, s          ; "You must enter a password to access thi"...
mov     rdi, rax        ; s
call    _puts
```

Then the program requests the user input and writes it to the `s1` variable:

```asm
lea     rax, [rbp+s1]
lea     rdx, aS         ; "%s"
mov     rsi, rax
mov     rdi, rdx
mov     eax, 0
call    ___isoc23_scanf
```

Here the first argument is the format string - `"%s"`, supplied in the RDI
register and second argument is the string address - `s1` variable, supplied in
the RSI register. EAX register indicates the number of XMM registers used
(floating point registers).

The program then jumps to what appears to be an if statement - the
password-checking logic:

```asm
loc_125D:
lea     rdx, enc_msg    ; "'(\",-6:'(\","
lea     rax, [rbp+s1]
mov     rsi, rdx        ; s2
mov     rdi, rax        ; s1
call    _strcmp
test    eax, eax
jnz     short loc_122E
```

The `strcmp` function takes two arguments - first string in RDI register and
second string in the RSI register:

```asm
lea     rdx, enc_msg    ; "'(\",-6:'(\","
lea     rax, [rbp+s1]
mov     rsi, rdx        ; s2
mov     rdi, rax        ; s1
call    _strcmp
```

So these instructions compare the user-input (`s1`variable on the stack) with
the string decoded earlier (stored in the enc_msg variable). The function
returns zero in the EAX register, if the strings are equal.

Then if the EAX is not zero (strings are not equal), the program prints error
message, requests new password and then loops back to the if statement:

```asm
loc_122E:
lea     rax, format     ; "wrong password, try again.\n> "
mov     rdi, rax        ; format
mov     eax, 0
call    _printf         ; print the error message
lea     rax, [rbp+s1]
lea     rdx, aS         ; "%s"
mov     rsi, rax
mov     rdi, rdx
mov     eax, 0
call    ___isoc23_scanf ; request a new password from the user
```

Once the password matches with the earlier decrypted one, we encounter another
loop setup:

```asm
mov     [rbp+var_18], 0
jmp     short loc_12B2

loc_12B2:
mov     eax, [rbp+var_18]
cmp     eax, 16h
jbe     short loc_1280
```

This time the variable `var_18` acts as the loop counter, hence I will refer to
it as `j` from now on. The loop condition appears to be `while EAX <= 0x16`
(22 decimal), hence the loop executes 23 times total.

Inside the loop, the program does the following:

```asm
loc_1280:
mov     eax, [rbp+j]
cdqe
lea     rdx, flag
movzx   eax, byte ptr [rax+rdx]
mov     edx, [rbp+j]
mov     ecx, edx
movzx   edx, [rbp+var_1D]
add     edx, ecx
xor     eax, edx
mov     ecx, eax
mov     eax, [rbp+j]
cdqe
lea     rdx, flag
mov     [rax+rdx], cl
add     [rbp+j], 1
```

This appears to be very similar to the password decryption code. The `flag`
variable is being loaded into the EAX register, the loop counter into the ECX
register and the `var_1D` variable (184 decimal, calculated earlier) into the
EDX register:

```asm
mov     eax, [rbp+j]
cdqe
lea     rdx, flag
movzx   eax, byte ptr [rax+rdx]
mov     edx, [rbp+j]
mov     ecx, edx
movzx   edx, [rbp+var_1D]
```

Then the sum of the loop counter and the 184 decimal in EDX is XORed against the
byte of the `flag` string:

```asm
add     edx, ecx
xor     eax, edx
```

The modified byte is then written back to the `flag` string:

```asm
mov     ecx, eax
mov     eax, [rbp+j]
cdqe
lea     rdx, flag
mov     [rax+rdx], cl
```

, and the loop counter incremented:

```asm
add     [rbp+j], 1
```

So essentially this loop performs a bitwise XOR between the string `flag` and
(j + 184).

Upon decoding the flag, the program prints it:

```asm
lea     rax, flag
mov     rdi, rax        ; s
call    _puts
```

Finally, the program ends with the `main` function epilogue:

```asm
mov     eax, 0
mov     rdx, [rbp+var_8]  ; load stack canary
sub     rdx, fs:28h       ; verify stack canary
jz      short locret_12E2 ; if successful, end program peacefully

call    ___stack_chk_fail ; if canary fails, throw stack error

locret_12E2:
leave                     ; destroy stack frame and return
retn
main endp
```

---

### Program Summary

The program stores two encrypted strings - the password and the flag. It
decrypts the password using bitwise XOR operation against a constant key - 105
decimal and then compares the decrypted password to the user input. If the user
entered correct password, the program decrypts the flag by performing bitwise
XOR of the flag string with loop counter (byte number, starting at zero) + 184.
The decrypted flag is then printed to the user.

---

### Patch

The simplest way to get the flag is to simply bypass the password check by
modifying the binary.

First let's bypass the user input, so the program executes without requesting
password in the first place. We could do that by replacing the segment with
`puts` and `scanf` function calls with the unconditional jump to the if
statement (password checker):

```asm
jmp     short loc_125D
```

So this code:

```asm
mov     eax, cs:multiplier
mov     edx, eax
mov     eax, cs:offset
xor     eax, edx
mov     [rbp+var_1D], al
lea     rax, s          ; "You must enter a password to access thi"...
mov     rdi, rax        ; s
call    _puts
lea     rax, [rbp+s1]
lea     rdx, aS         ; "%s"
mov     rsi, rax
mov     rdi, rdx
mov     eax, 0
call    ___isoc23_scanf
jmp     short loc_125D
```

now turns into the following:

```asm
mov     eax, cs:multiplier
mov     edx, eax
mov     eax, cs:offset
xor     eax, edx
mov     [rbp+var_1D], al
jmp     short loc_125D
```

However, the program still doesn't give us the flag, since the password checker
obviously fails. We could bypass this by changing the verification logic:

```asm
lea     rdx, enc_msg    ; "'(\",-6:'(\","
lea     rax, [rbp+s1]
mov     rsi, rdx        ; s2
mov     rdi, rax        ; s1
call    _strcmp
test    eax, eax
jnz     short loc_122E
```

To bypass the check, we could simply change the conditional jump at the end:

```asm
jnz     short loc_122E
```

to some useless instruction that does nothing:

```asm
xor eax, eax
```

So we get:

```asm
lea     rax, [rbp+s1]
mov     rsi, rdx        ; s2
mov     rdi, rax        ; s1
call    _strcmp
test    eax, eax
xor eax, eax
```

Now when we execute the resulting binary:

```sh

> ./crackme_patch.patched

FLAG{CIPHER_ENCRYPTION}

```

And there is our flag!

We could also use GDB to find the actual password, since it is stored in memory
unencrypted at some point:

```
(gdb) file crackme.patched
Reading symbols from crackme.patched...
(No debugging symbols found in crackme.patched)

(gdb) start
Temporary breakpoint 1 at 0x119d
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib64/libthread_db.so.1".

Temporary breakpoint 1, 0x000055555555519d in main ()
```

Now that the program is in memory, we could see the section addresses. We are
specifically interested in where the `data` segment starts:

```
(gdb) info files

Entry point: 0x555555555080
[...]
0x0000555555558030 - 0x0000555555558078 is .data
```

Now let's find and set the breakpoint at some point after the password is
decrypted:

```
(gdb) disassemble main

   0x00005555555551e7 <+78>:    mov    -0x1c(%rbp),%eax
   0x00005555555551ea <+81>:    cmp    $0xa,%eax
   0x00005555555551ed <+84>:    jbe    0x5555555551b9 <main+32>
   0x00005555555551ef <+86>:    mov    0x2e4b(%rip),%eax        # 0x555555558040 <multiplier>
```

Here, directly after the loop at `0x00005555555551ed`, is the perfect place.
Hence our breakpoint will be at `*0x00005555555551ef`:

```
(gdb) break *0x00005555555551ef
Breakpoint 2 at 0x5555555551ef

(gdb) run
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib64/libthread_db.so.1".

Breakpoint 2, 0x00005555555551ef in main ()
```

At this point in execution, the password should already be stored unencrypted in
the data segment, so let's see what data segment actually looks like:

```
(gdb) x/50bx 0x0000555555558030
0x555555558030: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x555555558038: 0x38    0x80    0x55    0x55    0x55    0x55    0x00    0x00
0x555555558040 <multiplier>:    0xbb    0x00    0x00    0x00    0x03    0x00    0x00    0x00
0x555555558048 <enc_msg>:   0x4e    0x41    0x4b    0x45    0x44    0x5f    0x53    0x4e
0x555555558050 <enc_msg+8>: 0x41    0x4b    0x45    0x00    0x69    0x00    0x00    0x00
0x555555558058: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x555555558060 <flag>:  0xfe    0xf5
```

The `<enc_msg>` at `0x555555558048` is exactly what we are looking for - the
password string. It is also null-terminated, so we can read it as a string:

```
(gdb) x/s 0x555555558048
0x555555558048 <enc_msg>:   "NAKED_SNAKE"
```

And there is our password!

```sh
> ./crackme.patched
You must enter a password to access this program!
NAKED_SNAKE
FLAG{CIPHER_ENCRYPTION}
```

---

### Keygen

Now that we know how the program and the decryption algorithm work, we can
write a simple decryption script to get both the password and the flag:

```c
#include <stdio.h>

int main() {
    char pass[11] = "'(\",-6:'(\",";

    char key = 105;

    for (int i = 0; i < 11; i++) {
        pass[i] = pass[i] ^ key;
    }

    printf("Password: %s\n", pass);

    return 0;
}
```

And like expected, the password matches:

```sh
> gcc keygen.c -o keygen

> ./keygen
Password: NAKED_SNAKE
```

Since the actual flag is also just an encrypted string, we could decrypt the
flag in our keygen as well:

```c
#include <stdio.h>

int main() {
    char pass[11] = "'(\",-6:'(\",";

    char key = 105;

    for (int i = 0; i < 11; i++) {
        pass[i] = pass[i] ^ key;
    }

    printf("Password: %s\n", pass);

    char flag[23] = {0xFE, 0xF5, 0xFB, 0xFC, 0xC7, 0xFE, 0xF7, 0xEF, 0x88, 0x84, 0x90, 0x9C, 0x81, 0x8B, 0x85, 0x95, 0x91, 0x99, 0x9E, 0x82, 0x83, 0x83, 0xB3};

    for (int i = 0; i < 23; i++) {
        flag[i] = flag[i] ^ (i + 184);
    }

    printf("Flag: %s\n", flag);

    return 0;
}
```

```
> gcc keygen.c -o keygen

> ./keygen
Password: NAKED_SNAKE
Flag: FLAG{CIPHER_ENCRYPTION}
```

And there we go, the flag.

---

[Back to home](./../crackmes.md)
