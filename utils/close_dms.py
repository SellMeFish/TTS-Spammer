import requests
import json
import time
from typing import Tuple
from utils.discord_utils import get_headers, validate_token
from colorama import Fore, Style, init

init()
def close_all_dms(token: str, delay: float = 0.5) -> Tuple[int, int]:

    if not validate_token(token):
        print(f"{Fore.RED}❌ Ungültiger Discord Token!{Style.RESET_ALL}")
        return 0, 0

    headers = get_headers(token)
    success = 0
    failed = 0

    try:
        response = requests.get(
            "https://discord.com/api/v9/users/@me/channels",
            headers=headers
        )

        if response.status_code != 200:
            print(f"{Fore.RED}Fehler beim Abrufen der DM-Kanäle: {response.status_code}{Style.RESET_ALL}")
            return 0, 0

        channels = response.json()
        total = len(channels)

        print(f"\n{Fore.CYAN}Gefundene DM-Kanäle: {total}{Style.RESET_ALL}\n")
        for channel in channels:
            channel_id = channel['id']
            recipients = channel.get('recipients', [])
            recipient_name = recipients[0]['username'] if recipients else 'Unbekannt'

            print(f"{Fore.YELLOW}Schließe DM mit {recipient_name}... {Style.RESET_ALL}", end='', flush=True)

            try:
                close_response = requests.delete(
                    f"https://discord.com/api/v9/channels/{channel_id}",
                    headers=headers
                )

                if close_response.status_code in [200, 204]:
                    success += 1
                    print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                else:
                    failed += 1
                    print(f"{Fore.RED}✗{Style.RESET_ALL}")

                time.sleep(delay)

            except Exception as e:
                failed += 1
                print(f"{Fore.RED}✗ Fehler: {str(e)}{Style.RESET_ALL}")

        return success, total

    except Exception as e:
        print(f"{Fore.RED}Unerwarteter Fehler: {str(e)}{Style.RESET_ALL}")
        return 0, 0

if __name__ == "__main__":
    token = input(f"{Fore.CYAN}Discord Token eingeben: {Style.RESET_ALL}")
    success, total = close_all_dms(token)
    print(f"\n{Fore.CYAN}Ergebnis: {Fore.GREEN}{success}{Fore.CYAN} von {total} DMs geschlossen{Style.RESET_ALL}")