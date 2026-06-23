import os
import json
import re
import urllib.parse

workspace_dir = r"g:\HackForGov2025\h4g"
index_path = os.path.join(workspace_dir, "writeups-index.json")

# Define cybersecurity tag mappings
TAG_KEYWORDS = {
    "WordPress": [r"wordpress", r"wp-", r"wpscan"],
    "SQLi": [r"sqli", r"sql injection", r"sql-injection", r"mysql", r"postgres", r"sqlite"],
    "LFI": [r"lfi", r"local file inclusion", r"file inclusion"],
    "RCE": [r"rce", r"remote code execution", r"command injection", r"exec\("],
    "SSTI": [r"ssti", r"server-side template injection", r"jinja2", r"mako", r"thymeleaf"],
    "XXE": [r"xxe", r"xml external entity"],
    "SSRF": [r"ssrf", r"server-side request forgery"],
    "XSS": [r"xss", r"cross-site scripting", r"cross site scripting"],
    "CSRF": [r"csrf", r"cross-site request forgery"],
    "Directory Traversal": [r"directory traversal", r"path traversal", r"\.\./\.\."],
    "File Upload": [r"file upload", r"upload shell", r"upload bypass"],
    "XOR": [r"xor", r"exclusive or", r"xor encryption"],
    "RSA": [r"rsa", r"openssl rsautl", r"id_rsa"],
    "AES": [r"aes", r"aes-128", r"aes-256"],
    "Assembly": [r"assembly", r"x86", r"x64", r"asm", r"registers", r"mov ", r"jmp ", r"cmp "],
    "IDA Pro": [r"ida pro", r"ida", r"decompiler"],
    "Ghidra": [r"ghidra"],
    "GDB": [r"gdb", r"gnu debugger"],
    "Keygen": [r"keygen", r"key generator", r"key validation"],
    "Patching": [r"patch", r"patching", r"binary patch"],
    "Obfuscation": [r"obfuscated", r"obfuscation", r"deobfuscate"],
    "Golang": [r"golang", r"go binary", r"go build"],
    "Rust": [r"rust", r"cargo"],
    ".NET": [r"\.net", r"dnspy", r"ilspy", r"c#", r"mono "],
    "Anti-Debugging": [r"anti-debug", r"anti-debugging", r"ptrace", r"isdebuggerpresent"],
    "Buffer Overflow": [r"buffer overflow", r"bof", r"stack overflow", r"vuln\("],
    "ROP": [r"rop chain", r"rop", r"return-oriented"],
    "Format String": [r"format string", r"printf\("],
    "Privilege Escalation": [r"privilege escalation", r"privesc", r"escalate", r"root access"],
    "Sudo PrivEsc": [r"sudo -l", r"sudo privilege", r"sudoers"],
    "Cronjob PrivEsc": [r"cronjob", r"cron", r"/etc/crontab"],
    "SUID": [r"suid", r"setuid", r"perm -4000"],
    "Active Directory": [r"active directory", r"kerberos", r"kerberoast", r"bloodhound", r"domain controller"],
    "Nmap": [r"nmap", r"port scan"],
    "Reverse Shell": [r"reverse shell", r"revshell", r"nc -e", r"bash -i"],
    "SSH": [r"ssh", r"id_rsa", r"authorized_keys"],
    "FTP": [r"ftp", r"anonymous ftp"],
    "SMB": [r"smb", r"samba", r"smbclient", r"smbget"],
    "RPC": [r"rpc", r"rpcclient"],
    "NFS": [r"nfs", r"showmount"],
    "LDAP": [r"ldap"],
    "Redis": [r"redis", r"redis-cli"],
    "WebDAV": [r"webdav"],
    "Tomcat": [r"tomcat"],
    "Jenkins": [r"jenkins"],
    "Wireshark": [r"wireshark", r"pcap", r"tshark"],
    "Volatility": [r"volatility"],
    "Steghide": [r"steghide"],
    "Binwalk": [r"binwalk"],
    "Metadata": [r"metadata", r"exiftool"]
}

def get_referenced_file(content, current_dir):
    # Markdown links: [label](path)
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for label, path in links:
        if path.startswith("http://") or path.startswith("https://") or path.startswith("#"):
            continue
        path = path.split("?")[0].split("#")[0]
        path = urllib.parse.unquote(path)
        ref_path = os.path.abspath(os.path.join(current_dir, path))
        if ref_path.startswith(os.path.abspath(workspace_dir)):
            return ref_path
            
    # Check for raw local file paths
    words = content.split()
    for word in words:
        if ("/" in word or "\\" in word) and any(word.endswith(ext) for ext in [".md", ".txt", ".py", ".c", ".sol", ".json", ".png", ".jpg", ".zip", ".exe"]):
            clean_word = word.strip("`'\"(),.:;")
            ref_path = os.path.abspath(os.path.join(current_dir, clean_word))
            if os.path.exists(ref_path) and os.path.isfile(ref_path) and ref_path.startswith(os.path.abspath(workspace_dir)):
                return ref_path
    return None

def clean_markdown_for_summary(content):
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove HTML tags
    content = re.sub(r'<[^>]*>', '', content)
    # Remove images and links
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)
    # Split into lines
    lines = [line.strip() for line in content.split('\n')]
    
    clean_paragraphs = []
    for line in lines:
        if not line:
            continue
        # Skip headers
        if line.startswith('#'):
            continue
        # Skip lists/tables lines or code snippets
        if line.startswith('|') or line.startswith('-') or line.startswith('*') or line.startswith('>'):
            # Skip bullet points unless they look like normal sentences
            if len(line) < 25:
                continue
        # Clean markdown formatting like bold, code spans
        line = line.replace('**', '').replace('__', '').replace('`', '').replace('::', '').replace('||', '')
        line = re.sub(r'\s+', ' ', line).strip()
        if len(line) > 30 and not line.startswith('/') and not line.startswith('$'):
            clean_paragraphs.append(line)
            if len(clean_paragraphs) >= 2:
                break
                
    if clean_paragraphs:
        summary = " ".join(clean_paragraphs)
        if len(summary) > 160:
            summary = summary[:157] + "..."
        return summary
    return ""

