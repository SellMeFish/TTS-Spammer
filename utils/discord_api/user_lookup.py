import requests
import json
import time
from colorama import Fore, Style, init

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def get_user_info(user_id, token=None):
    try:
        url = f"https://discord.com/api/v9/users/{user_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        if token:
            headers['Authorization'] = token
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {'error': 'User not found'}
        elif response.status_code == 401:
            return {'error': 'Invalid token or unauthorized'}
        else:
            return {'error': f'API error: {response.status_code}'}
            
    except Exception as e:
        return {'error': f'Request failed: {str(e)}'}

def get_user_profile(user_id, token=None):
    try:
        url = f"https://discord.com/api/v9/users/{user_id}/profile"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        if token:
            headers['Authorization'] = token
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception:
        return None

def get_mutual_guilds(user_id, token):
    try:
        url = f"https://discord.com/api/v9/users/{user_id}/relationships"
        headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
            
    except Exception:
        return []

def format_timestamp(timestamp):
    if not timestamp:
        return "Unknown"
    
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp

def display_user_info(user_data, profile_data=None):
    if 'error' in user_data:
        print_colored(f"[ERROR] {user_data['error']}", Fore.RED)
        return
    
    print_colored("=" * 80, Fore.CYAN)
    print_colored("👤 DISCORD USER INFORMATION", Fore.WHITE)
    print_colored("=" * 80, Fore.CYAN)
    
    username = user_data.get('username', 'Unknown')
    discriminator = user_data.get('discriminator', '0000')
    global_name = user_data.get('global_name')
    
    if global_name:
        print_colored(f"🏷️  Display Name: {global_name}", Fore.GREEN)
        print_colored(f"👤 Username: {username}#{discriminator}", Fore.WHITE)
    else:
        print_colored(f"👤 Username: {username}#{discriminator}", Fore.WHITE)
    
    print_colored(f"🆔 User ID: {user_data.get('id', 'Unknown')}", Fore.YELLOW)
    
    if user_data.get('avatar'):
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png?size=512"
        print_colored(f"🖼️  Avatar: {avatar_url}", Fore.BLUE)
    else:
        print_colored("🖼️  Avatar: Default Discord Avatar", Fore.CYAN)
    
    if user_data.get('banner'):
        banner_url = f"https://cdn.discordapp.com/banners/{user_data['id']}/{user_data['banner']}.png?size=1024"
        print_colored(f"🎨 Banner: {banner_url}", Fore.MAGENTA)
    
    flags = user_data.get('public_flags', 0)
    badges = []
    
    flag_meanings = {
        1: "Discord Employee",
        2: "Partnered Server Owner",
        4: "HypeSquad Events",
        8: "Bug Hunter Level 1",
        64: "House Bravery",
        128: "House Brilliance",
        256: "House Balance",
        512: "Early Nitro Supporter",
        1024: "Team User",
        4096: "Bug Hunter Level 2",
        8192: "Verified Bot",
        16384: "Early Verified Bot Developer",
        131072: "Discord Certified Moderator",
        1048576: "Bot HTTP Interactions",
        4194304: "Active Developer"
    }
    
    for flag_value, meaning in flag_meanings.items():
        if flags & flag_value:
            badges.append(meaning)
    
    if badges:
        print_colored(f"🏅 Badges: {', '.join(badges)}", Fore.YELLOW)
    
    if user_data.get('bot'):
        print_colored("🤖 Account Type: Bot", Fore.MAGENTA)
    else:
        print_colored("👨 Account Type: User", Fore.GREEN)
    
    if user_data.get('system'):
        print_colored("⚙️  System Account: Yes", Fore.RED)
    
    if user_data.get('verified') is not None:
        status = "Yes" if user_data['verified'] else "No"
        print_colored(f"✅ Verified: {status}", Fore.GREEN if user_data['verified'] else Fore.RED)
    
    if profile_data:
        print_colored("\n📋 PROFILE INFORMATION", Fore.CYAN)
        print_colored("-" * 40, Fore.CYAN)
        
        user_profile = profile_data.get('user', {})
        
        if user_profile.get('bio'):
            print_colored(f"📝 Bio: {user_profile['bio']}", Fore.WHITE)
        
        if user_profile.get('accent_color'):
            print_colored(f"🎨 Accent Color: #{user_profile['accent_color']:06x}", Fore.MAGENTA)
        
        premium_type = user_profile.get('premium_type')
        if premium_type:
            premium_types = {1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}
            print_colored(f"💎 Nitro: {premium_types.get(premium_type, 'Unknown')}", Fore.YELLOW)
        
        connected_accounts = profile_data.get('connected_accounts', [])
        if connected_accounts:
            print_colored("\n🔗 CONNECTED ACCOUNTS", Fore.CYAN)
            for account in connected_accounts:
                platform = account.get('type', 'Unknown').title()
                name = account.get('name', 'Unknown')
                verified = "✅" if account.get('verified') else "❌"
                print_colored(f"   {platform}: {name} {verified}", Fore.WHITE)
        
        mutual_guilds = profile_data.get('mutual_guilds', [])
        if mutual_guilds:
            print_colored(f"\n🏰 Mutual Servers: {len(mutual_guilds)}", Fore.CYAN)
            for guild in mutual_guilds[:5]:
                print_colored(f"   • {guild.get('name', 'Unknown Server')}", Fore.WHITE)
            if len(mutual_guilds) > 5:
                print_colored(f"   ... and {len(mutual_guilds) - 5} more", Fore.YELLOW)

