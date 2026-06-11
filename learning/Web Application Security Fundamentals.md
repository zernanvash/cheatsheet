# Web Application Security Fundamentals

Use this after [Web Fundamentals](Web%20Fundamentals.md). The focus is risk categories and beginner security checks before using exploit templates.

Source summarized:

- Esther7171 TryHackMe walkthrough: [Web Application Security](https://github.com/Esther7171/TryHackMe-Walkthroughs/blob/main/Room/Web-Application-Security/readme.md)

## Core Risk Categories

- Identification and authentication failures: weak login controls, unlimited attempts, poor reset logic, default credentials.
- Cryptographic failures: sensitive data over cleartext, weak storage, missing HTTPS, exposed secrets.
- Access control failures: users can view or modify objects they should not control.
- Injection: user input reaches SQL, shell, template, XML, LDAP, or other interpreters.
- Security misconfiguration: debug mode, verbose errors, default admin panels, unsafe methods.

## Beginner Web Security Loop

1. Identify the app purpose and user roles.
2. Capture normal requests.
3. Change IDs, methods, roles, cookies, and body values one at a time.
4. Compare status code, redirect, response length, and displayed data.
5. Keep proof minimal and stay inside lab scope.

## IDOR Basics

IDOR happens when an object ID is trusted without checking whether the current user owns or can access it.

Signals:

- URLs such as `/user/2`, `/invoice?id=10`, `/api/users/123`.
- JSON fields such as `user_id`, `account`, `role`, or `owner`.
- A normal user can view or edit another user's record by changing an ID.

Study path:

```text
GET /api/user/1
GET /api/user/2
POST /api/user/2
```

Only test against lab objects or accounts you are allowed to use.

## Authentication Checks

- Rate limiting or lockout on login.
- Username enumeration through error text, status, timing, or response size.
- Password reset token length and reuse.
- Session invalidation after logout or password change.
- Cookies that trust client-side `admin`, `role`, or `user_id`.

## Crypto And Transport Checks

- Login over HTTP instead of HTTPS.
- Secrets in URLs, GET parameters, or client-side JavaScript.
- Cookies missing `Secure` or `HttpOnly`.
- Weak JWT secrets or unsigned token behavior in CTF labs.

## When To Jump To Blueprints

- Login bypass or database behavior -> [SQL Injection To Credentials](../blueprints/machine-attacks/SQL%20Injection%20To%20Credentials.md).
- Object ID abuse -> [Web Exploit Blueprint](../blueprints/Web%20Exploit%20Blueprint.md#4a-parameter-enumeration).
- Weak auth or creds -> [Password Attacks](../tools/Password%20Attacks.md).
- Source or config leak -> [File Disclosure And Source Review](../blueprints/machine-attacks/File%20Disclosure%20And%20Source%20Review.md).
