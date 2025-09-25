# 📊 Анализ хранения данных в системе

## 🔍 **Куда добавляются новые трассы из админ-панели?**

### ✅ **Ответ: В SQLite базу данных (НЕ в Google Sheets)**

## 🗄️ **Структура хранения данных:**

### **1. Основная база данных:**
- **Тип**: SQLite3
- **Файл**: `db.sqlite3`
- **Модель**: `Route` в `routes/models.py`
- **API**: Django REST Framework endpoints

### **2. Google Sheets:**
- **Роль**: Дополнительный источник данных для отображения
- **Синхронизация**: Только для чтения на главной странице
- **Обновление**: Через кнопки "Экспорт/Импорт" в Google Sheets

## 🔄 **Поток данных:**

### **Админ-панель → SQLite:**
```
Админ-панель (JavaScript) 
    ↓ POST /api/routes/
Django API (RouteViewSet.create)
    ↓ serializer.save()
SQLite Database (Route model)
```

### **Главная страница ← Google Sheets:**
```
Google Sheets API
    ↓ import_routes_from_sheets()
Django View (home_view)
    ↓ render template
Главная страница (отображение)
```

## 📋 **Детали реализации:**

### **API Endpoints для админ-панели:**
- **Создание**: `POST /api/routes/`
- **Редактирование**: `PUT /api/routes/{id}/`
- **Удаление**: `DELETE /api/routes/{id}/`
- **Обновление статуса**: `PATCH /api/routes/{id}/`

### **Модель Route в SQLite:**
```python
class Route(models.Model):
    route_number = models.PositiveIntegerField(unique=True)
    track_number = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=5)
    color = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    setup_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    takedown_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
```

### **Google Sheets интеграция:**
- **Чтение**: `RoutesGoogleSheetsSync.import_routes_from_sheets()`
- **Запись**: `RoutesGoogleSheetsSync.export_routes_to_sheets()`
- **Лист**: "Трудность" (sheet_name = 'Трудность')

## ⚠️ **Важные моменты:**

### **1. Разделение данных:**
- **Админ-панель** работает с **SQLite**
- **Главная страница** показывает данные из **Google Sheets**
- **Нет автоматической синхронизации** между ними

### **2. Потенциальные проблемы:**
- **Дублирование данных**: трассы могут существовать в обеих системах
- **Несинхронизированность**: изменения в админке не отражаются на главной
- **Разные источники**: админка и главная страница показывают разные данные

### **3. Рекомендации:**
- **Синхронизация**: добавить автоматическую синхронизацию после изменений
- **Единый источник**: выбрать один источник истины (SQLite или Google Sheets)
- **Уведомления**: информировать пользователя о необходимости синхронизации

## 🎯 **Текущее состояние:**

### **✅ Что работает:**
- **Админ-панель**: полный CRUD в SQLite
- **Главная страница**: отображение данных из Google Sheets
- **API**: все endpoints функционируют

### **⚠️ Что нужно учесть:**
- **Данные не синхронизированы** между SQLite и Google Sheets
- **Изменения в админке** не видны на главной странице
- **Нужна синхронизация** для актуальности данных

## 🔧 **Возможные решения:**

### **1. Автоматическая синхронизация:**
```python
# После создания/обновления трассы в админке
def sync_to_google_sheets(route_data):
    sync = RoutesGoogleSheetsSync()
    sync.export_routes_to_sheets([route_data])
```

### **2. Единый источник данных:**
- **Вариант A**: Все данные только в SQLite, Google Sheets для экспорта
- **Вариант B**: Все данные только в Google Sheets, SQLite для кэширования

### **3. Уведомления пользователю:**
- Показывать статус синхронизации
- Кнопки для принудительной синхронизации
- Предупреждения о несинхронизированных данных

## 📝 **Заключение:**

**Новые трассы из админ-панели добавляются в SQLite базу данных, а НЕ в Google Sheets.**

**Для полной функциональности системы рекомендуется добавить синхронизацию между SQLite и Google Sheets.**
