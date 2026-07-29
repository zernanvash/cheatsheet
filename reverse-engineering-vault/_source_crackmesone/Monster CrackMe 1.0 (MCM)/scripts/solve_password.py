from z3 import Int, Solver, sat

DATA_HEX_TEST1 = "4f000000d000000051010000d201000053020000d402000055030000d603000057000000d800000059010000da0100005b020000dc0200005d030000de0300005f000000e000000061010000e201000063020000e402000065030000e603000067000000e800000069010000ea0100006b020000ec0200006d030000ee0300006f000000f000000071010000f201000073020000f402000075030000f603000077000000f800000079010000fa0100007b020000fc0200007d030000fe0300007f000000000100008101000002020000830200000403000085030000060000008700000008010000890100000a0200008b0200000c0300008d0300000e000000"
BLOB_HEX = "48d9ed8a1dff9a7bb0d1e57c15f7927388e9ddbb2dcfaa4b80e1d5b325c7a243"
MASK = 0xB3E192F8A4D5C6B7 ^ 0x9F2D38B17C6A4E5F

# need decoded[0]=0xF0 and decoded[3:11]=01 00 00 00 00 00 00 00
TARGET = {0: 0xF0, 3: 0x01, 4: 0x00, 5: 0x00, 6: 0x00, 7: 0x00, 8: 0x00, 9: 0x00, 10: 0x00}
INDICES = sorted(TARGET.keys())


def build_high():
    high = [0] * 4096
    u = 0xDEADBEEF
    idx = 0
    for _ in range(0x40):
        for _ in range(4):
            for _ in range(16):
                u = (u * 0x19660D + 0x3C6EF35F) & 0xFFFFFFFF
                high[idx] = u & 0x3FF
                idx += 1
    return high


def coeff_row(high, n):
    row = [0] * 64
    for j in range(4):
        for k in range(16):
            row[j * 16 + k] = high[(n * 4 + j) * 16 + k] & 0xFF
    return row


def main():
    data = bytes.fromhex(DATA_HEX_TEST1)
    blob = bytes.fromhex(BLOB_HEX)
    mask = MASK.to_bytes(8, "little")
    high = build_high()

    # low-byte of edx for each constrained key index
    need = {}
    for n in INDICES:
        key_n = blob[n] ^ mask[n & 7] ^ TARGET[n]
        data_n = data[n * 4]
        need[n] = (data_n - key_n) & 0xFF

    # Try shortest printable lengths first.
    for nvars in range(1, 65):
        s = Solver()
        xs = [Int(f"x{i}") for i in range(nvars)]

        for x in xs:
            s.add(x >= 0x20, x <= 0x7e)

        for n in INDICES:
            coeffs = coeff_row(high, n)
            expr = 0
            for i in range(nvars):
                expr += coeffs[i] * xs[i]
            s.add(expr % 256 == need[n])

        if s.check() != sat:
            continue

        m = s.model()
        out = ''.join(chr(m[x].as_long()) for x in xs)
        print(f"length={nvars}")
        print(out)
        return

    print("no solution")


if __name__ == "__main__":
    main()
