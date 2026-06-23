# razkom_v1.1 by [RAZKOM](https://crackmes.one/user/RAZKOM) - [\[url\]](https://crackmes.one/crackme/69968b7589af4192123d7aad)

Difficulty: 2.0

Language: C/C++

Platform: Windows

Arch: x86-64

---

Description:

Goal: Reverse engineer the key validation algorithm and either find a valid key
manually or write a keygen. Patching the binary will not reveal the secret
message — a valid key is required to decrypt it.

Instructions: Run razkom_v1.exe, enter a key at the prompt when asked. A correct
key will decrypt and display a hidden message. See HINT.txt for the key format.
No installation required.

Dependencies: None. Standalone Windows x64 executable.

EDIT: Any valid key will be accepted, but only the original key will decrypt the
secret message correctly. Patching or keygen alone won't get you there — you
need to fully understand the algorithm.

---

Files:

- [README.txt](./files/README.txt) - challenge info
- [HINT.txt](./files/HINT.txt) - flag format
- [razkom_v1.1.exe](./files/razkom_v1.1.exe) - executable

---

## Running the Executable

```sh
> wine razkom_v1.1.exe

  [ CrackMe v1 by RAZKOM ]
  -------------------------------------------------------
  Find a valid key to decrypt the secret message.
  Enter key: test
  [-] Invalid key.
```

---

## Program Analysis

`Note: IDA Pro was used to deassemble the program`

The program first verifies that the flag is of the correct format:

```c
while ( 1 )
{
  v7 = GetStdHandle(0xFFFFFFF5);
  SetConsoleTextAttribute(v7, 0xEu);
  sub_140001020("  Enter key: ");
  v8 = GetStdHandle(0xFFFFFFF5);
  SetConsoleTextAttribute(v8, 7u);
  sub_140001080("%63s");
  if ( strlen(Str) == 23
    && Str[3] == 45
    && Str[7] == 45
    && Str[11] == 45
    && Str[15] == 45
    && Str[19] == 45
    && (unsigned __int8)sub_1400010E0(Str) )
  {
    break;
  }
```

Apart from the specified flag format, the program checks the input against
`sub_1400010E0`, which must return `1` in EAX to pass the check:

```c
result = strlen(a1) == 23   // string must be 23 chars long
      && (v2 = a1[2], (*a1 + a1[1]) % 26 + 65 == v2) // a1[0]+a1[1] % 26 + 65 == a1[2]
      && (_BYTE)v2 == 82    // a1[2] == 'R'
      && (v3 = a1[6], (a1[4] + a1[5]) % 26 + 65 == v3) // a1[4]+a1[5] % 26 + 65 == a1[6]
      && (_BYTE)v3 == 65    // a1[6] == 'A'
      && (v4 = a1[10], (a1[8] + a1[9]) % 26 + 65 == v4) // a1[8]+a1[9] % 26 + 65 == a1[10]
      && (_BYTE)v4 == 90    // a1[10] == 'Z'
      && (v5 = a1[14], (a1[12] + a1[13]) % 26 + 65 == v5) // a1[12]+a1[13] % 26 + 65 == a1[14]
      && (_BYTE)v5 == 75    // a1[14] == 'K'
      && (v6 = a1[18], (a1[16] + a1[17]) % 26 + 65 == v6) // a1[16]+a1[17] % 26 + 65 == a1[18]
      && (_BYTE)v6 == 79    // a1[18] == 'O'
      && (v7 = a1[22], (a1[20] + a1[21]) % 26 + 65 == v7) // a1[20]+a1[21] % 26 + 65 == a1[22]
      && (_BYTE)v7 == 77;   // a1[22] == 'M'
return result;
```

Just to verify, we can easily generate all key possibilities with a C script:

```c
#include <stdio.h>
#include <string.h>

void get_all_valid(char a) {
    static char* alp = "QWERTYUIOPASDFGHJKLZXCVBNM";

    for (int i = 0; i < strlen(alp); i++)
        for (int j = 0; j < strlen(alp); j++)
            if ((alp[i] + alp[j]) % 26 + 65 == a)
                printf("%c%c ", alp[i], alp[j]);
}

int main() {
    static char* s = "RAZKOM";

    for (int i = 0; i < 6; i++) {
        get_all_valid(s[i]);
        printf("\n\n");
    }

    return 0;
}
```

