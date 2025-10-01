#!/usr/bin/env python3
"""
Скрипт для экспорта данных из локальной базы в хостинг PythonAnywhere
"""

import os
import django
import requests
import json
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import Route, AdminUser

def export_routes_to_hosting():
    """Экспорт трасс на хостинг"""
    print("🚀 Начинаем экспорт трасс на хостинг...")
    
    # URL хостинга
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Получаем все трассы из локальной базы
    routes = Route.objects.all()
    print(f"📊 Найдено {routes.count()} трасс в локальной базе")
    
    exported_count = 0
    failed_count = 0
    
    for route in routes:
        try:
            # Подготавливаем данные для отправки
            route_data = {
                'route_number': route.route_number,
                'track_lane': route.track_lane,
                'name': route.name,
                'difficulty': route.difficulty,
                'author': route.author,
                'color': route.color,
                'setup_date': str(route.setup_date) if route.setup_date else '',
                'description': route.description or '',
                'is_active': route.is_active
            }
            
            # Отправляем POST запрос на хостинг
            response = requests.post(
                f"{hosting_url}/api/routes/",
                json=route_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                exported_count += 1
                print(f"✅ Трасса {route.route_number} ({route.name}) экспортирована")
            else:
                failed_count += 1
                print(f"❌ Ошибка экспорта трассы {route.route_number}: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Ошибка при экспорте трассы {route.route_number}: {e}")
    
    print(f"\n📈 Результаты экспорта:")
    print(f"✅ Успешно экспортировано: {exported_count}")
    print(f"❌ Ошибок: {failed_count}")
    
    return exported_count, failed_count

def export_admin_users_to_hosting():
    """Экспорт админ пользователей на хостинг"""
    print("\n👤 Начинаем экспорт админ пользователей...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Получаем всех админ пользователей
    admin_users = AdminUser.objects.all()
    print(f"👥 Найдено {admin_users.count()} админ пользователей")
    
    exported_count = 0
    failed_count = 0
    
    for admin in admin_users:
        try:
            # Подготавливаем данные для отправки
            admin_data = {
                'username': admin.username,
                'password': 'admin123',  # Используем стандартный пароль
                'full_name': admin.full_name
            }
            
            # Отправляем POST запрос на хостинг
            response = requests.post(
                f"{hosting_url}/api/admin/create/",
                json=admin_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                exported_count += 1
                print(f"✅ Админ пользователь {admin.username} экспортирован")
            else:
                failed_count += 1
                print(f"❌ Ошибка экспорта админа {admin.username}: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Ошибка при экспорте админа {admin.username}: {e}")
    
    print(f"\n📈 Результаты экспорта админов:")
    print(f"✅ Успешно экспортировано: {exported_count}")
    print(f"❌ Ошибок: {failed_count}")
    
    return exported_count, failed_count

def check_hosting_status():
    """Проверка статуса хостинга"""
    print("🔍 Проверяем статус хостинга...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    try:
        # Проверяем главную страницу
        response = requests.get(f"{hosting_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Главная страница хостинга доступна")
        else:
            print(f"❌ Главная страница недоступна: {response.status_code}")
            return False
            
        # Проверяем API
        response = requests.get(f"{hosting_url}/api/routes/", timeout=10)
        if response.status_code == 200:
            print("✅ API хостинга доступен")
        else:
            print(f"❌ API недоступен: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к хостингу: {e}")
        return False

def main():
    """Основная функция"""
    print("🌐 Экспорт данных на PythonAnywhere")
    print("=" * 50)
    
    # Проверяем статус хостинга
    if not check_hosting_status():
        print("❌ Хостинг недоступен. Проверьте подключение к интернету.")
        return
    
    print("\n" + "=" * 50)
    
    # Экспортируем трассы
    routes_exported, routes_failed = export_routes_to_hosting()
    
    # Экспортируем админ пользователей
    admins_exported, admins_failed = export_admin_users_to_hosting()
    
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Трассы: {routes_exported} экспортировано, {routes_failed} ошибок")
    print(f"Админы: {admins_exported} экспортировано, {admins_failed} ошибок")
    
    if routes_failed == 0 and admins_failed == 0:
        print("🎉 Все данные успешно экспортированы на хостинг!")
    else:
        print("⚠️  Некоторые данные не удалось экспортировать")

if __name__ == '__main__':
    main()
