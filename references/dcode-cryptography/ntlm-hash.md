# NTLM Hash

> Source: [https://www.dcode.fr/ntlm-hash](https://www.dcode.fr/ntlm-hash)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is an NTLM hash? (Definition)

An NTLM hash (or NT hash ) is a 128-bit (16-byte) cryptographic fingerprint. NTLM (NT LAN Manager) is a remnant (still very much present) of the Windows ecosystem. Although Microsoft is now pushing towards Kerberos, NTLM hashing remains central to many network and security operations.

Example: 31D6CFE0D16AE931B73C59D7E0C089C0 is an NTLM hash

## How do I calculate an NTLM hash?

To calculate an NTLM hash: encode the password in UTF-16LE and then apply the MD4 algorithm to this string. The result is a 128-bit hash (32 hexadecimal characters).

Example: password is encoded as 700061007300730077006f0072006400 in UTF-16LE hexadecimal and produces the MD4 hash 8846f7eaee8fb117ad06bdd830b7586c

Often, the hexadecimal string representing an NTLM hash is displayed with uppercase characters.

## How to decode an NTLM hash?

A hash cannot be decoded: a hash function like MD4 is designed to be one-way; there is no algorithm that can directly recover the password from its hash.

However, it is possible to use a dictionary attack, which consists of testing a set of likely passwords until one is found that produces the same hash.

dCode uses a dictionary of several million passwords, but if the password is not in the dictionary, the search will fail.

## What is the difference between NTLM hash, LM hash, and Kerberos?

Historically, the LAN Manager (LM) hash was the first standard; this older DES-based algorithm is now considered obsolete and extremely vulnerable.

Subsequently, it was superseded by the NTLM hash, which uses MD4 and introduces case sensitivity. While it represents a more secure step than the LM format, it remains vulnerable to modern brute-force and pass-the-hash attacks.

Currently, the standard is Kerberos, a modern protocol that breaks with previous methods by using encrypted tickets. Unlike its predecessors, it establishes mutual authentication and strong encryption, with the critical advantage of never transmitting a hash over the network during the transaction.

## Where are NTLM hashes stored?

NTLM hashes are stored:

— On a local machine: in the SAM file ( %SystemRoot%\System32\config\SAM ), accessible only with SYSTEM privileges.

— In an Active Directory domain: in the NTDS.dit database on domain controllers, as well as in the memory of the LSASS.exe process.
