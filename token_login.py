import os
import sys
import json
import requests
import shutil
import time
import zipfile
import io
import platform
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess

RESET = '\033[0m'

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def center(text):
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

def pretty_print(text, color=(255,64,64), newline=True):
    ansi = rgb(*color)
    line = center(text)
    if newline:
        print(ansi + line + RESET)
    else:
        print(ansi + line + RESET, end='')

def loading_spinner():
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for frame in frames:
        sys.stdout.write(f'\r{rgb(192,0,0)}{center(f"Loading {frame}")}{RESET}')
        sys.stdout.flush()
        time.sleep(0.08)
    print()

def validate_token(token):
    """
    Validates Discord token and returns user info
    """
    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(
            "https://discord.com/api/v9/users/@me",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception:
        return None

def setup_chrome_driver():
    """
    Sets up ChromeDriver with incognito mode
    """
    try:
        pretty_print("Setting up Chrome...", (255, 64, 64))
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Add user agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Download and setup ChromeDriver
        pretty_print("Downloading ChromeDriver...", (255, 64, 64))
        service = Service(ChromeDriverManager().install())
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    except Exception as e:
        pretty_print(f"✗ Error setting up Chrome: {str(e)}", (255, 0, 0))
        return None

def login_with_token(token, debug=False):
    """
    Validates token, shows user info, and starts browser_login.py in a new terminal.
    """
    try:
        user_info = validate_token(token)
        if not user_info:
            pretty_print("✗ Invalid token!", (255, 0, 0))
            return False
        username = user_info.get("username", "Unknown")
        discriminator = user_info.get("discriminator", "0000")
        user_id = user_info.get("id", "Unknown")
        email = user_info.get("email", "Not available")
        phone = user_info.get("phone", "Not available")
        pretty_print("Token validated successfully!", (0, 255, 128))
        pretty_print("User Information:", (255, 64, 64))
        pretty_print(f"Username: {username}#{discriminator}", (255, 255, 255))
        pretty_print(f"User ID: {user_id}", (255, 255, 255))
        pretty_print(f"Email: {email}", (255, 255, 255))
        pretty_print(f"Phone: {phone}", (255, 255, 255))
        if debug:
            pretty_print("\nDebug Information:", (180, 180, 180))
            pretty_print(f"Token: {token}", (180, 180, 180))
        pretty_print("\nDo you want to login with this token?", (255, 64, 64))
        choice = input(rgb(255, 32, 32) + center("Proceed? (y/n): ") + RESET).lower()
        if choice == 'y':
            # Starte browser_login.py in neuem Terminal
            if platform.system() == "Windows":
                subprocess.Popen(
                    ['start', 'cmd', '/k', sys.executable, 'browser_login.py', token],
                    shell=True
                )
            else:
                subprocess.Popen(
                    ['x-terminal-emulator', '-e', f'{sys.executable} browser_login.py {token}']
                )
            pretty_print("✓ Injection! Token Injection started...", (0, 255, 128))
            time.sleep(10)
            pretty_print("✓ Login successful! Browser started in a new window.", (0, 255, 128))
            return True
        else:
            pretty_print("Login cancelled", (255, 64, 64))
            return False
    except Exception as e:
        pretty_print(f"✗ Error: {str(e)}", (255, 0, 0))
        return False

def main():
    print("\n" + "="*50)
    pretty_print("Discord Token Login", (255, 64, 64))
    print("="*50 + "\n")
    
    # Get token
    token = input(rgb(255, 32, 32) + center("Enter Discord Token: ") + RESET).strip()
    print(f"[DEBUG] Token entered: '{token}'")  # Debug-Ausgabe
    if not token:
        pretty_print("✗ No token provided!", (255, 0, 0))
        return
    
    # Debug mode
    debug = input(rgb(255, 32, 32) + center("Enable debug mode? (y/n): ") + RESET).lower() == 'y'
    
    # Start login process
    print("\n")
    login_with_token(token, debug)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        pretty_print("Program terminated.", (192, 0, 0))
        sys.exit(0) 