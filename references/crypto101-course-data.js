window.CRYPTO101_COURSE = {
  source: "Crypto101.pdf",
  author: "Laurens Van Houtven (lvh)",
  license: "CC BY-NC 4.0",
  modules: [
    {
      id: "xor", number: "01", track: "Foundations", title: "XOR and One-Time Pads", pages: "17–27", level: "Start here", time: "25 min",
      tags: ["XOR", "one-time pad", "known plaintext", "key reuse"],
      objectives: ["Read XOR as a reversible bit operation", "Explain why a true one-time pad has perfect secrecy", "Recognize the failure caused by reusing key material"],
      summary: "XOR is the smallest useful model of reversible encryption: applying the same key twice restores the message. A one-time pad is secure only when its key is uniformly random, as long as the message, kept secret, and never reused.",
      sections: [
        ["Mental model", "XOR is a controlled inverter. A key bit of 0 leaves a message bit unchanged; a key bit of 1 flips it. Because x XOR k XOR k = x, the same operation encrypts and decrypts."],
        ["Why the one-time pad works", "For every candidate plaintext there is a key that maps the ciphertext to it, so the ciphertext alone cannot distinguish the real message. The demanding key rules—not XOR itself—provide perfect secrecy."],
        ["How it fails", "If two messages reuse a pad, XORing their ciphertexts cancels the key and exposes the XOR of both plaintexts. Language structure and guessed fragments can then recover content and key bytes."],
        ["CTF lens", "Repeated-key XOR often reveals periodic key lengths, readable scoring peaks, or crib-dragging opportunities. First test whether key material repeats or whether multiple ciphertexts share it."]
      ],
      checkpoint: ["Why does applying XOR with the same key twice recover the input?", "Which one-time-pad requirement is violated when two ciphertexts share a key?", "What disappears when two reused-pad ciphertexts are XORed together?"]
    },
    {
      id: "block-ciphers", number: "02", track: "Foundations", title: "Block Ciphers: AES, DES, and 3DES", pages: "28–40", level: "Core", time: "30 min",
      tags: ["AES", "DES", "3DES", "permutation", "ECB"],
      objectives: ["Describe a block cipher as a keyed permutation", "Separate a block cipher from its mode of operation", "Understand why DES-era key sizes are inadequate"],
      summary: "A block cipher maps fixed-size plaintext blocks to ciphertext blocks under a key. AES is the modern example; DES and 3DES show how design age and effective key size matter. A raw block cipher does not safely encrypt an arbitrary message by itself.",
      sections: [
        ["Mental model", "For each key, the cipher chooses one reversible permutation of all possible blocks. Decryption walks that mapping backward. Security depends on the mapping appearing unpredictable without the key."],
        ["AES", "AES operates on 128-bit blocks and transforms a byte matrix through repeated substitution, permutation, mixing, and key addition. Its supported key sizes change the number of rounds, not the block size."],
        ["DES and 3DES", "DES has a small effective key and is brute-forceable. 3DES applies DES multiple times to extend its useful life, but it remains a legacy construction with a small block size and poor modern fit."],
        ["CTF lens", "Look for fixed block boundaries, repeated blocks, padding, and mode clues. Identifying AES alone is incomplete: mode, IV or nonce, padding, key, and authentication also matter."]
      ],
      checkpoint: ["What property makes a block cipher decryptable?", "Does AES-256 use a larger block than AES-128?", "Why is naming only AES insufficient to describe an encryption scheme?"]
    },
    {
      id: "stream-modes", number: "03", track: "Foundations", title: "Stream Ciphers and Block-Cipher Modes", pages: "41–80", level: "Core", time: "55 min",
      tags: ["CBC", "CTR", "RC4", "Salsa20", "padding oracle", "bit flipping", "nonce"],
      objectives: ["Explain how keystream encryption differs from block encryption", "Trace CBC and CTR data flow", "Recognize malleability, IV/nonce reuse, and padding-oracle failures"],
      summary: "Stream encryption combines plaintext with a generated keystream. Modes such as CBC and CTR adapt block ciphers to longer messages, but each introduces strict IV, nonce, padding, and authentication requirements.",
      sections: [
        ["CBC", "Each plaintext block is XORed with the previous ciphertext block before encryption; the IV supplies the first link. Unpredictable IVs prevent repeated prefixes from producing revealing ciphertext relationships."],
        ["Padding and oracles", "CBC needs padding for partial blocks. If a system reveals whether modified ciphertext has valid padding, an attacker can recover plaintext byte by byte without learning the key."],
        ["Native streams and CTR", "RC4 and Salsa20 generate keystream directly; CTR encrypts successive counter values to create one. Reusing the same stream position repeats keystream and recreates the reused-pad problem."],
        ["Integrity is separate", "Unauthenticated stream-like encryption is malleable: changing ciphertext bits predictably changes plaintext bits. Use authenticated encryption rather than assuming secrecy implies integrity."]
      ],
      checkpoint: ["Why must a CTR nonce/counter combination never repeat under one key?", "What information does a padding oracle leak?", "Why can an attacker alter stream-encrypted plaintext without decrypting it?"]
    },
    {
      id: "key-exchange", number: "04", track: "Trust & Identity", title: "Key Exchange: DH and ECDH", pages: "81–89", level: "Core", time: "25 min",
      tags: ["Diffie-Hellman", "ECDH", "discrete logarithm", "forward secrecy", "MITM"],
      objectives: ["Explain how two parties derive a shared secret over a public channel", "Connect DH security to a hard inverse problem", "State why unauthenticated key exchange permits interception"],
      summary: "Diffie–Hellman lets peers combine private choices with public values to arrive at the same shared secret. Discrete-log hardness protects those private choices, but authentication is still required to know who shares the key.",
      sections: [
        ["Abstract exchange", "Both peers perform a private operation and exchange public results. The construction is arranged so applying either private contribution last produces the same secret."],
        ["Discrete-log and elliptic-curve forms", "Classic DH uses modular exponentiation; ECDH uses scalar multiplication on elliptic-curve groups. Both rely on an operation that is easy forward and believed hard to reverse."],
        ["The missing identity", "Plain DH does not authenticate public values. A machine-in-the-middle can establish a separate secret with each side unless signatures, certificates, or another authenticator bind the exchange."],
        ["Forward secrecy", "Fresh ephemeral DH keys keep an old session secret even if a long-term authentication key is compromised later, assuming ephemeral secrets were erased."]
      ],
      checkpoint: ["What hard problem protects classic DH?", "What attack remains possible against unauthenticated DH?", "Why do ephemeral exchange keys improve forward secrecy?"]
    },
    {
      id: "public-key", number: "05", track: "Trust & Identity", title: "Public-Key Encryption: RSA and ECC", pages: "90–97", level: "Core", time: "30 min",
      tags: ["RSA", "ECC", "OAEP", "hybrid encryption", "authentication"],
      objectives: ["Distinguish public and private key roles", "Explain why systems normally use hybrid encryption", "Recognize textbook RSA as unsafe"],
      summary: "Public-key encryption solves key-distribution problems by publishing an encryption key while keeping decryption capability private. Because it is slower and structurally delicate, real systems use it to protect symmetric session keys rather than bulk data.",
      sections: [
        ["RSA idea", "RSA builds a trapdoor permutation from modular exponentiation. The public exponent and modulus enable the forward operation; secret factor-related information enables efficient inversion."],
        ["Padding is part of the scheme", "Raw or textbook RSA is deterministic and algebraically malleable. Secure randomized encodings such as OAEP are not cosmetic—they supply properties the bare mathematical operation lacks."],
        ["Hybrid encryption", "Generate a random symmetric key, encrypt the data efficiently with it, then protect that small key using public-key machinery. This combines scalable data encryption with manageable key distribution."],
        ["Encryption is not identity", "Anyone can use a recipient's public key. Public-key encryption alone does not prove who created a message; authentication or signatures must be composed separately."]
      ],
      checkpoint: ["Why is RSA rarely used for an entire large file?", "What security problem does randomized RSA padding address?", "Does possession of a recipient's public key prove sender identity?"]
    },
    {
      id: "hashes", number: "06", track: "Trust & Identity", title: "Hash Functions and Password Storage", pages: "98–110", level: "Core", time: "35 min",
      tags: ["MD5", "SHA-1", "SHA-2", "SHA-3", "password storage", "length extension", "Merkle tree"],
      objectives: ["Differentiate preimage, second-preimage, and collision resistance", "Explain why fast general hashes are poor password stores", "Recognize length-extension exposure in naive constructions"],
      summary: "A cryptographic hash compresses arbitrary input to a fixed-size digest. Different security properties answer different attacker goals, and not every hash construction is safe for authentication or password storage.",
      sections: [
        ["Three resistance goals", "Preimage resistance hides an input behind its digest; second-preimage resistance prevents replacing a known input; collision resistance makes finding any equal-digest pair difficult. These are related but distinct claims."],
        ["Algorithm history", "MD5 and SHA-1 demonstrate practical collision failure. SHA-2 and SHA-3 represent different modern design families, but the surrounding construction still determines whether a use is safe."],
        ["Passwords", "Passwords have limited entropy, so attackers can guess them offline. Salts prevent shared precomputation; deliberately expensive password KDFs raise the cost per guess."],
        ["Length extension and trees", "Some iterative hashes allow appending data to a digest of an unknown-prefixed message, breaking naive secret-prefix authentication. Hash trees instead organize many digests for efficient verification."]
      ],
      checkpoint: ["Which hash property is broken by finding any two colliding messages?", "What does a salt prevent?", "Why is hash(secret || message) not automatically a safe MAC?"]
    },
    {
      id: "macs", number: "07", track: "Trust & Identity", title: "Message Authentication Codes and AEAD", pages: "111–129", level: "Core", time: "35 min",
      tags: ["MAC", "HMAC", "GCM", "OCB", "authenticated encryption", "encrypt-then-MAC"],
      objectives: ["Explain the integrity and authenticity provided by a MAC", "Compare composition orders", "Recognize authenticated encryption as a combined interface"],
      summary: "A MAC lets parties sharing a secret detect unauthorized modification and forgery. HMAC safely wraps hash functions, while authenticated-encryption modes combine confidentiality and integrity under carefully defined inputs.",
      sections: [
        ["What a MAC proves", "A valid tag shows that someone holding the shared key authenticated the exact message. It does not provide non-repudiation because every verifier can also generate tags."],
        ["Composition order", "Encrypt-then-MAC authenticates the ciphertext before attempting decryption and is the clean composition presented as the robust choice. Other orders can expose parsing or oracle behavior."],
        ["HMAC", "HMAC uses nested keyed hashing with distinct inner and outer pads, avoiding the naive secret-prefix weaknesses of many iterative hash functions."],
        ["Authenticated encryption", "OCB and GCM provide confidentiality and authenticity together. Their security still depends on key and nonce discipline, and associated data can be authenticated without being encrypted."]
      ],
      checkpoint: ["Why can a MAC verifier not prove authorship to a third party?", "Which composition validates ciphertext before decryption?", "What input-reuse rule is especially important for GCM?"]
    },
    {
      id: "signatures", number: "08", track: "Trust & Identity", title: "Digital Signatures: RSA, DSA, and ECDSA", pages: "130–136", level: "Core", time: "25 min",
      tags: ["digital signature", "RSA signature", "DSA", "ECDSA", "nonce reuse", "repudiation"],
      objectives: ["Separate signatures from encryption", "Explain the role of DSA/ECDSA per-message nonces", "Recognize when deniable authentication is preferable"],
      summary: "Digital signatures bind a message to a private signing key and allow public verification. DSA-family signatures require an unpredictable, unique nonce; reuse can expose the private key.",
      sections: [
        ["Signing is not decrypting", "Signature schemes use private signing and public verification, but secure signatures are specifically designed and encoded constructions—not simply public-key encryption run backward."],
        ["DSA and ECDSA", "Both combine a message digest, private key, group operation, and per-message nonce. ECDSA moves the group arithmetic to an elliptic curve while retaining the critical nonce requirement."],
        ["Nonce catastrophe", "Reusing or predictably generating the per-message nonce creates related equations from which an observer can solve for the signing key. Good randomness or deterministic nonce derivation is essential."],
        ["Repudiable authenticators", "Some conversations need authentication without transferable proof. Shared-key authenticators can let participants trust messages while preventing either from proving authorship to outsiders."]
      ],
      checkpoint: ["Why is a signature not merely RSA encryption with the private key?", "What secret can ECDSA nonce reuse reveal?", "When might transferable proof be undesirable?"]
    },
    {
      id: "kdfs", number: "09", track: "Key Material", title: "Key Derivation Functions", pages: "137–142", level: "Core", time: "20 min",
      tags: ["PBKDF2", "bcrypt", "scrypt", "HKDF", "password stretching", "domain separation"],
      objectives: ["Separate password KDFs from general key expansion", "Explain salt and work-factor roles", "Use distinct derived keys for distinct purposes"],
      summary: "KDFs turn imperfect or shared source material into keys suited to particular jobs. Password KDFs deliberately slow guessing; extract-and-expand designs derive multiple independent keys from stronger shared secrets.",
      sections: [
        ["Password stretching", "PBKDF2, bcrypt, and scrypt raise the cost of every password guess. A unique salt prevents one precomputed table from attacking many users; configurable cost lets defenders track hardware improvements."],
        ["Memory hardness", "scrypt adds substantial memory cost so highly parallel custom cracking hardware loses some of its advantage over ordinary defenders."],
        ["HKDF", "HKDF first extracts a pseudorandom key from source material, then expands it into context-labeled outputs. This supports key separation without treating a password as if it were already a uniform secret."],
        ["CTF lens", "Identify the exact KDF, salt, iteration or cost parameters, output length, and encoding. Similar-looking recipes produce completely different keys when any parameter changes."]
      ],
      checkpoint: ["What different jobs do a salt and a work factor perform?", "Why is scrypt called memory-hard?", "Why derive separate encryption and authentication keys?"]
    },
    {
      id: "rngs", number: "10", track: "Key Material", title: "Random Number Generators", pages: "143–161", level: "Core", time: "30 min",
      tags: ["entropy", "CSPRNG", "Yarrow", "Blum Blum Shub", "Dual_EC_DRBG", "Mersenne Twister"],
      objectives: ["Distinguish entropy sources from deterministic generators", "State the requirements of a CSPRNG", "Recognize predictable general-purpose PRNGs as unsafe for secrets"],
      summary: "Cryptography needs unpredictable keys and nonces, but computers usually expand scarce physical entropy with deterministic generators. A CSPRNG must resist prediction and recover safely as new entropy arrives.",
      sections: [
        ["Entropy pipeline", "Physical or system events provide uncertain input. A generator conditions and accumulates that entropy, then expands internal state into many outputs. Output volume is not the same as entropy amount."],
        ["Security properties", "An observer of outputs should not predict future outputs or reconstruct earlier ones after state compromise. Reseeding helps recovery when fresh entropy becomes available."],
        ["Design examples", "Yarrow models pools and reseeding; Blum Blum Shub has a strong number-theoretic basis but is slow; Dual_EC_DRBG illustrates how suspicious constants can undermine trust."],
        ["Mersenne Twister", "Mersenne Twister is excellent for simulation but its state can be reconstructed from enough outputs. It must not generate keys, tokens, password resets, or other attacker-facing secrets."]
      ],
      checkpoint: ["Is a long pseudorandom output necessarily high entropy?", "What happens after enough Mersenne Twister outputs are observed?", "Why is reseeding valuable after state compromise?"]
    },
    {
      id: "tls", number: "11", track: "Complete Systems", title: "SSL and TLS", pages: "163–174", level: "System", time: "40 min",
      tags: ["TLS", "handshake", "certificate authority", "forward secrecy", "BEAST", "CRIME", "POODLE", "HSTS"],
      objectives: ["Trace the high-level TLS handshake", "Explain the role and limits of certificate authorities", "Connect historical attacks to violated cryptographic assumptions"],
      summary: "TLS combines negotiation, key exchange, authentication, encryption, and integrity to secure a transport channel. Its history shows that secure primitives can still fail through composition, legacy compatibility, side channels, and configuration.",
      sections: [
        ["Handshake", "Peers negotiate parameters, authenticate the server with certificates, establish shared key material, and confirm that the transcript has not been altered before protecting application data."],
        ["Trust model", "Certificate authorities bind public keys to names. Self-signed and client certificates change how trust is established but do not remove the need to verify identities and key ownership."],
        ["Forward secrecy", "Ephemeral key exchange prevents later theft of a long-term server key from decrypting previously recorded sessions."],
        ["Attack lessons", "BEAST and POODLE exploit CBC-era behavior, CRIME exploits compression leakage, and Lucky 13 exploits timing. HSTS and pinning address different parts of downgrade and trust exposure."]
      ],
      checkpoint: ["What does a server certificate bind together?", "Which handshake choice can provide forward secrecy?", "Why can compression leak secrets even when encryption is sound?"]
    },
    {
      id: "openpgp", number: "12", track: "Complete Systems", title: "OpenPGP and GPG", pages: "175–178", level: "System", time: "20 min",
      tags: ["OpenPGP", "GPG", "web of trust", "key signing", "hybrid encryption"],
      objectives: ["Describe OpenPGP's hybrid-encryption role", "Explain the web-of-trust model", "Separate key availability from key authenticity"],
      summary: "OpenPGP applies public-key cryptography to files and messages and uses signatures for identity claims. Its decentralized web of trust replaces a single CA hierarchy with user-managed attestations and judgment.",
      sections: [
        ["Message protection", "OpenPGP typically protects content with a randomly generated symmetric session key and encrypts that small key to one or more recipients."],
        ["Signatures", "A sender can sign content so recipients verify integrity and association with a signing key. The remaining question is whether that key truly belongs to the claimed person."],
        ["Web of trust", "Users sign bindings between identities and keys. Trust emerges from paths of attestations, but key signing only helps when participants verify identity and manage revocation carefully."],
        ["Operational lesson", "Finding a key on a server proves availability, not authenticity. Fingerprints must be checked through an independently trusted path."]
      ],
      checkpoint: ["Why does OpenPGP use a symmetric session key?", "What does signing another person's key assert?", "Does downloading a key from a key server authenticate it?"]
    },
    {
      id: "otr", number: "13", track: "Complete Systems", title: "Off-the-Record Messaging", pages: "179–184", level: "System", time: "25 min",
      tags: ["OTR", "authenticated key exchange", "deniability", "forward secrecy", "SMP"],
      objectives: ["Explain OTR's combination of authentication and deniability", "Describe how evolving keys support forward secrecy", "Identify the purpose of the Socialist Millionaires' Protocol"],
      summary: "OTR is designed for private interactive conversation: parties authenticate each other while avoiding durable, transferable signatures. Short-lived key material and later disclosure of authentication keys support forward secrecy and deniability.",
      sections: [
        ["Conversation goals", "OTR seeks confidentiality, peer authentication, forward secrecy, and deniability. These goals differ from signed email, where durable third-party-verifiable proof may be intentional."],
        ["Authenticated exchange", "The protocol establishes ephemeral keys and authenticates the exchange without making ordinary messages permanently signed artifacts."],
        ["SMP", "The Socialist Millionaires' Protocol lets both sides test whether they share a secret answer without revealing the answer itself, providing an out-of-band identity check."],
        ["Key evolution", "Session keys change and old keys are discarded. Revealing obsolete MAC keys later lets anyone forge old-looking transcripts, weakening their value as proof while live messages remain authenticated."]
      ],
      checkpoint: ["How does OTR differ from digitally signed chat logs?", "What does SMP compare without revealing it?", "Why are old authentication keys disclosed?"]
    },
    {
      id: "modular-arithmetic", number: "14", track: "Math & Implementation", title: "Modular Arithmetic", pages: "186–201", level: "Foundation", time: "45 min",
      tags: ["modular arithmetic", "prime", "inverse", "exponentiation", "discrete logarithm", "Montgomery ladder"],
      objectives: ["Perform basic operations modulo n", "Relate inverses and exponentiation to public-key systems", "Explain the asymmetric difficulty of discrete logarithms"],
      summary: "Modular arithmetic wraps integer operations into finite sets. Its group structure enables efficient forward computation while supporting hard inverse problems used by RSA and Diffie–Hellman.",
      sections: [
        ["Clock arithmetic", "Values equivalent by a multiple of the modulus represent the same residue. Addition, subtraction, and multiplication can be reduced throughout a calculation."],
        ["Inverses and division", "Division means multiplying by a modular inverse, which exists only under the required coprimality conditions. Prime moduli make many useful structures predictable."],
        ["Fast exponentiation", "Exponentiation by squaring computes large powers with logarithmically many multiplications. Regular patterns such as a Montgomery ladder can also reduce timing leakage."],
        ["Discrete logarithms", "Computing g^x is easy, while recovering x from g and g^x in a suitable group is believed hard. That imbalance underpins classic DH and DSA."]
      ],
      checkpoint: ["When does a modular inverse exist?", "Why is exponentiation by squaring efficient?", "Which direction of the discrete-log relationship is intended to be hard?"]
    },
    {
      id: "elliptic-curves", number: "15", track: "Math & Implementation", title: "Elliptic Curves", pages: "202–204", level: "Advanced", time: "30 min",
      tags: ["elliptic curve", "point addition", "scalar multiplication", "ECDLP", "ECC"],
      objectives: ["View curve points as an algebraic group", "Connect repeated point addition to scalar multiplication", "State the elliptic-curve discrete-log problem"],
      summary: "Selected points on an elliptic curve form a group with a geometric addition rule. Repeated addition is efficient, but reversing scalar multiplication is hard in well-chosen groups, enabling compact public-key cryptography.",
      sections: [
        ["Group of points", "The curve equation and a point at infinity define a set closed under a geometric-algebraic addition rule. Identity, inverses, and associativity make the set usable as a cryptographic group."],
        ["Scalar multiplication", "Adding a point to itself k times is written kP and can be computed efficiently using double-and-add techniques analogous to fast modular exponentiation."],
        ["ECDLP", "Given P and Q = kP, recovering k is the elliptic-curve discrete-log problem. Proper curve and subgroup selection is essential; not every mathematically valid curve is cryptographically safe."],
        ["Where it appears", "ECDH uses scalar multiplication for shared secrets, while ECDSA uses it for signatures. ECC achieves comparable security goals with smaller public values than classic finite-field systems."]
      ],
      checkpoint: ["What plays the role of exponentiation in an elliptic-curve group?", "What value is hidden in Q = kP?", "Why does curve selection matter?"]
    },
    {
      id: "side-channels", number: "16", track: "Math & Implementation", title: "Side-Channel Attacks", pages: "205", level: "Advanced", time: "15 min",
      tags: ["side channel", "timing", "power analysis", "constant time", "Montgomery ladder"],
      objectives: ["Explain how implementation behavior leaks secrets", "Recognize timing and power as observation channels", "Connect regular algorithms to leakage reduction"],
      summary: "A mathematically secure algorithm can leak through how it runs. Timing and power consumption may correlate with secret-dependent branches or operations, allowing attackers to infer keys without breaking the underlying hard problem.",
      sections: [
        ["Timing", "If execution time depends on secret bits, repeated precise measurements can reveal those bits statistically. Network noise may complicate an attack without necessarily preventing it."],
        ["Power", "Simple and differential power analysis inspect device consumption to distinguish operations or correlate hypotheses with measurements."],
        ["Countermeasure mindset", "Constant-time code, regular operation sequences, blinding, masking, and careful hardware design reduce observable correlation. The exact defense depends on the leakage model."],
        ["Core lesson", "Cryptographic security is a property of the full implementation and environment, not only the formula or algorithm name."]
      ],
      checkpoint: ["What causes a timing side channel?", "Why can regular operation sequences help?", "Does a strong algorithm guarantee a side-channel-safe implementation?"]
    }
  ]
};
