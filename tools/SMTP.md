# SMTP

SMTP enumeration and manual interaction for authorized labs.

## Ports

- `25` SMTP
- `465` SMTPS
- `587` submission
- `110` POP3
- `995` POP3S
- `143` IMAP
- `993` IMAPS

## Banner And Manual Commands

```bash
nc -nv target 25
telnet target 25
openssl s_client -connect target:465
openssl s_client -starttls smtp -connect target:587
```

Manual sequence:

```text
HELO test.local
VRFY user
EXPN users
MAIL FROM:<test@test.local>
RCPT TO:<user@example.local>
QUIT
```

## User Enumeration

```bash
smtp-user-enum -M VRFY -U users.txt -t target
smtp-user-enum -M EXPN -U users.txt -t target
smtp-user-enum -M RCPT -U users.txt -t target
```

Use valid users as inputs for scoped password attacks, phishing simulation only when explicitly authorized, or mail service login testing.

## Mail Clients

```bash
openssl s_client -connect target:993
curl -k "imaps://target" --user user:password
curl -k "pop3s://target" --user user:password
```

Search mail for credentials, reset links, internal hostnames, and attachments.
