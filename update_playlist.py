import os
import re
from datetime import datetime
import urllib.request

SOURCE_URL = "https://iptv.org.ua/iptv/avto-full.m3u"
APPEND_FILE = os.path.join("IPTV", "assets", "00111112222.m3u")
OUTPUT_FILE = os.path.join("IPTV", "assets", "ropotel7844.m3u")

HEADER_EPG = '#EXTM3U url-tvg="https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg.xml.gz,https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg7.xml.gz,http://epg.one/epg.xml.gz"'

def main():
    # 1. Скачиваем исходный плейлист
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    lines = content.splitlines()

    # 2. Формируем дату/время (по времени сервера GitHub / UTC)
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f"#EXTINF:-1, Ревизия - {now_str}"

    # 3. Меняем заголовок и вторую строку
    lines[0] = HEADER_EPG
    lines[1] = new_revision_line
    # lines[2] (родная ссылка на поток) остается нетронутой

    # 4. Читаем локальный файл хвоста, если он существует
    append_lines = []
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_clean = line.rstrip("\r\n")
                # Пропускаем дублирующий заголовок #EXTM3U, если он есть в файле
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
