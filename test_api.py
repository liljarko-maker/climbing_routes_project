#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации API трасс скалодрома
Запуск: python test_api.py
"""

import requests
import json
from datetime import datetime

# Базовый URL API
BASE_URL = "http://127.0.0.1:8000/api"

def print_response(response, title):
    """Красивый вывод ответа API"""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_basic_crud():
    """Тестирование основных CRUD операций"""
    print("\n🔧 ТЕСТИРОВАНИЕ ОСНОВНЫХ CRUD ОПЕРАЦИЙ")
    
    # 1. Получить список трасс
    print("\n1. Получение списка трасс...")
    response = requests.get(f"{BASE_URL}/routes/")
    print_response(response, "СПИСОК ТРАСС")
    
    # 2. Создать новую трассу
    print("\n2. Создание новой трассы...")
    new_route = {
        "name": "Тестовая трасса",
        "difficulty": "medium",
        "author": "Тестовый автор",
        "color": "оранжевый",
        "description": "Трасса для тестирования API"
    }
    response = requests.post(f"{BASE_URL}/routes/", json=new_route)
    print_response(response, "СОЗДАНИЕ ТРАССЫ")
    
    if response.status_code == 201:
        route_id = response.json()['id']
        
        # 3. Получить конкретную трассу
        print(f"\n3. Получение трассы с ID {route_id}...")
        response = requests.get(f"{BASE_URL}/routes/{route_id}/")
        print_response(response, f"ТРАССА ID {route_id}")
        
        # 4. Обновить трассу
        print(f"\n4. Обновление трассы с ID {route_id}...")
        update_data = {
            "name": "Обновленная тестовая трасса",
            "description": "Обновленное описание"
        }
        response = requests.patch(f"{BASE_URL}/routes/{route_id}/", json=update_data)
        print_response(response, f"ОБНОВЛЕНИЕ ТРАССЫ ID {route_id}")
        
        # 5. Переключить статус активности
        print(f"\n5. Переключение статуса активности трассы ID {route_id}...")
        response = requests.post(f"{BASE_URL}/routes/{route_id}/toggle-active/")
        print_response(response, f"ПЕРЕКЛЮЧЕНИЕ СТАТУСА ТРАССЫ ID {route_id}")
        
        return route_id
    else:
        print("❌ Не удалось создать трассу для тестирования")
        return None

def test_bulk_operations():
    """Тестирование массовых операций"""
    print("\n📦 ТЕСТИРОВАНИЕ МАССОВЫХ ОПЕРАЦИЙ")
    
    # 1. Массовое создание трасс
    print("\n1. Массовое создание трасс...")
    bulk_routes = {
        "routes": [
            {
                "name": "Массовая трасса 1",
                "difficulty": "easy",
                "author": "Массовый автор",
                "color": "розовый",
                "description": "Первая массовая трасса"
            },
            {
                "name": "Массовая трасса 2",
                "difficulty": "hard",
                "author": "Массовый автор",
                "color": "голубой",
                "description": "Вторая массовая трасса"
            },
            {
                "name": "Массовая трасса 3",
                "difficulty": "expert",
                "author": "Другой автор",
                "color": "фиолетовый",
                "description": "Третья массовая трасса"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/routes/bulk/", json=bulk_routes)
    print_response(response, "МАССОВОЕ СОЗДАНИЕ ТРАСС")
    
    # Получить ID созданных трасс для дальнейшего тестирования
    created_ids = []
    if response.status_code in [201, 207]:
        for route in response.json().get('created_routes', []):
            created_ids.append(route['id'])
    
    # 2. Массовое обновление трасс
    if created_ids:
        print(f"\n2. Массовое обновление трасс...")
        bulk_updates = {
            "updates": [
                {
                    "id": created_ids[0],
                    "description": "Обновленное описание для массовой трассы 1"
                },
                {
                    "id": created_ids[1],
                    "is_active": False
                }
            ]
        }
        response = requests.post(f"{BASE_URL}/routes/bulk-update/", json=bulk_updates)
        print_response(response, "МАССОВОЕ ОБНОВЛЕНИЕ ТРАСС")
        
        # 3. Массовое удаление трасс
        print(f"\n3. Массовое удаление трасс...")
        bulk_delete = {
            "route_ids": created_ids
        }
        response = requests.delete(f"{BASE_URL}/routes/bulk/", json=bulk_delete)
        print_response(response, "МАССОВОЕ УДАЛЕНИЕ ТРАСС")

def test_search_and_filters():
    """Тестирование поиска и фильтрации"""
    print("\n🔍 ТЕСТИРОВАНИЕ ПОИСКА И ФИЛЬТРАЦИИ")
    
    # 1. Поиск по названию
    print("\n1. Поиск по названию...")
    response = requests.get(f"{BASE_URL}/routes/search/?name=тест")
    print_response(response, "ПОИСК ПО НАЗВАНИЮ")
    
    # 2. Фильтр по сложности
    print("\n2. Фильтр по сложности...")
    response = requests.get(f"{BASE_URL}/routes/search/?difficulty=medium")
    print_response(response, "ФИЛЬТР ПО СЛОЖНОСТИ")
    
    # 3. Фильтр по автору
    print("\n3. Фильтр по автору...")
    response = requests.get(f"{BASE_URL}/routes/search/?author=тест")
    print_response(response, "ФИЛЬТР ПО АВТОРУ")
    
    # 4. Комбинированный поиск
    print("\n4. Комбинированный поиск...")
    response = requests.get(f"{BASE_URL}/routes/search/?difficulty=easy&is_active=true&ordering=name")
    print_response(response, "КОМБИНИРОВАННЫЙ ПОИСК")

def test_additional_endpoints():
    """Тестирование дополнительных endpoints"""
    print("\n📊 ТЕСТИРОВАНИЕ ДОПОЛНИТЕЛЬНЫХ ENDPOINTS")
    
    # 1. Получить уровни сложности
    print("\n1. Получение уровней сложности...")
    response = requests.get(f"{BASE_URL}/difficulty-levels/")
    print_response(response, "УРОВНИ СЛОЖНОСТИ")
    
    # 2. Получить статистику
    print("\n2. Получение статистики...")
    response = requests.get(f"{BASE_URL}/stats/")
    print_response(response, "СТАТИСТИКА ТРАСС")
    
    # 3. Получить список авторов
    print("\n3. Получение списка авторов...")
    response = requests.get(f"{BASE_URL}/routes/authors/")
    print_response(response, "СПИСОК АВТОРОВ")
    
    # 4. Получить список цветов
    print("\n4. Получение списка цветов...")
    response = requests.get(f"{BASE_URL}/routes/colors/")
    print_response(response, "СПИСОК ЦВЕТОВ")

def test_error_handling():
    """Тестирование обработки ошибок"""
    print("\n❌ ТЕСТИРОВАНИЕ ОБРАБОТКИ ОШИБОК")
    
    # 1. Получить несуществующую трассу
    print("\n1. Получение несуществующей трассы...")
    response = requests.get(f"{BASE_URL}/routes/99999/")
    print_response(response, "НЕСУЩЕСТВУЮЩАЯ ТРАССА")
    
    # 2. Создать трассу с некорректными данными
    print("\n2. Создание трассы с некорректными данными...")
    invalid_route = {
        "name": "",  # Пустое название
        "difficulty": "invalid",  # Некорректная сложность
        "author": "",  # Пустой автор
        "color": ""  # Пустой цвет
    }
    response = requests.post(f"{BASE_URL}/routes/", json=invalid_route)
    print_response(response, "НЕКОРРЕКТНЫЕ ДАННЫЕ")

def main():
    """Основная функция тестирования"""
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ API ТРАСС СКАЛОДРОМА")
    print(f"Базовый URL: {BASE_URL}")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Проверка доступности сервера
        response = requests.get(f"{BASE_URL}/stats/")
        if response.status_code != 200:
            print("❌ Сервер недоступен! Убедитесь, что Django сервер запущен.")
            return
        
        # Запуск тестов
        test_basic_crud()
        test_bulk_operations()
        test_search_and_filters()
        test_additional_endpoints()
        test_error_handling()
        
        print("\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print("\nДля просмотра логов проверьте файл climbing_routes.log")
        
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения! Убедитесь, что сервер запущен на http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
