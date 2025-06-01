import os
import sys
import time
import json
import requests
import subprocess
from discord_webhook import DiscordWebhook
import inquirer
import shutil
from utils.spammer import spam_webhook, loading_spinner
from colorama import Fore, Style, init
from utils.update import main as run_updater
from utils.nitro_generator import run_nitro_generator
from utils.token_generator import run_token_generator

# Initialize colorama
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
                subprocess.call([sys.executable, 'update.py'])
            else:
                os.system(f'{sys.executable} update.py')
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

def show_webhook_box():
    box_color = rgb(0, 255, 0)
    text_color = rgb(255, 255, 255)
    url = "No webhook set"
    max_url_len = 35
    if len(url) > max_url_len:
        url = url[:15] + '...' + url[-15:]
    width = 50
    padding = (width - len(url)) // 2
    top = box_color + center("╔" + "═" * (width - 2) + "╗") + RESET
    url_line = box_color + center("║" + " " * padding + text_color + url + " " * (width - 2 - padding - len(url)) + box_color + "║") + RESET
    bot = box_color + center("╚" + "═" * (width - 2) + "╝") + RESET
    print(top)
    print(url_line)
    print(bot)

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


def print_banner(show_webhook=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    for idx, line in enumerate(BANNER):
        color = rgb(*RED_GRADIENT[idx % len(RED_GRADIENT)])
        print(color + center(line) + RESET)
    print()
    print(rgb(255,0,64) + center("=" * shutil.get_terminal_size().columns) + RESET)
    print(rgb(255,32,64) + center("Made by cyberseall") + RESET)
    print(rgb(255,0,64) + center("=" * shutil.get_terminal_size().columns) + RESET)
    print(rgb(255,64,64) + center("Discord AIO Tool 2025") + RESET)
    print()
    show_status()
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
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for frame in frames:
        sys.stdout.write(f'\r{rgb(192,0,0)}{center(f"Loading {frame}")}{RESET}')
        sys.stdout.flush()
        time.sleep(0.08)
    print()


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
        loading_spinner()
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

    from theme_spammer import spam_theme
    spam_theme(token, amount, interval, debug)

def ask_token(prompt="Enter Discord Token: "):
    empty_count = 0
    while True:
        token = clean_singleline_input_left(prompt)
        if token:
            return token
        empty_count += 1
        if empty_count >= 2:
            pretty_print("No token entered twice. Returning to main menu...", (255,64,64))
            return None
        pretty_print("No token entered! Please try again or press Ctrl+C to cancel.", (255,64,64))

def token_login_menu():
    print_banner()
    token = ask_token()
    debug = input(rgb(255,32,32) + "Enable debug mode? (y/n): " + RESET).lower() == 'y'
    from utils.token_login import login_with_token
    login_with_token(token, debug)

def server_cloner_menu():
    subprocess.run([sys.executable, 'utils/server_cloner.py'])

def webhook_deleter_menu():
    subprocess.run([sys.executable, 'utils/webhook_deleter.py'])

def main_menu():
    while True:
        print_banner(show_webhook=False)
        questions = [
            inquirer.List('choice',
                         message="Select a feature:",
                         choices=[
                             'Discord Webhook Spammer',
                             'Nitro Generator & Checker',
                             'Token Generator',
                             'Token Info',
                             'Token Login',
                             'Close All DMs',
                             'Unfriend All Friends',
                             'DM All Friends',
                             'Delete/Leave All Servers',
                             'Theme Spammer',
                             'Server Cloner',
                             'Webhook Deleter',
                             'Exit'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == 'Exit':
            print_banner()
            pretty_print("Goodbye! 👋", (255,32,32))
            break
        if answers['choice'] == 'Discord Webhook Spammer':
            webhook_spammer_menu()
        elif answers['choice'] == 'Nitro Generator & Checker':
            run_nitro_generator()
        elif answers['choice'] == 'Token Generator':
            run_token_generator()
        elif answers['choice'] == 'Token Info':
            token = ask_token()
            if token:
                from utils.token_info import display_token_info
                display_token_info(token)
        elif answers['choice'] == 'Token Login':
            token_login_menu()
        elif answers['choice'] == 'Close All DMs':
            token = ask_token()
            if token:
                from utils.close_dms import close_all_dms
                success, total = close_all_dms(token)
                pretty_print(f"Result: {success} of {total} DMs closed", (0,255,0))
        elif answers['choice'] == 'Unfriend All Friends':
            token = ask_token()
            if token:
                from utils.unfriend import unfriend_all
                success, total = unfriend_all(token)
                pretty_print(f"Result: {success} of {total} friends removed", (0,255,0))
        elif answers['choice'] == 'DM All Friends':
            token = ask_token()
            if token:
                message = clean_singleline_input_left("Enter message: ")
                if message:
                    from utils.dm_all import dm_all_friends
                    success, total = dm_all_friends(token, message)
                    pretty_print(f"Result: {success} of {total} messages sent", (0,255,0))
        elif answers['choice'] == 'Delete/Leave All Servers':
            token = ask_token()
            if token:
                from utils.leave_servers import leave_all_servers
                deleted, left, failed, total = leave_all_servers(token)
                pretty_print("Result:", (0,255,0))
                pretty_print(f"- {deleted} servers deleted", (0,255,0))
                pretty_print(f"- {left} servers left", (0,255,0))
                pretty_print(f"- {failed} errors", (255,0,0))
                pretty_print(f"- {total} servers total", (0,255,0))
        elif answers['choice'] == 'Theme Spammer':
            theme_spam_menu()
        elif answers['choice'] == 'Server Cloner':
            server_cloner_menu()
        elif answers['choice'] == 'Webhook Deleter':
            webhook_deleter_menu()
        questions = [
            inquirer.List('continue',
                         message="Return to main menu?",
                         choices=['Yes', 'No'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers['continue'] == 'No':
            print_banner()
            pretty_print("Goodbye! 👋", (255,32,32))
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        sys.exit(0) 
