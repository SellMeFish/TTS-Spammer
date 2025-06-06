#!/usr/bin/env python3

import requests
import time
import json
import random
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

PERMISSIONS = {
    'CREATE_INSTANT_INVITE': 1 << 0,
    'KICK_MEMBERS': 1 << 1,
    'BAN_MEMBERS': 1 << 2,
    'ADMINISTRATOR': 1 << 3,
    'MANAGE_CHANNELS': 1 << 4,
    'MANAGE_GUILD': 1 << 5,
    'ADD_REACTIONS': 1 << 6,
    'VIEW_AUDIT_LOG': 1 << 7,
    'PRIORITY_SPEAKER': 1 << 8,
    'STREAM': 1 << 9,
    'VIEW_CHANNEL': 1 << 10,
    'SEND_MESSAGES': 1 << 11,
    'SEND_TTS_MESSAGES': 1 << 12,
    'MANAGE_MESSAGES': 1 << 13,
    'EMBED_LINKS': 1 << 14,
    'ATTACH_FILES': 1 << 15,
    'READ_MESSAGE_HISTORY': 1 << 16,
    'MENTION_EVERYONE': 1 << 17,
    'USE_EXTERNAL_EMOJIS': 1 << 18,
    'VIEW_GUILD_INSIGHTS': 1 << 19,
    'CONNECT': 1 << 20,
    'SPEAK': 1 << 21,
    'MUTE_MEMBERS': 1 << 22,
    'DEAFEN_MEMBERS': 1 << 23,
    'MOVE_MEMBERS': 1 << 24,
    'USE_VAD': 1 << 25,
    'CHANGE_NICKNAME': 1 << 26,
    'MANAGE_NICKNAMES': 1 << 27,
    'MANAGE_ROLES': 1 << 28,
    'MANAGE_WEBHOOKS': 1 << 29,
    'MANAGE_EMOJIS': 1 << 30,
}

def get_all_roles(token, guild_id):
    """Get all roles from the server"""
    pretty_print("🎭 Fetching all server roles...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
    if response.status_code != 200:
        pretty_print(f"❌ Failed to get roles: {response.status_code}", (255,0,0))
        return []
    
    roles = response.json()
    pretty_print(f"✅ Found {len(roles)} roles", (0,255,0))
    return roles

def get_all_channels(token, guild_id):
    """Get all channels from the server"""
    pretty_print("📁 Fetching all server channels...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
    if response.status_code != 200:
        pretty_print(f"❌ Failed to get channels: {response.status_code}", (255,0,0))
        return []
    
    channels = response.json()
    pretty_print(f"✅ Found {len(channels)} channels", (0,255,0))
    return channels

def randomize_role_permissions(token, guild_id, role):
    """Randomize permissions for a single role"""
    if role['name'] == '@everyone':
        return False
    headers = get_headers(token)
    
    random_perms = 0
    for perm_name, perm_bit in PERMISSIONS.items():
        if random.choice([True, False]): 
            random_perms |= perm_bit
    
    role_data = {
        'permissions': str(random_perms)
    }
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}',
            headers=headers,
            json=role_data
        )
        if response.status_code == 200:
            pretty_print(f"✅ Randomized permissions for role: {role['name']}", (0,255,0))
            return True
        else:
            pretty_print(f"❌ Failed to update role {role['name']}: {response.status_code}", (255,0,0))
            return False
    except Exception as e:
        pretty_print(f"❌ Error updating role {role['name']}: {str(e)}", (255,0,0))
        return False

