"""Show official acquisition instructions or verify explicitly supplied MRI headers."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("t1", "t1ce", "t2", "flair"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    paths = [getattr(args, name) for name in ("t1", "t1ce", "t2", "flair")]
    if not any(paths):
        print("Request BraTS 2020 through the official access process:")
        print("https://www.med.upenn.edu/cbica/brats2020/registration.html")
        print("https://www.med.upenn.edu/cbica/brats2020/data.html")
        print("After accepting the provider's terms yourself, supply --t1 --t1ce --t2 --flair to verify headers.")
        return
    if not all(paths):
        parser.error("Supply all four modality paths.")
    from src.data.preprocessing import inspect_headers
    inspect_headers(paths)
    print("PASS: four aligned 240 x 240 x 155 volumes with 1 mm spacing. No inference performed.")


if __name__ == "__main__":
    main()
