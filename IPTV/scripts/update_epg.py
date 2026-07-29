#!/usr/bin/env python3
import requests
import os
import sys

# ========== НАСТРОЙКИ ИСТОЧНИКОВ ==========
# Основной EPG
URL_MAIN = "https://epg.team/5.5.xml.gz?pkg=582,722,262,1002,704,482,822,422,263,862,442,802,522,282,762,1022,63,41"
OUT_MAIN = "IPTV/epg.xml.gz"

# EPG7 - ИСПРАВЛЕННЫЙ АДРЕС
URL_EPG7 = "https://iptvx.one/EPG"  # <--- ЗДЕСЬ БЫЛО ИСПРАВЛЕНИЕ
OUT_EPG7 = "IPTV/epg7.xml.gz"

# Минимальный допустимый размер файла в байтах (10 КБ)
MIN_FILE_SIZE = 10 * 1024

# ========== ФУНКЦИЯ СКАЧИВАНИЯ ==========
def download(url, out_file, name):
    """
    Скачивает файл с проверкой:
    - HTTP статуса
    - Content-Type
    - Размера файла
    """
    print(f"📥 Скачиваю {name} из {url}...")
    
    try:
        # Выполняем запрос с таймаутом
        with requests.get(url, stream=True, timeout=60) as r:
            # Проверяем HTTP статус
            r.raise_for_status()
            
            # Проверяем Content-Type (должен быть gzip или application/octet-stream)
            content_type = r.headers.get('content-type', '').lower()
            if not ('gzip' in content_type or 'application' in content_type or 'octet-stream' in content_type):
                print(f"⚠️  {name}: сервер вернул неожиданный Content-Type: {content_type}")
                print(f"   Возможно, это HTML-страница с ошибкой, а не gz-файл")
                return False
            
            # Создаем папку, если её нет
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            
            # Скачиваем файл
            with open(out_file, "wb") as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1 МБ
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            # Проверяем размер скачанного файла
            if downloaded < MIN_FILE_SIZE:
                print(f"⚠️  {name}: файл слишком маленький ({downloaded} байт)")
                print(f"   Минимальный допустимый размер: {MIN_FILE_SIZE} байт")
                print(f"   Возможно, сервер вернул ошибку вместо файла")
                
                # Удаляем битый файл
                if os.path.exists(out_file):
                    os.remove(out_file)
                    print(f"   🗑️  Файл удалён (чтобы не закоммитить пустышку)")
                return False
            
            print(f"✅ {name} обновлён: {out_file} ({downloaded} байт)")
            return True
            
    except requests.exceptions.Timeout:
        print(f"❌ {name}: Таймаут при скачивании (превышено время ожидания)")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ {name}: HTTP ошибка {e.response.status_code}")
        if e.response.status_code == 404:
            print(f"   Файл не найден на сервере (404)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: Ошибка соединения (не могу подключиться к серверу)")
        return False
    except Exception as e:
        print(f"❌ {name}: Неожиданная ошибка: {e}")
        return False

# ========== ОСНОВНАЯ ФУНКЦИЯ ==========
def main():
    """
    Основная функция: скачивает оба EPG-файла.
    Если один не скачался - остальные всё равно будут обработаны.
    """
    print("🚀 Запуск обновления EPG...")
    print("=" * 60)
    
    success_main = download(URL_MAIN, OUT_MAIN, "EPG основной")
    success_epg7 = download(URL_EPG7, OUT_EPG7, "EPG7")
    
    print("=" * 60)
    
    if success_main and success_epg7:
        print("✅ Все файлы успешно обновлены!")
        sys.exit(0)  # Успешный код возврата
    elif success_main:
        print("⚠️  Только основной EPG обновлён, EPG7 пропущен")
        sys.exit(0)  # Всё равно выход с успехом, чтобы не ломать CI
    elif success_epg7:
        print("⚠️  Только EPG7 обновлён, основной EPG пропущен")
        sys.exit(0)
    else:
        print("❌ Ни один файл не был обновлён!")
        sys.exit(1)  # Код ошибки (опционально)

# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    main()
