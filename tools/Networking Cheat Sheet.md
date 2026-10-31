# Networking Cheat Sheet

A comprehensive, operational reference covering Enterprise & CCNA networking, IPv4 subnetting, routing protocols, Layer 2 switching, network security, infrastructure services, and automation.

---

## 📑 Quick Navigation

| Section | Focus Areas |
|---|---|
| [1. IPv4 Subnetting](#1-ipv4-subnetting) | CIDR table (/24–/32), hosts, block sizes, calculation formulas |
| [2. IPv4 Addressing](#2-ipv4-addressing) | Classes A–E, RFC 1918 private ranges, Loopback, APIPA |
| [3. IPv6 Fundamentals](#3-ipv6-fundamentals) | Scopes, EUI-64, SLAAC, DHCPv6 flags, Cisco IPv6 configuration |
| [4. Ports & Transport Layer](#4-ports--transport-layer) | Common TCP/UDP ports, 3-way handshake, TCP vs. UDP traits |
| [5. Cabling & Physical Ethernet](#5-cabling--physical-ethernet) | Copper (Cat5e/6/6a), Fiber (MMF/SMF), pinouts, PoE, Layer 1/2 faults |
| [6. Automation & Programmability](#6-automation--programmability) | REST verbs, HTTP codes, JSON, SDN architecture, NETCONF/RESTCONF, Ansible |
| [7. Wireless (802.11)](#7-wireless-80211) | 802.11a/b/g/n/ac/ax standards, 2.4 GHz channels, WPA2/WPA3, CAPWAP, WLC |
| [8. VLANs & 802.1Q Trunking](#8-vlans--8021q-trunking) | Access ports, 802.1Q trunking, native VLAN, DTP nonegotiate |
| [9. Spanning Tree Protocol (STP)](#9-spanning-tree-protocol-stp) | BID election, path costs, 802.1D vs RSTP states, PortFast, BPDU Guard |
| [10. EtherChannel & Discovery](#10-etherchannel--discovery) | LACP vs PAgP, port-channel configuration, CDP & LLDP timers |
| [11. Network Architecture](#11-network-architecture) | 2-tier collapsed core, 3-tier, spine-leaf, cloud models, hypervisors |
| [12. Essential Verification Commands](#12-essential-verification-commands) | Cisco IOS show commands for switching, routing, and discovery |
| [13. Route Selection & AD](#13-route-selection--ad) | Longest prefix match, Administrative Distance table, route codes |
| [14. Static & Default Routing](#14-static--default-routing) | Next-hop, default route, floating static backup, L3 switch routing |
| [15. OSPFv2 Single & Multi-Area](#15-ospfv2-single--multi-area) | Configuration, RID election, DR/BDR, timers, neighbor states |
| [16. Inter-VLAN Routing](#16-inter-vlan-routing) | Router-on-a-Stick (ROAS), Layer 3 SVIs, routed ports |
| [17. First Hop Redundancy (FHRP)](#17-first-hop-redundancy-fhrp) | HSRP v1/v2, priorities, preemption, VRRP, GLBP |
| [18. NAT & PAT](#18-nat--pat) | Static 1:1 NAT, Dynamic Pool NAT, PAT (Overload), Inside/Outside logic |
| [19. Infrastructure Services & QoS](#19-infrastructure-services--qos) | Cisco DHCP server, DHCP relay, Syslog severity levels, SNMP, DSCP QoS |
| [20. Port Security & Layer 2 Defense](#20-port-security--layer-2-defense) | Sticky MAC, violation modes (shutdown/restrict/protect), DHCP Snooping, DAI |
| [21. Access Control Lists (ACLs)](#21-access-control-lists-acls) | Standard vs Extended ranges, wildcard masks, interface & VTY placement |
| [22. Device Access & AAA](#22-device-access--aaa) | SSH hardening, RADIUS vs TACACS+, 802.1X, IPsec protocols |

---

## 1. IPv4 Subnetting

### Subnet Reference Table (/24 to /32)

| Prefix | Subnet Mask | Block Size | Usable Hosts | Use Case |
|---|---|---|---|---|
| **/24** | `255.255.255.0` | 256 | 254 | Standard LAN segment |
| **/25** | `255.255.255.128` | 128 | 126 | Split /24 into 2 subnets |
| **/26** | `255.255.255.192` | 64 | 62 | Medium department / DMZ |
| **/27** | `255.255.255.224` | 32 | 30 | Small office / server rack |
| **/28** | `255.255.255.240` | 16 | 14 | Small subnet / appliance group |
| **/29** | `255.255.255.248` | 8 | 6 | Public IP block / WAN cluster |
| **/30** | `255.255.255.252` | 4 | 2 | Point-to-point link |
| **/31** | `255.255.255.254` | 2 | 2 | Point-to-point link (RFC 3021, no bcast/net ID) |
| **/32** | `255.255.255.255` | 1 | 1 | Single host / Loopback interface |

### Subnet Calculation Formulas

- **Usable Hosts:** `2^h - 2` (where `h` = number of host bits remaining)
- **Total Subnets Created:** `2^n` (where `n` = number of borrowed subnet bits)
- **Block Size (Magic Number):** `256 - interesting octet value`

---

## 2. IPv4 Addressing

### Address Classes

| Class | First Octet Range | Default Prefix | Purpose / Note |
|---|---|---|---|
| **Class A** | `1` – `126` | `/8` (`255.0.0.0`) | Very large enterprise networks |
| **Class B** | `128` – `191` | `/16` (`255.255.0.0`) | Medium to large networks |
| **Class C** | `192` – `223` | `/24` (`255.255.255.0`) | Small LANs |
| **Class D** | `224` – `239` | N/A | Multicast groups (OSPF, RIP, HSRP, etc.) |
| **Class E** | `240` – `255` | N/A | Experimental / Reserved |

### Private & Special IPv4 Ranges

- **RFC 1918 Private Ranges:**
  - Class A: `10.0.0.0/8` (`10.0.0.0` – `10.255.255.255`)
  - Class B: `172.16.0.0/12` (`172.16.0.0` – `172.31.255.255`)
  - Class C: `192.168.0.0/16` (`192.168.0.0` – `192.168.255.255`)
- **Loopback:** `127.0.0.0/8` (Local host stack testing, e.g. `127.0.0.1`)
- **APIPA (Automatic Private IP Addressing):** `169.254.0.0/16` (Assigned by OS when DHCP discovery fails)

---

## 3. IPv6 Fundamentals

### Address Scopes & Types

| Prefix | Scope | Description |
|---|---|---|
| `2000::/3` | **Global Unicast** | Globally routable public IPv6 addresses |
| `FE80::/10` | **Link-Local** | Non-routable; valid only on local Layer 2 link |
| `FC00::/7` | **Unique-Local** | Private IPv6 addresses (equivalent to RFC 1918) |
| `FF00::/8` | **Multicast** | Multicast traffic; replaces IPv4 broadcast |
| `::1` | **Loopback** | Localhost IPv6 loopback address |
| `::` | **Unspecified** | Indicates absence of an address (DHCP request) |
| `::/0` | **Default Route** | IPv6 default quad-zero route |
| `FF02::1` | **All Nodes** | Reaches every IPv6 device on the local link |
| `FF02::2` | **All Routers** | Reaches every IPv6 router on the local link |

### EUI-64 Interface Identifier Generation

1. Split 48-bit MAC address in half (24 bits / 24 bits).
2. Insert `FFFE` in the middle to make it 64 bits.
3. Invert the 7th bit (Universal/Local bit) of the first byte.

### Address Auto-Configuration

- **SLAAC (Stateless Address Autoconfiguration):** Client sends Router Solicitation (`RS`), router answers with Router Advertisement (`RA`).
- **RA Flags:**
  - `M=1` (Managed): Stateful DHCPv6 (DHCP server assigns IPv6 address and DNS).
  - `O=1` (Other): Stateless DHCPv6 (SLAAC assigns address, DHCP supplies DNS/domain).

### Cisco IPv6 Configuration

```cisco
! Enable IPv6 routing globally
ipv6 unicast-routing

interface GigabitEthernet0/0
 ipv6 address 2001:db8:1::1/64
 ipv6 address fe80::1 link-local
 no shutdown

! IPv6 Default Static Route
ipv6 route ::/0 2001:db8:1::2
```

---

## 4. Ports & Transport Layer

### Well-Known TCP & UDP Services

| Protocol | Port | Description |
|---|---|---|
| **FTP** | `20` (Data) / `21` (Control) | File Transfer Protocol |
| **SSH** | `22` | Secure Shell |
| **Telnet** | `23` | Unencrypted remote terminal |
| **SMTP** | `25` | Simple Mail Transfer Protocol |
| **TACACS+** | `49` | Cisco AAA security protocol (TCP) |
| **DNS** | `53` | UDP for queries; TCP for zone transfers (`>512` bytes) |
| **DHCP** | `67` (Server) / `68` (Client) | Dynamic Host Configuration Protocol (UDP) |
| **TFTP** | `69` | Trivial File Transfer Protocol (UDP) |
| **HTTP** | `80` | Hypertext Transfer Protocol |
| **NTP** | `123` | Network Time Protocol (UDP) |
| **SNMP** | `161` (Poll) / `162` (Trap) | Simple Network Management Protocol (UDP) |
| **BGP** | `179` | Border Gateway Protocol (TCP) |
| **HTTPS** | `443` | HTTP over TLS/SSL |
| **Syslog** | `514` | System event logging (UDP) |
| **RADIUS** | `1812` (Auth) / `1813` (Acct) | Remote Authentication Dial-In User Service (UDP) |

### Transport Characteristics

- **TCP (Transmission Control Protocol):** Connection-oriented, 3-way handshake (`SYN` > `SYN-ACK` > `ACK`), sequenced segments, reliable acknowledgement, windowing / flow control.
- **UDP (User Datagram Protocol):** Connectionless, no acknowledgement or flow control, minimal packet header overhead, optimal for real-time traffic (VoIP, streaming, DNS queries).

---

## 5. Cabling & Physical Ethernet

### Physical Media Standards

| Standard | Cable Type | Max Distance | Notes |
|---|---|---|---|
| **10/100/1000BASE-T** | UTP Cat5e / Cat6 | 100 m | Standard twisted pair copper |
| **10GBASE-T** | Cat6a (100 m) / Cat6 (55 m) | 100 m / 55 m | 10 Gigabit Ethernet copper |
| **1000BASE-SX** | MMF (Multi-Mode Fiber) | 550 m | Short wavelength (850 nm) fiber |
| **1000BASE-LX** | SMF (Single-Mode Fiber) | 5 km | Long wavelength (1310 nm) fiber |
| **10GBASE-SR** | MMF (Multi-Mode Fiber) | 300 m | 10G Short-reach optical link |
| **10GBASE-LR** | SMF (Single-Mode Fiber) | 10 km | 10G Long-reach optical link |

### Cable Pinouts & Rules

- **Straight-Through Cable:** Unlike devices (PC to Switch, Router to Switch).
- **Crossover Cable:** Like devices (Switch to Switch, Router to Router, PC to PC).
  > Modern switches automatically detect pinouts using **Auto-MDIX**.

### Power over Ethernet (PoE)

- **802.3af (PoE):** Up to `15.4 W` per port (delivers ~12.95 W to device).
- **802.3at (PoE+):** Up to `30 W` per port (delivers ~25.5 W to device).
- **802.3bt (PoE++ / 4PPoE):** Up to `60 W` (Type 3) or `90 W` (Type 4).

### Layer 1 & 2 Diagnostics

- **CRC Errors / Runts:** Typically caused by faulty physical cabling, loose connectors, or electrical interference.
- **Late Collisions:** Hallmarked indicator of a **duplex mismatch** (one side half-duplex, other full-duplex).
- **Ethernet Frame Boundaries:**
  - Minimum Frame Size: `64 bytes` (Frames `< 64 B` are dropped as "runts").
  - Maximum Frame Size (MTU): `1500 bytes` payload (Total frame `1518 bytes`).
  - MAC Address Length: `48 bits` (6 bytes, hexadecimal).

---

## 6. Automation & Programmability

### REST APIs & HTTP Verbs

| Method | CRUD Action | Idempotent | Description |
|---|---|---|---|
| `GET` | Read | Yes | Retrieve resource data without modifying state |
| `POST` | Create | No | Create a new subordinate resource |
| `PUT` | Replace | Yes | Overwrite or replace an entire target resource |
| `PATCH` | Modify | No | Apply partial modifications to a resource |
| `DELETE` | Remove | Yes | Delete target resource |

### Common HTTP Status Codes

- `200 OK`: Request succeeded.
- `201 Created`: Resource successfully created.
- `400 Bad Request`: Client syntax / validation error.
- `401 Unauthorized`: Missing or invalid authentication credentials.
- `403 Forbidden`: Authenticated, but lacking permission.
- `404 Not Found`: Target resource does not exist.

### Data Formats & Network Programmability

- **JSON (JavaScript Object Notation):**
  - Key-value object: `{"interface": "GigabitEthernet0/1", "enabled": true}`
  - Arrays: `["vlan10", "vlan20", "vlan30"]`
- **Software-Defined Networking (SDN):**
  - **Northbound API:** Connects SDN Controller to business applications / orchestration scripts (usually REST).
  - **Southbound API:** Connects SDN Controller to physical switches & routers (e.g. NETCONF, OpenFlow, RESTCONF).
- **Network Management Protocols:**
  - **NETCONF:** Transport over `SSH Port 830`, payload encoded in `XML`.
  - **RESTCONF:** Transport over `HTTPS Port 443`, payload encoded in `JSON` or `XML`.
- **Configuration Management Tools:**
  - **Ansible:** Agentless, push model, configured using YAML playbooks over SSH.
  - **Puppet / Chef:** Agent-based, pull model, runs manifests (Puppet) or recipes (Chef).

---

## 7. Wireless (802.11)

### 802.11 Wi-Fi Standards

| Standard | Commercial Name | Frequency | Max Data Rate |
|---|---|---|---|
| **802.11b** | Legacy | 2.4 GHz | 11 Mbps |
| **802.11a** | Legacy | 5 GHz | 54 Mbps |
| **802.11g** | Legacy | 2.4 GHz | 54 Mbps |
| **802.11n** | **Wi-Fi 4** | 2.4 GHz / 5 GHz | 600 Mbps |
| **802.11ac** | **Wi-Fi 5** | 5 GHz | 6.9 Gbps |
| **802.11ax** | **Wi-Fi 6** | 2.4 GHz / 5 GHz | 9.6 Gbps |
| **Wi-Fi 6E** | Extension | 6 GHz | 9.6 Gbps |

### 2.4 GHz Spectrum & Channels

- Non-overlapping 20 MHz channels in the 2.4 GHz band: **1, 6, and 11**.

### Wireless Security & Architecture

- **Security Standards:**
  - **WPA2:** Uses `AES-CCMP` encryption.
  - **WPA3:** Uses `SAE` (Simultaneous Authentication of Equals) to prevent offline dictionary attacks.
  - **Enterprise Mode:** Requires `802.1X / EAP` with a centralized RADIUS server.
- **CAPWAP (Control and Provisioning of Wireless Access Points):**
  - Control channel: `UDP 5246`
  - Data channel: `UDP 5247`
- **AP Operating Modes:** Local (central switched), FlexConnect (remote branch with local switching), Monitor, Sniffer, Rogue Detector, Bridge.
- **Switchport Modes for APs:**
  - Lightweight AP (LAP): Switchport configured as **Access** (CAPWAP encapsulates all VLANs).
  - Autonomous AP: Switchport configured as **Trunk** (native VLAN for management, tagged VLANs for SSIDs).
- **WLAN Definition:** Defined on the Wireless LAN Controller (WLC) as `SSID + VLAN Mapping + Security Policy`.

---

## 8. VLANs & 802.1Q Trunking

### Access Port Configuration

```cisco
vlan 10
 name USERS
vlan 20
 name VOICE

interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 spanning-tree portfast
```

### 802.1Q Trunk Port Configuration

```cisco
interface GigabitEthernet0/24
 switchport trunk encapsulation dot1q   ! Required on Layer 3 / older Catalyst switches
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 switchport trunk native vlan 99
 switchport nonegotiate                 ! Disables Dynamic Trunking Protocol (DTP)
```

### VLAN Rules & Encapsulation

- **Normal VLAN Range:** `1` – `1005` (Saved in `vlan.dat` flash memory; 1002–1005 reserved).
- **Extended VLAN Range:** `1006` – `4094` (Saved in running-config; requires VTP transparent mode in older switches).
- **802.1Q Tag:** Inserts a **4-byte header** into the standard Ethernet frame.
- **Native VLAN:** Frames belonging to the native VLAN are transmitted **untagged** over the trunk.

---

## 9. Spanning Tree Protocol (STP)

### Root Bridge & Root Port Election

1. **Root Bridge Election:** Switch with the **lowest Bridge ID (BID)** wins.
   - `BID = Priority (Default 32768 + VLAN ID) + MAC Address`.
2. **Root Port Selection (on non-root switches):**
   - Lowest Root Path Cost > Lowest Sender BID > Lowest Sender Port ID.
3. **Port Path Costs:**
   - `10 Mbps`: Cost 100
   - `100 Mbps`: Cost 19
   - `1 Gbps`: Cost 4
   - `10 Gbps`: Cost 2

### STP States & Timers

- **Classic 802.1D Port States:**
  - `Blocking` (20s Max Age) > `Listening` (15s Forward Delay) > `Learning` (15s Forward Delay) > `Forwarding` (~50s total convergence).
- **STP Timers:** Hello: `2s`, Max Age: `20s`, Forward Delay: `15s`.
- **RSTP (802.1w) Port States:** `Discarding` > `Learning` > `Forwarding`.
- **RSTP Port Roles:** Root, Designated, Alternate (backup for root port), Backup (backup for designated port).

### Cisco STP Configuration

```cisco
! Enable Rapid-PVST+
spanning-tree mode rapid-pvst

! Configure Root Bridge Priorities
spanning-tree vlan 10 root primary        ! Lowers priority to 24576
spanning-tree vlan 10 root secondary      ! Lowers priority to 28672
spanning-tree vlan 10 priority 4096       ! Must be configured in increments of 4096

! Edge Port Protection
interface range GigabitEthernet0/1-10
 spanning-tree portfast                  ! Immediately transitions port to Forwarding
 spanning-tree bpduguard enable          ! Shuts down port (err-disable) if BPDU received
```

---

## 10. EtherChannel & Discovery

### Link Aggregation Configuration

```cisco
interface range GigabitEthernet0/1 - 2
 channel-group 1 mode active
 exit

interface Port-channel 1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
```

### EtherChannel Negotiation Protocols

| Protocol | Standard | Channel Modes | Notes |
|---|---|---|---|
| **LACP** | IEEE 802.3ad (Open) | `active` / `passive` | `active` initiates; at least one side must be `active` |
| **PAgP** | Cisco Proprietary | `desirable` / `auto` | `desirable` initiates; at least one side must be `desirable` |
| **Static** | N/A | `on` | Forces channel; no negotiation packets |

> **Prerequisites:** Speed, Duplex, Switchport Mode (Access/Trunk), Native VLAN, and Allowed VLAN list **must match** across all member interfaces. Maximum 8 active links per bundle.

### Device Discovery Protocols

- **CDP (Cisco Discovery Protocol):** Cisco proprietary, Layer 2 protocol.
  - Timers: Hello `60s`, Holdtime `180s`.
  - Commands: `cdp run` (global), `cdp enable` (interface), `show cdp neighbors [detail]`.
- **LLDP (Link Layer Discovery Protocol):** IEEE 802.1AB open standard.
  - Timers: Hello `30s`, Holdtime `120s`.
  - Commands: `lldp run` (global), `show lldp neighbors [detail]`.

---

## 11. Network Architecture

### Hierarchical Campus & Data Center Models

- **2-Tier Collapsed Core:** Core and Distribution layers merged into one logical tier; connects directly to the Access tier. Best for small-to-medium offices.
- **3-Tier Design:**
  - **Core:** High-speed packet switching backbone (no packet filtering).
  - **Distribution:** Policy routing, VLAN termination, access control lists, and QoS boundary.
  - **Access:** Direct end-user device connectivity and port security.
- **Spine-Leaf:** Modern data center architecture providing equidistant, predictable latency for East-West traffic across servers.

### Cloud Computing Models & Virtualization

- **Cloud Service Models:**
  - **IaaS (Infrastructure as a Service):** Cloud provider manages hardware; customer manages OS, middleware, and applications (e.g. AWS EC2).
  - **PaaS (Platform as a Service):** Provider manages OS and runtime; customer manages app code (e.g. AWS Elastic Beanstalk).
  - **SaaS (Software as a Service):** Provider manages complete application stack (e.g. Microsoft 365, Google Workspace).
- **Hypervisors:**
  - **Type 1 (Bare-Metal):** Runs directly on physical hardware (VMware ESXi, Microsoft Hyper-V, KVM).
  - **Type 2 (Hosted):** Runs on top of a host operating system (VMware Workstation, VirtualBox).

---

## 12. Essential Verification Commands

```cisco
! Switching & Layer 2 Verification
show vlan brief
show interfaces trunk
show interfaces status
show mac address-table
show spanning-tree
show etherchannel summary

! Discovery Protocols
show cdp neighbors
show cdp neighbors detail
show lldp neighbors

! IP & Interface Verification
show ip interface brief
show ip route
show running-config
```

---

## 13. Route Selection & Administrative Distance

### Route Selection Precedence

When a router evaluates multiple routes to a destination, it chooses in this exact order:
1. **Longest Prefix Match:** Most specific subnet mask wins (e.g. `/30` beats `/24`).
2. **Lowest Administrative Distance (AD):** Route source believability.
3. **Lowest Metric:** Cost calculation within the specific routing protocol.

### Administrative Distance (AD) Table

| Route Source | Administrative Distance (AD) | Metric Unit |
|---|---|---|
| **Directly Connected** | `0` | None |
| **Static Route** | `1` | Configurable |
| **eBGP (External BGP)** | `20` | Path attributes |
| **EIGRP (Internal)** | `90` | Bandwidth + Delay |
| **OSPF** | `110` | Cost (Reference Bandwidth / Interface Bandwidth) |
| **IS-IS** | `115` | Arbitrary cost |
| **RIP** | `120` | Hop count (Max 15 hops; 16 = unreachable) |
| **EIGRP (External)** | `170` | Bandwidth + Delay |
| **iBGP (Internal BGP)** | `200` | Path attributes |
| **Unreachable / Unknown** | `255` | Route will not be installed in routing table |

### Routing Table Codes

- `C`: Connected
- `L`: Local (`/32` host address on router interface)
- `S`: Static
- `O`: OSPF
- `D`: EIGRP
- `B`: BGP
- `R`: RIP

---

## 14. Static & Default Routing

```cisco
! Standard Static Route: ip route <dest-network> <netmask> <next-hop-ip>
ip route 10.1.0.0 255.255.255.0 192.168.1.2

! Quad-Zero Default Route (Gateway of Last Resort)
ip route 0.0.0.0 0.0.0.0 203.0.113.1

! Floating Static Route (Backup route with AD 200 > default AD 1)
ip route 10.1.0.0 255.255.255.0 192.168.9.2 200

! Enable IPv4 routing on Layer 3 Catalyst Switch
ip routing

! Verification
show ip route
show ip route static
show ip protocols
```

---

## 15. OSPFv2 (Open Shortest Path First)

### OSPFv2 Single-Area & Multi-Area Configuration

```cisco
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/0      ! Suppresses hello packets on user LAN
 default-information originate            ! Injects default route into OSPF
 auto-cost reference-bandwidth 1000       ! Updates reference BW to 1000 Mbps (1 Gbps)

! Interface-level OSPF alternative
interface GigabitEthernet0/1
 ip ospf 1 area 0
 ip ospf priority 100                     ! Adjusts DR election priority
 ip ospf network point-to-point           ! Skips DR/BDR election
```

### OSPF Architecture & Mechanics

- **Cost Formula:** `Reference Bandwidth / Interface Bandwidth` (Default reference BW = `100 Mbps`).
- **Hello / Dead Timers:**
  - Broadcast & Point-to-Point links: `10s / 40s`.
  - Non-Broadcast Multi-Access (NBMA): `30s / 120s`.
- **Multicast Addresses:**
  - `224.0.0.5`: All OSPF Routers.
  - `224.0.0.6`: All DR and BDR Routers.
  - IP Protocol: `89`.
- **DR / BDR Election:**
  1. Highest interface priority (Priority `0` = never eligible).
  2. Highest Router ID (RID).
- **Router ID (RID) Precedence:**
  1. Manually configured `router-id`.
  2. Highest IPv4 address on any active **Loopback** interface.
  3. Highest IPv4 address on any active **physical** interface.
- **Neighbor States:** `Down` > `Init` > `2-Way` (DR/BDR elected) > `ExStart` > `Exchange` > `Loading` > `Full`.
- **Adjacency Requirements (Must Match):** Area ID, Subnet & Subnet Mask, Hello & Dead intervals, Authentication keys, MTU size, and Stub area flags.
- **Verification:** `show ip ospf neighbor`, `show ip ospf interface brief`.

---

## 16. Inter-VLAN Routing

### Router-on-a-Stick (ROAS)

```cisco
interface GigabitEthernet0/0.10
 encapsulation dot1q 10
 ip address 10.0.10.1 255.255.255.0

interface GigabitEthernet0/0.20
 encapsulation dot1q 20
 ip address 10.0.20.1 255.255.255.0

interface GigabitEthernet0/0
 no ip address
 no shutdown
```

### Layer 3 Switch Switch Virtual Interface (SVI)

```cisco
ip routing

interface Vlan10
 ip address 10.0.10.1 255.255.255.0
 no shutdown

interface Vlan20
 ip address 10.0.20.1 255.255.255.0
 no shutdown
```

### Routed Port (Layer 3 Switch Physical Port)

```cisco
interface GigabitEthernet0/24
 no switchport
 ip address 10.0.0.1 255.255.255.0
 no shutdown
```

---

## 17. First Hop Redundancy Protocols (FHRP)

### HSRP (Hot Standby Router Protocol - Cisco)

```cisco
interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.0
 standby 1 ip 10.0.0.1                    ! Virtual default gateway IP
 standby 1 priority 110                   ! Default priority is 100
 standby 1 preempt                        ! Allows higher priority router to take over
```

### FHRP Protocol Comparison

| Feature | HSRP v1 | HSRP v2 | VRRP (RFC 5798) | GLBP |
|---|---|---|---|---|
| **Standard** | Cisco Proprietary | Cisco Proprietary | Open Standard | Cisco Proprietary |
| **Multicast IP** | `224.0.0.2` | `224.0.0.102` | `224.0.0.18` | `224.0.0.102` |
| **Transport** | UDP `1985` | UDP `1985` | IP Protocol `112` | UDP `3222` |
| **Default Timers**| Hello: 3s, Hold: 10s | Hello: 3s, Hold: 10s | Hello: 1s, Skew: ~3s | Hello: 3s, Hold: 10s |
| **Preemption** | Disabled by default | Disabled by default | Enabled by default | Disabled by default |
| **Active Nodes** | 1 Active, 1 Standby | 1 Active, 1 Standby | 1 Master, Backups | Active Load Balancing (up to 4 forwarders) |

---

## 18. NAT & PAT (Network Address Translation)

### NAT Types & Terminology

- **Inside Local:** Private IP assigned to the host on the internal network (e.g. `10.0.0.5`).
- **Inside Global:** Globally routable public IP representing the inside host to the outside (e.g. `203.0.113.5`).
- **Outside Local:** IP address of an outside host as known to the inside network.
- **Outside Global:** Actual public IP address allocated to the outside destination.

### Cisco NAT Configuration

```cisco
! 1. Static 1:1 NAT (Port Forwarding / DMZ Server)
ip nat inside source static 10.0.0.5 203.0.113.5

! 2. Dynamic NAT with IP Pool
ip nat pool PUB 203.0.113.10 203.0.113.20 netmask 255.255.255.0
access-list 1 permit 10.0.0.0 0.0.0.255
ip nat inside source list 1 pool PUB

! 3. PAT / NAT Overload (Most Common Internet Access Design)
access-list 1 permit 10.0.0.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

! Interface Designations
interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside

! Verification
show ip nat translations
show ip nat statistics
```

---

## 19. Infrastructure Services & QoS

### Cisco DHCP Server & Relay Agent

```cisco
! Exclude static IPs / gateways
ip dhcp excluded-address 10.0.0.1 10.0.0.10

! Define DHCP Pool
ip dhcp pool LAN_USERS
 network 10.0.0.0 255.255.255.0
 default-router 10.0.0.1
 dns-server 8.8.8.8 1.1.1.1
 domain-name lab.local
 lease 1 0 0                              ! 1 day lease

! DHCP Relay Agent (On Router Interface facing clients)
interface GigabitEthernet0/0
 ip helper-address 10.1.1.5               ! Forwards broadcast DHCP as unicast to server
```

- **DHCP DORA Process:**
  1. **Discover:** Client sends broadcast (`255.255.255.255`).
  2. **Offer:** Server responds with offered IP and options.
  3. **Request:** Client formally requests the offered IP (broadcast).
  4. **Acknowledge (ACK):** Server confirms lease.

### NTP & Syslog Logging

```cisco
ntp server 10.1.1.1
logging host 10.1.1.9
logging trap informational
```

### Syslog Severity Levels (0 – 7)

*Mnemonic:* **E**very **A**lley **C**at **E**ats **W**et **N**oodles **I**n **D**ublin

| Level | Severity Name | Description |
|---|---|---|
| **0** | **Emergency** | System is unusable |
| **1** | **Alert** | Immediate action needed |
| **2** | **Critical** | Critical conditions |
| **3** | **Error** | Error conditions |
| **4** | **Warning** | Warning conditions |
| **5** | **Notice** | Normal but significant conditions |
| **6** | **Informational** | Informational messages |
| **7** | **Debug** | Detailed output from debug commands |

### SNMP & Quality of Service (QoS)

- **SNMP Versions:**
  - `SNMPv2c`: Authenticates using unencrypted plaintext community strings (`ro` / `rw`).
  - `SNMPv3`: Secure; supports `noAuthNoPriv`, `authNoPriv`, and `authPriv` (MD5/SHA auth + DES/AES encryption).
- **QoS DSCP (Differentiated Services Code Point) Values:**
  - `EF` (Expedited Forwarding - DSCP 46): Voice traffic (low latency, low jitter).
  - `AF41` (Assured Forwarding - DSCP 34): Interactive video.
  - `BE` (Best Effort - DSCP 0): Standard bulk data traffic.

---

## 20. Port Security & Layer 2 Defense

### Switchport Port Security

```cisco
interface GigabitEthernet0/2
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
```

### Port Security Violation Modes

| Violation Mode | Drops Frames? | Increments Counter? | Logs Syslog/SNMP? | Disables Port? |
|---|---|---|---|---|
| **protect** | Yes | No | No | No (Silently drops traffic) |
| **restrict** | Yes | Yes | Yes | No |
| **shutdown** | Yes | Yes | Yes | Yes (`err-disable` state; default) |

### Layer 2 Mitigations: DHCP Snooping & DAI

```cisco
! Enable DHCP Snooping globally and per VLAN
ip dhcp snooping
ip dhcp snooping vlan 10

! Enable Dynamic ARP Inspection (DAI)
ip arp inspection vlan 10

! Trust Uplink Ports (towards legitimate DHCP server / router)
interface GigabitEthernet0/24
 ip dhcp snooping trust
 ip arp inspection trust
```

---

## 21. Access Control Lists (ACLs)

### ACL Number Ranges & Placement

| ACL Type | Number Ranges | Filtering Capabilities | Recommended Placement |
|---|---|---|---|
| **Standard** | `1` – `99`, `1300` – `1999` | Source IPv4 address only | Place **closest to destination** |
| **Extended** | `100` – `199`, `2000` – `2699` | Source IP, Dest IP, Protocol, Ports | Place **closest to source** |

### Extended Named ACL Configuration

```cisco
ip access-list extended SECURE_WEB
 permit tcp 10.0.0.0 0.0.0.255 any eq 443
 permit tcp 10.0.0.0 0.0.0.255 any eq 80
 deny ip any any                          ! (Implicit deny exists by default)

! Apply to Interface
interface GigabitEthernet0/0
 ip access-group SECURE_WEB in

! Secure Remote VTY Lines using Standard ACL
access-list 10 permit 192.168.1.0 0.0.0.255
line vty 0 15
 access-class 10 in
```

### Wildcard Mask Rules

- Wildcard mask is the inverse of the subnet mask (`255.255.255.255 - Subnet Mask`).
  - Subnet `255.255.255.0` -> Wildcard `0.0.0.255`
  - `host 10.0.0.1` -> `10.0.0.1 0.0.0.0`
  - `any` -> `0.0.0.0 255.255.255.255`
- **Evaluation Order:** Top-to-bottom, first match terminates processing, implicit deny at the end of every ACL. Limit 1 ACL per interface, per direction (`in`/`out`), per protocol.

---

## 22. Device Access & AAA

### Device Hardening & SSH Setup

```cisco
! Global Passwords & Service Encryption
enable secret StrongPassword123!
service password-encryption

! Domain name required for cryptographic key generation
ip domain-name lab.local
crypto key generate rsa modulus 2048

! Enforce SSHv2 and local authentication
ip ssh version 2
username admin secret AdminSecurePassword456!

line vty 0 15
 transport input ssh
 login local
 exec-timeout 10 0
```

### AAA Authentication Protocols

- **RADIUS (Remote Authentication Dial-In User Service):**
  - Ports: `UDP 1812` (Authentication) / `UDP 1813` (Accounting).
  - Open IETF standard.
  - Combines Authentication and Authorization; encrypts **only the password** field in the packet.
- **TACACS+ (Terminal Access Controller Access-Control System Plus):**
  - Port: `TCP 49`.
  - Cisco proprietary.
  - Separates **A**uthentication, **A**uthorization, and **A**ccounting into distinct functions.
  - Encrypts the **entire packet body**.

### 802.1X Port-Based Authentication

- **Supplicant:** Client workstation running 802.1X software.
- **Authenticator:** Switch or Wireless Access Point enforcing port security.
- **Authentication Server:** Centralized RADIUS / Cisco ISE server verifying user credentials.

### IPsec Framework Protocols

- **ESP (Encapsulating Security Payload):** IP Protocol `50` (provides confidentiality, integrity, and authentication).
- **AH (Authentication Header):** IP Protocol `51` (provides integrity and authentication; **no encryption**).
- **IKE (Internet Key Exchange):** UDP Port `500` (negotiates security associations and key exchange).

---

## 🔗 Related Resources

- [Linux Networking & Packet Analysis](Networking.md) — Linux network commands, routes, tcpdump, Scapy, and Responder
- [Nmap Cheat Sheet](Nmap%20Cheat%20Sheet.md) — Host discovery and port scanning syntax
- [Wireless Cheat Sheet](Wireless.md) — Wi-Fi capture, inspection, and WPA cracking
- [0xrefs Interactive Reference](../0xrefs.html) — Dynamic pentesting command generator
