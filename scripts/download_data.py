"""Download a BEIR dataset.

Usage (run from project root):  python -m scripts.download_data scifact
"""
import sys
import zipfile
from pathlib import Path

import httpx

BEIR_URL = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip"
DATA_DIR = Path("data")

def download(name: str) -> Path:
    target = DATA_DIR / name
    if target.exists():
        print(f"{target} already exists, skipping download")
        return target

    DATA_DIR.mkdir(exist_ok=True)
    zip_path = DATA_DIR / f"{name}.zip"
    url = BEIR_URL.format(name=name)
    print(f"Downloading {url} ...")

     # stream=True style: write in pieces instead of holding the whole file in memory
    with httpx.stream("GET", url, follow_redirects=True, timeout=60) as response:
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            for piece in response.iter_bytes():
                f.write(piece)

    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(DATA_DIR)
    zip_path.unlink()  # delete the zip, keep the extracted folder
    print(f"Saved to {target}")
    return target

if __name__ == "__main__":
    download(sys.argv[1] if len(sys.argv) > 1 else "scifact")