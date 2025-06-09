import requests
import time
import json
from colorama import Fore, Style, init

init()

def change_language(token, language_code, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'locale': language_code
    }
    
    try:
        response = requests.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Language Change Status: {response.status_code}{Style.RESET_ALL}")
        
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

def change_theme(token, theme, debug=False):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'theme': theme
    }
    
    try:
        response = requests.patch(
            'https://discord.com/api/v9/users/@me/settings',
            headers=headers,
            json=payload
        )
        
        if debug:
            print(f"{Fore.CYAN}[DEBUG] Theme Change Status: {response.status_code}{Style.RESET_ALL}")
        
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

def spam_language_changes(token, languages, amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for lang_idx, language in enumerate(languages):
            print(f"{Fore.YELLOW}Change {i+1}/{amount} - Language {lang_idx+1}/{len(languages)} ({language})...{Style.RESET_ALL}")
            
            result = change_language(token, language, debug)
            result['change_number'] = i + 1
            result['language'] = language
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Language changed to {language}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def spam_theme_changes(token, themes, amount=10, interval=1, debug=False):
    results = []
    
    for i in range(amount):
        for theme_idx, theme in enumerate(themes):
            print(f"{Fore.YELLOW}Change {i+1}/{amount} - Theme {theme_idx+1}/{len(themes)} ({theme})...{Style.RESET_ALL}")
            
            result = change_theme(token, theme, debug)
            result['change_number'] = i + 1
            result['theme'] = theme
            results.append(result)
            
            if result['success']:
                print(f"{Fore.GREEN}  ✓ Theme changed to {theme}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✗ Failed: {result['reason']}{Style.RESET_ALL}")
                if 'retry_after' in result:
                    time.sleep(result['retry_after'])
            
            time.sleep(interval)
    
    return results

def run_settings_spam():
    print(f"{Fore.CYAN}Settings Spam Tool{Style.RESET_ALL}")
    print("1. Spam language changes")
    print("2. Spam theme changes")
    print("3. Spam both language and theme")
    
    choice = input(f"{Fore.YELLOW}Select option (1-3): {Style.RESET_ALL}").strip()
    
    token = input(f"{Fore.YELLOW}Enter user token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided{Style.RESET_ALL}")
        return
    
    try:
        amount = int(input(f"{Fore.YELLOW}Number of changes: {Style.RESET_ALL}"))
    except ValueError:
        amount = 10
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between changes (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    languages = ['en-US', 'en-GB', 'de', 'fr', 'es-ES', 'ja', 'ko', 'zh-CN', 'zh-TW', 'ru']
    themes = ['dark', 'light']
    
    if choice == '1':
        results = spam_language_changes(token, languages, amount, interval, debug)
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful language changes{Style.RESET_ALL}")
    
    elif choice == '2':
        results = spam_theme_changes(token, themes, amount, interval, debug)
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful theme changes{Style.RESET_ALL}")
    
    elif choice == '3':
        print(f"{Fore.YELLOW}Spamming both language and theme changes...{Style.RESET_ALL}")
        
        lang_results = spam_language_changes(token, languages, amount // 2, interval, debug)
        theme_results = spam_theme_changes(token, themes, amount // 2, interval, debug)
        
        total_results = lang_results + theme_results
        success_count = sum(1 for r in total_results if r['success'])
        total_count = len(total_results)
        
        print(f"\n{Fore.CYAN}Results: {success_count}/{total_count} successful setting changes{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    run_settings_spam() 