#!/usr/bin/env python3
"""
Скрипт для тестирования подключения к Google Sheets
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

def test_credentials():
    """Тестирование файла credentials.json"""
    print("🔍 Проверка файла credentials.json...")
    
    credentials_path = 'credentials.json'
    if not os.path.exists(credentials_path):
        print("❌ Файл credentials.json не найден!")
        return False
    
    try:
        import json
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in creds:
                print(f"❌ Отсутствует поле: {field}")
                return False
        
        print(f"✅ Файл credentials.json корректен")
        print(f"   Project ID: {creds['project_id']}")
        print(f"   Client Email: {creds['client_email']}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка чтения credentials.json: {e}")
        return False

def test_google_sheets_connection():
    """Тестирование подключения к Google Sheets"""
    print("\n🔍 Тестирование подключения к Google Sheets...")
    
    try:
        manager = GoogleSheetsManager()
        if not manager.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        # Пытаемся прочитать тестовые данные
        test_data = manager.read_sheet('A1:Z1')
        print(f"✅ Подключение к Google Sheets успешно!")
        print(f"   Прочитано {len(test_data)} строк")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к Google Sheets: {e}")
        return False

def test_export_routes():
    """Тестирование экспорта трасс"""
    print("\n🔍 Тестирование экспорта трасс...")
    
    try:
        # Получаем все трассы
        routes = Route.objects.all()
        routes_data = RouteSerializer(routes, many=True).data
        
        print(f"   Найдено {len(routes_data)} трасс в базе данных")
        
        # Тестируем синхронизацию
        sync = RoutesGoogleSheetsSync()
        success = sync.export_routes_to_sheets(routes_data)
        
        if success:
            print("✅ Экспорт трасс успешен!")
            return True
        else:
            print("❌ Ошибка экспорта трасс")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование Google Sheets интеграции")
    print("=" * 50)
    
    # Проверяем credentials
    if not test_credentials():
        print("\n❌ Тестирование прервано: неверные credentials")
        return
    
    # Проверяем подключение
    if not test_google_sheets_connection():
        print("\n❌ Тестирование прервано: нет подключения к Google Sheets")
        print("\n💡 Убедитесь, что:")
        print("   1. ID таблицы указан в settings.py")
        print("   2. Таблица доступна для service account")
        print("   3. Google Sheets API включен")
        return
    
    # Тестируем экспорт
    test_export_routes()
    
    print("\n✅ Тестирование завершено!")

if __name__ == '__main__':
    main()
