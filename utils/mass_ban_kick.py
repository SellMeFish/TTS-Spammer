

import requests
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import inquirer
import random

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def get_all_members(token, guild_id):
    pretty_print("👥 Fetching all server members...", (255,128,0))
    headers = get_headers(token)
    members = []
    after = None
    
    while True:
        url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000'
        if after:
            url += f'&after={after}'
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            pretty_print(f"❌ Failed to get members: {response.status_code}", (255,0,0))
            break
        
        batch = response.json()
        if not batch:
            break
        
        members.extend(batch)
        after = batch[-1]['user']['id']
        pretty_print(f"📥 Fetched {len(members)} members so far...", (0,255,255))
        
        if len(batch) < 1000:
            break
        
        time.sleep(1)
    
    pretty_print(f"✅ Total members fetched: {len(members)}", (0,255,0))
    return members

def ban_member(token, guild_id, user_id, username, reason="Mass Ban", delete_days=7):
    headers = get_headers(token)
    
    ban_data = {
        'delete_message_days': delete_days,
        'reason': reason
    }
    
    try:
        response = requests.put(
            f'https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}',
            headers=headers,
            json=ban_data
        )
        if response.status_code == 204:
            pretty_print(f"✅ Banned: {username}", (0,255,0))
            return True
        else:
            pretty_print(f"❌ Failed to ban {username}: {response.status_code}", (255,0,0))
            return False
    except Exception as e:
        pretty_print(f"❌ Error banning {username}: {str(e)}", (255,0,0))
        return False

def kick_member(token, guild_id, user_id, username, reason="Mass Kick"):
    headers = get_headers(token)
    
    kick_data = {
        'reason': reason
    }
    
    try:
        response = requests.delete(
            f'https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}',
            headers=headers,
            json=kick_data
        )
        if response.status_code == 204:
            pretty_print(f"✅ Kicked: {username}", (0,255,0))
            return True
        else:
            pretty_print(f"❌ Failed to kick {username}: {response.status_code}", (255,0,0))
            return False
    except Exception as e:
        pretty_print(f"❌ Error kicking {username}: {str(e)}", (255,0,0))
        return False

def mass_ban_all(token, guild_id, members, reason="Mass Ban Operation", delete_days=7):
    pretty_print(f"🔨 Starting mass ban of {len(members)} members...", (255,128,0))
    
    banned_count = 0
    failed_count = 0
    
    def ban_worker(member):
        user_id = member['user']['id']
        username = member['user']['username']
        
        if ban_member(token, guild_id, user_id, username, reason, delete_days):
            return 1, 0
        else:
            return 0, 1
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(ban_worker, member) for member in members]
        for future in as_completed(futures):
            banned, failed = future.result()
            banned_count += banned
            failed_count += failed
            time.sleep(2)
    
    pretty_print(f"🔨 Mass ban completed: {banned_count} banned, {failed_count} failed", (255,255,0))
    return banned_count, failed_count

def mass_kick_all(token, guild_id, members, reason="Mass Kick Operation"):
    pretty_print(f"👢 Starting mass kick of {len(members)} members...", (255,128,0))
    
    kicked_count = 0
    failed_count = 0
    
    def kick_worker(member):
        user_id = member['user']['id']
        username = member['user']['username']
        
        if kick_member(token, guild_id, user_id, username, reason):
            return 1, 0
        else:
            return 0, 1
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(kick_worker, member) for member in members]
        for future in as_completed(futures):
            kicked, failed = future.result()
            kicked_count += kicked
            failed_count += failed
            time.sleep(1)
    
    pretty_print(f"👢 Mass kick completed: {kicked_count} kicked, {failed_count} failed", (255,255,0))
    return kicked_count, failed_count

