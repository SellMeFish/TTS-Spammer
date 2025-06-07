import webbrowser
import time
import os
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

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

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    line = center(text)
    print(ansi + line + '\033[0m')

def run_browser_login():
    """Browser Login Funktion"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("🌐 BROWSER LOGIN", (255, 128, 0))
    print()
    
    pretty_print("This will open Discord in your browser", (255, 255, 0))
    confirm = input(rgb(255, 32, 32) + center("Continue? (y/n): ") + '\033[0m')
    
    if confirm.lower() != 'y':
        pretty_print("❌ Cancelled!", (255, 0, 0))
        return
    
    try:
        webbrowser.open('https://discord.com/login')
        pretty_print("✅ Browser opened!", (0, 255, 0))
        pretty_print("Please login in your browser", (255, 255, 0))
    except Exception as e:
        pretty_print(f"❌ Error: {str(e)}", (255, 0, 0))
    
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m') 