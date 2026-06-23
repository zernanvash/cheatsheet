# Filmsy | PG Practice

***
## No more flimsy excuses

## Author: Ven3xy
## Released on: Aug 30, 2022
## Walkthrough: Yes
***



Running our nmap scan we have 3 open ports

```bash
# Nmap 7.94SVN scan initiated Sun Feb 25 05:01:41 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.194.220
Increasing send delay for 192.168.194.220 from 0 to 5 due to 234 out of 584 dropped probes since last increase.
Warning: 192.168.194.220 giving up on port because retransmission cap hit (6).
Nmap scan report for 192.168.194.220
Host is up (0.16s latency).
Not shown: 42087 closed tcp ports (conn-refused), 23445 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 62:36:1a:5c:d3:e3:7b:e1:70:f8:a3:b3:1c:4c:24:38 (RSA)
|   256 ee:25:fc:23:66:05:c0:c1:ec:47:c6:bb:00:c7:4f:53 (ECDSA)
|_  256 83:5c:51:ac:32:e5:3a:21:7c:f6:c2:cd:93:68:58:d8 (ED25519)
80/tcp   open  http    OpenResty web app server 1.21.4.1
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Welcome to OpenResty!
|_http-server-header: openresty/1.21.4.1
3306/tcp open  mysql   MySQL (unauthorized)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Feb 25 05:06:06 2024 -- 1 IP address (1 host up) scanned in 265.30 seconds
```



Navigating to port 80/HTTP we have a web application running on `openresty` version `1.21.4.1`


![](https://i.imgur.com/95khHwl.png)





Viewing page source we don't have any important/juicy information :(


![](https://i.imgur.com/plDehyF.png)



We can't also connect via `mysql` as it does not allow us, whereas running my nmap scan once more i discovered 2 new open ports 🙃 (Always run your nmap scan twice while playing PG)



```
# Nmap 7.94SVN scan initiated Sun Feb 25 05:45:03 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.194.220
Warning: 192.168.194.220 giving up on port because retransmission cap hit (6).
Nmap scan report for 192.168.194.220
Host is up (0.15s latency).
Not shown: 58065 closed tcp ports (conn-refused), 7465 filtered tcp ports (no-response)
PORT      STATE SERVICE             VERSION
22/tcp    open  ssh                 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 62:36:1a:5c:d3:e3:7b:e1:70:f8:a3:b3:1c:4c:24:38 (RSA)
|   256 ee:25:fc:23:66:05:c0:c1:ec:47:c6:bb:00:c7:4f:53 (ECDSA)
|_  256 83:5c:51:ac:32:e5:3a:21:7c:f6:c2:cd:93:68:58:d8 (ED25519)
80/tcp    open  http                OpenResty web app server 1.21.4.1
|_http-server-header: openresty/1.21.4.1
| http-methods: 
|_  Supported Methods: HEAD
|_http-title: Welcome to OpenResty!
3306/tcp  open  mysql               MySQL (unauthorized)
9443/tcp  open  ssl/tungsten-https?
43500/tcp open  http                OpenResty web app server
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
|_http-server-header: APISIX/2.8
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Feb 25 05:48:18 2024 -- 1 IP address (1 host up) scanned in 194.58 seconds
```


Checking port `9443` we have this page which **occurs when a browser sends a request to a web server that the server cannot understand or process correctly**


![](https://i.imgur.com/b5yKSyd.png)

Checking port `43500` we have this page, saying Route no found

![](https://i.imgur.com/Thc6ro2.png)



However enumerating the `http-server-header: APISIX/2.8` i found there is an exploit for this on [exploit-db](https://www.exploit-db.com/exploits/50829?source=post_page-----5f920b22ccff--------------------------------) that leads to a Remote Code Execution vulnerability



![](https://i.imgur.com/CQxBdRw.png)


Checking crontab we can see that the user `root` runs `apt-get update` every minute


![](https://i.imgur.com/nxJqW3a.png)



We can create our own apt pre-invoke script in the `/etc/apt/apt.conf.d/` where the scripts are generally kept, first let's confirm if we have write access to this directory



![](https://i.imgur.com/2j6swJF.png)


Yes we do have write access, using this [article](https://systemweakness.com/code-execution-with-apt-update-in-crontab-privesc-in-linux-e6d6ffa8d076) as a guide i created a file named `00whatever` and put the below payload to grant the `/root` directory all permissions for all users


```
APT::Update::Pre-Invoke {"chmod -R 777 /root"};
```




![](https://i.imgur.com/yNwOdOa.png)



Running the below command we can see that we truly do have access




![](https://i.imgur.com/6spPMUF.png)



we can then regain the `proof.txt` flag as a normal user

GG


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
