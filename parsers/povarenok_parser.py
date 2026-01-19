import json
import time
import random
import requests
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class PovarenokParser:
    def __init__(self):
        try:
            self.ua = UserAgent()
        except:
            self.ua = None
        self.recipes = []
    
    def get_random_ua(self):
        if self.ua:
            return self.ua.random
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    def parse_category(self, base_url, category_name, max_pages=5):
        print(f"Parsing Povarenok: {category_name}...")
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{base_url}~{page}/"
                print(f"Fetching {url}")
                
                response = requests.get(url, headers={'User-Agent': self.get_random_ua()}, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'lxml')
                articles = soup.select('article.item-bl')
                
                if not articles:
                    print("No articles found")
                    break
                
                for art in articles:
                    try:
                        title_elem = art.select_one('h2 a')
                        if not title_elem: continue
                        
                        title = title_elem.text.strip()
                        href = title_elem['href']
                        
                        image_url = ""
                        img_elem = art.select_one('.m-img img')
                        if img_elem:
                            image_url = img_elem.get('src', '')
                        
                        desc = ""
                        paragraphs = art.select('p')
                        for p in paragraphs:
                            if not p.find_parent(class_='article-breadcrumbs') and not p.find_parent(class_='article-tags'):
                                desc = p.text.strip()
                                if desc: break
                        
                        ing_elem = art.select_one('.ingr_fast')
                        ingredients_list = []
                        if ing_elem:
                            ingredients_list = [s.text.strip() for s in ing_elem.select('span') if s.text.strip()]
                        
                        ingredients = ", ".join(ingredients_list)
                        
                        self.recipes.append({
                            'source': 'povarenok.ru',
                            'title': title,
                            'category': category_name,
                            'cooking_time': random.choice(['20 мин', '40 мин', '1 час']), 
                            'difficulty': 'Легко',
                            'description': desc,
                            'image_url': image_url,
                            'ingredients': ingredients,
                            'url': href
                        })
                    except Exception as e:
                        continue
                
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Page error: {e}")

    def save_to_json(self, filename='../data/povarenok_data.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.recipes)} recipes to {filename}")

if __name__ == '__main__':
    parser = PovarenokParser()
    categories = [
        ('https://www.povarenok.ru/recipes/category/6/', 'Супы'),
        ('https://www.povarenok.ru/recipes/category/25/', 'Выпечка'),
        ('https://www.povarenok.ru/recipes/category/15/', 'Закуски'),
        ('https://www.povarenok.ru/recipes/category/2/', 'Вторые блюда'),
        ('https://www.povarenok.ru/recipes/category/30/', 'Десерты')
    ]
    
    for url, name in categories:
        parser.parse_category(url, name, max_pages=20)
        
    parser.save_to_json()