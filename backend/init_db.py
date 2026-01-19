import sys
sys.path.append('.')

from app.database import init_db

if __name__ == '__main__':
    print("Создание таблиц базы данных...")
    init_db()
    print("Готово!")

