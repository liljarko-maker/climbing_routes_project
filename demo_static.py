#!/usr/bin/env python3
"""
Статическая демонстрация API трасс скалодрома
Показывает, как будет работать API без запуска сервера
"""

import json
from datetime import datetime

def print_section(title):
    """Красивый вывод заголовка"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_json(data, title="JSON Response"):
    """Красивый вывод JSON"""
    print(f"\n{title}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def demo_api_structure():
    """Демонстрация структуры API"""
    print_section("🏗️ СТРУКТУРА API ТРАСС СКАЛОДРОМА")
    
    print("""
📋 ОСНОВНЫЕ ENDPOINTS:

🔹 CRUD операции:
   GET    /api/routes/              - Список всех трасс
   POST   /api/routes/              - Создание новой трассы
   GET    /api/routes/{id}/         - Получение конкретной трассы
   PUT    /api/routes/{id}/         - Полное обновление трассы
   PATCH  /api/routes/{id}/         - Частичное обновление трассы
   DELETE /api/routes/{id}/         - Удаление трассы

🔹 Массовые операции:
   POST   /api/routes/bulk/         - Массовое создание трасс
   DELETE /api/routes/bulk/         - Массовое удаление трасс
   POST   /api/routes/bulk-update/  - Массовое обновление трасс

🔹 Поиск и фильтрация:
   GET    /api/routes/search/       - Расширенный поиск
   GET    /api/routes/authors/      - Список авторов с статистикой
   GET    /api/routes/colors/       - Список цветов с статистикой
   POST   /api/routes/{id}/toggle-active/ - Переключение статуса

🔹 Дополнительные:
   GET    /api/difficulty-levels/   - Уровни сложности
   GET    /api/stats/               - Общая статистика
    """)

def demo_data_structures():
    """Демонстрация структур данных"""
    print_section("📊 СТРУКТУРЫ ДАННЫХ")
    
    # Пример трассы
    sample_route = {
        "id": 1,
        "name": "Красная линия",
        "difficulty": "medium",
        "difficulty_display": "Средняя",
        "author": "Иван Петров",
        "color": "красный",
        "created_at": "2024-01-01T12:00:00Z",
        "description": "Интересная трасса с техничными движениями",
        "is_active": True
    }
    
    print_json(sample_route, "Пример трассы")
    
    # Уровни сложности
    difficulty_levels = [
        {"value": "easy", "label": "Легкая"},
        {"value": "medium", "label": "Средняя"},
        {"value": "hard", "label": "Сложная"},
        {"value": "expert", "label": "Экспертная"}
    ]
    
    print_json(difficulty_levels, "Уровни сложности")
    
    # Статистика
    stats = {
        "total_routes": 15,
        "active_routes": 12,
        "inactive_routes": 3,
        "difficulty_distribution": {
            "easy": {"label": "Легкая", "count": 5},
            "medium": {"label": "Средняя", "count": 6},
            "hard": {"label": "Сложная", "count": 3},
            "expert": {"label": "Экспертная", "count": 1}
        },
        "color_distribution": {
            "красный": 4,
            "синий": 3,
            "зеленый": 2,
            "черный": 2,
            "желтый": 2,
            "фиолетовый": 2
        }
    }
    
    print_json(stats, "Пример статистики")

def demo_api_examples():
    """Демонстрация примеров использования API"""
    print_section("🔧 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ API")
    
    print("""
📝 СОЗДАНИЕ ТРАССЫ:
curl -X POST http://127.0.0.1:8000/api/routes/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Новая трасса",
    "difficulty": "medium",
    "author": "Автор",
    "color": "красный",
    "description": "Описание трассы"
  }'

📋 ПОЛУЧЕНИЕ СПИСКА ТРАСС:
curl http://127.0.0.1:8000/api/routes/

🔍 ПОИСК ПО СЛОЖНОСТИ:
curl "http://127.0.0.1:8000/api/routes/search/?difficulty=medium"

🔍 ПОИСК ПО АВТОРУ:
curl "http://127.0.0.1:8000/api/routes/search/?author=Иван"

🔍 КОМБИНИРОВАННЫЙ ПОИСК:
curl "http://127.0.0.1:8000/api/routes/search/?difficulty=easy&is_active=true&ordering=name"

📦 МАССОВОЕ СОЗДАНИЕ:
curl -X POST http://127.0.0.1:8000/api/routes/bulk/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "routes": [
      {
        "name": "Трасса 1",
        "difficulty": "easy",
        "author": "Автор 1",
        "color": "зеленый"
      },
      {
        "name": "Трасса 2",
        "difficulty": "hard",
        "author": "Автор 2",
        "color": "синий"
      }
    ]
  }'

