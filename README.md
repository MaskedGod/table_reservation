# 🍽️ Table Reservation API

Асинхронное REST API для **бронирования столиков в ресторане**. Поддерживает создание и управление бронированиями и столами с проверкой на пересечения во времени. Построено на основе FastAPI с расширяемой архитектурой.

---

## 🚀 Возможности

- 📅 CRUD для бронирований
- 🍽️ CRUD для столиков
- 🚫 Проверка пересечений бронирований
- 🧪 Тесты с Pytest и PostgreSQL
- 🐳 Docker + docker-compose
- 🔁 Alembic миграции
- ♻️ Расширяемая архитектура на основе generic репозиториев и сервисов

---

## 📁 Структура проекта

```bash
app/
├── core/               # Конфигурация, подключение к БД
├── dependencies/       # Провайдеры зависимостей FastAPI
├── models/             # SQLAlchemy модели
├── repositories/       # Generic и конкретные репозитории
├── routers/            # FastAPI маршруты (ендпоинты)
├── schemas/            # Pydantic-схемы
├── services/           # Generic и конкретные сервисы
├── migrations/         # Alembic миграции
├── tests/              # Pytest тесты и docker-compose для них
...
```

---

## 🔗 API Эндпоинты

### 📋 Брони (`/reservations`)

| Метод | Эндпоинт              | Описание                                              |
|-------|------------------------|--------------------------------------------------------|
| GET   | `/reservations/`       | Получить список всех броней                           |
| POST  | `/reservations/`       | Создать бронь (с проверкой на пересечение времени)    |
| DELETE| `/reservations/{id}`   | Удалить бронь по ID                                   |

#### 🔁 Пример запроса `POST /reservations/`

```json
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2025-04-08T18:00:00",
  "duration_minutes": 90
}
```

> ⚠️ При конфликте по времени возвращается `409 Conflict` с сообщением:  
> `{"detail": "Table is already reserved at this time."}`

---

### 🪑 Столики (`/tables`)

| Метод | Эндпоинт         | Описание                        |
|-------|------------------|----------------------------------|
| GET   | `/tables/`       | Получить список всех столиков   |
| POST  | `/tables/`       | Создать новый столик            |
| DELETE| `/tables/{id}`   | Удалить столик по ID            |

#### 🛠 Пример запроса `POST /tables/`

```json
{
  "name": "Table 3",
  "seats": 4,
  "location": "терраса"
}
```

---

## ⚙️ Логика бронирования

- ❌ Нельзя создать бронь, если в указанный временной интервал столик уже занят.
- 🕒 Учитывается длительность в минутах (`duration_minutes`).
- ✅ Все данные валидируются через Pydantic-схемы и сервисный слой.

---

## 🧠 Расширяемость с помощью дженериков

### 🗃️ Generic Repository

Файл: `repositories/base.py`

```python
class BaseRepository(Generic[ModelType]):
    async def get_all(...) -> list[ModelType]: ...
    async def create(...) -> ModelType: ...
    async def delete(...) -> bool: ...
```

Легко расширяется:

```python
class CustomRepo(BaseRepository[MyModel]):
    ...
```

---

### 🧩 Generic Service

Файл: `services/base.py`

```python
class BaseService(Generic[ModelType]):
    def __init__(self, repo: BaseRepository[ModelType]): ...
```

Создание нового сервиса:

```python
class MyEntityService(BaseService[MyEntity]):
    ...
```

> Подходит для масштабируемых систем: добавление новых сущностей требует минимального кода.

---

## 🐳 Запуск проекта

1. **Клонируй репозиторий**:

```bash
git clone https://github.com/MaskedGod/table_reservation.git
cd table_reservation
```

2. **Скопируй файл окружения**:

```bash
cp .env.example .env
```

3. **Запусти приложение с помощью Docker Compose**:

```bash
docker compose up --build
```

4. **API будет доступно по адресу**:  
   📍 [http://localhost:8000](http://localhost:8000)

5. **Swagger-документация доступна по адресу**:  
   🧪 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Запуск тестов

1. Запусти отдельную тестовую БД:

```bash
docker compose -f tests/docker-compose.test.yml up -d
```

2. Установи [uv](https://github.com/astral-sh/uv) (опционально) — быстрый менеджер зависимостей:

```bash
pip install uv
```

3. Установи зависимости:

```bash
uv sync 
```

или

```bash
pip install -r requirements.txt
```

4. Запусти тесты:

```bash
pytest -v
```
