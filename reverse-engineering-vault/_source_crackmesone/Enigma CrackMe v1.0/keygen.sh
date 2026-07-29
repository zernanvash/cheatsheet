#!/usr/bin/env bash
# Usage: ./keygen.sh "Name"
NAME="${1:-Alice}"
LEN=${#NAME}
BIN="$(dirname "$0")/enigma_crackme.exe"

cat > /tmp/keygen.gdb << EOF
set pagination off
b main
run
set \$k = (unsigned int)derive_key("$NAME", $LEN)
set \$c0 = (unsigned int)((unsigned long long)transform(\$k) & 0xffff)
set \$c1 = (unsigned int)((unsigned long long)transform(\$k ^ 0xa5a5a5a5) & 0xffff)
set \$c2 = (unsigned int)((unsigned long long)transform(\$k ^ \$c0) & 0xffff)
set \$c3 = (\$c0 ^ \$c1 ^ \$c2) & 0xffff
printf "%04X-%04X-%04X-%04X\n", \$c0, \$c1, \$c2, \$c3
quit
EOF

gdb -q "$BIN" < /tmp/keygen.gdb 2>/dev/null | tr -d '\r' | grep -oE '[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}'
