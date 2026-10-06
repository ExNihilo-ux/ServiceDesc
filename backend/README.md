# Backend: ServiceDesc Airport Maintenance

Бэкенд системы обслуживания аэропорта на FastAPI + PostgreSQL (pgvector).

## Архитектура миграций (SQL-First)

### Структура папок
- `sql/migrations/` — UP-скрипты (применение изменений).
- `sql/rollbacks/` — DOWN-скрипты (откат изменений).
- `alembic/versions/` — Python-обёртки (runner'ы), генерируются автоматически.
- `scripts/new_migration.py` — Утилита для создания новых миграций.

### 🚀 Workflow создания миграции

1. **Создать новую миграцию:**
   ```bash
   python scripts/new_migration.py "описание_изменений"

Скрипт автоматически создаст:
    sql/migrations/XXX_description.sql
    sql/rollbacks/XXX_description.down.sql
    alembic/versions/run_sql_XXX.py

Написать SQL:
Открой созданные .sql файлы и напиши код между комментариями BEGIN; и COMMIT;.
Применить миграцию:
    docker compose exec backend alembic upgrade head

Откатить последнюю миграцию (при необходимости):
    docker compose exec backend alembic downgrade -1

alembic upgrade head        Применить все неприменённые миграции
alembic downgrade -1        Откатить последнюю миграцию
alembic downgrade <rev_id>  Откатить к конкретной ревизии
alembic current             Показать текущую версию схемы
alembic history --verbose   Показать историю всех миграций