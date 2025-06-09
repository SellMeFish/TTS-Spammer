import requests
import time
import json
from colorama import Fore, Style

def add_reaction(token, channel_id, message_id, emoji, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    emoji_encoded = requests.utils.quote(emoji)
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me'
    
    try:
        response = requests.put(url, headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] React Status: {response.status_code}{Style.RESET_ALL}")
        
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

def get_channel_messages(token, channel_id, limit=50, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}'
    
    try:
        response = requests.get(url, headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Messages Status: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        if debug:
            print(f"{Fore.RED}[DEBUG] Error getting messages: {str(e)}{Style.RESET_ALL}")
        return []

def mass_react_messages(tokens, channel_id, message_ids, emojis, interval=1, debug=False):
    results = []
    
    for token_idx, token in enumerate(tokens, 1):
        print(f"{Fore.YELLOW}Processing token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
        
        for msg_idx, message_id in enumerate(message_ids, 1):
            print(f"{Fore.CYAN}  Reacting to message {msg_idx}/{len(message_ids)} ({message_id})...{Style.RESET_ALL}")
            
            for emoji_idx, emoji in enumerate(emojis, 1):
                print(f"{Fore.MAGENTA}    Adding reaction {emoji_idx}/{len(emojis)} ({emoji})...{Style.RESET_ALL}")
                
                result = add_reaction(token.strip(), channel_id, message_id, emoji.strip(), debug)
                result['token_index'] = token_idx
                result['message_id'] = message_id
                result['emoji'] = emoji.strip()
                results.append(result)
                
                if result['success']:
                    print(f"{Fore.GREEN}    ✓ Reaction added{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}    ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                    if 'retry_after' in result:
                        time.sleep(result['retry_after'])
                
                time.sleep(interval)
    
    return results

def mass_react_channel(tokens, channel_id, emojis, message_limit=10, interval=1, debug=False):
    results = []
    
    if not tokens:
        return results
    
    messages = get_channel_messages(tokens[0].strip(), channel_id, message_limit, debug)
    message_ids = [msg['id'] for msg in messages]
    
    if not message_ids:
        print(f"{Fore.RED}No messages found in channel{Style.RESET_ALL}")
        return results
    
    print(f"{Fore.CYAN}Found {len(message_ids)} messages to react to{Style.RESET_ALL}")
    
    return mass_react_messages(tokens, channel_id, message_ids, emojis, interval, debug)

def run_mass_react():
    print(f"{Fore.CYAN}Mass React Tool{Style.RESET_ALL}")
    print("1. React to specific messages")
    print("2. React to recent messages in channel")
    
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
    
    channel_id = input(f"{Fore.YELLOW}Enter channel ID: {Style.RESET_ALL}").strip()
    if not channel_id:
        print(f"{Fore.RED}No channel ID provided{Style.RESET_ALL}")
        return
    
    emojis = []
    print(f"{Fore.YELLOW}Enter emojis/reactions (one per line, empty line to finish):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Examples: 👍, 😂, :custom_emoji:, <:name:id>{Style.RESET_ALL}")
    while True:
        emoji = input().strip()
        if not emoji:
            break
        emojis.append(emoji)
    
    if not emojis:
        print(f"{Fore.RED}No emojis provided{Style.RESET_ALL}")
        return
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between reactions (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        message_ids = []
        print(f"{Fore.YELLOW}Enter message IDs (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            msg_id = input().strip()
            if not msg_id:
                break
            message_ids.append(msg_id)
        
        if message_ids:
            results = mass_react_messages(tokens, channel_id, message_ids, emojis, interval, debug)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful reactions{Style.RESET_ALL}")
    
    elif choice == '2':
        try:
            message_limit = int(input(f"{Fore.YELLOW}Number of recent messages to react to (max 50): {Style.RESET_ALL}"))
            message_limit = min(message_limit, 50)
        except ValueError:
            message_limit = 10
        
        results = mass_react_channel(tokens, channel_id, emojis, message_limit, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful reactions{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}") 
# update
