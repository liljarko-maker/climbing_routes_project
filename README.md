# Система учета трасс на скалодроме

Django REST API для управления трассами на скалодроме с возможностью отслеживания сложности, автора, цвета и даты создания.

## Возможности

- ✅ CRUD операции с трассами
- ✅ Уровни сложности (Легкая, Средняя, Сложная, Экспертная)
- ✅ Фильтрация по различным параметрам
- ✅ Поиск по названию
- ✅ Статистика по трассам
- ✅ Админ-панель для управления
- ✅ REST API с JSON ответами

## Установка и запуск

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
# На macOS/Linux:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя (опционально)
python manage.py createsuperuser
```

### 3. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## API Endpoints

### Основные операции с трассами

- `GET /api/routes/` - Получить список всех трасс
- `POST /api/routes/` - Создать новую трассу
- `GET /api/routes/{id}/` - Получить конкретную трассу
- `PUT /api/routes/{id}/` - Обновить трассу
- `PATCH /api/routes/{id}/` - Частично обновить трассу
- `DELETE /api/routes/{id}/` - Удалить трассу

### Массовые операции

- `POST /api/routes/bulk/` - Массовое создание трасс
- `DELETE /api/routes/bulk/` - Массовое удаление трасс
- `POST /api/routes/bulk-update/` - Массовое обновление трасс

### Поиск и фильтрация

- `GET /api/routes/search/` - Расширенный поиск с множественными критериями
- `GET /api/routes/authors/` - Получить список всех авторов с статистикой
- `GET /api/routes/colors/` - Получить список всех цветов с статистикой
- `POST /api/routes/{id}/toggle-active/` - Переключить статус активности трассы

### Дополнительные endpoints

- `GET /api/difficulty-levels/` - Получить доступные уровни сложности
- `GET /api/stats/` - Получить статистику по трассам

### Параметры фильтрации для GET /api/routes/

- `difficulty` - Фильтр по уровню сложности (easy, medium, hard, expert)
- `author` - Фильтр по автору (частичное совпадение)
- `color` - Фильтр по цвету (частичное совпадение)
- `is_active` - Фильтр по активности (true/false)
- `search` - Поиск по названию трассы

### Примеры запросов

```bash
# Получить все трассы
curl http://127.0.0.1:8000/api/routes/

# Получить только сложные трассы
curl http://127.0.0.1:8000/api/routes/?difficulty=hard

# Поиск трасс по автору
curl http://127.0.0.1:8000/api/routes/?author=Иван

# Получить статистику
curl http://127.0.0.1:8000/api/stats/

# Создать новую трассу
curl -X POST http://127.0.0.1:8000/api/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Красная линия",
    "difficulty": "medium",
    "author": "Иван Петров",
    "color": "красный",
    "description": "Интересная трасса с техничными движениями"
  }'

# Массовое создание трасс
curl -X POST http://127.0.0.1:8000/api/routes/bulk/ \
  -H "Content-Type: application/json" \
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

# Расширенный поиск
curl "http://127.0.0.1:8000/api/routes/search/?difficulty=medium&is_active=true&ordering=name&page=1&page_size=10"

# Получить список авторов
curl http://127.0.0.1:8000/api/routes/authors/

# Переключить статус активности
curl -X POST http://127.0.0.1:8000/api/routes/1/toggle-active/
```

## Структура данных трассы

```json
{
  "id": 1,
  "name": "Красная линия",
  "difficulty": "medium",
  "difficulty_display": "Средняя",
  "author": "Иван Петров",
  "color": "красный",
  "created_at": "2024-01-01T12:00:00Z",
  "description": "Интересная трасса с техничными движениями",
  "is_active": true
}
```

## Уровни сложности

- `easy` - Легкая
- `medium` - Средняя
- `hard` - Сложная
- `expert` - Экспертная

## Админ-панель

Доступна по адресу: http://127.0.0.1:8000/admin/

Для входа используйте учетные данные суперпользователя, созданного командой `createsuperuser`.

## Структура проекта

```
climbing_routes_project/
├── climbing_routes_project/     # Основные настройки Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── routes/                      # Приложение для работы с трассами
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Тестирование

### Быстрая демонстрация

```bash
# Запуск демонстрации
python demo.py
```

### Полное тестирование API

```bash
# Запуск всех тестов
python test_api.py
```

### Ручное тестирование

1. Запустите сервер: `python manage.py runserver`
2. Откройте браузер: http://127.0.0.1:8000/api/routes/
3. Используйте админ-панель: http://127.0.0.1:8000/admin/

## Разработка

Для разработки рекомендуется:

1. Использовать виртуальное окружение
2. Создать файл `.env` для переменных окружения
3. Настроить логирование (уже настроено)
4. Добавить тесты (есть тестовые скрипты)
5. Настроить CORS для фронтенда

## Лицензия

MIT License
