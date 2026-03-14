# Organizations Catalog API

REST API-сервис справочника организаций на стеке **FastAPI + SQLAlchemy + Alembic**.

## Функциональность

### Сущности
- **Organization**: название, несколько телефонов, одно здание, несколько видов деятельности.
- **Building**: адрес, широта, долгота.
- **Activity**: древовидная классификация деятельностей (максимум 3 уровня вложенности).

### Реализованные API-сценарии
- Список организаций в конкретном здании.
- Список организаций по виду деятельности.
- Поиск организаций по виду деятельности с учетом дочерних (`include_children=true`).
- Поиск организаций по названию.
- Поиск организаций в радиусе от точки (`lat`, `lon`, `radius_km`).
- Поиск организаций в прямоугольной области (`min_lat`, `max_lat`, `min_lon`, `max_lon`).
- Получение организации по идентификатору.
- Список зданий.
- Список деятельностей.

### Безопасность
Все API-методы под `/api/v1/*` защищены статическим ключом в заголовке:

```text
X-API-Key: super-secret-key
```

---

## Структура проекта

```text
app/
  api/v1/               # роуты
  core/                 # конфигурация и безопасность
  db/                   # сессия, base, seed/init
  models/               # SQLAlchemy модели
  schemas/              # Pydantic-схемы
  services/             # бизнес-логика выборок
alembic/                # миграции
tests/                  # тесты API
```

---

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.db.init_data
uvicorn app.main:app --reload
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
python -m app.db.init_data
uvicorn app.main:app --reload
```

После запуска:
- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

---

## Запуск в Docker (PostgreSQL + API)

```bash
cp .env.example .env
docker compose up --build
```

Порты:
- API: `8000`
- PostgreSQL (host): `55432` (`55432 -> 5432`)

---

## Проверка API вручную

### PowerShell (рекомендуется)

```powershell
$h = @{ "X-API-Key" = "super-secret-key" }

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/buildings/" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations?building_id=1" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations/1" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations?activity_id=1&include_children=true" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations?name=Авто" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations?lat=55.7558&lon=37.6173&radius_km=2" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/organizations?min_lat=55.74&max_lat=55.76&min_lon=37.60&max_lon=37.63" -Headers $h
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/activities/" -Headers $h
```

### Linux/macOS

```bash
curl -H "X-API-Key: super-secret-key" http://localhost:8000/api/v1/buildings/
curl -H "X-API-Key: super-secret-key" "http://localhost:8000/api/v1/organizations?building_id=1"
curl -H "X-API-Key: super-secret-key" http://localhost:8000/api/v1/organizations/1
curl -H "X-API-Key: super-secret-key" "http://localhost:8000/api/v1/organizations?activity_id=1&include_children=true"
curl -H "X-API-Key: super-secret-key" "http://localhost:8000/api/v1/organizations?name=Авто"
curl -H "X-API-Key: super-secret-key" "http://localhost:8000/api/v1/organizations?lat=55.7558&lon=37.6173&radius_km=2"
curl -H "X-API-Key: super-secret-key" "http://localhost:8000/api/v1/organizations?min_lat=55.74&max_lat=55.76&min_lon=37.60&max_lon=37.63"
curl -H "X-API-Key: super-secret-key" http://localhost:8000/api/v1/activities/
```

---

## Тесты

```bash
pytest -q
```

---


## Примечания по данным

Проект содержит базовый seed-набор:
- 2 здания,
- дерево деятельностей (Еда/Автомобили + дочерние),
- 2 организации с телефонами и привязкой к деятельностям.

Seed идемпотентный: повторный запуск не дублирует записи, если здания уже существуют.