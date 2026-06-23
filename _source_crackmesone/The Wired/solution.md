# `OpenWiredSource's The Wired`

Challenge_URL: https://crackmes.one/crackme/6a3720828a86e4c2c55254ec

## Program behaviour

with no args :
```bash
$ ./thewired
[-] The Wired is just a higher field of reality
```
with some args :
```bash
$ ./thewired flag
[-] Incorrect Password
```

Also program creates .png file in current directory. On picture we can see anime character Lain from "Experiments Lain"

```bash 
.rw-r--r-- 178k xxxxxxx 21 jun 08:36  lain_is_here.png
.rwxr-xr-x 193k xxxxxxx 20 jun 23:21 󰡯 thewired
```
## File analysis

```bash
$ file ./thewired
./thewired: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2ca7c393b9364ef1416bc0ee12a343701fb9658e, for GNU/Linux 3.2.0, stripped
```
Runned with ltrace :
```bash
$ ltrace ./thewired flag
fopen("lain_is_here.png", "wb")                         = 0x55fa168b8010 
fwrite("\211PNG\r\n\032\n", 1, 177508, 0x55fa168b8010)  = 177508
fclose(0x55fa168b8010)                                  = 0
strcmp("flag", "we_all_love_serial_experiments_l"...)   = -17
puts("[-] Incorrect Password"[-] Incorrect Password)    = 23
+++ exited (status 0) +++
```

If we look at `strcmp()`, there it is! Flag is `we_all_love_serial_experiments_l...` , that i suppose expands to `we_all_love_serial_experiments_lain`.

```bash
$ ./thewired we_all_love_serial_experiments_lain
================================
          THE WIRED
================================

ACCESS GRANTED

Welcome to The Wired.

Everyone is connected.

[ONLINE]
```

I think there more than 1 way to do this, but im too newbie for ts.
Peace all, thx to **OpenWiredSource** for this crackme! Hope we will meet again on crackme`s.one.

