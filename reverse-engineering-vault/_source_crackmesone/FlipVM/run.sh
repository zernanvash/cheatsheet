#!/usr/bin/env bash
set -euo pipefail
python3 keygen.py
if [[ -f code.flp ]]; then
  python3 patch.py code.flp patched.flp
  echo "patched.flp generated"
else
  echo "Put code.flp in this directory, then run: python3 patch.py code.flp patched.flp"
fi
