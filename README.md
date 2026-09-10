# Habits

REST API для управления привычками. Проект разработан на Django REST Framework и контейнеризирован с использованием Docker Compose.

## Стек

* Python 3.14
* Django 6
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Celery Beat
* Nginx
* Gunicorn
* Docker / Docker Compose
* GitHub Actions

## Запуск проекта локально

### 1. Клонирование репозитория

```bash
git clone https://github.com/neron262013-sudo/Habits.git
cd Habits
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.template`:

```bash
cp .env.template .env
```

Для Windows PowerShell:

```powershell
Copy-Item .env.template .env
```

Заполните необходимые переменные окружения в `.env`.

Файл `.env` содержит конфиденциальные данные и не должен добавляться в Git.

### 3. Запуск проекта

Все сервисы проекта запускаются одной командой:

```bash
docker compose up -d --build
```

Docker Compose автоматически создаёт и запускает следующие сервисы:

* `web` — Django + Gunicorn;
* `db` — PostgreSQL;
* `redis` — Redis;
* `celery` — Celery worker;
* `celery-beat` — Celery Beat;
* `nginx` — Nginx.

Миграции базы данных выполняются отдельным сервисом `migrate` перед запуском Django, Celery и Celery Beat.

### 4. Проверка состояния контейнеров

```bash
docker compose ps
```

Основные сервисы должны иметь статус `Up`, а PostgreSQL и Redis — статус `healthy`.

### 5. Остановка проекта

```bash
docker compose down
```

Команда останавливает и удаляет контейнеры, но сохраняет данные PostgreSQL и Redis в Docker volumes.

Для удаления контейнеров вместе с volumes:

```bash
docker compose down -v
```

> Используйте `-v` с осторожностью, поскольку при этом удаляются данные из Docker volumes.

## Доступ к API

После запуска проекта API доступно через Nginx:

```text
http://localhost/habits/
```

Для просмотра API в формате JSON:

```text
http://localhost/habits/?format=json
```

Защищённые endpoints требуют JWT-аутентификации.

## Доступ к приложению на сервере

После успешного автоматического deploy приложение доступно по адресу:

```text
http://158.160.219.194/habits/
```

Endpoint защищён JWT-аутентификацией. При обращении без токена ожидается ответ `401 Unauthorized`.

## Документация API

В проекте используется `drf-yasg` для генерации документации API.

Swagger/OpenAPI документация доступна через настроенные endpoints проекта.

## Архитектура Docker Compose

Проект состоит из отдельных контейнеров для основных сервисов:

```text
                    ┌──────────────┐
                    │    Nginx     │
                    │     :80      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Django/Web   │
                    │   Gunicorn   │
                    │     :8000    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │PostgreSQL│ │  Redis   │ │  Celery  │
        └──────────┘ └──────────┘ └─────┬────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │ Celery Beat  │
                                 └──────────────┘

                           ┌──────────────┐
                           │    migrate   │
                           │   migrations │
                           └──────────────┘
```

Nginx используется как reverse proxy перед Django и обслуживает статические и media-файлы.

Сервис `migrate` выполняет миграции базы данных перед запуском зависимых сервисов.

## Тестирование

Для запуска тестов локально:

```bash
python manage.py test
```

Или внутри контейнера Django:

```bash
docker compose run --rm web python manage.py test
```

## Линтинг

Для проверки кода используется Flake8:

```bash
flake8 .
```

## CI/CD

В проекте настроен GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

Pipeline состоит из следующих этапов:

```text
test
  ↓
lint
  ↓
build
  ↓
deploy
```

### Test

На этапе `test`:

1. устанавливается Python;
2. устанавливаются зависимости из `requirements.txt`;
3. запускаются тесты Django.

### Lint

После успешного прохождения тестов запускается Flake8 для проверки качества кода.

### Build

После успешного линтинга проверяется возможность сборки Docker-образа:

```bash
docker build -t habits-app .
```

### Deploy

Deploy выполняется автоматически после успешного прохождения всех предыдущих этапов.

Деплой запускается при push в ветку:

```text
feature/course_6
```

GitHub Actions подключается к удалённому серверу по SSH и выполняет:

```bash
git pull
docker compose down
docker compose up -d --build
```

После этого на сервере запускается обновлённая версия проекта.

## Настройка GitHub Actions

Для автоматического deploy в настройках репозитория GitHub необходимо добавить следующие Secrets:

```text
SSH_KEY
SSH_USER
SERVER_IP
DEPLOY_DIR
```

### SSH_KEY

Приватный SSH-ключ, используемый GitHub Actions для подключения к серверу.

### SSH_USER

Пользователь удалённого сервера.

### SERVER_IP

Публичный IP-адрес сервера.

### DEPLOY_DIR

Путь к директории проекта на сервере.

Например:

```text
/home/admin1/habits
```

Приватные ключи и другие секретные данные не должны храниться непосредственно в репозитории.

## Настройка удалённого сервера

На сервере должны быть установлены:

* Docker;
* Docker Compose;
* Git;
* SSH-доступ.

Проект размещается в отдельной директории:

```text
/home/admin1/habits
```

После первоначального клонирования репозитория и настройки `.env` дальнейшее обновление проекта выполняется автоматически через GitHub Actions.

## Deploy

После push в `feature/course_6` GitHub Actions:

1. запускает тесты;
2. выполняет линтинг;
3. проверяет сборку Docker-образа;
4. подключается к серверу по SSH;
5. обновляет код через `git pull`;
6. останавливает текущие контейнеры;
7. пересобирает Docker-образы;
8. запускает обновлённую версию проекта через Docker Compose.

Проверить состояние сервисов на сервере можно командой:

```bash
docker compose ps
```

После успешного deploy приложение доступно через Nginx:

```text
http://158.160.219.194/habits/
```

## Важные файлы

```text
Dockerfile
docker-compose.yml

nginx/
├── Dockerfile
└── nginx.conf

.github/
└── workflows/
    └── ci.yml

.env.template
requirements.txt
```

Файл `.env` используется для локальной и серверной конфигурации и не добавляется в репозиторий.

## Остановка серверного проекта

Для остановки контейнеров на сервере:

```bash
docker compose down
```

Для повторного запуска:

```bash
docker compose up -d --build
```

В штатном режиме после изменения кода ручной запуск не требуется — обновление выполняется автоматически через GitHub Actions.
