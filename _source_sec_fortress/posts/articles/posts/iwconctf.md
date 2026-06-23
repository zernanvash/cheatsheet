# **IWCONCTF 2023**

IWCON CTF 2023, is the first ever CTF hosted by [**IWCON**](https://iwcon.live/). Me and my team [**@SacredShell**](https://ctftime.org/team/222957) manage to secure 37th place out of 138 teams, This is a huge opportunity for me as i was able to carry the team as a **captain** and learnt alot also, through various challenges. Here is a detailed writeup of all challenges i solved 😆

![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/968c0310-b650-4687-af01-ab6fdfaa960f)


# **Warmup**


### **Socialize**


Navigating to the [discord](https://discord.gg/H7sQx76n) server we have this `iwconctf` channel created already


![](https://i.imgur.com/YxLPTNi.png)

Clicking it gives us the first flag



![](https://i.imgur.com/u1feGAv.png)


### **runme**

We have a `runme.class` file, in which we can go ahead and download


![](https://i.imgur.com/kbD6iNo.png)


Sine we can't just compile a `.class` file because it contains Java bytecode to run on a JVM, Read more from [here](https://unix.stackexchange.com/questions/604163/how-do-i-run-these-class-files), we can go ahead and compile using this website [https://www.decompiler.com/](https://www.decompiler.com/) 


![](https://i.imgur.com/GNa7Ces.png)


After compiling it, go ahead and save the file as `iwcon.java` because In Java, the name of the Java file should match the name of the public class defined within that file


![](https://i.imgur.com/mj6hq5V.png)


Now do this, to get our flag on your terminal 


```bash
~$ javac iwcon.java
~$ java iwcon
```


Incase you don't have `javac` or you get an error, then you need to do the below to install a more updated version of `java` 

```bash

wget "https://download.oracle.com/java/20/archive/jdk-20_linux-x64_bin.rpm"

sudo rpm -ivh jdk-20_linux-x64_bin.rpm  --nodeps
```

Hmmm, but i noticed we still don't have a flag 😭



![](https://i.imgur.com/NesgFsL.png)




To obtain the decoded flag, we can use the `get_flag` method. Modify the `main` method to call `get_flag` and print the result, we can go ahead and replace the `iwcon.java` file with this content:


```java
import java.util.Arrays;
import java.util.Base64;

public class iwcon {
   public static String get_flag() {
      byte[] var0 = "YPSiRhFjpXbIfgVc]NnHoeWlJ_mOEUQT[L`^kKGMda\\Z".getBytes();
      byte[] var1 = "c54h1dW2z1yVNTdfzRITS9MJMnj53ByM3Xz0D7azN9Xe".getBytes();
      byte[] var2 = new byte[var1.length];

      for(int var3 = 0; var3 < var1.length; ++var3) {
         var2[var3] = var1[var0[var3] - 69];
      }

      System.out.println(Arrays.toString(Base64.getDecoder().decode(var2)));
      return new String(Base64.getDecoder().decode(var2));
   }

   public static void main(String[] var0) {
      String decodedFlag = get_flag();
      System.out.println("Decoded Flag: " + decodedFlag);
   }
}     
```



Run the commands again and you should have the flag

![](https://i.imgur.com/a304Sx6.png)


# **MISC**


### **Decrypt the Hidden Message**

We are given a `.jpeg` file to analyze


![](https://i.imgur.com/R4MhzP6.png)


Running the `file` command on this file, we got the flag

```bash
file hidden.jpeg
```


![](https://i.imgur.com/HzPBK6B.png)



### **D3CODE2**



We are giving a `TXT` file with the following content

![](https://i.imgur.com/TIFscex.png)

Passing the content to **Cyberchef** gave us a morse code ouput

![](https://i.imgur.com/D1KOl6h.png)


Then from `morse code` to `Hex` and from `Hex` to `base64`, which gives us the flag


# **CRYPTO**

### **Rota23r**

We are given this statement

![](https://i.imgur.com/XaOhL7G.png)


Converting from `rot13` tells us to read the **rules** page


![](https://i.imgur.com/v70SHJA.png)


Navigating to `https://ctf.iwcon.live/rules` and viewing **page-source** we have this


![](https://i.imgur.com/gDwpAAT.png)



After sorting it out, i noticed it is also a `rot13` encoded text

![](https://i.imgur.com/egbK3yA.png)


The text says `M0V_M3_T0_G3T_TH3_FL4G`, Go ahead and submit it, `IWCON{M0V_M3_T0_G3T_TH3_FL4G}` 

![](https://i.imgur.com/lGXqjr3.png)






### **Survival**


We are given this hash -:

![](https://i.imgur.com/DkPj4Y6.png)


After various enumeration i found out it uses "**Weak Password Encryption in Argus Surveillance DVR 4.0**"


![](https://i.imgur.com/ZCmfU7I.png)



Got a script to decrypt this hash from [here](https://github.com/s3l33/CVE-2022-25012/blob/main/CVE-2022-25012.py), Then ran it and got our flag


![](https://i.imgur.com/BtdXC73.png)


### **Triple Trouble**

We are given a password hash to decrypt

```
Crack me if you can :P

Password Hash: 244127784dcb989c2e1d569837e3de17

Flag Format: IWCON{password}
```


After several hours of enumeration i decided to use the challenge name as a hint "**Triple Trouble**", Meaning this password was hashed three times using `MD5`

![](https://i.imgur.com/YZ04RGq.png)

Then with the little help of **AI** 😂, i made this python script and was able to reverse the hash

```python
import hashlib

def triple_md5(input_str):
    hash_result = hashlib.md5(input_str.encode()).hexdigest()
    hash_result = hashlib.md5(hash_result.encode()).hexdigest()
    hash_result = hashlib.md5(hash_result.encode()).hexdigest()
    return hash_result

def crack_md5_hash(md5_hash, dictionary_file):
    with open(dictionary_file, 'r') as f:
        for word in f:
            word = word.strip()
            hashed_word = triple_md5(word)
            if hashed_word == md5_hash:
                return word
    return None

given_hash = "244127784dcb989c2e1d569837e3de17"
dictionary_file = "/usr/share/wordlists/rockyou.txt"  # Replace with the path to your dictionary file

password = crack_md5_hash(given_hash, dictionary_file)

if password:
    print(f"Password found: {password}")
else:
    print("Password not found.")
```


![](https://i.imgur.com/eyxB9BC.png)


Now go ahead and submit our flag



![](https://i.imgur.com/eEGCI4s.png)


### **IW-cl0ud**

For this challenge we are given this hint `Bucket: iwcon`


![](https://i.imgur.com/ZUIt4Su.png)


Immediately, my mind went to **s3 buckets**, we can use a tool called `cloud_enum`, Install with the following command


```bash
git clone https://github.com/initstring/cloud_enum  
cd cloud_enum  
virtualenv -p python3 .  
source bin/activate  
pip3 install -r requirements.txt
```


We can then run the tool with the following command

```bash
python3 cloud_enum.py -k iwcon --disable-azure --disable-gcp
```


![](https://i.imgur.com/lOd56Tv.png)


As we can see we have a zip file, downloading and unzipping this zip file gives us this `logss` directory with series of folders


![](https://i.imgur.com/uBUrHnC.png)


Using this command we can get our flag, this print all lines that don't match the following expression

```bash
cat */*|grep -v CRITICAL | grep -v ERROR | grep -v INFO | grep -v DEBUG|grep -v WARNING 
```


![](https://i.imgur.com/rMCgZTf.png)


We can then get the flag since it is in `base64`

![](https://i.imgur.com/SaFNfeH.png)

### **QueueAre**




![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/30d407e6-586f-417d-a219-00f33a6c6f2e)




<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>




