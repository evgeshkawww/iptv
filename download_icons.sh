#!/bin/bash
set -e

INPUT_FILE="IPTV/ico/tabl_ico.txt"
OUTPUT_DIR="IPTV/ico"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r url; do
    # имя файла = последняя часть ссылки
    filename=$(basename "$url")
    echo "Скачиваю $url -> $OUTPUT_DIR/$filename"
    curl -s -L "$url" -o "$OUTPUT_DIR/$filename"
done < "$INPUT_FILE"
