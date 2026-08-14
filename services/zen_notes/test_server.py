import tempfile
import json
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

from services.zen_notes import server


class SanitizerTests(unittest.TestCase):
    def test_removes_scripts_handlers_and_unsafe_links(self):
        value = '<h2 onclick="bad()">Title</h2><script>alert(1)</script><a href="javascript:bad()">bad</a><a href="https://example.com">ok</a>'
        self.assertEqual(server.sanitize_html(value), '<h2>Title</h2>alert(1)<a>bad</a><a href="https://example.com">ok</a>')

    def test_keeps_editor_table_structure(self):
        value = '<div class="table-wrap unknown"><table><tbody><tr><td contenteditable="true">cell</td></tr></tbody></table></div>'
        self.assertEqual(server.sanitize_html(value), '<div class="table-wrap"><table><tbody><tr><td>cell</td></tr></tbody></table></div>')


class StoreTests(unittest.TestCase):
    def test_atomic_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "notes.json"
            with patch.object(server, "DATA_FILE", target):
                server.save_store({"notes": {"one": {"revision": 1}}})
                self.assertEqual(server.load_store()["notes"]["one"]["revision"], 1)


class ApiTests(unittest.TestCase):
    def test_public_save_read_and_revision_conflict(self):
        note_id = next(iter(server.known_ids()))
        with tempfile.TemporaryDirectory() as directory, patch.object(server, "DATA_FILE", Path(directory) / "notes.json"):
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{httpd.server_port}"
            try:
                body = json.dumps({"title": "Shared title", "html": '<p onclick="bad()">safe<script>bad()</script></p>', "revision": 0}).encode()
                request = Request(f"{base}/api/zen-notes/{note_id}", data=body, method="PUT", headers={"Content-Type": "application/json"})
                saved = json.load(urlopen(request))
                self.assertEqual(saved["note"]["revision"], 1)
                self.assertNotIn("onclick", saved["note"]["html"])
                self.assertNotIn("<script", saved["note"]["html"])
                listing = json.load(urlopen(f"{base}/api/zen-notes"))
                self.assertEqual(listing["notes"][note_id]["title"], "Shared title")
                with self.assertRaises(HTTPError) as conflict:
                    urlopen(request)
                self.assertEqual(conflict.exception.code, 409)
            finally:
                httpd.shutdown()
                httpd.server_close()


if __name__ == "__main__":
    unittest.main()
