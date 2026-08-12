import unittest

from services.cipher_identifier.classifier import identify


class ClassifierTests(unittest.TestCase):
    def first(self, text): return identify(text)["candidates"][0]["id"]

    def test_hex(self): self.assertEqual(self.first("48656c6c6f20776f726c64"), "hex")
    def test_base64(self): self.assertEqual(self.first("SGVsbG8gd29ybGQ="), "base64")
    def test_binary(self): self.assertEqual(self.first("1001000 1100101 1101100 1101100 1101111"), "binary-ascii")
    def test_decimal_ascii(self): self.assertEqual(self.first("72 101 108 108 111"), "decimal-ascii")
    def test_morse(self): self.assertEqual(self.first(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."), "morse")
    def test_bacon(self): self.assertEqual(self.first("AABAA AABAB ABABB ABABB ABBBA"), "bacon")
    def test_adfgx(self): self.assertEqual(self.first("ADFGXGDAFFAGDX"), "adfgx")
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): identify("   ")
    def test_size_rejected(self):
        with self.assertRaises(ValueError): identify("A" * 20001)


if __name__ == "__main__": unittest.main()
