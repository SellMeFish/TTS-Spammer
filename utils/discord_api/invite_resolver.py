import requests
import json
import re
from datetime import datetime
from colorama import Fore, Style, init

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def extract_invite_code(invite_input):
    patterns = [
        r'discord\.gg/([a-zA-Z0-9]+)',
        r'discord\.com/invite/([a-zA-Z0-9]+)',
        r'discordapp\.com/invite/([a-zA-Z0-9]+)',
        r'^([a-zA-Z0-9]+)$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, invite_input)
        if match:
            return match.group(1)
    return None

def resolve_invite(invite_code, token=None):
    print_colored(f"[INFO] Resolving invite: {invite_code}", Fore.CYAN)
    
    url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    if token:
        headers['Authorization'] = f'Bot {token}' if not token.startswith('Bot ') else token
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_colored("[SUCCESS] Invite resolved successfully", Fore.GREEN)
            return data
        elif response.status_code == 404:
            print_colored("[ERROR] Invite not found or expired", Fore.RED)
            return None
        elif response.status_code == 429:
            print_colored("[ERROR] Rate limited", Fore.RED)
            return None
        else:
            print_colored(f"[ERROR] API returned status {response.status_code}", Fore.RED)
            return None
            
    except Exception as e:
        print_colored(f"[ERROR] Request failed: {str(e)}", Fore.RED)
        return None

def get_server_icon_url(guild_data):
    if not guild_data.get('icon'):
        return None
    
    guild_id = guild_data['id']
    icon_hash = guild_data['icon']
    extension = 'gif' if icon_hash.startswith('a_') else 'png'
    
    return f"https://cdn.discordapp.com/icons/{guild_id}/{icon_hash}.{extension}?size=1024"

def get_server_banner_url(guild_data):
    if not guild_data.get('banner'):
        return None
    
    guild_id = guild_data['id']
    banner_hash = guild_data['banner']
    extension = 'gif' if banner_hash.startswith('a_') else 'png'
    
    return f"https://cdn.discordapp.com/banners/{guild_id}/{banner_hash}.{extension}?size=1024"

def get_server_splash_url(guild_data):
    if not guild_data.get('splash'):
        return None
    
    guild_id = guild_data['id']
    splash_hash = guild_data['splash']
    
    return f"https://cdn.discordapp.com/splashes/{guild_id}/{splash_hash}.png?size=1024"

def format_verification_level(level):
    levels = {
        0: "None",
        1: "Low",
        2: "Medium", 
        3: "High",
        4: "Very High"
    }
    return levels.get(level, "Unknown")

def format_nsfw_level(level):
    levels = {
        0: "Default",
        1: "Explicit",
        2: "Safe",
        3: "Age Restricted"
    }
    return levels.get(level, "Unknown")

def format_premium_tier(tier):
    tiers = {
        0: "No Boost",
        1: "Tier 1",
        2: "Tier 2", 
        3: "Tier 3"
    }
    return tiers.get(tier, "Unknown")

def snowflake_to_timestamp(snowflake):
    try:
        timestamp = ((int(snowflake) >> 22) + 1420070400000) / 1000
        return datetime.fromtimestamp(timestamp)
    except:
        return None

def display_invite_info(invite_data):
    if not invite_data:
        print_colored("[ERROR] No invite data to display!", Fore.RED)
        return
    
    print_colored("\n" + "=" * 70, Fore.CYAN)
    print_colored("                INVITE INFORMATION", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    
    invite_code = invite_data.get('code', 'Unknown')
    print_colored(f"\nInvite Code: {invite_code}", Fore.WHITE)
    print_colored(f"Invite URL: https://discord.gg/{invite_code}", Fore.BLUE)
    
    guild = invite_data.get('guild')
    if guild:
        print_colored(f"\n--- SERVER INFORMATION ---", Fore.YELLOW)
        print_colored(f"Server Name: {guild.get('name', 'Unknown')}", Fore.WHITE)
        print_colored(f"Server ID: {guild.get('id', 'Unknown')}", Fore.YELLOW)
        
        creation_date = snowflake_to_timestamp(guild.get('id'))
        if creation_date:
            print_colored(f"Created: {creation_date.strftime('%Y-%m-%d %H:%M:%S UTC')}", Fore.CYAN)
            days_old = (datetime.now() - creation_date).days
            print_colored(f"Age: {days_old} days", Fore.CYAN)
        
        description = guild.get('description')
        if description:
            print_colored(f"Description: {description}", Fore.CYAN)
        
        verification_level = format_verification_level(guild.get('verification_level', 0))
        print_colored(f"Verification Level: {verification_level}", Fore.MAGENTA)
        
        nsfw_level = format_nsfw_level(guild.get('nsfw_level', 0))
        print_colored(f"NSFW Level: {nsfw_level}", Fore.MAGENTA)
        
        premium_tier = format_premium_tier(guild.get('premium_tier', 0))
        print_colored(f"Boost Level: {premium_tier}", Fore.MAGENTA)
        
        if guild.get('premium_subscription_count'):
            print_colored(f"Boost Count: {guild['premium_subscription_count']}", Fore.MAGENTA)
        
        vanity_url = guild.get('vanity_url_code')
        if vanity_url:
            print_colored(f"Vanity URL: discord.gg/{vanity_url}", Fore.BLUE)
        
        features = guild.get('features', [])
        if features:
            print_colored(f"Features: {', '.join(features)}", Fore.GREEN)
        
        icon_url = get_server_icon_url(guild)
        if icon_url:
            print_colored(f"Icon URL: {icon_url}", Fore.BLUE)
        
        banner_url = get_server_banner_url(guild)
        if banner_url:
            print_colored(f"Banner URL: {banner_url}", Fore.BLUE)
        
        splash_url = get_server_splash_url(guild)
        if splash_url:
            print_colored(f"Splash URL: {splash_url}", Fore.BLUE)
    
    channel = invite_data.get('channel')
    if channel:
        print_colored(f"\n--- CHANNEL INFORMATION ---", Fore.YELLOW)
        print_colored(f"Channel Name: #{channel.get('name', 'Unknown')}", Fore.WHITE)
        print_colored(f"Channel ID: {channel.get('id', 'Unknown')}", Fore.YELLOW)
        
        channel_type = channel.get('type', 0)
        type_names = {0: "Text", 1: "DM", 2: "Voice", 3: "Group DM", 4: "Category", 5: "News", 10: "News Thread", 11: "Public Thread", 12: "Private Thread", 13: "Stage Voice", 15: "Forum"}
        print_colored(f"Channel Type: {type_names.get(channel_type, 'Unknown')}", Fore.CYAN)
    
    inviter = invite_data.get('inviter')
    if inviter:
        print_colored(f"\n--- INVITER INFORMATION ---", Fore.YELLOW)
        username = inviter.get('username', 'Unknown')
        discriminator = inviter.get('discriminator', '0')
        global_name = inviter.get('global_name')
        
        if discriminator == '0':
            display_name = f"@{username}"
            if global_name:
                display_name = f"{global_name} (@{username})"
        else:
            display_name = f"{username}#{discriminator}"
        
        print_colored(f"Inviter: {display_name}", Fore.WHITE)
        print_colored(f"Inviter ID: {inviter.get('id', 'Unknown')}", Fore.YELLOW)
    
    approximate_member_count = invite_data.get('approximate_member_count')
    if approximate_member_count is not None:
        print_colored(f"\n--- MEMBER STATISTICS ---", Fore.YELLOW)
        print_colored(f"Total Members: {approximate_member_count:,}", Fore.GREEN)
    
    approximate_presence_count = invite_data.get('approximate_presence_count')
    if approximate_presence_count is not None:
        print_colored(f"Online Members: {approximate_presence_count:,}", Fore.GREEN)
    
    expires_at = invite_data.get('expires_at')
    if expires_at:
        print_colored(f"\n--- EXPIRATION ---", Fore.YELLOW)
        print_colored(f"Expires At: {expires_at}", Fore.RED)
    else:
        print_colored(f"\n--- EXPIRATION ---", Fore.YELLOW)
        print_colored("Expires: Never", Fore.GREEN)
    
    uses = invite_data.get('uses')
    max_uses = invite_data.get('max_uses')
    if uses is not None:
        print_colored(f"\n--- USAGE STATISTICS ---", Fore.YELLOW)
        print_colored(f"Uses: {uses}", Fore.CYAN)
        if max_uses:
            print_colored(f"Max Uses: {max_uses}", Fore.CYAN)
        else:
            print_colored("Max Uses: Unlimited", Fore.GREEN)

def save_invite_info(invite_data, filename=None):
    if not filename:
        invite_code = invite_data.get('code', 'unknown')
        filename = f"invite_{invite_code}_info.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(invite_data, f, indent=2, ensure_ascii=False)
        print_colored(f"[SUCCESS] Invite info saved to {filename}", Fore.GREEN)
    except Exception as e:
        print_colored(f"[ERROR] Failed to save invite info: {str(e)}", Fore.RED)

def run_invite_resolver():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("              DISCORD INVITE RESOLVER", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nEnter Discord invite link or code:", Fore.WHITE)
        invite_input = input(f"{Fore.WHITE}Invite: {Style.RESET_ALL}").strip()
        
        if not invite_input:
            print_colored("[ERROR] No invite provided!", Fore.RED)
            continue
        
        invite_code = extract_invite_code(invite_input)
        if not invite_code:
            print_colored("[ERROR] Invalid invite format!", Fore.RED)
            continue
        
        print_colored("\nOptional: Enter Discord token for extended info (press Enter to skip):", Fore.YELLOW)
        token = input(f"{Fore.WHITE}Token: {Style.RESET_ALL}").strip()
        
        invite_data = resolve_invite(invite_code, token if token else None)
        
        if invite_data:
            display_invite_info(invite_data)
            
            save_choice = input(f"\n{Fore.WHITE}Save invite info to file? (y/n): {Style.RESET_ALL}").strip().lower()
            if save_choice == 'y':
                filename = input(f"{Fore.WHITE}Enter filename (press Enter for default): {Style.RESET_ALL}").strip()
                save_invite_info(invite_data, filename if filename else None)
        
        continue_choice = input(f"\n{Fore.WHITE}Resolve another invite? (y/n): {Style.RESET_ALL}").strip().lower()
        if continue_choice != 'y':
            break
    
    print_colored("Exiting invite resolver...", Fore.YELLOW)

if __name__ == "__main__":
    run_invite_resolver() 