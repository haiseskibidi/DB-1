import json
import time
import random
import requests
import os
from bs4 import BeautifulSoup

class Menu1000Parser:
    def __init__(self):
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.recipes = []
    
    def parse_category(self, base_url, category_name, max_pages=30):
        print(f"Parsing 1000.menu: {category_name}...")
        
        for page in range(1, max_pages + 1):
            try:
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}/{page}"
                    
                print(f"Fetching {url}")
                
                response = requests.get(url, headers={'User-Agent': self.ua}, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'lxml')
                
                items = soup.select('.cn-item')
                
                if not items:
                    print("No items found")
                    if page > 1:
                        break
                
                for item in items:
                    try:
                        title_elem = item.select_one('a.h5')
                        if not title_elem: 
                            continue
                        
                        title = title_elem.text.strip()
                        href = title_elem['href']
                        if not href.startswith('http'):
                            href = "https://1000.menu" + href
                        
                        desc_elem = item.select_one('.preview-text')
                        desc = desc_elem.text.strip() if desc_elem else ""
                        
                        time_elem = item.select_one('.level-right span')
                        time_val = time_elem.text.strip() if time_elem else "40 мин"
                        
                        ing_elem = item.select_one('.info.add_keywords')
                        ingredients = ing_elem.text.strip() if ing_elem else "См. на сайте"
                        
                        self.recipes.append({
                            'source': '1000.menu',
                            'title': title,
                            'category': category_name,
                            'cooking_time': time_val,
                            'difficulty': 'Сложно',
                            'description': desc,
                            'ingredients': ingredients,
                            'url': href
                        })
                    except Exception as e:
                        continue
                
                print(f"  Items so far: {len(self.recipes)}")
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Page error: {e}")

    def save_to_json(self, filename='../data/menu1000_data.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.recipes)} recipes to {filename}")

if __name__ == '__main__':
    parser = Menu1000Parser()
    categories = [
        ('https://1000.menu/catalog/salaty', 'Салаты'),
        ('https://1000.menu/catalog/zakuski', 'Закуски'),
        ('https://1000.menu/catalog/supy', 'Супы'),
        ('https://1000.menu/catalog/vypechka', 'Выпечка')
    ]
    
    for url, name in categories:
        parser.parse_category(url, name, max_pages=20)
        
    parser.save_to_json()