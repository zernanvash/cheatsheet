# Ignite

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/676cb3273c613c9ba00688162efc0979.png)

## Difficulty = Easy 

***

Running our nmap scan, looks like we have only 1 port opened

```bash
# Nmap 7.94 scan initiated Thu Oct 19 09:28:07 2023 as: nmap -p- -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.238.54
Nmap scan report for 10.10.238.54
Host is up (0.14s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/fuel/
|_http-title: Welcome to FUEL CMS
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Oct 19 09:29:54 2023 -- 1 IP address (1 host up) scanned in 107.47 seconds
```


Navigating to port `80/HTTP` we have the version boldly written 😄


![](https://i.imgur.com/jia00yx.png)



Enumerating this version we have a [Remote Code Execution Exploit](https://github.com/ice-wzl/Fuel-1.4.1-RCE-Updated/blob/main/Fuel-Updated.py), we can there for run this script and get our shell


![](https://i.imgur.com/3tosjg3.png)

Change directory to `/tmp` and send a tool called [linpeas](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) to target machine



![](https://i.imgur.com/MYQjonp.png)

Navigating to `/var/www/html/fuel/application/config` we found a username and password

![](https://i.imgur.com/IyTwp71.png)


We can then switch user to root


![](https://i.imgur.com/FD6Mxgn.png)

Bankai 🎎


![](https://i.pinimg.com/originals/37/72/7b/37727b94893310b00a4420c709583369.gif)




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

