## improved some shit..
import requests
import json
import time
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import inquirer
from faker import Faker
import tempfile
import os
import base64
import hashlib
import uuid
from typing import Optional, Dict, List, Tuple, Any
import logging
from dataclasses import dataclass
from enum import Enum

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 128, 0)
    BLUE = (0, 128, 255)
    PURPLE = (128, 0, 255)
    CYAN = (0, 255, 255)

def rgb(r: int, g: int, b: int) -> str:
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text: str, color: Tuple[int, int, int] = Color.RED) -> None:
    ansi = rgb(*color)
    print(ansi + text + RESET)
    logger.info(text)

class ServiceType(Enum):
    TWOCAPTCHA = "2captcha"
    ANTICAPTCHA = "anticaptcha"
    CAPMONSTER = "capmonster"
    CAPSOLVER = "capsolver"

class EmailProviderType(Enum):
    TEMPMAIL = "tempmail"
    GUERRILLAMAIL = "guerrillamail"
    TENMINUTEMAIL = "10minutemail"
    RANDOM = "random"

@dataclass
class AccountData:
    username: str
    password: str
    email: str
    email_provider: str
    global_name: str
    date_of_birth: str
    first_name: str
    last_name: str

@dataclass
class GenerationResult:
    success: bool
    token: Optional[str] = None
    user_data: Optional[AccountData] = None
    error: Optional[str] = None
    needs_verification: bool = False

