// Основные функции для работы с API
class APIManager {
    constructor() {
        this.baseURL = '/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Обработчик формы создания трассы
        const form = document.getElementById('create-route-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleCreateRoute(e));
        }

        // Плавная прокрутка для навигации
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    async loadInitialData() {
        // Загружаем статистику при загрузке страницы
        try {
            await this.testAPI('GET', '/api/stats/');
        } catch (error) {
            console.log('Не удалось загрузить статистику:', error);
        }
    }

    async testAPI(method, endpoint, data = null) {
        const resultDiv = document.getElementById('api-result');
        if (!resultDiv) return;

        // Показываем индикатор загрузки
        resultDiv.innerHTML = '<div class="loading"></div> Загрузка...';

        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(this.baseURL + endpoint, options);
            const result = await response.json();

            // Форматируем результат
            const formattedResult = this.formatAPIResult(method, endpoint, response.status, result);
            resultDiv.innerHTML = formattedResult;

            // Добавляем анимацию
            resultDiv.classList.add('fade-in');

        } catch (error) {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Ошибка:</strong> ${error.message}
                </div>
            `;
        }
    }

    formatAPIResult(method, endpoint, status, data) {
        const statusClass = status >= 200 && status < 300 ? 'success' : 'danger';
        const statusText = status >= 200 && status < 300 ? 'Успешно' : 'Ошибка';
        
        return `
            <div class="alert alert-${statusClass}">
                <strong>${method} ${endpoint}</strong> - ${statusText} (${status})
            </div>
            <pre class="mb-0">${JSON.stringify(data, null, 2)}</pre>
        `;
    }

    async handleCreateRoute(event) {
        event.preventDefault();
        
        const formData = {
            route_number: parseInt(document.getElementById('route-number').value),
            track_number: parseInt(document.getElementById('track-number').value),
            name: document.getElementById('route-name').value,
            difficulty: document.getElementById('route-difficulty').value,
            color: document.getElementById('route-color').value,
            author: document.getElementById('route-author').value,
            setup_date: document.getElementById('setup-date').value,
            description: document.getElementById('route-description').value
        };

        // Добавляем дату скрутки если указана
        const takedownDate = document.getElementById('takedown-date').value;
        if (takedownDate) {
            formData.takedown_date = takedownDate;
        }

        // Валидация
        if (!formData.route_number || !formData.track_number || !formData.name || 
            !formData.difficulty || !formData.color || !formData.author || !formData.setup_date) {
            this.showAlert('Пожалуйста, заполните все обязательные поля', 'warning');
            return;
        }

        // Валидация номера дорожки
        if (formData.track_number < 1 || formData.track_number > 3) {
            this.showAlert('Номер дорожки должен быть от 1 до 3', 'warning');
            return;
        }

        // Валидация дат
        if (formData.takedown_date && formData.takedown_date < formData.setup_date) {
            this.showAlert('Дата скрутки не может быть раньше даты накрутки', 'warning');
            return;
        }

        try {
            await this.testAPI('POST', '/api/routes/', formData);
            
            // Очищаем форму
            document.getElementById('create-route-form').reset();
            
            // Показываем уведомление об успехе
            this.showAlert('Трасса успешно создана!', 'success');
            
            // Обновляем страницу через 2 секунды
            setTimeout(() => {
                window.location.reload();
            }, 2000);

        } catch (error) {
            this.showAlert('Ошибка при создании трассы: ' + error.message, 'danger');
        }
    }

    showAlert(message, type) {
        // Создаем уведомление
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Автоматически скрываем через 5 секунд
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Метод для тестирования различных endpoints
    async testSearch() {
        const searchParams = new URLSearchParams({
            search: 'тест',
            difficulty: 'easy',
            is_active: 'true'
        });
        
        await this.testAPI('GET', `/api/routes/search/?${searchParams}`);
    }

    async testBulkCreate() {
        const testData = {
            routes: [
                {
                    name: 'Тестовая трасса 1',
                    author: 'Тестовый автор',
                    difficulty: 'easy',
                    color: 'красный',
                    description: 'Описание тестовой трассы 1'
                },
                {
                    name: 'Тестовая трасса 2',
                    author: 'Тестовый автор',
                    difficulty: 'medium',
                    color: 'синий',
                    description: 'Описание тестовой трассы 2'
                }
            ]
        };

        await this.testAPI('POST', '/api/routes/bulk/', testData);
    }
}

// Глобальные функции для кнопок
function testAPI(method, endpoint) {
    if (window.apiManager) {
        window.apiManager.testAPI(method, endpoint);
    }
}

function testSearch() {
    if (window.apiManager) {
        window.apiManager.testSearch();
    }
}

function testBulkCreate() {
    if (window.apiManager) {
        window.apiManager.testBulkCreate();
    }
}

// Google Sheets функции
async function exportToSheets() {
    const resultDiv = document.getElementById('sheets-result');
    const messageSpan = document.getElementById('sheets-message');
    
    if (resultDiv) {
        resultDiv.style.display = 'block';
        messageSpan.textContent = 'Экспорт в Google Sheets...';
    }
    
    try {
        const response = await fetch('/api/google-sheets/export/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            messageSpan.textContent = result.message;
            resultDiv.className = 'mt-3 alert alert-success';
        } else {
            messageSpan.textContent = result.error || 'Ошибка при экспорте';
            resultDiv.className = 'mt-3 alert alert-danger';
        }
    } catch (error) {
        messageSpan.textContent = 'Ошибка подключения: ' + error.message;
        resultDiv.className = 'mt-3 alert alert-danger';
    }
}

async function importFromSheets() {
    const resultDiv = document.getElementById('sheets-result');
    const messageSpan = document.getElementById('sheets-message');
    
    if (resultDiv) {
        resultDiv.style.display = 'block';
        messageSpan.textContent = 'Импорт из Google Sheets...';
    }
    
    try {
        const response = await fetch('/api/google-sheets/import/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            messageSpan.textContent = result.message;
            resultDiv.className = 'mt-3 alert alert-success';
            
            // Обновляем страницу через 2 секунды
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            messageSpan.textContent = result.error || 'Ошибка при импорте';
            resultDiv.className = 'mt-3 alert alert-danger';
        }
    } catch (error) {
        messageSpan.textContent = 'Ошибка подключения: ' + error.message;
        resultDiv.className = 'mt-3 alert alert-danger';
    }
}

async function checkSheetsStatus() {
    const resultDiv = document.getElementById('sheets-result');
    const messageSpan = document.getElementById('sheets-message');
    
    if (resultDiv) {
        resultDiv.style.display = 'block';
        messageSpan.textContent = 'Проверка статуса...';
    }
    
    try {
        const response = await fetch('/api/google-sheets/status/');
        const result = await response.json();
        
        if (response.ok) {
            messageSpan.textContent = result.message;
            resultDiv.className = 'mt-3 alert alert-success';
        } else {
            messageSpan.textContent = result.message || 'Ошибка подключения';
            resultDiv.className = 'mt-3 alert alert-warning';
        }
    } catch (error) {
        messageSpan.textContent = 'Ошибка подключения: ' + error.message;
        resultDiv.className = 'mt-3 alert alert-danger';
    }
}

// Функции для загрузки данных из разных источников
async function loadDjangoData() {
    showLoadingIndicator();
    updateButtonStates('django');
    
    try {
        // Перезагружаем страницу для получения данных из Django
        window.location.reload();
    } catch (error) {
        hideLoadingIndicator();
        showAlert('Ошибка загрузки данных из Django: ' + error.message, 'danger');
    }
}

async function loadSheetsData() {
    showLoadingIndicator();
    updateButtonStates('sheets');
    
    try {
        const response = await fetch('/api/google-sheets/routes/');
        const result = await response.json();
        
        if (response.ok) {
            updateTableWithData(result.routes, 'Google Sheets');
            updateDataSourceInfo('Google Sheets', result.count);
        } else {
            showAlert('Ошибка загрузки данных из Google Sheets: ' + (result.error || 'Неизвестная ошибка'), 'danger');
        }
    } catch (error) {
        showAlert('Ошибка подключения к Google Sheets: ' + error.message, 'danger');
    } finally {
        hideLoadingIndicator();
    }
}

function showLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    const tableContainer = document.getElementById('routes-table-container');
    
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
    if (tableContainer) {
        tableContainer.style.display = 'none';
    }
}

function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    const tableContainer = document.getElementById('routes-table-container');
    
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
    if (tableContainer) {
        tableContainer.style.display = 'block';
    }
}

function updateButtonStates(activeSource) {
    const djangoBtn = document.getElementById('django-data-btn');
    const sheetsBtn = document.getElementById('sheets-data-btn');
    
    if (djangoBtn && sheetsBtn) {
        if (activeSource === 'django') {
            djangoBtn.className = 'btn btn-primary';
            sheetsBtn.className = 'btn btn-outline-primary';
        } else if (activeSource === 'sheets') {
            djangoBtn.className = 'btn btn-outline-primary';
            sheetsBtn.className = 'btn btn-primary';
        }
    }
}

function updateDataSourceInfo(source, count) {
    const infoElement = document.getElementById('data-source-info');
    if (infoElement) {
        infoElement.textContent = `Загружены данные из ${source} (${count} трасс)`;
    }
}

function updateTableWithData(routes, source) {
    const tbody = document.getElementById('routes-table-body');
    if (!tbody) return;
    
    // Очищаем таблицу
    tbody.innerHTML = '';
    
    if (routes && routes.length > 0) {
        routes.forEach(route => {
            const row = createTableRow(route);
            tbody.appendChild(row);
        });
    } else {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `
            <td colspan="10" class="text-center text-muted">
                <i class="fas fa-info-circle"></i> Нет трасс в ${source}
            </td>
        `;
        tbody.appendChild(emptyRow);
    }
}

function createTableRow(route) {
    const row = document.createElement('tr');
    
    // Форматируем даты
    const setupDate = route.setup_date ? formatDate(route.setup_date) : '-';
    const takedownDate = route.takedown_date ? formatDate(route.takedown_date) : '<span class="text-muted">-</span>';
    
    // Определяем статус
    const isActive = route.is_active || route.takedown_date === null || route.takedown_date === '';
    const statusBadge = isActive ? 
        '<span class="badge bg-success"><i class="fas fa-check"></i> Активна</span>' :
        '<span class="badge bg-warning"><i class="fas fa-times"></i> Скручена</span>';
    
    // Определяем иконку сложности
    const difficultyIcon = getDifficultyIcon(route.difficulty);
    
    // Обрезаем описание
    const description = route.description ? 
        `<span class="text-truncate" style="max-width: 200px;" title="${route.description}">${route.description.length > 50 ? route.description.substring(0, 50) + '...' : route.description}</span>` :
        '<span class="text-muted">-</span>';
    
    row.innerHTML = `
        <td><strong>№${route.route_number || ''}</strong></td>
        <td><span class="badge bg-info">${route.track_number || ''}</span></td>
        <td><strong>${route.name || ''}</strong></td>
        <td>
            <span class="badge difficulty-${(route.difficulty || 'secondary').toLowerCase()}">
                ${difficultyIcon} ${route.difficulty || ''}
            </span>
        </td>
        <td>
            <span class="badge" style="background-color: ${route.color || '#6c757d'}; color: white;">
                ${route.color || ''}
            </span>
        </td>
        <td>${route.author || ''}</td>
        <td>${setupDate}</td>
        <td>${takedownDate}</td>
        <td>${statusBadge}</td>
        <td>${description}</td>
    `;
    
    return row;
}

function getDifficultyIcon(difficulty) {
    if (!difficulty) return '';
    
    if (difficulty === '4-5') {
        return '<i class="fas fa-seedling"></i>';
    } else if (difficulty === '6A' || difficulty === '6A+') {
        return '<i class="fas fa-leaf"></i>';
    } else if (difficulty === '6B' || difficulty === '6B+' || difficulty === '6C' || difficulty === '6C+') {
        return '<i class="fas fa-fire"></i>';
    } else if (difficulty === '7A' || difficulty === '7A+' || difficulty === '7B' || difficulty === '7B+') {
        return '<i class="fas fa-bolt"></i>';
    } else if (difficulty === '7C' || difficulty === '7C+' || difficulty === '8A' || difficulty === '8A+') {
        return '<i class="fas fa-skull"></i>';
    } else if (difficulty === '8B' || difficulty === '8B+' || difficulty === '8C' || difficulty === '9A') {
        return '<i class="fas fa-dragon"></i>';
    }
    return '';
}

function formatDate(dateString) {
    if (!dateString) return '-';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU');
    } catch (error) {
        return dateString;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    window.apiManager = new APIManager();
    
    // Добавляем дополнительные кнопки тестирования
    addTestButtons();
});

function addTestButtons() {
    const testSection = document.querySelector('#test .card-body .row .col-md-6:first-child');
    if (testSection) {
        const additionalButtons = `
            <button class="btn btn-outline-secondary" onclick="testSearch()">
                <i class="fas fa-search"></i> Тестовый поиск
            </button>
            <button class="btn btn-outline-dark" onclick="testBulkCreate()">
                <i class="fas fa-layer-group"></i> Массовое создание
            </button>
        `;
        
        testSection.innerHTML += additionalButtons;
    }
}

// Утилиты для работы с данными
class DataUtils {
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static formatDifficulty(difficulty) {
        const difficultyMap = {
            'easy': 'Легкая',
            'medium': 'Средняя',
            'hard': 'Сложная',
            'expert': 'Экспертная'
        };
        return difficultyMap[difficulty] || difficulty;
    }

    static getDifficultyIcon(difficulty) {
        const iconMap = {
            'easy': 'fas fa-seedling text-success',
            'medium': 'fas fa-leaf text-warning',
            'hard': 'fas fa-fire text-danger',
            'expert': 'fas fa-skull text-dark'
        };
        return iconMap[difficulty] || 'fas fa-question text-secondary';
    }
}

// Обработка ошибок
window.addEventListener('error', function(e) {
    console.error('JavaScript ошибка:', e.error);
});

// Обработка необработанных промисов
window.addEventListener('unhandledrejection', function(e) {
    console.error('Необработанная ошибка промиса:', e.reason);
});

// Экспорт для использования в других скриптах
window.APIManager = APIManager;
window.DataUtils = DataUtils;
