# Ozon Job Clone

Приложение для поиска работы, аналог Ozon Job. Состоит из backend API на FastAPI и frontend на HTML/JS.

## Структура проекта

- `main.py` - Backend сервер на FastAPI
- `index.html` - Frontend интерфейс
- `requirements.txt` - Зависимости Python

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск backend сервера

```bash
python main.py
```

Сервер запустится на http://127.0.0.1:8000

### 3. Открытие frontend

Откройте файл `index.html` в браузере или используйте простой HTTP сервер:

```bash
# Python 3
python -m http.server 8080

# Затем откройте http://localhost:8080/index.html
```

## API Endpoints

### Вакансии
- `GET /api/jobs` - Получить список всех вакансий
  - Параметры: `location` (город), `job_type` (тип занятости)
- `GET /api/jobs/{job_id}` - Получить конкретную вакансию
- `POST /api/jobs` - Создать новую вакансию

### Отклики
- `POST /api/applications` - Отправить отклик на вакансию
- `GET /api/applications` - Получить список откликов

## Функционал

### Для соискателей:
- Поиск вакансий по городу и типу занятости
- Просмотр деталей вакансии (зарплата, описание, требования)
- Отправка отклика с резюме

### Для работодателей (через API):
- Создание новых вакансий
- Управление списком вакансий

## Технологии

**Backend:**
- FastAPI - современный фреймворк для создания API
- Pydantic - валидация данных
- Uvicorn - ASGI сервер

**Frontend:**
- Vanilla JavaScript
- CSS3 с анимациями
- Fetch API для работы с backend

## Примеры использования API

### Получить все вакансии:
```bash
curl http://127.0.0.1:8000/api/jobs
```

### Найти вакансии в Москве:
```bash
curl "http://127.0.0.1:8000/api/jobs?location=Москва"
```

### Создать вакансию:
```bash
curl -X POST http://127.0.0.1:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Менеджер",
    "company": "ООО Ромашка",
    "salary_min": 50000,
    "salary_max": 80000,
    "description": "Работа с клиентами",
    "location": "Казань",
    "type": "Full-time"
  }'
```

### Отправить отклик:
```bash
curl -X POST http://127.0.0.1:8000/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "<ID_ВАКАНСИИ>",
    "applicant_name": "Иван Иванов",
    "applicant_contact": "ivan@example.com",
    "resume_text": "Опыт работы 5 лет..."
  }'
```

## Примечания

- Данные хранятся в памяти приложения (после перезапуска сервера данные сбрасываются)
- Для production использования необходимо подключить базу данных (PostgreSQL, MongoDB и т.д.)
- Добавить аутентификацию и авторизацию пользователей
