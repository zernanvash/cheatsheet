# Gadget Writeup

Challenge_URL: https://crackmes.one/crackme/6987dc623eb49a23d34176ed

when chall.exe starts:

1) opens gadget.hex
2) reads the full file into virtualalloc memory
3) runs tests by calling code loaded from gadget.hex at offset 0x40c
4) if test returns 0x1e it asks for input
5) it creates a thread with start routine at 0x140001b80
6) thread returns 1 for success and 0 for fail
7) main prints correct or wrong based on thread exit code


from rdata we have

- enter the flag:
- correct!
- wrong!
- fdb6ece8caefdeb4c2a5d6efc0efd6b7ccb3a19cfc8bdeacc299a1b2fc8bdda7c0ecdaa6d59afca6c98aa9e6

xrefs show these are used in fcn.140008100, which is the main driver


fcn.140008100 handles file io, tests, input, and worker thread launch
relevant path:

- read gadget.hex --> global size at 0x14000e030 and buffer at 0x14000e038
- test call --> [buffer + 0x40c](0xa, 0x14)
- expect return 0x1e
- read user input with fgets
- trim newline and CR
- create thread with lpstartaddress = 0x140001b80 and lpparameter = input buffer
- wait for thread
- get thread exit code
  - exit code == 1 --> print correct
  - else --> print wrong

function at 0x140001b80 is the actual checker

1) picks function pointers from gadget blob offsets
   - init or helper at buffer + 0x3e2
   - compare function at buffer + 0x55a if file is large enough
2) builds a local target string with fcn.140001450
3) transforms the user input via fcn.140001af0
4) calls compare function from gadget with
   transformed_input and target_string
5) returns 1 if compare returns 0


so:

local_target = fcn.140001450()
transformed = fcn.140001af0(user_input)
cmp_res = gadget_cmp(transformed, local_target)
return (cmp_res == 0)



fcn.140001450 copies a hardcoded ascii hex string into a local buffer. that exact target string is
fdb6ece8caefdeb4c2a5d6efc0efd6b7ccb3a19cfc8bdeacc299a1b2fc8bdda7c0ecdaa6d59afca6c98aa9e6


fcn.140001af0 is a pipeline of three sub steps
- step 1 --> base64 encode input
  done by fcn.1400015b0

- step 2 --> xor each byte with key stream
  done by fcn.140001870
  key stream is alternating bytes 0x98, 0xdf

- step 3 --> hex encode result bytes to lowercase ascii
  done by fcn.140001950

so the full forward transform  is

input --> base64(input) --> xor alt key 98 df --> hex lowercase

and this transformed text is compared to the hardcoded target hex string


so, to invert, given

target_hex = fdb6ece8caefdeb4c2a5d6efc0efd6b7ccb3a19cfc8bdeacc299a1b2fc8bdda7c0ecdaa6d59afca6c98aa9e6

invert is

1) bytes_44 = fromhex(target_hex)
2) b64_bytes[i] = bytes_44[i] xor key[i mod 2]
   key[0] = 0x98
   key[1] = 0xdf
3) input = base64_decode(b64_bytes)

after xor inversion we get this base64 text

eit7R0FkZzN0X0NhTl9CdTFsZF9mdTExX3ByMEdyQU19

then base64 decode gives

z+{GAdg3t_CaN_Bu1ld_fu11_pr0GrAM}
