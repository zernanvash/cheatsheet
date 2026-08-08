# Diffie-Hellman Key Exchange

> Source: [https://www.dcode.fr/diffie-hellman-key-exchange](https://www.dcode.fr/diffie-hellman-key-exchange)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is Diffie-Hellman Key Exchange? (Definition)

Diffie-Hellman key exchange is a mathematical/cryptographic protocol that allows two parties, even if they have never met before, to establish a shared secret over an insecure communication channel.

The principle relies on mathematical properties that allow a common secret key to be calculated without ever transmitting it directly.

An observer intercepting all public communications would not be able to deduce the shared secret.

This shared secret key can then be used as a symmetric encryption key to encrypt and decrypt messages or data exchanged between the two parties.

## How does Diffie-Hellman Key Exchange work?

Two people, Alice and Bob, get in touch and publicly choose two common parameters: a large prime number $ P $ and a number $ G $ such that $ G < P $.

Alice then chooses a number $ a $ at random, called her private key, which she keeps secret. She then calculates $ A = G^a \mod P $. The value $ A $ is called Alice's public key and is sent publicly to Bob.

Similarly, Bob chooses a number $ b $ at random, called his private key, which he keeps secret. He calculates $ B = G^b \mod P $, his public key, and sends it publicly to Alice.

Alice, having received $ B $, calculates the value $ S = B^a \mod P $.

Bob, having received $ A $, calculates the value $ S = A^b \mod P $.

Thanks to the properties of modular arithmetic , both calculations yield exactly the same value $ S $. This value is the shared secret key. They can then communicate by encrypting their messages with this key.

An attacker who only observes the public values $ P $, $ G $, $ A $ and $ B $ cannot calculate $ S $ without knowing $ a $ or $ b $, because this would require solving the discrete logarithm problem, which is considered difficult for sufficiently large parameters.

P = 101 G = 12 a = 123 b = 345 A = G^a%P = 35 B = G^b%P = 60 S = B^a%P = A^b%P = 62

P = 101 G = 12 a = 123 b = 345 A = G^a%P = 35 B = G^b%P = 60 S = B^a%P = A^b%P = 62

## What are the Diffie-Hellman forces?

The main advantage of Diffie-Hellman is that it allows the establishment of a shared secret key over an insecure channel, without any prior secrecy between the communicating parties.

Another advantage is the theoretical robustness of the protocol when used with sufficiently large and well-chosen parameters. Diffie-Hellman also allows the use of ephemeral keys, which provides forward secrecy: the compromise of a private key at a given time does not allow the decryption of past communications.

## What are the weaknesses of Diffie-Hellman? (Disadvantages)

The DHKE ( Diffie-Hellman Key Exchange) protocol is vulnerable to several types of attacks:

— Man-in-the-middle attacks: an attacker intercepts the communication of the 2 parties and pretends to be the other party.

— Attack by reflection: an attacker sends a fake message asking to perform a new key exchange with himself, authentication of the parties is therefore preferable.

— Attack by precalculation/factorization: private keys are generally less than 1024 bits, precalculation of combinations with low values is possible but very costly in time and resources.

## Why the number P must be prime?

When $ P $ is a prime number, the set of integers modulo $ P $ forms a mathematical group with good algebraic properties, notably the absence of zero divisors .

These properties guarantee that exponential operations modulo $ P $ behave predictably and securely, which is essential for Diffie-Hellman security.

It is theoretically possible to use a non-prime $ P $, but in this case, security relies on the difficulty of factoring $ P $. If an attacker knows this factorization, they can break the key exchange.

## How to find out the private keys?

Private keys, by definition, are never shared publicly and remain known only to their owner.

Knowing a public key does not allow one to easily retrieve the corresponding private key; this is a well-known mathematical problem (known as the discrete logarithm problem).

Private keys are generated using cryptographically secure random number generators.

It is recommended to generate new private keys for each communication session to limit the impact of a potential compromise.

## What is elliptic curve-based key exchange?

An elliptic version of Diffie-Hellman (Elliptic curve Diffie–Hellman ECDH) is based on the same principles as classical Diffie-Hellman , but uses elliptic curves instead of classical modular arithmetic .

This approach achieves an equivalent level of security with smaller key sizes, improving performance and reducing resource requirements.

## When was Diffie-Hellman Key Exchange invented?

Whitfield Diffie and Martin Hellman presented their method in 1976.
