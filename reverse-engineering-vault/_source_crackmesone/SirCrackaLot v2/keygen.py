import argparse
import subprocess


INV_7A69_MOD_2_16 = 0xB5D9


def u32(x: int) -> int:
    return x & 0xFFFFFFFF


def rol32(x: int, n: int) -> int:
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def rol16(x: int, n: int) -> int:
    x &= 0xFFFF
    return ((x << n) | (x >> (16 - n))) & 0xFFFF


def rol16_in_u32(x: int, n: int) -> int:
    return (x & 0xFFFF0000) | rol16(x, n)


def gen_crc16_table() -> list[int]:
    table = []
    for i in range(256):
        v = i
        for _ in range(8):
            if v & 1:
                v = (v >> 1) ^ 0xA001
            else:
                v >>= 1
        table.append(v & 0xFFFF)
    return table


def dwords_to_words(dws: list[int]) -> list[int]:
    out: list[int] = []
    for d in dws:
        d &= 0xFFFFFFFF
        out.append(d & 0xFFFF)
        out.append((d >> 16) & 0xFFFF)
    return out


def words_to_dwords(ws: list[int]) -> list[int]:
    return [
        (ws[0] & 0xFFFF) | ((ws[1] & 0xFFFF) << 16),
        (ws[2] & 0xFFFF) | ((ws[3] & 0xFFFF) << 16),
        (ws[4] & 0xFFFF) | ((ws[5] & 0xFFFF) << 16),
        (ws[6] & 0xFFFF) | ((ws[7] & 0xFFFF) << 16),
    ]


def pshuflw(ws: list[int], imm: int) -> list[int]:
    out = ws[:]
    for i in range(4):
        out[i] = ws[(imm >> (2 * i)) & 3]
    return out


def pshufhw(ws: list[int], imm: int) -> list[int]:
    out = ws[:]
    for i in range(4):
        out[4 + i] = ws[4 + ((imm >> (2 * i)) & 3)]
    return out


def pshufd(ws: list[int], imm: int) -> list[int]:
    d = words_to_dwords(ws)
    outd = [d[(imm >> (2 * i)) & 3] for i in range(4)]
    return dwords_to_words(outd)


def punpckhdq(a: list[int], b: list[int]) -> list[int]:
    ad = words_to_dwords(a)
    bd = words_to_dwords(b)
    return dwords_to_words([ad[2], bd[2], ad[3], bd[3]])


def pand(a: list[int], b: list[int]) -> list[int]:
    return [(x & y) & 0xFFFF for x, y in zip(a, b)]


def pandn(a: list[int], b: list[int]) -> list[int]:
    return [((~x) & y) & 0xFFFF for x, y in zip(a, b)]


def por(a: list[int], b: list[int]) -> list[int]:
    return [((x | y) & 0xFFFF) for x, y in zip(a, b)]


def pinsrw(ws: list[int], value: int, idx: int) -> list[int]:
    out = ws[:]
    out[idx] = value & 0xFFFF
    return out


def pmullw(a: list[int], b: list[int]) -> list[int]:
    return [((x * y) & 0xFFFF) for x, y in zip(a, b)]


def paddw(a: list[int], b: list[int]) -> list[int]:
    return [((x + y) & 0xFFFF) for x, y in zip(a, b)]


def psrldq(ws: list[int], imm_bytes: int) -> list[int]:
    b = bytearray()
    for w in ws:
        b.extend((w & 0xFFFF).to_bytes(2, "little"))
    if imm_bytes >= 16:
        b2 = bytearray(16)
    else:
        b2 = b[imm_bytes:] + bytearray(imm_bytes)
    out = []
    for i in range(0, 16, 2):
        out.append(int.from_bytes(b2[i : i + 2], "little"))
    return out


def psrld(ws: list[int], imm_bits: int) -> list[int]:
    d = words_to_dwords(ws)
    d = [((x >> imm_bits) & 0xFFFFFFFF) for x in d]
    return dwords_to_words(d)


def shufps(a: list[int], b: list[int], imm: int) -> list[int]:
    ad = words_to_dwords(a)
    bd = words_to_dwords(b)
    outd = [
        ad[(imm >> 0) & 3],
        ad[(imm >> 2) & 3],
        bd[(imm >> 4) & 3],
        bd[(imm >> 6) & 3],
    ]
    return dwords_to_words(outd)


def movd(ws: list[int]) -> int:
    return ((ws[1] & 0xFFFF) << 16) | (ws[0] & 0xFFFF)


def swap(a: list[int], i: int, j: int) -> None:
    a[i], a[j] = a[j], a[i]


def mul_add_hi16(u: int, mul: int, add: int) -> int:
    return (u32(u * mul + add) >> 16) & 0xFFFF


