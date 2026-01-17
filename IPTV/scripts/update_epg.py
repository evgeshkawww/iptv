#!/usr/bin/env python3
import requests

URL = "https://epg.team/5.5.xml.gz?pkg=582,722,262,1002,704,482,822,422,263,862,442,802,522,282,762,1022,63,41"
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
