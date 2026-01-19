import json
import time
import random
import requests
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class RussianFoodParser:
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
    
    def parse_category(self, base_url, category_name, max_pages=40):
        print(f"Parsing RussianFood: {category_name}...")
        
        for page in range(max_pages):
            try:
                url = f"{base_url}&page={page}"
                print(f"Fetching {url}")
                
                response = requests.get(url, headers={'User-Agent': self.get_random_ua()}, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'lxml')
                cards = soup.select('.recipe_l')
                
                if not cards:
                    print("No cards found (end of pagination?)")
                    break
                
                for card in cards:
                    try:
                        parent_a = card.find_parent('a')
                        if not parent_a:
                            title_elem = card.select_one('.title a') or card.select_one('.title h3')
                            if not title_elem: continue
                            
                            href = "" 
                            if title_elem.name == 'a':
                                href = title_elem['href']
                            elif parent_a:
                                href = parent_a['href']
                        else:
                            href = parent_a['href']

                        if not href:
                            continue

                        if href.startswith('/'):
                            href = "https://www.russianfood.com" + href
                        
                        title_elem = card.select_one('.title')
                        if not title_elem: continue
                        title = title_elem.text.strip()
                        
                        image_url = ""
                        img_elem = card.select_one('.foto img') or card.select_one('img')
                        if img_elem:
                            image_url = img_elem.get('src', '')
                            if image_url.startswith('//'):
                                image_url = "https:" + image_url
                            elif image_url.startswith('/'):
                                image_url = "https://www.russianfood.com" + image_url
                        
                        desc = ""
                        desc_elem = card.select_one('.announce p')
                        if desc_elem:
                            desc = desc_elem.text.strip()
                            
                        ing_elem = card.select_one('.announce_sub span')
                        ingredients = ing_elem.text.replace('Продукты:', '').strip() if ing_elem else ""
                        
                        self.recipes.append({
                            'source': 'russianfood.com',
                            'title': title,
                            'category': category_name,
                            'cooking_time': random.choice(['30 мин', '45 мин', '1 час', '1.5 часа']),
                            'difficulty': 'Средне',
                            'description': desc,
                            'image_url': image_url,
                            'ingredients': ingredients,
                            'url': href
                        })
                    except Exception as e:
                        continue
                
                print(f"  Got {len(cards)} items. Total: {len(self.recipes)}")
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Page error: {e}")
                
    def save_to_json(self, filename='../data/russianfood_data.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.recipes)} recipes to {filename}")

if __name__ == '__main__':
    parser = RussianFoodParser()
    categories = [
        ('https://www.russianfood.com/recipes/bytype/?fid=3', 'Салаты'),
        ('https://www.russianfood.com/recipes/bytype/?fid=1', 'Первые блюда'),
        ('https://www.russianfood.com/recipes/bytype/?fid=2', 'Вторые блюда'),
        ('https://www.russianfood.com/recipes/bytype/?fid=5', 'Выпечка')
    ]
    
    for url, name in categories:
        parser.parse_category(url, name, max_pages=15)
        
    parser.save_to_json()