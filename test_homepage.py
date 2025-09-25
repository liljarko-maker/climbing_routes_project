#!/usr/bin/env python3
"""
Скрипт для тестирования главной страницы веб-приложения
"""

import requests
import json
import time

def test_homepage():
    """Тестирование главной страницы"""
    base_url = "http://127.0.0.1:8000"
    
    print("🏔️ Тестирование главной страницы веб-приложения")
    print("=" * 50)
    
    try:
        # Тест главной страницы
        print("1. Тестирование главной страницы...")
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Главная страница загружается успешно")
            print(f"   Статус: {response.status_code}")
            print(f"   Размер ответа: {len(response.content)} байт")
            
            # Проверяем наличие ключевых элементов
            content = response.text
            if "Управление API трасс скалодрома" in content:
                print("✅ Заголовок найден")
            if "Статистика" in content:
                print("✅ Секция статистики найдена")
            if "API Endpoints" in content:
                print("✅ Секция API найдена")
            if "Тестирование API" in content:
                print("✅ Секция тестирования найдена")
                
        else:
            print(f"❌ Ошибка загрузки главной страницы: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
        print("   Убедитесь, что сервер запущен: python3 manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False
    
    # Тест API endpoints
    print("\n2. Тестирование API endpoints...")
    
    api_endpoints = [
        ("/api/routes/", "GET", "Список трасс"),
        ("/api/stats/", "GET", "Статистика"),
        ("/api/difficulty-levels/", "GET", "Уровни сложности"),
        ("/api/routes/authors/", "GET", "Список авторов"),
        ("/api/routes/colors/", "GET", "Список цветов"),
    ]
    
    for endpoint, method, description in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
            else:
                print(f"⚠️  {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Ошибка - {e}")
    
    # Тест создания трассы
    print("\n3. Тестирование создания трассы...")
    test_route = {
        "name": "Тестовая трасса",
        "author": "Тестовый автор",
        "difficulty": "easy",
        "color": "красный",
        "description": "Описание тестовой трассы"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/routes/",
            json=test_route,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            print("✅ Тестовая трасса создана успешно")
            route_data = response.json()
            print(f"   ID: {route_data.get('id')}")
            print(f"   Название: {route_data.get('name')}")
        else:
            print(f"⚠️  Ошибка создания трассы: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при создании трассы: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print("\nДля просмотра главной страницы откройте:")
    print("http://127.0.0.1:8000/")
    
    return True

if __name__ == "__main__":
    test_homepage()
