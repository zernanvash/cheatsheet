# BobxReal You Can't do it V2 ;) Writeup

Challenge_URL: https://crackmes.one/crackme/69991ad28c526c61da611dd0

main behavior:
- seed setup from time/pid constants
- vectored exception handler setup and trigger
- internal table/program generation
- user input read and length checks
- randomized handler loop for final decision

- veh handler: "0x140002190"
- init funcs:
  - "0x140002250"
  - "0x140003ec0"
  - "0x1400024e0"
- real checker handler: "0x140004520"
- vm interpreter: "0x1400034e0"
- dispatch state loop: "0x140005d23" block


key globals:
- "0x140030b68" --> evolving 64-bit seed/state
- "0x140030b58" --> loop selector xor state
- "0x140030e08" --> 32-bit exception seed ("exc_seed")
- "0x140030b70..0x140030b7c" --> 4 target dwords for checker
- "0x140030e10" --> randomized dispatch pointer table
- "0x140030b61" --> anti/debug flag that alters checker behavior


seed + exception
early main seed path:
- calls "GetTickCount64"
- calls "GetCurrentProcessId"
- xors with "0xfeedfacedeadc0de"
- runs xorshift style mixing loop (32 rounds)
- writes mixed value into "0x140030b68"

veh path at "0x140002190":
- handles exception code "0x80000003" and "0xc0decafe"
- computes:
  - exc_seed = GetTickCount() ^ GetCurrentProcessId() ^ 0xabcdef01
- stores "exc_seed" at "0x140030e08"
- xors selector state ("0x140030b58") with same value

then main does second mixing stage using "exc_seed" and continues init


dispatch loop
- input length must be 16

loop core near "0x140005d23":
- starts with "eax = 0x11"
- computes index by modulo 10 using:
  - "ecx = [0x140030b58] ^ eax"
  - arithmetic trick with "0xcccccccd" to do "% 10"
- picks function pointer from dispatch structure at "0x140030e10"
- calls function
- repeats until:
  - return "0x99" --> success
  - return "0xff" --> fail

this outer loop is the reason method 1 works


handler behavior in dispatch set
- "0x140004220" --> returns "0x22"
- "0x140004230" --> anti-debug heavy, returns "0x33" or "0xff", may set flags
- "0x1400044a0" --> returns "0x44" or "0xff"
- "0x1400044d0" --> returns "0x55" or "0xff"
- "0x140004500" --> integrity check route, returns "0x66" or "0xff"
- "0x140004520" --> vm checker route, returns "0x77" or "0xff"
- "0x140004770" --> returns "0x88" or "0xff" (effectively often "0x88")
- "0x140004790" --> crc heavy route, can yield "0x99" or "0xff"
- "0x140004a60" --> constant "0x99"
- "0x140004a70" --> constant "0xff"

- there are legitimate routing chains where key is not the deciding factor
- this enables random retry success behavior




method 1 (randomized route exploit)
idea:
- if length is 16, keep launching with fixed key
- rely on randomized dispatcher eventually hitting success terminal

fixed same key can produce both outcomes across launches


- input len != 16 --> fail
- input len == 16 --> randomized loop
- random route hits success --> correct <-- stop
- else --> wrong --> relaunch





method 2 (keygen)
real checker:
- function "0x140004520"
- it prepares vm state, runs "0x1400034e0", extracts 4 dword outputs
- compares outputs against "0x140030b70..0x140030b7c"
- returns:
  - "0x77" when checker condition passes path
  - "0xff" on checker fail path

special branch inside checker:
if anti flag ("0x140030b61") is set:
- sets output sentinel "0xdeadbeef"
- updates target globals from current outputt

otherwise does direct compare against targets

vm extraction:
- extracted runtime blobs:
  - opcode map ("opmap")
  - vm program ("prog_len = 129")
  - crc/seed table
  - targets
- opmap for used bytes is mostly identity mapping for vm op ids

vm behavior:
- loads 4 input dwords (bytes 0..15)
- applies repeated xor against table words at offsets "0x10..0x4c"
- in observed table, this xor sequence net effect is neutral for final chekced words
- final checked output equals input[0..15] as 4 little-endian dwords

--> required key bytes == target dwords serialized little endian <--



recovery approach:
- run init under emulator with many random seeds
- vary 64-bit seed and 32-bit "exc_seed"
- observe generated targets

result
- targets do not depend on initial 64-bit seed in final relation
- targets depend only on "exc_seed"


-> "target[i] = base[i] ^ exc_seed"

base constants (from "exc_seed = 0")
- "0x6e2f1a3b"
- "0xc4d85f92"
- "0x1b7e3c6d"
- "0xa09f4e21"

exc_seed comes from veh computation
-> "exc_seed = GetTickCount() ^ GetCurrentProcessId() ^ 0xabcdef01"
(stored at global "0x140030e08"))


formula
given "exc_seed" (u32):
- "D0 = 0x6e2f1a3b ^ exc_seed"
- "D1 = 0xc4d85f92 ^ exc_seed"
- "D2 = 0x1b7e3c6d ^ exc_seed"
- "D3 = 0xa09f4e21 ^ exc_seed"

key: "key = pack_le32(D0) || pack_le32(D1) || pack_le32(D2) || pack_le32(D3)" (= 16 key bytes)




!! note:
even with correct formula key, full app can still print "wrong." on some runs cause outer randomized dispatcher can terminate in fail path before useful route


check out the scripts in /random_method/ and /keygen_method/
(tested on linux + wine)
