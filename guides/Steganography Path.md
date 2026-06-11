# Steganography Path

Workflow for CTF/lab files where data may be hidden in images, audio, archives, metadata, whitespace, or file structure. Start broad and non-destructive, then move into format-specific tools.

## 1. Triage

```bash
file sample
ls -lh sample
sha256sum sample
strings -n 8 sample | head
exiftool sample
binwalk sample
```

Look for:

- wrong file extension
- metadata comments, author fields, GPS, software names
- embedded archives or appended data
- visible artifacts, odd dimensions, alpha channel, unusual color palette
- password hints in challenge text or companion files

## 2. Linux CLI Tools

### General File And Metadata

```bash
file image.png
exiftool image.png
strings -n 8 image.png
xxd image.png | less
binwalk image.png
binwalk -e image.png
foremost image.png
```

Use when the file may contain metadata, appended archives, embedded files, or a misleading extension.

### Image Stego

```bash
zsteg image.png
zsteg -a image.png
steghide info image.jpg
steghide extract -sf image.jpg
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

Use `zsteg` for PNG/BMP bit-plane and channel checks. Use `steghide`/`stegseek` when JPG/WAV files may hide payloads with a passphrase.

### Audio Stego

```bash
file audio.wav
exiftool audio.wav
strings -n 8 audio.wav
binwalk audio.wav
sox audio.wav -n stat
```

Open spectrograms in Audacity or Sonic Visualiser when audio sounds odd, has long silence, or challenge text hints at sound/frequency.

### Whitespace And Text Stego

```bash
cat -A hidden.txt
xxd hidden.txt
stegsnow -C hidden.txt
```

Use when whitespace, line endings, tabs, Morse, zero-width characters, or strange spacing appear.

## 3. Python Script Tools

### Extract Printable Strings From Binary

```python
from pathlib import Path
import re

data = Path("sample").read_bytes()
for s in re.findall(rb"[ -~]{6,}", data):
    print(s.decode(errors="ignore"))
```

### Check PNG RGBA Alpha Channel

```python
from PIL import Image

img = Image.open("image.png").convert("RGBA")
chars = []
for y in range(img.height):
    for x in range(img.width):
        a = img.getpixel((x, y))[3]
        if 32 <= a <= 126:
            chars.append(chr(a))
print("".join(chars))
```

### Extract LSB Bits From Pixels

```python
from PIL import Image

img = Image.open("image.png").convert("RGB")
bits = []
for pixel in img.getdata():
    for channel in pixel:
        bits.append(str(channel & 1))

out = bytearray()
for i in range(0, len(bits), 8):
    byte = int("".join(bits[i:i+8]), 2)
    out.append(byte)

print(out[:500])
```

Try bit order reversal if output is close but unreadable.

### Compare Two Images

```python
from PIL import Image, ImageChops

a = Image.open("a.png").convert("RGB")
b = Image.open("b.png").convert("RGB")
diff = ImageChops.difference(a, b)
diff.save("diff.png")
```

Use when challenge gives an original and modified image.

## 4. Web Tools

Use web tools for visual inspection and quick transforms when local tools are unavailable. Do not upload sensitive real-world files.

- CyberChef: Base64, hex, Morse, XOR, magic, decompression, entropy checks.
- Aperi'Solve: automated image stego triage.
- StegOnline: bit planes, color channels, image browser, LSB extraction.
- dCode: classical ciphers and visual encodings.
- Sonic Visualiser or Audacity locally for spectrograms.

## 5. Decision Branches

### Metadata Hit

If `exiftool` finds a comment, author, password, GPS, or software version:

1. Decode obvious encodings.
2. Try discovered words as steghide/archive passwords.
3. Search the software/version if it implies a known tool chain.

### Embedded File Hit

If `binwalk` or `foremost` extracts files:

1. Run `file` on each extracted file.
2. Check archives for passwords.
3. Use `zip2john`, `rar2john`, or `7z2john` when encrypted.
4. Recurse into extracted images/audio/text.

### Image Bit-Plane Hit

If visual tools show letters in planes/channels:

1. Export the plane.
2. Rotate/invert/adjust contrast if needed.
3. OCR manually or with Python if text is clear.

### Password-Protected Stego

If `steghide info` shows embedded data but asks for a passphrase:

1. Build a candidate list from challenge title, metadata, page text, filenames, and found strings.
2. Try `stegseek` with a scoped wordlist.
3. Extract and triage the recovered file.

## 6. Study Use Cases

- [Steganography examples](../references/Challenge%20Use%20Cases.md#steganography)
- [Cryptography Path](Cryptography%20Path.md)
- [REV Python Toolkit](../tools/REV%20Python%20Toolkit.md)
