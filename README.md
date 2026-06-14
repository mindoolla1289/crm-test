# CRM «Спецтехника»

Мини‑CRM для учёта заявок на аренду спецтехники: клиенты, техника и заявки со статусами, пагинацией, фильтрацией и сортировкой.

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** Vue 3 + Pinia + Vite + Axios
- **Запуск:** Makefile (локально) или Docker Compose

---

## Структура проекта

```
crm/
├── Makefile                 # команды запуска
├── docker-compose.yml       # backend + frontend в Docker
├── backend/
│   ├── app/
│   │   ├── main.py          # точка входа FastAPI
│   │   ├── database.py      # подключение к БД, сессии
│   │   ├── models/models.py # SQLAlchemy-модели (Client, Equipment, Order)
│   │   ├── schemas/schemas.py # Pydantic-схемы
│   │   └── routers/         # clients.py, equipment.py, orders.py
│   ├── seed.py              # тестовые данные
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── main.js          # точка входа Vue
    │   ├── App.vue          # layout + вкладки
    │   ├── api.js           # axios-инстанс (baseURL: /api)
    │   ├── views/           # OrdersView, ClientsView, EquipmentView
    │   ├── components/      # OrderForm.vue
    │   └── stores/          # ordersStore.js, catalogStore.js (Pinia)
    ├── index.html
    ├── vite.config.js       # dev-прокси /api → backend
    ├── nginx.conf           # прод-прокси /api → backend
    ├── package.json
    └── Dockerfile
```

---

## Требования

- Python 3.10+
- Node.js 18+ и npm
- (опционально) Docker + Docker Compose

---

## 🪟 Запуск на Windows для новичка (с нуля, через Docker)

Этот раздел — для тех, кто запускает проект впервые и ничего не настраивал.
Docker сам поднимет и backend, и frontend — **ничего больше (Python, Node) ставить не нужно.**

### Шаг 1. Установить Docker Desktop

1. Открой страницу загрузки: **https://www.docker.com/products/docker-desktop/**
2. Нажми кнопку **Download for Windows** (вариант *Windows — AMD64*; для ноутбуков
   на ARM-процессоре выбери *Windows — ARM64*).
3. Запусти скачанный файл **`Docker Desktop Installer.exe`**.
4. В установщике оставь галочку **«Use WSL 2 instead of Hyper-V»** включённой и нажми **OK**.
   - Если появится сообщение, что нужен **WSL 2**, выполни в PowerShell (от имени
     администратора) команду `wsl --install`, перезагрузи компьютер и снова открой Docker Desktop.
5. После установки **перезагрузи компьютер**, если установщик попросит.
6. Запусти **Docker Desktop** (значок кита 🐳 в трее). Подожди, пока внизу слева
   индикатор станет зелёным — **Engine running**. Docker готов.

> Проверка: открой **PowerShell** и набери `docker --version` — должна появиться версия.

### Шаг 2. Скачать проект

- Если есть архив проекта — распакуй его в удобную папку, например `C:\projects\CRM`.
- Если проект в Git: установи Git с **https://git-scm.com/download/win**, затем в PowerShell:
  ```powershell
  git clone <ссылка-на-репозиторий> C:\projects\CRM
  ```

### Шаг 3. Запустить

1. Открой **PowerShell**.
2. Перейди в папку `crm` внутри проекта (где лежит файл `docker-compose.yml`):
   ```powershell
   cd C:\projects\CRM\crm
   ```
3. Запусти весь проект одной командой:
   ```powershell
   docker compose up --build
   ```
   Первый запуск занимает несколько минут — Docker скачивает образы и собирает проект.
   Когда в логах появятся строки от `crm-backend` и `crm-frontend`, всё готово.

### Шаг 4. Открыть в браузере

| Что          | Адрес                        |
|--------------|------------------------------|
| Приложение   | http://localhost:8080        |
| API-доки     | http://localhost:8000/docs   |

### Остановить / запустить снова

- **Остановить:** нажми `Ctrl + C` в окне PowerShell, затем выполни `docker compose down`.
- **Запустить снова** (образы уже собраны — быстро): `docker compose up`.

### Если порт занят

Если при запуске будет ошибка вида *«port is already allocated»* — значит порт `8080`
или `8000` занят другой программой. Открой `docker-compose.yml` и поменяй левое число
в строках `ports`, например `8081:80` вместо `8080:80`, и запусти снова.

