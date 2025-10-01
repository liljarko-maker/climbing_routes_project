#!/usr/bin/env python3
"""
Скрипт для тестирования входа в админ панель на хостинге
"""
import requests
import time

def test_hosting_login():
    """Тестируем вход в админ панель на хостинге"""
    print("🔐 Тестирование входа в админ панель на хостинге...")
    
    base_url = "http://koterik.pythonanywhere.com"
    
    # Создаем сессию для сохранения cookies
    session = requests.Session()
    
    try:
        # Получаем страницу входа
        print("📄 Получаем страницу входа...")
        login_page = session.get(f"{base_url}/api/login/")
        
        if login_page.status_code != 200:
            print(f"❌ Ошибка получения страницы входа: {login_page.status_code}")
            return
        
        print("✅ Страница входа получена")
        
        # Извлекаем CSRF токен
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value
                break
        
        if not csrf_token:
            print("❌ CSRF токен не найден")
            return
        
        print(f"🔑 CSRF токен: {csrf_token[:20]}...")
        
        # Данные для входа
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'csrfmiddlewaretoken': csrf_token
        }
        
        # Заголовки
        headers = {
            'Referer': f"{base_url}/api/login/",
            'X-CSRFToken': csrf_token
        }
        
        # Отправляем POST запрос на вход
        print("🚀 Отправляем данные для входа...")
        login_response = session.post(
            f"{base_url}/api/login/",
            data=login_data,
            headers=headers,
            allow_redirects=False
        )
        
        print(f"📊 Ответ сервера: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print("✅ Успешный вход! Перенаправление получено")
            
            # Проверяем админ панель
            print("🔍 Проверяем доступ к админ панели...")
            admin_response = session.get(f"{base_url}/api/admin/")
            
            if admin_response.status_code == 200:
                print("✅ Админ панель доступна!")
                
                # Проверяем, есть ли данные администратора в ответе
                if 'admin_username' in admin_response.text or 'admin' in admin_response.text:
                    print("✅ Данные администратора найдены в ответе")
                else:
                    print("⚠️ Данные администратора не найдены в ответе")
                    
            else:
                print(f"❌ Админ панель недоступна: {admin_response.status_code}")
                
        elif login_response.status_code == 200:
            print("❌ Вход не удался - остались на странице входа")
            
            # Проверяем, есть ли сообщение об ошибке
            if 'error' in login_response.text.lower() or 'неверный' in login_response.text.lower():
                print("❌ Обнаружено сообщение об ошибке входа")
            else:
                print("⚠️ Неясная причина неудачного входа")
                
        else:
            print(f"❌ Неожиданный ответ сервера: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    test_hosting_login()
