# MD5

> Source: [https://www.dcode.fr/md5-hash](https://www.dcode.fr/md5-hash)
> Retrieved: 2026-08-08
> Attribution: dCode.fr (CC BY notice on the source page).
> Reference-only extract: no converter, solver, API, or implementation code.

## What is MD5? (Definition)

MD5 (Message Digest Algorithm 5) is a cryptographic hash function that transforms data (file, password, etc.) into a unique 128-bit digital fingerprint, typically represented by a 32-character hexadecimal string.

This fingerprint allows you to verify the integrity of the data: any modification to the original data produces a different fingerprint.

Example: After downloading a file, comparing its MD5 fingerprint with the one published by the publisher ensures that it has not been altered.

## How to encrypt in MD5?

MD5 hashing transforms data into a 128-bit hash using nonlinear operations combined with binary rotations and additions .

MD5 processes the message in 512-bit blocks and modifies four registers A, B, C, and D (initialized to 0x67452301 , 0xEFCDAB89 , 0x98BADCFE , and 0x10325476 , respectively).

Each block undergoes 64 steps where MD5 combines:

— one of the following nonlinear functions: F(B,C,D) = (B & C) | ((~B) & D) , G(B,C,D) = (B & D) | (C & (~D)) , H(B,C,D) = B ^ C ^ D or I(B,C,D) = C ^ (B | (~D))

— an addition ( modulo 2 ^32) with A, a constant K, and a word from the message M,

— a left-bitwise rotation,

— then another addition with B.

These operations shuffle the bits using logical functions, carry-overs from additions , and rotations. After all the blocks, the concatenated registers A, B, C, and D form the 128-bit hash.

Example: dCode is crypted e9837d47b610ee29399831f917791a44 it is not the same hash for dcode (without uppercase) which gives a9d3d129549e80065aa8e109ec40a7c8

## How to decrypt MD5 cipher?

MD5 is a one-way function: there is no md5decrypt() method to recover the original data from its hash.

However, brute-force attacks (testing all possible combinations ) or attacks using rainbow tables (databases of pre-calculated hashes) can recover the entry if it is simple or present in a database.

dCode uses its word dictionaries (10 million potential passwords) from which the MD5 hash is already pre-calculated.

If a password is not in the databases, then decryption will fail.

## How to recognize MD5 ciphertext?

The hash is composed of 32 hexadecimal characters 0123456789abcdef , so 128 bits.

The characters are close to random, therefore unpredictable with high entropy.

## When to use MD5 hashing?

MD5 is used for file integrity verification (as a checksum), creating digital signatures, and in certain security protocols.

However, its use is now discouraged for the security of sensitive data such as passwords.

## What is a MD5 collision?

Statistically speaking, for any string (and there is an infinite number), the MD5 associates for a given value a 128-bit fingerprint (a finite number of possibilities). It is therefore mandatory that there are collisions (2 strings with the same hash). Several research works on the subject have demonstrated that the MD5 algorithm, although creating a large entropy of data, could be attacked, and that it was possible to generate chains with the same fingerprints (after several hours of neat calculations).

Example: Discovered by Wang & Yu in How to break MD5 and other hash functions , the two hexadecimal values (the values and not the ASCII string) 4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2 4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2 have the same hash: '008ee33a9d58b51cfeb425b0959121c9 (they only differ by 8 hexadecimal digits)

Since this publication in 2005, MD5 encryption is no longer considered cryptographically, giving way to its successors: SHA1 then SHA256 .

## What are the variants of the MD5 cipher?

The MD5 is threatened by the growing computing capabilities of supercomputers and processors capable of parallelizing hash functions . Thus, to complicate the search by the rainbow tables (passwords databases), it is recommended to add salt (a prefix or a suffix) to the password. With this salting step, the precalculated tables must be calculated again to take account of the salt which systematically modifies all the fingerprints.

Example: MD5 (dCode) = e9837d47b610ee29399831f917791a44 but MD5 (dCodeSUFFIX) = 523e9a807fc1d2766c3e3d8f132d4991

Another variant is the application of DOUBLE MD5 , which consists in applying the hash algorithm twice.

Example: MD5 (dCode) = e9837d47b610ee29399831f917791a44 but MD5 ( MD5 (dCode)) = c1127c7b6fdcafd97a96b37eaf035eaf

MD5 is not the only hash function , it also exists SHA1 , SHA256 , SHA512 etc.

## What does MD5 mean?

MD5 stands for Message Digest 5:

— Message Digest: A unique summary (hint) of a piece of data.

— 5: The 5th version of the algorithm (successor to MD4 ).

## What is the list of MD5 Magic Hashes for PHP?

The PHP language has a default functionality: the type juggling which allows to not define the type of variable used, the PHP engine tries to automatically detect if the variable is a string, an integer, etc.

However this functionality can become a flaw when handling MD5 string whose value has the form 0e followed by digits between 0 and 9. Indeed, in this case, the PHP engine will convert the string into a floating number having the value 0.

Here is a list of magic MD5 hashes:

String MD5 (String) ABJIHVY 0e755264355178451322893275696586 DQWRASX 0e742373665639232907775599582643 DYAXWCA 0e424759758842488633464374063001 EEIZDOI 0e782601363539291779881938479162 GEGHBXL 0e248776895502908863709684713578 GGHMVOE 0e362766013028313274586933780773 GZECLQZ 0e537612333747236407713628225676 IHKFRNS 0e256160682445802696926137988570 MAUXXQC 0e478478466848439040434801845361 MMHUWUV 0e701732711630150438129209816536 NOOPCJF 0e818888003657176127862245791911 NWWKITQ 0e763082070976038347657360817689 PJNPDWY 0e291529052894702774557631701704 QLTHNDT 0e405967825401955372549139051580 QNKCDZO 0e830400451993494058024219903391

String MD5 (String) ABJIHVY 0e755264355178451322893275696586 DQWRASX 0e742373665639232907775599582643 DYAXWCA 0e424759758842488633464374063001 EEIZDOI 0e782601363539291779881938479162 GEGHBXL 0e248776895502908863709684713578 GGHMVOE 0e362766013028313274586933780773 GZECLQZ 0e537612333747236407713628225676 IHKFRNS 0e256160682445802696926137988570 MAUXXQC 0e478478466848439040434801845361 MMHUWUV 0e701732711630150438129209816536 NOOPCJF 0e818888003657176127862245791911 NWWKITQ 0e763082070976038347657360817689 PJNPDWY 0e291529052894702774557631701704 QLTHNDT 0e405967825401955372549139051580 QNKCDZO 0e830400451993494058024219903391

Bonus strings that can also be evaluated at 0 : 0e215962017 , 0e730083352 , 0e807097110 , 0e840922711

## When was MD5 invented?

The MD5 was invented by Ronald Rivest in 1991 to replace its predecessor, MD4 .
