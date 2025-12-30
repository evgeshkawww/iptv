#!/bin/bash

INPUT_FILE="IPTV/ico/tabl_ico.txt"
OUTPUT_DIR="IPTV/ico"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r url; do
    filename=$(basename "$url")
    echo "Скачиваю $url -> $OUTPUT_DIR/$filename"
    curl -f -L -A "Mozilla/5.0" "$url" -o "$OUTPUT_DIR/$filename" || echo "Ошибка при скачивании $url"
done < "$INPUT_FILE"
