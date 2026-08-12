import json
import unittest

from services.cipher_identifier.opencode_advisor import _extract_text, _json_object


class AdvisorParsingTests(unittest.TestCase):
    def test_extract_nested_part(self):
        raw = json.dumps({"type": "text", "part": {"text": '{"ranking":["hex"],"explanation":"x","questions":[]}'}})
        self.assertIn('"hex"', _extract_text(raw))

    def test_extract_json_object(self):
        self.assertEqual(_json_object('prefix {"ranking":[]} suffix')["ranking"], [])

    def test_missing_json_rejected(self):
        with self.assertRaises(ValueError): _json_object("plain response")


if __name__ == "__main__": unittest.main()