```sh
> gcc keygen_format.c -o keygen_format
> ./keygen_format
QB WV EN RA TY YT UX IJ OD PC AR SZ DO FM GL HK JI KH LG ZS XU CP VW BQ NE MF

QK WE EW RJ TH YC UG IS OM PL AA SI DX FV GU HT JR KQ LP ZB XD CY VF BZ NN MO

QJ WD EV RI TG YB UF IR OL PK AZ SH DW FU GT HS JQ KP LO ZA XC CX VE BY NM MN

QU WO EG RT TR YM UQ IC OW PV AK SS DH FF GE HD JB KA LZ ZL XN CI VP BJ NX MY

QY WS EK RX TV YQ UU IG OA PZ AO SW DL FJ GI HH JF KE LD ZP XR CM VT BN NB MC

QW WQ EI RV TT YO US IE OY PX AM SU DJ FH GG HF JD KC LB ZN XP CK VR BL NZ MA
```

Hence, one viable flag is `QBR-QKA-QJZ-QUK-QYO-QWM`:

```sh
> wine razkom_v1.1.exe
  [ CrackMe v1 by RAZKOM ]
  -------------------------------------------------------
  Find a valid key to decrypt the secret message.
  Enter key: QBR-QKA-QJZ-QUK-QYO-QWM

  [+] Key accepted! Decrypting...

  @lngbktugjtiuzs!Aou<eooued0gy mbrsn4cr{kmy8
Soeaco ln m4knqo wtwt#zou0~ho~lht:{f wl ir6tkf cgmees.Gecl}t kyrg9 'RKZOD@A'
```

Great! Now we just need to find the right combination of these key fragments.

The flag is decrypted using a simple XOR against the key:

```c
  do
  {
    sub_140001020("%c", byte_140003330[v12] ^ (unsigned int)Str[(unsigned int)v12 % 0x17]);
    v12 = (unsigned int)(v12 + 1);
  }
  while ( (int)v12 < 127 );
```

The `byte_140003330` points to the encrypted data block:

```
byte_140003330  db 11h, 2Eh, 3Ch, 4Ah, 33h, 20h, 35h, 58h, 36h, 20h, 2Eh
                db 44h, 24h, 2Fh, 38h, 0Ch, 45h, 18h, 20h, 58h, 6Dh, 32h
                db 22h, 3Eh, 2 dup(37h), 49h, 61h, 2Ch, 38h, 0Dh, 3Ch
                db 2 dup(28h), 5Eh, 3Fh, 61h, 28h, 5Fh, 2Eh, 22h, 24h
                db 40h, 28h, 6Fh, 47h, 2, 2Dh, 37h, 4Ch, 32h, 24h, 61h
                db 41h, 3Fh, 35h, 7Ah, 40h, 2Eh, 61h, 20h, 43h, 20h, 36h
                db 6Fh, 5Ah, 25h, 20h, 39h, 72h, 38h, 3Dh, 58h, 61h, 35h
                db 29h, 42h, 2Fh, 26h, 32h, 59h, 6Bh, 2Eh, 2Dh, 0Dh, 26h
                db 35h, 6Fh, 44h, 23h, 61h, 39h, 3Ah, 24h, 72h, 4Eh, 2Eh
                db 2 dup(2Ch), 48h, 34h, 35h, 29h, 3, 41h, 12h, 2Eh, 4Eh
                db 3Dh, 24h, 3Bh, 0Dh, 3Ah, 2Eh, 3Fh, 36h, 7Bh, 72h, 0Ah
                db 3, 0, 1Bh, 62h, 15h, 0Ah, 1Bh, 0Ah, 4Bh, 52h, 41h, 5Ah
                db 4Bh, 4Fh, 4Dh, 0Ah dup(0)
```

There appears to be no more useful data.

---

## Program Summary

The program takes a key as input, validates it to be of the following format:

`XYZ-XYZ-XYZ-XYZ-XYZ-XYZ`, where `Z` are `"RAZKOM"` letters and `X` and `Y`
follow a pattern: `(X + Y) % 26 + 65 == Z`.

