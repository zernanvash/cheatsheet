# crackit Writeup

# WRITEUP crackit

The description show us a good information:
"It is actually a python script compiled by Pyinstaller."

Ok you need to extract python files from the binary.

We will use pyinstxtractor ( https://github.com/extremecoders-re/pyinstxtractor.git)

Like explain on git page, we need to run pyinstxtractor.py on the binary:

---
✓ snorky@archlinux:~/reverse/crackones.me/crackit2$ python3 pyinstxtractor/pyinstxtractor.py crackit
[+] Processing crackit
[+] Pyinstaller version: 2.1+
[+] Python version: 3.14
[+] Length of package: 8783119 bytes
[+] Found 54 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: crackit.pyc
[+] Found 130 files in PYZ archive
[+] Successfully extracted pyinstaller archive: crackit

You can now use a python decompiler on the pyc files within the extracted directory
---


A directory is just created (crackit_extracted):
---
✓ snorky@archlinux:~/reverse/crackones.me/crackit2$ ls
69a65b6c7a778cfffbfb680e.zip  crackit  crackit_extracted  pyinstxtractor
---


List what the directory contain, and we can find a crackit.pyc:
---
✓ snorky@archlinux:~/reverse/crackones.me/crackit2$ ls crackit_extracted/
PYZ.pyz            libbz2.so.1           libssl.so.3          pyiboot01_bootstrap.pyc  python3.14
PYZ.pyz_extracted  libcrypto.so.3        libz.so.1            pyimod01_archive.pyc     struct.pyc
base_library.zip   liblzma.so.5          libzstd.so.1         pyimod02_importers.pyc
crackit.pyc        libpython3.14.so.1.0  pyi_rth_inspect.pyc  pyimod03_ctypes.pyc
---

Run a hexdump -C on binary and we found the key:
---
✓ snorky@archlinux:~/reverse/crackones.me/crackit2/crackit_extracted$ hexdump -C crackit.pyc
[...]
00000160  20 63 61 6e 20 64 6f 20  69 74 21 29 09 7a 04 43  | can do it!).z.C|
00000170  54 46 7b da 03 4d 79 5f  da 03 53 33 63 da 04 72  |TF{..My_..S3c..r|
00000180  33 74 5f da 04 46 6c 34  67 7a 04 7d 57 6f 57 da  |3t_..Fl4gz.}WoW.|
00000190  03 59 6f 75 da 05 46 6f  75 6e 64 da 02 4d 65 29  |.You..Found..Me)|
000001a0  09 da 03 73 79 73 da 05  70 61 72 74 73 da 04 6a  |...sys..parts..j|
[...]
---

✓ snorky@archlinux:~/reverse/crackones.me/crackit2$ ./crackit CTF{My_S3cr3t_Fl4g}WoWYouFoundMe
You cracked me!

Thanks for this crackme..
