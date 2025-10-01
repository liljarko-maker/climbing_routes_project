#!/usr/bin/env python3
"""
Скрипт для создания админ пользователя на хостинге PythonAnywhere
"""

import requests
import json

def create_admin_on_hosting():
    """Создание админ пользователя на хостинге"""
    print("👤 Создаем админ пользователя на хостинге...")
    
    # URL хостинга
    hosting_url = "https://koterik.pythonanywhere.com"
    
    # Данные для создания админа
    admin_data = {
        'username': 'admin',
        'password': 'admin123',
        'full_name': 'Администратор'
    }
    
    try:
        # Отправляем POST запрос на хостинг
        response = requests.post(
            f"{hosting_url}/api/admin/create/",
            json=admin_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📡 Статус ответа: {response.status_code}")
        print(f"📄 Ответ сервера: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Админ пользователь успешно создан на хостинге!")
            return True
        else:
            print(f"❌ Ошибка создания админа: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании админа: {e}")
        return False

def test_admin_login():
    """Тестирование входа админа на хостинге"""
    print("\n🔐 Тестируем вход админа на хостинге...")
    
    hosting_url = "https://koterik.pythonanywhere.com"
    
    try:
        # Получаем CSRF токен
        session = requests.Session()
        login_page = session.get(f"{hosting_url}/api/login/")
        
        if login_page.status_code == 200:
            print("✅ Страница входа доступна")
            
            # Данные для входа
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            # Отправляем POST запрос для входа
            login_response = session.post(
                f"{hosting_url}/api/login/",
                data=login_data,
                allow_redirects=False
            )
            
            print(f"📡 Статус входа: {login_response.status_code}")
            
            if login_response.status_code == 302:
                print("✅ Вход успешен! Перенаправление на админ панель")
                return True
            else:
                print(f"❌ Ошибка входа: {login_response.status_code}")
                print(f"📄 Ответ: {login_response.text}")
                return False
        else:
            print(f"❌ Страница входа недоступна: {login_page.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании входа: {e}")
        return False

def main():
    """Основная функция"""
    print("🌐 Создание админ пользователя на PythonAnywhere")
    print("=" * 50)
    
    # Создаем админа
    admin_created = create_admin_on_hosting()
    
    if admin_created:
        # Тестируем вход
        login_success = test_admin_login()
        
        if login_success:
            print("\n🎉 Админ пользователь создан и протестирован успешно!")
            print("🔗 Ссылки для доступа:")
            print(f"   Главная страница: https://koterik.pythonanywhere.com/")
            print(f"   Админ панель: https://koterik.pythonanywhere.com/api/login/")
            print(f"   Логин: admin")
            print(f"   Пароль: admin123")
        else:
            print("\n⚠️  Админ создан, но вход не работает")
    else:
        print("\n❌ Не удалось создать админ пользователя")

if __name__ == '__main__':
    main()