📊 ПОЛУЧЕНИЕ СТАТИСТИКИ:
curl http://127.0.0.1:8000/api/stats/

👥 СПИСОК АВТОРОВ:
curl http://127.0.0.1:8000/api/routes/authors/

🎨 СПИСОК ЦВЕТОВ:
curl http://127.0.0.1:8000/api/routes/colors/

⚡ ПЕРЕКЛЮЧЕНИЕ СТАТУСА:
curl -X POST http://127.0.0.1:8000/api/routes/1/toggle-active/
    """)

def demo_features():
    """Демонстрация возможностей"""
    print_section("✨ ВОЗМОЖНОСТИ ПРОЕКТА")
    
    features = [
        "✅ Полный CRUD функционал для трасс",
        "✅ Массовые операции (создание/удаление/обновление)",
        "✅ Расширенный поиск с множественными критериями",
        "✅ Фильтрация по сложности, автору, цвету, дате",
        "✅ Сортировка по любому полю",
        "✅ Пагинация результатов",
        "✅ Статистика по всем параметрам",
        "✅ Логирование всех операций",
        "✅ Валидация данных",
        "✅ Обработка ошибок",
        "✅ Админ-панель Django",
        "✅ REST API с JSON ответами",
        "✅ Тестовые скрипты",
        "✅ Docker поддержка"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print(f"\n📁 СТРУКТУРА ПРОЕКТА:")
    print(f"  climbing_routes_project/")
    print(f"  ├── climbing_routes_project/  # Настройки Django")
    print(f"  ├── routes/                   # Приложение трасс")
    print(f"  │   ├── models.py            # Модели данных")
    print(f"  │   ├── views.py             # API представления")
    print(f"  │   ├── serializers.py       # Сериализаторы")
    print(f"  │   ├── urls.py              # URL маршруты")
    print(f"  │   └── admin.py             # Админ-панель")
    print(f"  ├── manage.py                # Управление Django")
    print(f"  ├── requirements.txt         # Зависимости")
    print(f"  ├── Dockerfile               # Docker образ")
    print(f"  ├── docker-compose.yml       # Docker Compose")
    print(f"  ├── test_api.py              # Тесты API")
    print(f"  ├── demo.py                  # Демонстрация")
    print(f"  └── README.md                # Документация")

def demo_installation():
    """Демонстрация установки"""
    print_section("🚀 УСТАНОВКА И ЗАПУСК")
    
    print("""
📋 СПОСОБЫ УСТАНОВКИ:

1️⃣ ЧЕРЕЗ DOCKER (Рекомендуется):
   docker-compose up --build
   # или
   ./start.sh

2️⃣ ЛОКАЛЬНАЯ УСТАНОВКА:
   # Установка зависимостей
   pip3 install -r requirements.txt
   
   # Применение миграций
   python3 manage.py migrate
   
   # Загрузка тестовых данных
   python3 manage.py load_sample_data
   
   # Запуск сервера
   python3 manage.py runserver

3️⃣ ЧЕРЕЗ HOMEBREW:
   brew install python
   pip3 install -r requirements.txt
   python3 manage.py migrate
   python3 manage.py runserver

🔧 ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ:
   python3 manage.py createsuperuser  # Создание админа
   python3 demo.py                    # Быстрая демонстрация
   python3 test_api.py                # Полное тестирование
    """)

def main():
    """Основная функция демонстрации"""
    print("🎯 СТАТИЧЕСКАЯ ДЕМОНСТРАЦИЯ API ТРАСС СКАЛОДРОМА")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    demo_api_structure()
    demo_data_structures()
    demo_api_examples()
    demo_features()
    demo_installation()
    
    print_section("🎉 ЗАКЛЮЧЕНИЕ")
    print("""
Проект полностью готов к использованию! 

📚 Документация:
   - README.md - основная документация
   - SETUP.md - инструкции по установке
   - test_api.py - примеры тестирования

🌐 После запуска сервера:
   - API: http://127.0.0.1:8000/api/
   - Админ: http://127.0.0.1:8000/admin/
   - Список трасс: http://127.0.0.1:8000/api/routes/

🔧 Для запуска выберите один из способов:
   1. Docker: ./start.sh
   2. Локально: pip3 install -r requirements.txt && python3 manage.py runserver
   3. Homebrew: brew install python && pip3 install -r requirements.txt
    """)

if __name__ == "__main__":
    main()
