import os
import sys

try:
    print("=" * 60)
    print("Запуск парсеров")
    print("=" * 60)
    
    print("\nПарсинг Povarenok...")
    os.system(f"{sys.executable} povarenok_parser.py")

    print("\nПарсинг RussianFood...")
    os.system(f"{sys.executable} russianfood_parser.py")

    print("\nПарсинг 1000.menu...")
    os.system(f"{sys.executable} menu1000_parser.py")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Готово! Данные в ../data/")
print("=" * 60)