# Lian_Yu

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/c72d580db69a726dfb8da8aa6eaa2f5a.jpeg)

## Difficulty = Easy

***

Running our nmap scan we have -:


```bash
# Nmap 7.94 scan initiated Tue Oct 24 01:20:41 2023 as: nmap -p80,22,21,111,56529 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.107.192
Nmap scan report for 10.10.107.192
Host is up (0.28s latency).

PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.2
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp    open  http    Apache httpd
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          42893/udp   status
|   100024  1          46972/tcp6  status
|   100024  1          50675/udp6  status
|_  100024  1          56529/tcp   status
56529/tcp open  status  1 (RPC #100024)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Oct 24 01:21:10 2023 -- 1 IP address (1 host up) scanned in 28.98 seconds
```


We can't connect via `FTP` as an anonymous **User**

![](https://i.imgur.com/XG68mFA.png)

Navigating to port `80/HTTP` we have a message

![](https://i.imgur.com/Ojj0LMQ.png)

Viewing **Page-Source** we have the background image **URL**

![](https://i.imgur.com/4FT91Zd.png)

We can download the image using `wget`

![](https://i.imgur.com/NRF0pir.png)

Inspecting the image with **strings**, **stegsolve**, **binwalk** and other steganography tools, i literally found nothing so i decided to dir/file bruteforce with `ffuf`

![](https://i.imgur.com/Ky7LcSm.png)

Navigating to `/island` we have

![](https://i.imgur.com/wxw0kCy.png)


Decided to run `ffuf` on `/island` again and we have

![](https://i.imgur.com/Uu7Pfjm.png)

Navigating to `/island/2100` we have this page

![](https://i.imgur.com/pjl6djs.png)

Viewing **page-source** we have

![](https://i.imgur.com/h0FMDNb.png)


since we have `.ticket` in the message we will add this to our extension filter while fuzzing with `ffuf`

![](https://i.imgur.com/Fciu9gu.png)


Navigating to `/island/2100/green_arrow.ticket` we have


![](https://i.imgur.com/XlMZgVI.png)

Hmmm 🤔, looks like base58, we can go ahead and decode it

![](https://i.imgur.com/h92NDPW.png)

We can therefore login with the username **vigilante** and password given

![](https://i.imgur.com/beDO8KZ.png)

Download all files with this two commands

```bash
$ mget .*
$ mget *
```

Running `stegseek` on `aa.jpg` we found a zip file, go ahead and change the name from `aa.jpg.out` to `ss.zip`


![](https://i.imgur.com/JF2I86X.png)


Then unzip `ss.zip` with the `zip` command

![](https://i.imgur.com/9HJqRGM.png)


Concatenating `shado` we have a password while `passwd.txt` gives us a **just for fun** letter 😂


![](https://i.imgur.com/OKElFDU.png)

We can't forget the `.other_user.txt` file


![](https://i.imgur.com/xzIiuqk.png)

Concatenating it gives us a lot of usernames


![](https://i.imgur.com/ThevLKq.png)


I was thinking of bruteforcing but trying out `slades:M3tahuman` via `SSH` got us logged in


![](https://i.imgur.com/9AXy6RU.png)


Running `sudo -l` we can see that `pkexec` is allowed to run using **root** permissions, so we can gain root with the following command -:

```bash
$ sudo pkexec /bin/bash
```

![](https://i.imgur.com/Fml0d2Q.png)

GG 🚀


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



