#!/usr/bin/env python3
import requests

URL_MAIN = "https://epg.team/5.5.xml.gz?pkg=582,722,262,1002,704,482,822,422,263,862,442,802,522,282,762,1022,63,41"
OUT_MAIN = "IPTV/epg.xml.gz"

URL_EPG7 = "https://iptvx.one/EPG7"
OUT_EPG7 = "IPTV/epg7.xml.gz"


def download(url, out_file, name):
    print(f"Скачиваю {name}...")
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(out_file, "wb") as f:
        f.write(r.content)
    print(f"{name} обновлён: {out_file}")


if __name__ == "__main__":
    download(URL_MAIN, OUT_MAIN, "EPG основной")
    download(URL_EPG7, OUT_EPG7, "EPG7")