def main():
    if not os.path.exists(index_path):
        print(f"Index file not found: {index_path}")
        return

    with open(index_path, "r", encoding="utf-8-sig") as f:
        writeups = json.load(f)

    print(f"Initial writeups count: {len(writeups)}")

    pruned_writeups = []
    removed_count = 0

    for idx, w in enumerate(writeups):
        path_val = w["path"]
        full_path = os.path.join(workspace_dir, path_val)
        
        # 1. Existence and type check
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            print(f"PRUNING: {path_val} (File does not exist or is not a file)")
            removed_count += 1
            # If the file exists but it's not a file (maybe directory), we don't delete. If it's missing, nothing to delete.
            continue
            
        # 2. Size check
        size = os.path.getsize(full_path)
        if size == 0:
            print(f"PRUNING: {path_val} (File is 0 bytes)")
            removed_count += 1
            try:
                os.remove(full_path)
                print(f"Deleted empty file: {full_path}")
            except Exception as e:
                print(f"Failed to delete empty file {full_path}: {e}")
            continue
            
        # 3. Read content
        with open(full_path, "r", encoding="utf-8", errors="ignore") as mf:
            content = mf.read().strip()
            
        if not content:
            print(f"PRUNING: {path_val} (Content is empty string)")
            removed_count += 1
            try:
                os.remove(full_path)
                print(f"Deleted empty file: {full_path}")
            except Exception as e:
                print(f"Failed to delete empty file {full_path}: {e}")
            continue
            
        # 4. Check for empty/missing reference files in short writeups
        current_dir = os.path.dirname(full_path)
        ref_file = get_referenced_file(content, current_dir)
        
        # If it's very short and points to a reference file, verify that reference file
        if len(content) < 180 and ref_file:
            ref_rel = os.path.relpath(ref_file, workspace_dir)
            if not os.path.exists(ref_file) or not os.path.isfile(ref_file) or os.path.getsize(ref_file) == 0:
                print(f"PRUNING: {path_val} (Points to empty or missing reference file: {ref_rel})")
                removed_count += 1
                try:
                    os.remove(full_path)
                    print(f"Deleted empty writeup pointer file: {full_path}")
                except Exception as e:
                    print(f"Failed to delete file {full_path}: {e}")
                continue
                
        # Keep the writeup and enrich it!
        pruned_writeups.append((w, content, full_path))

    print(f"Pruning complete. Kept {len(pruned_writeups)} writeups. Removed {removed_count}.")

    final_index = []

    for w, content, full_path in pruned_writeups:
        # Detect tags based on keywords
        tags = []
        for tag, patterns in TAG_KEYWORDS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    tags.append(tag)
                    break
        
        # Limit tags count and sort
        tags = sorted(list(set(tags)))
        
        # Generate summary
        summary = clean_markdown_for_summary(content)
        if not summary:
            # Fallback summary
            category = w.get("category", "General")
            origin = w.get("origin", "CTF")
            if tags:
                summary = f"A {category} challenge from {origin} focusing on {', '.join(tags[:3])}."
            else:
                summary = f"Walkthrough of {w['title']} ({category} challenge from {origin})."
                
        # Cryptic title context resolution
        title_raw = w.get("title", "")
        # Remove markdown decorations from original title to test it
        title_clean = title_raw.replace("**", "").replace("||", "").replace("::", "").strip()
        
        context_title = None
        # Check if the title is cryptic (e.g., hex string like 0x39, or single number, or very short)
        is_hex = re.match(r'^0x[0-9a-fA-F]+$', title_clean)
        is_num = re.match(r'^\d+$', title_clean)
        is_cryptic = is_hex or is_num or len(title_clean) < 5
        
        if is_cryptic:
            # Try to build context
            path_lower = full_path.lower()
            lab_name = ""
            if "labs/venus" in path_lower or "/venus/" in path_lower:
                lab_name = "Venus Lab"
            elif "labs/hades" in path_lower or "/hades/" in path_lower:
                lab_name = "Hades Lab"
                
            # Search for mission description or objective in file
            mission_match = re.search(r'moving from `([^`]+)` to `([^`]+)`', content)
            if not mission_match:
                mission_match = re.search(r'moving from ([^\s]+) to ([^\s]+)', content, re.IGNORECASE)
                
            if mission_match:
                from_user = mission_match.group(1).strip("`'\"(),.:;")
                to_user = mission_match.group(2).strip("`'\"(),.:;")
                context_title = f"{lab_name} Mission {title_clean} ({from_user} -> {to_user})"
            elif lab_name:
                context_title = f"{lab_name} Mission {title_clean}"
            else:
                # General challenge
                context_title = f"Challenge {title_clean}"
                
        # Update/create fields on the index item
        enriched_item = {
            "title": w["title"],
            "path": w["path"],
            "category": w["category"],
            "origin": w["origin"],
            "headings": w.get("headings", []),
            "snippet": w.get("snippet", ""),
            "summary": summary,
            "tags": tags
        }
        if context_title:
            enriched_item["context_title"] = context_title
            
        final_index.append(enriched_item)

    # Write the enriched writeups index back
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(final_index, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully wrote enriched writeups-index.json with {len(final_index)} items.")

if __name__ == "__main__":
    main()
