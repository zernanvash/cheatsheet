# Cr4ckM3 Writeup

Challenge_URL: https://crackmes.one/crackme/6a21ed4d266afadcd56fabd9

## Summary

`Cr4ckM3.exe` is a Windows x64 GUI crackme that mimics a Windows activation dialog. The native executable is mainly a .NET host. The real activation logic is inside an embedded .NET assembly named `Cr4ckM3.dll`.

The product key is generated from the username:

1. Require username length to be at least 6 characters.
2. Compute `SHA256(username UTF-8)`.
3. Substitute each hash byte through a fixed 256-byte lookup table.
4. Encode the resulting bytes with the custom alphabet `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`.
5. Take the first 25 encoded characters.
6. Format as five groups of five characters: `XXXXX-XXXXX-XXXXX-XXXXX-XXXXX`.

Keygen: [`keygen.py`](./keygen.py)

## Target

```text
File: Cr4ckM3.exe
Type: PE32+ executable (GUI) x86-64, Windows
MD5: 50ba58d61e7bd9ce8dd99239001f6a4b
SHA256: 90ceeaeb44a6e94116dbe9e3a5bab7d7b24291382afd6ecd52610e6a0bf136e3
```

Extracted managed payload:

```text
File: embedded Cr4ckM3.dll
Type: PE32+ executable (GUI) x86-64 Mono/.NET assembly
SHA256: 389027d92aaf8595a2571c4c6b1933aed36876bffa1eefe228280ce9fe40f608
```

Tools used:

```text
IDA Pro / Hex-Rays
ilspycmd
Python 3
```

## Triage

Opening the EXE in IDA shows a normal PE32+ Windows GUI executable. The string table contains .NET-related paths and names, including:

```text
Cr4ckM3.dll
Q:\cscrackme\Cr4ckM3\obj\Release\net8.0-windows\win-x64\Cr4ckM3.pdb
System.Windows.Markup
```

Searching the raw file for PE and .NET metadata signatures showed another valid PE image embedded at file offset `0x25000`. This embedded image contains the .NET metadata signature `BSJB`, so I extracted it and decompiled it as the managed assembly.

The decompiled assembly only had one important application class:

```text
Cr4ckM3.MainWindow
```

## Activation Handler

The activation button is wired to `MainWindow.F04`. The relevant decompiled logic is:

```csharp
private void F04(object sender, RoutedEventArgs e)
{
    string username = V03.Text;
    string enteredKey = V04.Text.Trim().ToUpper();

    if (username.Length < 6)
    {
        MessageBox.Show("Username must be at least 6 characters long.", "Error", ...);
        return;
    }

    string expectedKey = F06(username);

    if (enteredKey == expectedKey)
        MessageBox.Show("Activation successful!", "Success", ...);
    else
        MessageBox.Show("The product key you entered didn't work. Check the key and try again.",
                        "Activation Error", ...);
}
```

So the only real check is:

```text
entered_key == F06(username)
```

## Key Formatting

The product-key textbox has a text-changed handler, `F07`, that strips dashes, uppercases the input, limits it to 25 characters, and reinserts dashes every five characters.

Simplified:

```csharp
text = V04.Text.Replace("-", "").ToUpper();
if (text.Length > 25)
    text = text.Substring(0, 25);

for (int i = 0; i < text.Length; i++)
{
    if (i > 0 && i % 5 == 0)
        output.Append("-");
    output.Append(text[i]);
}
```

This confirms the expected key shape is:

```text
XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
```

## Key Generation

The key-generation routine is `MainWindow.F06`.

Simplified pseudocode:

```csharp
private string F06(string username)
{
    byte[] data = SHA256.Create().ComputeHash(Encoding.UTF8.GetBytes(username));

    for (int i = 0; i < data.Length; i++)
        data[i] = subst[data[i]];

    StringBuilder encoded = new StringBuilder();
    int bitBuffer = 0;
    int bitCount = 0;

    foreach (byte b in data)
    {
        bitBuffer = (bitBuffer << 8) | b;
        bitCount += 8;

        while (bitCount >= 5)
        {
            bitCount -= 5;
            encoded.Append("ABCDEFGHJKLMNPQRSTUVWXYZ23456789"[(bitBuffer >> bitCount) & 0x1F]);
        }
    }

    if (bitCount > 0)
        encoded.Append("ABCDEFGHJKLMNPQRSTUVWXYZ23456789"[(bitBuffer << (5 - bitCount)) & 0x1F]);

    string raw = encoded.ToString().Substring(0, 25);
    return raw.Substring(0, 5) + "-" +
           raw.Substring(5, 5) + "-" +
           raw.Substring(10, 5) + "-" +
           raw.Substring(15, 5) + "-" +
           raw.Substring(20, 5);
}
```

The custom alphabet intentionally omits ambiguous characters:

```text
ABCDEFGHJKLMNPQRSTUVWXYZ23456789
```

The 256-byte substitution table is stored in `<PrivateImplementationDetails>` as static IL data and loaded into the `V01` field with `RuntimeHelpers.InitializeArray`.

## Keygen

The recovered algorithm was implemented in Python:

```python
#!/usr/bin/env python3
import argparse
import hashlib

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

SUBST = bytes([
    0x0f, 0x9d, 0xad, 0x16, 0x79, 0xcf, 0x76, 0x94,
    0xc0, 0xf3, 0xf2, 0x51, 0x8f, 0xf6, 0x2b, 0x71,
    0xe0, 0xe7, 0x98, 0x53, 0x37, 0x1d, 0x5b, 0xa3,
    0xa2, 0x64, 0x89, 0xcb, 0xab, 0x39, 0xea, 0xf4,
    0x4f, 0x3e, 0x1c, 0xd1, 0x11, 0x92, 0xc4, 0xaf,
    0xa1, 0x9a, 0xe3, 0x7e, 0x52, 0xa0, 0xc9, 0x43,
    0x0e, 0xe8, 0x1f, 0xca, 0x97, 0x70, 0xa7, 0xce,
    0x50, 0xd2, 0x66, 0xf7, 0x24, 0x1e, 0x74, 0xed,
    0x08, 0x86, 0xac, 0x2d, 0x0b, 0xdf, 0x7d, 0x73,
    0xfb, 0xd3, 0x30, 0x40, 0x3c, 0x90, 0x03, 0x6f,
    0xcd, 0xa5, 0xa9, 0x5c, 0xba, 0x3f, 0x6c, 0x4b,
    0xb2, 0x60, 0x14, 0xe4, 0x5d, 0x81, 0x6d, 0x87,
    0xef, 0x85, 0xd5, 0x84, 0x3b, 0x68, 0x0d, 0x82,
    0xf0, 0xe9, 0x25, 0x48, 0x7a, 0x95, 0x41, 0xb5,
    0xb6, 0x8e, 0x96, 0x06, 0x20, 0x33, 0xfc, 0xb7,
    0x58, 0x3d, 0xf8, 0x45, 0x36, 0xd6, 0xf5, 0x65,
    0xe1, 0x10, 0xb1, 0xa4, 0x69, 0xbb, 0x23, 0xaa,
    0x5a, 0x4c, 0x7f, 0xda, 0x47, 0xc7, 0xee, 0x2f,
    0xf9, 0x57, 0xd8, 0x80, 0x4e, 0x46, 0x09, 0x4a,
    0xc8, 0x32, 0xb0, 0x26, 0xe6, 0x2a, 0xf1, 0xeb,
    0x7c, 0xc1, 0xdd, 0x22, 0x35, 0x17, 0xd4, 0x19,
    0x7b, 0xbc, 0x9b, 0xb3, 0x6b, 0xb8, 0xfa, 0xdb,
    0x15, 0x49, 0xc5, 0x9c, 0x05, 0xc6, 0x72, 0x63,
    0x55, 0xa8, 0x38, 0x99, 0x12, 0x31, 0x13, 0x88,
    0x44, 0xde, 0x04, 0x56, 0x91, 0xfe, 0x6e, 0x75,
    0x42, 0x02, 0x07, 0x54, 0x8b, 0xbd, 0x9f, 0x28,
    0x5e, 0x18, 0x77, 0xb4, 0x2e, 0xe5, 0x3a, 0x4d,
    0x78, 0xd0, 0x21, 0xdc, 0xd9, 0x62, 0x27, 0xe2,
    0x29, 0x8d, 0xbe, 0x01, 0xcc, 0x93, 0x67, 0x2c,
    0x8a, 0xc2, 0x0a, 0x1a, 0x0c, 0x5f, 0xb9, 0x00,
    0x61, 0xc3, 0xbf, 0x9e, 0xd7, 0xfd, 0x34, 0x83,
    0x59, 0xae, 0x1b, 0x8c, 0xff, 0x6a, 0xa6, 0xec,
])

def generate_key(username):
    digest = bytearray(hashlib.sha256(username.encode("utf-8")).digest())
    for i, value in enumerate(digest):
        digest[i] = SUBST[value]

    chars = []
    bit_buffer = 0
    bit_count = 0

    for value in digest:
        bit_buffer = ((bit_buffer << 8) | value) & 0xFFFFFFFF
        bit_count += 8
        while bit_count >= 5:
            bit_count -= 5
            chars.append(ALPHABET[(bit_buffer >> bit_count) & 0x1F])

    if bit_count > 0:
        chars.append(ALPHABET[((bit_buffer << (5 - bit_count)) & 0xFFFFFFFF) & 0x1F])

    raw = "".join(chars)[:25]
    return "-".join(raw[i:i + 5] for i in range(0, 25, 5))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cr4ckM3 key generator")
    parser.add_argument("username")
    args = parser.parse_args()

    if len(args.username) < 6:
        raise SystemExit("username must be at least 6 characters")

    print(generate_key(args.username))
```

## Validation

Running the keygen:

```bash
python3 keygen.py singularity
```

produces:

```text
SYAB7-VTAWQ-H9AAR-4N2C8-YV2HD
```

Another example:

```bash
python3 keygen.py WindowsUser
```

produces:

```text
9QE38-AND8V-H6YUQ-7MN28-JEFVK
```

These keys match the format produced and checked by the application: uppercase custom base32, 25 significant characters, grouped with dashes every five characters.

## Final Answer

For username:

```text
singularity
```

the valid activation key is:

```text
SYAB7-VTAWQ-H9AAR-4N2C8-YV2HD
```

The included `keygen.py` can generate a valid key for any username of at least six characters.
