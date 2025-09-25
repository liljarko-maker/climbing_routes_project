#!/usr/bin/env python3
"""
Демонстрационный скрипт для быстрого тестирования API
Запуск: python demo.py
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def demo_quick_test():
    """Быстрая демонстрация основных возможностей API"""
    print("🎯 БЫСТРАЯ ДЕМОНСТРАЦИЯ API ТРАСС СКАЛОДРОМА")
    print("=" * 60)
    
    # 1. Создать несколько тестовых трасс
    print("\n1️⃣ Создание тестовых трасс...")
    test_routes = [
        {
            "name": "Красная стена",
            "difficulty": "easy",
            "author": "Иван Петров",
            "color": "красный",
            "description": "Простая трасса для начинающих"
        },
        {
            "name": "Синий маршрут",
            "difficulty": "medium",
            "author": "Анна Смирнова",
            "color": "синий",
            "description": "Средняя сложность с техничными движениями"
        },
        {
            "name": "Черная дыра",
            "difficulty": "expert",
            "author": "Михаил Козлов",
            "color": "черный",
            "description": "Экспертная трасса для опытных скалолазов"
        }
    ]
    
    created_routes = []
    for route in test_routes:
        response = requests.post(f"{BASE_URL}/routes/", json=route)
        if response.status_code == 201:
            created_routes.append(response.json())
            print(f"   ✅ Создана: {route['name']}")
        else:
            print(f"   ❌ Ошибка создания: {route['name']}")
    
    # 2. Показать все трассы
    print(f"\n2️⃣ Получение всех трасс ({len(created_routes)} создано)...")
    response = requests.get(f"{BASE_URL}/routes/")
    if response.status_code == 200:
        routes = response.json()
        print(f"   📊 Всего трасс в базе: {len(routes)}")
        for route in routes[:3]:  # Показать первые 3
            print(f"   • {route['name']} ({route['difficulty_display']}) - {route['author']}")
    
    # 3. Поиск по сложности
    print(f"\n3️⃣ Поиск средних трасс...")
    response = requests.get(f"{BASE_URL}/routes/search/?difficulty=medium")
    if response.status_code == 200:
        results = response.json()
        print(f"   🔍 Найдено средних трасс: {results['count']}")
        for route in results['results']:
            print(f"   • {route['name']} - {route['author']}")
    
    # 4. Получить статистику
    print(f"\n4️⃣ Статистика трасс...")
    response = requests.get(f"{BASE_URL}/stats/")
    if response.status_code == 200:
        stats = response.json()
        print(f"   📈 Всего трасс: {stats['total_routes']}")
        print(f"   ✅ Активных: {stats['active_routes']}")
        print(f"   ❌ Неактивных: {stats['inactive_routes']}")
        
        print(f"   📊 По сложности:")
        for difficulty, data in stats['difficulty_distribution'].items():
            print(f"     • {data['label']}: {data['count']}")
    
    # 5. Получить список авторов
    print(f"\n5️⃣ Список авторов...")
    response = requests.get(f"{BASE_URL}/routes/authors/")
    if response.status_code == 200:
        authors = response.json()
        print(f"   👥 Авторов: {len(authors)}")
        for author in authors:
            print(f"   • {author['name']}: {author['total_routes']} трасс")
    
    # 6. Массовое создание
    print(f"\n6️⃣ Массовое создание трасс...")
    bulk_routes = {
        "routes": [
            {
                "name": "Зеленая линия",
                "difficulty": "easy",
                "author": "Демо автор",
                "color": "зеленый"
            },
            {
                "name": "Фиолетовая мечта",
                "difficulty": "hard",
                "author": "Демо автор",
                "color": "фиолетовый"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/routes/bulk/", json=bulk_routes)
    if response.status_code in [201, 207]:
        result = response.json()
        print(f"   ✅ Создано: {len(result.get('created_routes', []))} трасс")
        if result.get('errors'):
            print(f"   ⚠️ Ошибок: {len(result['errors'])}")
    
    print(f"\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print(f"   🌐 API доступно по адресу: {BASE_URL}")
    print(f"   📚 Документация: {BASE_URL}/routes/")
    print(f"   🔧 Админ-панель: http://127.0.0.1:8000/admin/")

def check_server():
    """Проверка доступности сервера"""
    try:
        response = requests.get(f"{BASE_URL}/stats/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 ДЕМОНСТРАЦИЯ API ТРАСС СКАЛОДРОМА")
    print("=" * 50)
    
    # Проверка сервера
    print("🔍 Проверка доступности сервера...")
    if not check_server():
        print("❌ Сервер недоступен!")
        print("   Убедитесь, что Django сервер запущен:")
        print("   python manage.py runserver")
        return
    
    print("✅ Сервер доступен!")
    time.sleep(1)
    
    # Запуск демонстрации
    demo_quick_test()

if __name__ == "__main__":
    main()