def chaos_channel_permissions(token, guild_id, channel, roles):
    """Create chaotic permission overwrites for a channel"""
    headers = get_headers(token)
    
    permission_overwrites = []
    
    selected_roles = random.sample(roles, min(5, len(roles)))
    
    for role in selected_roles:
        if role['name'] == '@everyone':
            continue
            
        allow_perms = 0
        deny_perms = 0
        
        for perm_name, perm_bit in PERMISSIONS.items():
            choice = random.choice(['allow', 'deny', 'neutral'])
            if choice == 'allow':
                allow_perms |= perm_bit
            elif choice == 'deny':
                deny_perms |= perm_bit
        
        permission_overwrites.append({
            'id': role['id'],
            'type': 0,  # Role
            'allow': str(allow_perms),
            'deny': str(deny_perms)
        })
    
    channel_data = {
        'permission_overwrites': permission_overwrites
    }
    
    try:
        response = requests.patch(
            f'https://discord.com/api/v9/channels/{channel["id"]}',
            headers=headers,
            json=channel_data
        )
        if response.status_code == 200:
            pretty_print(f"✅ Chaos permissions applied to: {channel['name']}", (0,255,0))
            return True
        else:
            pretty_print(f"❌ Failed to update channel {channel['name']}: {response.status_code}", (255,0,0))
            return False
    except Exception as e:
        pretty_print(f"❌ Error updating channel {channel['name']}: {str(e)}", (255,0,0))
        return False

def create_chaos_roles(token, guild_id, count=10):
    """Create multiple roles with chaotic permissions"""
    pretty_print(f"🎭 Creating {count} chaos roles...", (255,128,0))
    headers = get_headers(token)
    
    chaos_names = [
        "💀 CHAOS ADMIN 💀", "🔥 DESTROYER 🔥", "⚡ RANDOM POWER ⚡",
        "🌪️ PERMISSION STORM 🌪️", "💥 EXPLOSIVE ROLE 💥", "🎲 DICE ROLL 🎲",
        "🚀 ROCKET CHAOS 🚀", "⭐ STAR DESTROYER ⭐", "🌈 RAINBOW CHAOS 🌈",
        "💎 DIAMOND CHAOS 💎", "🔮 MYSTIC POWER 🔮", "🎪 CIRCUS MASTER 🎪"
    ]
    
    created_count = 0
    
    for i in range(count):
        random_perms = 0
        for perm_name, perm_bit in PERMISSIONS.items():
            if random.choice([True, False, False]):
                random_perms |= perm_bit
        
        random_color = random.randint(0, 16777215)
        
        role_data = {
            'name': random.choice(chaos_names) + f" #{i+1:02d}",
            'permissions': str(random_perms),
            'color': random_color,
            'hoist': random.choice([True, False]),
            'mentionable': random.choice([True, False])
        }
        
        try:
            response = requests.post(
                f'https://discord.com/api/v9/guilds/{guild_id}/roles',
                headers=headers,
                json=role_data
            )
            if response.status_code == 200:
                role = response.json()
                pretty_print(f"✅ Created chaos role: {role['name']}", (0,255,0))
                created_count += 1
            else:
                pretty_print(f"❌ Failed to create role: {response.status_code}", (255,0,0))
        except Exception as e:
            pretty_print(f"❌ Error creating role: {str(e)}", (255,0,0))
        
        time.sleep(1)
    
    pretty_print(f"🎭 Created {created_count}/{count} chaos roles", (255,255,0))
    return created_count

def assign_random_roles_to_members(token, guild_id, roles):
    """Assign random roles to all members"""
    pretty_print("👥 Assigning random roles to members...", (255,128,0))
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
    
    assignable_roles = [r for r in roles if r['name'] != '@everyone' and not r.get('managed', False)]
    
    assigned_count = 0
    
    for member in members[:50]:
        if member['user'].get('bot', False):
            continue
        
        num_roles = random.randint(1, min(5, len(assignable_roles)))
        selected_roles = random.sample(assignable_roles, num_roles)
        
        current_role_ids = member.get('roles', [])
        new_role_ids = list(set(current_role_ids + [r['id'] for r in selected_roles]))
        
        member_data = {
            'roles': new_role_ids
        }
        
        try:
            response = requests.patch(
                f'https://discord.com/api/v9/guilds/{guild_id}/members/{member["user"]["id"]}',
                headers=headers,
                json=member_data
            )
            if response.status_code == 200:
                pretty_print(f"✅ Assigned random roles to: {member['user']['username']}", (0,255,0))
                assigned_count += 1
            else:
                pretty_print(f"❌ Failed to assign roles to {member['user']['username']}: {response.status_code}", (255,0,0))
        except Exception as e:
            pretty_print(f"❌ Error assigning roles to {member['user']['username']}: {str(e)}", (255,0,0))
        
        time.sleep(2)
    
    pretty_print(f"👥 Assigned random roles to {assigned_count} members", (255,255,0))
    return assigned_count

