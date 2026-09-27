"""Hash verification only; never imports torch or loads checkpoint objects."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "checkpoints/MODEL_MANIFEST.json").read_text())
    for item in manifest:
        if not item["included"]:
            continue
        path = root / item["path"]
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest().upper()
        if digest != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise SystemExit("FAIL: " + item["model"])
        print("PASS: " + item["model"] + " " + digest)
    for line in (root / "reproducibility/SHA256SUMS.txt").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        with (root / rel).open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest().upper() != digest:
                raise SystemExit("FAIL: " + rel)
    print("PASS: complete release artifact roster.")


if __name__ == "__main__":
    main()