class CaptchaSolver:
    
    def __init__(self, api_key: str, service: str = "2captcha"):
        self.api_key = api_key
        self.service = ServiceType(service.lower())
        self.session = self._create_session()
        self.max_retries = 3
        self.timeout = 300

        self.services = {
            ServiceType.TWOCAPTCHA: {
                "submit": "http://2captcha.com/in.php",
                "result": "http://2captcha.com/res.php"
            },
            ServiceType.ANTICAPTCHA: {
                "submit": "https://api.anti-captcha.com/createTask",
                "result": "https://api.anti-captcha.com/getTaskResult"
            },
            ServiceType.CAPMONSTER: {
                "submit": "https://api.capmonster.cloud/createTask",
                "result": "https://api.capmonster.cloud/getTaskResult"
            },
            ServiceType.CAPSOLVER: {
                "submit": "https://api.capsolver.com/createTask",
                "result": "https://api.capsolver.com/getTaskResult"
            }
        }

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        return session

    def solve_hcaptcha(self, site_key: Optional[str] = None, 
                      page_url: str = "https://discord.com/register", 
                      proxy: Optional[str] = None) -> Optional[str]:
        if not site_key:
            site_key = "a9b5fb07-92ff-493f-86fe-352a2803b3df"

        pretty_print(f"Solving Discord hCAPTCHA with {self.service.value.upper()}...", Color.ORANGE)
        pretty_print(f"Site Key: {site_key}", Color.YELLOW)

        for attempt in range(self.max_retries):
            try:
                if self.service == ServiceType.TWOCAPTCHA:
                    return self._solve_2captcha_hcaptcha(site_key, page_url, proxy)
                elif self.service == ServiceType.ANTICAPTCHA:
                    return self._solve_anticaptcha_hcaptcha(site_key, page_url, proxy)
                elif self.service == ServiceType.CAPMONSTER:
                    return self._solve_capmonster_hcaptcha(site_key, page_url, proxy)
                elif self.service == ServiceType.CAPSOLVER:
                    return self._solve_capsolver_hcaptcha(site_key, page_url, proxy)
            except Exception as e:
                pretty_print(f"Attempt {attempt + 1} failed: {str(e)}", Color.RED)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                
        pretty_print("All CAPTCHA solve attempts failed!", Color.RED)
        return None

    def _solve_2captcha_hcaptcha(self, site_key: str, page_url: str, proxy: Optional[str]) -> Optional[str]:
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

            response = self.session.post(self.services[ServiceType.TWOCAPTCHA]["submit"], 
                                       data=submit_data, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result['status'] != 1:
                raise Exception(f"Submit failed: {result.get('error_text', 'Unknown error')}")

            captcha_id = result['request']
            pretty_print(f"CAPTCHA submitted, ID: {captcha_id}", Color.GREEN)

            return self._wait_for_2captcha_solution(captcha_id)

        except Exception as e:
            pretty_print(f"2captcha error: {str(e)}", Color.RED)
            return None

    def _wait_for_2captcha_solution(self, captcha_id: str) -> Optional[str]:
        start_time = time.time()
        
        while time.time() - start_time < self.timeout:
            try:
                result_data = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }

                response = self.session.get(self.services[ServiceType.TWOCAPTCHA]["result"], 
                                          params=result_data, timeout=30)
                response.raise_for_status()
                result = response.json()

                if result['status'] == 1:
                    pretty_print("CAPTCHA solved successfully!", Color.GREEN)
                    return result['request']
                elif result['request'] == 'CAPCHA_NOT_READY':
                    elapsed = int(time.time() - start_time)
                    pretty_print(f"Waiting for solution... ({elapsed}s/{self.timeout}s)", Color.YELLOW)
                    time.sleep(5)
                    continue
                else:
                    raise Exception(f"Solve failed: {result.get('error_text', 'Unknown error')}")

            except Exception as e:
                pretty_print(f"Polling error: {str(e)}", Color.RED)
                time.sleep(5)

        pretty_print("CAPTCHA solve timeout!", Color.RED)
        return None

    def _solve_anticaptcha_hcaptcha(self, site_key: str, page_url: str, proxy: Optional[str]) -> Optional[str]:
        return self._solve_task_based_captcha(ServiceType.ANTICAPTCHA, site_key, page_url, proxy)

    def _solve_capmonster_hcaptcha(self, site_key: str, page_url: str, proxy: Optional[str]) -> Optional[str]:
        return self._solve_task_based_captcha(ServiceType.CAPMONSTER, site_key, page_url, proxy)

    def _solve_capsolver_hcaptcha(self, site_key: str, page_url: str, proxy: Optional[str]) -> Optional[str]:
        return self._solve_task_based_captcha(ServiceType.CAPSOLVER, site_key, page_url, proxy)

    def _solve_task_based_captcha(self, service: ServiceType, site_key: str, 
                                 page_url: str, proxy: Optional[str]) -> Optional[str]:
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
                if len(proxy_parts) >= 2:
                    task_data["task"].update({
                        "proxyType": "http",
                        "proxyAddress": proxy_parts[0],
                        "proxyPort": int(proxy_parts[1])
                    })

            response = self.session.post(self.services[service]["submit"], 
                                       json=task_data, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result.get('errorId') != 0:
                raise Exception(f"Submit failed: {result.get('errorDescription', 'Unknown error')}")

            task_id = result['taskId']
            pretty_print(f"CAPTCHA submitted, ID: {task_id}", Color.GREEN)

            return self._wait_for_task_solution(service, task_id)

        except Exception as e:
            pretty_print(f"{service.value} error: {str(e)}", Color.RED)
            return None

    def _wait_for_task_solution(self, service: ServiceType, task_id: str) -> Optional[str]:
        start_time = time.time()
        
        while time.time() - start_time < self.timeout:
            try:
                result_data = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }

                response = self.session.post(self.services[service]["result"], 
                                           json=result_data, timeout=30)
                response.raise_for_status()
                result = response.json()

                if result.get('status') == 'ready':
                    pretty_print("CAPTCHA solved successfully!", Color.GREEN)
                    return result['solution']['gRecaptchaResponse']
                elif result.get('status') == 'processing':
                    elapsed = int(time.time() - start_time)
                    pretty_print(f"Waiting for solution... ({elapsed}s/{self.timeout}s)", Color.YELLOW)
                    time.sleep(5)
                    continue
                else:
                    raise Exception(f"Solve failed: {result.get('errorDescription', 'Unknown error')}")

            except Exception as e:
                pretty_print(f"Polling error: {str(e)}", Color.RED)
                time.sleep(5)

        pretty_print("CAPTCHA solve timeout!", Color.RED)
        return None

