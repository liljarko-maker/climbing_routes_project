// Фильтрация и поиск трасс

let allRoutes = [];
let filteredRoutes = [];

// Функция для принудительного применения стилей сложности
function applyDifficultyStyles() {
    // Находим все бейджи сложности в основной таблице
    const difficultyBadges = document.querySelectorAll('#routes-table .badge[class*="difficulty-"]');
    
    difficultyBadges.forEach(badge => {
        const className = badge.className;
        
        // Применяем черный цвет для всех уровней
        if (className.includes('difficulty-4') || 
            className.includes('difficulty-5') || 
            className.includes('difficulty-6a') || 
            className.includes('difficulty-6b') || 
            className.includes('difficulty-6c') || 
            className.includes('difficulty-7a') ||
            className.includes('difficulty-7b') || 
            className.includes('difficulty-7c') || 
            className.includes('difficulty-8a') || 
            className.includes('difficulty-8b') || 
            className.includes('difficulty-8c') || 
            className.includes('difficulty-9a')) {
            badge.style.color = '#000000';
            badge.style.setProperty('color', '#000000', 'important');
        }
    });
    
    // Находим все бейджи сложности в таблице результатов фильтрации
    const filteredBadges = document.querySelectorAll('#filtered-results .badge[class*="difficulty-"]');
    
    filteredBadges.forEach(badge => {
        const className = badge.className;
        
        // Применяем черный цвет для всех уровней
        if (className.includes('difficulty-4') || 
            className.includes('difficulty-5') || 
            className.includes('difficulty-6a') || 
            className.includes('difficulty-6b') || 
            className.includes('difficulty-6c') || 
            className.includes('difficulty-7a') ||
            className.includes('difficulty-7b') || 
            className.includes('difficulty-7c') || 
            className.includes('difficulty-8a') || 
            className.includes('difficulty-8b') || 
            className.includes('difficulty-8c') || 
            className.includes('difficulty-9a')) {
            badge.style.color = '#000000';
            badge.style.setProperty('color', '#000000', 'important');
        }
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, начинаем инициализацию фильтрации');
    
    // Проверяем наличие элементов
    const table = document.getElementById('routes-table');
    const difficultyFilter = document.getElementById('difficultyFilter');
    const authorFilter = document.getElementById('authorFilter');
    const colorFilter = document.getElementById('colorFilter');
    
    console.log('Найдены элементы:', {
        table: !!table,
        difficultyFilter: !!difficultyFilter,
        authorFilter: !!authorFilter,
        colorFilter: !!colorFilter
    });
    
    // Собираем все трассы из таблицы
    collectRoutesFromTable();
    console.log('Собрано трасс:', allRoutes.length);
    
    // Принудительно применяем стили для сложности
    applyDifficultyStyles();
    
    // Инициализируем фильтры
    initializeFilters();
    
    console.log('Инициализация фильтрации завершена');
});

// Сбор данных о трассах из таблицы
function collectRoutesFromTable() {
    allRoutes = [];
    const tableRows = document.querySelectorAll('#routes-table tbody tr, #routes-table-body tr');
    console.log('Найдено строк в таблице:', tableRows.length);
    
    tableRows.forEach((row, index) => {
        // Пропускаем строку с сообщением "Нет трасс"
        if (row.textContent.includes('Нет трасс')) {
            return;
        }
        
        // Проверяем, что у строки есть нужные ячейки
        if (row.cells && row.cells.length >= 7) {
            // Извлекаем данные из ячеек, учитывая HTML структуру
            const trackLaneCell = row.cells[0];
            const nameCell = row.cells[1];
            const difficultyCell = row.cells[2];
            const colorCell = row.cells[3];
            const authorCell = row.cells[4];
            const setupDateCell = row.cells[5];
            const descriptionCell = row.cells[6];
            
            // Извлекаем чистые значения, убирая HTML теги и лишние символы
            const trackLane = trackLaneCell ? trackLaneCell.textContent.trim() : '';
            const name = nameCell ? nameCell.textContent.trim() : '';
            const difficulty = difficultyCell ? difficultyCell.textContent.trim().replace(/\s+/g, ' ').trim() : '';
            const color = colorCell ? colorCell.textContent.trim() : '';
            const author = authorCell ? authorCell.textContent.trim() : '';
            const setupDate = setupDateCell ? setupDateCell.textContent.trim() : '';
            const description = descriptionCell ? descriptionCell.textContent.trim() : '';
            
            const route = {
                id: row.dataset.routeId || `route_${index}`,
                trackLane: trackLane,
                name: name,
                difficulty: difficulty,
                color: color,
                author: author,
                setupDate: setupDate,
                description: description,
                element: row
            };
            
            // Отладочная информация
            console.log('Собранная трасса:', route);
            
            // Добавляем только если есть основные данные
            if (route.name && route.name !== '-') {
                allRoutes.push(route);
            }
        }
    });
    
    filteredRoutes = [...allRoutes];
    console.log(`Загружено ${allRoutes.length} трасс для фильтрации`);
}

// Инициализация фильтров
function initializeFilters() {
    // Заполняем выпадающие списки авторов и цветов
    populateAuthorFilter();
    populateColorFilter();
    
    // Показываем все трассы по умолчанию
    showAllRoutes();
}

// Заполнение фильтра авторов
function populateAuthorFilter() {
    const authorFilter = document.getElementById('authorFilter');
    const authors = [...new Set(allRoutes.map(route => route.author))].sort();
    
    // Очищаем существующие опции (кроме первой)
    while (authorFilter.children.length > 1) {
        authorFilter.removeChild(authorFilter.lastChild);
    }
    
    // Добавляем авторов
    authors.forEach(author => {
        const option = document.createElement('option');
        option.value = author;
        option.textContent = author;
        authorFilter.appendChild(option);
    });
}

// Заполнение фильтра цветов
function populateColorFilter() {
    const colorFilter = document.getElementById('colorFilter');
    const colors = [...new Set(allRoutes.map(route => route.color))].sort();
    
    // Очищаем существующие опции (кроме первой)
    while (colorFilter.children.length > 1) {
        colorFilter.removeChild(colorFilter.lastChild);
    }
    
    // Добавляем цвета
    colors.forEach(color => {
        const option = document.createElement('option');
        option.value = color;
        option.textContent = color;
        colorFilter.appendChild(option);
    });
}

// Основная функция фильтрации
function filterRoutes() {
    console.log('Функция filterRoutes вызвана');
    
    const difficulty = document.getElementById('difficultyFilter').value;
    const lane = document.getElementById('laneFilter').value;
    const author = document.getElementById('authorFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    const color = document.getElementById('colorFilter').value;
    
    console.log('Фильтры:', { difficulty, lane, author, dateFilter, searchText, color });
    console.log('Всего трасс для фильтрации:', allRoutes.length);
    
    // Отладочная информация для первых нескольких трасс
    if (allRoutes.length > 0) {
        console.log('Примеры данных трасс:');
        allRoutes.slice(0, 3).forEach((route, index) => {
            console.log(`Трасса ${index + 1}:`, {
                trackLane: route.trackLane,
                name: route.name,
                difficulty: route.difficulty,
                author: route.author,
                color: route.color
            });
        });
    }
    
    filteredRoutes = allRoutes.filter(route => {
        // Фильтр по сложности (извлекаем чистую сложность из текста с иконками)
        if (difficulty) {
            const cleanDifficulty = route.difficulty.replace(/[^\w\s+-]/g, '').trim();
            if (!cleanDifficulty.includes(difficulty)) {
                return false;
            }
        }
        
        // Фильтр по дорожке
        if (lane && route.trackLane !== lane) {
            return false;
        }
        
        // Фильтр по автору
        if (author && route.author !== author) {
            return false;
        }
        
        // Фильтр по цвету
        if (color && route.color !== color) {
            return false;
        }
        
        // Фильтр по дате
        if (dateFilter && !matchesDateFilter(route.setupDate, dateFilter)) {
            return false;
        }
        
        // Поиск по названию
        if (searchText && !route.name.toLowerCase().includes(searchText)) {
            return false;
        }
        
        return true;
    });
    
    console.log('Отфильтровано трасс:', filteredRoutes.length);
    
    // Обновляем отображение
    updateTableDisplay();
    updateFilterResults();
    
    // Принудительно применяем стили для сложности
    setTimeout(applyDifficultyStyles, 100);
}

// Проверка соответствия даты фильтру
function matchesDateFilter(setupDate, filterType) {
    if (!setupDate) return false;
    
    const today = new Date();
    const routeDate = parseDate(setupDate);
    
    if (!routeDate) return false;
    
    const diffTime = today - routeDate;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    switch (filterType) {
        case 'today':
            return diffDays === 0;
        case 'week':
            return diffDays <= 7;
        case 'month':
            return diffDays <= 30;
        case '3months':
            return diffDays <= 90;
        case '6months':
            return diffDays <= 180;
        case 'year':
            return diffDays <= 365;
        default:
            return true;
    }
}

// Парсинг даты в формате DD.MM.YYYY
function parseDate(dateString) {
    const parts = dateString.split('.');
    if (parts.length !== 3) return null;
    
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1; // Месяцы в JS начинаются с 0
    const year = parseInt(parts[2], 10);
    
    return new Date(year, month, day);
}

// Обновление отображения таблицы
function updateTableDisplay() {
    const filteredResultsDiv = document.getElementById('filtered-results');
    const filteredContainer = document.getElementById('filtered-routes-container');
    const originalTable = document.getElementById('routes');
    
    // Проверяем, применены ли фильтры
    const hasActiveFilters = document.getElementById('difficultyFilter').value || 
                            document.getElementById('laneFilter').value || 
                            document.getElementById('authorFilter').value || 
                            document.getElementById('dateFilter').value || 
                            document.getElementById('searchInput').value || 
                            document.getElementById('colorFilter').value;
    
    if (!hasActiveFilters) {
        // Если фильтры не применены, показываем оригинальную таблицу
        if (filteredResultsDiv) filteredResultsDiv.style.display = 'none';
        if (originalTable) originalTable.style.display = 'block';
        
        // Показываем все трассы в оригинальной таблице
        allRoutes.forEach(route => {
            route.element.style.display = '';
        });
    } else {
        // Если фильтры применены, показываем результаты фильтрации
        if (originalTable) originalTable.style.display = 'none';
        if (filteredResultsDiv) filteredResultsDiv.style.display = 'block';
        
        // Создаем HTML для отфильтрованных трасс (включая случай пустых результатов)
        createFilteredResultsHTML(filteredContainer);
    }
}

// Создание HTML для отфильтрованных результатов
function createFilteredResultsHTML(container) {
    if (!container) return;
    
    // Проверяем, есть ли результаты
    if (filteredRoutes.length === 0) {
        // Получаем информацию о примененных фильтрах
        const activeFilters = [];
        const difficulty = document.getElementById('difficultyFilter').value;
        const lane = document.getElementById('laneFilter').value;
        const author = document.getElementById('authorFilter').value;
        const dateFilter = document.getElementById('dateFilter').value;
        const searchText = document.getElementById('searchInput').value;
        const color = document.getElementById('colorFilter').value;
        
        if (difficulty) activeFilters.push(`Сложность: ${difficulty}`);
        if (lane) activeFilters.push(`Дорожка: ${lane}`);
        if (author) activeFilters.push(`Автор: ${author}`);
        if (dateFilter) activeFilters.push(`Дата: ${dateFilter}`);
        if (searchText) activeFilters.push(`Поиск: "${searchText}"`);
        if (color) activeFilters.push(`Цвет: ${color}`);
        
        const filtersText = activeFilters.length > 0 ? 
            `<p class="mb-2"><strong>Примененные фильтры:</strong><br><small class="text-muted">${activeFilters.join(', ')}</small></p>` : '';
        
        container.innerHTML = `
            <div class="alert alert-info text-center" role="alert">
                <i class="fas fa-info-circle me-2"></i>
                <strong>Нет трасс с такими фильтрами</strong>
                ${filtersText}
                <p class="mb-0 mt-2">Попробуйте изменить критерии поиска или очистить фильтры</p>
                <button class="btn btn-outline-primary btn-sm mt-3" onclick="clearAllFilters()">
                    <i class="fas fa-times me-1"></i> Очистить все фильтры
                </button>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Дорожка</th>
                        <th>Название</th>
                        <th>Сложность</th>
                        <th>Цвет</th>
                        <th>Автор</th>
                        <th>Дата накрутки</th>
                        <th>Описание</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    filteredRoutes.forEach(route => {
        html += `
            <tr>
                <td><span class="badge bg-info">${route.trackLane}</span></td>
                <td><strong>${route.name}</strong></td>
                <td><span class="badge difficulty-${route.difficulty}">${route.difficulty}</span></td>
                <td><span class="badge color-cell color-${route.color.toLowerCase()}" style="background-color: ${route.color.toLowerCase()};">${route.color}</span></td>
                <td>${route.author}</td>
                <td>${route.setupDate}</td>
                <td>${route.description || '<span class="text-muted">Нет описания</span>'}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// Обновление информации о результатах фильтрации
function updateFilterResults() {
    const resultsElement = document.getElementById('filterResults');
    const totalCount = allRoutes.length;
    const filteredCount = filteredRoutes.length;
    
    if (filteredCount === totalCount) {
        resultsElement.textContent = `Показано ${totalCount} из ${totalCount} трасс`;
    } else {
        resultsElement.textContent = `Показано ${filteredCount} из ${totalCount} трасс`;
    }
}

// Показать все трассы
function showAllRoutes() {
    filteredRoutes = [...allRoutes];
    updateTableDisplay();
    updateFilterResults();
}

// Очистка всех фильтров
function clearFilters() {
    document.getElementById('difficultyFilter').value = '';
    document.getElementById('laneFilter').value = '';
    document.getElementById('authorFilter').value = '';
    document.getElementById('dateFilter').value = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('colorFilter').value = '';
    
    // Сбрасываем фильтрацию
    filteredRoutes = [...allRoutes];
    updateTableDisplay();
    updateFilterResults();
}

// Алиас для кнопки "Очистить все фильтры"
function clearAllFilters() {
    clearFilters();
}


// Функция для обновления данных (вызывается при изменении данных на странице)
function refreshRoutesData() {
    collectRoutesFromTable();
    initializeFilters();
}
