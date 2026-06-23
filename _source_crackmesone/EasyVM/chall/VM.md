[CorpCons's EasyVM](https://crackmes.one/crackme/69723bb7d735cd51e7a1aa78) - original link to crackmes

Author - [Profile](https://crackmes.one/user/CorpCons)

Language - C/C++

Arch - x86-64

Platform - Windows

Main function starts at 2290 - a bit cleared and renamed one.

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  HIDWORD(Block[0]) = 0;
  v35 = 0i64;
  v36 = 0;
  v37 = 0;
  *v78 = 0i64;
  v79 = 0i64;
  v80 = 0i64;
  memcpy_wrapper(v78, "%)44#%2GGGGG", 0xCui64);
  si128 = _mm_load_si128(&xmmword_14002F870);
  v5 = _mm_load_si128(&xmmword_14002F830);
  v6 = _mm_load_si128(&xmmword_14002F8B0);
  v7 = _mm_load_si128(&xmmword_14002F880);
  v8 = _mm_load_si128(&xmmword_14002F840);
  v9 = _mm_load_si128(&xmmword_14002F8A0);
  v10 = _mm_load_si128(&xmmword_14002F850);
  v11 = _mm_load_si128(&xmmword_14002F890);
  v12 = _mm_load_si128(&xmmword_14002F860);
  while ( 1 )
  {
    print_string(v3, "\nPlease Enter 10-char License Key: ");
    for ( i = 0i64; i != 10; ++i )
      read_input_char(v13, &v35 + i);
    v41[0] = 73;
    v41[1] = v35;
    v42 = 1090604848;
    v43 = 73;
    v44 = BYTE1(v35);
    v45[0] = 0x5341014941024F30i64;
    *&v45[1] = v12;
    v46 = v11;
    v47 = 73;
    v48 = BYTE2(v35);
    v49 = 1090604848;
    v50 = 73;
    v51 = BYTE3(v35);
    v52 = 1090670384;
    v53 = 1396769097;
    v54 = v10;
    v55 = v9;
    v56 = 73;
    v57 = BYTE4(v35);
    v58 = 1090604848;
    v59 = 73;
    v60 = BYTE5(v35);
    v61 = 1090670384;
    v62 = 1094779209;
    v63 = HIBYTE(v35);
    v64 = 810242864;
    v65 = 1094779475;
    strcpy(v66, "\nAO\nA0");
    *&v66[7] = si128;
    v66[23] = 73;
    v66[24] = BYTE6(v35);
    v67 = 1090604848;
    v68 = 73;
    v69 = HIBYTE(v35);
    v70 = 1090670384;
    v71 = 1396769097;
    v72 = v8;
    v73 = v7;
    v74 = v6;
    v75 = v5;
    v76 = si128;
    v15 = vm_interpreter(HIBYTE(v35), v41);
    v16 = v15 + 2;
    v17 = v15 == 0;
    if ( (v17 & (v15 == 0)) != 0 )
      break;
    v18 = print_string(v17, "This license key is corrupted.");
    sub_140002A70(v18);
  }
  v19 = string_constructor(v77, v78);
  v35 = v19;
  *&Block[1] = 0i64;
  v39 = 0i64;
  v40 = 0i64;
  memcpy_wrapper(&Block[1], byte_14002F760, 0i64);
  HIDWORD(Block[0]) = 1;
  v21 = 0;
  if ( v19[2] )
  {
    v22 = 51 * v16;
    v23 = Block[0];
    do
    {
      v24 = v19;
      if ( v19[3] > 0xFui64 )
        v24 = *v19;
      v25 = v22;
      LOBYTE(v25) = *(v24 + v21) ^ v22;
      v20 = v39;
      if ( v39 >= v40 )
      {
        sub_140003970(&Block[1], 1i64, v23, v25);
      }
      else
      {
        ++v39;
        v26 = &Block[1];
        if ( v40 > 0xF )
          v26 = Block[1];
        *(v26 + v20) = v25;
        *(v26 + v20 + 1) = 0;
      }
      ++v21;
    }
    while ( v21 < v19[2] );
  }
  v27 = v19[3];
  if ( v27 > 0xF )
  {
    v28 = *v19;
    if ( v27 + 1 < 0x1000 )
    {
      v29 = *v19;
    }
    else
    {
      v29 = *(v28 - 8);
      if ( (v28 - v29 - 8) > 0x1F )
        __fastfail(5u);
    }
    j_j_j__free_base(v29);
  }
  v19[2] = 0i64;
  v19[3] = 15i64;
  *v19 = 0;
  v30 = &Block[1];
  if ( v40 > 0xF )
    v30 = Block[1];
  v31 = string_destructor(v20, v30, v39);
  sub_140002A70(v31);
  if ( v40 > 0xF )
  {
    if ( v40 + 1 < 0x1000 )
    {
      v32 = Block[1];
    }
    else
    {
      v32 = *(Block[1] - 8i64);
      if ( (Block[1] - v32 - 8i64) > 0x1F )
        __fastfail(5u);
    }
    j_j_j__free_base(v32);
  } 
}
```

Initial Inspection
The function performs the following actions:

1. Outputs the prompt "Please Enter 10-char License Key: ".
2. Reads 10 input characters into the buffer in a loop.

![check_len.png](image1.png)

1. Forms a byte array on the stack (var_200) by mixing the entered characters with hard-coded constants (0x49, 0x4F, etc.).

![vm_init.png](Collect_data_for_vm.png)

1. Passes this array to the vm_interpreter function.
2. Depending on the result of this function (return value in AL), displays a success or
error message.

Analyzing the VM architecture

The vm_interpreter function is a simple stack/register machine interpreter.

![VM_GRAPH.png](vm_graph.png)

VM state:

Accumulator: Stored in the AL register (8 bits).

Registers: 16 byte array (emulated registers R0-R15) located in the stack (var_18).

![vm_registers.png](virt_registers.png)

Each instruction occupies 3 bytes:
[Opcode] [Operand] [Mode].

Instruction system (reconstructed from interpreter code):

0x49 (‘I’) -> LOAD: Load operand into Accumulator.

0x4F (‘O’) -> STORE: Save the Accumulator into the R[Operand] register.

0x41 (‘A’) -> ADD: Add operand to the Accumulator.

0x53 (‘S’) -> SUB: Subtract operand from the Accumulator.

0x58 (‘X’) -> XOR: XOR the accumulator with the operand.

Reconstructing the verification algorithm
The main function generates the "byte code" dynamically by inserting the characters of our key (In0...In9) as operands.
By analyzing the order in which bytes are written to the buffer before calling VM, we can break the program into 4 logical blocks. All
operations are performed on the accumulator, the result is accumulated in the register R10.

Notations: InN is the key symbol under the index N.

1. Block 1:
    
    LOAD In0 -> SUB ‘K’ (0x4B) -> STORE R10 (R10 = In0 - 0x4B)
    
    LOAD In1 -> SUB ‘E’ (0x45) -> ADD R10 -> STORE R10 (R10 += In1 - 0x45)
    
    Totals: R10 = In0 + In1 - 0x90
    
2. Block 2:
    
    LOAD In2 -> SUB ‘Y’ (0x59) -> ADD R10 -> STORE R10
    
    LOAD In3 -> SUB ‘-’ (0x2D) -> ADD R10 -> STORE R10
    
    Total: R10 += In2 + In3 - 0x86
    
3. Block 3:
    
    LOAD In4 -> ADD In7 -> SUB ‘K’ (0x4B) -> SUB In5 -> ADD R10 -> STORE R10
    
    Total: R10 += In4 + In7 - In5 - 0x4B
    
4. Block 4:
    
    LOAD In6 -> SUB In7 -> ADD R10
    
    Total: The accumulator contains the final sum.
    

Final equation:
VM returns the value of the accumulator. The check in main requires the result to be 0.

Let's collect all parts of the equation (all calculations modulo 256):
(In0 - 0x4B) + (In1 - 0x45) + (In2 - 0x59) + (In3 - 0x2D) + (In4 + In7 - In5 - 0x4B) + (In6 - In7) = 0

Note that In7 occurs with a plus and minus sign, so it is abbreviated. The symbols In8 and In9 are not
involved in the check.

Let's simplify the equation:
In0 + In1 + In2 + In3 + In4 - In5 + In6 - (0x4B + 0x45 + 0x59 + 0x2D + 0x4B) = 0
Sum of constants: 75 + 69 + 89 + 45 + 75 = 353.
353 mod 256 = 97 (0x61)

Total formula:
In0 + In1 + In2 + In3 + In4 - In5 + In6 = 97 (mod 256)

So based what we have found we can write keygen

→

```python
import random
import string

def generate_key():
    charset = string.ascii_letters + string.digits + string.punctuation
    while True:
        k = [random.choice(charset) for _ in range(6)]
        current_sum = sum(ord(c) for c in k[:5]) - ord(k[5])
        target_k6 = (353 - current_sum) % 256
        if 32 <= target_k6 <= 126:
            k6_char = chr(target_k6)
            k.append(k6_char)
            k.extend([random.choice(charset) for _ in range(3)])
            return "".join(k)

for i in range(5):
    print(f"Key {i + 1}: {generate_key()}")
```

![keys.png](keys.png)

![result.png](result.png)

You can also join my telegram channel - dimension59 there will be more reverse engineering content