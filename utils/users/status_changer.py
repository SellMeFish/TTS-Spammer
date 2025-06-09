import requests
import time
import json
from colorama import Fore, Style, init

init()

def change_status(token, status_text, status_type="playing", debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    status_types = {
        "playing": 0,
        "streaming": 1,
        "listening": 2,
        "watching": 3,
        "custom": 4,
        "competing": 5
    }
    
    activity = {
        "name": status_text,
        "type": status_types.get(status_type.lower(), 0)
    }
    
    payload = {
        "op": 3,
        "d": {
            "since": None,
            "activities": [activity],
            "status": "online",
            "afk": False
        }
    }
    
    try:
        response = requests.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json={"custom_status": {"text": status_text}}
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Status Change Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return {'success': True}
        elif response.status_code == 429:
            retry_after = 2
            try:
                data = response.json()
                retry_after = float(data.get('retry_after', 2))
            except:
                pass
            return {'success': False, 'reason': f'Rate limited - wait {retry_after}s', 'retry_after': retry_after}
        else:
            return {'success': False, 'reason': f'HTTP {response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'reason': f'Error: {str(e)}'}

def change_custom_status(token, status_text, emoji=None, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    custom_status = {
        "text": status_text
    }
    
    if emoji:
        custom_status["emoji_name"] = emoji
    
    payload = {
        "custom_status": custom_status
    }
    
    try:
        response = requests.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Custom Status Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return {'success': True}
        elif response.status_code == 429:
            retry_after = 2
            try:
                data = response.json()
                retry_after = float(data.get('retry_after', 2))
            except:
                pass
            return {'success': False, 'reason': f'Rate limited - wait {retry_after}s', 'retry_after': retry_after}
        else:
            return {'success': False, 'reason': f'HTTP {response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'reason': f'Error: {str(e)}'}

def run_status_changer():
    print(f"{Fore.CYAN}Status Changer Tool{Style.RESET_ALL}")
    print("1. Change activity status")
    print("2. Change custom status")
    
    choice = input(f"{Fore.YELLOW}Select option (1-2): {Style.RESET_ALL}").strip()
    
    token = input(f"{Fore.YELLOW}Enter user token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided{Style.RESET_ALL}")
        return
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        status_text = input(f"{Fore.YELLOW}Enter status text: {Style.RESET_ALL}").strip()
        if not status_text:
            print(f"{Fore.RED}No status text provided{Style.RESET_ALL}")
            return
        
        print("Status types: playing, streaming, listening, watching, custom, competing")
        status_type = input(f"{Fore.YELLOW}Enter status type (default: playing): {Style.RESET_ALL}").strip()
        if not status_type:
            status_type = "playing"
        
        result = change_status(token, status_text, status_type, debug)
        
        if result['success']:
            print(f"{Fore.GREEN}✓ Activity status changed successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '2':
        status_text = input(f"{Fore.YELLOW}Enter custom status text: {Style.RESET_ALL}").strip()
        if not status_text:
            print(f"{Fore.RED}No status text provided{Style.RESET_ALL}")
            return
        
        emoji = input(f"{Fore.YELLOW}Enter emoji (optional): {Style.RESET_ALL}").strip()
        
        result = change_custom_status(token, status_text, emoji if emoji else None, debug)
        
        if result['success']:
            print(f"{Fore.GREEN}✓ Custom status changed successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    run_status_changer() 