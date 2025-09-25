#!/usr/bin/env python3
"""
Скрипт для импорта данных из Google Sheets в SQLite базу данных
"""

import os
import sys
import django
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import Route
from routes.google_sheets import RoutesGoogleSheetsSync

def import_routes_from_google_sheets():
    """Импорт трасс из Google Sheets в SQLite базу данных"""
    
    print("🔄 Начинаем импорт данных из Google Sheets...")
    
    try:
        # Подключаемся к Google Sheets
        sync = RoutesGoogleSheetsSync()
        routes_data = sync.import_routes_from_sheets()
        
        print(f"📊 Получено {len(routes_data)} трасс из Google Sheets")
        
        # Очищаем существующие данные
        Route.objects.all().delete()
        print("🗑️ Очищена существующая база данных")
        
        # Импортируем новые данные
        imported_count = 0
        skipped_count = 0
        track_number_counter = 1
        
        for route_data in routes_data:
            try:
                # Генерируем номер трассы, если его нет
                track_number = route_data.get('track_number')
                if not track_number or track_number == 0:
                    track_number = track_number_counter
                    track_number_counter += 1
                
                # Создаем объект Route
                route = Route(
                    track_number=track_number,
                    track_lane=route_data.get('track_lane', 1),
                    name=route_data.get('name', ''),
                    difficulty=route_data.get('difficulty', '-'),
                    color=route_data.get('color', ''),
                    author=route_data.get('author', ''),
                    setup_date=route_data.get('setup_date', ''),
                    description=route_data.get('description', ''),
                    is_active=route_data.get('is_active', True)
                )
                
                # Сохраняем в базу данных
                route.save()
                imported_count += 1
                
                if imported_count % 50 == 0:
                    print(f"✅ Импортировано {imported_count} трасс...")
                    
            except Exception as e:
                print(f"❌ Ошибка при импорте трассы {route_data.get('name', 'Unknown')}: {str(e)}")
                skipped_count += 1
                continue
        
        print(f"\n🎉 Импорт завершен!")
        print(f"✅ Успешно импортировано: {imported_count} трасс")
        print(f"❌ Пропущено: {skipped_count} трасс")
        
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
        
    except Exception as e:
        print(f"❌ Критическая ошибка при импорте: {str(e)}")
        return False

def main():
    """Главная функция"""
    print("🚀 Запуск импорта данных из Google Sheets в SQLite")
    print("=" * 60)
    
    # Проверяем подключение к Google Sheets
    try:
        sync = RoutesGoogleSheetsSync()
        print("✅ Подключение к Google Sheets установлено")
    except Exception as e:
        print(f"❌ Ошибка подключения к Google Sheets: {str(e)}")
        return
    
    # Запускаем импорт
    success = import_routes_from_google_sheets()
    
    if success:
        print("\n🎉 Импорт успешно завершен!")
        print("Теперь все данные хранятся в SQLite базе данных")
    else:
        print("\n❌ Импорт завершился с ошибками")
        sys.exit(1)

if __name__ == "__main__":
    main()
