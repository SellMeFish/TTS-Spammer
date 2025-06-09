import os
import sys
import time
import random
import string
import base64
import json
import threading
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm

init()

def generate_random_string(length):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_token():

    user_id = str(random.randint(100000000000000000, 999999999999999999))

    timestamp = int(datetime.now().timestamp())
    timestamp_bytes = timestamp.to_bytes(4, 'big')
    timestamp_b64 = base64.b64encode(timestamp_bytes).decode('utf-8').rstrip('=')

    random_part = generate_random_string(27)

    token = f"{user_id}.{timestamp_b64}.{random_part}"
    return token

def save_tokens(tokens, filename="generated_tokens.txt"):

    with open(filename, "a") as f:
        for token in tokens:
            f.write(f"{token}\n")

def loading_animation(stop_event):

    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}{chars[i]} Generating tokens...{Style.RESET_ALL}")
        sys.stdout.flush()
        i = (i + 1) % len(chars)
        time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")

def run_token_generator():

    print(f"\n{Fore.YELLOW}=== Discord Token Generator ==={Style.RESET_ALL}\n")

    try:
        amount = int(input(f"{Fore.CYAN}How many tokens to generate? {Style.RESET_ALL}"))
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError as e:
        print(f"{Fore.RED}Please enter a valid number! {str(e)}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Starting Token Generator...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Generated tokens will be saved to 'generated_tokens.txt'{Style.RESET_ALL}\n")

    stop_event = threading.Event()

    anim_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    anim_thread.start()

    tokens = []
    with tqdm(total=amount, desc=f"{Fore.CYAN}Generating{Style.RESET_ALL}",
             bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for _ in range(amount):
            token = generate_token()
            tokens.append(token)
            pbar.update(1)

    stop_event.set()
    anim_thread.join()

    save_tokens(tokens)

    print(f"\n{Fore.CYAN}=== Results ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Successfully generated {amount} tokens!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Tokens saved to 'generated_tokens.txt'{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Sample tokens:{Style.RESET_ALL}")
    for i, token in enumerate(tokens[:3], 1):
        print(f"{Fore.GREEN}{i}. {token}{Style.RESET_ALL}")
    if len(tokens) > 3:
        print(f"{Fore.YELLOW}... and {len(tokens)-3} more{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        run_token_generator()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
# update
