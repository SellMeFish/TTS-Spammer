import os
import sys
import requests
import zipfile
import io
import shutil
import time
from colorama import Fore, Style, init
from tqdm import tqdm

init()

GITHUB_REPO = "SellMeFish/TTS-Spammer"
RAW_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.txt"
ZIP_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = "version.txt"

PRESERVE_FILES = [
    "update.py",
    "config.json",
    "tokens.txt",
    "proxies.txt",
    "user_data.json",
    "settings.json"
]

def print_banner():
    banner = f"""{Fore.CYAN}{r'''
   __  __          __      __       __
  / / / /___  ____/ /___ _/ /____  / /
 / / / / __ \/ __  / __ `/ __/ _ \/ /
/ /_/ / /_/ / /_/ / /_/ / /_/  __/_/
\____/ .___/\__,_/\__,_/\__/\___(_)
    /_/
'''}{Style.RESET_ALL}"""
    print(banner)
    print(f"{Fore.YELLOW}=== Discord Tool Updater ==={Style.RESET_ALL}\n")

def loading_animation(duration=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(duration * 10):
        for char in chars:
            sys.stdout.write(f"\r{Fore.CYAN}{char} Checking for updates...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")

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
    except Exception as e:
        print(f"{Fore.RED}Error fetching remote version: {str(e)}{Style.RESET_ALL}")
    return None

def backup_important_files():
    backup_dir = "_backup_temp"
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    os.makedirs(backup_dir)
    
    backed_up = []
    for file in PRESERVE_FILES:
        if os.path.exists(file):
            try:
                shutil.copy2(file, os.path.join(backup_dir, file))
                backed_up.append(file)
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Could not backup {file}: {str(e)}{Style.RESET_ALL}")
    
    return backed_up

def restore_important_files(backed_up_files):
    backup_dir = "_backup_temp"
    restored = []
    
    for file in backed_up_files:
        backup_path = os.path.join(backup_dir, file)
        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, file)
                restored.append(file)
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Could not restore {file}: {str(e)}{Style.RESET_ALL}")
    
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    
    return restored

def cleanup_old_files():
    print(f"\n{Fore.CYAN}Cleaning up old files...{Style.RESET_ALL}")
    
    backed_up = backup_important_files()
    if backed_up:
        print(f"{Fore.GREEN}Backed up: {', '.join(backed_up)}{Style.RESET_ALL}")
    
    current_dir = os.getcwd()
    files_deleted = 0
    dirs_deleted = 0
    
    for item in os.listdir(current_dir):
        if item in ["update.py", "_backup_temp", "_update_temp", "_update.zip"]:
            continue
            
        item_path = os.path.join(current_dir, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                files_deleted += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                dirs_deleted += 1
            
            sys.stdout.write(f"\r{Fore.RED}Deleted: {files_deleted} files, {dirs_deleted} directories{Style.RESET_ALL}")
            sys.stdout.flush()
        except Exception as e:
            print(f"\n{Fore.YELLOW}Warning: Could not delete {item}: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✓ Cleanup complete: {files_deleted} files and {dirs_deleted} directories removed{Style.RESET_ALL}")
    return backed_up

def download_with_progress(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True,
                       desc=f"{Fore.CYAN}Downloading{Style.RESET_ALL}",
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')

    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()

def download_and_extract_zip():
    print(f"\n{Fore.CYAN}Downloading latest version...{Style.RESET_ALL}")
    temp_zip = "_update.zip"

    try:
        download_with_progress(ZIP_URL, temp_zip)

        print(f"\n{Fore.CYAN}Extracting update...{Style.RESET_ALL}")
        with zipfile.ZipFile(temp_zip, 'r') as z:
            total_files = len(z.namelist())
            with tqdm(total=total_files, desc=f"{Fore.CYAN}Extracting{Style.RESET_ALL}") as pbar:
                for file in z.namelist():
                    z.extract(file, "_update_temp")
                    pbar.update(1)

        extracted = [d for d in os.listdir("_update_temp") if os.path.isdir(os.path.join("_update_temp", d))][0]
        src_path = os.path.join("_update_temp", extracted)

        print(f"\n{Fore.CYAN}Installing new files...{Style.RESET_ALL}")
        files_copied = 0
        for root, dirs, files in os.walk(src_path):
            rel_path = os.path.relpath(root, src_path)
            for file in files:
                if file == "update.py": continue
                src_file = os.path.join(root, file)
                dst_file = os.path.join(os.getcwd(), rel_path, file) if rel_path != "." else os.path.join(os.getcwd(), file)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                files_copied += 1
                sys.stdout.write(f"\r{Fore.GREEN}Files installed: {files_copied}{Style.RESET_ALL}")
                sys.stdout.flush()

        print("\n")
        shutil.rmtree("_update_temp")
        os.remove(temp_zip)
        return True

    except Exception as e:
        print(f"\n{Fore.RED}Error during update: {str(e)}{Style.RESET_ALL}")
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        if os.path.exists("_update_temp"):
            shutil.rmtree("_update_temp")
        return False

def main():
    print_banner()
    loading_animation()

    local_version = get_local_version()
    remote_version = get_remote_version()

    print(f"\n{Fore.CYAN}Versions:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Local:  {local_version or 'Not installed'}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Remote: {remote_version or 'Not available'}{Style.RESET_ALL}\n")

    if not remote_version:
        print(f"{Fore.RED}[ERROR] Could not fetch remote version. Please check your internet connection.{Style.RESET_ALL}")
        return

    if local_version == remote_version:
        print(f"{Fore.GREEN}You already have the latest version!{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}A new version is available!{Style.RESET_ALL}")
    print(f"{Fore.RED}WARNING: This will completely remove all old files and install fresh!{Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}Do you want to continue with the clean update? (y/n): {Style.RESET_ALL}").lower()

    if choice != 'y':
        print(f"{Fore.YELLOW}Update cancelled.{Style.RESET_ALL}")
        return

    backed_up_files = cleanup_old_files()

    if download_and_extract_zip():
        restored_files = restore_important_files(backed_up_files)
        if restored_files:
            print(f"{Fore.GREEN}Restored: {', '.join(restored_files)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✓ Clean update successful!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please restart the tool.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ Update failed.{Style.RESET_ALL}")
        if backed_up_files:
            print(f"{Fore.CYAN}Attempting to restore backup...{Style.RESET_ALL}")
            restore_important_files(backed_up_files)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Update cancelled.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
# update
