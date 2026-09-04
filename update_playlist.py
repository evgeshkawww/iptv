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
    # 2. Удаляем круглые скобки
    val = val.replace('(', '').replace(')', '')
    # 3. Убираем лишние пробелы
    val = re.sub(r'\s{2,}', ' ', val).strip()
    return f'group-title="{val}"'

def main():
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

    # 1. Группируем входящий плейлист по блокам (каждый блок = один канал)
    blocks = []
    current_block = []

    for line in raw_lines:
        line_clean = line.rstrip("\r\n")
        # Пропускаем пустые строки и старый заголовок
        if not line_clean or line_clean.startswith("#EXTM3U"):
            continue

        if line_clean.startswith("#EXTINF"):
            if current_block:
                blocks.append(current_block)
                current_block = []
            current_block.append(line_clean)
        elif current_block:
            current_block.append(line_clean)

    if current_block:
        blocks.append(current_block)

    # 2. Фильтрация каналов
    cleaned_channels = []

    for block in blocks:
        extinf_line = block[0]

        # Удаляем старую ревизию источника
        if "Ревизия" in extinf_line or "iptv.org.ua" in extinf_line:
            continue

        # Извлекаем точное значение group-title
        gt_match = re.search(r'group-title="([^"]*)"', extinf_line, re.IGNORECASE)
        if gt_match:
            group_value = gt_match.group(1).strip().upper()
            # Если это в точности "KINO ZAL" — полностью отбрасываем весь блок
            if group_value == "KINO ZAL":
                continue

        # В оставшихся категориях (включая "4K KINO ZAL") убираем VPN и скобки
        block[0] = re.sub(r'group-title="([^"]*?)"', clean_group_title, block[0])
        cleaned_channels.extend(block)

    # 3. Собираем результирующий список строк
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f'#EXTINF:-1 group-title="Приобрести V.I.P⚠️", Ревизия - {now_str}'

    output_lines = [
        HEADER_EPG,
        new_revision_line,
        PROMO_STREAM_URL
    ]

    # Добавляем отфильтрованные каналы из сети
    output_lines.extend(cleaned_channels)

    # 4. Добавляем хвост из файла 00111112222.m3u
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_c = line.rstrip("\r\n")
                if not line_c or line_c.startswith("#EXTM3U"):
                    continue
                output_lines.append(line_c)

    # 5. Записываем файл в UTF-8 без BOM с окончаниями LF (\n)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Готово! Сохранено строк: {len(output_lines)}")

if __name__ == "__main__":
    main()
