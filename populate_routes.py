#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных трассами с правильной структурой
35 дорожек, по 4 трассы на каждой дорожке (всего 140 трасс)
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import Route

def populate_routes():
    """Заполнение базы данных трассами"""
    
    print("🔄 Начинаем заполнение базы данных трассами...")
    
    # Очищаем существующие данные
    Route.objects.all().delete()
    print("🗑️ Очищена существующая база данных")
    
    # Список сложностей
    difficulties = ['4', '4-5', '5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '7c+', '8a', '8a+', '8b', '8b+', '8c', '9a']
    
    # Список цветов
    colors = ['Красный', 'Синий', 'Зеленый', 'Желтый', 'Фиолетовый', 'Оранжевый', 'Розовый', 'Белый', 'Черный', 'Серый', 'Бирюзовый', 'Коричневый']
    
    # Список авторов
    authors = ['Женя Калашников', 'Alex Prikazchikov', 'Саша Торубарин', 'Никита Бондарев', 'Анна Смирнова', 'Максим Петров', 'Елена Козлова', 'Дмитрий Волков']
    
    # Список названий трасс
    route_names = [
        'Трасса', 'Вертикаль', 'Диагональ', 'Траверс', 'Крыша', 'Стена', 'Угол', 'Переход',
        'Мощь', 'Техника', 'Выносливость', 'Гибкость', 'Баланс', 'Координация', 'Скорость',
        'Терпение', 'Смелость', 'Логика', 'Интуиция', 'Творчество', 'Гармония', 'Энергия',
        'Движение', 'Поток', 'Ритм', 'Мелодия', 'Танец', 'Полет', 'Свобода', 'Мечта'
    ]
    
    route_number = 1
    created_count = 0
    
    # Создаем трассы для каждой дорожки
    for lane in range(1, 36):  # 35 дорожек
        for position in range(1, 5):  # 4 трассы на дорожке
            try:
                # Генерируем случайные данные
                difficulty = random.choice(difficulties)
                color = random.choice(colors)
                author = random.choice(authors)
                name = f"{random.choice(route_names)} {route_number}"
                
                # Генерируем случайную дату в последние 6 месяцев
                days_ago = random.randint(1, 180)
                setup_date = datetime.now() - timedelta(days=days_ago)
                setup_date_str = setup_date.strftime('%d.%m.%Y')
                
                # Создаем описание
                description = f"Трасса на дорожке {lane}, позиция {position}. Сложность: {difficulty}"
                
                # Создаем объект Route
                route = Route(
                    route_number=route_number,
                    track_lane=lane,
                    name=name,
                    difficulty=difficulty,
                    color=color,
                    author=author,
                    setup_date=setup_date_str,
                    description=description,
                    is_active=random.choice([True, True, True, False])  # 75% активных
                )
                
                # Сохраняем в базу данных
                route.save()
                created_count += 1
                route_number += 1
                
                if created_count % 50 == 0:
                    print(f"✅ Создано {created_count} трасс...")
                    
            except Exception as e:
                print(f"❌ Ошибка при создании трассы {route_number}: {str(e)}")
                continue
    
    print(f"\n🎉 Заполнение завершено!")
    print(f"✅ Создано: {created_count} трасс")
    
    # Показываем статистику
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(is_active=True).count()
    inactive_routes = Route.objects.filter(is_active=False).count()
    
    print(f"\n📊 Статистика базы данных:")
    print(f"   Всего трасс: {total_routes}")
    print(f"   Активных: {active_routes}")
    print(f"   Неактивных: {inactive_routes}")
    
    # Показываем распределение по дорожкам
    print(f"\n🛤️ Распределение по дорожкам:")
    for lane in range(1, 36):
        count = Route.objects.filter(track_lane=lane).count()
        if count > 0:
            print(f"   Дорожка {lane}: {count} трасс")
    
    return True

def main():
    """Главная функция"""
    print("🚀 Запуск заполнения базы данных трассами")
    print("=" * 60)
    print("Структура: 35 дорожек, по 4 трассы на каждой (всего 140 трасс)")
    print("=" * 60)
    
    # Запускаем заполнение
    success = populate_routes()
    
    if success:
        print("\n🎉 Заполнение успешно завершено!")
        print("Теперь база данных содержит 140 трасс с правильной структурой")
    else:
        print("\n❌ Заполнение завершилось с ошибками")
        sys.exit(1)

if __name__ == "__main__":
    main()
