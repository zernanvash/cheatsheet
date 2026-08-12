"""Deterministic cipher fingerprinting for the H4G Cipher Identifier.

This module ranks a fixed catalogue from measurable text features. It never
claims that a cipher is proven: identification without challenge context is
necessarily probabilistic.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CipherRule:
    id: str
    name: str
    family: str
    description: str
    scorer: Callable[[dict], tuple[float, list[str], list[str]]]


def clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def add(score: float, condition: bool, points: float, evidence: list[str], message: str) -> float:
    if condition:
        evidence.append(message)
        return score + points
    return score


def features(text: str) -> dict:
    stripped = text.strip()
    letters = [char.upper() for char in stripped if char.isalpha() and char.isascii()]
    alnum = [char for char in stripped if char.isalnum() and char.isascii()]
    counts = Counter(letters)
    total = len(letters)
    ic = sum(value * (value - 1) for value in counts.values()) / (total * (total - 1)) if total > 1 else 0.0
    entropy = -sum((value / total) * math.log2(value / total) for value in counts.values()) if total else 0.0
    tokens = re.findall(r"[A-Za-z0-9+/=]+|[^\s]", stripped)
    numeric = re.findall(r"(?<![A-Za-z0-9])[+-]?\d+(?![A-Za-z0-9])", stripped)
    words = re.findall(r"[A-Za-z]+", stripped)
    return {
        "length": len(stripped), "letters": total, "letter_ratio": total / max(1, len(stripped)),
        "alphabet_size": len(counts), "ic": ic, "entropy": entropy, "counts": counts,
        "tokens": tokens, "numeric": numeric, "words": words,
        "spaces": stripped.count(" "), "digits": sum(char.isdigit() for char in stripped),
        "punctuation": sum(not char.isalnum() and not char.isspace() for char in stripped),
        "uppercase_ratio": sum(char.isupper() for char in stripped if char.isalpha()) / max(1, total),
        "unique_ratio": len(set(alnum)) / max(1, len(alnum)), "raw": stripped,
    }


def encoding_rule(kind: str) -> Callable[[dict], tuple[float, list[str], list[str]]]:
    def score(f: dict) -> tuple[float, list[str], list[str]]:
        raw, compact, evidence = f["raw"], re.sub(r"\s+", "", f["raw"]), []
        value = 0.0
        if kind == "hex":
            valid = bool(compact) and bool(re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+", compact))
            value = add(value, valid, 55, evidence, "Only hexadecimal symbols are present.")
            value = add(value, valid and (compact.lower().startswith("0x") or bool(re.search(r"[A-Fa-f]", compact))), 25, evidence, "Hexadecimal-specific notation or A-F digits are present.")
            value = add(value, valid and len(compact.removeprefix("0x")) % 2 == 0, 10, evidence, "The digit count forms complete bytes.")
        elif kind == "base64":
            valid = bool(compact) and bool(re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", compact))
            value = add(value, valid, 52, evidence, "The alphabet matches Base64.")
            value = add(value, valid and len(compact) % 4 == 0, 18, evidence, "Length is divisible by four.")
            value = add(value, valid and compact.endswith(("=", "==")), 18, evidence, "Standard Base64 padding is present.")
        elif kind == "binary":
            groups = raw.split()
            valid = bool(compact) and bool(re.fullmatch(r"[01]+", compact))
            value = add(value, valid, 72, evidence, "Only binary digits are present.")
            value = add(value, valid and bool(groups) and all(len(x) in (7, 8) for x in groups), 22, evidence, "Whitespace groups are 7 or 8 bits.")
        elif kind == "decimal_ascii":
            nums = [int(x) for x in f["numeric"] if x.lstrip("+-").isdigit()]
            value = add(value, len(nums) >= 3 and len(nums) == len(raw.replace(",", " ").split()), 45, evidence, "Input is a separated decimal sequence.")
            value = add(value, bool(nums) and all(0 <= x <= 127 for x in nums), 40, evidence, "All values fit 7-bit ASCII.")
        return clamp(value), evidence, ["Decode this encoding before testing classical ciphers."]
    return score


def morse(f: dict) -> tuple[float, list[str], list[str]]:
    raw, evidence = f["raw"], []
    score = add(0, bool(raw) and bool(re.fullmatch(r"[.\-_/|\s]+", raw)), 82, evidence, "Only dots, dashes, and Morse separators are present.")
    score = add(score, "/" in raw or "  " in raw, 10, evidence, "Word separators are present.")
    return clamp(score), evidence, ["Try International Morse with slash or double-space word boundaries."]


def bacon(f: dict) -> tuple[float, list[str], list[str]]:
    compact, evidence = re.sub(r"\s+", "", f["raw"]).upper(), []
    alphabet = set(compact)
    score = add(0, len(compact) >= 10 and (alphabet <= {"A", "B"} or alphabet <= {"0", "1"}), 68, evidence, "The complete message uses a two-symbol alphabet.")
    score = add(score, bool(compact) and len(compact) % 5 == 0, 20, evidence, "Length divides into Baconian groups of five.")
    return clamp(score), evidence, ["Map the two symbols to A/B and test both orientations."]


def affine_like(name: str) -> Callable[[dict], tuple[float, list[str], list[str]]]:
    def score(f: dict) -> tuple[float, list[str], list[str]]:
        evidence, value = [], 0.0
        value = add(value, f["letters"] >= 12 and f["letter_ratio"] > 0.72, 24, evidence, "Ciphertext is predominantly alphabetic.")
        value = add(value, f["ic"] >= 0.052, 28, evidence, f"Index of coincidence is language-like ({f['ic']:.3f}).")
        value = add(value, f["spaces"] > 0, 12, evidence, "Word boundaries are preserved.")
        if name == "caesar": value = add(value, f["alphabet_size"] >= 8, 8, evidence, "Alphabet coverage supports a shifted alphabet.")
        if name == "atbash": value = add(value, f["uppercase_ratio"] > 0.75, 4, evidence, "Consistent letter casing is compatible with substitution.")
        if name == "mono": value += 8
        return clamp(value), evidence, ["Use frequency analysis and known flag prefixes.", "Test Caesar/ROT and Atbash before general substitution."]
    return score


def polyalphabetic(f: dict) -> tuple[float, list[str], list[str]]:
    evidence, score = [], 0.0
    score = add(score, f["letters"] >= 20 and f["letter_ratio"] > 0.75, 25, evidence, "Long predominantly alphabetic text.")
    score = add(score, 0.032 <= f["ic"] <= 0.052, 38, evidence, f"Low/intermediate index of coincidence ({f['ic']:.3f}).")
    score = add(score, f["alphabet_size"] >= 16, 12, evidence, "Broad alphabet usage is present.")
    return clamp(score), evidence, ["Estimate key length with repeated sequences and IC by column.", "Test Vigenère, Beaufort, and Autokey variants."]


def transposition(f: dict) -> tuple[float, list[str], list[str]]:
    evidence, score = [], 0.0
    score = add(score, f["letters"] >= 20 and f["letter_ratio"] > 0.78, 22, evidence, "Text is mostly alphabetic.")
    score = add(score, f["ic"] >= 0.055, 36, evidence, f"Language-like frequency distribution survives ({f['ic']:.3f}).")
    score = add(score, f["spaces"] == 0, 14, evidence, "Word boundaries are absent.")
    return clamp(score), evidence, ["Test rail fence and column widths that divide or nearly divide the length."]


def playfair(f: dict) -> tuple[float, list[str], list[str]]:
    evidence, score = [], 0.0
    score = add(score, f["letters"] >= 20 and f["letters"] % 2 == 0, 30, evidence, "Alphabetic length is even, matching digraph encryption.")
    score = add(score, f["spaces"] == 0 and f["letter_ratio"] > 0.9, 18, evidence, "Continuous alphabetic ciphertext.")
    score = add(score, f["alphabet_size"] <= 25, 18, evidence, "At most 25 letters appear, compatible with an I/J square.")
    return clamp(score), evidence, ["Split into digraphs and inspect repeated-letter separators such as X."]


def adfg(f: dict) -> tuple[float, list[str], list[str]]:
    compact, evidence = re.sub(r"[^A-Za-z]", "", f["raw"]).upper(), []
    alphabet = set(compact)
    score = add(0, len(compact) >= 10 and alphabet <= set("ADFGX"), 88, evidence, "Alphabet is restricted to A, D, F, G, X.")
    score = add(score, len(compact) % 2 == 0, 8, evidence, "Length forms coordinate pairs.")
    if alphabet <= set("ADFGVX") and "V" in alphabet:
        score = max(score, 92); evidence.append("The V symbol points specifically to ADFGVX.")
    return clamp(score), evidence, ["Test ADFGX/ADFGVX fractionation followed by columnar transposition."]


def fractionated_symbols(f: dict) -> tuple[float, list[str], list[str]]:
    evidence, score = [], 0.0
    score = add(score, f["length"] >= 12 and f["letter_ratio"] < 0.35, 24, evidence, "Few ordinary letters are present.")
    score = add(score, 3 <= len(set(f["raw"]) - set(" \n\r\t")) <= 8, 28, evidence, "A small symbol alphabet suggests fractionation.")
    return clamp(score), evidence, ["Check Polybius coordinates, tap code, and custom symbol substitutions."]


RULES = [
    CipherRule("hex", "Hexadecimal encoding", "Encoding", "Byte values written in base 16.", encoding_rule("hex")),
    CipherRule("base64", "Base64", "Encoding", "Binary-to-text encoding using a 64-symbol alphabet.", encoding_rule("base64")),
    CipherRule("binary-ascii", "Binary ASCII", "Encoding", "ASCII values represented as binary groups.", encoding_rule("binary")),
    CipherRule("decimal-ascii", "Decimal ASCII", "Encoding", "ASCII values represented as decimal integers.", encoding_rule("decimal_ascii")),
    CipherRule("morse", "Morse code", "Code", "Dots and dashes separated into letters and words.", morse),
    CipherRule("bacon", "Baconian cipher", "Bilateral substitution", "Five-symbol groups over a two-symbol alphabet.", bacon),
    CipherRule("adfgx", "ADFGX / ADFGVX", "Fractionation", "Polybius coordinates combined with transposition.", adfg),
    CipherRule("caesar", "Caesar / ROT", "Monoalphabetic substitution", "A fixed alphabet shift.", affine_like("caesar")),
    CipherRule("atbash", "Atbash", "Monoalphabetic substitution", "A reversed alphabet substitution.", affine_like("atbash")),
    CipherRule("affine", "Affine cipher", "Monoalphabetic substitution", "A modular linear substitution.", affine_like("affine")),
    CipherRule("substitution", "Monoalphabetic substitution", "Substitution", "One fixed ciphertext symbol per plaintext letter.", affine_like("mono")),
    CipherRule("vigenere", "Vigenère-family cipher", "Polyalphabetic substitution", "A repeating or evolving alphabetic key.", polyalphabetic),
    CipherRule("transposition", "Transposition cipher", "Transposition", "Reorders plaintext characters while retaining frequencies.", transposition),
    CipherRule("playfair", "Playfair cipher", "Digraph substitution", "Encrypts letter pairs through a 5×5 square.", playfair),
    CipherRule("polybius", "Polybius / Tap code", "Coordinate substitution", "Represents characters as coordinate pairs.", fractionated_symbols),
]

CATALOGUE = {rule.id: rule for rule in RULES}


def identify(text: str, limit: int = 8) -> dict:
    if not isinstance(text, str): raise TypeError("text must be a string")
    if not text.strip(): raise ValueError("Enter ciphertext to identify.")
    if len(text) > 20_000: raise ValueError("Ciphertext exceeds the 20,000 character limit.")
    f = features(text)
    ranked = []
    for rule in RULES:
        score, evidence, next_steps = rule.scorer(f)
        if score > 5:
            ranked.append({"id": rule.id, "name": rule.name, "family": rule.family,
                           "description": rule.description, "score": round(score, 1),
                           "evidence": evidence, "next_steps": next_steps})
    ranked.sort(key=lambda item: (-item["score"], item["name"]))
    summary = {key: f[key] for key in ("length", "letters", "letter_ratio", "alphabet_size", "ic", "entropy", "digits", "punctuation", "spaces")}
    summary["letter_ratio"] = round(summary["letter_ratio"], 4); summary["ic"] = round(summary["ic"], 4); summary["entropy"] = round(summary["entropy"], 4)
    return {"features": summary, "candidates": ranked[:max(1, min(limit, 12))],
            "disclaimer": "Ranks are hypotheses from measurable structure, not cryptographic proof."}
