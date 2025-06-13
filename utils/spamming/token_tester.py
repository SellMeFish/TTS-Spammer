import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

def test_discord_token(token):
    """Test if a Discord token is valid and get user info"""
    
    # Clean up token
    token = token.strip()
    
    # Format token properly
    if not token.startswith('Bot ') and not token.startswith('Bearer '):
        auth_token = token
    else:
        auth_token = token
    
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"{Fore.CYAN}Testing Discord Token...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Token (first 20 chars): {token[:20]}...{Style.RESET_ALL}")
    
    try:
        # Test token by getting user info
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
        
        print(f"{Fore.CYAN}Status Code: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"{Fore.GREEN}✓ Token is VALID{Style.RESET_ALL}")
            print(f"{Fore.CYAN}User: {user_data.get('username')}#{user_data.get('discriminator')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}ID: {user_data.get('id')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Verified: {user_data.get('verified')}{Style.RESET_ALL}")
            return True
        elif response.status_code == 401:
            print(f"{Fore.RED}✗ Token is INVALID or EXPIRED{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Check your token format and validity{Style.RESET_ALL}")
            return False
        elif response.status_code == 429:
            print(f"{Fore.YELLOW}⚠ Rate Limited - Wait before testing again{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.RED}✗ Unexpected status: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.RED}Response: {response.text[:200]}{Style.RESET_ALL}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}✗ Connection timeout{Style.RESET_ALL}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}✗ Connection error - Check internet connection{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
        return False

def test_channel_access(token, channel_id):
    """Test if token can access a specific channel"""
    
    token = token.strip()
    if not token.startswith('Bot ') and not token.startswith('Bearer '):
        auth_token = token
    else:
        auth_token = token
    
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n{Fore.CYAN}Testing Channel Access...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Channel ID: {channel_id}{Style.RESET_ALL}")
    
    try:
        # Test channel access
        response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers, timeout=10)
        
        print(f"{Fore.CYAN}Status Code: {response.status_code}{Style.RESET_ALL}")
        
        if response.status_code == 200:
            channel_data = response.json()
            print(f"{Fore.GREEN}✓ Channel access GRANTED{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Channel: #{channel_data.get('name', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Type: {channel_data.get('type', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Guild ID: {channel_data.get('guild_id', 'DM')}{Style.RESET_ALL}")
            return True
        elif response.status_code == 401:
            print(f"{Fore.RED}✗ Unauthorized - Invalid token{Style.RESET_ALL}")
            return False
        elif response.status_code == 403:
            print(f"{Fore.RED}✗ Forbidden - No permission to access channel{Style.RESET_ALL}")
            return False
        elif response.status_code == 404:
            print(f"{Fore.RED}✗ Channel not found{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.RED}✗ Unexpected status: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.RED}Response: {response.text[:200]}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
        return False

def run_token_test():
    """Main function to run token tests"""
    
    print(f"{Fore.CYAN}════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.CYAN}        Discord Token Tester Tool        {Style.RESET_ALL}")
    print(f"{Fore.CYAN}════════════════════════════════════════{Style.RESET_ALL}")
    
    token = input(f"\n{Fore.YELLOW}Enter Discord Token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}No token provided!{Style.RESET_ALL}")
        return
    
    # Test token validity
    if test_discord_token(token):
        print(f"\n{Fore.GREEN}Token is working!{Style.RESET_ALL}")
        
        # Test channel access
        channel_id = input(f"\n{Fore.YELLOW}Enter Channel ID to test (optional): {Style.RESET_ALL}").strip()
        if channel_id:
            test_channel_access(token, channel_id)
    else:
        print(f"\n{Fore.RED}Token test failed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Common issues:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Token is invalid or expired{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Wrong token format{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Account is disabled{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Connection issues{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    run_token_test() 