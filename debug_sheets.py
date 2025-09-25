#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с Google Sheets
"""

import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('/Users/Kostya/Documents/climbing_routes_project')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.google_sheets import GoogleSheetsManager, RoutesGoogleSheetsSync
from routes.models import Route
from routes.serializers import RouteSerializer

def debug_sheets_data():
    """Диагностика данных Google Sheets"""
    print("🔍 Диагностика Google Sheets")
    print("=" * 50)
    
    # 1. Проверяем подключение
    print("\n1. Проверка подключения...")
    try:
        manager = GoogleSheetsManager()
        if manager.service:
            print("✅ Google Sheets API подключен")
            print(f"   Spreadsheet ID: {manager.spreadsheet_id}")
        else:
            print("❌ Google Sheets API не подключен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    # 2. Читаем сырые данные из Google Sheets
    print("\n2. Чтение сырых данных из Google Sheets...")
    try:
        raw_data = manager.read_sheet('Routes!A1:Z100')
        print(f"✅ Прочитано {len(raw_data)} строк")
        
        if raw_data:
            print("   Заголовки:", raw_data[0])
            if len(raw_data) > 1:
                print("   Первая строка данных:", raw_data[1])
            if len(raw_data) > 2:
                print("   Вторая строка данных:", raw_data[2])
    except Exception as e:
        print(f"❌ Ошибка чтения: {e}")
        return
    
    # 3. Проверяем импорт через RoutesGoogleSheetsSync
    print("\n3. Проверка импорта через RoutesGoogleSheetsSync...")
    try:
        sync = RoutesGoogleSheetsSync()
        imported_data = sync.import_routes_from_sheets()
        print(f"✅ Импортировано {len(imported_data)} трасс")
        
        if imported_data:
            print("   Первая трасса:")
            for key, value in imported_data[0].items():
                print(f"     {key}: {value}")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Сравниваем с данными Django
    print("\n4. Сравнение с данными Django...")
    try:
        django_routes = Route.objects.all()
        django_data = RouteSerializer(django_routes, many=True).data
        
        print(f"   Django БД: {len(django_data)} трасс")
        print(f"   Google Sheets: {len(imported_data)} трасс")
        
        if len(django_data) != len(imported_data):
            print("   ⚠️  Количество трасс отличается!")
        
        # Проверяем первые несколько трасс
        print("\n   Сравнение первых 3 трасс:")
        for i in range(min(3, len(django_data), len(imported_data))):
            django_route = django_data[i]
            sheets_route = imported_data[i]
            
            print(f"\n   Трасса {i+1}:")
            print(f"     Django: №{django_route.get('route_number')} - {django_route.get('name')}")
            print(f"     Sheets: №{sheets_route.get('route_number')} - {sheets_route.get('name')}")
            
            if django_route.get('name') != sheets_route.get('name'):
                print("     ⚠️  Названия не совпадают!")
            
    except Exception as e:
        print(f"❌ Ошибка сравнения: {e}")
    
    # 5. Проверяем время последнего обновления
    print("\n5. Проверка времени обновления...")
    try:
        # Получаем информацию о таблице
        spreadsheet = manager.service.spreadsheets().get(
            spreadsheetId=manager.spreadsheet_id
        ).execute()
        
        print(f"   Название таблицы: {spreadsheet.get('properties', {}).get('title', 'Unknown')}")
        
        # Проверяем листы
        sheets = spreadsheet.get('sheets', [])
        routes_sheet = None
        for sheet in sheets:
            if sheet.get('properties', {}).get('title') == 'Routes':
                routes_sheet = sheet
                break
        
        if routes_sheet:
            print("   ✅ Лист 'Routes' найден")
            print(f"   ID листа: {routes_sheet.get('properties', {}).get('sheetId')}")
        else:
            print("   ❌ Лист 'Routes' не найден")
            
    except Exception as e:
        print(f"❌ Ошибка получения информации о таблице: {e}")

if __name__ == '__main__':
    debug_sheets_data()
