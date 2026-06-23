Challenge_URL: https://crackmes.one/crackme/69ff482c8fab7bbca273011e

gurneyburner52 back at it AGAIN with another banger today we will be attempting the fresh `ASMe | ASM CrackMe`
i thoroughly enjoyed this challenge despite having **NO** snacks and it took about 23 minutes to solve, i still think its a relatively tough challenge
and it helps that i have some decent compute ^.^ oh well here we go:

## quick answer

valid serial:

```text
pXi8
```

## summary

this crackme is a small Win32 GUI program in ASM as written in description/title. the binary has no normal import table and it resolves APIs manually by walking the PEB loader list and hashing export names. most user-facing strings that i saw were stack dwords XOR-decoded at runtime

the button handler reads the edit control text into a global buffer, hashes the input with a repeated FNV-1a-style loop and uses the resulting 32-bit value as a key to decrypt a small self-modifying code stub. (neat!) if the key is correct then the stub decrypts into a valid adb check and returns the xor key for the "Correct Key!" message

the target hash/decryption key is:

```text
0x350721c5
```

as mentioned a short printable preimage for that is:

```text
pXi8
```

## initial recon

Ghidra (mmgmnghh I LVEO YOU GHIDRA I WILL NEVER USE BINARYNINJA!!) identifies the executable as a tiny PE32 program

```text
Image base: 00400000
.text:     00401000 - 004019ff
.data:     00402000 - 004021ff
.tls:      00403000 - 004031ff
Entry:     00401000
TLS cb:    0040151b
```

i see no normal imports which tells me it might be manual api resolution

## api resolution

at 00401000, the code walks the PEB loader list and hashes module names using ROR13-style hash. two module hashes are important here

```text
KERNEL32.DLL -> 0x6e2bca17
NTDLL.DLL    -> 0xad74dbf2
```

now function 004015d1 resolves exported APIs from a module base in EBX. it iterates the export name table and computes the same ROR13 hash over ASCII export names, and returns the resolved func address.

several resolved API hashes map to the usual WIN32 gui funcs:

```text
0xec0e4e8e -> LoadLibraryA
0x73e2d87e -> ExitProcess
0x7946c61b -> VirtualProtect
0x51e20cca -> RegisterClassExA
0x84454941 -> CreateWindowExA
0x7ac67bed -> GetMessageA
0x8fde2c7e -> TranslateMessage
0x690a1701 -> DispatchMessageA
0xb9a87723 -> DefWindowProcA
0x4be0469d -> PostQuitMessage
0xa1ccb963 -> GetWindowTextA
0xbc4da2a8 -> MessageBoxA
```

the gui setup creates:

```text
Window class: PWNClass
Window title: CrackMe by PWN
Static text:  Enter Key:
Edit id:      0x3e9
Button text:  Check
Button id:    0x3ea
```

## runtime string decoding

function 00401983 is a small XOR decoder:

```asm
00401983  push eax
00401984  push ecx
00401985  push esi
00401986  mov  eax, [esi]
00401988  xor  eax, edx
0040198a  mov  [esi], eax
0040198c  add  esi, 4
0040198f  loop 00401986
00401991  pop  esi
00401992  pop  ecx
00401993  pop  eax
00401994  ret
```

the program places encoded dwords on the stack, sets ESI to the stack buffer, sets ECX to the dword count, sets EDX to the XOR key, and calls this decoder.

examples:

```text
0x05c481bc, 0x138fc0fa, 0x77a19ea5 XOR 0x77a1f2c9
-> "user32.dll"

0x012cffc9, 0x0a08adf9, 0x6f43ace7 XOR 0x6f438d9e
-> "Wrong Key!"

0x1d3ee261, 0x4f38ee47, 0x4e35e869, 0x6f4c8d22 XOR 0x6f4c8d22
-> "Correct Key!"
```

## window procedure

the main window procedure starts at 0040164b

relevant behavior:

