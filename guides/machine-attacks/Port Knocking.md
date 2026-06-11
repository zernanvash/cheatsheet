# Port Knocking

Use when scans show very few services, hints mention knocking, or source/files reveal a sequence of ports.

## Signals

- Only SSH/web closed or filtered despite challenge hints.
- Config files mention `knockd`, sequences, or firewall rules.
- Web/source clues are numeric and ordered.

## Main Path

```bash
nmap -p- --min-rate 5000 target
for p in 1111 2222 3333; do nc -zv target $p; done
nmap -p- --min-rate 5000 target
```

Run the sequence, then rescan immediately for newly opened services.

## Options To Try

- Try TCP and UDP knocks if the hint is unclear.
- Preserve order exactly; delays can matter.
- Watch packet direction and source IP if using VPN/tun interfaces.
- If new SSH opens, test recovered credentials or keys.

## Study Examples

- Sec-Fortress `Alzheimer`: port knocking unlocks the next service.
- HMV-style machines often hide this behind small web or file clues.
