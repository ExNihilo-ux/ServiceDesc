# backend/scripts/new_migration.py
"""
Генератор шаблонов для SQL-first миграций Alembic.
Разделяет UP и DOWN скрипты по разным папкам.

Использование:
    python scripts/new_migration.py "add_masking_functions"
"""
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
SQL_UP_DIR = BASE_DIR / "sql" / "migrations"     # Папка для UP-скриптов
SQL_DOWN_DIR = BASE_DIR / "sql" / "rollbacks"    # Папка для DOWN-скриптов
ALEMBIC_VERSIONS = BASE_DIR / "alembic" / "versions"


def get_next_revision():
    """Находит последний номер ревизии."""
    existing = sorted(SQL_UP_DIR.glob("*.sql"))
    
    valid_revisions = []
    for f in existing:
        parts = f.stem.split("_")
        if parts[0].isdigit():
            valid_revisions.append(int(parts[0]))
    
    if not valid_revisions:
        return "001"
    
    last_num = max(valid_revisions)
    return f"{last_num + 1:03d}"


def create_migration(name: str):
    revision = get_next_revision()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_name = name.lower().replace(" ", "_").replace("-", "_")
    
    # Пути к файлам в РАЗНЫХ папках
    up_file = SQL_UP_DIR / f"{revision}_{safe_name}.sql"
    down_file = SQL_DOWN_DIR / f"{revision}_{safe_name}.down.sql"
    runner_file = ALEMBIC_VERSIONS / f"run_sql_{revision}.py"
    
    # Создаем папки если их нет
    SQL_UP_DIR.mkdir(parents=True, exist_ok=True)
    SQL_DOWN_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. UP SQL шаблон
    up_content = f"""-- {revision}_{safe_name}.sql
-- Created: {timestamp}
-- Description: TODO

BEGIN;

-- Твой SQL код здесь

COMMIT;
"""
    
    # 2. DOWN SQL шаблон
    down_content = f"""-- {revision}_{safe_name}.down.sql
-- Created: {timestamp}
-- Description: Rollback for {revision}_{safe_name}

BEGIN;

-- Твой rollback SQL здесь

COMMIT;
"""
    
    # 3. Генерация Runner
    prev_revision = f"{int(revision) - 1:03d}" if revision != "001" else None
    
    runner_content = f'''"""Auto-generated SQL migration runner

Revision ID: {revision}
Created: {timestamp}
"""
from pathlib import Path
from typing import Sequence, Union
from alembic import op

# === КОНФИГУРАЦИЯ МИГРАЦИИ ===
REVISION_ID = '{revision}'
DOWN_REVISION = {'None' if prev_revision is None else f"'{prev_revision}'"}
UP_SQL = Path(__file__).parent.parent.parent / "sql" / "migrations" / "{revision}_{safe_name}.sql"
DOWN_SQL = Path(__file__).parent.parent.parent / "sql" / "rollbacks" / "{revision}_{safe_name}.down.sql"
# ==========================

revision: str = REVISION_ID
down_revision: Union[str, None] = DOWN_REVISION
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _exec(path: Path) -> None:
    """Безопасное выполнение SQL-файла."""
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {{path}}")
    
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"SQL file is empty: {{path}}")
    
    op.execute(content)


def upgrade() -> None:
    _exec(UP_SQL)


def downgrade() -> None:
    _exec(DOWN_SQL)
'''
    
    # 4. Запись файлов
    up_file.write_text(up_content, encoding="utf-8")
    down_file.write_text(down_content, encoding="utf-8")
    runner_file.write_text(runner_content, encoding="utf-8")
    
    print(f"   Миграция {revision} создана:")
    print(f"   UP:   {up_file.relative_to(BASE_DIR)}")
    print(f"   DOWN: {down_file.relative_to(BASE_DIR)}")
    print(f"   RUN:  {runner_file.relative_to(BASE_DIR)}")
    print(f"\n Отредактируй SQL-файлы и запусти:")
    print(f"   docker compose exec backend alembic upgrade head")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python scripts/new_migration.py \"описание миграции\"")
        sys.exit(1)
    
    create_migration(sys.argv[1])