def seal3_from_u_and_l160(u: int, local160_u32: int) -> int:
    # build and shuffle the 0..15 vector exactly like 0x10ae8..0x10da2
    a = list(range(16))
    x = u32(u * 0x41C64E6D + 0x3039)
    swap(a, 15, ((x >> 14) & 0x3C) // 4)
    swap(a, 14, mul_add_hi16(u, 0xC2A29A69, 0xD3DC167E) % 15) # EXTRACT_1
    swap(a, 13, mul_add_hi16(u, 0x807DBCB5, 0xA70427DF) % 14) # EXTRACT_1
    swap(a, 12, mul_add_hi16(u, 0xEE067F11, 0xD6651C2C) % 13) # EXTRACT_1
    swap(a, 11, mul_add_hi16(u, 0xEBA1483D, 0x0DAA96F5) % 12) # EXTRACT_1
    swap(a, 10, mul_add_hi16(u, 0xD3DC57F9, 0xC21F1C8A) % 11) # EXTRACT_1
    swap(a, 9, mul_add_hi16(u, 0x9B355305, 0x3EAD62FB) % 10)  # EXTRACT_1
    swap(a, 8, mul_add_hi16(u, 0xCFDDDF21, 0xCD1DCF18) % 9)   # EXTRACT_1
    x = u32(u * 0x0FFA0F0D + 0xAF5AAD71)
    swap(a, 7, ((x >> 14) & 0x1C) // 4)
    swap(a, 6, mul_add_hi16(u, 0xEF1C5E89, 0x20DA7756) % 7)
    swap(a, 5, mul_add_hi16(u, 0x5AD7FE55, 0xAFE533D7) % 6)
    swap(a, 4, mul_add_hi16(u, 0xC8333031, 0x69ACC4C4) % 5)
    x = u32(u * 0x8D6072DD + 0x961BAFAD)
    swap(a, 3, ((x >> 14) & 0x0C) // 4)
    swap(a, 2, mul_add_hi16(u, 0x88FE3E19, 0x261EB2E2) % 3)
    x = u32(u * 0xCB2C0EA5 + 0x95933673)
    swap(a, 1, ((x >> 14) & 0x04) // 4)

    mem_180 = dwords_to_words([a[0], a[1], a[2], a[3]])
    mem_150 = dwords_to_words([a[2], a[3], a[4], a[5]])
    mem_160 = dwords_to_words([a[4], a[5], a[6], a[7]])
    mem_140 = dwords_to_words([a[6], a[7], a[8], a[9]])
    mem_170 = dwords_to_words([a[12], a[13], a[14], a[15]])
    mem_e0 = [a[1] & 0xFFFF, a[12] & 0xFFFF, 0, 0, 0, 0, 0, 0] # after AA

    const_2fd0 = dwords_to_words([0x00040001, 0x00100008, 0x00000000, 0x00000000])
    const_3050 = dwords_to_words([0xFFFFFFFF, 0x0000FFFF, 0x00000000, 0xFFFFFFFF])
    const_3110 = dwords_to_words([0x000D0002, 0x000F000E, 0x00000000, 0x00000000])
    const_3140 = dwords_to_words([0x00050003, 0x00070006, 0x000A0009, 0x000C000B])
    const_3170 = dwords_to_words([0xFFFFFFFF, 0x0000FFFF, 0xFFFFFFFF, 0xFFFFFFFF])

    xmm0 = pshuflw(mem_140, 0x00)
    xmm1 = pshufhw(xmm0, 0xE8)
    xmm2 = pshufhw(mem_150, 0xE8)
    xmm2 = pshufd(xmm2, 0xE8)
    xmm2 = pshuflw(xmm2, 0xF8)
    xmm2 = pand(xmm2, const_3050)
    xmm0 = pandn(const_3050, xmm1)
    xmm0 = por(xmm0, xmm2)
    xmm0 = pinsrw(xmm0, a[10], 6)
    xmm0 = pinsrw(xmm0, a[11], 7)
    xmm0 = pmullw(xmm0, const_3140)

    xmm4 = mem_e0[:]
    xmm4 = pinsrw(xmm4, a[13], 2)
    xmm4 = pinsrw(xmm4, a[14], 3)
    xmm4 = pmullw(xmm4, const_3110) #ok

    xmm5 = psrldq(mem_170, 6)
    xmm2 = pshufd(mem_160, 0xFA)
    xmm3 = pshufd(mem_180, 0xC4)
    xmm3 = pshufhw(xmm3, 0xE8)
    xmm3 = punpckhdq(xmm3, xmm2)
    xmm3 = pand(xmm3, const_3170)
    xmm1 = pandn(const_3170, xmm5)
    xmm1 = por(xmm1, xmm3)
    xmm1 = pmullw(xmm1, const_2fd0)
    xmm1 = paddw(xmm1, xmm4)
    xmm1 = paddw(xmm1, xmm0)
    xmm1 = shufps(xmm1, xmm0, 0xE4)
    xmm0 = pshufd(xmm0, 0xEE)
    xmm0 = paddw(xmm0, xmm1)
    xmm1 = pshufd(xmm0, 0x55)
    xmm1 = paddw(xmm1, xmm0)
    xmm0 = xmm1[:]
    xmm0 = psrld(xmm0, 16)
    xmm0 = paddw(xmm0, xmm1)
    eax = movd(xmm0)
    return u32(eax ^ local160_u32)


def calc_parts(username: str) -> tuple[int, int, int, int]:
    b = username.encode("utf-8")
    n = len(b)
    v = 0  # normal run

    if n == 0:
        local110_u32 = u32(v ^ 0x6042)
        local160_u32 = 0x6042
        u = u32(0x6042 ^ v)
    else:
        h = u32(v ^ 0xDEADBEEF)
        rem4 = n & 3
        i = 0
        while i < rem4:
            h = rol32(h, 5)
            h = u32(h ^ b[i])
            h = u32(h * 0x1000193)
            i += 1
        while i < n:
            h = rol32(h, 5)
            h = u32(h ^ b[i + 0])
            h = u32(h * 0x1000193)
            h = rol32(h, 5)
            h = u32(h ^ b[i + 1])
            h = u32(h * 0x1000193)
            h = rol32(h, 5)
            h = u32(h ^ b[i + 2])
            h = u32(h * 0x1000193)
            h = rol32(h, 5)
            h = u32(h ^ b[i + 3])
            h = u32(h * 0x1000193)
            i += 4

        local110_u32 = u32(n + ((h >> 16) ^ h))

        x = local110_u32
        rem8 = n & 7
        i = 0
        while i < rem8:
            x = u32(x + b[i])
            x = rol16_in_u32(x, 3)
            i += 1
        while i < n:
            x = u32(x + b[i + 0])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 1])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 2])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 3])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 4])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 5])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 6])
            x = rol16_in_u32(x, 3)
            x = u32(x + b[i + 7])
            x = rol16_in_u32(x, 3)
            i += 8

        local160_u32 = 0x1337
        if ((x & 0xFFFF) ^ (v & 0xFFFF)) != 0:
            local160_u32 = u32(x ^ v)

        h31 = local160_u32 & 0xFFFF
        i = 0
        while i < rem8:
            h31 = u32(h31 * 31 + b[i])
            i += 1
        while i < n:
            h31 = u32(h31 * 31 + b[i + 0])
            h31 = u32(h31 * 31 + b[i + 1])
            h31 = u32(h31 * 31 + b[i + 2])
            h31 = u32(h31 * 31 + b[i + 3])
            h31 = u32(h31 * 31 + b[i + 4])
            h31 = u32(h31 * 31 + b[i + 5])
            h31 = u32(h31 * 31 + b[i + 6])
            h31 = u32(h31 * 31 + b[i + 7])
            i += 8
        u = u32(h31 ^ v)

    seal1 = local110_u32 & 0xFFFF
    seal3_u32 = seal3_from_u_and_l160(u, local160_u32)
    seal3 = seal3_u32 & 0xFFFF

    t = gen_crc16_table()
    ecx = local110_u32
    edx = (ecx >> 8) & 0xFFFFFFFF
    esi = ecx & 0xFF
    esi = t[esi]
    edx = u32(edx ^ esi)
    esi >>= 8
    edx = t[edx & 0xFF]
    edi = local160_u32
    esi = u32(esi ^ edi)
    esi = u32(esi ^ edx)
    esi &= 0xFF
    edx = u32(edx ^ edi)
    edx >>= 8
    esi = t[esi]
    edx = u32(edx ^ esi)
    esi >>= 8
    edx = t[edx & 0xFF]
    esi = u32(esi ^ edx)
    esi = u32(esi ^ seal3_u32)
    esi &= 0xFF
    edx = u32(edx ^ seal3_u32)
    edx >>= 8
    eax = t[esi]
    edx = u32(edx ^ eax)
    eax >>= 8
    edx &= 0xFF
    si = v & 0xFFFF
    si ^= t[edx]
    esi = u32(si ^ eax)
    seal4 = esi & 0xFFFF

    seal2 = ((local160_u32 & 0xFFFF) * INV_7A69_MOD_2_16) & 0xFFFF
    return seal1, seal2, seal3, seal4


def make_key(username: str) -> str:
    s1, s2, s3, s4 = calc_parts(username)
    return f"{s1:04X}-{s2:04X}-{s3:04X}-{s4:04X}"


def verify(binary_path: str, username: str, key: str) -> bool: # temp test
    payload = f"{username}\n{key}\n"
    p = subprocess.run([binary_path], input=payload, text=True, capture_output=True, check=False)
    return p.returncode == 0 and "welcomes thee" in p.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description="69a07e02fb7f76ef92045c40 keygen")
    parser.add_argument("username", help="username to generate key for")
    parser.add_argument("--binary", default="./SirCrackaLot", help="path to challenge binary")
    parser.add_argument("--verify", action="store_true", help="verify key against the binary")
    args = parser.parse_args()

    key = make_key(args.username)
    print(key)
    if args.verify:
        print("VALID" if verify(args.binary, args.username, key) else "INVALID")


if __name__ == "__main__":
    main()
