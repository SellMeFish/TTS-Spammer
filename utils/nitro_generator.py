import os
import sys
import time
import random
import string
import requests
import threading
from colorama import Fore, Style, init
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

init()

NITRO_URL = "https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

def generate_nitro_code():
    """Generate a random Discord Nitro gift code."""
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"https://discord.gift/{code}"

def check_nitro_code(code):
    """Check if a Nitro code is valid."""
    try:
        code_part = code.split('/')[-1]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(NITRO_URL.format(code=code_part), headers=headers, timeout=10)
        
        # valid codes usually return 200 so, invalid ones return 404 or 400
        if response.status_code == 200:
            return True, code
        elif response.status_code == 429:
            print(f"\n{Fore.YELLOW}⚠ Rate limited. Pausing...{Style.RESET_ALL}")
            time.sleep(2)
            return False, code
        else:
            return False, code
    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}Network error: {str(e)}{Style.RESET_ALL}")
        return False, code
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        return False, code

def save_valid_code(code):
    """Save valid Nitro codes to a file."""
    with open("valid_nitro.txt", "a") as f:
        f.write(f"{code}\n")

def loading_animation(stop_event):
    """Show loading animation while checking codes."""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}{chars[i]} Checking Nitro codes...{Style.RESET_ALL}")
        sys.stdout.flush()
        i = (i + 1) % len(chars)
        time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")

def run_nitro_generator():
    """Run the Nitro Generator & Checker."""
    print(f"\n{Fore.YELLOW}=== Discord Nitro Generator & Checker ==={Style.RESET_ALL}\n")

    try:
        amount = int(input(f"{Fore.CYAN}How many codes to generate? {Style.RESET_ALL}"))
        threads = int(input(f"{Fore.CYAN}How many threads? (1-10) {Style.RESET_ALL}"))
        threads = min(max(1, threads), 10)
    except ValueError:
        print(f"{Fore.RED}Please enter valid numbers!{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Starting Nitro Generator & Checker...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Generated codes will be saved to 'valid_nitro.txt'{Style.RESET_ALL}\n")

    stop_event = threading.Event()

    anim_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    anim_thread.start()

    valid_codes = []
    total_checked = 0

    with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:  # limited to 3 to avoid rate limits
        codes = [generate_nitro_code() for _ in range(amount)]

        with tqdm(total=amount, desc=f"{Fore.CYAN}Checking{Style.RESET_ALL}", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            for is_valid, code in executor.map(check_nitro_code, codes):
                total_checked += 1
                if is_valid:
                    valid_codes.append(code)
                    save_valid_code(code)
                    print(f"\n{Fore.GREEN}✓ Valid code found: {code}{Style.RESET_ALL}")
                pbar.update(1)
                # added small delay to avoid overwhelming the API
                time.sleep(0.1)

    stop_event.set()
    anim_thread.join()

    print(f"\n{Fore.CYAN}=== Results ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Total codes checked: {total_checked}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Valid codes found: {len(valid_codes)}{Style.RESET_ALL}")
    if valid_codes:
        print(f"\n{Fore.GREEN}Valid codes saved to 'valid_nitro.txt'{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Valid codes:{Style.RESET_ALL}")
        for code in valid_codes:
            print(f"{Fore.GREEN}✓ {code}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        run_nitro_generator()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