class EmailProvider:
    
    def __init__(self, provider: str = "tempmail"):
        self.provider = EmailProviderType(provider.lower())
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return session

    def get_temp_email(self) -> Tuple[str, str]:
        if self.provider == EmailProviderType.TEMPMAIL:
            return self._get_tempmail_email()
        elif self.provider == EmailProviderType.GUERRILLAMAIL:
            return self._get_guerrillamail_email()
        elif self.provider == EmailProviderType.TENMINUTEMAIL:
            return self._get_10minutemail_email()
        else:
            return self._generate_random_email()

    def _get_tempmail_email(self) -> Tuple[str, str]:
        try:
            response = self.session.get(
                "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
                timeout=10
            )
            response.raise_for_status()
            
            emails = response.json()
            if emails and isinstance(emails, list):
                return emails[0], "1secmail"
        except Exception as e:
            logger.warning(f"1secmail failed: {str(e)}")
        
        return self._generate_random_email()

    def _get_guerrillamail_email(self) -> Tuple[str, str]:
        try:
            response = self.session.get(
                "https://www.guerrillamail.com/ajax.php?f=get_email_address",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            email = data.get('email_addr')
            if email:
                return email, "guerrillamail"
        except Exception as e:
            logger.warning(f"GuerrillaMail failed: {str(e)}")
        
        return self._generate_random_email()

    def _get_10minutemail_email(self) -> Tuple[str, str]:
        try:
            response = self.session.get(
                "https://10minutemail.com/10MinuteMail/index.html",
                timeout=10
            )
            response.raise_for_status()
            
            import re
            email_match = re.search(
                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', 
                response.text
            )
            if email_match:
                return email_match.group(1), "10minutemail"
        except Exception as e:
            logger.warning(f"10MinuteMail failed: {str(e)}")
        
        return self._generate_random_email()

    def _generate_random_email(self) -> Tuple[str, str]:
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com"]
        username = ''.join(random.choices(
            string.ascii_lowercase + string.digits, 
            k=random.randint(8, 12)
        ))
        domain = random.choice(domains)
        return f"{username}@{domain}", "generated"

    def check_inbox(self, email: str, provider_type: str) -> List[Dict[str, Any]]:
        if provider_type == "1secmail":
            return self._check_1secmail_inbox(email)
        elif provider_type == "guerrillamail":
            return self._check_guerrillamail_inbox(email)
        return []

    def _check_1secmail_inbox(self, email: str) -> List[Dict[str, Any]]:
        try:
            login, domain = email.split('@')
            response = self.session.get(
                f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"1secmail inbox check failed: {str(e)}")
            return []

    def _check_guerrillamail_inbox(self, email: str) -> List[Dict[str, Any]]:
        return []

class DiscordAccountGenerator:
    
    def __init__(self, captcha_solver: Optional[CaptchaSolver] = None, 
                 email_provider: Optional[EmailProvider] = None):
        self.captcha_solver = captcha_solver
        self.email_provider = email_provider or EmailProvider()
        self.faker = Faker()
        self.session = self._create_session()
        
        self.register_url = "https://discord.com/api/v9/auth/register"
        self.verify_url = "https://discord.com/api/v9/auth/verify"
        self.phone_url = "https://discord.com/api/v9/users/@me/phone"

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        
        headers = {
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
        
        session.headers.update(headers)
        return session

    def _generate_super_properties(self) -> str:
        try:
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
            return base64.b64encode(props_json.encode()).decode()

        except Exception as e:
            logger.warning(f"Failed to generate super properties: {str(e)}")
            return "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIzMDAwMCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="

    def generate_fingerprint(self) -> str:
        try:
            timestamp = str(random.randint(1300000000000000000, 1500000000000000000))
            
            unique_data = f"{uuid.uuid4()}{time.time()}{random.randint(1000000, 9999999)}"
            hash_bytes = hashlib.sha256(unique_data.encode()).digest()
            
            hash_b64 = base64.b64encode(hash_bytes).decode()[:26]
            hash_clean = hash_b64.replace('+', '-').replace('/', '_').rstrip('=')
            
            fingerprint = f"{timestamp}.{hash_clean}"
            pretty_print(f"Generated fingerprint: {fingerprint}", Color.CYAN)
            return fingerprint

        except Exception as e:
            logger.warning(f"Failed to generate fingerprint: {str(e)}")
            timestamp = str(random.randint(1300000000000000000, 1500000000000000000))
            fallback_hash = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_', 
                k=26
            ))
            return f"{timestamp}.{fallback_hash}"

    def generate_unique_username(self) -> str:
        timestamp = str(int(time.time()))[-6:]
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        random_suffix = random.randint(1000, 99999)
        
        first_name = self.faker.first_name().lower()
        last_name = self.faker.last_name().lower()
        
        strategies = [
            f"{first_name}{last_name}{timestamp}",
            f"{first_name}_{random_suffix}",
            f"user{unique_id}",
            f"{first_name}{random.randint(10000, 99999)}",
            f"discord{timestamp}{random.randint(10, 99)}",
            f"{first_name}__{last_name}{random.randint(10, 99)}",
            f"gen{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
            f"{first_name}x{random_suffix}",
            f"u{unique_id[:6]}{random.randint(10, 99)}",
            f"{first_name}.{last_name}.{random.randint(10, 99)}"
        ]
        
        username = random.choice(strategies)
        return username[:32] if len(username) > 32 else username

    def generate_user_data(self) -> AccountData:
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        
        username = self.generate_unique_username()
        password = self.faker.password(
            length=random.randint(12, 20), 
            special_chars=True, 
            digits=True, 
            upper_case=True, 
            lower_case=True
        )
        
        email, email_provider = self.email_provider.get_temp_email()
        birth_date = self.faker.date_of_birth(minimum_age=18, maximum_age=50)
        
        return AccountData(
            username=username,
            password=password,
            email=email,
            email_provider=email_provider,
            global_name=f"{first_name} {last_name}",
            date_of_birth=birth_date.strftime('%Y-%m-%d'),
            first_name=first_name,
            last_name=last_name
        )

    def create_account(self, user_data: AccountData, proxy: Optional[str] = None) -> GenerationResult:
        pretty_print(f"Creating account for {user_data.username}...", Color.ORANGE)
        
        try:
            fingerprint = self.generate_fingerprint()
            
            register_data = {
                'username': user_data.username,
                'password': user_data.password,
                'email': user_data.email,
                'global_name': user_data.global_name,
                'date_of_birth': user_data.date_of_birth,
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
            
            return self._handle_registration_response(response, register_data, user_data, proxies)
            
        except Exception as e:
            error_msg = f"Account creation error: {str(e)}"
            pretty_print(error_msg, Color.RED)
            logger.error(error_msg)
            return GenerationResult(success=False, error=str(e))

    def _handle_registration_response(self, response: requests.Response, 
                                    register_data: Dict[str, Any], 
                                    user_data: AccountData, 
                                    proxies: Optional[Dict[str, str]]) -> GenerationResult:
        if response.status_code == 201:
            result = response.json()
            token = result.get('token')
            if token:
                pretty_print(f"Account created successfully! Token: {token[:20]}...", Color.GREEN)
                return GenerationResult(
                    success=True,
                    token=token,
                    user_data=user_data,
                    needs_verification=False
                )
        
        elif response.status_code == 400:
            error_data = response.json()
            pretty_print(f"Registration error: {error_data}", Color.YELLOW)
            
            if 'captcha_key' in error_data or 'captcha_sitekey' in error_data:
                return self._handle_captcha_requirement(error_data, register_data, user_data, proxies)
            
            if self._is_username_taken(error_data):
                return self._retry_with_new_username(register_data, user_data, proxies)
            
            error_msg = str(error_data.get('errors', error_data))
            return GenerationResult(success=False, error=error_msg)
        
        else:
            error_msg = f'HTTP {response.status_code}: {response.text[:200]}'
            pretty_print(error_msg, Color.RED)
            return GenerationResult(success=False, error=error_msg)

    def _handle_captcha_requirement(self, error_data: Dict[str, Any], 
                                  register_data: Dict[str, Any], 
                                  user_data: AccountData, 
                                  proxies: Optional[Dict[str, str]]) -> GenerationResult:
        pretty_print("CAPTCHA required, solving...", Color.YELLOW)
        
        if not self.captcha_solver:
            return GenerationResult(success=False, error='CAPTCHA required but no solver configured')
        
        site_key = error_data.get('captcha_sitekey', ["a9b5fb07-92ff-493f-86fe-352a2803b3df"])[0]
        proxy = proxies.get('http', '').replace('http://', '') if proxies else None
        
        captcha_solution = self.captcha_solver.solve_hcaptcha(
            site_key=site_key,
            page_url="https://discord.com/register",
            proxy=proxy
        )
        
        if not captcha_solution:
            return GenerationResult(success=False, error='CAPTCHA solve failed')
        
        register_data['captcha_key'] = captcha_solution
        pretty_print("Retrying registration with CAPTCHA solution...", Color.YELLOW)
        
        try:
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
                    pretty_print(f"Account created with CAPTCHA! Token: {token[:20]}...", Color.GREEN)
                    return GenerationResult(
                        success=True,
                        token=token,
                        user_data=user_data,
                        needs_verification=False
                    )
            
            error_data = response.json() if response.status_code == 400 else {}
            error_msg = str(error_data.get('errors', f'HTTP {response.status_code}'))
            return GenerationResult(success=False, error=error_msg)
            
        except Exception as e:
            return GenerationResult(success=False, error=f'CAPTCHA retry error: {str(e)}')

    def _is_username_taken(self, error_data: Dict[str, Any]) -> bool:
        errors = error_data.get('errors', {})
        username_errors = errors.get('username', {}).get('_errors', [])
        return any('USERNAME_ALREADY_TAKEN' in str(err) for err in username_errors)

    def _retry_with_new_username(self, register_data: Dict[str, Any], 
                                user_data: AccountData, 
                                proxies: Optional[Dict[str, str]]) -> GenerationResult:
        pretty_print("Username taken, trying alternatives...", Color.YELLOW)
        
        max_retries = 3
        for attempt in range(max_retries):
            new_username = self.generate_unique_username()
            register_data['username'] = new_username
            register_data['global_name'] = f"User {new_username}"
            
            pretty_print(f"Retry {attempt + 1}/{max_retries} with username: {new_username}", Color.YELLOW)
            
            try:
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
                        new_user_data = AccountData(
                            username=new_username,
                            password=user_data.password,
                            email=user_data.email,
                            email_provider=user_data.email_provider,
                            global_name=f"User {new_username}",
                            date_of_birth=user_data.date_of_birth,
                            first_name=user_data.first_name,
                            last_name=user_data.last_name
                        )
                        
                        pretty_print(f"Account created with retry! Token: {token[:20]}...", Color.GREEN)
                        return GenerationResult(
                            success=True,
                            token=token,
                            user_data=new_user_data,
                            needs_verification=False
                        )
                
                elif response.status_code == 400:
                    error_data = response.json()
                    if not self._is_username_taken(error_data):
                        break
                else:
                    break
                    
            except Exception as e:
                logger.warning(f"Username retry {attempt + 1} failed: {str(e)}")
                break
        
        return GenerationResult(success=False, error='All username retries failed')

def save_accounts(accounts: List[GenerationResult], filename: str = "generated_accounts.txt") -> bool:
    try:
        successful_accounts = [acc for acc in accounts if acc.success and acc.user_data]
        
        if not successful_accounts:
            pretty_print("No successful accounts to save", Color.YELLOW)
            return False
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== GENERATED DISCORD ACCOUNTS ===\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total successful: {len(successful_accounts)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, account in enumerate(successful_accounts, 1):
                user_data = account.user_data
                f.write(f"Account #{i}:\n")
                f.write(f"Username: {user_data.username}\n")
                f.write(f"Email: {user_data.email}\n")
                f.write(f"Password: {user_data.password}\n")
                f.write(f"Token: {account.token}\n")
                f.write(f"Global Name: {user_data.global_name}\n")
                f.write(f"Birth Date: {user_data.date_of_birth}\n")
                f.write(f"Email Provider: {user_data.email_provider}\n")
                f.write("-" * 50 + "\n\n")

        pretty_print(f"Successfully saved {len(successful_accounts)} accounts to {filename}", Color.GREEN)
        return True
        
    except Exception as e:
        error_msg = f"Failed to save accounts: {str(e)}"
        pretty_print(error_msg, Color.RED)
        logger.error(error_msg)
        return False

def load_proxies(proxy_file: str) -> List[str]:
    proxies = []
    
    if not os.path.exists(proxy_file):
        pretty_print(f"Proxy file not found: {proxy_file}", Color.RED)
        return proxies
    
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2 and parts[1].isdigit():
                        proxies.append(line)
                    else:
                        logger.warning(f"Invalid proxy format on line {line_num}: {line}")
        
        pretty_print(f"Loaded {len(proxies)} valid proxies", Color.GREEN)
        
    except Exception as e:
        error_msg = f"Failed to load proxies: {str(e)}"
        pretty_print(error_msg, Color.RED)
        logger.error(error_msg)
    
    return proxies

def generate_single_account(generator: DiscordAccountGenerator, 
                          index: int, total: int, 
                          proxies: List[str]) -> GenerationResult:
    try:
        proxy = random.choice(proxies) if proxies else None
        user_data = generator.generate_user_data()
        
        pretty_print(f"[{index + 1}/{total}] Generating: {user_data.username}", Color.YELLOW)
        
        result = generator.create_account(user_data, proxy)
        
        if result.success:
            pretty_print(f"[{index + 1}/{total}] Success: {user_data.username}", Color.GREEN)
        else:
            pretty_print(f"[{index + 1}/{total}] Failed: {result.error}", Color.RED)
        
        return result
        
    except Exception as e:
        error_msg = f"Error generating account {index + 1}: {str(e)}"
        pretty_print(error_msg, Color.RED)
        logger.error(error_msg)
        return GenerationResult(success=False, error=str(e))

def run_account_generator() -> List[GenerationResult]:
    pretty_print("DISCORD ACCOUNT GENERATOR v2.0", Color.RED)
    pretty_print("=" * 50, Color.RED)
    
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
        inquirer.Text('max_workers', message="Max concurrent workers (1-5)?", default="3"),
    ]

    answers = inquirer.prompt(questions)
    if not answers:
        return []

    try:
        count = int(answers['count'])
        max_workers = min(max(int(answers['max_workers']), 1), 5)
        if count <= 0:
            raise ValueError("Count must be positive")
    except ValueError as e:
        pretty_print(f"Invalid input: {str(e)}", Color.RED)
        return []

    captcha_solver = None
    if answers['captcha_service'] != 'none':
        api_key = input(f"Enter {answers['captcha_service'].upper()} API key: ").strip()
        if api_key:
            captcha_solver = CaptchaSolver(api_key, answers['captcha_service'])
        else:
            pretty_print("No API key provided!", Color.RED)
            return []

    email_provider = EmailProvider(answers['email_provider'])

    proxies = []
    if answers['use_proxy']:
        proxy_file = input("Enter proxy file path (format: ip:port): ").strip()
        if proxy_file:
            proxies = load_proxies(proxy_file)
            if not proxies:
                pretty_print("No valid proxies loaded, continuing without proxies", Color.YELLOW)

    generator = DiscordAccountGenerator(captcha_solver, email_provider)
    generated_accounts = []

    pretty_print(f"Starting generation of {count} accounts with {max_workers} workers...", Color.ORANGE)
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(generate_single_account, generator, i, count, proxies): i 
            for i in range(count)
        }
        
        for future in as_completed(future_to_index):
            result = future.result()
            generated_accounts.append(result)

    end_time = time.time()
    duration = end_time - start_time
    successful = sum(1 for acc in generated_accounts if acc.success)
    failed = count - successful

    pretty_print("=" * 50, Color.RED)
    pretty_print("GENERATION COMPLETE", Color.RED)
    pretty_print(f"Duration: {duration:.1f} seconds", Color.CYAN)
    pretty_print(f"Successful: {successful}", Color.GREEN)
    pretty_print(f"Failed: {failed}", Color.RED)
    pretty_print(f"Success Rate: {(successful/count)*100:.1f}%", Color.YELLOW)

    if successful > 0:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"discord_accounts_{timestamp}.txt"
        save_accounts(generated_accounts, filename)
    else:
        pretty_print("No accounts to save", Color.YELLOW)

    return generated_accounts

if __name__ == "__main__":
    try:
        run_account_generator()
    except KeyboardInterrupt:
        pretty_print("\nGeneration interrupted by user", Color.YELLOW)
    except Exception as e:
        pretty_print(f"Unexpected error: {str(e)}", Color.RED)
        logger.exception("Unexpected error in main")