```asm
0040164e  cmp [ebp+0c], 0x111      ; WM_COMMAND
00401655  jz  00401673
...
00401673  mov eax, [ebp+10]
00401676  cmp ax, 0x3ea            ; Check button id
0040167a  jz  00401690
...
00401690  push 0x100
00401695  push 0x40204c            ; input buffer
0040169a  push [0x004021a4]        ; edit hwnd
004016a0  call [GetWindowTextA]
```

if the edit box is empty, it does nothing. otherwise, it enters the protected check path. if that returns 0 it decoded and displays "Wrong Key!" (aww man) if it returns nonzero then it uses that return value to decode and display "Correct Key!"

## anti-debug and multiplier setup

there is a TLS callback at 0040151b, on normal startup it fixes the hash multiplier:

```text
Initial DAT_00402000: 0xdfadbb2d
TLS XOR value:        0xdeadbabe
Clean multiplier:     0x01000193
```

SO!!!!!

```text
0xdfadbb2d XOR 0xdeadbabe = 0x01000193
```

we have just found the FNV prime!! the tls callback and startup code also contain adb checks. if some checks fail then the multiplier is changed to a bad value such as 0x13371337 (so freaking leet haxor xd) or 0x5a8e4c19 which prevent the right decryption key from being produced

startup also calls some native anti-debug apis like NtSetInformationThread with ThreadHideFromDebugger and NtQueryInformationProcess with ProcessDebugPort
but if u thought that could stop gurneyburner52 u are sorely mistaken!!! >:3

## hidden check routine

the protected check routine is at 00401864

it first computes a code checksum over 00401000 for 0x9a5 bytes:

```asm
0040189b  mov esi, 0x401000
004018a0  mov ecx, 0x9a5
004018a5  xor eax, eax
004018a7  movzx edx, byte ptr [esi]
004018aa  add eax, edx
004018ac  ror eax, 7
004018af  inc esi
004018b0  loop 004018a7
```

then:

```text
key = 0x811c9dc5 XOR dword_004019cd XOR checksum
```

in the clean binary, dword_004019cd equals the computed checksum, so they cancel out:

```text
checksum       = 0xd2eb8a27
dword_004019cd = 0xd2eb8a27
initial key    = 0x811c9dc5
```

then it hashes the input at 0040204c
this means that the effective clean hash algorithm is:

```c
uint32_t key = 0x811c9dc5;

for (uint32_t round = 0; round < 0x4c4b40; round++) {
    for (char *p = input; *p != 0; p++) {
        key = (key ^ (uint8_t)*p) * 0x01000193;
    }
}
```

this is FNV-1a-like, but repeated 0x4c4b40 times over the same input (thats 5 million times..)

## self modifying stub

i thought this was kinda cool but after hashing the routine calls VirtualProtect to make 004019a5 writable/executable and decrypts 9 dwords:

```asm
004018e2  push 0x40214c
004018e7  push 0x40
004018e9  push 0x24
004018eb  push 0x4019a5
004018f0  call [VirtualProtect]

004018f6  push ebx                 ; EBX is input-derived hash key
004018f7  mov edi, 0x4019a5
004018fc  mov ecx, 9

00401901  mov eax, [edi]
00401903  xor [edi], ebx
00401905  add ebx, eax             ; original ciphertext dword
00401907  rol ebx, 5
0040190a  add edi, 4
0040190d  loop 00401901

0040190f  call 004019a5
```

so the hash output must also be the correct decryption key for the stub

the encrypted bytes at 004019a5 are:

```text
a1 80 37 35 cd 4c 54 3f 52 33 66 f7 d0 94 44 aa
17 25 2d 2e 4e 8f 3c 8d 9b c1 36 5c a2 54 67 5e
3c 1d ed 07
```

the correct decryption key is:

```text
0x350721c5
```

and decrypting with that key gives:

