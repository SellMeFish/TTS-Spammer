import requests
import time
import json
import base64
from colorama import Fore, Style, init

init()

def change_avatar(token, avatar_path, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        with open(avatar_path, 'rb') as f:
            avatar_data = f.read()
        
        avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')
        
        file_extension = avatar_path.lower().split('.')[-1]
        if file_extension in ['jpg', 'jpeg']:
            mime_type = 'image/jpeg'
        elif file_extension == 'png':
            mime_type = 'image/png'
        elif file_extension == 'gif':
            mime_type = 'image/gif'
        else:
            return {'success': False, 'reason': 'Unsupported file format. Use JPG, PNG, or GIF.'}
        
        data_uri = f"data:{mime_type};base64,{avatar_base64}"
        
        payload = {
            'avatar': data_uri
        }
        
        response = requests.patch(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Avatar Change Status: {response.status_code}{Style.RESET_ALL}")
        
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
    
    except FileNotFoundError:
        return {'success': False, 'reason': 'Avatar file not found'}
    except Exception as e:
        return {'success': False, 'reason': f'Error: {str(e)}'}

def remove_avatar(token, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'avatar': None
    }
    
    try:
        response = requests.patch(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Avatar Remove Status: {response.status_code}{Style.RESET_ALL}")
        
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

def run_avatar_changer():
    print(f"{Fore.CYAN}Avatar Changer Tool{Style.RESET_ALL}")
    print("1. Change avatar")
    print("2. Remove avatar")
    
    choice = input(f"{Fore.YELLOW}Select option (1-2): {Style.RESET_ALL}").strip()
    
    token = input(f"{Fore.YELLOW}Enter user token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided{Style.RESET_ALL}")
        return
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        avatar_path = input(f"{Fore.YELLOW}Enter path to avatar image: {Style.RESET_ALL}").strip()
        if not avatar_path:
            print(f"{Fore.RED}No avatar path provided{Style.RESET_ALL}")
            return
        
        result = change_avatar(token, avatar_path, debug)
        
        if result['success']:
            print(f"{Fore.GREEN}✓ Avatar changed successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '2':
        result = remove_avatar(token, debug)
        
        if result['success']:
            print(f"{Fore.GREEN}✓ Avatar removed successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    run_avatar_changer() 