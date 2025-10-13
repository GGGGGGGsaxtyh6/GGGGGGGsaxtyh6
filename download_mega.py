import sys
from mega import Mega

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: download_mega.py <url> <dest_dir>")
        sys.exit(1)
    url = sys.argv[1]
    dest_dir = sys.argv[2]
    mega = Mega()
    m = mega.login()  # anonymous
    path = m.download_url(url, dest_dir)
    print(path)
