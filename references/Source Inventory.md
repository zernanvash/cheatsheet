# Source Inventory

Local source folders retained for future restructuring and writeup mining. These folders are intentionally outside the main study route and are ignored by Git through `_source_*/`.

## TryHackMe Sources

### Cajac TryHackMe Writeups

- Local folder: `_source_tryhackme_cajac`
- Upstream: https://github.com/Cajac/TryHackMe-Writeups
- Local contents observed: `Challenges`, `Learning_Paths`, `Modules`, `Networks`, `Walkthroughs`, and repository README/assets.
- Use later for: TryHackMe room-to-technique mapping, study examples, and room categorization.

### 0xb0b TryHackMe GitBook

- Local folder: `_source_0xb0b_tryhackme`
- Upstream: https://0xb0b.gitbook.io/writeups/tryhackme/
- Local seed files saved:
  - `2023.md`
  - `2024.md`
  - `2025.md`
  - `2026.md`
  - `soupedecode-01.md`
  - `sitemap.xml`
  - `sitemap-pages.xml`
- Notes: GitBook exposes Markdown alternates for the TryHackMe year indexes at `https://0xb0b.gitbook.io/writeups/tryhackme/YYYY.md` for 2023-2026. Use the sitemap later to choose which individual room pages to mirror or analyze.

## Existing Sources

- `_source_0xrefs`
  - Upstream: https://github.com/0xrefs/0xrefs.github.io
  - Use for: Interactive command cheatsheet queries, variable injection, and shell history generation.
  - Folded into: [0xrefs Interactive Command Reference](../0xrefs.html) and local manifests.
- `_source_hackmyvm_writeups`
  - Use later for: boot2root technique mapping, especially LFI, upload, anonymous FTP, SSH keys, SUID, cron, Docker, kernel CVEs, TFTP, and unusual Linux service pivots.
  - Folded into: [Machine Exploitation Databank](../blueprints/Machine%20Exploitation%20Databank.md) and [Machine Attack Blueprint Index](../blueprints/machine-attacks/Machine%20Attack%20Blueprint%20Index.md).
- `_source_picoctf_cajac`
  - Use later for: support patterns inside machine challenges, especially source review, SQLi, SSTI, XXE, WebAssembly, pcap analysis, crypto/stego artifacts, and buffer overflow practice.
  - Folded into: [picoCTF Web and REV Patterns](../guides/picoCTF%20Web%20and%20REV%20Patterns.md), [Challenge Use Cases](Challenge%20Use%20Cases.md), and the new machine artifact blueprints.
- `_source_ruycr4ft_cheatsheets`
  - Use later for: command variants and quick syntax reinforcement.
- `_source_sec_fortress`
  - Use later for: indexed writeup technique mining across TryHackMe, HackTheBox, Proving Grounds, PwnTillDawn, Vulnyx, and HackMyVM.
  - Folded into: [Sec-Fortress Writeups Index](../guides/Sec-Fortress%20Writeups%20Index.md) and new blueprints for SSRF, WebDAV, XXE, SSTI, Webmin, ActiveMQ/CVE-style services, ADCS, NTLM capture, TFTP, and port knocking.
- `_source_temperance`
  - Use later for: solver scripting, service interaction, and reverse/support challenge workflows.

## Fundamentals Sources Added

- Official TryHackMe room: [Web Application Basics](https://tryhackme.com/room/webapplicationbasics)
- Official TryHackMe room: [Web Application Security](https://tryhackme.com/room/introwebapplicationsecurity)
- Official TryHackMe room: [Red Team Fundamentals](https://tryhackme.com/room/redteamfundamentals)
- Official TryHackMe room: [Windows Fundamentals 1](https://tryhackme.com/room/windowsfundamentals1xbx)
- Local offline PDF: [Web Exploitation.pdf](Web%20Exploitation.pdf)