def run_permission_chaos():
    """Main function for permission chaos"""
    pretty_print("🔒 PERMISSION CHAOS - ULTIMATE DISRUPTION 🔒", (255,0,0))
    pretty_print("=" * 60, (255,0,0))
    pretty_print("⚠️  WARNING: This will completely scramble all permissions! ⚠️", (255,255,0))
    pretty_print("The server will become completely chaotic!", (255,128,0))
    print()
    
    token = input("Enter Discord Token: ").strip()
    if not token:
        pretty_print("❌ No token provided!", (255,0,0))
        return
    guild_id = input("Enter Server/Guild ID: ").strip()
    if not guild_id:
        pretty_print("❌ No guild ID provided!", (255,0,0))
        return
    
    questions = [
        inquirer.List('confirm',
                     message="Are you sure you want to create PERMISSION CHAOS?",
                     choices=['No, cancel', 'Yes, CHAOS TIME!'],
                     ),
    ]
    answers = inquirer.prompt(questions)
    if not answers or answers['confirm'] != 'Yes, CHAOS TIME!':
        pretty_print("❌ Operation cancelled", (255,255,0))
        return
    
    final_confirm = input("Type 'CHAOS' to confirm permission destruction: ").strip()
    if final_confirm != 'CHAOS':
        pretty_print("❌ Operation cancelled", (255,255,0))
        return
    
    pretty_print("🔒 Starting permission chaos...", (255,0,0))
    print()
    
    roles = get_all_roles(token, guild_id)
    channels = get_all_channels(token, guild_id)
    
    if not roles or not channels:
        pretty_print("❌ Failed to get server data", (255,0,0))
        return
    
    results = {
        'roles_randomized': 0,
        'channels_chaosed': 0,
        'chaos_roles_created': 0,
        'members_assigned': 0
    }
    
    try:
        pretty_print("🎭 Phase 1: Randomizing existing role permissions...", (255,128,0))
        for role in roles:
            if randomize_role_permissions(token, guild_id, role):
                results['roles_randomized'] += 1
            time.sleep(1)
        
        pretty_print("🎭 Phase 2: Creating chaos roles...", (255,128,0))
        results['chaos_roles_created'] = create_chaos_roles(token, guild_id, 15)
        
        pretty_print("📁 Phase 3: Applying chaos to channel permissions...", (255,128,0))
        updated_roles = get_all_roles(token, guild_id)
        
        for channel in channels:
            if chaos_channel_permissions(token, guild_id, channel, updated_roles):
                results['channels_chaosed'] += 1
            time.sleep(1)
        
        pretty_print("👥 Phase 4: Assigning random roles to members...", (255,128,0))
        results['members_assigned'] = assign_random_roles_to_members(token, guild_id, updated_roles)
        
    except Exception as e:
        pretty_print(f"❌ Critical error during chaos: {str(e)}", (255,0,0))
    
    # Final results
    print()
    pretty_print("🔒 PERMISSION CHAOS COMPLETED 🔒", (255,0,0))
    pretty_print("=" * 50, (255,0,0))
    pretty_print(f"🎭 Existing roles randomized: {results['roles_randomized']}", (255,255,0))
    pretty_print(f"🎭 Chaos roles created: {results['chaos_roles_created']}", (255,255,0))
    pretty_print(f"📁 Channels with chaos permissions: {results['channels_chaosed']}", (255,255,0))
    pretty_print(f"👥 Members with random roles: {results['members_assigned']}", (255,255,0))
    print()
    pretty_print("The server permissions are now in complete chaos! 🔒💀", (255,0,0))
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    run_permission_chaos() 