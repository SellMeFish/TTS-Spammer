import requests
import time
import json
from colorama import Fore, Style

def send_ping_message(token, channel_id, user_ids, message="", interval=1, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    ping_text = " ".join([f"<@{user_id}>" for user_id in user_ids])
    full_message = f"{ping_text} {message}".strip()
    
    payload = {
        'content': full_message
    }
    
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Ping Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return {'success': True, 'message_id': response.json().get('id')}
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

def get_server_members(token, server_id, limit=100, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    url = f'https://discord.com/api/v9/guilds/{server_id}/members?limit={limit}'
    
    try:
        response = requests.get(url, headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Members Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            members = response.json()
            return [member['user']['id'] for member in members if not member['user'].get('bot', False)]
        else:
            return []
    except Exception as e:
        if debug:
            print(f"{Fore.RED}[DEBUG] Error getting members: {str(e)}{Style.RESET_ALL}")
        return []

def ping_spam_users(tokens, channel_id, user_ids, message="", amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
            
            result = send_ping_message(token.strip(), channel_id, user_ids, message, interval, debug)
            result['message_number'] = i + 1
            result['token_index'] = token_idx
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Ping message sent{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def ping_spam_everyone(tokens, channel_id, message="", amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
            
            headers = {
                'Authorization': tokens[token_idx-1].strip(),
                'Content-Type': 'application/json'
            }
            
            full_message = f"@everyone {message}".strip()
            payload = {'content': full_message}
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                
                if debug:
                    print(f"{Fore.CYAN}[DEBUG] Everyone Status: {response.status_code}{Style.RESET_ALL}")
                
                if response.status_code == 200:
                    result = {'success': True, 'message_id': response.json().get('id')}
                    print(f"{Fore.GREEN}  ✓ @everyone message sent{Style.RESET_ALL}")
                elif response.status_code == 429:
                    retry_after = 2
                    try:
                        data = response.json()
                        retry_after = float(data.get('retry_after', 2))
                    except:
                        pass
                    result = {'success': False, 'reason': f'Rate limited - wait {retry_after}s', 'retry_after': retry_after}
                    print(f"{Fore.RED}  ✗ Rate limited: {retry_after}s{Style.RESET_ALL}")
                    time.sleep(retry_after)
                else:
                    result = {'success': False, 'reason': f'HTTP {response.status_code}'}
                    print(f"{Fore.RED}  ✗ Failed: HTTP {response.status_code}{Style.RESET_ALL}")
                
                result['message_number'] = i + 1
                result['token_index'] = token_idx
                results.append(result)
                
            except Exception as e:
                result = {'success': False, 'reason': f'Error: {str(e)}', 'message_number': i + 1, 'token_index': token_idx}
                results.append(result)
                print(f"{Fore.RED}  ✗ Error: {str(e)}{Style.RESET_ALL}")
            
            time.sleep(interval)
    
    return results

def run_ping_spam():
    print(f"{Fore.CYAN}Ping Spam Tool{Style.RESET_ALL}")
    print("1. Ping specific users")
    print("2. Ping @everyone")
    print("3. Ping server members")
    
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
    
    channel_id = input(f"{Fore.YELLOW}Enter channel ID: {Style.RESET_ALL}").strip()
    if not channel_id:
        print(f"{Fore.RED}No channel ID provided{Style.RESET_ALL}")
        return
    
    message = input(f"{Fore.YELLOW}Enter message (optional): {Style.RESET_ALL}").strip()
    
    try:
        amount = int(input(f"{Fore.YELLOW}Number of messages to send: {Style.RESET_ALL}"))
    except ValueError:
        amount = 10
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between messages (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        user_ids = []
        print(f"{Fore.YELLOW}Enter user IDs to ping (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            user_id = input().strip()
            if not user_id:
                break
            user_ids.append(user_id)
        
        if user_ids:
            results = ping_spam_users(tokens, channel_id, user_ids, message, amount, interval, debug)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful ping messages{Style.RESET_ALL}")
    
    elif choice == '2':
        results = ping_spam_everyone(tokens, channel_id, message, amount, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful @everyone messages{Style.RESET_ALL}")
    
    elif choice == '3':
        server_id = input(f"{Fore.YELLOW}Enter server ID: {Style.RESET_ALL}").strip()
        if not server_id:
            print(f"{Fore.RED}No server ID provided{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Getting server members...{Style.RESET_ALL}")
        member_ids = get_server_members(tokens[0].strip(), server_id, 100, debug)
        
        if member_ids:
            print(f"{Fore.CYAN}Found {len(member_ids)} members to ping{Style.RESET_ALL}")
            results = ping_spam_users(tokens, channel_id, member_ids[:20], message, amount, interval, debug)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful member ping messages{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No members found or no permission to view members{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}") 