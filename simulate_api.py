#!/usr/bin/env python3
"""
Симуляция API для добавления трасс скалодрома
Демонстрирует работу API без запуска Django сервера
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

class RouteAPI:
    """Симуляция API для работы с трассами"""
    
    def __init__(self):
        self.routes = []
        self.next_id = 1
        self.difficulty_levels = [
            {"value": "easy", "label": "Легкая"},
            {"value": "medium", "label": "Средняя"},
            {"value": "hard", "label": "Сложная"},
            {"value": "expert", "label": "Экспертная"}
        ]
    
    def validate_route_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация данных трассы"""
        errors = {}
        
        # Проверка обязательных полей
        required_fields = ['name', 'difficulty', 'author', 'color']
        for field in required_fields:
            if not data.get(field) or not str(data[field]).strip():
                errors[field] = f"Поле '{field}' обязательно для заполнения"
        
        # Проверка уровня сложности
        if 'difficulty' in data:
            valid_difficulties = [level['value'] for level in self.difficulty_levels]
            if data['difficulty'] not in valid_difficulties:
                errors['difficulty'] = f"Некорректный уровень сложности. Доступные: {', '.join(valid_difficulties)}"
        
        return errors
    
    def create_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание новой трассы"""
        print(f"🔧 Создание трассы: {data.get('name', 'Без названия')}")
        
        # Валидация
        errors = self.validate_route_data(data)
        if errors:
            return {
                "success": False,
                "errors": errors,
                "message": "Ошибки валидации данных"
            }
        
        # Создание трассы
        route = {
            "id": self.next_id,
            "name": data['name'].strip(),
            "difficulty": data['difficulty'],
            "difficulty_display": next(
                level['label'] for level in self.difficulty_levels 
                if level['value'] == data['difficulty']
            ),
            "author": data['author'].strip(),
            "color": data['color'].strip(),
            "created_at": datetime.now().isoformat() + "Z",
            "description": data.get('description', '').strip(),
            "is_active": data.get('is_active', True)
        }
        
        self.routes.append(route)
        self.next_id += 1
        
        print(f"✅ Трасса создана успешно! ID: {route['id']}")
        return {
            "success": True,
            "route": route,
            "message": f"Трасса '{route['name']}' создана успешно"
        }
    
    def get_routes(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Получение списка трасс с фильтрацией"""
        print(f"📋 Получение списка трасс...")
        
        filtered_routes = self.routes.copy()
        
        if filters:
            # Фильтр по сложности
            if 'difficulty' in filters:
                filtered_routes = [r for r in filtered_routes if r['difficulty'] == filters['difficulty']]
            
            # Фильтр по автору
            if 'author' in filters:
                filtered_routes = [r for r in filtered_routes if filters['author'].lower() in r['author'].lower()]
            
            # Фильтр по цвету
            if 'color' in filters:
                filtered_routes = [r for r in filtered_routes if filters['color'].lower() in r['color'].lower()]
            
            # Фильтр по активности
            if 'is_active' in filters:
                filtered_routes = [r for r in filtered_routes if r['is_active'] == filters['is_active']]
            
            # Поиск по названию
            if 'search' in filters:
                search_term = filters['search'].lower()
                filtered_routes = [r for r in filtered_routes if search_term in r['name'].lower()]
        
        return {
            "success": True,
            "routes": filtered_routes,
            "count": len(filtered_routes),
            "message": f"Найдено {len(filtered_routes)} трасс"
        }
    
    def get_route(self, route_id: int) -> Dict[str, Any]:
        """Получение конкретной трассы"""
        print(f"🔍 Поиск трассы с ID: {route_id}")
        
        for route in self.routes:
            if route['id'] == route_id:
                return {
                    "success": True,
                    "route": route,
                    "message": f"Трасса '{route['name']}' найдена"
                }
        
        return {
            "success": False,
            "error": "Трасса не найдена",
            "message": f"Трасса с ID {route_id} не найдена"
        }
    
    def update_route(self, route_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление трассы"""
        print(f"✏️ Обновление трассы с ID: {route_id}")
        
        for i, route in enumerate(self.routes):
            if route['id'] == route_id:
                # Валидация (только для переданных полей)
                validation_data = {k: v for k, v in data.items() if v is not None}
                errors = self.validate_route_data(validation_data)
                if errors:
                    return {
                        "success": False,
                        "errors": errors,
                        "message": "Ошибки валидации данных"
                    }
                
                # Обновление полей
                for key, value in data.items():
                    if value is not None:
                        route[key] = value.strip() if isinstance(value, str) else value
                
                # Обновление отображаемого уровня сложности
                if 'difficulty' in data:
                    route['difficulty_display'] = next(
                        level['label'] for level in self.difficulty_levels 
                        if level['value'] == data['difficulty']
                    )
                
                print(f"✅ Трасса обновлена: {route['name']}")
                return {
                    "success": True,
                    "route": route,
                    "message": f"Трасса '{route['name']}' обновлена успешно"
                }
        
        return {
            "success": False,
            "error": "Трасса не найдена",
            "message": f"Трасса с ID {route_id} не найдена"
        }
    
    def delete_route(self, route_id: int) -> Dict[str, Any]:
        """Удаление трассы"""
        print(f"🗑️ Удаление трассы с ID: {route_id}")
        
        for i, route in enumerate(self.routes):
            if route['id'] == route_id:
                deleted_route = self.routes.pop(i)
                print(f"✅ Трасса удалена: {deleted_route['name']}")
                return {
                    "success": True,
                    "message": f"Трасса '{deleted_route['name']}' удалена успешно"
                }
        
        return {
            "success": False,
            "error": "Трасса не найдена",
            "message": f"Трасса с ID {route_id} не найдена"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики"""
        print("📊 Получение статистики...")
        
        total_routes = len(self.routes)
        active_routes = len([r for r in self.routes if r['is_active']])
        
        # Статистика по сложности
        difficulty_stats = {}
        for level in self.difficulty_levels:
            count = len([r for r in self.routes if r['difficulty'] == level['value']])
            difficulty_stats[level['value']] = {
                "label": level['label'],
                "count": count
            }
        
        # Статистика по цветам
        color_stats = {}
        for route in self.routes:
            color = route['color']
            color_stats[color] = color_stats.get(color, 0) + 1
        
        return {
            "success": True,
            "stats": {
                "total_routes": total_routes,
                "active_routes": active_routes,
                "inactive_routes": total_routes - active_routes,
                "difficulty_distribution": difficulty_stats,
                "color_distribution": color_stats
            },
            "message": "Статистика получена успешно"
        }

def print_response(response: Dict[str, Any], title: str = "API Response"):
    """Красивый вывод ответа API"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2, ensure_ascii=False))

def demo_api():
    """Демонстрация работы API"""
    print("🚀 ЗАПУСК СИМУЛЯЦИИ API ТРАСС СКАЛОДРОМА")
    print("=" * 60)
    
    api = RouteAPI()
    
    # 1. Создание трасс
    print("\n1️⃣ СОЗДАНИЕ ТРАСС")
    print("-" * 30)
    
    test_routes = [
        {
            "name": "Красная линия",
            "difficulty": "medium",
            "author": "Иван Петров",
            "color": "красный",
            "description": "Интересная трасса с техничными движениями"
        },
        {
            "name": "Синий маршрут",
            "difficulty": "easy",
            "author": "Анна Смирнова",
            "color": "синий",
            "description": "Простая трасса для начинающих"
        },
        {
            "name": "Черная дыра",
            "difficulty": "expert",
            "author": "Михаил Козлов",
            "color": "черный",
            "description": "Экспертная трасса для опытных скалолазов"
        }
    ]
    
    for route_data in test_routes:
        response = api.create_route(route_data)
        print_response(response, f"СОЗДАНИЕ: {route_data['name']}")
        time.sleep(0.5)
    
    # 2. Получение списка трасс
    print("\n2️⃣ ПОЛУЧЕНИЕ СПИСКА ТРАСС")
    print("-" * 30)
    response = api.get_routes()
    print_response(response, "СПИСОК ВСЕХ ТРАСС")
    
    # 3. Фильтрация по сложности
    print("\n3️⃣ ФИЛЬТРАЦИЯ ПО СЛОЖНОСТИ")
    print("-" * 30)
    response = api.get_routes({"difficulty": "medium"})
    print_response(response, "СРЕДНИЕ ТРАССЫ")
    
    # 4. Поиск по автору
    print("\n4️⃣ ПОИСК ПО АВТОРУ")
    print("-" * 30)
    response = api.get_routes({"author": "Иван"})
    print_response(response, "ТРАССЫ АВТОРА ИВАН")
    
    # 5. Получение конкретной трассы
    print("\n5️⃣ ПОЛУЧЕНИЕ КОНКРЕТНОЙ ТРАССЫ")
    print("-" * 30)
    response = api.get_route(1)
    print_response(response, "ТРАССА ID 1")
    
    # 6. Обновление трассы
    print("\n6️⃣ ОБНОВЛЕНИЕ ТРАССЫ")
    print("-" * 30)
    update_data = {
        "name": "Обновленная красная линия",
        "description": "Обновленное описание трассы"
    }
    response = api.update_route(1, update_data)
    print_response(response, "ОБНОВЛЕНИЕ ТРАССЫ ID 1")
    
    # 7. Статистика
    print("\n7️⃣ СТАТИСТИКА")
    print("-" * 30)
    response = api.get_stats()
    print_response(response, "СТАТИСТИКА ТРАСС")
    
    # 8. Интерактивный режим
    print("\n8️⃣ ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("-" * 30)
    print("Теперь вы можете добавлять свои трассы!")
    print("Введите данные трассы (или 'quit' для выхода):")
    
    while True:
        print("\n" + "="*40)
        print("ДОБАВЛЕНИЕ НОВОЙ ТРАССЫ")
        print("="*40)
        
        name = input("Название трассы: ").strip()
        if name.lower() == 'quit':
            break
        
        print("Уровни сложности: easy, medium, hard, expert")
        difficulty = input("Сложность: ").strip()
        
        author = input("Автор: ").strip()
        color = input("Цвет: ").strip()
        description = input("Описание (необязательно): ").strip()
        
        route_data = {
            "name": name,
            "difficulty": difficulty,
            "author": author,
            "color": color,
            "description": description
        }
        
        response = api.create_route(route_data)
        print_response(response, "РЕЗУЛЬТАТ СОЗДАНИЯ")
        
        if response["success"]:
            print(f"\n🎉 Трасса '{name}' успешно добавлена!")
        else:
            print(f"\n❌ Ошибка при создании трассы: {response.get('message', 'Неизвестная ошибка')}")
    
    # Финальная статистика
    print("\n" + "="*60)
    print(" ФИНАЛЬНАЯ СТАТИСТИКА")
    print("="*60)
    response = api.get_stats()
    print_response(response, "ИТОГОВАЯ СТАТИСТИКА")
    
    print("\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("Спасибо за использование симуляции API трасс скалодрома!")

if __name__ == "__main__":
    demo_api()
