# 📊 Настройка Google Sheets как дополнительной БД

## 🎯 Обзор

Добавлена интеграция с Google Sheets для синхронизации данных трасс. Теперь можно экспортировать данные из Django в Google таблицы и импортировать обратно.

## 🔧 Что добавлено

### 1. **Google Sheets API интеграция**
- Модуль `routes/google_sheets.py` для работы с API
- Класс `GoogleSheetsManager` для базовых операций
- Класс `RoutesGoogleSheetsSync` для синхронизации трасс

### 2. **Новые API endpoints**
- `POST /api/google-sheets/export/` - Экспорт всех трасс в Google Sheets
- `POST /api/google-sheets/import/` - Импорт трасс из Google Sheets
- `GET /api/google-sheets/status/` - Проверка статуса подключения

### 3. **Настройки Django**
- `GOOGLE_SHEETS_ID` - ID вашей Google таблицы
- `GOOGLE_CREDENTIALS_PATH` - Путь к файлу учетных данных

## 📋 Пошаговая настройка

### Шаг 1: Создание Google Cloud проекта

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google Sheets API:
   - Перейдите в "APIs & Services" > "Library"
   - Найдите "Google Sheets API" и включите его

### Шаг 2: Создание учетных данных

1. В Google Cloud Console перейдите в "APIs & Services" > "Credentials"
2. Нажмите "Create Credentials" > "Service Account"
3. Заполните данные:
   - **Name**: `climbing-routes-service`
   - **Description**: `Service account for climbing routes project`
4. Создайте ключ:
   - Выберите созданный service account
   - Перейдите в "Keys" > "Add Key" > "Create new key"
   - Выберите "JSON" формат
   - Скачайте файл и переименуйте в `credentials.json`

### Шаг 3: Настройка Google Sheets

1. Создайте новую Google таблицу
2. Скопируйте ID таблицы из URL (между `/d/` и `/edit`)
3. Поделитесь таблицей с service account:
   - Нажмите "Share" в Google Sheets
   - Добавьте email service account (из credentials.json)
   - Дайте права "Editor"

### Шаг 4: Настройка Django проекта

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Поместите файл credentials.json в корень проекта:**
   ```
   climbing_routes_project/
   ├── credentials.json  # ← Поместите сюда
   ├── manage.py
   └── ...
   ```

3. **Обновите настройки в `settings.py`:**
   ```python
   # Замените на ваши значения
   GOOGLE_SHEETS_ID = 'your-actual-sheets-id-here'
   GOOGLE_CREDENTIALS_PATH = 'credentials.json'
   ```

### Шаг 5: Тестирование

1. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

2. **Проверьте статус подключения:**
   ```bash
   curl http://127.0.0.1:8000/api/google-sheets/status/
   ```

3. **Экспортируйте данные:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/google-sheets/export/
   ```

## 🚀 Использование

### Экспорт в Google Sheets
```bash
curl -X POST http://127.0.0.1:8000/api/google-sheets/export/
```

**Ответ:**
```json
{
    "message": "Успешно экспортировано 10 трасс в Google Sheets",
    "exported_count": 10
}
```

### Импорт из Google Sheets
```bash
curl -X POST http://127.0.0.1:8000/api/google-sheets/import/
```

**Ответ:**
```json
{
    "message": "Импортировано 5 трасс из Google Sheets",
    "imported_count": 5,
    "errors": []
}
```

### Проверка статуса
```bash
curl http://127.0.0.1:8000/api/google-sheets/status/
```

**Ответ:**
```json
{
    "status": "connected",
    "message": "Google Sheets подключен успешно"
}
```

## 📊 Структура Google Sheets

Таблица будет содержать следующие колонки:

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ID | Номер трассы | Дорожка | Название | Сложность | Цвет | Автор | Дата накрутки | Дата скрутки | Описание | Статус | Дата создания |

## 🔒 Безопасность

### Важные моменты:
1. **НЕ коммитьте** файл `credentials.json` в Git
2. Добавьте в `.gitignore`:
   ```
   credentials.json
   *.json
   ```
3. Используйте переменные окружения для продакшена:
   ```python
   GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
   GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')
   ```

## 🎨 Веб-интерфейс

Можно добавить кнопки в главную страницу:

```html
<!-- Добавить в templates/home.html -->
<div class="row mb-3">
    <div class="col-12">
        <h4>Google Sheets</h4>
        <button class="btn btn-success" onclick="exportToSheets()">
            <i class="fas fa-upload"></i> Экспорт в Google Sheets
        </button>
        <button class="btn btn-info" onclick="importFromSheets()">
            <i class="fas fa-download"></i> Импорт из Google Sheets
        </button>
        <button class="btn btn-secondary" onclick="checkSheetsStatus()">
            <i class="fas fa-check"></i> Проверить статус
        </button>
    </div>
</div>
```

## 🐛 Устранение неполадок

### Ошибка: "Google Sheets API не инициализирован"
- Проверьте путь к файлу `credentials.json`
- Убедитесь, что файл существует и доступен для чтения

### Ошибка: "Permission denied"
- Проверьте, что service account имеет доступ к таблице
- Убедитесь, что таблица существует и ID правильный

### Ошибка: "API not enabled"
- Включите Google Sheets API в Google Cloud Console
- Подождите несколько минут после включения

## 📈 Возможности расширения

1. **Автоматическая синхронизация** - по расписанию
2. **Двусторонняя синхронизация** - изменения в Google Sheets обновляют Django
3. **Фильтрация данных** - экспорт только определенных трасс
4. **Уведомления** - при успешной/неуспешной синхронизации
5. **Логирование** - детальные логи операций

## ✅ Готово!

После настройки у вас будет:
- ✅ Полная интеграция с Google Sheets
- ✅ API для экспорта/импорта данных
- ✅ Автоматическая синхронизация структуры
- ✅ Обработка ошибок и логирование
- ✅ Готовность к расширению функциональности

**Google Sheets теперь работает как дополнительная БД!** 📊
