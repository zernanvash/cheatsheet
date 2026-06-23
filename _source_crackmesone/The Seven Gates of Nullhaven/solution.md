# The Seven Gates of Nullhaven Writeup

static stripped elf64. no symbols, but string anchors made navigation easy

the important gate entry points were
gate 1 --> 0x402e5f
gate 2 --> 0x403004
gate 3 --> 0x403280
gate 4 --> 0x403511
gate 5 --> 0x4037d2
gate 6 --> 0x4039a0
gate 7 --> 0x403d40

a key early observation was input api behavior
- function 0x401b00 reads fixed raw bytes from stdin, not line based
- function 0x401b40 is line based and trims newline



gate 1 > looked like an overflow, but the real logic was a structured buffer validator

checks
- length > 0x28
- bytes at offset 32..35 must be etag
- bytes at offset 36..39 must be 0x0000b00f in little endian
- byte at offset 40 must be 0x01
- low 16 bits of a crc style accumulator must equal 0x9857

the crc routine at 0x402096 is not reflected crc32
it behaves like a crc16 ccitt style step

init eax = 0xffffffff
for each byte --> eax xor= byte << 8
repeat 8 times --> if sign bit of ax set then eax = (eax << 1) xor 0x1021 else eax = eax << 1

because most bytes were free, i fixed bytes 0..29 to zero and solved only bytes 30 and 31 by search (65536 candidates)

byte 30 = 0x86
byte 31 = 0x67

payload: 0000000000000000000000000000000000000000000000000000000000008667455441470fb0000001

flag 1: NULLHAVEN{OVERFLOW_THE_ABYSS_8A3F}

as i already said: acceptance is a static pattern plus a 16 bit checksum target. once the offsets are known, the solution space collapses quickly



gate 2 > two fixed block reads and constant checks

room 1 read: 64 bytes into buffer a
room 2 read: 64 bytes into buffer b

there must be no newline inserted between the payload blocks  (64 raw)

room1 dword at +32 --> 0xdecade42
room1 dword at +36 --> 0x50484153
room2 dword at +32 --> 0x4f50454e
room2 dword at +36 --> room1_dword32 xor 0xcafebabe = 0x143464fc

once those words are placed, the gate opens

flag 2: NULLHAVEN{CHAINED_CORRUPTION_B7E2}




gate 3: crypto style gate. requires 32 chars

transform pipeline
- input --> xor with 32 byte fibonacci stream --> nibble substitution table --> per byte rol schedule --> compare with 32 byte target

fibonacci stream generation in code is register based and produced
- 01 01 02 03 05 08 0d 15 22 37 59 90 e9 79 62 db 3d 18 55 6d c2 2f f1 20 11 31 42 73 b5 28 dd 05

the nibble table at 0x49ce40 is a permutation, so it is invertible
rol schedule is 1..7 repeating, so that is invertible too via ror

inversion
- target --> ror schedule --> inverse nibble map --> xor fibonacci

recovered input: SOLVETHEPUZZLEOFNULLHAVEN12345XX

flag 3: NULLHAVEN{UNRAVEL_THE_CIPHER_C9D1}



gate 4 > format check (xxxx-xxxx-xxxx-xxxx )with uppercase hex digits accepted by parser helper 0x4034be

let the parsed 16 bit groups be a, b, c, d.
constraints were:

- c xor a = 0x2ef3
- (d + b) mod 65536 = 0x425e
- (a * b) mod 65536 = 0xc033

this system has many solutions.. choosing a = 1 gives

- b = 0xc033
- c = 0x2ef2
- d = 0x425e - 0xc033 mod 65536 = 0x822b

0001-C033-2EF2-822B

flag 4 payload as hex: (includes non printable bytes)

349408f2eb0bd187e006c2ec369f14f1f171ba94ef



gate 5 > graph walk hidden behind moves

logic in 0x4037d2

- state starts at 0
- for each move char --> choose one of 4 transition entries for current state
- entry is xor obfuscated with 0xdeadbeef
- must remain in state range 0..15
- final raw transition value must equal 0xdeadbee2 ( state 13)

transition table base is 0x49cea0, 16 states x 4 edges

because state space is tiny, bfs finds shortest accepting path immediately

solution: UDLD

machine is only 16 states... static graph plus bfs == near instant solve

gate 6

- key length must be 11
- key must match a static value in code
- then sha256(key) is computed
- aes 128 ecb decrypt uses first 16 bytes of hash as key against static ciphertext
- if plaintext validation passes, flag prints

the important secret is hardcoded :(

key: VEIL_LIFTED

flag: NULLHAVEN{THROUGH_THE_STATIC_71AC}


gate 7 > this gate should be "final convergence" of prior tokens. actual behavior is weaker and mostly independent

flow: input (non empty) --> sha256 --> take first 16 bytes --> aes 128 ecb decrypt static block at 0x49d060 --> check output shape

acceptance check is not a strict phrase compare. it only requires a printable ascii prefix until first null with a small length bound. that means many unrelated inputs can pass by chance.

i used a targeted random search and found a valid key quickly: LwbsZVbFY9QZbCJ1qn-WkXpRuHgVE5iYZ5BsM7zOir_LWDFzN.WeRuan

successful run shows: ALL GATES HAVE BEEN BREACHED!




solved set

gate 1 core payload hex:
0000000000000000000000000000000000000000000000000000000000008667455441470fb0000001

gate 2 room1 constraints payload:
dword +32 = 0xdecade42
dword +36 = 0x50484153

gate 2 room2 constraints payload:
dword +32 = 0x4f50454e
dword +36 = 0x143464fc

gate 3 input:
SOLVETHEPUZZLEOFNULLHAVEN12345XX

gate 4 serial:
0001-C033-2EF2-822B

gate 5 path:
UDLD

gate 6 key:
VEIL_LIFTED

gate 7 key:
LwbsZVbFY9QZbCJ1qn-WkXpRuHgVE5iYZ5BsM7zOir_LWDFzN.WeRuan
