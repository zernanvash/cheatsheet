# Archive And Password Manager Cracking

Use when the machine gives encrypted archives, KeePass databases, GPG material, SSH keys, office files, or backup bundles.

## Signals

- Files: `.zip`, `.7z`, `.rar`, `.kdbx`, `.gpg`, `.asc`, `.bak`, `.tar.gz`, `.sql`, `.old`.
- Downloaded share or web backup contains protected material.
- Hints point to a user, pet, site name, room theme, or custom wordlist.

## Main Path

```bash
file artifact
strings artifact | head
zip2john secret.zip > zip.hash
keepass2john vault.kdbx > keepass.hash
john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
john keepass.hash --wordlist=words.txt
```

After cracking, search extracted content for credentials, keys, hostnames, source code, and reuse opportunities.

## Options To Try

- Build a custom list with `cewl` from the target web app.
- Try filenames, usernames, company names, and challenge titles as mutations.
- For SSH keys, use `ssh2john` if passphrase-protected.
- For GPG, inspect key IDs, usernames, and recovered passphrases before decrypting.
- If archive extraction fails, repair or carve with `binwalk`, `7z`, or `foremost`.

## Study Examples

- HackMyVM and TryHackMe chains often hide SSH keys or app credentials inside ZIP/KeePass/backups.
- picoCTF-style support challenges teach the conversion-and-crack workflow used later on machines.
