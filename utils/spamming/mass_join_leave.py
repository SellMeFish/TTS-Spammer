import requests
import time
import json
from colorama import Fore, Style

def join_server(token, invite_code, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    url = f'https://discord.com/api/v9/invites/{invite_code}'
    
    try:
        response = requests.post(url, headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Join Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            data = response.json()
            return {'success': True, 'server_name': data.get('guild', {}).get('name', 'Unknown')}
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

def leave_server(token, server_id, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    url = f'https://discord.com/api/v9/users/@me/guilds/{server_id}'
    
    try:
        response = requests.delete(url, headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Leave Status: {response.status_code}{Style.RESET_ALL}")
        
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

def get_user_servers(token, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Servers Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        if debug:
            print(f"{Fore.RED}[DEBUG] Error getting servers: {str(e)}{Style.RESET_ALL}")
        return []

def mass_join_servers(tokens, invite_codes, interval=1, debug=False):
    results = []
    
    for token_idx, token in enumerate(tokens, 1):
        print(f"{Fore.YELLOW}Processing token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
        
        for invite_idx, invite_code in enumerate(invite_codes, 1):
            print(f"{Fore.CYAN}  Joining server {invite_idx}/{len(invite_codes)} ({invite_code})...{Style.RESET_ALL}")
            
            result = join_server(token.strip(), invite_code.strip(), debug)
            result['token_index'] = token_idx
            result['invite_code'] = invite_code.strip()
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Joined: {result.get('server_name', 'Unknown')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def mass_leave_servers(tokens, server_ids=None, interval=1, debug=False):
    results = []
    
    for token_idx, token in enumerate(tokens, 1):
        print(f"{Fore.YELLOW}Processing token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
        
        if server_ids is None:
            servers = get_user_servers(token.strip(), debug)
            server_ids_to_leave = [server['id'] for server in servers]
        else:
            server_ids_to_leave = server_ids
        
        for server_idx, server_id in enumerate(server_ids_to_leave, 1):
            print(f"{Fore.CYAN}  Leaving server {server_idx}/{len(server_ids_to_leave)} ({server_id})...{Style.RESET_ALL}")
            
            result = leave_server(token.strip(), server_id, debug)
            result['token_index'] = token_idx
            result['server_id'] = server_id
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Left server{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def run_mass_join_leave():
    print(f"{Fore.CYAN}Mass Join/Leave Tool{Style.RESET_ALL}")
    print("1. Mass join servers")
    print("2. Mass leave servers")
    print("3. Mass leave all servers")
    
    choice = input(f"{Fore.YELLOW}Select option (1-3): {Style.RESET_ALL}").strip()
    
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
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between actions (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        invite_codes = []
        print(f"{Fore.YELLOW}Enter invite codes (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            invite = input().strip()
            if not invite:
                break
            invite_codes.append(invite.replace('https://discord.gg/', '').replace('discord.gg/', ''))
        
        if invite_codes:
            results = mass_join_servers(tokens, invite_codes, interval, debug)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful joins{Style.RESET_ALL}")
    
    elif choice == '2':
        server_ids = []
        print(f"{Fore.YELLOW}Enter server IDs (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            server_id = input().strip()
            if not server_id:
                break
            server_ids.append(server_id)
        
        if server_ids:
            results = mass_leave_servers(tokens, server_ids, interval, debug)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful leaves{Style.RESET_ALL}")
    
    elif choice == '3':
        results = mass_leave_servers(tokens, None, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful leaves{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}") 
# update
