from __future__ import annotations


CHUNK1_LAYOUT = [
    (0x00, 0x6261626464646161, 8),
    (0x08, 0x6161686164626161, 8),
    (0x0F, 0x6164616461616861, 8),
    (0x17, 0x61616261616461, 7),
]

CHUNK2_LAYOUT = [
    (0x00, 0x7567646464646464, 8),
    (0x08, 0x6464646164676764, 8),
    (0x0F, 0x6764646464616464, 8),
    (0x17, 0x64646767646464, 7),
]

CHUNK3_LAYOUT = [
    (0x00, 0x6366636565666666, 8),
    (0x08, 0x666F666666666566, 8),
    (0x10, 0x6663666366666F66, 8),
    (0x18, 0x63666566666366, 7),
]


def to_bits_lsb_first(value: int) -> str:
    out: list[str] = []
    while value > 0:
        out.append(chr((value & 1) + 0x30))
        value >>= 1
    return "".join(out)


def rebuild_overlapped_chunk(layout: list[tuple[int, int, int]]) -> bytes:
    buf = bytearray(b"\x00" * 0x40)
    for offset, value, size in layout:
        buf[offset:offset + size] = value.to_bytes(size, "little")
    return bytes(buf[:buf.index(0)])


def encode_literal_chunk(text: bytes, seed: int) -> str:
    key = seed + 0x0C
    return "".join(to_bits_lsb_first(byte ^ key) for byte in text)


def encode_candidate_flag(text: str) -> str:
    return "".join(to_bits_lsb_first(ord(ch) - 0x30) for ch in text)


def invert_flag_encoding(bitstream: str) -> str:
    prefix = "CTF{"
    suffix = "}"
    prefix_bits = encode_candidate_flag(prefix)
    suffix_bits = encode_candidate_flag(suffix)

    if not bitstream.startswith(prefix_bits):
        raise ValueError("reference does not start with the encoded ctf prefix")
    if not bitstream.endswith(suffix_bits):
        raise ValueError("reference does not end with the encoded closing brace")

    middle = bitstream[len(prefix_bits):len(bitstream) - len(suffix_bits)]
    out = list(prefix)

    allowed = []
    for codepoint in range(0x20, 0x7F):
        ch = chr(codepoint)
        bits = to_bits_lsb_first(codepoint - 0x30)
        if bits:
            allowed.append((ch, bits))

    # the encoding is not prefix-free, so use the flag format to anchor the
    # parse, then prefer the longest reasonable printable match.
    while middle:
        matches = [(ch, bits) for ch, bits in allowed if middle.startswith(bits)]
        if not matches:
            raise ValueError(f"no match for remaining bitstream: {middle[:64]!r}")
        preferred = [item for item in matches if item[0].isalnum() or item[0] in "_{}!-"]
        ch, bits = max(preferred or matches, key=lambda item: len(item[1]))
        out.append(ch)
        middle = middle[len(bits):]

    out.append(suffix)
    return "".join(out)


def build_reference() -> tuple[bytes, bytes, bytes, str]:
    chunk1 = rebuild_overlapped_chunk(CHUNK1_LAYOUT)
    chunk2 = rebuild_overlapped_chunk(CHUNK2_LAYOUT)
    chunk3 = rebuild_overlapped_chunk(CHUNK3_LAYOUT)
    reference = (
        encode_literal_chunk(chunk1, 0x54)
        + encode_literal_chunk(chunk2, 0x59)
        + encode_literal_chunk(chunk3, 0x5B)
    )
    return chunk1, chunk2, chunk3, reference


def main() -> None:
    chunk1, chunk2, chunk3, reference = build_reference()
    flag = invert_flag_encoding(reference)

    print(f"chunk1: {chunk1.decode()}")
    print(f"chunk2: {chunk2.decode()}")
    print(f"chunk3: {chunk3.decode()}")
    print(f"reference length: {len(reference)}")
    print(f"flag: {flag}")
    print(f"re-encodes correctly: {encode_candidate_flag(flag) == reference}")


if __name__ == "__main__":
    main()
