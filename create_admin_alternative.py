#!/usr/bin/env python3
"""
Альтернативный способ создания админ пользователя на хостинге
"""

import requests
import json

def create_admin_alternative():
    """Альтернативный способ создания админа"""
    print("👤 Пытаемся создать админа альтернативным способом...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Попробуем разные endpoints
    endpoints_to_try = [
        "/api/admin/create/",
        "/api/create-admin/",
        "/api/admin/",
        "/admin/create/",
        "/create-admin/"
    ]
    
    admin_data = {
        'username': 'admin',
        'password': 'admin123',
        'full_name': 'Администратор'
    }
    
    for endpoint in endpoints_to_try:
        try:
            print(f"🔍 Пробуем endpoint: {endpoint}")
            
            response = requests.post(
                f"{hosting_url}{endpoint}",
                json=admin_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"   Статус: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"✅ Успех! Админ создан через {endpoint}")
                return True
            elif response.status_code == 404:
                print(f"   ❌ Endpoint не найден")
            else:
                print(f"   ⚠️  Неожиданный статус: {response.status_code}")
                print(f"   Ответ: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return False

def test_direct_login():
    """Прямое тестирование входа"""
    print("\n🔐 Тестируем прямой вход...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    try:
        session = requests.Session()
        
        # Получаем страницу входа
        login_page = session.get(f"{hosting_url}/api/login/")
        print(f"📄 Страница входа: {login_page.status_code}")
        
        if login_page.status_code == 200:
            # Пробуем войти
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            login_response = session.post(
                f"{hosting_url}/api/login/",
                data=login_data,
                allow_redirects=False
            )
            
            print(f"📡 Результат входа: {login_response.status_code}")
            
            if login_response.status_code == 302:
                print("✅ Вход успешен!")
                return True
            else:
                print(f"❌ Ошибка входа: {login_response.status_code}")
                print(f"📄 Ответ: {login_response.text[:200]}")
                return False
        else:
            print(f"❌ Страница входа недоступна: {login_page.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

def check_existing_admins():
    """Проверяем существующих админов"""
    print("\n🔍 Проверяем существующих админов...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Попробуем разные способы проверки
    endpoints_to_check = [
        "/api/admins/",
        "/api/admin-users/",
        "/api/users/",
        "/admin/users/"
    ]
    
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"{hosting_url}{endpoint}", timeout=10)
            print(f"📡 {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Endpoint работает!")
                print(f"   📄 Ответ: {response.text[:200]}")
                return True
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return False

def main():
    """Основная функция"""
    print("🌐 Альтернативное создание админа на хостинге")
    print("=" * 60)
    
    # Проверяем существующих админов
    check_existing_admins()
    
    # Пробуем создать админа
    admin_created = create_admin_alternative()
    
    if not admin_created:
        print("\n⚠️  Не удалось создать админа через API")
        print("💡 Возможные решения:")
        print("   1. Обновить код на хостинге")
        print("   2. Создать админа через Django shell на хостинге")
        print("   3. Использовать существующего админа")
    
    # Тестируем вход
    login_success = test_direct_login()
    
    if login_success:
        print("\n🎉 Вход в админ панель работает!")
        print("🔗 Ссылки:")
        print(f"   Админ панель: https://koterik.pythonanywhere.com/api/login/")
        print(f"   Логин: admin")
        print(f"   Пароль: admin123")
    else:
        print("\n❌ Вход в админ панель не работает")
        print("💡 Нужно создать админ пользователя на хостинге")

if __name__ == '__main__':
    main()
