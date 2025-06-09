import requests
import time
import json
from colorama import Fore, Style, init

init()

def bypass_verification(token, guild_id, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/guilds/{guild_id}/members/@me',
            headers=headers,
            json={'pending': False}
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Verification Status: {response.status_code}{Style.RESET_ALL}")
        
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

def accept_rules(token, guild_id, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.put(
            f'https://discord.com/api/v9/guilds/{guild_id}/requests/@me',
            headers=headers,
            json={'application_status': 'SUBMITTED'}
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Rules Accept Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code in [200, 204]:
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

def run_verification_bypass():
    print(f"{Fore.CYAN}Verification Bypass Tool{Style.RESET_ALL}")
    print("1. Bypass member screening")
    print("2. Accept server rules")
    
    choice = input(f"{Fore.YELLOW}Select option (1-2): {Style.RESET_ALL}").strip()
    
    tokens = []
    print(f"{Fore.YELLOW}Enter tokens (one per line, empty line to finish):{Style.RESET_ALL}")
    while True:
        token = input().strip()
        if not token:
            break
        tokens.append(token)
    
    if not tokens:
        print(f"{Fore.RED}No tokens provided{Style.RESET_ALL}")
        return
    
    guild_id = input(f"{Fore.YELLOW}Enter server ID: {Style.RESET_ALL}").strip()
    if not guild_id:
        print(f"{Fore.RED}No server ID provided{Style.RESET_ALL}")
        return
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    results = []
    
    for token_idx, token in enumerate(tokens, 1):
        print(f"{Fore.YELLOW}Processing token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
        
        if choice == '1':
            result = bypass_verification(token.strip(), guild_id, debug)
        elif choice == '2':
            result = accept_rules(token.strip(), guild_id, debug)
        else:
            print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
            return
        
        result['token_index'] = token_idx
        results.append(result)
        
        if result['success']:
            print(f"{Fore.GREEN}  ✓ Verification bypassed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
            if 'retry_after' in result:
                time.sleep(result['retry_after'])
        
        time.sleep(0.5)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful bypasses{Style.RESET_ALL}")

if __name__ == "__main__":
    run_verification_bypass() 