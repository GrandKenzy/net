"""Cross-platform source-contract checks; no Bagron installation required."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
required = {
    "modules/http.bg", "modules/https.bg", "modules/headers.bg",
    "modules/file.bg", "modules/server.bg", "modules/url.bg",
    "library.bg", "scripts/build_lib.py", "tests/integration_http.py",
    "test_headers.bg", "test_url.bg",
}
for name in sorted(required):
    assert (ROOT / name).is_file(), f"Missing: {name}"
for name in ("modules/winsock.bg", "modules/linuxsock.bg"):
    assert not (ROOT / name).exists(), f"Duplicate native ABI: {name}"
for source in (ROOT / "modules").glob("*.bg"):
    value = source.read_text(encoding="utf-8")
    assert not re.search(r"^\s*extern\s+(?:c|windows)\b", value, re.MULTILINE), source
entry = (ROOT / "library.bg").read_text(encoding="utf-8")
assert not re.search(r"^\s*func\s+main\(", entry, re.MULTILINE)
assert "import { HttpClient } from http" in entry
assert "import { HttpServer } from server" in entry
server = (ROOT / "modules/server.bg").read_text(encoding="utf-8")
assert "open_input_beneath" in server
http = (ROOT / "modules/http.bg").read_text(encoding="utf-8")
assert "parse_framing" in http
assert "self.max_body_bytes" in http
print("Source-contract checks passed")
