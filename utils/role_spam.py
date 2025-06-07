

import requests
import time
import json
import random
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

ROLE_NAMES = [
    "💀 DEATH ROLE 💀",
    "🔥 FIRE MASTER 🔥",
    "⚡ ELECTRIC SHOCK ⚡",
    "💥 EXPLOSION EXPERT 💥",
    "🌪️ TORNADO RIDER 🌪️",
    "🎯 TARGET DESTROYER 🎯",
    "🚀 ROCKET LAUNCHER 🚀",
    "⭐ STAR KILLER ⭐",
    "🌈 RAINBOW WARRIOR 🌈",
    "💎 DIAMOND CRUSHER 💎",
    "🔮 MYSTIC DESTROYER 🔮",
    "🎪 CHAOS MASTER 🎪",
    "🎲 DICE ROLLER 🎲",
    "🎨 ART DESTROYER 🎨",
    "🎵 SOUND KILLER 🎵",
    "🎮 GAME BREAKER 🎮",
    "📱 PHONE HACKER 📱",
    "💻 VIRUS CREATOR 💻",
    "🖥️ SYSTEM CRASHER 🖥️",
    "⌨️ KEYBOARD SMASHER ⌨️"
]

CHAOS_ADJECTIVES = [
    "ULTIMATE", "SUPREME", "MEGA", "SUPER", "HYPER", "ULTRA", "EXTREME",
    "MAXIMUM", "INFINITE", "ETERNAL", "LEGENDARY", "MYTHICAL", "EPIC",
    "GODLIKE", "DIVINE", "COSMIC", "NUCLEAR", "ATOMIC", "QUANTUM", "CHAOS"
]

CHAOS_NOUNS = [
    "DESTROYER", "ANNIHILATOR", "OBLITERATOR", "TERMINATOR", "ELIMINATOR",
    "DEVASTATOR", "CRUSHER", "SMASHER", "BREAKER", "KILLER", "SLAYER",
    "WARRIOR", "MASTER", "LORD", "KING", "EMPEROR", "GOD", "DEMON",
    "BEAST", "MONSTER", "NIGHTMARE", "PHANTOM", "SHADOW", "VOID"
]

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

def generate_random_role_name():
    patterns = [
        lambda: random.choice(ROLE_NAMES),
        lambda: f"{random.choice(CHAOS_ADJECTIVES)} {random.choice(CHAOS_NOUNS)}",
        lambda: f"🎭 {random.choice(CHAOS_ADJECTIVES)} {random.choice(CHAOS_NOUNS)} 🎭",
        lambda: f"💀 {random.choice(CHAOS_NOUNS)} OF {random.choice(CHAOS_ADJECTIVES)} CHAOS 💀",
        lambda: "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20)),
        lambda: "💀" * random.randint(5, 15),
        lambda: "🔥" * random.randint(5, 15),
        lambda: "⚡" * random.randint(5, 15),
        lambda: f"ROLE-{random.randint(1000, 9999)}-CHAOS",
        lambda: f"SPAM-{random.randint(100, 999)}-ROLE"
    ]
    
    return random.choice(patterns)()

def generate_random_permissions():
    permissions = 0
    
    for perm_name, perm_bit in PERMISSIONS.items():
        if random.random() < 0.3:
            permissions |= perm_bit
    
    return permissions

