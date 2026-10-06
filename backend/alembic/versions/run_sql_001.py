"""Auto-generated SQL migration runner

Revision ID: 001
Created: 2026-10-06 15:21:38
"""
from pathlib import Path
from typing import Sequence, Union
from alembic import op

# === КОНФИГУРАЦИЯ МИГРАЦИИ ===
REVISION_ID = '001'
DOWN_REVISION = None
UP_SQL = Path(__file__).parent.parent.parent / "sql" / "migrations" / "001_add_init_tables.sql"
DOWN_SQL = Path(__file__).parent.parent.parent / "sql" / "rollbacks" / "001_add_init_tables.down.sql"
# ==========================

revision: str = REVISION_ID
down_revision: Union[str, None] = DOWN_REVISION
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _exec(path: Path) -> None:
    """Безопасное выполнение SQL-файла."""
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
