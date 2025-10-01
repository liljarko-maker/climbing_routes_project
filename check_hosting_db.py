#!/usr/bin/env python3
"""
Скрипт для проверки базы данных на хостинге
"""
import requests
import json

def check_hosting_database():
    """Проверяем базу данных на хостинге через API"""
    print("🗄️ Проверка базы данных на хостинге...")
    
    base_url = "http://koterik.pythonanywhere.com"
    
    try:
        # Проверяем статистику трасс
        print("📊 Проверяем статистику трасс...")
        stats_response = requests.get(f"{base_url}/api/stats/")
        
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"✅ Статистика получена: {stats_data}")
        else:
            print(f"❌ Ошибка получения статистики: {stats_response.status_code}")
        
        # Проверяем список трасс
        print("\n🏔️ Проверяем список трасс...")
        routes_response = requests.get(f"{base_url}/api/routes/")
        
        if routes_response.status_code == 200:
            routes_data = routes_response.json()
            print(f"✅ Трассы получены: {len(routes_data)} трасс")
            
            # Проверяем первые несколько трасс
            for i, route in enumerate(routes_data[:3]):
                print(f"   Трасса {i+1}: {route.get('name', 'Без названия')} (ID: {route.get('id')})")
        else:
            print(f"❌ Ошибка получения трасс: {routes_response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")

if __name__ == "__main__":
    check_hosting_database()