def create_single_role(token, guild_id, name=None, permissions=None, color=None):
    headers = get_headers(token)
    
    if not name:
        name = generate_random_role_name()
    
    if permissions is None:
        permissions = generate_random_permissions()
    
    if color is None:
        color = random.randint(0, 16777215)
    
    role_data = {
        'name': name,
        'permissions': str(permissions),
        'color': color,
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
            pretty_print(f"✅ Created role: {role['name']}", (0,255,0))
            return role
        else:
            pretty_print(f"❌ Failed to create role {name}: {response.status_code}", (255,0,0))
            return None
    except Exception as e:
        pretty_print(f"❌ Error creating role {name}: {str(e)}", (255,0,0))
        return None

def mass_create_roles(token, guild_id, count):
    pretty_print(f"🎭 Creating {count} roles...", (255,128,0))
    
    created_count = 0
    failed_count = 0
    
    def create_role_worker(i):
        role = create_single_role(token, guild_id)
        if role:
            return 1, 0
        else:
            return 0, 1
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_role_worker, i) for i in range(count)]
        for future in as_completed(futures):
            created, failed = future.result()
            created_count += created
            failed_count += failed
            time.sleep(1)
    
    pretty_print(f"🎭 Role creation completed: {created_count} created, {failed_count} failed", (255,255,0))
    return created_count, failed_count

def create_admin_roles(token, guild_id, count=20):
    pretty_print(f"👑 Creating {count} admin roles...", (255,128,0))
    
    admin_names = [
        "👑 SUPREME ADMIN 👑",
        "💀 DEATH ADMIN 💀",
        "🔥 FIRE ADMIN 🔥",
        "⚡ ELECTRIC ADMIN ⚡",
        "💥 EXPLOSIVE ADMIN 💥",
        "🌪️ TORNADO ADMIN 🌪️",
        "🎯 TARGET ADMIN 🎯",
        "🚀 ROCKET ADMIN 🚀",
        "⭐ STAR ADMIN ⭐",
        "🌈 RAINBOW ADMIN 🌈"
    ]
    
    created_count = 0
    
    for i in range(count):
        name = f"{random.choice(admin_names)} #{i+1:02d}"
        admin_permissions = PERMISSIONS['ADMINISTRATOR']
        color = random.randint(0, 16777215)
        
        if create_single_role(token, guild_id, name, admin_permissions, color):
            created_count += 1
        
        time.sleep(1)
    
    pretty_print(f"👑 Created {created_count}/{count} admin roles", (255,255,0))
    return created_count

def create_rainbow_roles(token, guild_id, count=50):
    pretty_print(f"🌈 Creating {count} rainbow roles...", (255,128,0))
    
    rainbow_colors = [
        0xFF0000,
        0xFF8000,
        0xFFFF00,
        0x80FF00,
        0x00FF00,
        0x00FF80,
        0x00FFFF,
        0x0080FF,
        0x0000FF,
        0x8000FF,
        0xFF00FF,
        0xFF0080
    ]
    
    created_count = 0
    
    for i in range(count):
        color = rainbow_colors[i % len(rainbow_colors)]
        name = f"🌈 RAINBOW {i+1:03d} 🌈"
        
        if create_single_role(token, guild_id, name, 0, color):
            created_count += 1
        
        time.sleep(0.8)
    
    pretty_print(f"🌈 Created {created_count}/{count} rainbow roles", (255,255,0))
    return created_count

def create_spam_roles(token, guild_id, count=100):
    pretty_print(f"📛 Creating {count} spam roles...", (255,128,0))
    
    spam_patterns = [
        lambda i: "💀" * (i % 20 + 1),
        lambda i: "🔥" * (i % 15 + 1),
        lambda i: "⚡" * (i % 10 + 1),
        lambda i: f"SPAM-{i:04d}",
        lambda i: f"ROLE-{random.randint(1000, 9999)}",
        lambda i: "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=15)),
        lambda i: f"💥-{i:03d}-💥",
        lambda i: f"🌪️-{i:03d}-🌪️"
    ]
    
    created_count = 0
    
    def create_spam_worker(i):
        pattern = random.choice(spam_patterns)
        name = pattern(i)
        
        if create_single_role(token, guild_id, name):
            return 1
        return 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(create_spam_worker, i) for i in range(count)]
        for future in as_completed(futures):
            created_count += future.result()
            time.sleep(0.5)
    
    pretty_print(f"📛 Created {created_count}/{count} spam roles", (255,255,0))
    return created_count

