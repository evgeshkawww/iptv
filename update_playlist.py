import os
import re
from datetime import datetime
import urllib.request

SOURCE_URL = "https://iptv.org.ua/iptv/avto-full.m3u"
APPEND_FILE = os.path.join("IPTV", "assets", "00111112222.m3u")
OUTPUT_FILE = os.path.join("IPTV", "assets", "ropotel7844.m3u")

HEADER_EPG = '#EXTM3U url-tvg="https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg.xml.gz,https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg7.xml.gz,http://epg.one/epg.xml.gz"'
PROMO_STREAM_URL = "http://premium-iptv.ru/promo.m3u8"

def clean_group_title(match):
    val = match.group(1)
    # 1. Удаляем упоминания с предлогом или дефисом: "с VPN", "-VPN"
    val = re.sub(r'\s+с\s+VPN\b', '', val, flags=re.IGNORECASE)
    val = re.sub(r'[-–—]\s*VPN\b', '', val, flags=re.IGNORECASE)
    # 2. Удаляем отдельно стоящее слово VPN
    val = re.sub(r'\bVPN\b', '', val, flags=re.IGNORECASE)
    # 3. Удаляем абсолютно ВСЕ круглые скобки ( и ) внутри категории
    val = val.replace('(', '').replace(')', '')
    # 4. Убираем лишние пробелы
    val = re.sub(r'\s{2,}', ' ', val).strip()
    return f'group-title="{val}"'

def main():
    # 1. Задаем браузерные заголовки
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://iptv.org.ua/"
    }
    
    req = urllib.request.Request(SOURCE_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    raw_lines = content.splitlines()

    # 2. Фильтрация KINO ZAL и очистка group-title
    cleaned_lines = []
    skip_current_track = False

    for line in raw_lines:
        line_clean = line.strip()
        
        # Если строка с описанием канала
        if line_clean.startswith("#EXTINF"):
            # Проверяем, не KINO ZAL ли это
            if re.search(r'group-title\s*=\s*["\']KINO ZAL["\']', line_clean, re.IGNORECASE):
                skip_current_track = True
                continue
            else:
                skip_current_track = False
                # Очищаем рубрики от VPN и скобок
                line_clean = re.sub(r'group-title="([^"]*?)"', clean_group_title, line_clean)
                cleaned_lines.append(line_clean)
                continue

        # Если это ссылка или вспомогательный тег (#EXTVLCOPT) удаляемого канала
        if skip_current_track:
            continue

        # Сохраняем остальные строки (пустые строки, EPG заголовок и т.д.)
        cleaned_lines.append(line_clean)

    lines = cleaned_lines

    # 3. Формируем дату/время и категорию для первого канала
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f'#EXTINF:-1 group-title="Приобрести V.I.P⚠️", Ревизия - {now_str}'

    # 4. Меняем заголовок (строка 1), название ревизии с категорией (строка 2) и ссылку на поток (строка 3)
    lines[0] = HEADER_EPG
    lines[1] = new_revision_line
    lines[2] = PROMO_STREAM_URL

    # 5. Читаем локальный файл хвоста
    append_lines = []
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_c = line.rstrip("\r\n")
                if line_c.startswith("#EXTM3U"):
                    continue
                append_lines.append(line_c)

    # 6. Склеиваем всё вместе
    all_lines = lines + append_lines

    # 7. Сохраняем результат в формате UTF-8 LF
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_lines) + "\n")

    print(f"Плейлист успешно сформирован: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
