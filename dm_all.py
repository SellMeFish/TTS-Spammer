import requests
import json
import time
import random
from typing import List, Dict
from discord_utils import get_headers, validate_token

def get_user_friends(token: str) -> List[Dict]:
    """
    Gets the friend list of a Discord account
    Type 1 = Accepted Friend
    Type 2 = Blocked
    Type 3 = Pending Incoming
    Type 4 = Pending Outgoing
    """
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': token,
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'de',
        'x-discord-timezone': 'Europe/Berlin',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImRlLURFIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQwNDI2OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
    }

    try:
        response = requests.get(
            'https://discord.com/api/v9/users/@me/relationships',
            headers=headers
        )
        
        if response.status_code == 200:
            relationships = response.json()
            # Filter only accepted friends (type 1)
            friends = [
                r for r in relationships 
                if r.get('type') == 1 
                and not r.get('user_ignored', False)
                and r.get('user', {}).get('username')
            ]
            return friends
        return []
    except Exception as e:
        print(f"Error fetching friend list: {str(e)}")
        return []

def create_dm_channel(token: str, user_id: str) -> str:
    headers = get_headers(token)
    payload = {
        'recipients': [user_id]
    }
    
    try:
        response = requests.post('https://discord.com/api/v9/users/@me/channels', headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['id']
        return None
    except Exception as e:
        print(f"Error creating DM channel: {str(e)}")
        return None

def generate_nonce() -> str:
    """Generates a Discord-compatible nonce"""
    return str(random.randint(100000000000000000, 999999999999999999))

def send_dm(token: str, channel_id: str, message: str) -> bool:
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me/' + channel_id,
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'de',
        'x-discord-timezone': 'Europe/Berlin',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImRlLURFIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQwNDI2OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
    }

    payload = {
        'content': message,
        'nonce': generate_nonce(),
        'tts': False,
        'flags': 0,
        'mobile_network_type': 'unknown'
    }
    
    try:
        response = requests.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            headers=headers,
            json=payload
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

def dm_all_friends(token: str, message: str, delay: float = 1.0) -> tuple[int, int]:
    if not validate_token(token):
        print("❌ Invalid Discord Token!")
        return 0, 0

    friends = get_user_friends(token)
    total = len(friends)
    success = 0

    print(f"\nFound friends: {total}")
    
    for friend in friends:
        user_id = friend['id']
        username = friend.get('user', {}).get('username', 'Unknown')
        
        print(f"Sending DM to: {username}...")
        
        # Create DM channel
        channel_id = create_dm_channel(token, user_id)
        if not channel_id:
            print(f"✗ Could not create DM channel for {username}")
            continue
            
        # Send message
        if send_dm(token, channel_id, message):
            success += 1
            print(f"✓ Message successfully sent to {username}")
        else:
            print(f"✗ Error sending message to {username}")
            
        time.sleep(delay)  # Delay to avoid rate limits
        
    return success, total

if __name__ == "__main__":
    token = input("Enter Discord Token: ")
    message = input("Enter message: ")
    success, total = dm_all_friends(token, message)
    print(f"\nResult: {success} of {total} messages sent successfully.") 