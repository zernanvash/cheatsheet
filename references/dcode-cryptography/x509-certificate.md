# X.509 Certificate

> Source: [https://www.dcode.fr/x509-certificate](https://www.dcode.fr/x509-certificate)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is an X.509 certificate? (Definition)

An X.509 certificate is a digital certificate standard used to authenticate an entity (a server, a user, a company, etc.). It relies on asymmetric cryptography (public/private key) and follows the format defined by the ITU-T (International Telecommunication Union).

Its primary function is to associate a public key with an identity (domain name, email address, etc.) and guarantee this association through a digital signature issued by a Certificate Authority (CA). This enables the securing of HTTPS (TLS/SSL) connections, the signing of software, the authentication of users or machines, and more.

## How to recognize an X.509 certificate?

An X.509 certificate can take several forms:

— Binary file (.der, .cer): DER (Distinguished Encoding Rules) encoded format

— Text file (.pem, .crt, .key): PEM ( Base64 , delimited by -----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----) format.

The content of an X.509 certificate generally consists of the following fields:

— Version

— Serial number

— Signature algorithm

— Issuer: Certificate Authority (CA)

— Subject: Certified identity (e.g., CN=example.com)

— Expiry date

etc.

## What are the variants of X.509 certificates?

X.509 certificates come in several types depending on their use:

— Server certificate, authenticates a website via HTTPS (TLS/SSL)

— Client certificate, authenticates a user or device, such as for a VPN

— CA certificate, issued by a certificate authority to sign other certificates

— Self-signed certificate, signed with its own private key (no CA), used for local development

— Wildcard certificate, covers a domain and its subdomains (e.g., *.example.com)

— S/MIME certificate, used to encrypt/sign secure emails

There are others.

## What is a Certification Authority (CA)?

A Certificate Authority (CA) is a trusted entity that issues, signs, and revokes X.509 certificates .

It guarantees the authenticity of the identities associated with public keys.

Example: Digicert, Symantec, Let's Encrypt, Microsoft AD CS

## What is a certificate revocation?

A certificate can be revoked before its expiry date if the private key is compromised, the certified identity is no longer valid, or the CA detects an anomaly or fraud.
