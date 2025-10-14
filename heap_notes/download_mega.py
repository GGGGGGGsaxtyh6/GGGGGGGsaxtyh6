#!/usr/bin/env python3
from mega import Mega
import sys

URL = "https://mega.nz/file/471yUTZQ#GVK25pDR3U-gd3GuAsyGCl3km8_lGRqCSP33AWnUFRo"

def main():
    out_dir = "."
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    m = Mega()
    a = m.login()  # anonymous
    print("Downloading...", flush=True)
    file = a.download_url(URL, dest_path=out_dir)
    print(f"Saved: {file}")

if __name__ == "__main__":
    main()
