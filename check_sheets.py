#!/usr/bin/env python3
"""
Скрипт для проверки структуры Google таблицы
"""

import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('/Users/Kostya/Documents/climbing_routes_project')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.google_sheets import GoogleSheetsManager

def check_sheets_structure():
    """Проверяет структуру Google таблицы"""
    print("🔍 Проверка структуры Google таблицы...")
    
    try:
        manager = GoogleSheetsManager()
        if not manager.service:
            print("❌ Google Sheets API не инициализирован")
            return
        
        # Получаем информацию о таблице
        spreadsheet = manager.service.spreadsheets().get(
            spreadsheetId=manager.spreadsheet_id
        ).execute()
        
        print(f"✅ Таблица найдена: {spreadsheet.get('properties', {}).get('title', 'Unknown')}")
        print(f"   ID: {manager.spreadsheet_id}")
        
        # Получаем список листов
        sheets = spreadsheet.get('sheets', [])
        print(f"\n📋 Найдено листов: {len(sheets)}")
        
        for i, sheet in enumerate(sheets):
            properties = sheet.get('properties', {})
            title = properties.get('title', f'Sheet{i+1}')
            sheet_id = properties.get('sheetId', 'Unknown')
            print(f"   {i+1}. '{title}' (ID: {sheet_id})")
        
        # Проверяем, есть ли лист Routes
        routes_sheet = None
        for sheet in sheets:
            if sheet.get('properties', {}).get('title') == 'Routes':
                routes_sheet = sheet
                break
        
        if routes_sheet:
            print("\n✅ Лист 'Routes' найден!")
        else:
            print("\n❌ Лист 'Routes' не найден!")
            print("💡 Нужно создать лист с названием 'Routes'")
            
            # Предлагаем создать лист
            try:
                create_sheet_request = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': 'Routes'
                            }
                        }
                    }]
                }
                
                result = manager.service.spreadsheets().batchUpdate(
                    spreadsheetId=manager.spreadsheet_id,
                    body=create_sheet_request
                ).execute()
                
                print("✅ Лист 'Routes' создан успешно!")
                
            except Exception as e:
                print(f"❌ Ошибка создания листа: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка проверки таблицы: {e}")

if __name__ == '__main__':
    check_sheets_structure()
