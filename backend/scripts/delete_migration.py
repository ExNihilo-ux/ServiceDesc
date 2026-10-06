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
SQL_UP_DIR = BASE_DIR / "sql" / "migrations"     # UP-скрипты
SQL_DOWN_DIR = BASE_DIR / "sql" / "rollbacks"    # DOWN-скрипты
ALEMBIC_VERSIONS = BASE_DIR / "alembic" / "versions"


def delete_last_migration():
    """Находит и удаляет последнюю неприменённую миграцию по номеру ревизии.
    
    Удаляет runner из alembic/versions/ и соответствующие SQL-файлы 
    из sql/migrations/ и sql/rollbacks/. Требует подтверждения пользователя.
    """
    # Находим последний runner по имени файла (run_sql_XXX.py)
    runners = sorted(ALEMBIC_VERSIONS.glob("run_sql_*.py"))
    if not runners:
        print("Нет миграций для удаления.")
        return
    
    last_runner = runners[-1]
    revision = last_runner.stem.split("_")[1]
    
    # Ищем UP и DOWN скрипты в разных папках
    up_files = list(SQL_UP_DIR.glob(f"{revision}_*.sql"))
    down_files = list(SQL_DOWN_DIR.glob(f"{revision}_*.down.sql"))
    
    files_to_delete = [last_runner] + up_files + down_files
    
    print(f" Будут удалены следующие файлы:")
    for f in files_to_delete:
        print(f"   - {f.relative_to(BASE_DIR)}")
    
    confirm = input("\nУдалить? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Отмена.")
        return
    
    for f in files_to_delete:
        f.unlink()
        print(f" Удалено: {f.relative_to(BASE_DIR)}")
    
    print("\nМиграция удалена.")
    print(" Если следующая миграция ссылалась на эту через down_revision — обнови её!")


if __name__ == "__main__":
    delete_last_migration()