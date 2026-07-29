"""
Test suite for crackmeh_solver.py — Gate 2 (test-first).

Covers all acceptance criteria (AC-1 through AC-8) from the plan.
"""

import os
import struct
import tempfile
import pytest

# The solver must be importable without side-effects (AC-5 implicit)
import crackmeh_solver as solver

CRACKME_PATH = os.path.join(os.path.dirname(__file__), "crackmeh.exe")
EXPECTED_XOR_KEY = bytes.fromhex("eb60114940b9e572f0e9e1fcf71f00ab")
EXPECTED_PASSWORD = "EasyPassword"


# ── AC-6: Unit tests for ror8/rol8 against known values ──────────────


class TestBitRotation:
    """AC-6: ror8/rol8 against >=3 reference values."""

    @pytest.mark.parametrize(
        "value, n, expected",
        [
            # ROL8(0x01, 3) = 0x08
            (0x01, 3, 0x08),
            # ROL8(0x80, 1) = 0x01
            (0x80, 1, 0x01),
            # ROL8(0xFF, 4) = 0xFF
            (0xFF, 4, 0xFF),
            # ROL8(0xAB, 3) = 0x5D  (10101011 -> 01011101)
            (0xAB, 3, 0x5D),
        ],
    )
    def test_rol8(self, value, n, expected):
        assert solver.rol8(value, n) == expected

    @pytest.mark.parametrize(
        "value, n, expected",
        [
            # ROR8(0x08, 3) = 0x01
            (0x08, 3, 0x01),
            # ROR8(0x01, 1) = 0x80
            (0x01, 1, 0x80),
            # ROR8(0xFF, 4) = 0xFF
            (0xFF, 4, 0xFF),
            # ROR8(0x5D, 3) = 0xAB
            (0x5D, 3, 0xAB),
        ],
    )
    def test_ror8(self, value, n, expected):
        assert solver.ror8(value, n) == expected

    def test_rol_ror_roundtrip(self):
        """ROL then ROR should return original byte."""
        for b in range(256):
            assert solver.ror8(solver.rol8(b, 3), 3) == b


# ── AC-1: Extract XOR key from trailer ──────────────────────────────


class TestKeyExtraction:
    """AC-1: Solver extracts XOR key from the trailer."""

    def test_extract_key(self):
        key, _enc_data = solver.parse_trailer(CRACKME_PATH)
        assert key == EXPECTED_XOR_KEY
        assert len(key) == 16

    def test_trailer_magic(self):
        """Verify trailer starts with DEADC0DE and ends with DEADBEEF."""
        with open(CRACKME_PATH, "rb") as f:
            f.seek(-60, 2)
            trailer = f.read(60)
        assert trailer[:4] == struct.pack("<I", 0xDEADC0DE)
        assert trailer[-4:] == struct.pack("<I", 0xDEADBEEF)


# ── AC-2: Decrypt correctly (MZ header verified) ────────────────────


class TestDecryption:
    """AC-2: Solver decrypts the inner PE correctly."""

    def test_decrypt_produces_mz_header(self):
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        decrypted = solver.decrypt(enc_data, key)
        assert decrypted[:2] == b"MZ", "Decrypted data must start with MZ"

    def test_decrypt_size(self):
        """Inner PE should be 18432 bytes (0x4800)."""
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        decrypted = solver.decrypt(enc_data, key)
        assert len(decrypted) == 18432


# ── AC-7: Valid PE headers (MZ + PE signatures) ─────────────────────


class TestPEValidation:
    """AC-7: Decrypted PE has valid MZ + PE signatures."""

    @pytest.fixture
    def decrypted_pe(self):
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        return solver.decrypt(enc_data, key)

    def test_mz_signature(self, decrypted_pe):
        assert decrypted_pe[:2] == b"MZ"

    def test_pe_signature(self, decrypted_pe):
        """PE signature at e_lfanew offset."""
        e_lfanew = struct.unpack_from("<I", decrypted_pe, 0x3C)[0]
        assert decrypted_pe[e_lfanew : e_lfanew + 4] == b"PE\x00\x00"

    def test_rich_header_present(self, decrypted_pe):
        """Rich header marker should be somewhere in the headers."""
        assert b"Rich" in decrypted_pe[:1024]


# ── AC-3 & AC-8: Find password in .data section ─────────────────────


class TestPasswordExtraction:
    """AC-3/AC-8: Solver finds 'EasyPassword' in decrypted .data section."""

    def test_find_password(self):
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        decrypted = solver.decrypt(enc_data, key)
        password = solver.find_password(decrypted)
        assert password == EXPECTED_PASSWORD

    def test_password_in_raw_data(self):
        """EasyPassword must exist as raw bytes in the decrypted PE."""
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        decrypted = solver.decrypt(enc_data, key)
        assert EXPECTED_PASSWORD.encode("ascii") in decrypted


# ── AC-4: Write decrypted PE to disk ────────────────────────────────


class TestWriteOutput:
    """AC-4: Solver writes decrypted CrackMeEasy.exe to disk."""

    def test_write_decrypted_pe(self):
        key, enc_data = solver.parse_trailer(CRACKME_PATH)
        decrypted = solver.decrypt(enc_data, key)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "CrackMeEasy.exe")
            solver.write_pe(decrypted, out_path)
            assert os.path.exists(out_path)
            with open(out_path, "rb") as f:
                data = f.read()
            assert data[:2] == b"MZ"
            assert len(data) == 18432


# ── AC-5: CLI interface ─────────────────────────────────────────────


class TestCLI:
    """AC-5: CLI prints password and saves inner PE."""

    def test_solve_returns_results(self):
        """solve() should return password and decrypted PE bytes."""
        result = solver.solve(CRACKME_PATH)
        assert result["password"] == EXPECTED_PASSWORD
        assert result["xor_key"] == EXPECTED_XOR_KEY
        assert result["inner_pe"][:2] == b"MZ"
        assert len(result["inner_pe"]) == 18432


# ── Import safety ───────────────────────────────────────────────────


class TestImportSafety:
    """Solver module must be importable without side-effects."""

    def test_no_side_effects_on_import(self):
        """If we got here, the import at module level succeeded without running main."""
        assert hasattr(solver, "solve")
        assert hasattr(solver, "parse_trailer")
        assert hasattr(solver, "decrypt")
        assert hasattr(solver, "find_password")
        assert hasattr(solver, "write_pe")
        assert hasattr(solver, "rol8")
        assert hasattr(solver, "ror8")
