import requests
import time
import json
from colorama import Fore, Style, init

init()

def send_dm_message(token, user_id, message, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    channel_payload = {
        'recipients': [user_id]
    }
    
    try:
        channel_response = requests.post(
            'https://discord.com/api/v9/users/@me/channels',
            headers=headers,
            json=channel_payload
        )
        
        if channel_response.status_code != 200:
            return {'success': False, 'reason': f'Failed to create DM channel: {channel_response.status_code}'}
        
        channel_id = channel_response.json()['id']
        
        message_payload = {
            'content': message
        }
        
        message_response = requests.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            headers=headers,
            json=message_payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] DM Status: {message_response.status_code}{Style.RESET_ALL}")
        
        if message_response.status_code == 200:
            return {'success': True, 'message_id': message_response.json().get('id')}
        elif message_response.status_code == 429:
            retry_after = 2
            try:
                data = message_response.json()
                retry_after = float(data.get('retry_after', 2))
            except:
                pass
            return {'success': False, 'reason': f'Rate limited - wait {retry_after}s', 'retry_after': retry_after}
        else:
            return {'success': False, 'reason': f'HTTP {message_response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'reason': f'Error: {str(e)}'}

def dm_spam_users(tokens, user_ids, message, amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            for user_id in user_ids:
                print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)} - User {user_id}...{Style.RESET_ALL}")
                
                result = send_dm_message(token.strip(), user_id, message, debug)
                result['message_number'] = i + 1
                result['token_index'] = token_idx
                result['user_id'] = user_id
                results.append(result)
                
                if result['success']:
                    print(f"{Fore.GREEN}  ✓ DM sent{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                    if 'retry_after' in result:
                        time.sleep(result['retry_after'])
                
                time.sleep(interval)
    
    return results

def run_dm_spam():
    print(f"{Fore.CYAN}DM Spam Tool{Style.RESET_ALL}")
    
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
    
    user_ids = []
    print(f"{Fore.YELLOW}Enter user IDs to DM (one per line, empty line to finish):{Style.RESET_ALL}")
    while True:
        user_id = input().strip()
        if not user_id:
            break
        user_ids.append(user_id)
    
    if not user_ids:
        print(f"{Fore.RED}No user IDs provided{Style.RESET_ALL}")
        return
    
    message = input(f"{Fore.YELLOW}Enter message: {Style.RESET_ALL}").strip()
    if not message:
        print(f"{Fore.RED}No message provided{Style.RESET_ALL}")
        return
    
    try:
        amount = int(input(f"{Fore.YELLOW}Number of messages to send: {Style.RESET_ALL}"))
    except ValueError:
        amount = 10
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between messages (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    results = dm_spam_users(tokens, user_ids, message, amount, interval, debug)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful DM messages{Style.RESET_ALL}")

if __name__ == "__main__":
    run_dm_spam() 