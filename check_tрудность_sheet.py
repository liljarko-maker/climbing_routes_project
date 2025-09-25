#!/usr/bin/env python3
"""
Скрипт для проверки листа "Трудность" в Google Sheets
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

def check_tрудность_sheet():
    """Проверка листа Трудность"""
    print("🔍 Проверка листа 'Трудность'")
    print("=" * 50)
    
    try:
        manager = GoogleSheetsManager()
        if not manager.service:
            print("❌ Google Sheets API не подключен")
            return
        
        print(f"✅ Google Sheets API подключен")
        print(f"   Spreadsheet ID: {manager.spreadsheet_id}")
        
        # Получаем информацию о таблице
        spreadsheet = manager.service.spreadsheets().get(
            spreadsheetId=manager.spreadsheet_id
        ).execute()
        
        print(f"\n📋 Название таблицы: {spreadsheet.get('properties', {}).get('title', 'Unknown')}")
        
        # Получаем список листов
        sheets = spreadsheet.get('sheets', [])
        print(f"\n📊 Найдено листов: {len(sheets)}")
        
        трудность_sheet = None
        for i, sheet in enumerate(sheets):
            title = sheet.get('properties', {}).get('title', 'Unknown')
            sheet_id = sheet.get('properties', {}).get('sheetId', 'Unknown')
            print(f"   {i+1}. '{title}' (ID: {sheet_id})")
            
            if title == 'Трудность':
                трудность_sheet = sheet
                print(f"      ✅ Найден лист 'Трудность'")
        
        if not трудность_sheet:
            print("\n❌ Лист 'Трудность' не найден!")
            return
        
        # Читаем данные из листа Трудность
        print(f"\n📖 Чтение данных из листа 'Трудность'...")
        try:
            data = manager.read_sheet('Трудность!A1:Z20')
            print(f"✅ Прочитано {len(data)} строк")
            
            if data:
                print(f"\n📋 Заголовки:")
                for i, header in enumerate(data[0]):
                    print(f"   {i+1}. {header}")
                
                if len(data) > 1:
                    print(f"\n📊 Первая строка данных:")
                    for i, cell in enumerate(data[1]):
                        print(f"   {data[0][i] if i < len(data[0]) else f'Column {i+1}'}: {cell}")
                
                if len(data) > 2:
                    print(f"\n📊 Вторая строка данных:")
                    for i, cell in enumerate(data[2]):
                        print(f"   {data[0][i] if i < len(data[0]) else f'Column {i+1}'}: {cell}")
                        
        except Exception as e:
            print(f"❌ Ошибка чтения данных: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_tрудность_sheet()
