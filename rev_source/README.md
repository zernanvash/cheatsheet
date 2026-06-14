# Reverse Engineering Source Inventory

Local source material used to improve the reverse engineering guide. These are retained for later review, but the main guide generalizes the techniques instead of copying challenge-specific solve paths.

## Local Notes

- `bitmap.md` - PBM/bitmap bit recovery, magic division constants, row/column mapping, and reversing generated visual output back to bytes.
- `NMTE-4667.md` - optimized matrix multiplication disguised as another domain, static equation extraction, pseudoinverse reasoning, and Z3 fallback.
- `restlessness.md` - staged shell-script and macOS artifact deobfuscation, XML entity cleanup, aliases, Base64/hex/ROT/rev pipelines, plist/mobileconfig inspection, launch daemon persistence, and red-herring handling.
- `writeip_my-favorite-ingredient.md` - static solving when execution fails due unsupported CPU instructions, encoded matrix/target extraction, and modulo-byte Z3 solving.
- `links.txt` - external reverse engineering writeups and tools queued for local mining.

## Linked Page Snapshots

Downloaded snapshots are stored in `linked_pages/` for offline reading. Medium blocked direct download, so that source is not mirrored here.

Generalized techniques extracted:

- PyInstaller extraction, `.pyc` version matching, Pyarmor deobfuscation, and disassembly-first recovery.
- Anti-debug bypasses such as `TracerPid` checks and state-function hit counting with batch GDB.
- VM/state-machine lifting into readable traces, pseudo-assembly, equations, and graph constraints.
- Graph/path solving from transition tables.
- Game-console and unusual architecture reversing by focusing on memory layout, palettes, and emulator-friendly state.
- Android/JAR/Flutter direction: decompile managed layers first, then inspect native/framework-specific assets.
- Specialized tooling references: `sohps`, `blutter`, and `Scalpel`.

## Usage

Start with [Reverse Engineering Blueprint](../blueprints/Reverse%20Engineering%20Blueprint.md). Open these source files only when you want to study a solved example behind a generalized technique.
