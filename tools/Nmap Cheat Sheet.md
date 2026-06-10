# Nmap Cheat Sheet

## Quick Scans

- `nmap ip` - basic scan
- `nmap -sV ip` - detect service versions
- `nmap -sC -sV ip` - default scripts + service versions
- `nmap -A ip` - aggressive scan: OS, versions, scripts, traceroute
- `nmap -F ip` - fast scan of common ports

## Targets

- `nmap 192.168.1.10` - single host
- `nmap 192.168.1.10 192.168.1.11` - multiple hosts
- `nmap 192.168.1.1-254` - IP range
- `nmap 192.168.1.0/24` - subnet scan
- `nmap -iL targets.txt` - scan targets from file

## Host Discovery

- `nmap -sn 192.168.1.0/24` - ping sweep, no port scan
- `nmap -Pn ip` - skip host discovery, treat host as up
- `nmap -n ip` - skip DNS resolution

## Ports

- `nmap -p 80 ip` - scan one port
- `nmap -p 1-1000 ip` - scan port range
- `nmap -p- ip` - scan all TCP ports
- `nmap -p 22,80,443 ip` - scan selected ports
- `nmap --top-ports 100 ip` - scan top 100 ports

## Scan Types

- `nmap -sS ip` - TCP SYN scan
- `nmap -sT ip` - TCP connect scan
- `nmap -sU ip` - UDP scan
- `nmap -sA ip` - TCP ACK scan

## OS and Version Detection

- `nmap -O ip` - OS detection
- `nmap --osscan-guess ip` - more aggressive OS guessing
- `nmap -sV --version-all ip` - stronger version detection

## NSE Scripts

- `nmap -sC ip` - default safe scripts
- `nmap --script=banner ip` - banner grabbing
- `nmap --script=http-title -p 80,443 ip` - web titles
- `nmap --script=vuln ip` - vulnerability scripts
- `nmap --script=http-enum -p 80,443 ip` - enumerate web paths

## Timing and Speed

- `nmap -T3 ip` - normal timing
- `nmap -T4 ip` - faster scan
- `nmap --min-rate 1000 ip` - send at least 1000 packets/sec
- `nmap --max-retries 2 ip` - reduce retries

## Output

- `nmap -oN scan.txt ip` - normal output
- `nmap -oX scan.xml ip` - XML output
- `nmap -oA scan ip` - save normal, grepable, and XML output
