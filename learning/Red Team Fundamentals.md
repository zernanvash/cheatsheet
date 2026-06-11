# Red Team Fundamentals

Use this for engagement vocabulary and mindset before the machine/databank blueprints.

Source summarized:

- Official TryHackMe room: [Red Team Fundamentals](https://tryhackme.com/room/redteamfundamentals)

## Assessment Types

- Vulnerability assessment: find and report as many weaknesses as possible, often with automated scanning.
- Penetration test: exploit vulnerabilities to prove impact and show how issues chain together.
- Red team engagement: emulate adversary tactics, techniques, and procedures to test detection and response.

Key difference: red teaming is not about finding every bug; it is about reaching agreed objectives while measuring defensive readiness.

## Teams And Cells

- Red cell: offensive operators.
- Blue cell: defenders, monitoring, and internal response.
- White cell: trusted controllers/referees who manage scope, rules, and safety.

Common red team roles:

- Lead: plans and coordinates.
- Assistant lead: supports planning and operations.
- Operator: executes tasks and documents results.

## Engagement Shapes

- Full engagement: end-to-end adversary simulation.
- Assumed breach: start with some access and test internal paths.
- Tabletop: discuss response to scenarios without live exploitation.

## Kill Chain Vocabulary

- Reconnaissance: collect target information.
- Weaponization: build the payload or delivery artifact.
- Delivery: get the payload to the target.
- Exploitation: trigger code execution or access.
- Installation: place tooling or establish access in a lab-approved way.
- Command and control: operate the compromised asset.
- Actions on objectives: reach the agreed goal.

## CTF Translation

- Objective: flags, proof files, target accounts, or challenge completion.
- Scope: only the target network/room/lab.
- Detection: usually not scored in beginner CTFs, but still useful to understand noise.
- Documentation: record commands, evidence, credentials, and decision points.

## When To Jump To Blueprints

- Boot2root or service challenge -> [Machine Exploitation Databank](../blueprints/Machine%20Exploitation%20Databank.md).
- AD environment -> [Active Directory Attack Path Cheat Sheet](../tools/Active%20Directory%20Attack%20Path%20Cheat%20Sheet.md).
- Post-exploitation decisions -> [Post-Exploitation](../tools/Post-Exploitation.md).
