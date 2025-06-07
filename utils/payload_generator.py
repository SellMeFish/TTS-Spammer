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

def generate_random_string(length=8):
    """Generates random variable names"""
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_text(text):
    """Obfuscates text with Base64"""
    return base64.b64encode(text.encode()).decode()


def run_payload_generator():
    """Redirect to Mini Payload Generator"""
    pretty_print("⚠️ This function has been removed!", (255, 128, 0))
    pretty_print("Use the Mini Payload Generator instead!", (255, 128, 0))
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m') 