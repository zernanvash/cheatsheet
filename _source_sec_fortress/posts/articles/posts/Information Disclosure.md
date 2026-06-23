# Information Disclosure || Portswigger

***


### **Lab: Information disclosure in error messages**

We are given the task -:

![](https://i.imgur.com/TtSxRDs.png)


Intercepting request of one of the project page we have this page -:


![](https://i.imgur.com/n3XShi3.png)


Changing `productId=2` to `productId="fuzz"`, we truly have the server version disclosed, **"Apache Struts x xx.xx.xx"** .


![](https://i.imgur.com/T6n40xb.png)



### **Lab: Information disclosure on debug page**


We are given the task -:


![](https://i.imgur.com/WtwwNv2.png)


Viewing details on one of the product page we have this -:

![](https://i.imgur.com/2o5BHZ5.png)


Since we are looking for a **debug page**, we can view page source with `Ctrl+U`, Scrolling down we have a commented directory

![](https://i.imgur.com/wWpwvrK.png)


Navigating to this directory we have a **phpinfo.php** page, Do `Ctrl+F` and find the secret key


![](https://i.imgur.com/f83gtTA.png)



### **Lab: Source code disclosure via backup files**


We are given the task -:


![](https://i.imgur.com/lKhICiX.png)



Since we are looking for **backup files** , we need to run a dir/file bruteforce, you can use `dirsearch`.


![](https://i.imgur.com/UtsCpFL.png)



Great !!. we found a `/backup` directory, Navigating there we have -:


![](https://i.imgur.com/BwaDd1T.png)


Navigating to `/backup/ProductTemplate.java.bak` we have the hard-coded database password

![](https://i.imgur.com/q39RnUg.png)


### **Lab: Authentication bypass via information disclosure**


We are given the task -:


![](https://i.imgur.com/XaR9GVT.png)


**Note:** We can use this simple python 3 [script](https://github.com/frank-leitner/portswigger-websecurity-academy/blob/main/06_information_disclosure/Authentication_bypass_via_information_disclosure/script.py) by [Frank Leitner](https://github.com/frank-leitner) to solve the lab quickly


![](https://i.imgur.com/gxxaXwa.png)



Using `dirsearch` to check for directories, we have a lot of `/admin` giving status code 401


![](https://i.imgur.com/esgnMXL.png)


A quick google search on status code `404` -:


![](https://i.imgur.com/AnQIufX.png)



Navigating to `/admin` we truly have this message


![](https://static.wixstatic.com/media/5840e3_89b72515915b40438a6b7d2419b93e56~mv2.png/v1/fill/w_740,h_277,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/5840e3_89b72515915b40438a6b7d2419b93e56~mv2.png)



Intercepting request and changing the **HTTP header** from `GET` to `TRACE` gives us this output -:


![frank leitner image](https://github.com/frank-leitner/portswigger-websecurity-academy/blob/main/06_information_disclosure/Authentication_bypass_via_information_disclosure/img/TRACE.png?raw=true)


Nice, we have a new header so we can just always add this header to every of our request with the `Match and Replace` rule, we can use `127.0.0.1` as the content to trick the application to believe that the request was originated from `localhost`


![](https://i.imgur.com/TrsdTnA.png)



Sending the request again with `GET` **HTTP header** and the `X-Custom-IP-Authorization` as `127.0.0.1` gives us an admin account page


![](https://i.imgur.com/NZLWfjJ.png)


Go ahead and delete user **carlos** to solve the lab


![](https://i.imgur.com/GXskPga.png)



### **Lab: Information disclosure in version control history**


We are given the task -:


![](https://i.imgur.com/Ua3WufJ.png)


Performing a dir/file bruteforce we found a `/.git` directory


![](https://i.imgur.com/eELKPrJ.png)


[...............]

![](https://i.imgur.com/LVImdzf.png)


We can download the content of `/.git` with `wget` 


```bash
$ wget --mirror -I .git https://0a41003a042095338382b403004b00c6.web-security-academy.net/.git/
```


![](https://i.imgur.com/Rimo1WV.png)

Change directory to where the files where downloaded to, you should see a hidden **.git** directory run the following command to check for deleted files -:


```bash
$ git status
```


![](https://i.imgur.com/0qS64zk.png)

Recover deleted files with the command -:


```bash
$ git restore .
```


![](https://i.imgur.com/gLtYnaD.png)


But as you can see we don't have the admin password yet, this is because we need to inspect the git log and find an  commit messages to give us leads

```bash
$ git log
```

![](https://i.imgur.com/YaSOw4F.png)


Since we now have the commit hash, we can now read each commit


```bash
$ git checkout <hash> .
```



![](https://i.imgur.com/meNfW0p.png)


We can also use the `git show` command also


![](https://i.imgur.com/0I8x4sZ.png)


Login with `Administrator:ex3s31i9uh9wtklzr8d1` and navigate to the **Admin Panel** then delete User **carlos**


![](https://i.imgur.com/9A9RE4C.png)


GG, Have fun 🤟🥳



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
