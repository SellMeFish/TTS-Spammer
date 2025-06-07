import requests
import json
from colorama import Fore, Style

def check_token(token, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Status Code: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                'valid': True,
                'username': user_data.get('username', 'Unknown'),
                'discriminator': user_data.get('discriminator', '0000'),
                'id': user_data.get('id', 'Unknown'),
                'email': user_data.get('email', 'Not available'),
                'verified': user_data.get('verified', False),
                'mfa_enabled': user_data.get('mfa_enabled', False),
                'premium_type': user_data.get('premium_type', 0),
                'phone': user_data.get('phone', 'Not available')
            }
        elif response.status_code == 401:
            return {'valid': False, 'reason': 'Invalid token'}
        elif response.status_code == 403:
            return {'valid': False, 'reason': 'Token locked/disabled'}
        elif response.status_code == 429:
            return {'valid': False, 'reason': 'Rate limited'}
        else:
            return {'valid': False, 'reason': f'HTTP {response.status_code}'}
            
    except Exception as e:
        return {'valid': False, 'reason': f'Error: {str(e)}'}

def check_multiple_tokens(tokens, debug=False):
    results = []
    for i, token in enumerate(tokens, 1):
        print(f"{Fore.YELLOW}Checking token {i}/{len(tokens)}...{Style.RESET_ALL}")
        result = check_token(token.strip(), debug)
        result['token'] = token.strip()
        results.append(result)
    return results

def display_token_results(results):
    valid_count = 0
    invalid_count = 0
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}TOKEN CHECKER RESULTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    for i, result in enumerate(results, 1):
        print(f"\n{Fore.WHITE}Token #{i}:{Style.RESET_ALL}")
        print(f"Token: {result['token'][:50]}...")
        
        if result['valid']:
            valid_count += 1
            print(f"{Fore.GREEN}Status: VALID{Style.RESET_ALL}")
            print(f"Username: {result['username']}#{result['discriminator']}")
            print(f"ID: {result['id']}")
            print(f"Email: {result['email']}")
            print(f"Verified: {result['verified']}")
            print(f"MFA Enabled: {result['mfa_enabled']}")
            print(f"Premium Type: {result['premium_type']}")
            print(f"Phone: {result['phone']}")
        else:
            invalid_count += 1
            print(f"{Fore.RED}Status: INVALID{Style.RESET_ALL}")
            print(f"Reason: {result['reason']}")
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Valid tokens: {valid_count}{Style.RESET_ALL}")
    print(f"{Fore.RED}Invalid tokens: {invalid_count}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Total tokens: {len(results)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def run_token_checker():
    print(f"{Fore.CYAN}Token Checker{Style.RESET_ALL}")
    print("1. Single token check")
    print("2. Multiple tokens check")
    print("3. Load tokens from file")
    
    choice = input(f"{Fore.YELLOW}Select option (1-3): {Style.RESET_ALL}").strip()
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    if choice == '1':
        token = input(f"{Fore.YELLOW}Enter Discord token: {Style.RESET_ALL}").strip()
        if token:
            result = check_token(token, debug)
            display_token_results([{**result, 'token': token}])
    
    elif choice == '2':
        tokens = []
        print(f"{Fore.YELLOW}Enter tokens (one per line, empty line to finish):{Style.RESET_ALL}")
        while True:
            token = input().strip()
            if not token:
                break
            tokens.append(token)
        
        if tokens:
            results = check_multiple_tokens(tokens, debug)
            display_token_results(results)
    
    elif choice == '3':
        filename = input(f"{Fore.YELLOW}Enter filename: {Style.RESET_ALL}").strip()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tokens = [line.strip() for line in f.readlines() if line.strip()]
            
            if tokens:
                results = check_multiple_tokens(tokens, debug)
                display_token_results(results)
            else:
                print(f"{Fore.RED}No tokens found in file{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}File not found{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error reading file: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}") 
# update
