"""Build the static writeup database used by writeups.html.

The source mirrors are read-only. This script discovers Markdown beneath every
``_source_*`` directory and writes one deterministic, browser-ready JSON file.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


VAULT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = VAULT_ROOT / "writeups-index.json"

CATEGORIES = (
    "Machine Exploitation",
    "Web Exploitation",
    "PWN / Binary Exploit",
    "Reverse Engineering",
    "Cryptography",
    "Forensics",
    "OSINT",
    "Steganography",
    "General",
)

CATEGORY_HINTS = (
    ("PWN / Binary Exploit", ("binary_exploitation", "binary exploitation", "/pwn/", " pwn ")),
    ("Reverse Engineering", ("reverse_engineering", "reverse engineering", "/rev/", " crackme", "keygen")),
    ("Web Exploitation", ("web_exploitation", "web exploitation", "/web/", " web challenge", " sqli", " xss")),
    ("Cryptography", ("cryptography", "/crypto/", " crypto challenge", " cipher", " rsa ", " aes ")),
    ("Forensics", ("forensics", "/forensic/", " pcap", " volatility")),
    ("OSINT", ("/osint/", " osint", "whois")),
    ("Steganography", ("steganography", "/stego/", " stego", "steghide")),
    ("Machine Exploitation", ("machine exploitation", "boot2root", "privilege escalation", " privesc")),
)

TAG_KEYWORDS = {
    "WordPress": (r"wordpress", r"wp-", r"wpscan"),
    "SQLi": (r"\bsqli\b", r"sql injection", r"sql-injection", r"\bmysql\b", r"\bpostgres\b", r"\bsqlite\b"),
    "LFI": (r"\blfi\b", r"local file inclusion", r"file inclusion"),
    "RCE": (r"\brce\b", r"remote code execution", r"command injection", r"\bexec\s*\("),
    "SSTI": (r"\bssti\b", r"server-side template injection", r"\bjinja2\b"),
    "XXE": (r"\bxxe\b", r"xml external entity"),
    "SSRF": (r"\bssrf\b", r"server-side request forgery"),
    "XSS": (r"\bxss\b", r"cross-site scripting", r"cross site scripting"),
    "CSRF": (r"\bcsrf\b", r"cross-site request forgery"),
    "Directory Traversal": (r"directory traversal", r"path traversal", r"\.\./\.\."),
    "File Upload": (r"file upload", r"upload shell", r"upload bypass"),
    "XOR": (r"\bxor\b", r"exclusive or", r"xor encryption"),
    "RSA": (r"\brsa\b", r"openssl rsautl", r"id_rsa"),
    "AES": (r"\baes\b", r"aes-128", r"aes-256"),
    "Assembly": (r"\bassembly\b", r"\bx86\b", r"\bx64\b", r"\basm\b", r"\bregisters?\b"),
    "IDA Pro": (r"ida pro", r"\bida\b", r"decompiler"),
    "Ghidra": (r"\bghidra\b",),
    "GDB": (r"\bgdb\b", r"gnu debugger"),
    "Keygen": (r"\bkeygen\b", r"key generator", r"key validation"),
    "Patching": (r"\bpatch(?:ing|ed)?\b", r"binary patch"),
    "Obfuscation": (r"obfuscat", r"deobfuscat"),
    "Golang": (r"\bgolang\b", r"go binary", r"go build"),
    "Rust": (r"\brust\b", r"\bcargo\b"),
    ".NET": (r"\.net\b", r"dnspy", r"ilspy", r"\bc#\b", r"\bmono\b"),
    "Anti-Debugging": (r"anti-debug", r"ptrace", r"isdebuggerpresent"),
    "Buffer Overflow": (r"buffer overflow", r"\bbof\b", r"stack overflow"),
    "ROP": (r"rop chain", r"return-oriented", r"\brop\b"),
    "Format String": (r"format string", r"printf\s*\("),
    "Privilege Escalation": (r"privilege escalation", r"\bprivesc\b", r"root access"),
    "Sudo PrivEsc": (r"sudo -l", r"sudoers"),
    "Cronjob PrivEsc": (r"cronjob", r"/etc/crontab"),
    "SUID": (r"\bsuid\b", r"setuid", r"perm -4000"),
    "Active Directory": (r"active directory", r"kerberoast", r"bloodhound", r"domain controller"),
    "Nmap": (r"\bnmap\b", r"port scan"),
    "Reverse Shell": (r"reverse shell", r"revshell", r"bash -i"),
    "SSH": (r"\bssh\b", r"id_rsa", r"authorized_keys"),
    "FTP": (r"\bftp\b", r"anonymous ftp"),
    "SMB": (r"\bsmb\b", r"samba", r"smbclient"),
    "RPC": (r"\brpc\b", r"rpcclient"),
    "NFS": (r"\bnfs\b", r"showmount"),
    "LDAP": (r"\bldap\b",),
    "Redis": (r"\bredis\b", r"redis-cli"),
    "WebDAV": (r"\bwebdav\b",),
    "Tomcat": (r"\btomcat\b",),
    "Jenkins": (r"\bjenkins\b",),
    "Wireshark": (r"\bwireshark\b", r"\bpcap\b", r"\btshark\b"),
    "Volatility": (r"\bvolatility\b",),
    "Steghide": (r"\bsteghide\b",),
    "Binwalk": (r"\bbinwalk\b",),
    "Metadata": (r"\bmetadata\b", r"\bexiftool\b"),
}


def normalize_path(path: Path | str) -> str:
    return str(path).replace("\\", "/").lstrip("./")


def tracked_paths() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=VAULT_ROOT, capture_output=True, check=False
    )
    if result.returncode:
        print("WARNING: git ls-files failed; embedding source Markdown for all records", file=sys.stderr)
        return set()
    return {p.decode("utf-8", "surrogateescape") for p in result.stdout.split(b"\0") if p}


def parse_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    text = markdown.lstrip("\ufeff")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw, body = text[4:end], text[end + 4 :].lstrip("\r\n")
    data: dict[str, object] = {}
    active_list: str | None = None
    for line in raw.splitlines():
        item = re.match(r"^\s*-\s+(.+)$", line)
        if item and active_list:
            cast = data.setdefault(active_list, [])
            if isinstance(cast, list):
                cast.append(item.group(1).strip(" '\""))
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1).lower(), match.group(2).strip()
        active_list = key if not value else None
        if value.startswith("[") and value.endswith("]"):
            data[key] = [part.strip(" '\"") for part in value[1:-1].split(",") if part.strip()]
        else:
            data[key] = value.strip(" '\"")
    return data, body


def headings_from(markdown: str) -> list[str]:
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", markdown, re.MULTILINE)]


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"^---\n.*?\n---\s*", "", markdown, count=1, flags=re.DOTALL)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<https?://[^>]+>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s*```[^\n]*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"[`*_~|>#]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def title_for(path: Path, frontmatter: dict[str, object], headings: list[str]) -> str:
    declared = frontmatter.get("title")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()
    if headings:
        return headings[0]
    return path.stem.replace("_", " ").replace("-", " ").strip() or "Untitled"


def origin_for(relative: str, frontmatter: dict[str, object]) -> str:
    declared = frontmatter.get("origin") or frontmatter.get("platform")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()
    low = f"/{relative.lower()}/"
    if low.startswith("/_source_tryhackme_cajac/") or low.startswith("/_source_0xb0b_tryhackme/") or "/posts/thm/" in low:
        return "TryHackMe"
    if low.startswith("/_source_hackmyvm_writeups/") or "/posts/hackmyvm/" in low:
        return "HackMyVM"
    if low.startswith("/_source_picoctf_cajac/"):
        return "picoCTF"
    if low.startswith("/_source_crackmesone/"):
        return "crackmes.one"
    if low.startswith("/_source_ruycr4ft_cheatsheets/"):
        return "ruycr4ft"
    if low.startswith("/_source_sec_fortress/"):
        if "/posts/htb/" in low:
            return "HackTheBox"
        if "/posts/pg/" in low:
            return "Proving Grounds"
        if "/posts/ptd/" in low:
            return "PwnTillDawn"
        if "/posts/vulnyx/" in low:
            return "Vulnyx"
        return "Sec-Fortress"
    return "Other"


def category_for(relative: str, frontmatter: dict[str, object], title: str, body: str) -> str:
    declared = frontmatter.get("category")
    if isinstance(declared, str):
        normalized = declared.strip().lower()
        aliases = {
            "pwn": "PWN / Binary Exploit", "binary": "PWN / Binary Exploit",
            "binary exploitation": "PWN / Binary Exploit", "rev": "Reverse Engineering",
            "reverse": "Reverse Engineering", "reverse engineering": "Reverse Engineering",
            "web": "Web Exploitation", "web exploitation": "Web Exploitation",
            "crypto": "Cryptography", "cryptography": "Cryptography",
            "forensics": "Forensics", "osint": "OSINT", "stego": "Steganography",
            "steganography": "Steganography", "machine": "Machine Exploitation",
        }
        if normalized in aliases:
            return aliases[normalized]
        if declared in CATEGORIES:
            return declared
    low_path = f"/{relative.lower()}/"
    sample = f" {low_path} {title.lower()} {body[:3000].lower()} "
    for category, hints in CATEGORY_HINTS:
        if any(hint in sample for hint in hints):
            return category
    if low_path.startswith("/_source_crackmesone/"):
        return "Reverse Engineering"
    if low_path.startswith("/_source_hackmyvm_writeups/") or "/posts/hackmyvm/" in low_path:
        return "Machine Exploitation"
    if low_path.startswith("/_source_temperance/"):
        return "Cryptography"
    if "/posts/pg/" in low_path or "/posts/htb/" in low_path or "/posts/thm/" in low_path or "/posts/vulnyx/" in low_path:
        return "Machine Exploitation"
    return "General"


def tags_for(frontmatter: dict[str, object], searchable: str) -> list[str]:
    tags: set[str] = set()
    declared = frontmatter.get("tags")
    if isinstance(declared, str):
        tags.update(x.strip() for x in re.split(r"[, ]+", declared) if x.strip())
    elif isinstance(declared, list):
        tags.update(str(x).strip() for x in declared if str(x).strip())
    for tag, patterns in TAG_KEYWORDS.items():
        if any(re.search(pattern, searchable, re.IGNORECASE) for pattern in patterns):
            tags.add(tag)
    return sorted(tags, key=str.casefold)


def snippet_for(body: str, title: str, category: str, origin: str, tags: list[str]) -> str:
    candidate = body
    if candidate.lower().startswith(title.lower()):
        candidate = candidate[len(title) :].lstrip(" :-—")
    if candidate:
        return candidate[:197].rstrip() + ("..." if len(candidate) > 200 else "")
    focus = f" focusing on {', '.join(tags[:3])}" if tags else ""
    return f"{category} material from {origin}{focus}."


def context_title_for(title: str, relative: str, markdown: str) -> str | None:
    clean = re.sub(r"[*|:]", "", title).strip()
    if not (re.fullmatch(r"0x[0-9a-f]+|\d+", clean, re.IGNORECASE) or len(clean) < 5):
        return None
    low = relative.lower()
    lab = "Venus Lab" if "/venus/" in f"/{low}" else "Hades Lab" if "/hades/" in f"/{low}" else ""
    mission = re.search(r"moving from `?([^`\s]+)`? to `?([^`\s]+)`?", markdown, re.IGNORECASE)
    if mission:
        return f"{lab + ' ' if lab else ''}Mission {clean} ({mission.group(1)} -> {mission.group(2)})"
    return f"{lab + ' ' if lab else ''}Mission {clean}" if lab else f"Challenge {clean}"


def discover_markdown() -> list[Path]:
    files: list[Path] = []
    for source in sorted(VAULT_ROOT.glob("_source_*"), key=lambda p: p.name.casefold()):
        if source.is_dir():
            files.extend(source.rglob("*.md"))
    return sorted(files, key=lambda p: normalize_path(p.relative_to(VAULT_ROOT)).casefold())


def build_index() -> tuple[list[dict[str, object]], list[str]]:
    tracked = tracked_paths()
    records: list[dict[str, object]] = []
    warnings: list[str] = []
    seen: set[str] = set()
    for path in discover_markdown():
        relative = normalize_path(path.relative_to(VAULT_ROOT))
        try:
            markdown = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError as error:
            warnings.append(f"{relative}: unreadable ({error})")
            continue
        if not markdown.strip():
            warnings.append(f"{relative}: empty; omitted")
            continue
        frontmatter, markdown_body = parse_frontmatter(markdown)
        headings = headings_from(markdown_body)
        title = title_for(path, frontmatter, headings)
        body = strip_markdown(markdown_body)
        origin = origin_for(relative, frontmatter)
        category = category_for(relative, frontmatter, title, body)
        tags = tags_for(frontmatter, f"{title}\n{body}")
        record: dict[str, object] = {
            "id": relative,
            "title": title,
            "path": relative,
            "category": category,
            "origin": origin,
            "headings": headings,
            "snippet": snippet_for(body, title, category, origin, tags),
            "tags": tags,
            "body": body,
        }
        context_title = context_title_for(title, relative, markdown_body)
        if context_title:
            record["context_title"] = context_title
        if relative not in tracked:
            record["source_markdown"] = markdown
        if relative in seen:
            warnings.append(f"{relative}: duplicate ID; omitted")
            continue
        seen.add(relative)
        records.append(record)
    return records, warnings


def serialized(records: list[dict[str, object]]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2) + "\n"


def validate(records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    ids = [str(item.get("id", "")) for item in records]
    if len(ids) != len(set(ids)):
        errors.append("duplicate IDs detected")
    required = {"id", "title", "path", "category", "origin", "headings", "snippet", "tags", "body"}
    for item in records:
        missing = required.difference(item)
        if missing:
            errors.append(f"{item.get('id', '<unknown>')}: missing {sorted(missing)}")
        if item.get("category") not in CATEGORIES:
            errors.append(f"{item.get('id')}: unknown category {item.get('category')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate and fail if writeups-index.json is stale")
    args = parser.parse_args()
    records, warnings = build_index()
    errors = validate(records)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    output = serialized(records)
    if args.check:
        current = INDEX_PATH.read_text(encoding="utf-8-sig") if INDEX_PATH.exists() else ""
        if current != output:
            print(f"STALE: {INDEX_PATH.name} must be regenerated", file=sys.stderr)
            return 1
        print(f"OK: {len(records)} records; {len(warnings)} warning(s); index is current")
        return 0
    INDEX_PATH.write_text(output, encoding="utf-8")
    embedded = sum("source_markdown" in record for record in records)
    print(f"Wrote {INDEX_PATH.name}: {len(records)} records, {embedded} embedded sources, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
