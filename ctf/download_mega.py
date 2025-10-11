import sys, os
from mega import Mega

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: download_mega.py <mega_url> [dest_dir]")
        sys.exit(1)
    url = sys.argv[1]
    dest_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(dest_dir, exist_ok=True)
    mega = Mega()
    result = mega.download_url(url, dest_dir)
    # mega.py may return the path or None; list directory to find newest file
    if result:
        print(result)
    else:
        # attempt to identify the most recent file in dest_dir
        entries = sorted(
            (os.path.join(dest_dir, f) for f in os.listdir(dest_dir)),
            key=lambda p: os.path.getmtime(p),
            reverse=True,
        )
        if entries:
            print(entries[0])
        else:
            print("downloaded")
