import requests
import json
from typing import Dict, Optional
from datetime import datetime, timezone
from colorama import Fore, Style, init

init()

def get_headers(token: str) -> dict:
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

def validate_token(token: str) -> bool:
    headers = get_headers(token)
    resp = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    return resp.status_code == 200

def get_creation_date(user_id: str) -> str:
    try:
        if isinstance(user_id, str):
            if not user_id.isdigit():
                print(f"{Fore.YELLOW}Warning: User ID contains non-digit characters: {user_id}{Style.RESET_ALL}")
                return 'Unknown'
            user_id_int = int(user_id)
        else:
            user_id_int = int(str(user_id))

        timestamp = (user_id_int >> 22) + 1420070400000
        dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except (ValueError, TypeError) as e:
        print(f"{Fore.YELLOW}Warning: Could not calculate creation date for ID {user_id}: {str(e)}{Style.RESET_ALL}")
        return 'Unknown'
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Unexpected error calculating creation date: {str(e)}{Style.RESET_ALL}")
        return 'Unknown'

def get_badges(flags: int) -> str:
    badge_map = {
        1 << 0: 'Staff',
        1 << 1: 'Partner',
        1 << 2: 'HypeSquad Events',
        1 << 3: 'Bug Hunter Level 1',
        1 << 6: 'HypeSquad Bravery',
        1 << 7: 'HypeSquad Brilliance',
        1 << 8: 'HypeSquad Balance',
        1 << 9: 'Early Supporter',
        1 << 10: 'Team User',
        1 << 14: 'Bug Hunter Level 2',
        1 << 16: 'Verified Bot',
        1 << 17: 'Early Verified Bot Developer',
        1 << 18: 'Discord Certified Moderator',
        1 << 19: 'Bot HTTP Interactions',
    }
    return ', '.join([name for bit, name in badge_map.items() if flags & bit]) or 'None'

def get_token_info(token: str) -> Optional[Dict]:
    if not token or not isinstance(token, str):
        print(f"{Fore.RED}❌ Invalid token format!{Style.RESET_ALL}")
        return None

    if not validate_token(token):
        print(f"{Fore.RED}❌ Invalid Discord token!{Style.RESET_ALL}")
        return None

    headers = get_headers(token)
    try:
        user_resp = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if user_resp.status_code != 200:
            print(f"{Fore.RED}Error fetching user data! Status code: {user_resp.status_code}{Style.RESET_ALL}")
            return None

        data = user_resp.json()

        user_id = data.get('id')
        if not user_id:
            print(f"{Fore.RED}Error: No user ID found in response!{Style.RESET_ALL}")
            return None

        user_id_str = str(user_id)
        if not user_id_str.isdigit():
            print(f"{Fore.RED}Error: User ID contains non-digit characters: {user_id_str}{Style.RESET_ALL}")
            return None

        creation_date = get_creation_date(user_id_str)
        nitro = False
        nitro_days = None
        try:
            nitro_resp = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers)
            if nitro_resp.status_code == 200:
                nitro_data = nitro_resp.json()
                if len(nitro_data) > 0:
                    nitro = True
                    sub = nitro_data[0]
                    if 'current_period_end' in sub:
                        try:
                            end = datetime.fromisoformat(sub['current_period_end'].replace('Z', '+00:00'))
                            now = datetime.now(timezone.utc)
                            nitro_days = (end - now).days
                        except (ValueError, TypeError):
                            nitro_days = None
        except Exception:
            pass
        payment_sources = []
        try:
            billing_resp = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers)
            if billing_resp.status_code == 200:
                payment_sources = billing_resp.json()
        except Exception:
            pass

        badges = get_badges(data.get('public_flags', 0))

        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id_str}/{data['avatar']}.png" if data.get('avatar') else 'None'

        return {
            'username': f"{data['username']}#{data['discriminator']}",
            'id': user_id_str,
            'created_at': creation_date,
            'locale': data.get('locale', 'en'),
            'badges': badges,
            'avatar_url': avatar_url,
            'token': token,
            'mfa_enabled': data.get('mfa_enabled', False),
            'email': data.get('email', 'Not available'),
            'phone': data.get('phone', 'Not available'),
            'verified': data.get('verified', False),
            'nitro': nitro,
            'nitro_days': nitro_days,
            'payment_methods': payment_sources
        }
    except Exception as e:
        print(f"{Fore.RED}Error fetching token information: {str(e)}{Style.RESET_ALL}")
        return None

