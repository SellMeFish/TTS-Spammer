import requests
import time
import json
from colorama import Fore, Style, init

init()

def change_nickname(token, guild_id, new_nickname, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'nick': new_nickname
    }
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/guilds/{guild_id}/members/@me',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Nickname Change Status: {response.status_code}{Style.RESET_ALL}")
        
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

def change_nickname_multiple_servers(token, guild_ids, new_nickname, debug=False):
    results = []
    
    for guild_id in guild_ids:
        print(f"{Fore.YELLOW}Changing nickname in server {guild_id}...{Style.RESET_ALL}")
        
        result = change_nickname(token, guild_id, new_nickname, debug)
        result['guild_id'] = guild_id
        results.append(result)
        
        if result['success']:
            print(f"{Fore.GREEN}  ✓ Nickname changed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
            if 'retry_after' in result:
                time.sleep(result['retry_after'])
        
        time.sleep(0.5)
    
    return results

def run_nickname_changer():
    print(f"{Fore.CYAN}Nickname Changer Tool{Style.RESET_ALL}")
    print("1. Change nickname in one server")
    print("2. Change nickname in multiple servers")
    
    choice = input(f"{Fore.YELLOW}Select option (1-2): {Style.RESET_ALL}").strip()
    
    token = input(f"{Fore.YELLOW}Enter user token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided{Style.RESET_ALL}")
        return
    
    new_nickname = input(f"{Fore.YELLOW}Enter new nickname: {Style.RESET_ALL}").strip()
    if not new_nickname:
        print(f"{Fore.RED}No nickname provided{Style.RESET_ALL}")
        return
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        guild_id = input(f"{Fore.YELLOW}Enter server ID: {Style.RESET_ALL}").strip()
        if not guild_id:
            print(f"{Fore.RED}No server ID provided{Style.RESET_ALL}")
            return
        
        result = change_nickname(token, guild_id, new_nickname, debug)
        
        if result['success']:
            print(f"{Fore.GREEN}✓ Nickname changed successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Failed: {result['reason']}{Style.RESET_ALL}")
    
    elif choice == '2':
        guild_ids = []
        print(f"{Fore.YELLOW}Enter server IDs (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            guild_id = input().strip()
            if not guild_id:
                break
            guild_ids.append(guild_id)
        
        if not guild_ids:
            print(f"{Fore.RED}No server IDs provided{Style.RESET_ALL}")
            return
        
        results = change_nickname_multiple_servers(token, guild_ids, new_nickname, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful nickname changes{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    run_nickname_changer() 