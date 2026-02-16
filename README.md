## Приложение для отслеживания привычек

Проект представляет собой REST API для управления привычками с использованием Django и Django REST Framework.

### 🌐 Демо сервер
**Адрес приложения:** 
http://158.160.85.129/
**Swagger документация:** 
http://158.160.85.129/swagger/
**Админка:** 
http://158.160.85.129/admin/

## 🚀 Быстрый запуск локально (с Docker)
### Требования
* Docker Engine 20.10+

* Docker Compose 2.0+

### Шаги запуска:

1. Клонируйте репозиторий
```
git clone https://github.com/Diesto070/CourseWork_5.git
cd CourseWork_5
```

2. Создайте файл окружения
```cp .env.example .env```

Отредактируйте .env файл, установите свои значения (секретные ключи, пароли БД и т.д.)

SECRET_KEY=...
DEBUG=...

**настройки базы данных**

POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...

3. Запустить все сервисы одной командой
```docker-compose up --build```

Или в фоновом режиме
```docker-compose up -d --build```
4. Остановка всех сервисов
docker-compose down


## 🐳 Архитектура контейнеров

Проект использует микросервисную архитектуру с Docker:

### Сервисы:
1. web - Django приложение (порт 8000)

2. db - PostgreSQL база данных (порт 5432)

3. redis - Redis для кеша и Celery брокера (порт 6379)

4. celery - Celery worker для фоновых задач

5. celery-beat - Celery beat для периодических задач

6. nginx - Nginx веб-сервер (порт 80)

## 🚀 Настройка CI/CD с GitHub Actions
### Требования для автоматического деплоя:

1. Сервер с Ubuntu/Debian

2. Установленные Docker и Docker Compose

3. Настроенный SSH доступ

4. Аккаунт на Docker Hub

### Настройка сервера:
Создайте виртуальную машину, подключитесь к ней. В рамках учебного проекта сервер развернут на базе Яндекс.Cloud по адресу: http://158.160.31.117/

### 1. Установка Docker на сервер:

```
# Подключение к серверу
ssh username@server_ip

# Установка Docker
sudo apt update && sudo apt install docker.io -y

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
# Перезапустите сессию SSH
```

### 2. Подготовка папки проекта:

``` 
# Создайте папку для проекта
mkdir -p /coursework5/
cd /coursework5/

# Клонируйте репозиторий
git clone <ваш-репозиторий> .

# Создайте .env файл
cp .env.example .env
nano .env  # Отредактируйте настройки

# Настройте права
chmod 600 .env
```

В созданной директории создайте файл .env с переменными, необходимыми для развертывания проекта:
```
cat > .env << 'EOF'
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
STATIC_ROOT=/app/staticfiles
POSTGRES_PASSWORD=your-password
POSTGRES_USER=postgres
POSTGRES_DB=postgres
DATABASE_URL=postgres://postgres:your-password@db:5432/postgres
EOF
```

### Настройка GitHub Secrets:

В настройках репозитория GitHub (Settings → Secrets and variables → Actions) добавьте:

1. DOCKER_HUB_USERNAME - ваш логин на Docker Hub
2. DOCKER_HUB_ACCESS_TOKEN - токен доступа Docker Hub

3. SERVER_IP - IP адрес вашего сервера

4. SSH_USER_SERVER - имя пользователя на сервере

5. SSH_KEY_PRIVATE - приватный SSH ключ

6. SECRET_KEY - секретный ключ Django для тестов

### Создание Docker Hub репозитория:
1. Зарегистрируйтесь на Docker Hub

2. Создайте репозиторий с именем coursework

3. Создайте Access Token: Settings → Security → New Access Token

## 🔄 GitHub Actions Workflow
### Процесс CI/CD состоит из 4 этапов:

### 1. Lint - Проверка кода
* Проверка синтаксиса с flake8

* Проверка стиля кодирования

### 2. Test - Запуск тестов
* Запуск unit-тестов Django

* Тестирование с PostgreSQL и Redis

* Проверка миграций

### 3. Build - Сборка Docker образа
* Сборка Docker образа

* Загрузка образа в Docker Hub

* Тегирование по хешу коммита

### 4. Deploy - Деплой на сервер
* Подключение к серверу по SSH

* Остановка старых контейнеров

* Загрузка нового образа

* Запуск обновленных контейнеров

* Проверка health check

## 📋 Файлы конфигурации
* Dockerfile
* docker-compose.yml
* .github/workflows/ci.yml
* .env.example

### Основные возможности
* **Аутентификация** через JWT токены
* **Управление привычками** (CRUD операции)
* **Напоминания в Telegram** о выполнении привычек
* **Публичные привычки** для общего доступа
* **Валидация** правил создания привычек
* **Периодические задачи** через Celery

### Технологии
* Python 3.11+
* Django 5.2
* Django REST Framework
* PostgreSQL
* Redis (кеш и Celery брокер)
* Celery + Celery Beat
* Telegram Bot API
* JWT аутентификация
* Swagger документация
* Docker - контейнеризация
* CI/CD - деплой на сервер


### Установка и запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение
3. Установить зависимости
4. Настроить базу данных (PostgreSQL)
5. Настроить переменные окружения
6. Применить миграции
7. Запустить сервер
8. Запустить Celery worker и Celery Beat (в отдельных терминалах)
9. Настроить Telegram Bot и получить API ключ


## API эндпоинты
### Аутентификация
* POST /users/register/ - регистрация
* POST /users/login/ - получение JWT токенов
* POST /users/api/token/refresh/ - обновление токена

### Привычки
* GET /habits/habits/ - список своих привычек
* POST /habits/habit/create/ - создать привычку
* GET /habits/habit/<id>/ - получить привычку
* PUT /habits/habit/<id>/update/ - обновить привычку
* DELETE /habits/habit/<id>/delete/ - удалить привычку
* GET /habits/public/ - публичные привычки

### Документация
* GET /swagger/ - Swagger UI
* GET /redoc/ - ReDoc
* GET /swagger<format>/ - JSON/ YAML схемы

## Правила валидации привычек
1. Нельзя одновременно указывать связанную привычку и вознаграждение
2. Время выполнения ≤ 120 секунд
3. Связанная привычка должна быть приятной
4. У приятной привычки не может быть связанной привычки или вознаграждения
5. Периодичность: 1-7 дней

## Напоминания в Telegram
Система автоматически отправляет напоминания в Telegram:
* Проверка каждую минуту через Celery Beat
* Отправка в указанное время (±2 минуты)
* Учет периодичности выполнения
* Кеширование дат отправки в Redis

## Структура проекта

config/          - основные настройки Django

habits/          - приложение для привычек

users/           - приложение для пользователей

pyproject.toml - зависимости


## Тестирование
Запуск тестов:
```python manage.py test habits.tests```
```python manage.py test users.tests```


### 📞 Контакты и поддержка
Проект разработан в рамках учебного курса. Для вопросов и предложений обращайтесь через Issues в репозитории.

**Автор:** Diesto070

**GitHub:** [Diesto070](https://github.com/Diesto070)