Once the key is validated, it is used to decrypt the flag by XOR.

---

## Keygen

The simplest way to solve this challenge is by checking all possible key
combinations for each block of data (there are only 26). For that I wrote this
simple C program:

```c
#include <stdio.h>
#include <string.h>

int main() {
    const unsigned char ciphertext[] =
        "\x11\x2E\x3C\x4A\x33\x20\x35\x58\x36\x20\x2E"
        "\x44\x24\x2F\x38\x0C\x45\x18\x20\x58\x6D\x32"
        "\x22\x3E\x37\x37\x49\x61\x2C\x38\x0D\x3C"
        "\x28\x28\x5E\x3F\x61\x28\x5F\x2E\x22\x24"
        "\x40\x28\x6F\x47\x02\x2D\x37\x4C\x32\x24\x61"
        "\x41\x3F\x35\x7A\x40\x2E\x61\x20\x43\x20\x36"
        "\x6F\x5A\x25\x20\x39\x72\x38\x3D\x58\x61\x35"
        "\x29\x42\x2F\x26\x32\x59\x6B\x2E\x2D\x0D\x26"
        "\x35\x6F\x44\x23\x61\x39\x3A\x24\x72\x4E\x2E"
        "\x2C\x2C\x48\x34\x35\x29\x03\x41\x12\x2E\x4E"
        "\x3D\x24\x3B\x0D\x3A\x2E\x3F\x36\x7B\x72\x0A"
        "\x03\x00\x1B\x62\x15\x0A\x1B\x0A\x4B\x52\x41\x5A"
        "\x4B\x4F\x4D"
        "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00";

    const char *key_formats[6][26] = {
        { "QB","WV","EN","RA","TY","YT","UX","IJ","OD","PC","AR","SZ","DO","FM","GL","HK","JI","KH","LG","ZS","XU","CP","VW","BQ","NE","MF" },
        { "QK","WE","EW","RJ","TH","YC","UG","IS","OM","PL","AA","SI","DX","FV","GU","HT","JR","KQ","LP","ZB","XD","CY","VF","BZ","NN","MO" },
        { "QJ","WD","EV","RI","TG","YB","UF","IR","OL","PK","AZ","SH","DW","FU","GT","HS","JQ","KP","LO","ZA","XC","CX","VE","BY","NM","MN" },
        { "QU","WO","EG","RT","TR","YM","UQ","IC","OW","PV","AK","SS","DH","FF","GE","HD","JB","KA","LZ","ZL","XN","CI","VP","BJ","NX","MY" },
        { "QY","WS","EK","RX","TV","YQ","UU","IG","OA","PZ","AO","SW","DL","FJ","GI","HH","JF","KE","LD","ZP","XR","CM","VT","BN","NB","MC" },
        { "QW","WQ","EI","RV","TT","YO","US","IE","OY","PX","AM","SU","DJ","FH","GG","HF","JD","KC","LB","ZN","XP","CK","VR","BL","NZ","MA" }
    };

    char keys[26][24];

    for (int i = 0; i < 26; i++) {
        for (int j = 0; j < 6; j++) {
            int k = j * 4;

            keys[i][k + 0] = key_formats[j][i][0];
            keys[i][k + 1] = key_formats[j][i][1];
        }

        keys[i][2]  = 'R';
        keys[i][6]  = 'A';
        keys[i][10] = 'Z';
        keys[i][14] = 'K';
        keys[i][18] = 'O';
        keys[i][22] = 'M';

        keys[i][3]  = '-';
        keys[i][7]  = '-';
        keys[i][11] = '-';
        keys[i][15] = '-';
        keys[i][19] = '-';

        keys[i][23] = 0;
    }

    int len = sizeof(ciphertext) - 1;
    for (int i = 0; i < 26; i++) {
        printf("%s\n", keys[i]);

        for (int j = 0; j <len; j++)
            printf("%c", ciphertext[j] ^ keys[i][j % 24]);

        printf("\n\n\n");
    }

    return 0;
}
```

Essentially, it just decrypts the ciphertext by each of the possible key
fragments. Now we only need to see which produce a valid plaintext:

