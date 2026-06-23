# U_Can't_Pass
## Initial Analysis:
- Using gdb to disassemble main, we get the following disassembly:
    ```
    Dump of assembler code for function main:
       0x0000555555555150 <+0>:	endbr64 
       0x0000555555555154 <+4>:	push   rbp
       0x0000555555555155 <+5>:	mov    rbp,rsp
    => 0x0000555555555158 <+8>:	sub    rsp,0x10
       0x000055555555515c <+12>:	mov    DWORD PTR [rbp-0x4],0x0
       0x0000555555555163 <+19>:	lea    rdi,[rip+0xe9a]        # 0x555555556004
       0x000055555555516a <+26>:	mov    al,0x0
       0x000055555555516c <+28>:	call   0x555555555050
       0x0000555555555171 <+33>:	mov    DWORD PTR [rbp-0x8],0xa
       0x0000555555555178 <+40>:	cmp    DWORD PTR [rbp-0x8],0xa
       0x000055555555517c <+44>:	je     0x55555555518e <main+62>
       0x000055555555517e <+46>:	lea    rdi,[rip+0xeab]        # 0x555555556030
       0x0000555555555185 <+53>:	mov    al,0x0
       0x0000555555555187 <+55>:	call   0x555555555050
       0x000055555555518c <+60>:	jmp    0x5555555551a4 <main+84>
       0x000055555555518e <+62>:	cmp    DWORD PTR [rbp-0x8],0xa
       0x0000555555555192 <+66>:	jne    0x5555555551a2 <main+82>
       0x0000555555555194 <+68>:	lea    rdi,[rip+0xe9f]        # 0x55555555603a
       0x000055555555519b <+75>:	mov    al,0x0
       0x000055555555519d <+77>:	call   0x555555555050
       0x00005555555551a2 <+82>:	jmp    0x5555555551a4 <main+84>
       0x00005555555551a4 <+84>:	mov    eax,DWORD PTR [rbp-0x4]
       0x00005555555551a7 <+87>:	add    rsp,0x10
       0x00005555555551ab <+91>:	pop    rbp
       0x00005555555551ac <+92>:	ret    
    End of assembler dump.

    ```
- We can verify that the function being called at <+28>, <+55> and <+77> are printf calls by examining the instructions using `x/10i 0x555555555050` and seeing that it is a stub for printf.
- The arguments being passed to rdi before these calls are therefore the strings being printed by printf.
- Upon examining the strings using `x/s <address>` we find that the string present at 0x555555556030 is the Success string.
- We see that the je instruction at <+44> is skipping the printf call we want, so we have to patch that instruction. I used vim to patch it using xxd in command-line mode, but you can patch it in any way you want. I changed the je instruction to a jne instruction and after running the program, we get the Success message everytime.