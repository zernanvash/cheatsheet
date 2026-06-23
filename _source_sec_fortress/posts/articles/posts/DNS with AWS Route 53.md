# **DNS with AWS Route 53**


![image](https://github.com/sec-fortress/sec-fortress.github.io/assets/132317714/17163918-9ec4-4c93-9eb5-411af84092c9)



## **There are two types of hosted zones**

- [ ] Public Hosted Zone
	- Can always be used from the internet generally


![](https://i.imgur.com/YXQFlWF.png)



- [ ] Private  Hosted Zone
	- Used for internal VPC-based resources
	- Note that, Amazon Virtual Private Cloud (_VPC_) is a service that lets you launch AWS _resources_ in a logically isolated virtual network that you define.


![](https://i.imgur.com/HOr3bsT.png)



## **Amazon Route 53 Routing Policies**

- **Route 53** is an intelligent DNS service.
- Routing policies determine which responses are provided to the client DNS resolver.

## **Types of Routing Policy**

| Routing Policy | What it does |
| :--- | :--- |
| Simple | Simple DNS response providing the IP Address associated with a name |
| Failover | If primary address is down (based on health checks ), routes to secondary destination |
| Geolocation | Uses geographic location  you're in (e.g Europe) to route you to the closest region |
| Geoproximity | Routes you to the closest region within a geographic area |
| Lateency | Directs you based on the lowest latency route to resources |
| Multivalue answer  | Returns several IP address and functions as a basic load balancer |
| Weighted | Uses the relative weights assigned to resources to determine which to route to |

## **Amazon route 53 Record types**

- [A record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#AFormat)
- [AAAA record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#AAAAFormat)
- [CAA record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#CAAFormat)
- [CNAME record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#CNAMEFormat)
- [DS record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#DSFormat)
- [MX record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#MXFormat)
- [NAPTR record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#NAPTRFormat)
- [NS record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#NSFormat)
- [PTR record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#PTRFormat)
- [SOA record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#SOAFormat)
- [SPF record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#SPFFormat)
- [SRV record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#SRVFormat)
- [TXT record type](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html#TXTFormat)


Highlighting the most common ones is the `CNAME` and the `ALIAS` record, You can read more about them from [here](https://help.ns1.com/hc/en-us/articles/360017511293-What-is-the-difference-between-CNAME-and-ALIAS-records)


<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>
