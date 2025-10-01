#!/usr/bin/env python3
"""
Тестовый скрипт для проверки входа в админ панель
"""
import os
import sys
import django
import requests
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import AdminUser

def test_admin_login():
    """Тестируем вход в админ панель"""
    print("🔍 Тестирование входа в админ панель...")
    
    # Проверяем админ пользователей
    admin_users = AdminUser.objects.all()
    print(f"📊 Найдено админ пользователей: {admin_users.count()}")
    
    for admin in admin_users:
        print(f"👤 Пользователь: {admin.username}")
        print(f"   Полное имя: {admin.full_name}")
        print(f"   Активен: {admin.is_active}")
        print(f"   Последний вход: {admin.last_login}")
        
        # Тестируем пароль
        test_password = "admin123"
        if admin.check_password(test_password):
            print(f"   ✅ Пароль '{test_password}' корректен")
        else:
            print(f"   ❌ Пароль '{test_password}' неверный")
    
    # Тестируем HTTP запросы
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Проверяем страницу входа
        response = requests.get(f"{base_url}/api/login/")
        print(f"\n🌐 Страница входа: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Страница входа доступна")
        else:
            print("❌ Страница входа недоступна")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке страницы входа: {e}")
    
    try:
        # Проверяем админ панель (должна перенаправлять на логин)
        response = requests.get(f"{base_url}/api/admin/")
        print(f"\n🔐 Админ панель: {response.status_code}")
        
        if response.status_code in [200, 302]:
            print("✅ Админ панель доступна")
        else:
            print("❌ Админ панель недоступна")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке админ панели: {e}")

if __name__ == "__main__":
    test_admin_login()
