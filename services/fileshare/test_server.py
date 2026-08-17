import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from services.fileshare import server


class FilenameTests(unittest.TestCase):
    def test_removes_paths_controls_and_trailing_dots(self):
        self.assertEqual(server.clean_filename("../folder/hello%20world.txt"), "hello world.txt")
        self.assertEqual(server.clean_filename("..\\evil\r\n.txt"), "evil.txt")


class ApiTests(unittest.TestCase):
    def test_upload_list_download_and_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patches = [patch.object(server, "DATA_DIR", root), patch.object(server, "FILES_DIR", root / "files"), patch.object(server, "INDEX_FILE", root / "index.json"), patch.object(server, "MAX_FILE_BYTES", 16), patch.object(server, "MAX_TOTAL_BYTES", 32)]
            for item in patches: item.start()
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_port}"
            try:
                body = b"hello vault"
                saved = json.load(urlopen(Request(f"{base}/api/fileshare?filename=notes.txt", data=body, method="POST", headers={"Content-Type": "application/octet-stream"})))
                file_id = saved["file"]["id"]
                listing = json.load(urlopen(f"{base}/api/fileshare"))
                self.assertEqual(listing["files"][0]["name"], "notes.txt")
                response = urlopen(f"{base}/api/fileshare/download/{file_id}")
                self.assertEqual(response.read(), body)
                self.assertIn("attachment", response.headers["Content-Disposition"])
                with self.assertRaises(HTTPError) as too_large:
                    urlopen(Request(f"{base}/api/fileshare?filename=large.bin", data=b"x" * 17, method="POST"))
                self.assertEqual(too_large.exception.code, 413)
            finally:
                httpd.shutdown(); httpd.server_close()
                for item in reversed(patches): item.stop()


if __name__ == "__main__":
    unittest.main()
