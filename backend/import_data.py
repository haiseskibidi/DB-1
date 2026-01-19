import sys
import os

# Add the parent directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db
from app.importer import run_import

if __name__ == '__main__':
    print("=" * 60)
    print("ИМПОРТ ДАННЫХ В БД")
    print("=" * 60)
    
    init_db()
    run_import()
    
    print("\n" + "=" * 60)
    print("ИМПОРТ ЗАВЕРШЕН!")
    print("=" * 60)