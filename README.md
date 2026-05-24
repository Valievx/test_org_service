# Organization Service


Асинхронный микросервис управления подразделениями на `FastAPI + SQLAlchemy + PostgreSQL`.

## Что умеет сервис

- Создать подразделение: `POST /api/v1/departments/`
- Получение подразделения: `GET /api/v1/departments/{department_id}`
- Создать сотрудника в подразделении: `POST /api/v1/departments/{department_id}/employees/`
- Переместить подразделение в другое (изменить parent) `PATCH /api/v1/departments/{department_id}`
- Удалить подразделение `DELETE /api/v1/departments/{department_id}`

## Стек

- Python 3.13
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (async)
- Alembic
- PostgreSQL
- Docker / docker-compose

## Быстрый старт

### 1) Подготовить `.env`

В корне проекта должен быть файл `.env` (пример):

```env
DEBUG=True
DATABASE_URL=postgresql+asyncpg://user:password@localhost/mydatabase 


POSTGRES_DB=postgres_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
```


### 2) Запустить сервисы

```bash
docker compose up -d --build
```

Будут подняты:
- `backend` (API на `:8000`)
- `database`

### 3) Проверить, что API доступен

- Swagger: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
