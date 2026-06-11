# PCAP And Traffic Artifact To Credentials

Use when a machine or support challenge provides packet captures, traffic logs, or intercepted credentials.

## Signals

- Files: `.pcap`, `.pcapng`, `.cap`, `.har`, proxy logs.
- Challenge text mentions sniffing, capture, traffic, packets, or network evidence.
- Web or SMB files include exported captures.

## Main Path

```bash
file capture.pcapng
tshark -r capture.pcapng -q -z io,phs
tshark -r capture.pcapng -Y 'http or ftp or telnet or smb or kerberos'
strings capture.pcapng | grep -Ei 'user|pass|token|flag|Authorization'
```

Extract cleartext credentials, hashes, hosts, paths, cookies, files, and protocol-specific artifacts.

## Options To Try

- Follow TCP streams in Wireshark for HTTP, FTP, Telnet, and custom services.
- Export objects from HTTP/SMB where available.
- Look for Basic auth, cookies, JWTs, NTLM handshakes, and Kerberos material.
- Convert handshakes to crackable formats only when the lab expects it.
- Feed discovered hostnames and credentials back into the machine workflow.

## Study Examples

- picoCTF forensics tasks are useful practice for extracting credentials and files from captures.
- Machine rooms sometimes hide credentials in traffic artifacts downloaded from SMB, FTP, or web.
