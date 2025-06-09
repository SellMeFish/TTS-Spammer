import requests
import time
import json
from colorama import Fore, Style, init

init()

def get_server_info(token, guild_id, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'https://discord.com/api/v9/guilds/{guild_id}',
            headers=headers
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Server Info Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {'success': False, 'reason': f'HTTP {response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'reason': f'Error: {str(e)}'}

def change_server_name(token, guild_id, new_name, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {'name': new_name}
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/guilds/{guild_id}',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Name Change Status: {response.status_code}{Style.RESET_ALL}")
        
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

def ban_user(token, guild_id, user_id, reason="", debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    params = {}
    if reason:
        params['reason'] = reason
    
    try:
        response = requests.put(
            f'https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}',
            headers=headers,
            params=params
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Ban Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 204:
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

def kick_user(token, guild_id, user_id, reason="", debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    params = {}
    if reason:
        params['reason'] = reason
    
    try:
        response = requests.delete(
            f'https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}',
            headers=headers,
            params=params
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Kick Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 204:
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

def run_server_management():
    print(f"{Fore.CYAN}Server Management Tool{Style.RESET_ALL}")
    print("1. Get server info")
    print("2. Change server name")
    print("3. Ban user")
    print("4. Kick user")
    
    choice = input(f"{Fore.YELLOW}Select option (1-4): {Style.RESET_ALL}").strip()
    
    token = input(f"{Fore.YELLOW}Enter bot/user token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided{Style.RESET_ALL}")
        return
    
    guild_id = input(f"{Fore.YELLOW}Enter server ID: {Style.RESET_ALL}").strip()
    if not guild_id:
        print(f"{Fore.RED}No server ID provided{Style.RESET_ALL}")
        return
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        result = get_server_info(token, guild_id, debug)
        if result['success']:
            server_data = result['data']
            print(f"\n{Fore.GREEN}Server Information:{Style.RESET_ALL}")
            print(f"Name: {server_data.get('name', 'Unknown')}")
            print(f"ID: {server_data.get('id', 'Unknown')}")
            print(f"Owner ID: {server_data.get('owner_id', 'Unknown')}")
            print(f"Member Count: {server_data.get('approximate_member_count', 'Unknown')}")
        else:
            print(f"{Fore.RED}Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '2':
        new_name = input(f"{Fore.YELLOW}Enter new server name: {Style.RESET_ALL}").strip()
        if new_name:
            result = change_server_name(token, guild_id, new_name, debug)
            if result['success']:
                print(f"{Fore.GREEN}✓ Server name changed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '3':
        user_id = input(f"{Fore.YELLOW}Enter user ID to ban: {Style.RESET_ALL}").strip()
        reason = input(f"{Fore.YELLOW}Enter ban reason (optional): {Style.RESET_ALL}").strip()
        if user_id:
            result = ban_user(token, guild_id, user_id, reason, debug)
            if result['success']:
                print(f"{Fore.GREEN}✓ User banned successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '4':
        user_id = input(f"{Fore.YELLOW}Enter user ID to kick: {Style.RESET_ALL}").strip()
        reason = input(f"{Fore.YELLOW}Enter kick reason (optional): {Style.RESET_ALL}").strip()
        if user_id:
            result = kick_user(token, guild_id, user_id, reason, debug)
            if result['success']:
                print(f"{Fore.GREEN}✓ User kicked successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    run_server_management() 