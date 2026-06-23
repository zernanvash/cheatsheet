# **Newly Discovered Zero-Day Attacks As Of October-17-2023 In The Past Few Weeks**


![Image Credit from : https://appcheck-ng.com/zero-day-vulnerabilities-explained/](https://appcheck-ng.com/wp-content/uploads/Zero-Day-Timeline.png)

***


## **Privilege escalation zero-day in the Atlassian Confluence Data Center and Server**

Microsoft has exposed 'Storm-0062,' a Chinese-backed threat group, exploiting a critical zero-day vulnerability in Atlassian Confluence Data Center and Server since September 14, 2023. Storm-0062, linked to China's Ministry of State Security, is known for targeting diverse sectors. Rapid7 released a proof-of-concept exploit, adding urgency to upgrading Confluence versions. Older releases and Atlassian-hosted instances remain unaffected. Refer to Atlassian's security bulletin for detailed information.

 
**_Reference :_** [https://www.bleepingcomputer.com/news/security/microsoft-state-hackers-exploiting-confluence-zero-day-since-september/](https://www.bleepingcomputer.com/news/security/microsoft-state-hackers-exploiting-confluence-zero-day-since-september/)


## **New IOS XE zero-day actively exploited on Cisco**

Cisco has issued a critical warning about an authentication bypass zero-day vulnerability (CVE-2023-20198) in its IOS XE software. The flaw, which is still awaiting a patch, impacts devices with the Web User Interface (Web UI) and HTTP or HTTPS Server features enabled. Attackers, if successful, can create an account with full administrator privileges, potentially leading to unauthorized activity. Cisco identified active exploitation in late September and noted related malicious activity involving the creation of local user accounts and the deployment of a malicious implant. Cisco advises disabling the HTTP Server feature on internet-facing systems to mitigate the risk.

**_Reference :_** [https://www.bleepingcomputer.com/news/security/cisco-warns-of-new-ios-xe-zero-day-actively-exploited-in-attacks/](https://www.bleepingcomputer.com/news/security/cisco-warns-of-new-ios-xe-zero-day-actively-exploited-in-attacks/)

## Zero-Day 'HTTP/2 Rapid Reset' DDoS Attack Sets Alarming Records

A newly discovered DDoS attack technique, known as 'HTTP/2 Rapid Reset,' has been actively exploited as a zero-day vulnerability since August, reaching record-breaking levels of attack magnitude. Amazon Web Services, Cloudflare, and Google have jointly announced successful mitigation of these attacks, with Google reporting a peak of 398 million requests per second. The technique leverages a zero-day vulnerability, CVE-2023-44487, within the HTTP/2 protocol, exploiting its stream cancellation feature to continuously send and cancel requests, overwhelming target servers. As attackers continue to adopt this method and expand their botnets, HTTP/2 Rapid Reset attacks are expected to break even greater records, posing significant challenges for mitigation.


**_Reference :_** [https://www.bleepingcomputer.com/news/security/new-http-2-rapid-reset-zero-day-attack-breaks-ddos-records/](https://www.bleepingcomputer.com/news/security/new-http-2-rapid-reset-zero-day-attack-breaks-ddos-records/)

## Critical Zero-Day Vulnerability in Exim Puts Millions of Servers at Risk

A severe zero-day vulnerability, identified as CVE-2023-42115, has been discovered in Exim mail transfer agent (MTA) software, allowing unauthenticated attackers to gain remote code execution on internet-exposed servers. The vulnerability, an Out-of-bounds Write weakness in the SMTP service, enables attackers to execute code in the context of the service account. Exim is widely used, and millions of servers are exposed to attacks, making it an attractive target for threat actors. While a patch is not yet available, administrators are advised to restrict remote access to mitigate potential exploitation. Additional Exim zero-day vulnerabilities with lower severity ratings were also disclosed.

**_Reference :_** [https://www.bleepingcomputer.com/news/security/millions-of-exim-mail-servers-exposed-to-zero-day-rce-attacks/](https://www.bleepingcomputer.com/news/security/millions-of-exim-mail-servers-exposed-to-zero-day-rce-attacks/)

## **Ways To Stay Ahead Of This Type Of Attack**

- Stay Informed: Keep an eye on security updates and advisories from Exim, your operating system provider, and security organizations. Being aware of potential threats is the first line of defense.

- Isolate Vulnerable Servers: If possible, isolate servers running Exim from the internet or restrict remote access. Reducing exposure minimizes the risk of exploitation.

- Update Exim: Apply any patches or updates released by Exim as soon as they become available. These updates are crucial for addressing vulnerabilities.

- Implement Firewalls: Utilize firewalls to filter and monitor incoming and outgoing traffic. This can help block suspicious activity and limit the attack surface.

- Regular Backups: Maintain regular backups of your server data. In case of an attack, you can restore your system to a clean state.

- Intrusion Detection Systems (IDS): Implement IDS to detect and alert you to any suspicious behavior or unauthorized access.

- Strong Access Controls: Strengthen access controls and authentication mechanisms. Use strong, unique passwords and consider two-factor authentication.

- Monitoring and Logging: Set up comprehensive monitoring and logging to track server activity. Unusual patterns can be early signs of an attack.

- Security Audits: Conduct security audits or penetration testing to identify vulnerabilities and weaknesses in your system.

- Regular Updates: Keep your entire system, not just Exim, up to date. Operating system updates, software patches, and security plugins all play a role in safeguarding your server.

- Incident Response Plan: Have a well-defined incident response plan in place. Knowing how to react in case of a breach can minimize damage and downtime.

- Security Training: Educate your team about security best practices. Human error is a common factor in security breaches.

- Utilize a Web Application Firewall (WAF): A WAF can help protect against web-based attacks and can act as an additional layer of defense.

- Limit Server Exposure: Only run necessary services and applications. Reducing the number of potential entry points can improve security.

**Remember, vigilance is key in maintaining server security. By staying informed, applying updates promptly, and having a robust security strategy in place, you can help protect your server against emerging threats like the Exim zero-day vulnerability. Stay safe and secure! 💪🔒 #ServerSecurity #ZeroDayProtection #SenseLearner**



- [ ] Facebook: [https://www.facebook.com/senselearner](https://www.facebook.com/senselearner)

- [ ] Instagram: [https://instagram.com/senselearner_technologies?
igshid=MzRlODBiNWFlZA==](https://instagram.com/senselearner_technologies?
igshid=MzRlODBiNWFlZA==)

- [ ] Linkedin: [https://www.linkedin.com/company/senselearner-technologies-pvt-ltd/](https://www.linkedin.com/company/senselearner-technologies-pvt-ltd/)



<button onclick="window.location.href='https://sec-fortress.github.io';">Back To Home螥</button>

