#!/usr/bin/env python3
"""
gpu bounded key search for 69ff482c8fab7bbca273011e
"""

from __future__ import annotations

import argparse
import math
import sys
import time

import cupy as cp
import numpy as np


TARGET = 0x350721C5
INITIAL = 0x811C9DC5
FNV_PRIME = 0x01000193
ROUNDS = 0x4C4B40


CUDA_SOURCE = r"""
extern "C" __global__
void search_keys(
    const unsigned char *alphabet,
    unsigned int alphabet_len,
    unsigned int serial_len,
    unsigned long long start,
    unsigned long long total,
    unsigned int stop_first,
    unsigned int max_results,
    unsigned int *result_count,
    unsigned long long *result_indices
) {
    unsigned long long tid = (unsigned long long)blockDim.x * blockIdx.x + threadIdx.x;
    unsigned long long idx = start + tid;

    if (idx >= total) return;
    if (stop_first && result_count[0] != 0u) return;
    if (serial_len > 16u) return;

    unsigned long long x = idx;
    unsigned char bytes[16];

    for (int pos = (int)serial_len - 1; pos >= 0; pos--) {
        bytes[pos] = alphabet[x % alphabet_len];
        x /= alphabet_len;
    }

    unsigned int key = 0x811c9dc5u;

    for (unsigned int round = 0; round < 0x4c4b40u; round++) {
        for (unsigned int i = 0; i < serial_len; i++) {
            key = (key ^ bytes[i]) * 0x01000193u;
        }
    }

    if (key == 0x350721c5u) {
        unsigned int slot = atomicAdd(result_count, 1u);
        if (slot < max_results) {
            result_indices[slot] = idx;
        }
    }
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="gpu bounded key search for 69ff482c8fab7bbca273011e")
    parser.add_argument("--alphabet", choices=["alnum", "printable", "lower", "upper", "digits", "hex"], default="alnum")
    parser.add_argument("--chars", help="custom alphabet")
    parser.add_argument("--length", type=int, help="single serial length")
    parser.add_argument("--min-len", type=int, default=1, help="minimum length")
    parser.add_argument("--max-len", type=int, default=4, help="maximum length")
    parser.add_argument("--all", action="store_true", help="search full range and print all hits")
    parser.add_argument("--chunk", type=int, default=262144, help="candidate count per kernel launch")
    parser.add_argument("--block", type=int, default=128, help="block size")
    parser.add_argument("--max-results", type=int, default=4096, help="maximum indices retained per chunk")
    return parser.parse_args()


def get_alphabet(args: argparse.Namespace) -> bytes:
    if args.chars is not None:
        alphabet = args.chars.encode("latin1")
    elif args.alphabet == "alnum":
        alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    elif args.alphabet == "printable":
        alphabet = bytes(range(0x20, 0x7F))
    elif args.alphabet == "lower":
        alphabet = b"abcdefghijklmnopqrstuvwxyz"
    elif args.alphabet == "upper":
        alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif args.alphabet == "digits":
        alphabet = b"0123456789"
    elif args.alphabet == "hex":
        alphabet = b"0123456789abcdef"
    else:
        raise ValueError(args.alphabet)

    if not alphabet:
        raise ValueError("alphabet must not be empty")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet contains duplicate bytes")
    return alphabet


def index_to_serial(index: int, alphabet: bytes, length: int) -> str:
    base = len(alphabet)
    out = bytearray(length)
    for pos in range(length - 1, -1, -1):
        out[pos] = alphabet[index % base]
        index //= base
    return out.decode("latin1")


def hash_serial(serial: str) -> int:
    key = INITIAL
    data = serial.encode("latin1")
    for _ in range(ROUNDS):
        for b in data:
            key = ((key ^ b) * FNV_PRIME) & 0xFFFFFFFF
    return key


def main() -> int:
    args = parse_args()
    alphabet = get_alphabet(args)

    if args.length is not None:
        lengths = [args.length]
    else:
        lengths = list(range(args.min_len, args.max_len + 1))

    if any(length <= 0 or length > 16 for length in lengths):
        print("lengths must be in the range 1..16", file=sys.stderr)
        return 2

    module = cp.RawModule(code=CUDA_SOURCE)
    kernel = module.get_function("search_keys")

    device_name = cp.cuda.runtime.getDeviceProperties(0)["name"].decode("ascii", "replace")
    print(f"GPU: {device_name}")
    print(f"target: 0x{TARGET:08x}")
    print(f"alphabet ({len(alphabet)}): {alphabet.decode('latin1')}")
    print(f"mode: {'all hits in bounded range' if args.all else 'stop at first hit'}")

    d_alphabet = cp.asarray(np.frombuffer(alphabet, dtype=np.uint8))
    d_count = cp.zeros(1, dtype=np.uint32)
    d_indices = cp.zeros(args.max_results, dtype=np.uint64)

    total_checked = 0
    all_hits: list[str] = []
    start_time = time.time()

    for length in lengths:
        total = len(alphabet) ** length
        print(f"\nlength {length}: {total:,} candidates")

        for start in range(0, total, args.chunk):
            n = min(args.chunk, total - start)
            d_count.fill(0)
            blocks = math.ceil(n / args.block)

            kernel(
                (blocks,),
                (args.block,),
                (
                    d_alphabet,
                    np.uint32(len(alphabet)),
                    np.uint32(length),
                    np.uint64(start),
                    np.uint64(total),
                    np.uint32(0 if args.all else 1),
                    np.uint32(args.max_results),
                    d_count,
                    d_indices,
                ),
            )
            cp.cuda.Stream.null.synchronize()

            total_checked += n
            count = int(d_count.get()[0])
            if count:
                retained = min(count, args.max_results)
                indices = d_indices[:retained].get()
                for raw_idx in indices:
                    serial = index_to_serial(int(raw_idx), alphabet, length)
                    if hash_serial(serial) == TARGET:
                        print(f"hit: {serial}")
                        all_hits.append(serial)
                        if not args.all:
                            elapsed = time.time() - start_time
                            print(f"\nchecked {total_checked:,} candidates in {elapsed:.2f}s")
                            return 0

                if count > args.max_results:
                    print(f"warning: chunk produced {count} hits; retained only {args.max_results}", file=sys.stderr)

            if start and (start // args.chunk) % 50 == 0:
                elapsed = time.time() - start_time
                rate = total_checked / elapsed if elapsed else 0
                print(f"  checked {total_checked:,} total, {rate:,.0f}/s")

    elapsed = time.time() - start_time
    print(f"\nchecked {total_checked:,} candidates in {elapsed:.2f}s")
    if all_hits:
        print("\nvalid serials:")
        for hit in all_hits:
            print(hit)
    else:
        print("no hits")

    return 0 if all_hits else 1


if __name__ == "__main__":
    raise SystemExit(main())

