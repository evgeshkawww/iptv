import os
from datetime import datetime
import urllib.request

SOURCE_URL = "https://iptv.org.ua/iptv/avto-full.m3u"
APPEND_FILE = os.path.join("IPTV", "assets", "00111112222.m3u")
OUTPUT_FILE = os.path.join("IPTV", "assets", "ropotel7844.m3u")

HEADER_EPG = '#EXTM3U url-tvg="https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg.xml.gz,https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg7.xml.gz,http://epg.one/epg.xml.gz"'

def main():
    # 1. Задаем полные браузерные заголовки для обхода блокировки 403
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://iptv.org.ua/"
    }
    
    req = urllib.request.Request(SOURCE_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    lines = content.splitlines()

    # 2. Формируем дату/время (по времени сервера UTC)
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f"#EXTINF:-1, Ревизия - {now_str}"

    # 3. Меняем заголовок и вторую строку
    lines[0] = HEADER_EPG
    lines[1] = new_revision_line

    # 4. Читаем локальный файл хвоста
    append_lines = []
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_clean = line.rstrip("\r\n")
                if line_clean.startswith("#EXTM3U"):
                    continue
                append_lines.append(line_clean)

    # 5. Склеиваем всё вместе
    all_lines = lines + append_lines

    # 6. Сохраняем в UTF-8 без BOM с переводами строк LF (\n)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_lines) + "\n")

    print(f"Плейлист успешно сформирован: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
