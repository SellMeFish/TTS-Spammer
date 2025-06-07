import requests
import time
import json
import os
import threading
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

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
    print(ansi + line + '\033[0m')

class GroupchatSpammerV2:
    def __init__(self, token, channel_id, message, amount, interval, threads=1):
        self.token = token
        self.channel_id = channel_id
        self.message = message
        self.amount = amount
        self.interval = interval
        self.threads = threads
        self.sent = 0
        self.errors = 0
        
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    def send_message(self, thread_id):
        """Sendet Nachrichten in einem Thread"""
        messages_per_thread = self.amount // self.threads
        if thread_id == 0:
            messages_per_thread += self.amount % self.threads
        
        for i in range(messages_per_thread):
            try:
                data = {'content': self.message}
                response = requests.post(self.url, headers=self.headers, json=data)
                
                if response.status_code == 200:
                    self.sent += 1
                    print(f"Thread {thread_id}: ✓ Message {self.sent}/{self.amount} sent")
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1)
                    print(f"Thread {thread_id}: ⏳ Rate limited, waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue
                else:
                    self.errors += 1
                    print(f"Thread {thread_id}: ✗ Error {response.status_code}")
                
                time.sleep(self.interval)
                
            except Exception as e:
                self.errors += 1
                print(f"Thread {thread_id}: ✗ Error: {str(e)}")
    
    def start_spam(self):
        """Starts the multi-thread spam"""
        pretty_print(f"Starting multi-thread spam: {self.threads} threads", (0, 255, 0))
        
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(target=self.send_message, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        pretty_print(f"✅ Spam completed! Sent: {self.sent}, Errors: {self.errors}", (0, 255, 0))

def run_groupchat_spammer_v2():
    """Groupchat Spammer V2 mit Multi-Threading"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("💬 GROUPCHAT SPAMMER V2 (Multi-Thread)", (255, 128, 0))
    print()
    
    token = input(rgb(255, 32, 32) + center("Enter Discord Token: ") + '\033[0m')
    if not token or not token.strip():
        pretty_print("❌ No token provided!", (255, 0, 0))
        return
    
    channel_id = input(rgb(255, 32, 32) + center("Enter Channel ID: ") + '\033[0m')
    if not channel_id or not channel_id.strip():
        pretty_print("❌ No channel ID provided!", (255, 0, 0))
        return
    
    message = input(rgb(255, 32, 32) + center("Enter message to spam: ") + '\033[0m')
    if not message or not message.strip():
        pretty_print("❌ No message provided!", (255, 0, 0))
        return
    
    try:
        amount = int(input(rgb(255, 32, 32) + center("How many messages? ") + '\033[0m'))
        interval = float(input(rgb(255, 32, 32) + center("Interval (seconds): ") + '\033[0m'))
        threads = int(input(rgb(255, 32, 32) + center("Number of threads (1-10): ") + '\033[0m'))
        
        if threads < 1 or threads > 10:
            threads = 1
            
    except ValueError:
        pretty_print("❌ Invalid input!", (255, 0, 0))
        return
    
    spammer = GroupchatSpammerV2(token, channel_id, message, amount, interval, threads)
    spammer.start_spam()
    
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m') 
# update
