# flag.wasm Writeup

Challenge_URL: https://crackmes.one/crackme/6a1ec0cad7ff92e1214c0283

## Summary

The challenge file is a WebAssembly module built with Javy. The flag is embedded near the end of the module in the final data segment, close to the marker string `flag_encoded_hex_bytes`.

Final flag:

```text
RELUNSEC{j3vy_1s_4w3s0m3}
```

## Metadata

| Field | Value |
| --- | --- |
| File | `/Users/singularity/Downloads/flag.wasm` |
| SHA-256 | `f77349adb390932541d8c09370aaa5d5ec7deabca426111243335521a1f7ac85` |
| Format | WebAssembly binary module, version 1 |
| Runtime hints | WASI imports, Javy 8.0.0, JavaScript ES2020 |
| Goal | Recover the embedded flag |
| Patching | Not used |

## Environment

Tools used:

- `file`
- `strings`
- `node`
- `npx wasm2wat`
- small Node.js scripts for WebAssembly section parsing

## Triage

First, identify the file format:

```bash
file /Users/singularity/Downloads/flag.wasm
```

Result:

```text
/Users/singularity/Downloads/flag.wasm: WebAssembly (wasm) binary module version 0x1 (MVP)
```

Then inspect readable strings:

```bash
strings -a /Users/singularity/Downloads/flag.wasm | grep -iE 'flag|ctf|pass|key|correct|wrong|success|error|usage'
```

The useful hit was:

```text
flag_encoded_hex_bytes
```

The strings also showed Javy metadata:

```text
producers
language
JavaScript
ES2020
processed-by
Javy
8.0.0
javy_source
```

That suggests this WASM was produced from JavaScript through Javy.

## WASM Section Inspection

The module has WASI imports and the following exports:

```text
memory
cabi_realloc
config-schema
_start
```

Running `_start` with Node's WASI shim did not print anything useful, so the next step was static analysis.

A custom section parser showed the important layout:

```text
id 10 size 922643
id 11 size 334138
id 0 size 64  custom name=producers
id 0 size 39  custom name=import_namespace
id 0 size 132 custom name=javy_source
id 0 size 132 custom name=target_features
```

The string `flag_encoded_hex_bytes` was found at raw file offset `1260747`, inside the data section rather than inside a normal export.

## Data Segment Analysis

Parsing section 11, the WASM data section, showed that the marker was in the final data segment:

```text
data count 7005
segment 7004
len 132
dataStart 1260729
dataEnd 1260861
markerAt 1260747
```

The bytes around the marker contained this pattern:

```text
... flag_encoded_hex_bytes ...
be 52 be 45 be 4c be 55 be 4e be 53 be 45 be 43
be 7b be 6a be 33 be 76 be 79 be 5f be 31 be 73
be 5f be 34 be 77 be 33 be 73 be 30 be 6d be 33
be 7d ...
```

The repeated `be XX` pattern is the important part. Taking each byte that follows `0xbe` gives:

```text
52 45 4c 55 4e 53 45 43 7b 6a 33 76 79 5f 31 73 5f 34 77 33 73 30 6d 33 7d
```

Decoded as ASCII:

```text
RELUNSEC{j3vy_1s_4w3s0m3}
```

## Extraction Script

This Node.js snippet reproduces the extraction:

```js
const fs = require("fs");

const wasm = fs.readFileSync("/Users/singularity/Downloads/flag.wasm");
const marker = Buffer.from("flag_encoded_hex_bytes");
const pos = wasm.indexOf(marker);

if (pos < 0) {
  throw new Error("marker not found");
}

const segmentEnd = 1260861;
const tail = wasm.subarray(pos, segmentEnd);

const chars = [];
for (let i = 0; i < tail.length - 1; i++) {
  if (tail[i] === 0xbe && tail[i + 1] >= 0x20 && tail[i + 1] < 0x7f) {
    chars.push(String.fromCharCode(tail[i + 1]));
  }
}

console.log(chars.join(""));
```

Output:

```text
RELUNSEC{j3vy_1s_4w3s0m3}
```

## Conclusion

The flag was not printed by the program. It was embedded in the WASM data section as part of Javy/QuickJS serialized data. The marker `flag_encoded_hex_bytes` led to the final data segment, where the flag was encoded as ASCII bytes following repeated `0xbe` bytes.

Final answer:

```text
RELUNSEC{j3vy_1s_4w3s0m3}
```
