#!/usr/bin/env python3
"""
Скрипт для обновления всех значений сложности на строчные буквы
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'climbing_routes_project.settings')
django.setup()

from routes.models import Route

def update_difficulty_to_lowercase():
    """Обновляем все значения сложности на строчные буквы"""
    print("🔄 Обновление значений сложности на строчные буквы...")
    
    # Маппинг заглавных букв на строчные
    mapping = {
        '6A': '6a',
        '6A+': '6a+',
        '6B': '6b',
        '6B+': '6b+',
        '6C': '6c',
        '6C+': '6c+',
        '7A': '7a',
        '7A+': '7a+',
        '7B': '7b',
        '7B+': '7b+',
        '7C': '7c',
        '7C+': '7c+',
        '8A': '8a',
        '8A+': '8a+',
        '8B': '8b',
        '8B+': '8b+',
        '8C': '8c',
        '9A': '9a'
    }
    
    updated_count = 0
    
    for old_value, new_value in mapping.items():
        routes = Route.objects.filter(difficulty=old_value)
        count = routes.count()
        
        if count > 0:
            print(f"📝 Обновляем {count} трасс с '{old_value}' на '{new_value}'")
            routes.update(difficulty=new_value)
            updated_count += count
    
    print(f"✅ Обновлено {updated_count} трасс")
    
    # Проверяем результат
    print("\n🔍 Проверяем результат...")
    values = set(Route.objects.values_list('difficulty', flat=True))
    print("Текущие значения сложности:")
    print(sorted(values))
    
    # Проверяем, остались ли заглавные буквы
    uppercase_values = [v for v in values if any(c.isupper() for c in v)]
    if uppercase_values:
        print(f"⚠️ Остались заглавные буквы: {uppercase_values}")
    else:
        print("✅ Все значения сложности теперь в строчных буквах!")

if __name__ == "__main__":
    update_difficulty_to_lowercase()
