"""Create a net.lib containing API modules, not example main() symbols.

Requires Bagron in PATH; only the Python standard library is used.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bagron", default="bagron")
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "net.lib")
    parser.add_argument("--version", default="1.0.0")
    args = parser.parse_args()
    if not (ROOT / "library.bg").is_file() or not (ROOT / "modules").is_dir():
        parser.error("library.bg and modules/ must exist")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bagron-net-lib-") as directory:
        source = Path(directory) / "net"
        source.mkdir()
        shutil.copy2(ROOT / "library.bg", source / "main.bg")
        shutil.copytree(ROOT / "modules", source / "modules")
        subprocess.run([args.bagron, "library", "--v1", str(source), "-o",
                        str(output), "--name", "net", "--version", args.version], check=True)
    subprocess.run([args.bagron, "verify", str(output)], check=True)
    print(f"Validated package: {output}")


if __name__ == "__main__":
    main()
