#!/usr/bin/env python3
import requests

URL = "https://epg.team/5.1.xml.gz"
OUT_FILE = "IPTV/epg.xml.gz"

def download_epg():
    print("Скачиваю EPG...")
    r = requests.get(URL, stream=True, timeout=60)
    r.raise_for_status()
    with open(OUT_FILE, "wb") as f:
        f.write(r.content)
    print("EPG обновлён:", OUT_FILE)

if __name__ == "__main__":
    download_epg()
