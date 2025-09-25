// Админ-панель - JavaScript функции

let currentRouteId = null;
let routesData = [];

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Загружаем данные трасс из таблицы
    loadRoutesData();
    
    // Устанавливаем текущую дату в поле даты накрутки
    const today = new Date();
    const dateString = today.toLocaleDateString('ru-RU');
    document.getElementById('setupDate').value = dateString;
});

// Загрузка данных трасс из таблицы
function loadRoutesData() {
    const table = document.getElementById('routes-table');
    const rows = table.querySelectorAll('tbody tr[data-route-id]');
    
    routesData = [];
    rows.forEach(row => {
        const routeData = {
            id: row.dataset.routeId,
            status: row.dataset.status,
            difficulty: row.dataset.difficulty,
            name: row.cells[2].textContent.trim(),
            author: row.cells[5].textContent.trim(),
            color: row.cells[4].textContent.trim(),
            setupDate: row.cells[6].textContent.trim(),
            isActive: row.cells[7].textContent.includes('Активна')
        };
        routesData.push(routeData);
    });
}

// Показать модальное окно для добавления трассы
function showAddRouteModal() {
    currentRouteId = null;
    document.getElementById('routeModalTitle').textContent = 'Добавить трассу';
    document.getElementById('routeForm').reset();
    
    // Устанавливаем текущую дату
    const today = new Date();
    const dateString = today.toLocaleDateString('ru-RU');
    document.getElementById('setupDate').value = dateString;
    
    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('routeModal'));
    modal.show();
}

// Редактировать трассу
function editRoute(routeId) {
    currentRouteId = routeId;
    document.getElementById('routeModalTitle').textContent = 'Редактировать трассу';
    
    // Находим данные трассы
    const routeData = routesData.find(route => route.id == routeId);
    if (!routeData) {
        alert('Трасса не найдена');
        return;
    }
    
    // Заполняем форму данными трассы
    document.getElementById('trackNumber').value = routeId;
    document.getElementById('routeName').value = routeData.name;
    document.getElementById('difficulty').value = getDifficultyFromRow(routeId);
    document.getElementById('color').value = routeData.color;
    document.getElementById('author').value = routeData.author;
    document.getElementById('setupDate').value = routeData.setupDate;
    document.getElementById('isActive').checked = routeData.isActive;
    
    // Получаем номер дорожки из таблицы
    const row = document.querySelector(`tr[data-route-id="${routeId}"]`);
    if (row) {
        const laneText = row.cells[1].textContent.trim();
        const laneNumber = laneText.replace(/\D/g, '');
        document.getElementById('trackLane').value = laneNumber;
    }
    
    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('routeModal'));
    modal.show();
}

// Получить сложность из строки таблицы
function getDifficultyFromRow(routeId) {
    const row = document.querySelector(`tr[data-route-id="${routeId}"]`);
    if (row) {
        const difficultyCell = row.cells[3];
        const badge = difficultyCell.querySelector('.badge');
        if (badge) {
            return badge.textContent.trim().replace(/[^\w\-\+]/g, '');
        }
    }
    return '';
}

// Сохранить трассу
function saveRoute() {
    const form = document.getElementById('routeForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const routeData = {
        track_number: parseInt(document.getElementById('trackNumber').value),
        track_lane: parseInt(document.getElementById('trackLane').value),
        name: document.getElementById('routeName').value,
        difficulty: document.getElementById('difficulty').value,
        color: document.getElementById('color').value,
        author: document.getElementById('author').value,
        setup_date: document.getElementById('setupDate').value,
        description: document.getElementById('description').value,
        is_active: document.getElementById('isActive').checked
    };
    
    // Валидация даты
    if (!isValidDate(routeData.setup_date)) {
        alert('Неверный формат даты. Используйте формат DD.MM.YYYY');
        return;
    }
    
    // Определяем URL и метод
    let url, method;
    if (currentRouteId) {
        // Редактирование существующей трассы
        url = `/api/routes/${currentRouteId}/`;
        method = 'PUT';
    } else {
        // Создание новой трассы
        url = '/api/routes/';
        method = 'POST';
    }
    
    // Отправляем запрос
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(routeData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Ошибка при сохранении трассы');
        }
    })
    .then(data => {
        alert('Трасса успешно сохранена!');
        location.reload(); // Перезагружаем страницу для обновления данных
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении трассы: ' + error.message);
    });
}

// Удалить трассу
function deleteRoute(routeId) {
    currentRouteId = routeId;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

// Подтвердить удаление
function confirmDelete() {
    if (!currentRouteId) return;
    
    fetch(`/api/routes/${currentRouteId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Трасса успешно удалена!');
            location.reload(); // Перезагружаем страницу для обновления данных
        } else {
            throw new Error('Ошибка при удалении трассы');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении трассы: ' + error.message);
    });
}

// Переключить статус трассы
function toggleRouteStatus(routeId, isActive) {
    const routeData = routesData.find(route => route.id == routeId);
    if (!routeData) {
        alert('Трасса не найдена');
        return;
    }
    
    const statusText = isActive ? 'активировать' : 'скрутить';
    if (!confirm(`Вы уверены, что хотите ${statusText} эту трассу?`)) {
        return;
    }
    
    // Обновляем статус
    routeData.isActive = isActive;
    
    // Отправляем запрос на обновление
    fetch(`/api/routes/${routeId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ is_active: isActive })
    })
    .then(response => {
        if (response.ok) {
            alert(`Трасса успешно ${isActive ? 'активирована' : 'скручена'}!`);
            location.reload(); // Перезагружаем страницу для обновления данных
        } else {
            throw new Error('Ошибка при обновлении статуса трассы');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при обновлении статуса трассы: ' + error.message);
    });
}

// Фильтрация трасс
function filterRoutes() {
    const statusFilter = document.getElementById('statusFilter').value;
    const difficultyFilter = document.getElementById('difficultyFilter').value;
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    
    const rows = document.querySelectorAll('#routes-table tbody tr[data-route-id]');
    
    rows.forEach(row => {
        let show = true;
        
        // Фильтр по статусу
        if (statusFilter !== 'all') {
            const rowStatus = row.dataset.status;
            if (statusFilter === 'active' && rowStatus !== 'active') show = false;
            if (statusFilter === 'inactive' && rowStatus !== 'inactive') show = false;
        }
        
        // Фильтр по сложности
        if (difficultyFilter !== 'all') {
            const rowDifficulty = row.dataset.difficulty;
            if (rowDifficulty !== difficultyFilter) show = false;
        }
        
        // Фильтр по поиску
        if (searchInput) {
            const routeName = row.cells[2].textContent.toLowerCase();
            if (!routeName.includes(searchInput)) show = false;
        }
        
        // Показываем/скрываем строку
        row.style.display = show ? '' : 'none';
    });
}

// Валидация даты
function isValidDate(dateString) {
    const regex = /^(\d{2})\.(\d{2})\.(\d{4})$/;
    const match = dateString.match(regex);
    
    if (!match) return false;
    
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const year = parseInt(match[3], 10);
    
    if (day < 1 || day > 31) return false;
    if (month < 1 || month > 12) return false;
    if (year < 2020 || year > 2030) return false;
    
    return true;
}

// Получить CSRF токен
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
