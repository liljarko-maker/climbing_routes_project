#!/usr/bin/env python3
"""
Простая демонстрация API трасс скалодрома
Работает без Django - показывает логику работы API
"""

import json
from datetime import datetime

class SimpleRouteAPI:
    """Простая реализация API для трасс"""
    
    def __init__(self):
        self.routes = []
        self.next_id = 1
        
    def add_route(self, name, difficulty, author, color, description=""):
        """Добавление новой трассы"""
        route = {
            "id": self.next_id,
            "name": name,
            "difficulty": difficulty,
            "author": author,
            "color": color,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": True
        }
        
        self.routes.append(route)
        self.next_id += 1
        
        print(f"✅ Трасса '{name}' добавлена успешно! (ID: {route['id']})")
        return route
    
    def get_routes(self):
        """Получение всех трасс"""
        return self.routes
    
    def search_routes(self, **filters):
        """Поиск трасс по критериям"""
        results = self.routes.copy()
        
        if 'difficulty' in filters:
            results = [r for r in results if r['difficulty'] == filters['difficulty']]
        
        if 'author' in filters:
            results = [r for r in results if filters['author'].lower() in r['author'].lower()]
        
        if 'color' in filters:
            results = [r for r in results if filters['color'].lower() in r['color'].lower()]
        
        return results
    
    def get_stats(self):
        """Получение статистики"""
        total = len(self.routes)
        active = len([r for r in self.routes if r['is_active']])
        
        difficulty_stats = {}
        for route in self.routes:
            diff = route['difficulty']
            difficulty_stats[diff] = difficulty_stats.get(diff, 0) + 1
        
        color_stats = {}
        for route in self.routes:
            color = route['color']
            color_stats[color] = color_stats.get(color, 0) + 1
        
        return {
            "total_routes": total,
            "active_routes": active,
            "inactive_routes": total - active,
            "difficulty_distribution": difficulty_stats,
            "color_distribution": color_stats
        }

def print_routes(routes, title="Список трасс"):
    """Красивый вывод списка трасс"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    
    if not routes:
        print("Трассы не найдены")
        return
    
    for route in routes:
        print(f"ID: {route['id']}")
        print(f"Название: {route['name']}")
        print(f"Сложность: {route['difficulty']}")
        print(f"Автор: {route['author']}")
        print(f"Цвет: {route['color']}")
        print(f"Создана: {route['created_at']}")
        if route['description']:
            print(f"Описание: {route['description']}")
        print("-" * 40)

def print_stats(stats):
    """Красивый вывод статистики"""
    print(f"\n{'='*60}")
    print(f" СТАТИСТИКА ТРАСС")
    print(f"{'='*60}")
    print(f"Всего трасс: {stats['total_routes']}")
    print(f"Активных: {stats['active_routes']}")
    print(f"Неактивных: {stats['inactive_routes']}")
    
    print(f"\nПо сложности:")
    for diff, count in stats['difficulty_distribution'].items():
        print(f"  {diff}: {count}")
    
    print(f"\nПо цветам:")
    for color, count in stats['color_distribution'].items():
        print(f"  {color}: {count}")

def main():
    """Основная функция демонстрации"""
    print("🏔️ ДЕМОНСТРАЦИЯ API ТРАСС СКАЛОДРОМА")
    print("=" * 60)
    
    api = SimpleRouteAPI()
    
    # Добавление демонстрационных трасс
    print("\n1️⃣ ДОБАВЛЕНИЕ ТРАСС")
    print("-" * 30)
    
    api.add_route(
        "Красная линия",
        "medium",
        "Иван Петров",
        "красный",
        "Интересная трасса с техничными движениями"
    )
    
    api.add_route(
        "Синий маршрут",
        "easy",
        "Анна Смирнова",
        "синий",
        "Простая трасса для начинающих"
    )
    
    api.add_route(
        "Черная дыра",
        "expert",
        "Михаил Козлов",
        "черный",
        "Экспертная трасса для опытных скалолазов"
    )
    
    api.add_route(
        "Зеленая стена",
        "hard",
        "Елена Волкова",
        "зеленый",
        "Сложная трасса с мощными движениями"
    )
    
    # Показать все трассы
    print("\n2️⃣ ВСЕ ТРАССЫ")
    print("-" * 30)
    all_routes = api.get_routes()
    print_routes(all_routes)
    
    # Поиск по сложности
    print("\n3️⃣ ПОИСК ПО СЛОЖНОСТИ (medium)")
    print("-" * 30)
    medium_routes = api.search_routes(difficulty="medium")
    print_routes(medium_routes, "Средние трассы")
    
    # Поиск по автору
    print("\n4️⃣ ПОИСК ПО АВТОРУ (Иван)")
    print("-" * 30)
    ivan_routes = api.search_routes(author="Иван")
    print_routes(ivan_routes, "Трассы автора Иван")
    
    # Статистика
    print("\n5️⃣ СТАТИСТИКА")
    print("-" * 30)
    stats = api.get_stats()
    print_stats(stats)
    
    # Интерактивный режим
    print("\n6️⃣ ИНТЕРАКТИВНЫЙ РЕЖИМ")
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
        
        if not name or not difficulty or not author or not color:
            print("❌ Все обязательные поля должны быть заполнены!")
            continue
        
        route = api.add_route(name, difficulty, author, color, description)
        
        # Показать обновленный список
        print(f"\n📋 Обновленный список трасс ({len(api.get_routes())} трасс):")
        print_routes(api.get_routes())
    
    # Финальная статистика
    print("\n" + "="*60)
    print(" ФИНАЛЬНАЯ СТАТИСТИКА")
    print("="*60)
    final_stats = api.get_stats()
    print_stats(final_stats)
    
    print("\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("Спасибо за использование API трасс скалодрома!")

if __name__ == "__main__":
    main()
