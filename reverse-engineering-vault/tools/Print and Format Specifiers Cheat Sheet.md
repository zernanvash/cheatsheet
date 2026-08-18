# Print and Format Specifiers Cheat Sheet

Use this reference when reading or writing formatted output in C, Python, shell scripts, debugger helpers, keygens, and byte-dump tools.

## Quick Answer: What Does `%02x` Mean?

`%02x` formats an integer as lowercase hexadecimal with a minimum width of two characters and leading zeroes.

```python
value = 10
print("%02x" % value)  # 0a
print(f"{value:02x}")  # 0a (modern Python)
```

```c
unsigned int value = 10;
printf("%02x\n", value); /* 0a */
```

| Part | Meaning |
| --- | --- |
| `%` | Start a conversion specification |
| `0` | Pad the field with zeroes instead of spaces |
| `2` | Use a minimum field width of two characters |
| `x` | Render an unsigned integer in lowercase hexadecimal |

The width is a minimum, not a limit. Formatting `0x123` with `%02x` still produces `123`.

## C `printf` Specification Anatomy

```text
%[flags][width][.precision][length]conversion
```

Example:

```text
%#018llx
```

This means: alternate form (`#`), zero padding (`0`), minimum width 18, `unsigned long long` (`ll`), lowercase hexadecimal (`x`). The width includes the `0x` prefix.

### Flags

| Flag | Meaning | Example | Result for the example value |
| --- | --- | --- | --- |
| `-` | Left-align within the field | `%-6d`, `42` | `42    ` |
| `+` | Always show a numeric sign | `%+d`, `42` | `+42` |
| space | Prefix positive values with a space | `% d`, `42` | ` 42` |
| `#` | Use an alternate representation | `%#x`, `42` | `0x2a` |
| `0` | Pad numeric fields with zeroes | `%06d`, `42` | `000042` |

If both `-` and `0` are present, left alignment wins and zero padding is ignored. For integer conversions, an explicitly specified precision also disables `0` padding.

### Width and Precision

| Form | Meaning | Example result |
| --- | --- | --- |
| `%8d` | Minimum width 8, right-aligned | `      42` |
| `%-8d` | Minimum width 8, left-aligned | `42      ` |
| `%08x` | Eight hexadecimal positions, zero-padded | `0000002a` |
| `%.4x` | At least four hexadecimal digits | `002a` |
| `%8.4x` | Width 8 with at least four digits | `    002a` |
| `%.3s` | Print at most three string characters | `rev` from `reverse` |
| `%8.2f` | Width 8 with two digits after the decimal | `   12.35` |
| `%*d` | Take the width from the next argument | runtime-controlled width |
| `%.*s` | Take the precision from the next argument | runtime-controlled string limit |

```c
printf("%*d\n", 6, 42);         /*     42 */
printf("%.*s\n", 4, "reverse"); /* reve */
```

### Integer Conversions

| Conversion | Meaning | Typical argument type |
| --- | --- | --- |
| `%d`, `%i` | Signed decimal | `int` |
| `%u` | Unsigned decimal | `unsigned int` |
| `%o` | Unsigned octal | `unsigned int` |
| `%x` | Unsigned lowercase hexadecimal | `unsigned int` |
| `%X` | Unsigned uppercase hexadecimal | `unsigned int` |
| `%c` | One character | `int` after integer promotion |

### Floating-Point Conversions

| Conversion | Meaning |
| --- | --- |
| `%f`, `%F` | Fixed-point decimal |
| `%e`, `%E` | Scientific notation |
| `%g`, `%G` | Shorter of fixed or scientific notation |
| `%a`, `%A` | Hexadecimal floating-point notation |

For `printf`, a `float` argument is promoted to `double`. Use `%f` for either promoted `float` or `double`; use `%Lf` for `long double`.

### Text, Pointer, and Special Conversions

| Conversion | Meaning | Important note |
| --- | --- | --- |
| `%s` | Null-terminated C string | Precision can cap the number of printed characters |
| `%c` | Single character | Receives an `int` due to promotion |
| `%p` | Pointer address | Pass a `void *`; representation is implementation-defined |
| `%%` | Literal percent sign | Consumes no argument |
| `%n` | Write the printed character count through a pointer | Dangerous with attacker-controlled formats |

### Length Modifiers

Length modifiers tell `printf` how to interpret the corresponding variadic argument.

| Modifier | Common integer use | Example |
| --- | --- | --- |
| `hh` | `signed char` / `unsigned char` after promotion | `%hhu`, `%02hhx` |
| `h` | `short` / `unsigned short` after promotion | `%hd`, `%hx` |
| none | `int` / `unsigned int` | `%d`, `%x` |
| `l` | `long` / `unsigned long` | `%ld`, `%lx` |
| `ll` | `long long` / `unsigned long long` | `%lld`, `%016llx` |
| `j` | `intmax_t` / `uintmax_t` | `%jd`, `%jx` |
| `z` | `size_t` or its signed counterpart | `%zu`, `%zx` |
| `t` | `ptrdiff_t` or its unsigned counterpart | `%td`, `%tx` |
| `L` | `long double` | `%Lf` |

