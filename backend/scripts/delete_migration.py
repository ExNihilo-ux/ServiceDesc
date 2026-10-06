# backend/scripts/delete_migration.py
"""
Безопасное удаление последней созданной миграции.
Работает ТОЛЬКО если миграция ещё НЕ применена к БД!

Использование:
    python scripts/delete_migration.py
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SQL_DIR = BASE_DIR / "sql" / "migrations"
ALEMBIC_VERSIONS = BASE_DIR / "alembic" / "versions"


def delete_last_migration():
    # Находим последний runner
    runners = sorted(ALEMBIC_VERSIONS.glob("run_sql_*.py"))
    if not runners:
        print(" Нет миграций для удаления.")
        return
    
    last_runner = runners[-1]
    revision = last_runner.stem.split("_")[1]
    
    # Ищем соответствующие SQL-файлы
    sql_files = list(SQL_DIR.glob(f"{revision}_*.sql"))
    
    files_to_delete = [last_runner] + sql_files
    
    print(f"⚠️  Будут удалены следующие файлы:")
    for f in files_to_delete:
        print(f"   - {f.relative_to(BASE_DIR)}")
    
    confirm = input("\nУдалить? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Отмена.")
        return
    
    for f in files_to_delete:
        f.unlink()
        print(f"Удалено: {f.relative_to(BASE_DIR)}")
    
    print("\nМиграция удалена.")
    print(" Если следующая миграция ссылалась на эту через down_revision — обнови её!")


if __name__ == "__main__":
    delete_last_migration()