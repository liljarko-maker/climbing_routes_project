#!/usr/bin/env python3
"""
Скрипт для тестирования отображения данных из Google Sheets
"""

import requests
import json

def test_api_endpoints():
    """Тестирование API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Тестирование отображения данных из Google Sheets")
    print("=" * 60)
    
    # Тест 1: Проверка статуса Google Sheets
    print("\n1. Проверка статуса Google Sheets...")
    try:
        response = requests.get(f"{base_url}/api/google-sheets/status/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Статус: {data['status']}")
            print(f"   Сообщение: {data['message']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    # Тест 2: Получение данных из Google Sheets
    print("\n2. Получение данных из Google Sheets...")
    try:
        response = requests.get(f"{base_url}/api/google-sheets/routes/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Загружено трасс: {data['count']}")
            print(f"   Источник: {data['source']}")
            
            if data['routes']:
                print("\n   Первые 3 трассы:")
                for i, route in enumerate(data['routes'][:3]):
                    print(f"   {i+1}. №{route['route_number']} - {route['name']} ({route['difficulty']}) - {route['author']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    # Тест 3: Проверка главной страницы
    print("\n3. Проверка главной страницы...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие элементов интерфейса
            checks = [
                ("Переключатель источника данных", "Источник данных" in content),
                ("Кнопка Django БД", "loadDjangoData()" in content),
                ("Кнопка Google Sheets", "loadSheetsData()" in content),
                ("Таблица трасс", "routes-table" in content),
                ("JavaScript функции", "loadSheetsData" in content),
            ]
            
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                
        else:
            print(f"❌ Ошибка загрузки страницы: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    # Тест 4: Сравнение данных Django vs Google Sheets
    print("\n4. Сравнение данных Django vs Google Sheets...")
    try:
        # Данные из Django
        django_response = requests.get(f"{base_url}/api/routes/")
        sheets_response = requests.get(f"{base_url}/api/google-sheets/routes/")
        
        if django_response.status_code == 200 and sheets_response.status_code == 200:
            django_data = django_response.json()
            sheets_data = sheets_response.json()
            
            django_count = len(django_data) if isinstance(django_data, list) else django_data.get('count', 0)
            sheets_count = sheets_data.get('count', 0)
            
            print(f"   Django БД: {django_count} трасс")
            print(f"   Google Sheets: {sheets_count} трасс")
            
            if django_count == sheets_count:
                print("   ✅ Количество трасс совпадает")
            else:
                print("   ⚠️  Количество трасс отличается")
        else:
            print("   ❌ Не удалось загрузить данные для сравнения")
            
    except Exception as e:
        print(f"   ❌ Ошибка сравнения: {e}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == '__main__':
    test_api_endpoints()
