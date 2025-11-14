# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WikipediaPage:
    """
    Этот класс описывает главную страницу Википедии
    и действия, которые на ней можно выполнить.
    """

    def __init__(self, driver):
        """
        Конструктор класса. При создании объекта страницы,
        мы передаем ему драйвер, чтобы страница могла управлять браузером.
        """
        self.driver = driver

        # --- ЛОКАТОРЫ ---
        # Здесь мы храним "адреса" всех элементов, с которыми работаем.
        # Если разработчики изменят ID поля, мы поправим его только в одном месте.

        # Поле поиска. Это кортеж, содержащий два значения:
        # 1. КАК искать (By.ID)
        # 2. ЧТО искать ("searchButton")
        self.SEARCH_INPUT = (By.ID, "searchInput")

        # Кнопка поиска.
        self.SEARCH_BUTTON = (By.ID, "searchButton")

    def open(self):
        """Метод для открытия главной страницы Википедии."""
        self.driver.get("https://ru.wikipedia.org/")
        return self  # Возвращаем self для возможности строить "цепочки вызовов"

    def search_for(self, text):
        """
        Метод для выполнения поиска.
        Он находит поле, вводит текст и нажимает на кнопку.
        """
        # Находим поле ввода, используя локатор SEARCH_INPUT
        search_input_element = self.driver.find_element(*self.SEARCH_INPUT)
        search_input_element.send_keys(text)

        # Находим кнопку поиска и кликаем на нее
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def get_title(self):
        """Метод, который просто возвращает заголовок текущей страницы."""
        return self.driver.title

    def wait_for_title_contains(self, text):
        """
        Метод-ожидание. Он будет ждать (до 10 секунд),
        пока в заголовке страницы не появится нужный текст.
        """
        WebDriverWait(self.driver, 10).until(
            EC.title_contains(text)
        )