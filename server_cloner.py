import requests
import time
import base64
import sys

RESET = '\033[0m'

COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'GRAY': '\033[90m',
}

def color(text, c):
    return COLORS.get(c, '') + str(text) + COLORS['ENDC']

def pretty_print(text, color_key='OKCYAN', newline=True):
    out = color(text, color_key)
    if newline:
        print(out)
    else:
        print(out, end='')

def clean_singleline_input(prompt):
    raw = input(color(prompt, 'OKBLUE'))
    cleaned = "".join(raw.split())
    return cleaned

def ask_token():
    while True:
        token = clean_singleline_input("Enter Discord Token: ")
        if token:
            return token
        pretty_print("No token entered! Please try again or press Ctrl+C to cancel.", 'WARNING')

def ask_server_id(prompt):
    while True:
        server_id = clean_singleline_input(prompt)
        if server_id.isdigit():
            return server_id
        pretty_print("Please enter a valid numeric server ID!", 'WARNING')

def get_guild_data(token, guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}?with_counts=true"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        pretty_print(f"Failed to fetch guild data: {resp.status_code} {resp.text}", 'FAIL')
        return None

def get_roles(token, guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles"
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        pretty_print(f"Failed to fetch roles: {resp.status_code} {resp.text}", 'FAIL')
        return []

def get_channels(token, guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        pretty_print(f"Failed to fetch channels: {resp.status_code} {resp.text}", 'FAIL')
        return []

def get_emojis(token, guild_id):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        pretty_print(f"Failed to fetch emojis: {resp.status_code} {resp.text}", 'FAIL')
        return []

def get_guild_icon(token, guild):
    if not guild.get('icon'):
        return None
    icon_url = f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.png"
    resp = requests.get(icon_url)
    if resp.status_code == 200:
        return resp.content
    return None

def create_role(token, guild_id, role):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {
        "name": role['name'],
        "color": role['color'],
        "hoist": role['hoist'],
        "permissions": role['permissions'],
        "mentionable": role['mentionable']
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        pretty_print(f"Failed to create role {role['name']}: {resp.status_code} {resp.text}", 'FAIL')
        return None

def create_category(token, guild_id, name, position):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"name": name, "type": 4, "position": position}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        pretty_print(f"Failed to create category {name}: {resp.status_code} {resp.text}", 'FAIL')
        return None

def create_channel(token, guild_id, channel, parent_id=None):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {
        "name": channel['name'],
        "type": channel['type'],
        "position": channel['position'],
        "parent_id": parent_id
    }
    if channel['type'] == 2:
        data['bitrate'] = min(channel.get('bitrate', 64000), 96000)  # Discord API Limit
        data['user_limit'] = channel.get('user_limit', 0)
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        pretty_print(f"Failed to create channel {channel['name']}: {resp.status_code} {resp.text}", 'FAIL')
        return None

def upload_emoji(token, guild_id, emoji):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    image_resp = requests.get(f"https://cdn.discordapp.com/emojis/{emoji['id']}.png")
    if image_resp.status_code != 200:
        pretty_print(f"Failed to download emoji {emoji['name']}", 'FAIL')
        return None
    b64img = "data:image/png;base64," + base64.b64encode(image_resp.content).decode()
    data = {"name": emoji['name'], "image": b64img}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        pretty_print(f"Failed to upload emoji {emoji['name']}: {resp.status_code} {resp.text}", 'FAIL')
        return None

def set_guild_icon(token, guild_id, icon_bytes):
    url = f"https://discord.com/api/v10/guilds/{guild_id}"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    b64icon = "data:image/png;base64," + base64.b64encode(icon_bytes).decode()
    data = {"icon": b64icon}
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        pretty_print("Server icon set successfully!", 'OKGREEN')
    else:
        pretty_print(f"Failed to set server icon: {resp.status_code} {resp.text}", 'FAIL')

def set_guild_name(token, guild_id, name, description=None):
    url = f"https://discord.com/api/v10/guilds/{guild_id}"
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"name": name}
    if description:
        data["description"] = description
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        pretty_print(f"Server name set to '{name}'!", 'OKGREEN')
    else:
        pretty_print(f"Failed to set server name: {resp.status_code} {resp.text}", 'FAIL')

def clear_target_guild(token, guild_id):
    pretty_print("Clearing target server...", 'WARNING')
    channels = get_channels(token, guild_id)
    for ch in channels:
        url = f"https://discord.com/api/v10/channels/{ch['id']}"
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        resp = requests.delete(url, headers=headers)
        if resp.status_code in (200, 204):
            pretty_print(f"Deleted channel: {ch['name']}", 'GRAY')
        time.sleep(0.3)
    emojis = get_emojis(token, guild_id)
    for emoji in emojis:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji['id']}"
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        resp = requests.delete(url, headers=headers)
        if resp.status_code in (200, 204):
            pretty_print(f"Deleted emoji: {emoji['name']}", 'GRAY')
        time.sleep(0.3)
    roles = get_roles(token, guild_id)
    for role in roles:
        if role['name'] == "@everyone":
            continue
        url = f"https://discord.com/api/v10/guilds/{guild_id}/roles/{role['id']}"
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        resp = requests.delete(url, headers=headers)
        if resp.status_code in (200, 204):
            pretty_print(f"Deleted role: {role['name']}", 'GRAY')
        time.sleep(0.3)
    pretty_print("Target server cleared!", 'OKGREEN')


