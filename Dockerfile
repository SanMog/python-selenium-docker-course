# Шаг 1: Выбираем базовый образ.
# Мы берем официальный образ с Python версии 3.9.
# "slim" - это облегченная версия, чтобы наш контейнер был меньше.
FROM python:3.9-slim

# Шаг 2: Устанавливаем Google Chrome и другие утилиты (НОВАЯ ВЕРСИЯ КОМАНДЫ)
RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# Шаг 3: Определяем рабочую директорию внутри контейнера.
# Все последующие команды будут выполняться из этой папки.
WORKDIR /app

# Шаг 4: Копируем файл с зависимостями в контейнер.
COPY requirements.txt .

# Шаг 5: Устанавливаем наши Python-библиотеки.
# --no-cache-dir - это хорошая практика, чтобы не раздувать размер контейнера кэшем.
RUN pip install --no-cache-dir -r requirements.txt

# Шаг 6: Копируем все остальные файлы нашего проекта (наши .py скрипты) в контейнер.
COPY . .

# Шаг 7: Указываем команду, которая будет запускаться при старте контейнера.
# В нашем случае - это запуск тестов с помощью pytest.
CMD ["pytest"]