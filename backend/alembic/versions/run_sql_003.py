"""Auto-generated SQL migration runner

Revision ID: 003
Created: 2026-10-07 10:16:30
"""
from pathlib import Path
from typing import Sequence, Union
from alembic import op

# === КОНФИГУРАЦИЯ МИГРАЦИИ ===
REVISION_ID = '003'
DOWN_REVISION = '002'
UP_SQL = Path(__file__).parent.parent.parent / "sql" / "migrations" / "003_fix_auto_ids_and_refactor_functions.sql"
DOWN_SQL = Path(__file__).parent.parent.parent / "sql" / "rollbacks" / "003_fix_auto_ids_and_refactor_functions.down.sql"
# ==========================

revision: str = REVISION_ID
down_revision: Union[str, None] = DOWN_REVISION
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _exec(path: Path) -> None:
    """Выполняет внешний SQL-файл внутри транзакции Alembic.
    
    Проверяет существование файла и его непустоту перед выполнением.
    Экранирование {path} необходимо для корректной генерации f-строк.
    """
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"SQL file is empty: {path}")
    
    op.execute(content)


def upgrade() -> None:
    _exec(UP_SQL)


def downgrade() -> None:
    _exec(DOWN_SQL)
