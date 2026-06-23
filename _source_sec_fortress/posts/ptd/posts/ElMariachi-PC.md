# **ElMariachi-PC**

***
![](https://pbs.twimg.com/media/F-OcyUmWEAAfKcl?format=jpg&name=small)

## **Difficulty = Easy**

***

Running our nmap scan we have 

```bash
# Nmap 7.94 scan initiated Sun Nov  5 22:05:48 2023 as: nmap -p- -sVC -v --min-rate=1000 -T4 -oN nmap.txt 10.150.150.69
Warning: 10.150.150.69 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.150.150.69
Host is up (0.15s latency).
Not shown: 65377 closed tcp ports (conn-refused), 143 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=ElMariachi-PC
| Issuer: commonName=ElMariachi-PC
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-11-05T03:35:18
| Not valid after:  2024-05-06T03:35:18
| MD5:   114d:c41e:0958:bfeb:7a14:72b4:54b3:ba16
|_SHA-1: fc7b:2c76:4b75:2e74:be06:52fb:18c1:2147:f86f:c153
|_ssl-date: 2023-11-06T03:44:15+00:00; +33m43s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: ELMARIACHI-PC
|   NetBIOS_Domain_Name: ELMARIACHI-PC
|   NetBIOS_Computer_Name: ELMARIACHI-PC
|   DNS_Domain_Name: ElMariachi-PC
|   DNS_Computer_Name: ElMariachi-PC
|   Product_Version: 10.0.17763
|_  System_Time: 2023-11-06T03:43:46+00:00
5040/tcp  open  unknown
7680/tcp  open  pando-pub?
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
50417/tcp open  msrpc         Microsoft Windows RPC
60000/tcp open  unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Content-Type: text/html
|     Content-Length: 177
|     Connection: Keep-Alive
|     <HTML><HEAD><TITLE>404 Not Found</TITLE></HEAD><BODY><H1>404 Not Found</H1>The requested URL nice%20ports%2C/Tri%6Eity.txt%2ebak was not found on this server.<P></BODY></HTML>
|   GetRequest: 
|     HTTP/1.1 401 Access Denied
|     Content-Type: text/html
|     Content-Length: 144
|     Connection: Keep-Alive
|     WWW-Authenticate: Digest realm="ThinVNC", qop="auth", nonce="YlrVP3oW5kDI2UcCehbmQA==", opaque="m2yqFi2usv3AY2yatYSTRmyNPAplB8C1oC"
|_    <HTML><HEAD><TITLE>401 Access Denied</TITLE></HEAD><BODY><H1>401 Access Denied</H1>The requested URL requires authorization.<P></BODY></HTML>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port60000-TCP:V=7.94%I=7%D=11/5%Time=65485876%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,179,"HTTP/1\.1\x20401\x20Access\x20Denied\r\nContent-Type:\x2
SF:0text/html\r\nContent-Length:\x20144\r\nConnection:\x20Keep-Alive\r\nWW
SF:W-Authenticate:\x20Digest\x20realm=\"ThinVNC\",\x20qop=\"auth\",\x20non
SF:ce=\"YlrVP3oW5kDI2UcCehbmQA==\",\x20opaque=\"m2yqFi2usv3AY2yatYSTRmyNPA
SF:plB8C1oC\"\r\n\r\n<HTML><HEAD><TITLE>401\x20Access\x20Denied</TITLE></H
SF:EAD><BODY><H1>401\x20Access\x20Denied</H1>The\x20requested\x20URL\x20\x
SF:20requires\x20authorization\.<P></BODY></HTML>\r\n")%r(FourOhFourReques
SF:t,111,"HTTP/1\.1\x20404\x20Not\x20Found\r\nContent-Type:\x20text/html\r
SF:\nContent-Length:\x20177\r\nConnection:\x20Keep-Alive\r\n\r\n<HTML><HEA
SF:D><TITLE>404\x20Not\x20Found</TITLE></HEAD><BODY><H1>404\x20Not\x20Foun
SF:d</H1>The\x20requested\x20URL\x20nice%20ports%2C/Tri%6Eity\.txt%2ebak\x
SF:20was\x20not\x20found\x20on\x20this\x20server\.<P></BODY></HTML>\r\n");
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 33m43s, deviation: 0s, median: 33m42s
|_smb2-time: Protocol negotiation failed (SMB2)

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Nov  5 22:10:33 2023 -- 1 IP address (1 host up) scanned in 285.00 seconds
```

Enumerating port `3389/RDP` with `nmap` we have


```bash
sec-fortress@Pwn-F0rk-3X3C:~/PTD/10.150.150.69$ nmap --script "rdp-enum-encryption or rdp-vuln-ms12-020 or rdp-ntlm-info" -p 3389 -T4 10.150.150.69  
Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-05 22:23 EST
Nmap scan report for 10.150.150.69
Host is up (0.24s latency).

PORT     STATE SERVICE
3389/tcp open  ms-wbt-server
| rdp-ntlm-info: 
|   Target_Name: ELMARIACHI-PC
|   NetBIOS_Domain_Name: ELMARIACHI-PC
|   NetBIOS_Computer_Name: ELMARIACHI-PC
|   DNS_Domain_Name: ElMariachi-PC
|   DNS_Computer_Name: ElMariachi-PC
|   Product_Version: 10.0.17763
|_  System_Time: 2023-11-06T03:57:39+00:00
| rdp-enum-encryption: 
|   Security layer
|     CredSSP (NLA): SUCCESS
|     CredSSP with Early User Auth: SUCCESS
|     RDSTLS: SUCCESS
|     SSL: SUCCESS
|_  RDP Protocol Version:  RDP 10.6 server

Nmap done: 1 IP address (1 host up) scanned in 10.44 seconds
```

Initially i enumerated the **RDP Protocol Version**, which gave me bluekeep exploits but non seems to work

![](https://i.imgur.com/0dzhBEE.png)


On port `60000` i was able to see something like **ThinVNC** and it definitely looks like a clue was waiting there for us

![](https://i.imgur.com/D338xY8.png)

After much googling i found an exploit from [MuirlandOracle](https://github.com/MuirlandOracle/CVE-2019-17662) that leads to an **Authentication Bypass** vulnerability, Running the exploit gives us this -:

![](https://i.imgur.com/6LtPYko.png)


Definitely i think that is the username and password for the **RDP** protocol, so we can go ahead and login via tool called `rdesktop`


```bash
$ rdesktop -d ElMariachi-PC -u <Username> -p <Password> 10.150.150.69
```


Hell yeah and  we are successfully logged in via **RDP**, you can submit the flag on The Desktop 😎

![](https://i.imgur.com/pM7HWDL.png)

GG 🚀


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