def display_token_info(token: str) -> None:
    try:
        info = get_token_info(token)
        if not info:
            return

        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                     Token Information                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Username        : {Fore.GREEN}{info['username']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} User ID         : {Fore.GREEN}{info['id']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Created At      : {Fore.GREEN}{info['created_at']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Language        : {Fore.GREEN}{info['locale']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Badges          : {Fore.GREEN}{info['badges']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Avatar URL      : {Fore.GREEN}{info['avatar_url']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Token           : {Fore.YELLOW}{info['token']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} 2FA Enabled     : {Fore.GREEN}{str(info['mfa_enabled'])}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Email           : {Fore.GREEN}{info['email']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Phone           : {Fore.GREEN}{info['phone']}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Verified        : {Fore.GREEN}{str(info['verified'])}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Nitro           : {Fore.GREEN}{str(info['nitro'])}{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL} Nitro Days Left : {Fore.GREEN}{str(info['nitro_days']) if info['nitro_days'] is not None else 'N/A'}{Style.RESET_ALL}
{Fore.CYAN}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}""")

        if info['payment_methods']:
            for idx, pm in enumerate(info['payment_methods'], 1):
                print(f"{Fore.CYAN}║{Style.RESET_ALL} Payment Method {idx}:")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Type         : {Fore.GREEN}{pm.get('type', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Valid        : {Fore.GREEN}{pm.get('valid', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Default      : {Fore.GREEN}{pm.get('default', 'N/A')}{Style.RESET_ALL}")
                if pm.get('type') == 1:
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}   Brand        : {Fore.GREEN}{pm.get('brand', 'N/A')}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}   Last 4       : {Fore.GREEN}{pm.get('last_4', 'N/A')}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}   Expires      : {Fore.GREEN}{pm.get('expires_month', 'N/A')}/{pm.get('expires_year', 'N/A')}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}   Holder Name  : {Fore.GREEN}{pm.get('billing_address', {}).get('name', 'N/A')}{Style.RESET_ALL}")
                elif pm.get('type') == 2:
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}   Paypal Email : {Fore.GREEN}{pm.get('email', 'N/A')}{Style.RESET_ALL}")
                addr = pm.get('billing_address', {})
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Address 1    : {Fore.GREEN}{addr.get('line_1', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Address 2    : {Fore.GREEN}{addr.get('line_2', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   City         : {Fore.GREEN}{addr.get('city', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Postal Code  : {Fore.GREEN}{addr.get('postal_code', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   State        : {Fore.GREEN}{addr.get('state', 'N/A')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}   Country      : {Fore.GREEN}{addr.get('country', 'N/A')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}║{Style.RESET_ALL} No payment methods found.")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}Error displaying token info: {str(e)}{Style.RESET_ALL}")
        return

def prompt_token_input() -> Optional[str]:
    attempts = 0
    while attempts < 2:
        try:
            token = input(f"{Fore.CYAN}Enter Discord token: {Style.RESET_ALL}").strip()
            if not token:
                print(f"{Fore.YELLOW}No token entered! Please try again or press Ctrl+C to cancel.{Style.RESET_ALL}")
                attempts += 1
                continue

            if not token.count('.') == 2:
                print(f"{Fore.RED}Invalid token format! Token should contain two dots.{Style.RESET_ALL}")
                attempts += 1
                continue

            print(f"{Fore.CYAN}Debug: Token format validation passed{Style.RESET_ALL}")
            return token

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}Unexpected error during token input: {str(e)}{Style.RESET_ALL}")
            attempts += 1

    print(f"{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
    return None

if __name__ == "__main__":
    try:
        token = prompt_token_input()
        if token:
            display_token_info(token)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
# update
