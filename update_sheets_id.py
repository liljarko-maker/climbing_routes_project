#!/usr/bin/env python3
"""
Скрипт для обновления ID Google таблицы в settings.py
"""

import re
import sys

def update_sheets_id(new_id):
    """Обновляет ID Google таблицы в settings.py"""
    
    settings_file = 'climbing_routes_project/settings.py'
    
    try:
        # Читаем файл
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем ID
        old_pattern = r"GOOGLE_SHEETS_ID = 'your-google-sheets-id-here'"
        new_pattern = f"GOOGLE_SHEETS_ID = '{new_id}'"
        
        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, new_pattern, content)
            
            # Записываем обновленный файл
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ ID Google таблицы обновлен: {new_id}")
            return True
        else:
            print("❌ Не найден placeholder для замены")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка обновления файла: {e}")
        return False

def main():
    """Основная функция"""
    if len(sys.argv) != 2:
        print("Использование: python update_sheets_id.py <SHEETS_ID>")
        print("\nПример:")
        print("python update_sheets_id.py 1ABC123DEF456GHI789JKL")
        print("\nID таблицы находится в URL между /d/ и /edit")
        print("https://docs.google.com/spreadsheets/d/1ABC123DEF456GHI789JKL/edit")
        return
    
    sheets_id = sys.argv[1]
    
    # Валидация ID (должен содержать только буквы, цифры, дефисы и подчеркивания)
    if not re.match(r'^[a-zA-Z0-9_-]+$', sheets_id):
        print("❌ Неверный формат ID таблицы")
        print("ID должен содержать только буквы, цифры, дефисы и подчеркивания")
        return
    
    update_sheets_id(sheets_id)

if __name__ == '__main__':
    main()