For fixed-width integers, prefer the portable macros from `<inttypes.h>`:

```c
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

uint8_t byte = 0x0a;
uint64_t state = UINT64_C(0x1234);

printf("byte=%02" PRIx8 "\n", byte);
printf("state=%016" PRIx64 "\n", state);
```

## Common C Formatting Patterns

| Goal | Format | Example output |
| --- | --- | --- |
| Two-digit lowercase byte | `%02x` | `0a` |
| Two-digit uppercase byte | `%02X` | `0A` |
| Eight-digit 32-bit-style hex | `%08x` | `deadbeef` |
| Sixteen-digit 64-bit-style hex | `%016llx` | `0000000000001234` |
| Hex with prefix | `%#x` | `0x2a` |
| Pointer | `%p` | implementation-defined, commonly `0x...` |
| Signed decimal with sign | `%+d` | `+42` |
| Zero-padded decimal | `%06d` | `000042` |
| Two decimal places | `%.2f` | `12.35` |
| Literal percent | `%%` | `%` |

### Safe Byte Dump

```c
#include <stddef.h>
#include <stdio.h>

void print_hex(const unsigned char *buffer, size_t length) {
    for (size_t i = 0; i < length; i++) {
        printf("%02x%s", (unsigned int)buffer[i], i + 1 == length ? "\n" : " ");
    }
}
```

The cast makes the promoted type expected by `%x` explicit. Using `unsigned char` also avoids sign extension of bytes at or above `0x80`.

## Python Legacy `%` Formatting

In Python, `print()` itself does not interpret `%02x`. The string `%` operator performs the formatting first, and `print()` outputs the resulting string.

```python
value = 42
formatted = "%02x" % value
print(formatted)  # 2a
```

### Common Python `%` Conversions

| Conversion | Meaning | Example |
| --- | --- | --- |
| `%d`, `%i` | Signed decimal integer | `"%d" % 42` |
| `%u` | Decimal integer; retained for compatibility | `"%u" % 42` |
| `%o` | Octal integer | `"%o" % 42` |
| `%x`, `%X` | Lowercase / uppercase hexadecimal | `"%02x" % 10` |
| `%e`, `%E` | Scientific notation | `"%.2e" % 1000` |
| `%f`, `%F` | Fixed-point decimal | `"%.2f" % 12.345` |
| `%g`, `%G` | Compact floating-point representation | `"%g" % 12.0` |
| `%c` | One character from an integer or one-character string | `"%c" % 65` |
| `%s` | Convert with `str()` | `"%s" % value` |
| `%r` | Convert with `repr()` | `"%r" % value` |
| `%a` | Convert with `ascii()` | `"%a" % value` |
| `%%` | Literal percent sign | `"100%%" % ()` |

Python's `%` formatting does not use C length modifiers such as `hh`, `l`, or `ll`; Python integers are not restricted to those C widths.

### Multiple and Named Values

```python
address = 0x401000
opcode = 0x90

print("address=%08x opcode=%02x" % (address, opcode))
print("address=%(address)08x opcode=%(opcode)02x" % {
    "address": address,
    "opcode": opcode,
})
```

## Modern Python: `format()` and f-Strings

Modern Python uses the format-specification mini-language:

```text
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

```python
value = 42

print(f"{value:02x}")    # 2a
print(f"{value:08X}")    # 0000002A
print(f"{value:#x}")     # 0x2a
print(f"{value:#010x}")  # 0x0000002a
print(f"{value:08b}")    # 00101010
print(f"{value:03d}")    # 042
```

The same specifications work with `format()`:

```python
print(format(42, "02x"))
print("{:02x}".format(42))
```

### Python Alignment and Fill

| Specifier | Meaning | Example result for `rev` |
| --- | --- | --- |
| `:<8` | Left-align in width 8 | `rev     ` |
| `:>8` | Right-align in width 8 | `     rev` |
| `:^8` | Center in width 8 | `  rev   ` |
| `:*^9` | Center and fill with `*` | `***rev***` |

```python
name = "rev"
print(f"{name:<8}")
print(f"{name:>8}")
print(f"{name:^8}")
print(f"{name:*^9}")
```

### Python Numeric Types

| Type | Meaning | Example |
| --- | --- | --- |
| `b` | Binary | `f"{42:08b}"` |
| `o` | Octal | `f"{42:o}"` |
| `d` | Decimal | `f"{42:04d}"` |
| `x`, `X` | Lowercase / uppercase hexadecimal | `f"{42:02x}"` |
| `f`, `F` | Fixed-point | `f"{12.345:.2f}"` |
| `e`, `E` | Scientific notation | `f"{1000:.2e}"` |
| `g`, `G` | Compact floating point | `f"{12.0:g}"` |
| `%` | Percentage | `f"{0.125:.1%}"` |
| `c` | Unicode character from an integer | `f"{65:c}"` |

### Python Byte-Dump Patterns

```python
data = bytes([0x00, 0x0a, 0x80, 0xff])

