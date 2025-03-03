FROM python:3.9-slim

WORKDIR /app

# Установка русской локали и необходимых пакетов для Eel
RUN apt-get update && apt-get install -y locales curl unzip \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

# Установка Chrome для режима Eel (headless)
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Определение переменных среды
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=ru_RU.UTF-8
ENV LANG=ru_RU.UTF-8
ENV PYTHONIOENCODING=utf-8
# Для headless режима Chrome
ENV DISPLAY=:99

# Указываем порты Eel
EXPOSE 8081 9090

# Запуск приложения
CMD ["python", "main/run.py"]
