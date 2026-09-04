import os
import re
from datetime import datetime
import urllib.request

SOURCE_URL = "https://iptv.org.ua/iptv/avto-full.m3u"
APPEND_FILE = os.path.join("IPTV", "assets", "00111112222.m3u")
OUTPUT_FILE = os.path.join("IPTV", "assets", "ropotel7844.m3u")

HEADER_EPG = '#EXTM3U url-tvg="https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg.xml.gz,https://raw.githubusercontent.com/evgeshkawww/iptv/main/IPTV/epg7.xml.gz,http://epg.one/epg.xml.gz"'
PROMO_STREAM_URL = "http://premium-iptv.ru/promo.m3u8"

def clean_group_name(val):
    # Заменяем возможные неразрывные пробелы
    val = val.replace('\xa0', ' ')
    # 1. Удаляем вариации VPN
    val = re.sub(r'\s+с\s+VPN\b', '', val, flags=re.IGNORECASE)
    val = re.sub(r'[-–—]\s*VPN\b', '', val, flags=re.IGNORECASE)
    val = re.sub(r'\bVPN\b', '', val, flags=re.IGNORECASE)
    # Удаляем слово Portal (если вдруг осталось в локальном файле)
    val = re.sub(r'\bPortal\b', '', val, flags=re.IGNORECASE)
    # 2. Удаляем абсолютно все круглые скобки
    val = val.replace('(', '').replace(')', '')
    # 3. Убираем лишние пробелы
    val = re.sub(r'\s{2,}', ' ', val).strip()
    return val

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://iptv.org.ua/"
    }
    
    raw_lines = []

    # 1. Читаем скачиваемый плейлист
    req = urllib.request.Request(SOURCE_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        raw_lines.extend(content.splitlines())

    # 2. СРАЗУ читаем локальный файл хвоста, чтобы фильтровать ВСЁ вместе
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                raw_lines.append(line)

    # 3. Разбиваем все строки на блоки (каждый канал — отдельный блок)
    blocks = []
    current_block = []

    for line in raw_lines:
        line_clean = line.rstrip("\r\n")
        # Игнорируем пустые строки и старые M3U-заголовки
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

    # 4. Фильтрация и очистка категорий для ОБОИХ файлов
    cleaned_channels = []

    for block in blocks:
        extinf_line = block[0]

        # Выкидываем оригинальную строку ревизии от источника
        if "Ревизия" in extinf_line or "iptv.org.ua" in extinf_line or "tva.org.ua" in extinf_line:
            continue

        # Извлекаем значение group-title
        gt_match = re.search(r'group-title="([^"]*)"', extinf_line, re.IGNORECASE)
        if gt_match:
            raw_group = gt_match.group(1)
            clean_group = clean_group_name(raw_group)

            # ЖЕЛЕЗНАЯ ПРОВЕРКА: если получилось строго "KINO ZAL" — выкидываем весь канал!
            if clean_group.upper() == "KINO ZAL":
                continue

            # Для оставшихся (включая "4K KINO ZAL") обновляем рубрику без скобок и VPN
            block[0] = extinf_line[:gt_match.start(1)] + clean_group + extinf_line[gt_match.end(1):]

        cleaned_channels.extend(block)

    # 5. Собираем итоговый плейлист с правильной шапкой
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_revision_line = f'#EXTINF:-1 group-title="Приобрести V.I.P⚠️", Ревизия - {now_str}'

    output_lines = [
        HEADER_EPG,
        new_revision_line,
        PROMO_STREAM_URL
    ]

    output_lines.extend(cleaned_channels)

    # 6. Сохраняем результат
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Готово! Сохранено строк: {len(output_lines)}")

if __name__ == "__main__":
    main()
