import requests
import time
import json
from colorama import Fore, Style, init

init()

def send_friend_request(token, username, discriminator, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'username': username,
        'discriminator': discriminator
    }
    
    try:
        response = requests.post(
            'https://discord.com/api/v9/users/@me/relationships',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Friend Request Status: {response.status_code}{Style.RESET_ALL}")
        
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

def spam_friend_requests(tokens, targets, amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            for target in targets:
                username, discriminator = target.split('#') if '#' in target else (target, '0')
                
                print(f"{Fore.YELLOW}Request {i+1}/{amount} - Token {token_idx}/{len(tokens)} - {username}#{discriminator}...{Style.RESET_ALL}")
                
                result = send_friend_request(token.strip(), username, discriminator, debug)
                result['request_number'] = i + 1
                result['token_index'] = token_idx
                result['target'] = target
                results.append(result)
                
                if result['success']:
                    print(f"{Fore.GREEN}  ✓ Friend request sent{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                    if 'retry_after' in result:
                        time.sleep(result['retry_after'])
                
                time.sleep(interval)
    
    return results

def run_friend_request_spam():
    print(f"{Fore.CYAN}Friend Request Spam Tool{Style.RESET_ALL}")
    
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
    
    targets = []
    print(f"{Fore.YELLOW}Enter usernames (username#discriminator or just username, one per line, empty line to finish):{Style.RESET_ALL}")
    while True:
        target = input().strip()
        if not target:
            break
        targets.append(target)
    
    if not targets:
        print(f"{Fore.RED}No targets provided{Style.RESET_ALL}")
        return
    
    try:
        amount = int(input(f"{Fore.YELLOW}Number of friend requests per target: {Style.RESET_ALL}"))
    except ValueError:
        amount = 10
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between requests (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    results = spam_friend_requests(tokens, targets, amount, interval, debug)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful friend requests{Style.RESET_ALL}")

if __name__ == "__main__":
    run_friend_request_spam() 