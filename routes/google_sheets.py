"""
Модуль для работы с Google Sheets API
"""

import os
import json
from typing import List, Dict, Any
from django.conf import settings
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsManager:
    """Менеджер для работы с Google Sheets"""
    
    def __init__(self):
        self.service = None
        self.spreadsheet_id = getattr(settings, 'GOOGLE_SHEETS_ID', None)
        self.credentials_path = getattr(settings, 'GOOGLE_CREDENTIALS_PATH', None)
        self._initialize_service()
    
    def _initialize_service(self):
        """Инициализация Google Sheets API"""
        try:
            if not self.credentials_path or not os.path.exists(self.credentials_path):
                logger.error("Путь к файлу учетных данных Google не найден")
                return
            
            # Области доступа для Google Sheets
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Загрузка учетных данных
            credentials = Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=scopes
            )
            
            # Создание сервиса
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets API успешно инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации Google Sheets API: {e}")
            self.service = None
    
    def read_sheet(self, range_name: str = 'A1:Z1000') -> List[List[Any]]:
        """Чтение данных из Google Sheets"""
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets API не инициализирован")
            return []
        
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Прочитано {len(values)} строк из Google Sheets")
            return values
            
        except Exception as e:
            logger.error(f"Ошибка чтения Google Sheets: {e}")
            return []
    
    def write_sheet(self, range_name: str, values: List[List[Any]]) -> bool:
        """Запись данных в Google Sheets"""
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets API не инициализирован")
            return False
        
        try:
            sheet = self.service.spreadsheets()
            body = {'values': values}
            
            result = sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Записано {result.get('updatedCells')} ячеек в Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка записи в Google Sheets: {e}")
            return False
    
    def append_to_sheet(self, range_name: str, values: List[List[Any]]) -> bool:
        """Добавление данных в конец листа"""
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets API не инициализирован")
            return False
        
        try:
            sheet = self.service.spreadsheets()
            body = {'values': values}
            
            result = sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Добавлено {result.get('updates', {}).get('updatedRows', 0)} строк в Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка добавления в Google Sheets: {e}")
            return False
    
    def clear_sheet(self, range_name: str) -> bool:
        """Очистка листа"""
        if not self.service or not self.spreadsheet_id:
            logger.error("Google Sheets API не инициализирован")
            return False
        
        try:
            sheet = self.service.spreadsheets()
            sheet.values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            logger.info(f"Лист {range_name} очищен")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка очистки Google Sheets: {e}")
            return False


class RoutesGoogleSheetsSync:
    """Синхронизация трасс с Google Sheets"""
    
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.sheet_name = 'Трудность'  # Используем существующий лист "Трудность"
    
    def export_routes_to_sheets(self, routes_data: List[Dict]) -> bool:
        """Экспорт трасс в Google Sheets"""
        try:
            # Подготовка заголовков
            headers = [
                'ID', 'Номер трассы', 'Дорожка', 'Название', 'Сложность', 
                'Цвет', 'Автор', 'Дата накрутки', 'Дата скрутки', 
                'Описание', 'Статус', 'Дата создания'
            ]
            
            # Подготовка данных
            rows = [headers]
            for route in routes_data:
                row = [
                    route.get('id', ''),
                    route.get('route_number', ''),
                    route.get('track_number', ''),
                    route.get('name', ''),
                    route.get('difficulty_display', ''),
                    route.get('color', ''),
                    route.get('author', ''),
                    route.get('setup_date', ''),
                    route.get('takedown_date', '') or '',
                    route.get('description', '') or '',
                    'Активна' if route.get('is_active') else 'Скручена',
                    route.get('created_at', '')
                ]
                rows.append(row)
            
            # Очистка и запись данных
            range_name = f'{self.sheet_name}!A1:Z1000'
            self.sheets_manager.clear_sheet(range_name)
            
            return self.sheets_manager.write_sheet(f'{self.sheet_name}!A1', rows)
            
        except Exception as e:
            logger.error(f"Ошибка экспорта в Google Sheets: {e}")
            return False
    
    def import_routes_from_sheets(self) -> List[Dict]:
        """Импорт трасс из Google Sheets (лист Трудность)"""
        try:
            range_name = f'{self.sheet_name}!A2:Z1000'  # Пропускаем заголовки
            rows = self.sheets_manager.read_sheet(range_name)
            
            routes = []
            route_number = 1  # Счетчик для нумерации трасс
            
            for row in rows:
                if len(row) >= 6:  # Минимальное количество колонок для листа Трудность
                    # Пропускаем пустые строки
                    if not any(row[:6]):
                        continue
                    
                    # Маппинг колонок листа Трудность:
                    # 0: № Дорожки, 1: Автор трассы, 2: Название, 3: Дата накрутки, 4: Цвет зацеп, 5: Категория, 6: Снимаем
                    
                    # Безопасное извлечение данных
                    track_number = None
                    try:
                        if row[0] and row[0].strip() and row[0].strip().isdigit():
                            track_number = int(row[0].strip())
                    except (ValueError, IndexError):
                        pass
                    
                    author = row[1].strip() if len(row) > 1 and row[1] else ''
                    name = row[2].strip() if len(row) > 2 and row[2] else f'Трасса {route_number}'
                    setup_date = row[3].strip() if len(row) > 3 and row[3] else ''
                    color = row[4].strip() if len(row) > 4 and row[4] else ''
                    difficulty = row[5].strip() if len(row) > 5 and row[5] else ''
                    is_takedown = row[6].strip() if len(row) > 6 and row[6] else ''
                    
                    # Пропускаем строки с заголовками или служебной информацией
                    if any(keyword in str(row).lower() for keyword in ['категории', 'дорожки', 'автор', 'название', 'дата']):
                        continue
                    
                    # Пропускаем строки без автора или с пустыми ключевыми полями
                    if not author or not difficulty:
                        continue
                    
                    # Создаем объект трассы
                    route = {
                        'route_number': route_number,
                        'track_number': track_number,
                        'name': name,
                        'difficulty': difficulty,
                        'color': color,
                        'author': author,
                        'setup_date': setup_date,
                        'takedown_date': None,  # В листе Трудность нет поля даты скрутки
                        'description': f'Импортировано из Google Sheets (лист {self.sheet_name})',
                        'is_active': not bool(is_takedown and is_takedown.strip()),  # Если поле "Снимаем" заполнено, то трасса неактивна
                    }
                    routes.append(route)
                    route_number += 1
            
            logger.info(f"Импортировано {len(routes)} трасс из Google Sheets (лист {self.sheet_name})")
            return routes
            
        except Exception as e:
            logger.error(f"Ошибка импорта из Google Sheets: {e}")
            return []
