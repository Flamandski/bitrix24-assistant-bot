import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SELENIUM_HEADLESS
from modules.database import save_or_update_doc


def setup_driver():
    options = Options()
    
    if SELENIUM_HEADLESS:
        options.add_argument("--headless")
    
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--allow-running-insecure-content")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    return webdriver.Chrome(options=options)

def scrape_and_save_to_db(urls_to_scrape):
    driver = setup_driver()
    success_count = 0
    
    for url in urls_to_scrape:
        try:
            print(f"🌐 Открываю: {url}")
            driver.get(url)
            
            # Ждём загрузки основного контента (используем точный класс из HTML)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dc-doc-page__body"))
            )
            time.sleep(2)
            
            try:
                title = driver.find_element(By.CSS_SELECTOR, "h1.dc-doc-page__title").text.strip()
            except:
                title = driver.find_element(By.TAG_NAME, "h1").text.strip()

            try:
                content_element = driver.find_element(By.CSS_SELECTOR, ".dc-doc-page__body")
                content = content_element.text.strip()
            except:
                content = driver.find_element(By.TAG_NAME, "main").text.strip()
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)
            
            category = url.split('/')[-2] if len(url.split('/')) > 2 else "general"
            
            save_or_update_doc(url=url, title=title, content=content, category=category)
            success_count += 1
            print(f"✅ Успешно: {title} ({len(content)} символов)")
            
        except Exception as e:
            print(f"❌ Ошибка парсинга {url}")
            print(f"   Тип: {type(e).__name__}")
            print(f"   Сообщение: {str(e)}")
            
    driver.quit()
    print(f"\n🎉 Парсинг завершен! Успешно: {success_count}/{len(urls_to_scrape)}")
if __name__ == "__main__":
    test_urls = [
        # Контакты
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-add.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-get.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-update.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-list.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-delete.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/contacts/crm-contact-fields.html",
        
        # Сделки
        "https://apidocs.bitrix24.ru/api-reference/crm/deals/crm-deal-add.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/deals/crm-deal-get.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/deals/crm-deal-list.html",
        
        # Лиды
        "https://apidocs.bitrix24.ru/api-reference/crm/leads/crm-lead-add.html",
        "https://apidocs.bitrix24.ru/api-reference/crm/leads/crm-lead-get.html",
        
        # Задачи
        "https://apidocs.bitrix24.ru/api-reference/tasks/task-add.html",
        "https://apidocs.bitrix24.ru/api-reference/tasks/task-get.html",
        
        # Пользователи
        "https://apidocs.bitrix24.ru/api-reference/user/user-add.html",
        "https://apidocs.bitrix24.ru/api-reference/user/user-get.html",
    ]
    scrape_and_save_to_db(test_urls)