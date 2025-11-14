# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Добавляем импорт для ОПЦИЙ Chrome
from selenium.webdriver.chrome.options import Options
# Импортируем наш новый класс страницы
from wikipedia_page import WikipediaPage


@pytest.fixture
def driver():
    """
    Фикстура, которая подготавливает и закрывает браузер
    для каждого теста.
    """
    # --- Настройка опций для запуска Chrome ---
    chrome_options = Options()
    # Самая главная опция: запускаем Chrome в headless-режиме
    chrome_options.add_argument("--headless")
    # Эта опция нужна для запуска в Docker, т.к. там нет "песочницы"
    chrome_options.add_argument("--no-sandbox")
    # Эта опция решает некоторые проблемы с памятью в Docker
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Указываем размер окна, чтобы верстка сайта была предсказуемой
    chrome_options.add_argument("--window-size=1920,1080")

    service = ChromeService(ChromeDriverManager().install())
    # Передаем наши опции при создании драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# --- ВОТ ЭТА ЧАСТЬ БЫЛА ПОТЕРЯНА ---
def test_search_python_on_wikipedia(driver):
    """
    Тест-кейс: Проверка функциональности поиска на сайте wikipedia.org.
    """
    # --- Подготовка ---
    # Создаем экземпляр нашей страницы, передавая ему "живой" браузер из фикстуры
    wiki_page = WikipediaPage(driver)

    # --- Шаги теста ---
    # 1. Открыть страницу
    wiki_page.open()

    # 2. Выполнить поиск по слову "Python"
    wiki_page.search_for("Python")

    # 3. Подождать, пока загрузится страница результатов
    wiki_page.wait_for_title_contains("Python")

    # --- Проверка (Assertion) ---
    # Убеждаемся, что слово "Python" действительно есть в заголовке новой страницы.
    assert "Python" in wiki_page.get_title()