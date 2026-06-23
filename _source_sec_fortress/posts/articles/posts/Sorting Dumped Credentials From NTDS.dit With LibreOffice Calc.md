# **Sorting Dumped Credentials From NTDS.dit With LibreOffice Calc**

***

After dumping the **NTDS.dit** secrets we have to sort out the **NT** part of this hashes that where dumped before we can crack them 👾

![](https://i.imgur.com/xd3Tc1Y.png)

We can use a Tool just like **MS EXCEL** called **LibreOffice Calc** to do this, Launch the tool and let do this ✈️

- [ ] Copy the whole part of these hashes

![](https://i.imgur.com/5N56Q7h.png)


- [ ] Paste it into **LibreOffice Calc** and you should see this prompt

![](https://i.imgur.com/ZEyVDgT.png)

- [ ] In the **Separator Options** menu Click **Separated by >> Other** then add a `:` and click **Ok**

![](https://i.imgur.com/PxaBYng.png)

- [ ] Now highlight this two columns as shown below and hit the **Delete** key on your keyboard, since we don't need them

**_Before :_**

![](https://i.imgur.com/1pEFS8m.png)

**_After :_**

![](https://i.imgur.com/E3KGZtf.png)

- [ ] Now save these hashes in a `.txt` file without the usernames and crack them with the syntax as shown below

```powershell
# Cracking NT hashes with hashcat
$ hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt -O

# Show cracked hashes
$ hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt -O --show
```

- [ ] Now copy the cracked hashes and create a New sheet on **LibreOffice Calc** , then paste it there.

![](https://i.imgur.com/odxoJ6z.png)

![](https://i.imgur.com/OOq0d62.png)


## **Performing a Vertical Lookup**

Now we want to lookup these hashes on each table we can watch this video to understand better

**Ooops, Looks like our Video didn't pop up, well you can View-Page source to see the magic ⚡**
![](https://github.com/sec-fortress/sec-fortress.github.io/blob/main/2023-09-25%2016-52-47.mp4)


## **Manual Method**

When it comes to sorting out the usernames and passwords we can do that in `Hashcat` also. Instead of just copying the NT part of the hash and putting it into a file, copy everything

**_Example :_** 

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:920ae267e048417fcfe00f49ecbd4b33:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DC=marvel,DC=local\pparker:1103:aad3b435b51404eeaad3b435b51404ee:c39f2beb3d2ec06a62cb887fb391dee0:::
 -Path DC=marvel,DC=local\fcastle:1104:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
 -Path DC=marvel,DC=local\tstark:1105:aad3b435b51404eeaad3b435b51404ee:d03b572b319e335ecd3e793412a28524:::
 -Path DC=marvel,DC=local\sqlservice:1106:aad3b435b51404eeaad3b435b51404ee:f4ab68f27303bcb4024650d8fc5f973a:::
hawkeye:1111:aad3b435b51404eeaad3b435b51404ee:43460d636f269c709b20049cee36ae7a:::
```

**_and in hashcat run the command :_**

```shell
$ hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt --show --username --outfile-format 2 | sort
```

**_The end result was :_**

```shell
$ hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt --show --username --outfile-format 2 | sort

 -Path DC=marvel,DC=local\fcastle:Password1
 -Path DC=marvel,DC=local\pparker:Password2
 -Path DC=marvel,DC=local\sqlservice:MYpassword123#
Administrator:P@$$w0rd!
hawkeye:Password1@
```

Just another way to do it. a bit quicker and if someone doesn't have **excel** or **LibreOffice Calc** in handy...


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
