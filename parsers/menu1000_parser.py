import json
import time
import random
import requests
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class Menu1000Parser:
    def __init__(self):
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.recipes = []
    
    def parse_recipe_details(self, item_data):
        url = item_data['url']
        try:
            response = requests.get(url, headers={'User-Agent': self.ua}, timeout=10)
            if response.status_code != 200:
                return item_data
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Полное описание
            desc_elem = soup.select_one('.description-text') or soup.select_one('.instructions')
            if desc_elem:
                item_data['description'] = desc_elem.text.strip()
            
            # Качественная картинка
            img_elem = soup.select_one('.main-photo img') or soup.select_one('.photo img')
            if img_elem:
                img_url = img_elem.get('src', '')
                if img_url and not img_url.startswith('http'):
                    item_data['image_url'] = "https:" + img_url
                elif img_url:
                    item_data['image_url'] = img_url
            
            # Сложность (попытка найти)
            difficulty = "Средне"
            info_params = soup.select('.info-param')
            for param in info_params:
                if 'Сложность' in param.text:
                    val = param.select_one('.value')
                    if val: difficulty = val.text.strip()
                    break
            item_data['difficulty'] = difficulty
            
            # Ингредиенты
            ing_elems = soup.select('.ingredient .name')
            if ing_elems:
                item_data['ingredients'] = ", ".join([ing.text.strip() for ing in ing_elems])
            
            return item_data
            
        except Exception as e:
            return item_data

    def parse_category(self, base_url, category_name, max_pages=5):
        print(f"Parsing 1000.menu: {category_name}...")
        
        for page in range(1, max_pages + 1):
            try:
                url = base_url if page == 1 else f"{base_url}/{page}"
                print(f"Fetching catalog {url}")
                
                response = requests.get(url, headers={'User-Agent': self.ua}, timeout=10)
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'lxml')
                items = soup.select('.cn-item')
                if not items:
                    break
                
                batch_items = []
                for item in items:
                    title_elem = item.select_one('a.h5')
                    if not title_elem: continue
                    
                    href = title_elem['href']
                    if not href.startswith('http'):
                        href = "https://1000.menu" + href
                    
                    time_elem = item.select_one('.level-right span')
                    
                    batch_items.append({
                        'source': '1000.menu',
                        'title': title_elem.text.strip(),
                        'category': category_name,
                        'cooking_time': time_elem.text.strip() if time_elem else "40 мин",
                        'difficulty': 'Средне', # Placeholder, updated in details
                        'description': '', 
                        'image_url': '',
                        'ingredients': '',
                        'url': href
                    })

                # Запускаем параллельный сбор деталей для батча (в 10 потоков)
                print(f"  Processing {len(batch_items)} items in parallel...")
                with ThreadPoolExecutor(max_workers=10) as executor:
                    results = list(executor.map(self.parse_recipe_details, batch_items))
                    self.recipes.extend(results)
                
                print(f"  Total recipes so far: {len(self.recipes)}")
                time.sleep(random.uniform(0.3, 0.7))
                
            except Exception as e:
                print(f"Page error: {e}")

    def save_to_json(self, filename='data/menu1000_data.json'):
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
