# Vim For Reversing Cheat Sheet

Use Vim to inspect decompiled code, clean payload scripts, compare solver output, and edit notes quickly during reverse engineering.

## Open And Navigate

```bash
vim file.txt
vim -R suspicious_script.sh
vim +120 file.txt
vim +'set ft=asm' dump.asm
```

Inside Vim:

| Key | Action |
|---|---|
| `h j k l` | move left/down/up/right |
| `gg` | top of file |
| `G` | end of file |
| `:120` | go to line 120 |
| `Ctrl-f` | page down |
| `Ctrl-b` | page up |
| `%` | jump between matching braces/parentheses |
| `zz` | center current line |

## Search

```vim
/flag
/strcmp
/0x401234
?main
n
N
```

Useful settings:

```vim
:set ignorecase smartcase
:set hlsearch
:nohlsearch
```

Search for hex-looking values:

```vim
/\v0x[0-9a-fA-F]+
```

Search for Base64-like blobs:

```vim
/\v[A-Za-z0-9+\/=]{30,}
```

## Editing Decompiled Code Or Scripts

| Command | Action |
|---|---|
| `i` | insert before cursor |
| `a` | insert after cursor |
| `Esc` | normal mode |
| `dd` | delete line |
| `yy` | copy line |
| `p` | paste after cursor |
| `u` | undo |
| `Ctrl-r` | redo |
| `ci"` | change inside quotes |
| `ci'` | change inside single quotes |
| `ci(` | change inside parentheses |
| `di{` | delete inside braces |

## Visual Selection

| Key | Action |
|---|---|
| `v` | character visual mode |
| `V` | line visual mode |
| `Ctrl-v` | block visual mode |
| `y` | yank selected text |
| `d` | delete selected text |
| `>` / `<` | indent / unindent |

Block insert for commenting/uncommenting columns:

```vim
Ctrl-v
j/k to select lines
I#
Esc
```

## Replace And Cleanup

Replace first match on each line:

```vim
:%s/old/new/
```

Replace all matches:

```vim
:%s/old/new/g
```

Remove carriage returns:

```vim
:%s/\r//g
```

Decode XML entities manually:

```vim
:%s/&amp;/\&/g
:%s/&gt;/>/g
:%s/&lt;/</g
```

Remove trailing whitespace:

```vim
:%s/\s\+$//e
```

Join minified split lines:

```vim
J
gJ
```

Reindent code:

```vim
gg=G
```

## Buffers, Splits, And Diff

```vim
:e other_file
:bn
:bp
:ls
:split other_file
:vsplit other_file
Ctrl-w h/j/k/l
```

Diff two files:

```bash
vimdiff original.py deobfuscated.py
```

Inside diff:

```vim
]c
[c
do
dp
```

## Read Command Output Into File

```vim
:r !strings -n 8 ./challenge
:r !objdump -M intel -d ./challenge
:r !python solve.py
```

Filter selected text through a command:

```vim
:'<,'>!base64 -d
:'<,'>!xxd -r -p
```

## Hex Editing With xxd

Open as hex:

```bash
vim -b sample.bin
```

Inside Vim:

```vim
:%!xxd
```

After editing hex bytes, convert back:

```vim
:%!xxd -r
:w patched.bin
```

Use this for small patches only. For larger binary patches, prefer Python or a dedicated hex editor.

## Folding Large Decompiled Files

```vim
:set foldmethod=indent
za
zM
zR
```

## Useful Settings

```vim
:set number
:set relativenumber
:set nowrap
:set list
:set tabstop=4 shiftwidth=4 expandtab
:syntax on
```

## Related

- [Reverse Engineering Playbook](../Reverse%20Engineering%20Playbook.md)
- [Reversing CLI Tools Cheat Sheet](Reversing%20CLI%20Tools%20Cheat%20Sheet.md)
- [Linux Text Processing](Linux%20Text%20Processing.md)
