import os
import sys
import time
import json
import requests
import base64
import shutil

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

def switch_theme(token, theme="dark", debug=False):
    """
    Switches Discord theme
    theme: "dark" or "light"
    """
    try:
        theme_settings = {
            "dark": "agYIAhABGgA=",  # Dark Mode
            "light": "agYIARABGgA="  # Light Mode
        }
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        payload = {
            "settings": theme_settings[theme]
        }
        
        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings-proto/1",
            headers=headers,
            json=payload
        )
        
        if debug:
            pretty_print(f"Status Code: {response.status_code}", (180,180,180))
            if response.text:
                pretty_print(f"Response: {response.text}", (180,180,180))
        
        if response.status_code == 200:
            pretty_print(f"✓ Successfully switched to {theme} theme!", (0, 255, 128))
            return True
        else:
            pretty_print(f"✗ Failed to switch theme! Status: {response.status_code}", (255, 0, 0))
            if debug and response.text:
                pretty_print(f"Error: {response.text}", (255, 0, 0))
            return False
            
    except Exception as e:
        pretty_print(f"✗ Error: {str(e)}", (255, 0, 0))
        return False

def spam_theme(token, amount, interval, debug=False):
    """
    Spams between Light and Dark theme
    """
    if not token:
        pretty_print("✗ No token provided!", (255, 0, 0))
        return False
        
    pretty_print(f"Starting theme spam... ({amount} switches)", (255, 64, 64))
    pretty_print(f"Interval: {interval} seconds", (255, 64, 64))
    
    success_count = 0
    current_theme = "dark"
    
    for i in range(amount):
        pretty_print(f"Switch {i+1}/{amount}...", (255, 64, 64))
        
        if switch_theme(token, current_theme, debug):
            success_count += 1
            
        current_theme = "light" if current_theme == "dark" else "dark"
        
        if i < amount - 1:
            pretty_print(f"Waiting {interval} seconds...", (255, 64, 64))
            time.sleep(interval)
    
    pretty_print(f"Finished! {success_count}/{amount} theme switches successful", (0, 255, 128))
    return True

def main():
    print("\n" + "="*50)
    pretty_print("Discord Theme Spammer", (255, 64, 64))
    print("="*50 + "\n")
    
    token = input(rgb(255, 32, 32) + center("Enter Discord Token: ") + RESET).strip()
    if not token:
        pretty_print("✗ No token provided!", (255, 0, 0))
        return
        
    try:
        amount = int(input(rgb(255, 32, 32) + center("How many theme switches? ") + RESET))
        if amount <= 0:
            pretty_print("✗ Amount must be positive!", (255, 0, 0))
            return
    except ValueError:
        pretty_print("✗ Invalid amount!", (255, 0, 0))
        return
        
    try:
        interval = float(input(rgb(255, 32, 32) + center("Interval between switches (seconds): ") + RESET))
        if interval < 0:
            pretty_print("✗ Interval cannot be negative!", (255, 0, 0))
            return
    except ValueError:
        pretty_print("✗ Invalid interval!", (255, 0, 0))
        return
    
    debug = input(rgb(255, 32, 32) + center("Enable debug mode? (y/n): ") + RESET).lower() == 'y'
    
    print("\n")
    spam_theme(token, amount, interval, debug)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        pretty_print("Program terminated.", (192, 0, 0))
        sys.exit(0) 
