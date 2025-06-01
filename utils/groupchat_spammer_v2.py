import requests
import json
import random
import time
from typing import List, Dict
from colorama import Fore, Style, init

init()

def get_headers(token: str) -> dict:
    return {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'content-type': 'application/json',
    }

def get_friends(token: str) -> List[Dict]:
    try:
        resp = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=get_headers(token))
        if resp.status_code == 200:
            relationships = resp.json()
            friends = [r for r in relationships if r.get('type') == 1 and r.get('user', {}).get('username')]
            return friends
        else:
            print(f"{Fore.RED}Error fetching friends: Status {resp.status_code}{Style.RESET_ALL}")
            return []
    except Exception as e:
        print(f"{Fore.RED}Error fetching friends: {str(e)}{Style.RESET_ALL}")
        return []

def create_group_dm(token: str, user_ids: List[str]) -> str:
    payload = {"recipients": user_ids}
    try:
        resp = requests.post('https://discord.com/api/v9/users/@me/channels', headers=get_headers(token), json=payload)
        if resp.status_code == 200:
            return resp.json()['id']
        else:
            print(f"{Fore.RED}Failed to create group DM: Status {resp.status_code}{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating group DM: {str(e)}{Style.RESET_ALL}")
        return None

def send_group_message(token: str, channel_id: str, message: str) -> bool:
    payload = {"content": message}
    try:
        resp = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=get_headers(token), json=payload)
        return resp.status_code == 200
    except Exception as e:
        print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
        return False

def groupchat_spammer(token: str):
    print(f"{Fore.CYAN}=== GroupChat Spammer ==={Style.RESET_ALL}")
    friends = get_friends(token)
    if not friends:
        print(f"{Fore.RED}No friends found!{Style.RESET_ALL}")
        return
    print(f"{Fore.CYAN}You have {len(friends)} friends.{Style.RESET_ALL}")
    mode = input(f"{Fore.CYAN}Choose mode ([1] Random friends, [2] Enter user IDs): {Style.RESET_ALL}").strip()
    if mode == '2':
        ids = input(f"{Fore.CYAN}Enter user IDs (comma separated): {Style.RESET_ALL}").strip()
        user_ids = [uid.strip() for uid in ids.split(',') if uid.strip()]
    else:
        count = input(f"{Fore.CYAN}How many users per group? (2-9): {Style.RESET_ALL}").strip()
        try:
            count = max(2, min(9, int(count)))
        except:
            count = 2
        user_ids = [f['id'] for f in random.sample(friends, min(count, len(friends)))]
    num_groups = input(f"{Fore.CYAN}How many group chats to create?: {Style.RESET_ALL}").strip()
    try:
        num_groups = max(1, int(num_groups))
    except:
        num_groups = 1
    message = input(f"{Fore.CYAN}Optional: Message to send in each group (leave blank for none): {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Creating group chats...{Style.RESET_ALL}")
    success = 0
    for i in range(num_groups):
        if mode == '1':
            user_ids = [f['id'] for f in random.sample(friends, min(count, len(friends)))]
        channel_id = create_group_dm(token, user_ids)
        if channel_id:
            if message:
                send_group_message(token, channel_id, message)
            print(f"{Fore.GREEN}[{i+1}/{num_groups}] Group chat created!{Style.RESET_ALL}")
            success += 1
        else:
            print(f"{Fore.RED}[{i+1}/{num_groups}] Failed to create group chat!{Style.RESET_ALL}")
        time.sleep(1)
    print(f"{Fore.CYAN}Done! {success}/{num_groups} group chats created.{Style.RESET_ALL}")

if __name__ == "__main__":
    from token_info import prompt_token_input
    token = prompt_token_input()
    if token:
        groupchat_spammer(token) 