print(data.hex())
print(data.hex(" "))
print(" ".join(f"{byte:02x}" for byte in data))
print("".join("%02x" % byte for byte in data))
```

Output:

```text
000a80ff
00 0a 80 ff
00 0a 80 ff
000a80ff
```

## Shell `printf`

POSIX shell `printf` uses a C-like format syntax and is more predictable across environments than `echo` for escapes and exact output.

```bash
printf '%02x\n' 10
printf '%08x\n' 3735928559
printf '%s\n' '68656c6c6f' | xxd -r -p
```

Quote the format string so the shell does not interpret special characters before `printf` receives them.

## `printf` Versus `scanf`

Similar-looking specifications have different meanings:

- In `printf`, width is the minimum output field width.
- In `scanf`, width is the maximum number of input characters to consume.
- In `scanf`, `float *` uses `%f`, while `double *` uses `%lf`.
- In `printf`, both promoted `float` and `double` use `%f`; `long double` uses `%Lf`.
- In `scanf`, `%n` writes the number of characters consumed and does not perform a conversion.

```c
unsigned int value;
char word[9];

scanf("%2x", &value); /* consume at most two hexadecimal characters */
scanf("%8s", word);   /* leave space for the terminating null byte */
```

## Reversing Clues

Format strings often reveal argument types and program intent before a function is fully understood:

| Observed string | Likely clue |
| --- | --- |
| `%02x` repeated in a loop | Byte-by-byte hex dump, hash, key, or ciphertext output |
| `%08x` | 32-bit word, flags, checksum, or address-like value |
| `%016llx` | 64-bit state, counter, timestamp, or key material |
| `%p` | Pointer logging or memory diagnostics |
| `%zu` | Buffer length, object count, or allocation size |
| `%.*s` | Length-bounded text or binary-safe diagnostic output |
| `%hhn` / `%n` | Character-count write; investigate for a format-string vulnerability |
| `scanf("%x", ...)` | User input parsed as hexadecimal |

When decompiling a variadic call, the format string is evidence for reconstructing argument types. Still verify the call site, casts, register usage, and stack layout; a malformed program can intentionally use mismatched types.

## Common Pitfalls

### Signed-byte expansion

Printing a negative `char` through an integer conversion can produce a value such as `ffffff80` instead of `80`. Convert through an unsigned byte type:

```c
signed char input = (signed char)0x80;
printf("%02x\n", (unsigned int)(unsigned char)input); /* 80 */
```

### Wrong variadic type

C does not type-check variadic arguments at runtime. A conversion that does not match the actual promoted argument type causes undefined behavior.

```c
size_t length = 16;
printf("%zu\n", length);
```

Do not assume `%lu` is portable for `size_t`; its underlying type differs across ABIs.

### Width mistaken for truncation

`%02x` does not restrict the result to one byte. Mask or validate the value when byte semantics matter:

```python
value = 0x123
print(f"{value:02x}")        # 123
print(f"{value & 0xff:02x}") # 23
```

### Literal percent signs

Use `%%` in C, legacy Python `%` formatting, and shell `printf`. A standalone `%` is sufficient in an f-string unless it is being used as the format type.

## Format-String Vulnerability Warning

Never allow untrusted text to become the C format string.

```c
/* Vulnerable: user input controls conversions such as %p or %n. */
printf(user_input);

/* Safer: user input is data for a fixed format. */
printf("%s", user_input);
```

> 🛡️ **Remediation Note:** Use constant format strings, enable compiler format warnings, treat warnings as errors, and review logging wrappers that forward variadic arguments. In GCC or Clang builds, `-Wall -Wextra -Wformat=2 -Wformat-security` catches many dangerous mismatches and non-literal formats.

## Compact Lookup

```text
%02x       lowercase byte-style hex: 0a
%02X       uppercase byte-style hex: 0A
%#04x      prefixed hex with total width 4: 0x0a
%08x       zero-padded 8-position hex
%016llx    zero-padded 16-position unsigned long long hex
%d         signed decimal
%u         unsigned decimal
%zu        size_t as unsigned decimal
%o         octal
%c         character
%s         string
%.8s       print at most 8 string characters
%p         pointer
%.2f       fixed-point with 2 fractional digits
%e         scientific notation
%%         literal percent sign
```

Modern Python equivalents generally remove the leading `%` and place the specification after `:`:

```python
f"{value:02x}"
f"{value:#010x}"
f"{value:08b}"
f"{value:.2f}"
f"{text:.8s}"
```
