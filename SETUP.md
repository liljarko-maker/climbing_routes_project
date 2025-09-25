# Инструкции по установке и запуску

## Проблема с инструментами разработки

На вашей системе не установлены инструменты разработки Xcode, которые необходимы для компиляции Python пакетов.

## Решения

### Вариант 1: Установка Xcode Command Line Tools (Рекомендуется)

```bash
# Установка инструментов разработки
xcode-select --install
```

После установки перезапустите терминал и выполните:

```bash
# Установка зависимостей
pip3 install -r requirements.txt

# Применение миграций
python3 manage.py migrate

# Создание суперпользователя (опционально)
python3 manage.py createsuperuser

# Загрузка тестовых данных
python3 manage.py load_sample_data

# Запуск сервера
python3 manage.py runserver
```

### Вариант 2: Использование Homebrew

```bash
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка Python через Homebrew
brew install python

# Установка зависимостей
pip3 install -r requirements.txt

# Запуск проекта
python3 manage.py migrate
python3 manage.py runserver
```

### Вариант 3: Использование Docker

Создайте файл `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Запуск:

```bash
# Сборка образа
docker build -t climbing-routes .

# Запуск контейнера
docker run -p 8000:8000 climbing-routes
```

## Проверка установки

После установки зависимостей проверьте:

```bash
# Проверка Django
python3 -c "import django; print('Django version:', django.get_version())"

# Проверка DRF
python3 -c "import rest_framework; print('DRF version:', rest_framework.VERSION)"
```

## Запуск проекта

```bash
# 1. Применение миграций
python3 manage.py migrate

# 2. Создание суперпользователя (опционально)
python3 manage.py createsuperuser

# 3. Загрузка тестовых данных
python3 manage.py load_sample_data

# 4. Запуск сервера
python3 manage.py runserver
```

## Тестирование

После запуска сервера:

```bash
# Быстрая демонстрация
python3 demo.py

# Полное тестирование
python3 test_api.py
```

## Доступные URL

- **API**: http://127.0.0.1:8000/api/
- **Админ-панель**: http://127.0.0.1:8000/admin/
- **Список трасс**: http://127.0.0.1:8000/api/routes/
- **Статистика**: http://127.0.0.1:8000/api/stats/

## Структура API

### Основные endpoints:
- `GET /api/routes/` - список трасс
- `POST /api/routes/` - создание трассы
- `GET /api/routes/{id}/` - получение трассы
- `PUT/PATCH /api/routes/{id}/` - обновление трассы
- `DELETE /api/routes/{id}/` - удаление трассы

### Массовые операции:
- `POST /api/routes/bulk/` - массовое создание
- `DELETE /api/routes/bulk/` - массовое удаление
- `POST /api/routes/bulk-update/` - массовое обновление

### Поиск и фильтрация:
- `GET /api/routes/search/` - расширенный поиск
- `GET /api/routes/authors/` - список авторов
- `GET /api/routes/colors/` - список цветов
- `POST /api/routes/{id}/toggle-active/` - переключение статуса

### Дополнительные:
- `GET /api/difficulty-levels/` - уровни сложности
- `GET /api/stats/` - статистика

## Примеры использования

### Создание трассы:
```bash
curl -X POST http://127.0.0.1:8000/api/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Красная линия",
    "difficulty": "medium",
    "author": "Иван Петров",
    "color": "красный",
    "description": "Интересная трасса"
  }'
```

### Получение списка трасс:
```bash
curl http://127.0.0.1:8000/api/routes/
```

### Поиск по сложности:
```bash
curl "http://127.0.0.1:8000/api/routes/search/?difficulty=medium"
```

## Логирование

Все операции логируются в файл `climbing_routes.log` в корне проекта.

## Устранение проблем

### Ошибка "command not found: python3"
Установите Python через Homebrew или используйте системный Python.

### Ошибка "No module named 'django'"
Установите зависимости: `pip3 install -r requirements.txt`

### Ошибка "xcode-select"
Установите инструменты разработки: `xcode-select --install`

### Ошибка миграций
Выполните: `python3 manage.py migrate`

### Порт занят
Используйте другой порт: `python3 manage.py runserver 8001`
