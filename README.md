# FastAPI Booking/Островок

## Описание
Этот проект предоставляет возможности по поиску отелей и предоставлении информации о доступных номер, в том числе с информацией о них.

Пользователь может зарегестироваться и забронировать номер в отеле. Также есть возможность получить все свои бронирования. 

## Использованные технологии
- FastAPI
- БД: PostgreSQL
- Работа с БД через ORM: SQLAlchemy
- Кэширования при помощи Redis
- Отложенные задачи: Celery + Flower
- Админка: SQLAlchemy Admin

## Предустановки
- Python 3.9
- PostgreSQL 15.3
- Redis 5.0.14.1 

Модули прописаны в файле requirements.txt.
## Запуск приложения

### Файл конфигурации
Для конфигурации необходимо добавить файл .env в корневую папку:
```
MODE=DEV


DB_HOST=database_host
DB_PORT=database_port
DB_USER=database_user
DB_PASS=database_password
DB_NAME=database_name

TEST_DB_HOST=test_db_host
TEST_DB_PORT=test_database_port
TEST_DB_USER=test_database_user
TEST_DB_PASS=test_database_password
TEST_DB_NAME=test_database_name

# Config for JWT authentication
SECRET_KEY=JWT_secret_key
ALGORITHM=JWT_encryption_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Config for email-server 
SMTP_HOST=smtp_server
SMTP_PORT=smtp_port
SMTP_USER=smtp_user_email
SMTP_PASS=smtp_password

REDIS_HOST=redis_host
REDIS_PORT=redis_port
```
### Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn:
```
uvicorn app.main:app --reload
```  
### Redis

Redis server должен быть запущен.
### Celery & Flower
Для запуска Celery используется команда
Linux/MacOS:
```
celery -A app.tasks.celery:celery worker --loglevel=INFO
```
Windows:
```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```

Для запуска Flower:
```
celery --app=app.tasks.celery:celery flower
``` 

## Обратная связь
Любые комментарии, вопрос и исправления пишите мне в [телеграм](https://t.me/Joann_D).