#!/usr/bin/env python3
"""
Скрипт для тестирования адаптивности веб-приложения
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_responsive_design():
    """Тестирование адаптивного дизайна"""
    print("🧪 Тестирование адаптивного дизайна")
    print("=" * 50)
    
    # Настройка Chrome для headless режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Разрешения для тестирования
    resolutions = [
        {"name": "iPhone SE", "width": 375, "height": 667},
        {"name": "iPhone 12", "width": 390, "height": 844},
        {"name": "iPad", "width": 768, "height": 1024},
        {"name": "Desktop", "width": 1920, "height": 1080},
    ]
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        for resolution in resolutions:
            print(f"\n📱 Тестирование {resolution['name']} ({resolution['width']}x{resolution['height']})")
            
            # Устанавливаем разрешение
            driver.set_window_size(resolution['width'], resolution['height'])
            
            # Тестируем главную страницу
            print("  🔍 Загрузка главной страницы...")
            driver.get(f"{base_url}/")
            
            # Ждем загрузки
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Проверяем основные элементы
            try:
                # Навигация
                navbar = driver.find_element(By.CLASS_NAME, "navbar")
                print(f"    ✅ Навигация: {navbar.size['width']}x{navbar.size['height']}")
                
                # Карточки статистики
                cards = driver.find_elements(By.CLASS_NAME, "card")
                print(f"    ✅ Карточки: найдено {len(cards)} карточек")
                
                # Таблица
                table = driver.find_element(By.CLASS_NAME, "table-responsive")
                print(f"    ✅ Таблица: {table.size['width']}x{table.size['height']}")
                
                # Фильтры
                filters = driver.find_element(By.CLASS_NAME, "filter-section")
                print(f"    ✅ Фильтры: {filters.size['width']}x{filters.size['height']}")
                
            except Exception as e:
                print(f"    ❌ Ошибка при проверке элементов: {e}")
            
            # Проверяем CSS медиа-запросы
            css_rules = driver.execute_script("""
                var sheets = document.styleSheets;
                var mediaQueries = [];
                for (var i = 0; i < sheets.length; i++) {
                    try {
                        var rules = sheets[i].cssRules || sheets[i].rules;
                        for (var j = 0; j < rules.length; j++) {
                            if (rules[j].type === CSSRule.MEDIA_RULE) {
                                mediaQueries.push(rules[j].media.mediaText);
                            }
                        }
                    } catch(e) {
                        // Игнорируем ошибки CORS
                    }
                }
                return mediaQueries;
            """)
            
            print(f"    📊 Найдено {len(css_rules)} медиа-запросов")
            
            # Делаем скриншот
            screenshot_name = f"screenshot_{resolution['name'].replace(' ', '_').lower()}.png"
            driver.save_screenshot(screenshot_name)
            print(f"    📸 Скриншот сохранен: {screenshot_name}")
            
            time.sleep(1)
        
        driver.quit()
        print("\n✅ Тестирование завершено успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        print("💡 Убедитесь, что:")
        print("   - Сервер запущен на http://127.0.0.1:8000")
        print("   - Установлен Chrome и ChromeDriver")
        print("   - Установлен selenium: pip install selenium")

def test_css_files():
    """Проверка CSS файлов"""
    print("\n🎨 Проверка CSS файлов")
    print("=" * 30)
    
    base_url = "http://127.0.0.1:8000"
    css_files = [
        "/static/css/style.css",
        "/static/css/mobile.css"
    ]
    
    for css_file in css_files:
        try:
            response = requests.get(f"{base_url}{css_file}")
            if response.status_code == 200:
                size_kb = len(response.content) / 1024
                print(f"✅ {css_file}: {size_kb:.1f} KB")
                
                # Проверяем наличие медиа-запросов
                content = response.text
                media_queries = content.count("@media")
                print(f"   📱 Медиа-запросов: {media_queries}")
                
            else:
                print(f"❌ {css_file}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {css_file}: {e}")

def test_html_templates():
    """Проверка HTML шаблонов"""
    print("\n📄 Проверка HTML шаблонов")
    print("=" * 30)
    
    base_url = "http://127.0.0.1:8000"
    pages = [
        "/",
        "/api/login/",
        "/api/admin/"
    ]
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}")
            if response.status_code == 200:
                content = response.text
                
                # Проверяем viewport meta tag
                if 'viewport' in content:
                    print(f"✅ {page}: viewport meta tag найден")
                else:
                    print(f"❌ {page}: viewport meta tag не найден")
                
                # Проверяем подключение CSS файлов
                css_count = content.count("style.css") + content.count("mobile.css")
                print(f"   🎨 CSS файлов подключено: {css_count}")
                
            else:
                print(f"❌ {page}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {page}: {e}")

def main():
    """Основная функция"""
    print("📱 Тестирование адаптивного дизайна")
    print("=" * 50)
    
    # Проверяем доступность сервера
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер доступен")
        else:
            print(f"❌ Сервер недоступен: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Сервер недоступен: {e}")
        return
    
    # Запускаем тесты
    test_css_files()
    test_html_templates()
    
    # Тестирование с Selenium (если доступен)
    try:
        test_responsive_design()
    except ImportError:
        print("\n⚠️  Selenium не установлен. Для полного тестирования установите:")
        print("   pip install selenium")
        print("   И скачайте ChromeDriver")
    except Exception as e:
        print(f"\n⚠️  Ошибка Selenium тестирования: {e}")
    
    print("\n🎉 Тестирование завершено!")
    print("\n💡 Для ручного тестирования:")
    print("   1. Откройте http://127.0.0.1:8000/")
    print("   2. Используйте инструменты разработчика (F12)")
    print("   3. Переключайтесь между разрешениями")
    print("   4. Проверьте работу на реальных устройствах")

if __name__ == '__main__':
    main()