def clone_server(token, source_id, target_id):
    pretty_print("\n" + "="*60, 'HEADER')
    pretty_print("        Discord Server Cloner", 'HEADER')
    pretty_print("="*60 + "\n", 'HEADER')
    pretty_print(f"Fetching source server...", 'OKCYAN')
    source_data = get_guild_data(token, source_id)
    if not source_data:
        return
    pretty_print(f"Source Server: {color(source_data['name'], 'BOLD')} ({source_id})", 'OKGREEN')
    pretty_print(f"Fetching target server...", 'OKCYAN')
    target_data = get_guild_data(token, target_id)
    if not target_data:
        return
    pretty_print(f"Target Server: {color(target_data['name'], 'BOLD')} ({target_id})", 'OKGREEN')

    clear_target_guild(token, target_id)

    pretty_print("Cloning server name...", 'OKCYAN')
    set_guild_name(token, target_id, source_data['name'], source_data.get('description'))

    pretty_print("Cloning server icon...", 'OKCYAN')
    icon_bytes = get_guild_icon(token, source_data)
    if icon_bytes:
        set_guild_icon(token, target_id, icon_bytes)
    else:
        pretty_print("No icon to clone.", 'WARNING')

    pretty_print("Cloning roles...", 'OKCYAN')
    source_roles = get_roles(token, source_id)
    role_map = {}
    for role in source_roles:
        if role['name'] == "@everyone":
            continue
        new_role = create_role(token, target_id, role)
        if new_role:
            role_map[role['id']] = new_role['id']
        time.sleep(0.5)

    pretty_print("Cloning categories and channels...", 'OKCYAN')
    source_channels = get_channels(token, source_id)
    categories = [c for c in source_channels if c['type'] == 4]
    channels = [c for c in source_channels if c['type'] != 4]
    cat_map = {}
    for cat in sorted(categories, key=lambda x: x['position']):
        new_cat = create_category(token, target_id, cat['name'], cat['position'])
        if new_cat:
            cat_map[cat['id']] = new_cat['id']
        time.sleep(0.5)
    for ch in sorted(channels, key=lambda x: x['position']):
        parent_id = cat_map.get(ch.get('parent_id')) if ch.get('parent_id') else None
        create_channel(token, target_id, ch, parent_id)
        time.sleep(0.5)

    pretty_print("Cloning emojis...", 'OKCYAN')
    source_emojis = get_emojis(token, source_id)
    for emoji in source_emojis:
        upload_emoji(token, target_id, emoji)
        time.sleep(1)

    pretty_print("\nClone complete!", 'OKGREEN')


def main():
    print("\n=== Discord Server Cloner ===\n")
    token = ask_token()
    source_id = ask_server_id("Enter Source Server ID: ")
    target_id = ask_server_id("Enter Target Server ID: ")
    clone_server(token, source_id, target_id)

if __name__ == "__main__":
    main() 
