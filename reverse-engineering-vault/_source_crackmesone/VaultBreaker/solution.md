## Call Path: `main` → `CheckPassword`

Challenge_URL: https://crackmes.one/crackme/69fba1198fab7bbca27300f2

```
main()  [0x103520]
  └─ MainWindow::MainWindow()  [0x103d10]
       └─ QObject::connectImpl(QPushButton::clicked → OnUnlockClicked)
            └─ QObject::connectImpl(QLineEdit::returnPressed → OnUnlockClicked)

[user clicks UNLOCK]
  └─ MainWindow::OnUnlockClicked()  [0x103a50]
       ├─ QLineEdit::text()          ← reads user input
       └─ MainWindow::CheckPassword()  [0x1038a0]
```

`main` creates a `QApplication` and a `MainWindow`, then enters the Qt event loop. The constructor at `0x103d10` wires both the button's `clicked` signal and the line-edit's `returnPressed` signal to the same slot — `OnUnlockClicked` — via `QObject::connectImpl`. When triggered, `OnUnlockClicked` reads the line-edit text and passes it to `CheckPassword`, displaying `"VAULT OPENED"` (green) or `"INVALID ACCESS CODE"` (red) depending on the result.

---

## CheckPassword Decompiled (`0x1038a0`)

```c
ulong MainWindow::CheckPassword(MainWindow *this, QString *input)
{
    // 1. Reject anything that isn't exactly 10 chars
    if (*(long *)(input + 0x10) != 10)
        return 0;

    // 2. Allocate a 10-byte working buffer
    QByteArray decoded(10, '\0');

    // 3. XOR-decode the compile-time constant table
    for (long i = 0; i < 10; i++) {
        byte enc = kEncoded[i];          // read one encoded byte
        decoded[i] = enc ^ 0x5a;         // XOR with the fixed key
    }

    // 4. Convert user input to UTF-8 and compare
    QByteArray utf8 = input->toUtf8();
    if (utf8.size() == decoded.size())
        return memcmp(utf8.data(), decoded.data(), decoded.size()) == 0;

    return 0;
}
```

---

## The Encoded Table

`kEncoded` lives in the `.rodata` section at `0x105818` — 10 hard-coded bytes:

| Index | Encoded | Key    | Decoded | Char |
|-------|---------|--------|---------|------|
| 0     | `0x15`  | `0x5a` | `0x4f`  | `O`  |
| 1     | `0x2a`  | `0x5a` | `0x70`  | `p`  |
| 2     | `0x69`  | `0x5a` | `0x33`  | `3`  |
| 3     | `0x34`  | `0x5a` | `0x6e`  | `n`  |
| 4     | `0x09`  | `0x5a` | `0x53`  | `S`  |
| 5     | `0x69`  | `0x5a` | `0x33`  | `3`  |
| 6     | `0x29`  | `0x5a` | `0x73`  | `s`  |
| 7     | `0x3b`  | `0x5a` | `0x61`  | `a`  |
| 8     | `0x37`  | `0x5a` | `0x6d`  | `m`  |
| 9     | `0x3f`  | `0x5a` | `0x65`  | `e`  |

The relevant assembly loop:

```asm
001038f8  LEA   R12, [0x105818]     ; R12 = kEncoded
00103915  MOVZX EBP, byte [R12+RBX] ; load encoded byte
0010393d  XOR   EBP, 0x5a           ; decode it
00103940  MOV   [RAX+RBX], BPL      ; store to buffer
00103944  ADD   RBX, 1
00103948  CMP   RBX, 0xa
0010394c  JNZ   0x103910            ; loop 10 times
```

---

## Solution

```
Op3nS3same
```

Enter this in the access code field and click `[ UNLOCK ]`. The label switches to `"VAULT OPENED"` in green and a message box confirms: *"VAULT UNLOCKED! Congratulations, you cracked it."*
