# Gift | HackMyVM

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/21525cf1-b2a8-4e86-ad70-15d0f19ab4f4)

## Difficulty = Easy

***


We can go ahead and start up our VM

![](https://i.imgur.com/ZOkB96q.png)

Then scan your network using `arp-scan`

![](https://i.imgur.com/35C3xYN.png)

Running our nmap scan we have


```bash
# Nmap 7.94 scan initiated Fri Oct 27 02:48:01 2023 as: nmap -p80,22 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 192.168.0.115
Nmap scan report for gift (192.168.0.115)
Host is up (0.00038s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.3 (protocol 2.0)
| ssh-hostkey: 
|   3072 2c:1b:36:27:e5:4c:52:7b:3e:10:94:41:39:ef:b2:95 (RSA)
|   256 93:c1:1e:32:24:0e:34:d9:02:0e:ff:c3:9c:59:9b:dd (ECDSA)
|_  256 81:ab:36:ec:b1:2b:5c:d2:86:55:12:0c:51:00:27:d7 (ED25519)
80/tcp open  http    nginx
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Site doesn't have a title (text/html).

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 27 02:48:13 2023 -- 1 IP address (1 host up) scanned in 12.10 seconds
```


Navigating to port `80/HTTP` we have


![](https://i.imgur.com/Skko9yz.png)



Nothing much in page-source so i decided to perform dir/file bruteforce

![](https://i.imgur.com/533nppx.png)

As we can see no results, made my recon and i decided to bruteforce `SSH` using the default **root** account

![](https://i.imgur.com/WFg8qu6.png)


As we can see we now have the **root** user password, let go ahead and login via `SSH`

![](https://i.imgur.com/PyeDF1w.png)

.....And we are **root** 🤟


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>