def selective_ban_by_criteria(token, guild_id, members):
    pretty_print("🎯 Selective Ban - Choose criteria:", (255,128,0))
    
    questions = [
        inquirer.List('criteria',
                     message="Select ban criteria:",
                     choices=[
                         'Ban members without roles',
                         'Ban members joined recently (last 7 days)',
                         'Ban members with specific role',
                         'Ban random percentage of members',
                         'Ban members by username pattern'
                     ]),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        return 0, 0
    
    criteria = answers['criteria']
    targets = []
    
    if criteria == 'Ban members without roles':
        targets = [m for m in members if len(m.get('roles', [])) == 0]
        pretty_print(f"🎯 Found {len(targets)} members without roles", (255,255,0))
        
    elif criteria == 'Ban members joined recently (last 7 days)':
        import datetime
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        targets = []
        for member in members:
            try:
                joined_at = datetime.datetime.fromisoformat(member['joined_at'].replace('Z', '+00:00'))
                if joined_at > week_ago:
                    targets.append(member)
            except:
                continue
        pretty_print(f"🎯 Found {len(targets)} members who joined recently", (255,255,0))
        
    elif criteria == 'Ban members with specific role':
        role_name = input("Enter role name to target: ").strip()
        if role_name:
            targets = [m for m in members if any(role_name.lower() in r.get('name', '').lower() for r in m.get('roles', []))]
            pretty_print(f"🎯 Found {len(targets)} members with role containing '{role_name}'", (255,255,0))
        
    elif criteria == 'Ban random percentage of members':
        try:
            percentage = float(input("Enter percentage to ban (0-100): "))
            if 0 <= percentage <= 100:
                count = int(len(members) * percentage / 100)
                targets = random.sample(members, min(count, len(members)))
                pretty_print(f"🎯 Selected {len(targets)} random members ({percentage}%)", (255,255,0))
        except ValueError:
            pretty_print("❌ Invalid percentage", (255,0,0))
            return 0, 0
            
    elif criteria == 'Ban members by username pattern':
        pattern = input("Enter username pattern to match: ").strip().lower()
        if pattern:
            targets = [m for m in members if pattern in m['user']['username'].lower()]
            pretty_print(f"🎯 Found {len(targets)} members matching pattern '{pattern}'", (255,255,0))
    
    if not targets:
        pretty_print("❌ No targets found matching criteria", (255,0,0))
        return 0, 0
    
    confirm = input(f"Ban {len(targets)} members? (y/N): ").strip().lower()
    if confirm != 'y':
        pretty_print("❌ Operation cancelled", (255,255,0))
        return 0, 0
    
    return mass_ban_all(token, guild_id, targets, f"Selective Ban - {criteria}")

def ban_by_user_list(token, guild_id):
    pretty_print("📝 Ban by User List", (255,128,0))
    
    user_input = input("Enter user IDs (comma-separated) or file path: ").strip()
    user_ids = []
    
    if user_input.endswith('.txt'):
        try:
            with open(user_input, 'r') as f:
                user_ids = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            pretty_print("❌ File not found", (255,0,0))
            return 0, 0
    else:
        user_ids = [uid.strip() for uid in user_input.split(',') if uid.strip()]
    
    if not user_ids:
        pretty_print("❌ No user IDs provided", (255,0,0))
        return 0, 0
    
    pretty_print(f"🎯 Banning {len(user_ids)} users...", (255,128,0))
    
    banned_count = 0
    failed_count = 0
    
    for user_id in user_ids:
        if ban_member(token, guild_id, user_id, f"User-{user_id}", "Manual Ban List"):
            banned_count += 1
        else:
            failed_count += 1
        time.sleep(1)
    
    pretty_print(f"📝 List ban completed: {banned_count} banned, {failed_count} failed", (255,255,0))
    return banned_count, failed_count

def run_mass_ban_kick():
    pretty_print("🔨 MASS BAN/KICK MANAGER 🔨", (255,0,0))
    pretty_print("Advanced member management with multiple strategies", (255,128,0))
    
    token = input("\n🔑 Enter Discord token: ").strip()
    if not token:
        pretty_print("❌ No token provided!", (255,0,0))
        return
    
    guild_id = input("🏠 Enter Server ID: ").strip()
    if not guild_id:
        pretty_print("❌ No server ID provided!", (255,0,0))
        return
    
    while True:
        pretty_print("\n🔨 Mass Ban/Kick Options:", (255,128,0))
        questions = [
            inquirer.List('action',
                         message="Select action:",
                         choices=[
                             '🔨 Mass Ban All Members',
                             '👢 Mass Kick All Members',
                             '🎯 Selective Ban by Criteria',
                             '📝 Ban by User ID List',
                             '📊 Show Member Statistics',
                             '🚪 Back to Main Menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            break
        
        action = answers['action']
        
        if action == '🚪 Back to Main Menu':
            break
        elif action == '📊 Show Member Statistics':
            members = get_all_members(token, guild_id)
            if members:
                pretty_print(f"📊 Server Statistics:", (255,255,0))
                pretty_print(f"   👥 Total members: {len(members)}", (255,255,255))
                
                no_roles = len([m for m in members if len(m.get('roles', [])) == 0])
                pretty_print(f"   🎭 Members without roles: {no_roles}", (255,255,255))
                
                bots = len([m for m in members if m['user'].get('bot', False)])
                pretty_print(f"   🤖 Bot accounts: {bots}", (255,255,255))
                
                humans = len(members) - bots
                pretty_print(f"   👤 Human accounts: {humans}", (255,255,255))
            continue
        
        members = get_all_members(token, guild_id)
        if not members:
            pretty_print("❌ Failed to fetch members", (255,0,0))
            continue
        
        if action == '🔨 Mass Ban All Members':
            pretty_print(f"⚠️ WARNING: This will ban ALL {len(members)} members!", (255,255,0))
            confirm = input("Type 'BAN ALL' to confirm: ").strip()
            if confirm == 'BAN ALL':
                mass_ban_all(token, guild_id, members)
            else:
                pretty_print("❌ Operation cancelled", (255,255,0))
                
        elif action == '👢 Mass Kick All Members':
            pretty_print(f"⚠️ WARNING: This will kick ALL {len(members)} members!", (255,255,0))
            confirm = input("Type 'KICK ALL' to confirm: ").strip()
            if confirm == 'KICK ALL':
                mass_kick_all(token, guild_id, members)
            else:
                pretty_print("❌ Operation cancelled", (255,255,0))
                
        elif action == '🎯 Selective Ban by Criteria':
            selective_ban_by_criteria(token, guild_id, members)
            
        elif action == '📝 Ban by User ID List':
            ban_by_user_list(token, guild_id)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_mass_ban_kick() 
# update
