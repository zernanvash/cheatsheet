import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "enrich_writeups.py"
SPEC = importlib.util.spec_from_file_location("enrich_writeups", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class IndexBuilderTests(unittest.TestCase):
    def test_frontmatter_and_title_fallbacks(self):
        data, body = MODULE.parse_frontmatter("---\ntitle: Demo\ntags: [rev, gdb]\n---\n# Ignored\nBody")
        self.assertEqual(data["title"], "Demo")
        self.assertEqual(data["tags"], ["rev", "gdb"])
        self.assertEqual(MODULE.title_for(Path("fallback.md"), data, MODULE.headings_from(body)), "Demo")
        self.assertEqual(MODULE.title_for(Path("fallback-name.md"), {}, []), "fallback name")

    def test_category_and_origin_mappings(self):
        self.assertEqual(
            MODULE.category_for("_source_picoctf_cajac/2025/Binary_Exploitation/demo.md", {}, "Demo", ""),
            "PWN / Binary Exploit",
        )
        self.assertEqual(
            MODULE.origin_for("_source_sec_fortress/posts/htb/posts/demo.md", {}),
            "HackTheBox",
        )
        self.assertEqual(
            MODULE.origin_for("_source_e0sec_ctf_writeups/v1tctf2026/demo/README.md", {}),
            "Other",
        )

    def test_markdown_cleanup_and_security_tags(self):
        markdown = "# Atari\n\n[Retro console](https://example.test) with `GDB` and a buffer overflow.\n```bash\necho test\n```"
        body = MODULE.strip_markdown(markdown)
        self.assertIn("Retro console", body)
        self.assertNotIn("https://", body)
        tags = MODULE.tags_for({}, body)
        self.assertIn("GDB", tags)
        self.assertIn("Buffer Overflow", tags)

    def test_context_title_for_lab_mission(self):
        title = MODULE.context_title_for(
            "0x26", "_source_hackmyvm_writeups/labs/venus/0x26.md", "moving from `alice` to `bob`"
        )
        self.assertEqual(title, "Venus Lab Mission 0x26 (alice -> bob)")

    def test_serialization_is_deterministic(self):
        records = [{"id": "a", "title": "Atari"}]
        self.assertEqual(MODULE.serialized(records), MODULE.serialized(records))
        self.assertTrue(MODULE.serialized(records).endswith("\n"))


if __name__ == "__main__":
    unittest.main()