```
RAR-RJA-RIZ-RTK-RXO-RVM
Congajtuditiv{s!@ou?do>evL~rLza3|p|=O-e

ARR-AAA-AZZ-AKK-AOO-AMM
P|ngratuwztieds!Wou,o>veLmyLir cck.

ZSR-ZBA-ZAZ-ZLK-ZPO-ZNM
K}ngibtulati~cs!Hou7|o>mdLvzLri;dxt5	O-m

KHR-KQA-KPZ-KAK-KEO-KCM
Zfngxqtu}ptions!]ou&qo>|LgiLcx

ODR-OMA-OLZ-OWK-OAO-OYM
^jng|mtuyltikxs!
You"ko>xsLcuL
```

Here we could notice:

```
"RAR" produces "Con..."
"-" produces "g"
"AAA" produces "rat..."
"-" produces "u"
"ZAZ" produces "lat..."
"-" produces "i"
"KAK" produces "ons"
"-" produces "!"
"OAO" produces "\nYo"
"-" produces "u"
```

Clearly the first word of the output is "Congratulations", and hence I was able
to easily identify 5 of the 6 key blocks:

`RAR-AAA-ZAZ-KAK-OAO-...`

The last key fragment is a bit unclear from that alone, but we could easily just
generate all 26 possibilities:

```c
#include <stdio.h>
#include <string.h>

int main() {
    const char ciphertext[] =
        "\x11\x2E\x3C\x4A\x33\x20\x35\x58\x36\x20\x2E"
        "\x44\x24\x2F\x38\x0C\x45\x18\x20\x58\x6D\x32"
        "\x22\x3E\x37\x37\x49\x61\x2C\x38\x0D\x3C"
        "\x28\x28\x5E\x3F\x61\x28\x5F\x2E\x22\x24"
        "\x40\x28\x6F\x47\x02\x2D\x37\x4C\x32\x24\x61"
        "\x41\x3F\x35\x7A\x40\x2E\x61\x20\x43\x20\x36"
        "\x6F\x5A\x25\x20\x39\x72\x38\x3D\x58\x61\x35"
        "\x29\x42\x2F\x26\x32\x59\x6B\x2E\x2D\x0D\x26"
        "\x35\x6F\x44\x23\x61\x39\x3A\x24\x72\x4E\x2E"
        "\x2C\x2C\x48\x34\x35\x29\x03\x41\x12\x2E\x4E"
        "\x3D\x24\x3B\x0D\x3A\x2E\x3F\x36\x7B\x72\x0A"
        "\x03\x00\x1B\x62\x15\x0A\x1B\x0A\x4B\x52\x41\x5A"
        "\x4B\x4F\x4D"
        "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00";

    char *key_formats[26] =
        { "QW","WQ","EI","RV","TT","YO","US","IE","OY","PX","AM","SU","DJ","FH","GG","HF","JD","KC","LB","ZN","XP","CK","VR","BL","NZ","MA" };

    char key[23] = "RAR-AAA-ZAZ-KAK-OAO-XXM";

    int len = sizeof(ciphertext) - 1;

    for (int i = 0; i < 26; i++) {
        key[20] = key_formats[i][0];
        key[21] = key_formats[i][1];

        printf("%s\n", key);

        for (int j = 0; j <len; j++)
            printf("%c", ciphertext[j] ^ key[j % 23]);

        printf("\n\n\n");
    }

    return 0;
}
```

And this reveals the decoded message, as well as the final key fragment:

```
RAR-AAA-ZAZ-KAK-OAO-MAM
Congratulations!
You solved my first crackme.
Please let me know what you thought of it in the comments.
Secret word: 'BAZOOKA'
```

To verify, let's test the key against the program itself:

```sh
> wine files/razkom_v1.1.exe

  [ CrackMe v1 by RAZKOM ]
  -------------------------------------------------------
  Find a valid key to decrypt the secret message.
  Enter key: RAR-AAA-ZAZ-KAK-OAO-MAM

  [+] Key accepted! Decrypting...

  Congratulations!
You solved my first crackme.
Please let me know what you thought of it in the comments.
Secret word: 'BAZOOKA'
```

---

[Back to home](./../crackmes.md)
