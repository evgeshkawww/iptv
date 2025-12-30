#!/bin/bash

INPUT_FILE="IPTV/ico/tabl_ico.txt"
OUTPUT_DIR="IPTV/ico"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r url; do
    # убираем пробелы и \r
    clean_url=$(echo "$url" | tr -d '\r' | xargs)
    filename=$(basename "$clean_url")
    echo "Скачиваю $clean_url -> $OUTPUT_DIR/$filename"
    curl -f -L -A "Mozilla/5.0" "$clean_url" -o "$OUTPUT_DIR/$filename" || echo "Ошибка при скачивании $clean_url"
done < "$INPUT_FILE"
