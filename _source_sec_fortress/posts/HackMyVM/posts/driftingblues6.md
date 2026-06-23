# **Driftingblues6**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/1c7b8528-5391-4ca1-918b-467edb8e82ef)

# **Difficulty = Easy**
***


As usual we run our network discovery scan, discovered `192.168.0.115`

![](https://i.imgur.com/870FsDS.png)


Running our nmap scan we discovered only one port


```bash
# Nmap 7.94 scan initiated Fri Nov 17 03:02:13 2023 as: nmap -p- -sVC -v --min-rate=1000 -T4 -oN nmap.txt 192.168.0.115
Nmap scan report for driftingblues (192.168.0.115)
Host is up (0.00028s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.2.22 ((Debian))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: driftingblues
| http-robots.txt: 1 disallowed entry 
|_/textpattern/textpattern
|_http-server-header: Apache/2.2.22 (Debian)

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Nov 17 03:02:27 2023 -- 1 IP address (1 host up) scanned in 13.82 seconds
```


Checking out port `80/HTTP` we have this website, Nothing really 🤪


![](https://i.imgur.com/PjVDr1a.png)


Checking out `/robots.txt` just as nmap as said we have this


![](https://i.imgur.com/481D7iN.png)


Navigating to `/textpattern/txtpattern` we have this login page


![](https://i.imgur.com/WkwNule.png)


As said earlier i decided to run a directory bruteforce with `ffuf` adding the `.zip` extension


![](https://i.imgur.com/Kuvl2Gx.png)



We can then download the zip file directly using the command below



```bash
$ wget 192.168.0.115/spammer.zip
```



When we try to unzip the file, we are asked for a password


![](https://i.imgur.com/TXoobpj.png)

Using a tool called `fcrackzip` we can go ahead and bruteforce the zip file


```bash
$ sudo apt install fcrackzip
$ fcrackzip -v -u -D -p /usr/share/wordlists/rockyou.txt spammer.zip
```


![](https://i.imgur.com/5nXdEHA.png)



We can go ahead and unzip the archive, which gives us `creds.txt`


![](https://i.imgur.com/U4h63Tr.png)


We can go ahead and login to the login page we found earlier


![](https://i.imgur.com/419HKOE.png)



Navigating to the **content** tab and clicking **Files** we where able to upload a PHP web shell



![](https://i.imgur.com/DqDBUKG.png)


Our PHP web shell was uploaded to `/textpattern/files` called `good.php`, you can find one from [www.revshells.com](www.revshells.com)


![](https://i.imgur.com/C40LrEu.png)


Hell yeah, we got reverse shell as user **www-data** (**Hint -:** Use a python payload for stable shell)


![](https://i.imgur.com/h5Gi1fr.png)


Enumerated the box, looking for users, only **www-data** exists, password in config files, SUID, Nothing !!! But running `uname -a` tells us the version of linux we are currently running on -:


![](https://i.imgur.com/zdKEJcq.png)


Unfortunately, this version of linux is vulnerable to the [Dirty cow](https://www.exploit-db.com/exploits/40616) # Race Condition Privilege Escalation exploit, this will be beneficial to us 😁


![](https://i.imgur.com/mM5atFa.png)


Go ahead and copy the code, then create a file name `cowroot.c` and save the file


![](https://i.imgur.com/B7XWtmh.png)



Compile the code using `GCC` with the following command


```bash
$ gcc cowroot.c -o cowroot -pthread
```


![](https://i.imgur.com/eNC4HMx.png)


Now run the code with `./cowroot` and you should be user **root**


![](https://i.imgur.com/5iYl7Gi.png)



GG 👾



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>





