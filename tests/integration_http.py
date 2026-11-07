"""Loopback HTTP integration tests. No third-party Python dependencies.

Run after compiling:
  python tests/integration_http.py --client /path/to/client-net --server /path/to/server-net
Tests require 127.0.0.1:8000 to be free.
"""
import argparse
import pathlib
import socket
import subprocess
import tempfile
import threading
import time

HOST, PORT = "127.0.0.1", 8000


def exchange(path):
    with socket.create_connection((HOST, PORT), timeout=2) as conn:
        conn.sendall(f"GET /{path} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n".encode())
        conn.settimeout(4)
        chunks = []
        while True:
            chunk = conn.recv(8192)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)


def server_checks(executable, base):
    root = base / "public"
    root.mkdir()
    (root / "main.bg").write_bytes(b"bagron-test")
    secret = base / "secret.txt"
    secret.write_bytes(b"not-public")
    (root / "shortcut").symlink_to(secret)
    server = subprocess.Popen([str(executable)], cwd=root)
    try:
        for _ in range(80):
            if server.poll() is not None:
                raise AssertionError(f"server exited unexpectedly: {server.returncode}")
            try:
                with socket.create_connection((HOST, PORT), timeout=.1):
                    break
            except OSError:
                time.sleep(.05)
        cases = [
            ("main.bg", b"HTTP/1.1 200"),
            ("missing", b"HTTP/1.1 404"),
            ("shortcut", b"HTTP/1.1 403"),
            ("../secret.txt", b"HTTP/1.1 403"),
        ]
        for path, status in cases:
            data = exchange(path)
            assert data.startswith(status), f"{path}: {data[:100]!r}"
            assert b"not-public" not in data
            print("PASS server:", path)
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


def client_checks(executable, root):
    (root / "build").mkdir()
    cases = [
        ("length", b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nhello", 0, b"hello", 0),
        ("chunked", b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nhello\r\n0\r\n\r\n", 0, b"hello", 0),
        ("unrelated", b"HTTP/1.1 200 OK\r\nX-Debug: chunked\r\n\r\nhello", 0, b"hello", 0),
        ("duplicate", b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\nContent-Length: 5\r\n\r\n", 248, None, 0),
        ("ambiguous", b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\nTransfer-Encoding: chunked\r\n\r\n", 248, None, 0),
        ("unknown-te", b"HTTP/1.1 200 OK\r\nTransfer-Encoding: gzip\r\n\r\n", 248, None, 0),
        ("too-large", b"HTTP/1.1 200 OK\r\nContent-Length: 600000000\r\n\r\n", 244, None, 0),
        ("zero-length", b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n", 0, b"", 3),
    ]
    for label, response, exit_code, expected, hold in cases:
        dest = root / "build" / "client_download.bg"
        dest.unlink(missing_ok=True)
        ready = threading.Event()
        errors = []

        def serve():
            try:
                with socket.socket() as listener:
                    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    listener.bind((HOST, PORT))
                    listener.listen(1)
                    ready.set()
                    peer, _ = listener.accept()
                    with peer:
                        peer.settimeout(3)
                        peer.recv(2048)
                        peer.sendall(response)
                        if hold:
                            time.sleep(hold)
            except Exception as exc:
                errors.append(exc)
                ready.set()

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        assert ready.wait(5) and not errors, f"{label}: listener failed: {errors}"
        proc = subprocess.run([str(executable)], cwd=root, timeout=2, capture_output=True)
        assert proc.returncode == exit_code, f"{label}: exit {proc.returncode}"
        if expected is not None:
            assert dest.read_bytes() == expected, f"{label}: body mismatch"
        thread.join(timeout=4)
        print("PASS client:", label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=pathlib.Path, required=True)
    parser.add_argument("--server", type=pathlib.Path)
    parser.add_argument("--headers", type=pathlib.Path)
    args = parser.parse_args()
    client = args.client.resolve()
    server = args.server.resolve() if args.server else None
    headers = args.headers.resolve() if args.headers else None
    if headers:
        subprocess.run([str(headers)], check=True, timeout=10)
    with tempfile.TemporaryDirectory(prefix="bagron-net-") as name:
        base = pathlib.Path(name)
        if server:
            server_checks(server, base)
        client_checks(client, base)
    print("All integration tests passed")


if __name__ == "__main__":
    main()
