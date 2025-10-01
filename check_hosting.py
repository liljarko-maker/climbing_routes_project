#!/usr/bin/env python3
"""
Скрипт для проверки доступности сайта на хостинге
"""
import requests
import time

def check_hosting():
    """Проверяем доступность сайта на хостинге"""
    print("🌐 Проверка доступности сайта на хостинге...")
    
    # Возможные домены
    domains = [
        "http://koterik.pythonanywhere.com",
        "http://liljarko-maker.pythonanywhere.com",
        "https://koterik.pythonanywhere.com",
        "https://liljarko-maker.pythonanywhere.com"
    ]
    
    for domain in domains:
        try:
            print(f"\n🔍 Проверяем: {domain}")
            
            # Проверяем главную страницу
            response = requests.get(f"{domain}/", timeout=10)
            print(f"   Главная страница: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Главная страница доступна")
                
                # Проверяем страницу входа
                login_response = requests.get(f"{domain}/api/login/", timeout=10)
                print(f"   Страница входа: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("   ✅ Страница входа доступна")
                else:
                    print("   ❌ Страница входа недоступна")
                
                # Проверяем админ панель
                admin_response = requests.get(f"{domain}/api/admin/", timeout=10)
                print(f"   Админ панель: {admin_response.status_code}")
                
                if admin_response.status_code in [200, 302]:
                    print("   ✅ Админ панель доступна")
                else:
                    print("   ❌ Админ панель недоступна")
                    
            else:
                print(f"   ❌ Главная страница недоступна: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Таймаут при подключении к {domain}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Ошибка подключения к {domain}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        time.sleep(1)  # Пауза между запросами

if __name__ == "__main__":
    check_hosting()
