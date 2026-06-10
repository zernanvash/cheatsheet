# Networking

Network support commands for recon, packet inspection, and lab automation.

## Interface And Routes

```bash
ip addr
ip route
ip neigh
route -n
```

## Packet Capture

```bash
tcpdump -i tun0 -nn
tcpdump -i tun0 host target
tcpdump -i tun0 port 80 -A
tcpdump -i tun0 -w capture.pcap
```

## Responder

```bash
responder -I tun0
responder -I eth0 -A
```

Use passive analyze mode first when you only need visibility. Capture and relay workflows require explicit scope.

## Scapy

```python
from scapy.all import *

pkt = IP(dst="127.0.0.1")/ICMP()
ans = sr1(pkt, timeout=1)
print(ans.summary() if ans else "no reply")
```

Port probe:

```python
from scapy.all import *

ans = sr1(IP(dst="target")/TCP(dport=80, flags="S"), timeout=1)
print(ans.sprintf("%TCP.flags%") if ans else "no reply")
```

## Useful Netcat

```bash
nc -nv target port
nc -lvnp 4444
```

## Related

- [Passive Recon](Passive%20Recon.md)
- [SMTP](SMTP.md)
- [Post-Exploitation](Post-Exploitation.md)
