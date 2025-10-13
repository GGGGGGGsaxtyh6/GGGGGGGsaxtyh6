from mega import Mega
import sys

URL = "https://mega.nz/file/h7VmXBhC#jW1lH565j3ST9eeYLLcr6LjzOnOxX_Vx7FYpWFTJOEs"
DEST_DIR = "/workspace"

def main():
    mega = Mega()
    m = mega.login()  # anonymous
    out_path = m.download_url(URL, DEST_DIR)
    print(out_path)

if __name__ == "__main__":
    main()
