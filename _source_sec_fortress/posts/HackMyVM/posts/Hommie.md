# Hommie | HackMyVM

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/7b2c5a6b-04bd-4271-afba-813cf52fafec)

## Difficulty = Easy

***

Running our ARP scan to detect live host we have a target

![](https://i.imgur.com/xH0aqQq.png)


Running our nmap scan we have -:


```bash
# Nmap 7.94 scan initiated Fri Oct 27 20:40:39 2023 as: nmap -p- -sCV -T4 -v --min-rate=1000 -oN nmap.txt -Pn 192.168.0.106
Nmap scan report for hommie (192.168.0.106)
Host is up (0.00084s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.0.158
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0               0 Sep 30  2020 index.html
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 c6:27:ab:53:ab:b9:c0:20:37:36:52:a9:60:d3:53:fc (RSA)
|   256 48:3b:28:1f:9a:23:da:71:f6:05:0b:a5:a6:c8:b7:b0 (ECDSA)
|_  256 b3:2e:7c:ff:62:2d:53:dd:63:97:d4:47:72:c8:4e:30 (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
| http-methods: 
|_  Supported Methods: GET HEAD
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Oct 27 20:40:54 2023 -- 1 IP address (1 host up) scanned in 14.68 seconds
```

Logging in to `FTP` as the **anonymous** user looks like we have a directory called `.web`

![](https://i.imgur.com/zuokYa1.png)

I noticed in this directory we can upload files from our local machine using the `PUT` command

![](https://i.imgur.com/Ve65dcL.png)

I was able to upload my `nmap.txt` scan file to the server, Navigating to port `80/HTTP` we have this -:


![](https://i.imgur.com/tzdzMFm.png)


Nothing much in page source, but navigating to `/nmap.txt` we have this -:


![](https://i.imgur.com/QmVJNXt.png)


Nice, our nmap scan result, we can therefore upload our PHP reverse shell, go ahead and use you favourite payload

- start up a listener `nc -lvnp 4444`
- then copy [this](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) to a file called `shell.shtml`
- make sure to change your `$ip`, use the `ifconfig` command to check

Now we can `cd` to the .web directory and upload our shell

![](https://i.imgur.com/Flc1kZP.png)

Navigating to the directory on the wbesite, it either our shell got downloaded back or can't execute commands, Trust me i tried out different webshells, After series of enumeration i peaked on [@muzec](https://twitter.com/muzecsec) writeup and saw that i need to run a UDP scan

![](https://i.imgur.com/8QKi862.png)


Nice, since `tftp` is a protocol that doesn't require authentication we can connect and try to download the `id_rsa` file


![](https://i.imgur.com/GpUeC64.png)

we now have the `id_rsa` file, let go ahead and connect using `SSH` with the username **alexia** we found

![](https://i.imgur.com/NOO0jNj.png)


After several navigation i found a file in `/opt` directory called **showMetheKey**


![](https://i.imgur.com/LLXUgj6.png)

also running `find / -type f -perm -u=s 2>/dev/null` points to the file as a `SUID` executable

![](https://i.imgur.com/TvaTPSl.png)

Running this `showMetheKey` file it looks like it provides user **alexia** `id_rsa` key

![](https://i.imgur.com/uEptaxX.png)

Using the `strings` command on the file looks like it checks for the `id_rsa` file from the **HOME** variable

![](https://i.imgur.com/A5r5Bil.png)

We can therefore change the **HOME** variable to `/root` so instead of looking up user **alexia** home directory for `id_rsa`, it looks up the user **root** home directory for it


![](https://i.imgur.com/oYAPHZ9.png)


run the **showMetheKey** SUID executable and you should have the root `id_rsa`


![](https://i.imgur.com/ROuX4Xb.png)


- copy the key content
- cd to `/tmp`
- save into a file
- chmod 600 `filename`
- ssh -i `filename` root@IP

![](https://i.imgur.com/QIFlfhd.png)


Now you should be root 🥳


![](https://i.imgur.com/rvIToWM.png)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


