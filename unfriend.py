import requests
import json
import time
from typing import List, Dict
from discord_utils import get_headers, validate_token

def get_user_friends(token: str) -> List[Dict]:
    headers = get_headers(token)
    try:
        response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
        if response.status_code == 200:
            return [r for r in response.json() if r.get('type') == 1]
        return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Freundesliste: {str(e)}")
        return []

def remove_friend(token: str, user_id: str) -> bool:
    headers = get_headers(token)
    try:
        response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{user_id}', headers=headers)
        return response.status_code == 204
    except Exception as e:
        print(f"Fehler beim Entfernen des Freundes: {str(e)}")
        return False

def unfriend_all(token: str, delay: float = 1.0) -> tuple[int, int]:
    if not validate_token(token):
        print("❌ Ungültiger Discord Token!")
        return 0, 0

    friends = get_user_friends(token)
    total = len(friends)
    success = 0

    print(f"\nGefundene Freunde: {total}")
    
    for friend in friends:
        user_id = friend['id']
        username = friend.get('user', {}).get('username', 'Unbekannt')
        
        print(f"Entferne Freund: {username}...")
        if remove_friend(token, user_id):
            success += 1
            print(f"✓ Erfolgreich entfernt: {username}")
        else:
            print(f"✗ Fehler beim Entfernen von: {username}")
            
        time.sleep(delay)
        
    return success, total

if __name__ == "__main__":
    token = input("Discord Token eingeben: ")
    success, total = unfriend_all(token)
    print(f"\nErgebnis: {success} von {total} Freunden wurden entfernt.") 
