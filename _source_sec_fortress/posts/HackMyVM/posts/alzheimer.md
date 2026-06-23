# **Alzheimer**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/57c3623e-c520-4301-a0ac-c5ecac454591)

## **Difficulty = Easy**

***

First things first, discover live host using `arp-scan`


![](https://i.imgur.com/oUV42aV.png)

running our nmap scan we have 

```bash
# Nmap 7.94 scan initiated Sat Oct 28 01:29:07 2023 as: nmap -p- -sCV -T4 -v --min-rate=1000 -oN nmap.txt 192.168.0.103
Nmap scan report for alzheimer (192.168.0.103)
Host is up (0.0013s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE    SERVICE VERSION
21/tcp open     ftp     vsftpd 3.0.3
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
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp filtered ssh
80/tcp filtered http
Service Info: OS: Unix

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Oct 28 01:29:14 2023 -- 1 IP address (1 host up) scanned in 7.50 seconds
```

Connecting to `FTP` via the anonymous user we have a `.secretnote.txt` file


![](https://i.imgur.com/6gK0hxF.png)


Transfer using the `mget` command


![](https://i.imgur.com/wNhiXJG.png)


We have a note that talks about port knocking


![](https://i.imgur.com/2CLUpqj.png)

Go ahead and do this

```bash
$ sudo apt-get install knockd
$ knock 192.168.0.103 1000 2000 3000 -v -d 1000
```

Port knocking takes time sometimes so you will have to perform the previous command multiple times

![](https://i.imgur.com/EU72U2o.png)



After more attempts all filtered ports are now opened

![](https://i.imgur.com/PeqYpW0.png)


Navigating to port `80/HTTP` we have this note

![](https://i.imgur.com/rRE5af3.png)


Performing dir/file bruteforce with `ffuf` we have

![](https://i.imgur.com/l0ok1Gp.png)


`/admin` gives us a 404 but `/home` gives us this


![](https://i.imgur.com/IiQtbVW.png)


`/secret` then gives us this

![](https://i.imgur.com/sDHhqL4.png)


Fuzzing again this time with `/secret` using `ffuf` we have

![](https://i.imgur.com/NXtO56K.png)


Navigating to `/secret/home` we have this


![](https://i.imgur.com/1i4GSGi.png)



fuzzed for parameters, checked file source, tried bruteforcing, Nothing !!!, checking few write-ups i found out we where meant to get the password from the `.secretnote.txt` file

![](https://i.imgur.com/SRBd1gW.png)

I don't think the box is broken, let move, logged in with the `SSH` credentials as user **medusa:ihavebeenalwayshere!!!**


![](https://i.imgur.com/LdOjpae.png)



Running `sudo -l` we have permissions to `/bin/id` with sudo privileges

![](https://i.imgur.com/h9fOAOC.png)

It seems like i couldn't get privilege escalation with **sudo**, running `find / -perm -4000 2>/dev/null` we can see we have permissions to run **capsh** with `SUID`


![](https://i.imgur.com/tntqCdH.png)


Checking [gtfobins]() we can get user **root** with `capsh`


![](https://i.imgur.com/D9VDRtQ.png)

Running the payload we are user **root**


![](https://i.imgur.com/gd384y8.png)




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>





 
