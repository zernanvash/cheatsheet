# Pivoting And Internal Services

Use when a compromised host exposes routes, internal-only listeners, or credentials that apply to another subnet/host.

## Signals

- `ip route`, `route print`, or `ipconfig /all` shows extra networks.
- Internal services listen on `127.0.0.1` or private subnets.
- Web app or config references internal hosts.
- Firewall blocks direct access but compromised host can reach it.

## Main Path

Linux:

```bash
ip addr
ip route
ss -tulpn
ssh -N -L 127.0.0.1:8080:127.0.0.1:80 user@target
ssh -N -D 127.0.0.1:1080 user@target
```

Windows:

```cmd
ipconfig /all
route print
netstat -ano
```

## Options To Try

- Local forward for one internal service.
- Dynamic SOCKS for repeated enumeration through proxychains.
- Remote forward when target can connect back to your host.
- Chisel or Ligolo-ng when SSH is unavailable.
- Meterpreter route/socks in lab networks when using Metasploit.
- Reuse discovered credentials against internal SMB, WinRM, DB, or web admin.

## Study Examples

- OSCP Others module lists local, dynamic, remote, and remote dynamic forwarding.
- 0xb0b and Cajac challenge chains often require re-enumeration after each foothold.
