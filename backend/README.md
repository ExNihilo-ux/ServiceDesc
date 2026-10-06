# Backend: ServiceDesc Airport Maintenance

Бэкенд системы обслуживания аэропорта на FastAPI + PostgreSQL (pgvector).

## Архитектура миграций (SQL-First)

Мы используем подход **SQL-First Migrations**. Схема БД описывается чистыми SQL-скриптами, а Alembic выступает только как система версионирования и доставки изменений. Это обеспечивает полный контроль над DDL, типами данных (включая pgvector) и индексами.

### Структура папок

| Папка | Назначение |
| :--- | :--- |
| `sql/migrations/` | UP-скрипты (применение изменений схемы) |
| `sql/rollbacks/` | DOWN-скрипты (откат изменений) |
| `alembic/versions/` | Python-обёртки (runner'ы), генерируются автоматически |
| `scripts/` | Утилиты автоматизации (`new_migration.py`) |

### Workflow создания миграции

1.  **Создать новую миграцию:**
    ```bash
    python scripts/new_migration.py "описание_изменений"
    ```
    Скрипт автоматически создаст три файла:
    -   `sql/migrations/XXX_description.sql`
    -   `sql/rollbacks/XXX_description.down.sql`
    -   `alembic/versions/run_sql_XXX.py`

2.  **Написать SQL:**
    Открой созданные `.sql` файлы и напиши код между комментариями `BEGIN;` и `COMMIT;`.

3.  **Применить миграцию:**
    ```bash
    docker compose exec backend alembic upgrade head
    ```

4.  **Откатить последнюю миграцию (при необходимости):**
    ```bash
    docker compose exec backend alembic downgrade -1
    ```

### Важные правила

-   **Никогда не редактируй** уже применённые SQL-файлы. Создавай новую миграцию для исправлений.
-   **Всегда пиши rollback-скрипт.** Миграция без отката считается недоделанной.
-   **Используй транзакции.** Все DDL-операции должны быть обёрнуты в `BEGIN; ... COMMIT;`.
-   **Не используй `--autogenerate`.** Автогенерация не понимает pgvector, кастомные типы и сложную логику.

## ️ Полезные команды Alembic

| Команда | Описание |
| :--- | :--- |
| `alembic upgrade head` | Применить все неприменённые миграции |
| `alembic downgrade -1` | Откатить последнюю миграцию |
| `alembic downgrade <rev_id>` | Откатить к конкретной ревизии |
| `alembic current` | Показать текущую версию схемы |
| `alembic history --verbose` | Показать историю всех миграций |

##  Инфраструктура

-   **Python:** 3.12-slim
-   **DB:** PostgreSQL 16 + pgvector
-   **Async Driver:** asyncpg (для приложения), psycopg2-binary (для Alembic)
-   **Config:** Все секреты вынесены в `.env`
-   **Containerization:** Docker Compose + Uvicorn (--reload)