def lookup_multiple_users(user_ids, token=None):
    print_colored(f"[INFO] Looking up {len(user_ids)} users...", Fore.CYAN)
    
    results = []
    for i, user_id in enumerate(user_ids, 1):
        print_colored(f"[{i}/{len(user_ids)}] Looking up user {user_id}...", Fore.YELLOW)
        
        user_data = get_user_info(user_id, token)
        profile_data = get_user_profile(user_id, token) if token else None
        
        results.append({
            'user_id': user_id,
            'user_data': user_data,
            'profile_data': profile_data
        })
        
        time.sleep(0.5)
    
    return results

def save_lookup_results(results, filename="user_lookup_results.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print_colored(f"[SUCCESS] Results saved to {filename}", Fore.GREEN)
    except Exception as e:
        print_colored(f"[ERROR] Failed to save results: {str(e)}", Fore.RED)

def run_user_lookup():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("            DISCORD USER LOOKUP TOOL", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    print_colored("Get detailed information about Discord users", Fore.YELLOW)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nSelect lookup method:", Fore.WHITE)
        print_colored("1. Single User Lookup", Fore.YELLOW)
        print_colored("2. Multiple Users Lookup", Fore.YELLOW)
        print_colored("3. Bulk Lookup from File", Fore.YELLOW)
        print_colored("4. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-4): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            user_id = input(f"{Fore.WHITE}Enter Discord User ID: {Style.RESET_ALL}").strip()
            if not user_id.isdigit():
                print_colored("[ERROR] Invalid User ID! Must be numbers only.", Fore.RED)
                continue
            
            use_token = input(f"{Fore.WHITE}Use Discord token for detailed info? (y/n): {Style.RESET_ALL}").strip().lower()
            token = None
            
            if use_token == 'y':
                token = input(f"{Fore.WHITE}Enter Discord token: {Style.RESET_ALL}").strip()
                if not token.startswith(('Bot ', 'Bearer ')):
                    token = f"Bearer {token}" if not token.startswith('mfa.') else token
            
            print_colored(f"[INFO] Looking up user {user_id}...", Fore.CYAN)
            
            user_data = get_user_info(user_id, token)
            profile_data = get_user_profile(user_id, token) if token else None
            
            display_user_info(user_data, profile_data)
            
        elif choice == '2':
            user_ids_input = input(f"{Fore.WHITE}Enter User IDs (comma separated): {Style.RESET_ALL}").strip()
            user_ids = [uid.strip() for uid in user_ids_input.split(',') if uid.strip().isdigit()]
            
            if not user_ids:
                print_colored("[ERROR] No valid User IDs provided!", Fore.RED)
                continue
            
            use_token = input(f"{Fore.WHITE}Use Discord token for detailed info? (y/n): {Style.RESET_ALL}").strip().lower()
            token = None
            
            if use_token == 'y':
                token = input(f"{Fore.WHITE}Enter Discord token: {Style.RESET_ALL}").strip()
                if not token.startswith(('Bot ', 'Bearer ')):
                    token = f"Bearer {token}" if not token.startswith('mfa.') else token
            
            results = lookup_multiple_users(user_ids, token)
            
            print_colored("\n" + "=" * 80, Fore.CYAN)
            print_colored("LOOKUP RESULTS", Fore.WHITE)
            print_colored("=" * 80, Fore.CYAN)
            
            for result in results:
                display_user_info(result['user_data'], result['profile_data'])
                print_colored("\n" + "-" * 80 + "\n", Fore.CYAN)
            
            save_choice = input(f"{Fore.WHITE}Save results to file? (y/n): {Style.RESET_ALL}").strip().lower()
            if save_choice == 'y':
                filename = input(f"{Fore.WHITE}Filename (default: user_lookup_results.json): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "user_lookup_results.json"
                save_lookup_results(results, filename)
            
        elif choice == '3':
            filename = input(f"{Fore.WHITE}Enter filename with User IDs (one per line): {Style.RESET_ALL}").strip()
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    user_ids = [line.strip() for line in f if line.strip().isdigit()]
                
                if not user_ids:
                    print_colored("[ERROR] No valid User IDs found in file!", Fore.RED)
                    continue
                
                print_colored(f"[INFO] Found {len(user_ids)} User IDs in file", Fore.GREEN)
                
                use_token = input(f"{Fore.WHITE}Use Discord token for detailed info? (y/n): {Style.RESET_ALL}").strip().lower()
                token = None
                
                if use_token == 'y':
                    token = input(f"{Fore.WHITE}Enter Discord token: {Style.RESET_ALL}").strip()
                    if not token.startswith(('Bot ', 'Bearer ')):
                        token = f"Bearer {token}" if not token.startswith('mfa.') else token
                
                results = lookup_multiple_users(user_ids, token)
                
                output_filename = f"bulk_lookup_{int(time.time())}.json"
                save_lookup_results(results, output_filename)
                
                print_colored(f"[SUCCESS] Bulk lookup completed! Results saved to {output_filename}", Fore.GREEN)
                
            except FileNotFoundError:
                print_colored(f"[ERROR] File '{filename}' not found!", Fore.RED)
            except Exception as e:
                print_colored(f"[ERROR] Failed to read file: {str(e)}", Fore.RED)
            
        elif choice == '4':
            print_colored("Exiting User Lookup Tool...", Fore.YELLOW)
            break
            
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
            continue
        
        continue_choice = input(f"\n{Fore.WHITE}Continue with User Lookup? (y/n): {Style.RESET_ALL}").strip().lower()
        if continue_choice != 'y':
            break

if __name__ == "__main__":
    run_user_lookup() 