# Погодное API

Сервис предоставляет информацию о погоде на основе данных от OpenWeatherMap с веб-интерфейсом на Eel.

## Возможности
- Получение текущей погоды для указанного города
- Прогноз погоды на ближайшие 5 дней
- Веб-интерфейс на базе Eel

## Установка и запуск

### Предварительные требования
- Docker и Docker Compose
- API ключ от OpenWeatherMap (уже настроен)

### Запуск проекта
```bash
# Клонирование репозитория
git clone <repo-url>
cd <repo-directory>

# Запуск с помощью Docker Compose
docker-compose up -d
```

### Запуск без Docker
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python main/run.py
```

## Интерфейс и API

### Веб-интерфейс
После запуска доступен по адресу:
- http://localhost:8081 (основной)
- http://localhost:9090 (запасной)

### Мониторинг

Проект поддерживает мониторинг с использованием Prometheus и Grafana.

- Prometheus: http://localhost:9091
- Grafana: http://localhost:3000 (логин/пароль: admin/admin)

## Структура проекта
```
.
├── main/
│   ├── run.py       # Основной скрипт запуска (Eel)
│   ├── api.py       # API для работы с OpenWeatherMap
│   ├── route.py     # Маршрутизация для Eel
│   └── app.py       # Flask приложение (альт. API)
├── static/          # Статические файлы для Eel
├── docker/
│   ├── prometheus/  # Конфигурация Prometheus
│   └── grafana/     # Конфигурация Grafana
├── Dockerfile       # Dockerfile для приложения
├── docker-compose.yml # Конфигурация Docker Compose
└── requirements.txt # Зависимости Python
```
