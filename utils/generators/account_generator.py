import requests
import json
import time
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import inquirer
from faker import Faker
import tempfile
import os
import base64

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    print(ansi + text + RESET)

class CaptchaSolver:
    def __init__(self, api_key, service="2captcha"):
        self.api_key = api_key
        self.service = service.lower()
        self.session = requests.Session()
        
        self.services = {
            "2captcha": {
                "submit": "http://2captcha.com/in.php",
                "result": "http://2captcha.com/res.php"
            },
            "anticaptcha": {
                "submit": "https://api.anti-captcha.com/createTask",
                "result": "https://api.anti-captcha.com/getTaskResult"
            },
            "capmonster": {
                "submit": "https://api.capmonster.cloud/createTask",
                "result": "https://api.capmonster.cloud/getTaskResult"
            },
            "capsolver": {
                "submit": "https://api.capsolver.com/createTask",
                "result": "https://api.capsolver.com/getTaskResult"
            }
        }
    
    def solve_hcaptcha(self, site_key=None, page_url="https://discord.com/register", proxy=None):
        if not site_key:
            site_key = "a9b5fb07-92ff-493f-86fe-352a2803b3df"
        
        pretty_print(f"Solving Discord hCaptcha with {self.service.upper()}...", (255,128,0))
        pretty_print(f"Site Key: {site_key}", (255,255,0))
        
        if self.service == "2captcha":
            return self._solve_2captcha_hcaptcha(site_key, page_url, proxy)
        elif self.service == "anticaptcha":
            return self._solve_anticaptcha_hcaptcha(site_key, page_url, proxy)
        elif self.service == "capmonster":
            return self._solve_capmonster_hcaptcha(site_key, page_url, proxy)
        elif self.service == "capsolver":
            return self._solve_capsolver_hcaptcha(site_key, page_url, proxy)
        else:
            pretty_print("Unsupported CAPTCHA service!", (255,0,0))
            return None
    
    def _solve_2captcha_hcaptcha(self, site_key, page_url, proxy=None):
        try:
            submit_data = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'sitekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
            
            if proxy:
                submit_data.update({
                    'proxy': proxy,
                    'proxytype': 'HTTP'
                })
            
            response = self.session.post(self.services["2captcha"]["submit"], data=submit_data)
            result = response.json()
            
            if result['status'] != 1:
                pretty_print(f"CAPTCHA submit failed: {result.get('error_text', 'Unknown error')}", (255,0,0))
                return None
            
            captcha_id = result['request']
            pretty_print(f"CAPTCHA submitted, ID: {captcha_id}", (0,255,0))
            
            for attempt in range(60):
                time.sleep(5)
                
                result_data = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                
                response = self.session.get(self.services["2captcha"]["result"], params=result_data)
                result = response.json()
                
                if result['status'] == 1:
                    pretty_print("CAPTCHA solved successfully!", (0,255,0))
                    return result['request']
                elif result['request'] == 'CAPCHA_NOT_READY':
                    pretty_print(f"Waiting for solution... ({attempt + 1}/60)", (255,255,0))
                    continue
                else:
                    pretty_print(f"CAPTCHA solve failed: {result.get('error_text', 'Unknown error')}", (255,0,0))
                    return None
            
            pretty_print("CAPTCHA solve timeout!", (255,0,0))
            return None
            
        except Exception as e:
            pretty_print(f"CAPTCHA solve error: {str(e)}", (255,0,0))
            return None
    
    def _solve_capmonster_hcaptcha(self, site_key, page_url, proxy=None):
        try:
            task_data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": page_url,
                    "websiteKey": site_key
                }
            }
            
            if proxy:
                task_data["task"]["type"] = "HCaptchaTask"
                proxy_parts = proxy.split(':')
                task_data["task"].update({
                    "proxyType": "http",
                    "proxyAddress": proxy_parts[0],
                    "proxyPort": int(proxy_parts[1])
                })
            
            response = self.session.post(self.services["capmonster"]["submit"], json=task_data)
            result = response.json()
            
            if result.get('errorId') != 0:
                pretty_print(f"CAPTCHA submit failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                return None
            
            task_id = result['taskId']
            pretty_print(f"CAPTCHA submitted, ID: {task_id}", (0,255,0))
            
            for attempt in range(60):
                time.sleep(5)
                
                result_data = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                
                response = self.session.post(self.services["capmonster"]["result"], json=result_data)
                result = response.json()
                
                if result.get('status') == 'ready':
                    pretty_print("CAPTCHA solved successfully!", (0,255,0))
                    return result['solution']['gRecaptchaResponse']
                elif result.get('status') == 'processing':
                    pretty_print(f"Waiting for solution... ({attempt + 1}/60)", (255,255,0))
                    continue
                else:
                    pretty_print(f"CAPTCHA solve failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                    return None
            
            pretty_print("CAPTCHA solve timeout!", (255,0,0))
            return None
            
        except Exception as e:
            pretty_print(f"CAPTCHA solve error: {str(e)}", (255,0,0))
            return None
    
    def _solve_capsolver_hcaptcha(self, site_key, page_url, proxy=None):
        try:
            task_data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "HCaptchaTaskProxyLess",
                    "websiteURL": page_url,
                    "websiteKey": site_key
                }
            }
            
            if proxy:
                task_data["task"]["type"] = "HCaptchaTask"
                proxy_parts = proxy.split(':')
                task_data["task"].update({
                    "proxyType": "http",
                    "proxyAddress": proxy_parts[0],
                    "proxyPort": int(proxy_parts[1])
                })
            
            response = self.session.post(self.services["capsolver"]["submit"], json=task_data)
            result = response.json()
            
            if result.get('errorId') != 0:
                pretty_print(f"CAPTCHA submit failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                return None
            
            task_id = result['taskId']
            pretty_print(f"CAPTCHA submitted, ID: {task_id}", (0,255,0))
            
            for attempt in range(60):
                time.sleep(5)
                
                result_data = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                
                response = self.session.post(self.services["capsolver"]["result"], json=result_data)
                result = response.json()
                
                if result.get('status') == 'ready':
                    pretty_print("CAPTCHA solved successfully!", (0,255,0))
                    return result['solution']['gRecaptchaResponse']
                elif result.get('status') == 'processing':
                    pretty_print(f"Waiting for solution... ({attempt + 1}/60)", (255,255,0))
                    continue
                else:
                    pretty_print(f"CAPTCHA solve failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                    return None
            
            pretty_print("CAPTCHA solve timeout!", (255,0,0))
            return None
            
        except Exception as e:
            pretty_print(f"CAPTCHA solve error: {str(e)}", (255,0,0))
            return None

    def _solve_anticaptcha_hcaptcha(self, site_key, page_url, proxy=None):
        try:
            task_data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": page_url,
                    "websiteKey": site_key
                }
            }
            
            if proxy:
                task_data["task"]["type"] = "HCaptchaTask"
                proxy_parts = proxy.split(':')
                task_data["task"].update({
                    "proxyType": "http",
                    "proxyAddress": proxy_parts[0],
                    "proxyPort": int(proxy_parts[1])
                })
            
            response = self.session.post(self.services["anticaptcha"]["submit"], json=task_data)
            result = response.json()
            
            if result.get('errorId') != 0:
                pretty_print(f"CAPTCHA submit failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                return None
            
            task_id = result['taskId']
            pretty_print(f"CAPTCHA submitted, ID: {task_id}", (0,255,0))
            
            for attempt in range(60):
                time.sleep(5)
                
                result_data = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                
                response = self.session.post(self.services["anticaptcha"]["result"], json=result_data)
                result = response.json()
                
                if result.get('status') == 'ready':
                    pretty_print("CAPTCHA solved successfully!", (0,255,0))
                    return result['solution']['gRecaptchaResponse']
                elif result.get('status') == 'processing':
                    pretty_print(f"Waiting for solution... ({attempt + 1}/60)", (255,255,0))
                    continue
                else:
                    pretty_print(f"CAPTCHA solve failed: {result.get('errorDescription', 'Unknown error')}", (255,0,0))
                    return None
            
            pretty_print("CAPTCHA solve timeout!", (255,0,0))
            return None
            
        except Exception as e:
            pretty_print(f"CAPTCHA solve error: {str(e)}", (255,0,0))
            return None

class EmailProvider:
    def __init__(self, provider="tempmail"):
        self.provider = provider.lower()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_temp_email(self):
        if self.provider == "tempmail":
            return self._get_tempmail_email()
        elif self.provider == "guerrillamail":
            return self._get_guerrillamail_email()
        elif self.provider == "10minutemail":
            return self._get_10minutemail_email()
        else:
            return self._generate_random_email()
    
    def _get_tempmail_email(self):
        try:
            response = self.session.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    return emails[0], "1secmail"
        except Exception:
            pass
        return self._generate_random_email()
    
    def _get_guerrillamail_email(self):
        try:
            response = self.session.get("https://www.guerrillamail.com/ajax.php?f=get_email_address")
            if response.status_code == 200:
                data = response.json()
                return data.get('email_addr'), "guerrillamail"
        except Exception:
            pass
        return self._generate_random_email()
    
    def _get_10minutemail_email(self):
        try:
            response = self.session.get("https://10minutemail.com/10MinuteMail/index.html")
            if response.status_code == 200:
                import re
                email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', response.text)
                if email_match:
                    return email_match.group(1), "10minutemail"
        except Exception:
            pass
        return self._generate_random_email()
    
    def _generate_random_email(self):
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
        domain = random.choice(domains)
        return f"{username}@{domain}", "generated"
    
    def check_inbox(self, email, provider_type):
        if provider_type == "1secmail":
            return self._check_1secmail_inbox(email)
        elif provider_type == "guerrillamail":
            return self._check_guerrillamail_inbox(email)
        else:
            return []
    
    def _check_1secmail_inbox(self, email):
        try:
            login, domain = email.split('@')
            response = self.session.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return []

class DiscordAccountGenerator:
    def __init__(self, captcha_solver=None, email_provider=None):
        self.captcha_solver = captcha_solver
        self.email_provider = email_provider or EmailProvider()
        self.faker = Faker()
        self.session = requests.Session()
        
        self.register_url = "https://discord.com/api/v9/auth/register"
        self.verify_url = "https://discord.com/api/v9/auth/verify"
        self.phone_url = "https://discord.com/api/v9/users/@me/phone"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'America/New_York',
            'X-Super-Properties': self._generate_super_properties(),
        }
        
        self.session.headers.update(self.headers)
    
    def _generate_ultra_unique_username(self):
        import uuid
        import hashlib
        
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        timestamp = str(int(time.time()))[-8:]
        random_chars = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        
        prefixes = ['user', 'discord', 'gamer', 'pro', 'elite', 'cyber', 'neo', 'alpha', 'beta', 'omega']
        suffixes = ['2024', '2025', 'x', 'pro', 'gaming', 'official', 'real', 'new', 'fresh', 'cool']
        
        ultra_styles = [
            f"{random.choice(prefixes)}{unique_id}",
            f"{random.choice(prefixes)}{timestamp}",
            f"{random_chars}{random.randint(1000, 9999)}",
            f"u{unique_id[:6]}{random.randint(10, 99)}",
            f"{random.choice(prefixes)}{random_chars}",
            f"discord{unique_id[:6]}",
            f"{random_chars}{random.choice(suffixes)}",
            f"user{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
            f"{random.choice(prefixes)}__{unique_id[:6]}",
            f"gen{timestamp}{random.randint(10, 99)}"
        ]
        
        username = random.choice(ultra_styles)
        return username[:32] if len(username) > 32 else username
    
    def _generate_super_properties(self):
        try:
            import base64
            
            super_props = {
                "os": "Windows",
                "browser": "Chrome",
                "device": "",
                "system_locale": "en-US",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "browser_version": "120.0.0.0",
                "os_version": "10",
                "referrer": "",
                "referring_domain": "",
                "referrer_current": "",
                "referring_domain_current": "",
                "release_channel": "stable",
                "client_build_number": random.randint(200000, 250000),
                "client_event_source": None
            }
            
            props_json = json.dumps(super_props, separators=(',', ':'))
            props_b64 = base64.b64encode(props_json.encode()).decode()
            
            return props_b64
            
        except Exception:
            return "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIzMDAwMCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    
    def get_discord_fingerprint(self):
        try:
            timestamp = str(random.randint(1300000000000000000, 1500000000000000000))
            
            import base64
            import hashlib
            import uuid
            
            unique_data = f"{uuid.uuid4()}{time.time()}{random.randint(1000000, 9999999)}"
            hash_bytes = hashlib.sha256(unique_data.encode()).digest()
            
            hash_b64 = base64.b64encode(hash_bytes).decode()[:26]
            hash_clean = hash_b64.replace('+', '-').replace('/', '_').rstrip('=')
            
            fingerprint = f"{timestamp}.{hash_clean}"
            
            pretty_print(f"Generated realistic fingerprint: {fingerprint}", (0,255,128))
            return fingerprint
            
        except Exception as e:
            pretty_print(f"Failed to generate fingerprint: {str(e)}", (255,0,0))
            
            timestamp = str(random.randint(1300000000000000000, 1500000000000000000))
            fallback_hash = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_', k=26))
            return f"{timestamp}.{fallback_hash}"
    
    def get_discord_cookies(self):
        try:
            response = self.session.get("https://discord.com/register")
            if response.status_code == 200:
                cookies = {}
                for cookie in self.session.cookies:
                    cookies[cookie.name] = cookie.value
                return cookies
        except Exception as e:
            pretty_print(f"Failed to get Discord cookies: {str(e)}", (255,0,0))
        return {}
    
    def generate_user_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        
        timestamp = str(int(time.time()))[-6:]
        random_suffix = random.randint(1000, 99999)
        
        username_styles = [
            f"{first_name.lower()}{last_name.lower()}{timestamp}",
            f"{first_name.lower()}_{random_suffix}",
            f"{first_name.lower()}{random.randint(10000, 99999)}",
            f"{last_name.lower()}{random.randint(1000, 9999)}",
            f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}",
            f"user{timestamp}{random.randint(10, 99)}",
            f"{first_name.lower()}__{random_suffix}",
            f"{first_name[:3].lower()}{last_name[:3].lower()}{timestamp}",
            f"discord{random.randint(100000, 999999)}",
            f"{first_name.lower()}.{last_name.lower()}.{random.randint(10, 99)}"
        ]
        
        username = random.choice(username_styles)
        
        if len(username) > 32:
            username = username[:32]
        
        password = self.faker.password(length=random.randint(12, 20), special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        email, email_provider = self.email_provider.get_temp_email()
        
        birth_date = self.faker.date_of_birth(minimum_age=18, maximum_age=50)
        
        return {
            'username': username,
            'password': password,
            'email': email,
            'email_provider': email_provider,
            'global_name': f"{first_name} {last_name}",
            'date_of_birth': birth_date.strftime('%Y-%m-%d'),
            'first_name': first_name,
            'last_name': last_name
        }
    
    def create_account(self, user_data, proxy=None):
        pretty_print(f"Creating account for {user_data['username']}...", (255,128,0))
        
        try:
            cookies = self.get_discord_cookies()
            fingerprint = self.get_discord_fingerprint()
            
            register_data = {
                'username': user_data['username'],
                'password': user_data['password'],
                'email': user_data['email'],
                'global_name': user_data['global_name'],
                'date_of_birth': user_data['date_of_birth'],
                'fingerprint': fingerprint,
                'consent': True,
                'gift_code_sku_id': None,
                'invite': None,
                'promotional_email_opt_in': False
            }
            
            proxies = None
            if proxy:
                proxies = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            
            response = self.session.post(
                self.register_url,
                json=register_data,
                proxies=proxies,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                token = result.get('token')
                if token:
                    pretty_print(f"Account created successfully! Token: {token[:20]}...", (0,255,0))
                    return {
                        'success': True,
                        'token': token,
                        'user_data': user_data,
                        'needs_verification': False
                    }
            
            elif response.status_code == 400:
                error_data = response.json()
                pretty_print(f"Registration error details: {error_data}", (255,255,0))
                
                if 'captcha_key' in error_data or 'captcha_sitekey' in error_data:
                    pretty_print("CAPTCHA required, solving...", (255,255,0))
                    
                    if not self.captcha_solver:
                        pretty_print("No CAPTCHA solver configured!", (255,0,0))
                        return {'success': False, 'error': 'CAPTCHA required but no solver configured'}
                    
                    site_key = None
                    if 'captcha_sitekey' in error_data:
                        site_key = error_data['captcha_sitekey'][0]
                    elif 'captcha_key' in error_data:
                        site_key = "a9b5fb07-92ff-493f-86fe-352a2803b3df"
                    
                    captcha_solution = self.captcha_solver.solve_hcaptcha(
                        site_key=site_key,
                        page_url="https://discord.com/register",
                        proxy=proxy
                    )
                    
                    if not captcha_solution:
                        return {'success': False, 'error': 'CAPTCHA solve failed'}
                    
                    register_data['captcha_key'] = captcha_solution
                    
                    pretty_print("Retrying registration with CAPTCHA solution...", (255,255,0))
                    
                    response = self.session.post(
                        self.register_url,
                        json=register_data,
                        proxies=proxies,
                        timeout=30
                    )
                    
                    if response.status_code == 201:
                        result = response.json()
                        token = result.get('token')
                        if token:
                            pretty_print(f"Account created with CAPTCHA! Token: {token[:20]}...", (0,255,0))
                            return {
                                'success': True,
                                'token': token,
                                'user_data': user_data,
                                'needs_verification': False
                            }
                
                errors = error_data.get('errors', {})
                
                if 'username' in errors and any('USERNAME_ALREADY_TAKEN' in str(err) for err in errors['username'].get('_errors', [])):
                    pretty_print("Username taken, generating new one...", (255,255,0))
                    
                    for retry in range(3):
                        if retry >= 1:
                            ultra_username = self._generate_ultra_unique_username()
                            new_user_data = user_data.copy()
                            new_user_data['username'] = ultra_username
                            new_user_data['global_name'] = f"User {ultra_username}"
                        else:
                            new_user_data = self.generate_user_data()
                            new_user_data['email'] = user_data['email']
                            new_user_data['email_provider'] = user_data['email_provider']
                            new_user_data['password'] = user_data['password']
                        
                        pretty_print(f"Retry {retry + 1}/3 with username: {new_user_data['username']}", (255,255,0))
                        
                        register_data['username'] = new_user_data['username']
                        register_data['global_name'] = new_user_data['global_name']
                        
                        response = self.session.post(
                            self.register_url,
                            json=register_data,
                            proxies=proxies,
                            timeout=30
                        )
                        
                        if response.status_code == 201:
                            result = response.json()
                            token = result.get('token')
                            if token:
                                pretty_print(f"Account created with retry! Token: {token[:20]}...", (0,255,0))
                                return {
                                    'success': True,
                                    'token': token,
                                    'user_data': new_user_data,
                                    'needs_verification': False
                                }
                        elif response.status_code == 400:
                            retry_error = response.json()
                            if 'username' in retry_error.get('errors', {}) and any('USERNAME_ALREADY_TAKEN' in str(err) for err in retry_error.get('errors', {}).get('username', {}).get('_errors', [])):
                                continue
                            else:
                                break
                        else:
                            break
                    
                    pretty_print("All username retries failed!", (255,0,0))
                
                error_msg = str(errors)
                pretty_print(f"Registration failed: {error_msg}", (255,0,0))
                return {'success': False, 'error': error_msg}
            
            else:
                pretty_print(f"Registration failed with status {response.status_code}", (255,0,0))
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            pretty_print(f"Account creation error: {str(e)}", (255,0,0))
            return {'success': False, 'error': str(e)}
    
    def verify_email(self, token, email, email_provider):
        pretty_print(f"Checking for verification email...", (255,128,0))
        
        for attempt in range(30):
            time.sleep(10)
            
            messages = self.email_provider.check_inbox(email, email_provider)
            
            for message in messages:
                if 'discord' in message.get('subject', '').lower():
                    pretty_print("Verification email found!", (0,255,0))
                    return True
            
            pretty_print(f"Waiting for verification email... ({attempt + 1}/30)", (255,255,0))
        
        pretty_print("Verification email timeout!", (255,0,0))
        return False
    
    def add_phone_number(self, token, phone_number=None):
        if not phone_number:
            phone_number = f"+1{random.randint(2000000000, 9999999999)}"
        
        pretty_print(f"Adding phone number: {phone_number}", (255,128,0))
        
        try:
            headers = self.headers.copy()
            headers['Authorization'] = token
            
            phone_data = {
                'phone': phone_number,
                'change_phone_reason': 'user_action_required'
            }
            
            response = self.session.post(
                self.phone_url,
                json=phone_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 204:
                pretty_print("Phone number added successfully!", (0,255,0))
                return True
            elif response.status_code == 400:
                error_data = response.json()
                pretty_print(f"Phone number failed: {error_data}", (255,0,0))
                return False
            else:
                pretty_print(f"Phone number failed with status {response.status_code}", (255,0,0))
                return False
                
        except Exception as e:
            pretty_print(f"Phone number error: {str(e)}", (255,0,0))
            return False

def save_accounts(accounts, filename="generated_accounts.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== GENERATED DISCORD ACCOUNTS ===\n\n")
            for i, account in enumerate(accounts, 1):
                if account['success']:
                    f.write(f"Account #{i}:\n")
                    f.write(f"Username: {account['user_data']['username']}\n")
                    f.write(f"Email: {account['user_data']['email']}\n")
                    f.write(f"Password: {account['user_data']['password']}\n")
                    f.write(f"Token: {account['token']}\n")
                    f.write(f"Global Name: {account['user_data']['global_name']}\n")
                    f.write(f"Birth Date: {account['user_data']['date_of_birth']}\n")
                    f.write("-" * 50 + "\n\n")
        
        pretty_print(f"Accounts saved to {filename}", (0,255,0))
        return True
    except Exception as e:
        pretty_print(f"Failed to save accounts: {str(e)}", (255,0,0))
        return False

def run_account_generator():
    pretty_print("DISCORD ACCOUNT GENERATOR", (255,64,64))
    pretty_print("=" * 50, (255,64,64))
    
    questions = [
        inquirer.Text('count', message="How many accounts to generate?", default="5"),
        inquirer.List('captcha_service',
                     message="Select CAPTCHA service:",
                     choices=['2captcha', 'anticaptcha', 'capmonster', 'capsolver', 'none']),
        inquirer.List('email_provider',
                     message="Select email provider:",
                     choices=['tempmail', 'guerrillamail', '10minutemail', 'random']),
        inquirer.Confirm('use_proxy', message="Use proxy rotation?", default=False),
        inquirer.Confirm('verify_emails', message="Attempt email verification?", default=False),
        inquirer.Confirm('add_phone', message="Add phone numbers to accounts?", default=False),
    ]
    
    answers = inquirer.prompt(questions)
    if not answers:
        return
    
    try:
        count = int(answers['count'])
    except ValueError:
        pretty_print("Invalid count!", (255,0,0))
        return
    
    captcha_solver = None
    if answers['captcha_service'] != 'none':
        api_key = input(f"Enter {answers['captcha_service'].upper()} API key: ").strip()
        if api_key:
            captcha_solver = CaptchaSolver(api_key, answers['captcha_service'])
        else:
            pretty_print("No API key provided!", (255,0,0))
            return
    
    email_provider = EmailProvider(answers['email_provider'])
    
    proxies = []
    if answers['use_proxy']:
        proxy_file = input("Enter proxy file path (format: ip:port): ").strip()
        if proxy_file and os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                pretty_print(f"Loaded {len(proxies)} proxies", (0,255,0))
            except Exception as e:
                pretty_print(f"Failed to load proxies: {str(e)}", (255,0,0))
    
    generator = DiscordAccountGenerator(captcha_solver, email_provider)
    generated_accounts = []
    
    pretty_print(f"Starting generation of {count} accounts...", (255,128,0))
    
    def generate_single_account(index):
        try:
            proxy = random.choice(proxies) if proxies else None
            user_data = generator.generate_user_data()
            
            pretty_print(f"[{index + 1}/{count}] Generating: {user_data['username']}", (255,255,0))
            
            result = generator.create_account(user_data, proxy)
            
            if result['success']:
                if answers['verify_emails']:
                    generator.verify_email(
                        result['token'],
                        user_data['email'],
                        user_data['email_provider']
                    )
                
                if answers['add_phone']:
                    generator.add_phone_number(result['token'])
            
            return result
            
        except Exception as e:
            pretty_print(f"Error generating account {index + 1}: {str(e)}", (255,0,0))
            return {'success': False, 'error': str(e)}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(generate_single_account, i) for i in range(count)]
        
        for future in futures:
            result = future.result()
            generated_accounts.append(result)
            
            if result['success']:
                pretty_print(f"Account generated successfully!", (0,255,0))
            else:
                pretty_print(f"Account generation failed: {result.get('error', 'Unknown error')}", (255,0,0))
    
    successful = sum(1 for acc in generated_accounts if acc['success'])
    failed = count - successful
    
    pretty_print("=" * 50, (255,64,64))
    pretty_print(f"GENERATION COMPLETE", (255,64,64))
    pretty_print(f"Successful: {successful}", (0,255,0))
    pretty_print(f"Failed: {failed}", (255,0,0))
    pretty_print(f"Success Rate: {(successful/count)*100:.1f}%", (255,255,0))
    
    if successful > 0:
        save_accounts(generated_accounts)
    
    return generated_accounts

if __name__ == "__main__":
    run_account_generator() 