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

# Initialize colorama
init()

# Discord Nitro Gift URL
NITRO_URL = "https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

def generate_nitro_code():
    """Generate a random Discord Nitro gift code."""
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"https://discord.gift/{code}"

def check_nitro_code(code):
    """Check if a Nitro code is valid."""
    try:
        response = requests.get(NITRO_URL.format(code=code.split('/')[-1]))
        if response.status_code == 200:
            return True, code
        return False, code
    except:
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
    
    # Get user input
    try:
        amount = int(input(f"{Fore.CYAN}How many codes to generate? {Style.RESET_ALL}"))
        threads = int(input(f"{Fore.CYAN}How many threads? (1-10) {Style.RESET_ALL}"))
        threads = min(max(1, threads), 10)  # Limit threads between 1 and 10
    except ValueError:
        print(f"{Fore.RED}Please enter valid numbers!{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Starting Nitro Generator & Checker...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Generated codes will be saved to 'valid_nitro.txt'{Style.RESET_ALL}\n")

    # Create stop event for animation
    stop_event = threading.Event()
    
    # Start loading animation in separate thread
    anim_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    anim_thread.start()

    # Generate and check codes
    valid_codes = []
    total_checked = 0
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Generate codes
        codes = [generate_nitro_code() for _ in range(amount)]
        
        # Check codes with progress bar
        with tqdm(total=amount, desc=f"{Fore.CYAN}Checking{Style.RESET_ALL}", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            for is_valid, code in executor.map(check_nitro_code, codes):
                total_checked += 1
                if is_valid:
                    valid_codes.append(code)
                    save_valid_code(code)
                    print(f"\n{Fore.GREEN}✓ Valid code found: {code}{Style.RESET_ALL}")
                pbar.update(1)

    # Stop animation
    stop_event.set()
    anim_thread.join()

    # Print results
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