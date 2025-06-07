import requests
import time
import json
import random
from colorama import Fore, Style

def send_channel_message(token, channel_id, message, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'content': message
    }
    
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Message Status: {response.status_code}{Style.RESET_ALL}")
        
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

def spam_channel_single_message(tokens, channel_id, message, amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)}...{Style.RESET_ALL}")
            
            result = send_channel_message(token.strip(), channel_id, message, debug)
            result['message_number'] = i + 1
            result['token_index'] = token_idx
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Message sent{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def spam_channel_multiple_messages(tokens, channel_id, messages, amount=10, interval=1, randomize=True, debug=False):
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            if randomize:
                message = random.choice(messages)
            else:
                message = messages[i % len(messages)]
            
            print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)} - '{message[:30]}...'{Style.RESET_ALL}")
            
            result = send_channel_message(token.strip(), channel_id, message, debug)
            result['message_number'] = i + 1
            result['token_index'] = token_idx
            result['message_content'] = message[:50]
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Message sent{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def spam_channel_random_text(tokens, channel_id, amount=10, interval=1, debug=False):
    random_words = [
        "hello", "world", "discord", "spam", "message", "random", "text", "bot", "user", "server",
        "channel", "voice", "chat", "game", "play", "fun", "cool", "awesome", "nice", "good",
        "bad", "test", "check", "work", "code", "python", "script", "tool", "hack", "admin"
    ]
    
    results = []
    
    for i in range(amount):
        for token_idx, token in enumerate(tokens, 1):
            random_message = " ".join(random.choices(random_words, k=random.randint(3, 8)))
            
            print(f"{Fore.YELLOW}Message {i+1}/{amount} - Token {token_idx}/{len(tokens)} - '{random_message}'{Style.RESET_ALL}")
            
            result = send_channel_message(token.strip(), channel_id, random_message, debug)
            result['message_number'] = i + 1
            result['token_index'] = token_idx
            result['message_content'] = random_message
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Random message sent{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def run_channel_spam():
    print(f"{Fore.CYAN}Channel Spam Tool{Style.RESET_ALL}")
    print("1. Spam single message")
    print("2. Spam multiple messages")
    print("3. Spam random text")
    
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
        message = input(f"{Fore.YELLOW}Enter message to spam: {Style.RESET_ALL}").strip()
        if not message:
            print(f"{Fore.RED}No message provided{Style.RESET_ALL}")
            return
        
        results = spam_channel_single_message(tokens, channel_id, message, amount, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful messages{Style.RESET_ALL}")
    
    elif choice == '2':
        messages = []
        print(f"{Fore.YELLOW}Enter messages to spam (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            message = input().strip()
            if not message:
                break
            messages.append(message)
        
        if not messages:
            print(f"{Fore.RED}No messages provided{Style.RESET_ALL}")
            return
        
        randomize = input(f"{Fore.YELLOW}Randomize message order? (y/n): {Style.RESET_ALL}").lower() == 'y'
        
        results = spam_channel_multiple_messages(tokens, channel_id, messages, amount, interval, randomize, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful messages{Style.RESET_ALL}")
    
    elif choice == '3':
        results = spam_channel_random_text(tokens, channel_id, amount, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful random messages{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}") 
# update
