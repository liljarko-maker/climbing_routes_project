#!/usr/bin/env python3
"""
Скрипт для загрузки данных на хостинг
"""
import os
import sys
import django
import requests
import json

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import Route, AdminUser

def upload_data_to_hosting():
    """Загружаем данные на хостинг"""
    print("🚀 Загрузка данных на хостинг...")
    
    base_url = "http://koterik.pythonanywhere.com"
    
    # Получаем данные из локальной базы
    routes = Route.objects.all()
    admin_users = AdminUser.objects.all()
    
    print(f"📊 Локальная база данных:")
    print(f"   Трасс: {routes.count()}")
    print(f"   Админ пользователей: {admin_users.count()}")
    
    if routes.count() == 0:
        print("❌ В локальной базе нет трасс для загрузки")
        return
    
    if admin_users.count() == 0:
        print("❌ В локальной базе нет админ пользователей для загрузки")
        return
    
    # Создаем сессию
    session = requests.Session()
    
    try:
        # Получаем CSRF токен
        login_page = session.get(f"{base_url}/api/login/")
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value
                break
        
        if not csrf_token:
            print("❌ Не удалось получить CSRF токен")
            return
        
        print(f"🔑 CSRF токен получен: {csrf_token[:20]}...")
        
        # Подготавливаем данные для загрузки
        routes_data = []
        for route in routes:
            route_data = {
                'track_lane': route.track_lane,
                'name': route.name,
                'difficulty': route.difficulty,
                'color': route.color,
                'author': route.author,
                'setup_date': str(route.setup_date) if route.setup_date else '',
                'description': route.description or '',
                'is_active': route.is_active
            }
            routes_data.append(route_data)
        
        print(f"📦 Подготовлено {len(routes_data)} трасс для загрузки")
        
        # Загружаем трассы по частям (по 10 штук)
        batch_size = 10
        uploaded_count = 0
        
        for i in range(0, len(routes_data), batch_size):
            batch = routes_data[i:i + batch_size]
            
            print(f"📤 Загружаем трассы {i+1}-{min(i+batch_size, len(routes_data))}...")
            
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            }
            
            response = session.post(
                f"{base_url}/api/routes/bulk/",
                json={'routes': batch},
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                uploaded_count += len(batch)
                print(f"✅ Загружено {len(batch)} трасс")
            else:
                print(f"❌ Ошибка загрузки: {response.status_code}")
                print(f"   Ответ: {response.text}")
        
        print(f"\n📊 Итого загружено: {uploaded_count} трасс")
        
        # Проверяем результат
        print("\n🔍 Проверяем результат...")
        check_response = requests.get(f"{base_url}/api/stats/")
        
        if check_response.status_code == 200:
            stats = check_response.json()
            print(f"✅ Статистика на хостинге: {stats['total_routes']} трасс")
        else:
            print(f"❌ Ошибка проверки: {check_response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")

if __name__ == "__main__":
    upload_data_to_hosting()
