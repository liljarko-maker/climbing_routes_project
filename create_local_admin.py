#!/usr/bin/env python3
"""
Создание админ пользователя в локальной базе
"""

import os
import django
import requests

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import AdminUser

def create_local_admin():
    """Создание админ пользователя в локальной базе"""
    print("👤 Создаем админ пользователя в локальной базе...")
    
    # Проверяем, существует ли уже админ
    if AdminUser.objects.filter(username='admin').exists():
        print("✅ Админ пользователь уже существует")
        admin = AdminUser.objects.get(username='admin')
        print(f"   ID: {admin.id}")
        print(f"   Имя: {admin.full_name}")
        print(f"   Активен: {admin.is_active}")
        return admin
    
    # Создаем нового админа
    admin = AdminUser.objects.create(
        username='admin',
        full_name='Администратор',
        is_active=True
    )
    admin.set_password('admin123')
    admin.save()
    
    print("✅ Админ пользователь создан успешно!")
    print(f"   ID: {admin.id}")
    print(f"   Логин: {admin.username}")
    print(f"   Пароль: admin123")
    print(f"   Имя: {admin.full_name}")
    
    return admin

def export_admin_to_hosting():
    """Экспорт админа на хостинг через API"""
    print("\n🌐 Экспортируем админа на хостинг...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Получаем админа из локальной базы
    try:
        admin = AdminUser.objects.get(username='admin')
    except AdminUser.DoesNotExist:
        print("❌ Админ пользователь не найден в локальной базе")
        return False
    
    # Подготавливаем данные для экспорта
    admin_data = {
        'username': admin.username,
        'password': 'admin123',  # Используем стандартный пароль
        'full_name': admin.full_name
    }
    
    # Пробуем разные endpoints
    endpoints = [
        "/api/admin/create/",
        "/api/create-admin/",
        "/admin/create/"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"🔍 Пробуем {endpoint}")
            
            response = requests.post(
                f"{hosting_url}{endpoint}",
                json=admin_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"   Статус: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"✅ Админ экспортирован через {endpoint}")
                return True
            elif response.status_code == 404:
                print(f"   ❌ Endpoint не найден")
            else:
                print(f"   ⚠️  Статус: {response.status_code}")
                print(f"   Ответ: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return False

def main():
    """Основная функция"""
    print("🔧 Создание и экспорт админ пользователя")
    print("=" * 50)
    
    # Создаем админа локально
    admin = create_local_admin()
    
    # Пробуем экспортировать на хостинг
    export_success = export_admin_to_hosting()
    
    if export_success:
        print("\n🎉 Админ пользователь создан и экспортирован!")
    else:
        print("\n⚠️  Админ создан локально, но не удалось экспортировать")
        print("💡 Для входа на хостинге нужно:")
        print("   1. Зайти в консоль PythonAnywhere")
        print("   2. Выполнить команды создания админа")
        print("   3. Или обновить код на хостинге")

if __name__ == '__main__':
    main()
