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
    # 1. Удаляем вариации VPN
    val = re.sub(r'\s+с\s+VPN\b', '', val, flags=re.IGNORECASE)
    val = re.sub(r'[-–—]\s*VPN\b', '', val, flags=re.IGNORECASE)
    val = re.sub(r'\bVPN\b', '', val, flags=re.IGNORECASE)
    # 2. Удаляем абсолютно все круглые скобки
    val = val.replace('(', '').replace(')', '')
    # 3. Убираем лишние пробелы
    val = re.sub(r'\s{2,}', ' ', val).strip()
    return f'group-title="{val}"'

def main():
    # 1. Браузерные заголовки
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

    # 2. Разбиваем плейлист на блоки по каналам
    header_lines = []
    blocks = []
    current_block = []

    for line in raw_lines:
        line_clean = line.rstrip("\r\n")
        if line_clean.startswith("#EXTINF"):
            if current_block:
                blocks.append(current_block)
                current_block = []
            current_block.append(line_clean)
        elif current_block:
            current_block.append(line_clean)
        else:
            header_lines.append(line_clean)
            
    if current_block:
        blocks.append(current_block)

    # 3. Фильтруем: сносим ТОЛЬКО чистый KINO ZAL (4K KINO ZAL остается)
    filtered_lines = list(header_lines)
    for block in blocks:
        extinf_line = block[0]
        
        # Захватываем само значение внутри group-title="..."
        gt_match = re.search(r'group-title="([^"]*)"', extinf_line, re.IGNORECASE)
        if gt_match:
            group_name = gt_match.group(1).strip().lower()
            # Если это строго "kino zal", выкидываем весь блок канала целиком
            if group_name == "kino zal":
                continue

        # Для оставшихся каналов (включая "4K KINO ZAL") чистим скобки и VPN
        block[0] = re.sub(r'group-title="([^"]*?)"', clean_group_title, block[0])
        filtered_lines.extend(block)

    lines = filtered_lines

    # 4. Формируем дату/время и категорию для первого промо-канала
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f'#EXTINF:-1 group-title="Приобрести V.I.P⚠️", Ревизия - {now_str}'

    # 5. Меняем заголовок (строка 1), ревизию (строка 2) и промо-ссылку (строка 3)
    if len(lines) > 0:
        lines[0] = HEADER_EPG
    if len(lines) > 1:
        lines[1] = new_revision_line
    if len(lines) > 2:
        lines[2] = PROMO_STREAM_URL

    # 6. Читаем локальный хвост 00111112222.m3u
    append_lines = []
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_c = line.rstrip("\r\n")
                if line_c.startswith("#EXTM3U"):
                    continue
                append_lines.append(line_c)

    # 7. Склеиваем всё вместе
    all_lines = lines + append_lines

    # 8. Сохраняем результат
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_lines) + "\n")

    print(f"Плейлист успешно сформирован: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