```asm
004019a5  mov eax, dword ptr fs:[0x30]
004019ab  cmp byte ptr [eax+2], 0
004019af  jne 004019c3
004019b1  mov eax, dword ptr [eax+0x68]
004019b4  and eax, 0x70
004019b9  test eax, eax
004019bb  jne 004019c3
004019bd  mov eax, 0x6f4c8d22
004019c2  ret
004019c3  xor eax, eax
004019c5  ret
004019c6  nop
004019c7  nop
004019c8  nop
```

sooo that confirms the expected behavior:

1. check PEB.BeingDebugged.
2. check PEB.NtGlobalFlag & 0x70.
3. if clean, return 0x6f4c8d22.
4. if debugged, return zero.

the return value 0x6f4c8d22 is then used as the XOR key to decode the success message

## recovering the serial (oh boy)

at this point the problem is really just:

```text
find input such that repeated_hash(input) == 0x350721c5
```

a small staged preimage search over short printable/alphanumeric inputs was enough. but wait... gurneyburner isn't that just bruteforcing??? well... normally a bruteforce would be idiotic considering it is hashed for about 5 MILLION rounds but.. we already know what hash we are looking for and we can just filter candidates by checking only the low 8 and low 16 bits, then running the full 32-bit hash only on the survivors!!

first one i found was pXi8

we can verify:

```javascript
const serial = "pXi8";
const target = 0x350721c5 >>> 0;
const prime = 0x01000193;
const rounds = 0x4c4b40;

let key = 0x811c9dc5 >>> 0;
const bytes = Buffer.from(serial, "ascii");

for (let r = 0; r < rounds; r++) {
  for (const b of bytes) {
    key = Math.imul((key ^ b) >>> 0, prime) >>> 0;
  }
}

console.log("hash = 0x" + key.toString(16).padStart(8, "0"));
console.log("ok =", key === target);
```

output:

```text
hash = 0x350721c5
ok = true
```

since pXi8 produces 0x350721c5, it decrypts the stub correctly. the stub returns 0x6f4c8d22, which decodes the success message of "Correct Key!"

## keygen? pls gurneyburner i dont like using pXi8 i want something longer or cooler

well this crackme doesn't have a name/serial pair or a reversible serial formula, it just takes your text input and reduces it to a 32-bit state:

```text
input -> repeated FNV-style hash -> 0x350721c5
```

so a "keygen" for this would basically be a preimage generator/finder for the fixed target hash. pXi8 is not the ONLY answer.

the target is only 32 bits so the other valid strings should exist in large enough input spaces. however, there is no clean closed-form way to turn arbitrary text into a valid serial, new serials are found by searching a bounded candidate space and testing.

```text
repeated_hash(candidate) == 0x350721c5
```

i've attached gpu_key_search.py and will explain it below

## GPU search for serials

gpu_key_search.py is included for bounded GPU preimage searches. it uses CuPy/NVRTC (i cba to install hashcat or cuda sdk while solving) to run the recovered hash on an NVIDIA GPU (sorry amd)

note that there are technically infinite serials unless the alphabet and length are bounded, this can enumerate all candidates inside a finite space, like all alphanumeric length-4 strings or all printable length-5 strings.

some example runs:

```powershell
python gpu_key_search.py --length 4
python gpu_key_search.py --length 4 --all
python gpu_key_search.py --alphabet printable --length 5 --all
python gpu_key_search.py --chars abcdef0123456789 --min-len 1 --max-len 6 --all
```

example run over all alphanumeric length-4 space on one of my RTX 5080:

```text
GPU: NVIDIA GeForce RTX 5080
target: 0x350721c5
alphabet (62): ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
mode: stop at first hit

length 4: 14,776,336 candidates
hit: pXi8

checked 9,961,472 candidates in 12.97s
```

search-space is the limiting factor here:

```text
alnum length 4:      62^4 =        14,776,336
alnum length 5:      62^5 =       916,132,832
alnum length 6:      62^6 =    56,800,235,584
printable length 5:  95^5 =     7,737,809,375
```

gurneyburner52 signing off thank u for reading and feel free to dm me on discord (id: 1442303538607816774) for any help! ^.^

