import os
import sys
import time
import json
import requests
from discord_webhook import DiscordWebhook

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def center(text):
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

def pretty_print(text, color=(255,64,64), newline=True):
    ansi = rgb(*color)
    line = center(text)
    if newline:
        print(ansi + line + RESET)
    else:
        print(ansi + line + RESET, end='')

def debug_info(text, indent=6, color=(180,180,180)):
    ansi = rgb(*color)
    prefix = " " * indent + "[DEBUG] "
    print(ansi + prefix + text + RESET)

def debug_json(data, indent=6, color=(180,180,180)):
    ansi = rgb(*color)
    prefix = " " * indent
    try:
        obj = json.loads(data)
        formatted = json.dumps(obj, indent=2)
        for line in formatted.splitlines():
            print(ansi + prefix + line + RESET)
    except Exception:
        print(ansi + prefix + data + RESET)

def loading_spinner():
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for frame in frames:
        sys.stdout.write(f'\r{rgb(192,0,0)}{center(f"Loading {frame}")}{RESET}')
        sys.stdout.flush()
        time.sleep(0.08)
    print()

def send_to_webhook(webhook_url, message, tts=False, debug=False):
    try:
        pretty_print("Sending message...", (255,0,64))
        loading_spinner()

        payload = {
            "content": message,
            "tts": tts
        }

        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(webhook_url, json=payload, headers=headers)

        if debug:
            debug_info(f"Status: {response.status_code}")
            if response.text:
                debug_info("Response:")
                debug_json(response.text)

        if response.status_code in (200, 204):
            status = "TTS" if tts else "Text"
            pretty_print(f"✓ {status} message sent successfully!", (0, 255, 128))
            return 'success'
        elif response.status_code == 429:
            retry_after = 2
            try:
                data = json.loads(response.text)
                retry_after = float(data.get('retry_after', 2))
            except Exception:
                pass
            pretty_print(f"Ratelimit hit! Waiting {retry_after} seconds...", (255,32,32))
            if debug:
                debug_info(f"Ratelimit-Response: {response.text}")
            time.sleep(retry_after)
            return 'ratelimited'
        else:
            pretty_print("✗ Error sending message!", (192,0,0))
            if debug:
                debug_info(f"Error Response: {response.text}")
            return 'error'
    except Exception as e:
        pretty_print(f"✗ Error: {str(e)}", (192,0,0))
        return 'error'

def spam_webhook(webhook_url, message, amount, interval, use_tts=False, debug=False):
    if use_tts:
        pretty_print("TTS mode: Enabled - Messages will be read aloud", (0, 255, 128))
    else:
        pretty_print("TTS mode: Disabled - Messages will be sent as text only", (255, 64, 64))

    for i in range(amount):
        pretty_print(f"Sending {i+1}/{amount}...", (255,64,64))
        result = send_to_webhook(webhook_url, message, use_tts, debug)

        if result == 'ratelimited':
            pretty_print("Retrying after ratelimit...", (255,32,32))

        if i < amount - 1:
            pretty_print(f"Waiting {interval} seconds before next message...")
            time.sleep(interval)

    return True

RESET = '\033[0m'
# update