def create_numbered_roles(token, guild_id, count=200):
    pretty_print(f"🔢 Creating {count} numbered roles...", (255,128,0))
    
    created_count = 0
    
    for i in range(count):
        name = f"ROLE-{i+1:04d}-CHAOS"
        
        if create_single_role(token, guild_id, name):
            created_count += 1
        
        time.sleep(0.3)
    
    pretty_print(f"🔢 Created {created_count}/{count} numbered roles", (255,255,0))
    return created_count

def run_role_spam():
    pretty_print("🎭 ROLE SPAM - MASS CREATION TOOL 🎭", (255,0,0))
    pretty_print("Creates unlimited roles with random names and permissions", (255,128,0))
    
    token = input("\n🔑 Enter Discord token: ").strip()
    if not token:
        pretty_print("❌ No token provided!", (255,0,0))
        return
    
    guild_id = input("🏠 Enter Server ID: ").strip()
    if not guild_id:
        pretty_print("❌ No server ID provided!", (255,0,0))
        return
    
    while True:
        pretty_print("\n🎭 Role Spam Options:", (255,128,0))
        questions = [
            inquirer.List('action',
                         message="Select role creation type:",
                         choices=[
                             '🎭 Mass Create Random Roles',
                             '👑 Create Admin Roles',
                             '🌈 Create Rainbow Roles',
                             '📛 Create Spam Roles',
                             '🔢 Create Numbered Roles',
                             '💥 ULTIMATE ROLE SPAM',
                             '🚪 Back to Main Menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            break
        
        action = answers['action']
        
        if action == '🚪 Back to Main Menu':
            break
        
        if action == '🎭 Mass Create Random Roles':
            count = input("Enter number of random roles to create (1-250): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 250:
                    mass_create_roles(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-250)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '👑 Create Admin Roles':
            count = input("Enter number of admin roles to create (1-50): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 50:
                    create_admin_roles(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-50)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🌈 Create Rainbow Roles':
            count = input("Enter number of rainbow roles to create (1-100): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 100:
                    create_rainbow_roles(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-100)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '📛 Create Spam Roles':
            count = input("Enter number of spam roles to create (1-200): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 200:
                    create_spam_roles(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-200)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🔢 Create Numbered Roles':
            count = input("Enter number of numbered roles to create (1-300): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 300:
                    create_numbered_roles(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-300)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '💥 ULTIMATE ROLE SPAM':
            pretty_print("💥 ULTIMATE SPAM - MAXIMUM ROLE CREATION!", (255,0,0))
            pretty_print("⚠️ This will create 500+ roles!", (255,255,0))
            
            confirm1 = input("Type 'SPAM' to confirm: ").strip()
            if confirm1 != 'SPAM':
                pretty_print("❌ Operation cancelled", (255,255,0))
                continue
            
            confirm2 = input("Type 'ROLES' to proceed: ").strip()
            if confirm2 != 'ROLES':
                pretty_print("❌ Operation cancelled", (255,255,0))
                continue
            
            pretty_print("\n💥 INITIATING ULTIMATE ROLE SPAM...", (255,0,0))
            time.sleep(2)
            
            pretty_print("🚀 Phase 1: Random Roles", (255,128,0))
            mass_create_roles(token, guild_id, 150)
            
            pretty_print("🚀 Phase 2: Admin Roles", (255,128,0))
            create_admin_roles(token, guild_id, 30)
            
            pretty_print("🚀 Phase 3: Rainbow Roles", (255,128,0))
            create_rainbow_roles(token, guild_id, 60)
            
            pretty_print("🚀 Phase 4: Spam Roles", (255,128,0))
            create_spam_roles(token, guild_id, 150)
            
            pretty_print("🚀 Phase 5: Numbered Roles", (255,128,0))
            create_numbered_roles(token, guild_id, 200)
            
            pretty_print("\n💥 ULTIMATE ROLE SPAM COMPLETED! 💥", (255,0,0))
            pretty_print("🎭 Server flooded with 500+ roles!", (255,255,0))
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_role_spam() 
# update