> ⚠️ Команды `make` на Windows из коробки не работают — они для macOS/Linux.
> На Windows используй команды `docker compose ...` из этого раздела.

---

## Быстрый старт (локально)

Все команды выполняются из папки `crm/`.

```bash
make install   # venv + pip-зависимости + npm install (один раз)
make seed      # загрузить тестовые данные в БД
make dev       # запустить backend и frontend вместе
```

После запуска:

| Сервис   | URL                          |
|----------|------------------------------|
| Frontend | http://localhost:5173        |
| Backend  | http://localhost:8001        |
| API-доки | http://localhost:8001/docs   |

Остановить — `Ctrl+C` в терминале с `make dev` (гасит оба процесса).

> **Порты.** Backend поднимается на **8001**, потому что `8000` может быть занят другим
> проектом. Изменить порт: `make dev BACKEND_PORT=8002` (тогда поправьте и `target`
> в `frontend/vite.config.js`).

---

## Команды Makefile

| Команда             | Что делает                                             |
|---------------------|--------------------------------------------------------|
| `make help`         | список всех команд                                     |
| `make install`      | установить зависимости backend + frontend              |
| `make seed`         | загрузить тестовые данные (если БД пуста)              |
| `make backend`      | запустить только backend (uvicorn, `--reload`)         |
| `make frontend`     | запустить только frontend (vite dev)                   |
| `make dev`          | запустить backend + frontend одновременно              |
| `make build`        | собрать Docker-образы                                  |
| `make up`           | поднять весь стек в Docker                              |
| `make down`         | остановить Docker-стек                                  |
| `make logs`         | смотреть логи Docker                                   |
| `make clean`        | удалить venv, node_modules, БД и кеши                  |

---

## Запуск через Docker

```bash
make up      # сборка и старт; frontend на http://localhost:8080
make logs    # логи
make down    # остановить
```

> Если порты `8000`/`8080` заняты, поменяйте маппинги в `docker-compose.yml`
> (секция `ports`).

---

## Использование

Интерфейс — три вкладки:

- **Заявки** — список заявок с пагинацией, фильтром по статусу и сортировкой по дате.
  Кнопка создания открывает форму (`OrderForm`): выбор клиента, техники, комментарий.
  Статусы: `new` → `in_progress` → `completed`. Заявки можно редактировать и удалять.
- **Клиенты** — справочник клиентов (имя, телефон, email). Создание / редактирование / удаление.
- **Спецтехника** — справочник техники (название, категория, описание). Создание / редактирование / удаление.

---

## API

Базовый префикс — `/api`. Полная интерактивная документация: **http://localhost:8001/docs**.

| Метод  | Эндпоинт                  | Описание                                   |
|--------|---------------------------|--------------------------------------------|
| GET    | `/api/clients/`           | список клиентов                            |
| POST   | `/api/clients/`           | создать клиента                            |
| PUT    | `/api/clients/{id}`       | обновить клиента                           |
| DELETE | `/api/clients/{id}`       | удалить клиента                            |
| GET    | `/api/equipment/`         | список техники                             |
| POST   | `/api/equipment/`         | создать технику                            |
| PUT    | `/api/equipment/{id}`     | обновить технику                           |
| DELETE | `/api/equipment/{id}`     | удалить технику                            |
| GET    | `/api/orders/`            | список заявок (пагинация/фильтр/сортировка)|
| POST   | `/api/orders/`            | создать заявку                             |
| PUT    | `/api/orders/{id}`        | обновить заявку (в т.ч. статус)            |
| DELETE | `/api/orders/{id}`        | удалить заявку                             |

**Параметры `GET /api/orders/`:**

| Параметр     | По умолчанию | Описание                          |
|--------------|--------------|-----------------------------------|
| `page`       | `1`          | номер страницы                    |
| `page_size`  | `10`         | размер страницы (1–100)           |
| `status`     | —            | фильтр: `new`/`in_progress`/`completed` |
| `sort_order` | `desc`       | сортировка по дате: `asc`/`desc`  |

Пример:

```bash
curl "http://localhost:8001/api/orders/?page=1&page_size=5&status=new&sort_order=desc"
```

---

## База данных

- SQLite-файл `backend/crm.db` создаётся автоматически.
- `make seed` заливает демо‑данные (клиенты, техника, заявки) **только если БД пуста** —
  повторный запуск ничего не меняет.
- Полный сброс: `make clean` (удалит БД), затем `make seed`.
