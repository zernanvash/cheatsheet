# The Barista's Secret Writeup

Challenge_URL: https://crackmes.one/crackme/69b878e2ddd6176826ae8a22

the binary has very descriptive symbol names thanks to the debug info left in by mingw

sym.anti_debug__
sym.deobf_unsigned_char_const__unsigned_long_long__unsigned_char__char_
sym.brew_hash_unsigned_char_const__unsigned_long_long_
sym.parse_blocks_char_const__unsigned_int__unsigned_int__unsigned_int_
sym.check1_unsigned_int__unsigned_int_
sym.check2_unsigned_int_
sym.check3_unsigned_int__unsigned_int_
sym.validate_char_const_
sym.main


the deobf function does a simple byte by byte XOR with a constant key

from the call sites we find XOR key 0x13 used throughout


applying it to the blob "P|wvQavdv`cav``|rarqzprQAVD>" at 0x140005050:

offset +0x08, len 8: "v`cav``|" ^ 0x13  --> "espresso"
offset +0x10, len 7: "rarqzpr"  ^ 0x13  --> "arabica"
offset +0x17, len 5: "QAVD>"    ^ 0x13  --> "BREW-"

the last one is used by parse_blocks to validate the key prefix
the first two are used by check2


parse blocks
1. deobfuscate and strncmp the first 5 bytes against "BREW-"
2. loop 3 times (one per block):
    - read 8 bytes from current position
    - validate each char is in [0-9], [a-f], or [A-F]
    - call strtoul(buf, NULL, 16) to get the uint32 value
    - after block 0 and block 1, expect a '-' separator

so each block is simply a 32-bit integer expressed as exactly 8 hex characters


check1(block1, block2)

xor eax, 0xc0ffee42
cmp dword [var_18h], eax   ; var_18h = block2
sete al

condition: block2 == block1 ^ 0xC0FFEE42

check2(block3)

decodes "espresso" (8 bytes) and "arabica" (7 bytes)
then builds two uint32 values from "espresso"

val1 = le32("espr") = 0x72707365
val2 = le32("esso") = 0x6F737365

and one from "arabica":

val3 = le32("arab") = 0x62617261

then checks: block3 ^ val1 ^ val2 ^ val3 == 0xCAFEBABE

and this means: block3 = 0xCAFEBABE ^ 0x72707365 ^ 0x6F737365 ^ 0x62617261 = 0xB59CC8DF



check3 builds an 8-byte buffer by extracting the individual bytes of block1 and block2
(effectively the two 32-bit values concatenated), then calls brew_hash on it

brew_hash:

uint32 brew_hash(uint8_t* data, uint64_t len) {
    uint32_t h = 0xC0FFEE42
    for i in range(len):
        h ^= data[i] * 0x9E3779B1
        h  = rol32(h, 13)
        h -= 0x3F001200
    return h
}

loop body

imul eax, eax, 0x9e3779b1   ; b * magic
xor  dword [var_4h], eax    ; h ^= contrib
rol  dword [var_4h], 0xd    ; h = rol32(h, 13)
sub  dword [var_4h], 0x3f001200


final check:

and eax, 0xfffff
cmp eax, 0xdecaf            ; lower 20 bits must equal 0xDECAF
sete al

so we need: brew_hash([block1_le_bytes || block2_le_bytes]) & 0xFFFFF == 0xDECAF




anti_debug() sets a global at 0x14000a0a0 if it detects a debugger. validate() reads it at the end and returns 0 if it is non- zero.



solving:

block3 = 0xB59CC8DF
block2 = block1 ^ 0xC0FFEE42  (determined once block1 is chosen)

for block1 we need to satisfy the hash constraint. the brew_hash is a non-invertible
custom function, so we use z3 to model it symbolicalyl and let it find a valid block1

b1 = BitVec('block1', 32)
b2 = b1 ^ 0xC0FFEE42
data = [b1[7:0], b1[15:8], b1[23:16], b1[31:24],
        b2[7:0], b2[15:8], b2[23:16], b2[31:24]]
h = brew_hash_z3(data)
solve: (h & 0xFFFFF) == 0xDECAF

z3 gives us:

block1 = 0x3D5AF284
block2 = 0x3D5AF284 ^ 0xC0FFEE42 = 0xFDA51CC6

so:

brew_hash([0x84, 0xF2, 0x5A, 0x3D, 0xC6, 0x1C, 0xA5, 0xFD]) = 0x1BADECAF
0x1BADECAF & 0xFFFFF = 0xDECAF  --> ok


key:  BREW-3D5AF284-FDA51CC6-B59CC8DF
flag: CODEBREW{3D5AF284-FDA51CC6-B59CC8DF}
