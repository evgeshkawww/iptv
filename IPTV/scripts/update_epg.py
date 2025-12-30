#!/usr/bin/env python3
import requests, gzip, shutil, os

URL = "http://epg.team/5.1.xml.gz"
TMP_FILE = "epg.xml.gz"
OUT_FILE = "epg.xml"

def download_epg():
    print("Скачиваю EPG...")
    r = requests.get(URL, stream=True, timeout=60)
    r.raise_for_status()
    with open(TMP_FILE, "wb") as f:
        f.write(r.content)

def unpack_epg():
    print("Распаковываю EPG...")
    with gzip.open(TMP_FILE, "rb") as f_in:
        with open(OUT_FILE, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(TMP_FILE)

if __name__ == "__main__":
    download_epg()
    unpack_epg()
    print("EPG обновлён:", OUT_FILE)

