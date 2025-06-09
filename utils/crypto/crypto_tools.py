import hashlib
import base64
import json
import requests
import time
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init
import itertools
from concurrent.futures import ThreadPoolExecutor
import os

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def generate_hash(text, hash_type):
    hash_functions = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
        'sha224': hashlib.sha224,
        'sha384': hashlib.sha384
    }
    
    if hash_type.lower() in hash_functions:
        hash_obj = hash_functions[hash_type.lower()]()
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    else:
        return None

def crack_hash_dictionary(target_hash, hash_type, wordlist):
    print_colored(f"[INFO] Starting dictionary attack on {hash_type.upper()} hash...", Fore.YELLOW)
    
    attempts = 0
    for word in wordlist:
        attempts += 1
        word = word.strip()
        generated_hash = generate_hash(word, hash_type)
        
        if generated_hash and generated_hash.lower() == target_hash.lower():
            print_colored(f"✅ HASH CRACKED! Password: {word}", Fore.GREEN)
            print_colored(f"Attempts: {attempts}", Fore.CYAN)
            return word
        
        if attempts % 1000 == 0:
            print_colored(f"[PROGRESS] Tried {attempts} passwords...", Fore.YELLOW)
    
    print_colored(f"❌ Hash not cracked after {attempts} attempts", Fore.RED)
    return None

def crack_hash_bruteforce(target_hash, hash_type, max_length=6):
    print_colored(f"[INFO] Starting brute force attack on {hash_type.upper()} hash...", Fore.YELLOW)
    print_colored(f"[INFO] Max length: {max_length} characters", Fore.CYAN)
    
    chars = string.ascii_lowercase + string.digits
    attempts = 0
    
    for length in range(1, max_length + 1):
        print_colored(f"[INFO] Trying passwords of length {length}...", Fore.CYAN)
        
        for combination in itertools.product(chars, repeat=length):
            attempts += 1
            password = ''.join(combination)
            generated_hash = generate_hash(password, hash_type)
            
            if generated_hash and generated_hash.lower() == target_hash.lower():
                print_colored(f"✅ HASH CRACKED! Password: {password}", Fore.GREEN)
                print_colored(f"Attempts: {attempts}", Fore.CYAN)
                return password
            
            if attempts % 10000 == 0:
                print_colored(f"[PROGRESS] Tried {attempts} combinations...", Fore.YELLOW)
    
    print_colored(f"❌ Hash not cracked after {attempts} attempts", Fore.RED)
    return None

def encrypt_text(text, password):
    try:
        password_bytes = password.encode()
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        
        fernet = Fernet(key)
        encrypted = fernet.encrypt(text.encode())
        
        result = {
            'encrypted': base64.b64encode(encrypted).decode(),
            'salt': base64.b64encode(salt).decode(),
            'algorithm': 'Fernet (AES 128)',
            'iterations': 100000
        }
        
        return result
        
    except Exception as e:
        return {'error': str(e)}

def decrypt_text(encrypted_data, password):
    try:
        password_bytes = password.encode()
        salt = base64.b64decode(encrypted_data['salt'])
        encrypted = base64.b64decode(encrypted_data['encrypted'])
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)
        
        return decrypted.decode()
        
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def encode_decode_base64(text, operation):
    try:
        if operation == 'encode':
            encoded = base64.b64encode(text.encode()).decode()
            return encoded
        elif operation == 'decode':
            decoded = base64.b64decode(text).decode()
            return decoded
    except Exception as e:
        return f"Error: {str(e)}"

def simple_steganography_encode(text, cover_text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    binary_text += '1111111111111110'
    
    result = []
    binary_index = 0
    
    for char in cover_text:
        if binary_index < len(binary_text):
            if binary_text[binary_index] == '1':
                result.append(char.upper())
            else:
                result.append(char.lower())
            binary_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

def simple_steganography_decode(stego_text):
    binary_data = ''
    
    for char in stego_text:
        if char.isupper():
            binary_data += '1'
        elif char.islower():
            binary_data += '0'
    
    end_marker = '1111111111111110'
    if end_marker in binary_data:
        binary_data = binary_data[:binary_data.index(end_marker)]
    
    try:
        decoded_text = ''
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                decoded_text += chr(int(byte, 2))
        return decoded_text
    except:
        return "Failed to decode hidden message"

def analyze_bitcoin_address(address):
    print_colored(f"[INFO] Analyzing Bitcoin address: {address}", Fore.YELLOW)
    
    try:
        url = f"https://blockstream.info/api/address/{address}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            balance_btc = data.get('chain_stats', {}).get('funded_txo_sum', 0) / 100000000
            spent_btc = data.get('chain_stats', {}).get('spent_txo_sum', 0) / 100000000
            current_balance = balance_btc - spent_btc
            
            tx_count = data.get('chain_stats', {}).get('tx_count', 0)
            
            print_colored(f"📊 BITCOIN ADDRESS ANALYSIS:", Fore.CYAN)
            print_colored(f"Address: {address}", Fore.WHITE)
            print_colored(f"Total Received: {balance_btc:.8f} BTC", Fore.GREEN)
            print_colored(f"Total Spent: {spent_btc:.8f} BTC", Fore.RED)
            print_colored(f"Current Balance: {current_balance:.8f} BTC", Fore.YELLOW)
            print_colored(f"Transaction Count: {tx_count}", Fore.CYAN)
            
            if current_balance > 0:
                btc_price_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
                price_response = requests.get(btc_price_url, timeout=5)
                if price_response.status_code == 200:
                    price_data = price_response.json()
                    usd_rate = float(price_data['bpi']['USD']['rate'].replace(',', ''))
                    usd_value = current_balance * usd_rate
                    print_colored(f"USD Value: ${usd_value:,.2f}", Fore.GREEN)
            
            return data
            
    except Exception as e:
        print_colored(f"❌ Error analyzing address: {str(e)}", Fore.RED)
        return None

def generate_common_passwords():
    common_passwords = [
        'password', '123456', '123456789', 'qwerty', 'abc123', 'password123',
        'admin', 'letmein', 'welcome', 'monkey', '1234567890', 'dragon',
        'master', 'shadow', 'superman', 'michael', 'football', 'baseball',
        'liverpool', 'jordan', 'princess', 'sunshine', 'iloveyou', 'charlie',
        'aa123456', 'donald', 'password1', 'qwerty123'
    ]
    
    variations = []
    for pwd in common_passwords:
        variations.extend([
            pwd,
            pwd.upper(),
            pwd.capitalize(),
            pwd + '!',
            pwd + '123',
            pwd + '2023',
            pwd + '2024',
            '123' + pwd,
            pwd + pwd,
        ])
    
    return list(set(variations))

def hash_identifier(hash_string):
    hash_length = len(hash_string)
    
    hash_types = {
        32: ['MD5', 'NTLM'],
        40: ['SHA1'],
        56: ['SHA224'],
        64: ['SHA256'],
        96: ['SHA384'],
        128: ['SHA512']
    }
    
    if hash_length in hash_types:
        return hash_types[hash_length]
    else:
        return ['Unknown']

def run_crypto_tools():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("            ADVANCED CRYPTO TOOLS", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    print_colored("Professional cryptography and security toolkit", Fore.YELLOW)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nSelect crypto tool:", Fore.WHITE)
        print_colored("1. Hash Generator", Fore.GREEN)
        print_colored("2. Hash Cracker (Dictionary)", Fore.YELLOW)
        print_colored("3. Hash Cracker (Brute Force)", Fore.YELLOW)
        print_colored("4. Text Encryption/Decryption", Fore.YELLOW)
        print_colored("5. Base64 Encoder/Decoder", Fore.YELLOW)
        print_colored("6. Simple Steganography", Fore.YELLOW)
        print_colored("7. Bitcoin Address Analyzer", Fore.YELLOW)
        print_colored("8. Hash Identifier", Fore.YELLOW)
        print_colored("9. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-9): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            text = input(f"{Fore.WHITE}Enter text to hash: {Style.RESET_ALL}").strip()
            if text:
                print_colored("\nGenerated Hashes:", Fore.CYAN)
                hash_types = ['md5', 'sha1', 'sha256', 'sha512']
                for hash_type in hash_types:
                    hash_result = generate_hash(text, hash_type)
                    print_colored(f"{hash_type.upper()}: {hash_result}", Fore.WHITE)
        
        elif choice == '2':
            target_hash = input(f"{Fore.WHITE}Enter hash to crack: {Style.RESET_ALL}").strip()
            if target_hash:
                possible_types = hash_identifier(target_hash)
                print_colored(f"Possible hash types: {', '.join(possible_types)}", Fore.CYAN)
                
                hash_type = input(f"{Fore.WHITE}Enter hash type (md5/sha1/sha256/etc): {Style.RESET_ALL}").strip()
                
                print_colored("[INFO] Using common password list...", Fore.YELLOW)
                wordlist = generate_common_passwords()
                
                result = crack_hash_dictionary(target_hash, hash_type, wordlist)
                if not result:
                    print_colored("Try brute force attack for better results", Fore.YELLOW)
        
        elif choice == '3':
            target_hash = input(f"{Fore.WHITE}Enter hash to crack: {Style.RESET_ALL}").strip()
            if target_hash:
                hash_type = input(f"{Fore.WHITE}Enter hash type (md5/sha1/sha256/etc): {Style.RESET_ALL}").strip()
                try:
                    max_length = int(input(f"{Fore.WHITE}Max password length (1-8, recommended: 4): {Style.RESET_ALL}") or "4")
                    max_length = min(max_length, 8)
                except:
                    max_length = 4
                
                print_colored(f"[WARNING] This may take a very long time for length > 4!", Fore.RED)
                confirm = input(f"{Fore.WHITE}Continue? (y/n): {Style.RESET_ALL}").strip().lower()
                if confirm == 'y':
                    crack_hash_bruteforce(target_hash, hash_type, max_length)
        
        elif choice == '4':
            print_colored("1. Encrypt Text", Fore.GREEN)
            print_colored("2. Decrypt Text", Fore.GREEN)
            
            sub_choice = input(f"{Fore.WHITE}Choose (1-2): {Style.RESET_ALL}").strip()
            
            if sub_choice == '1':
                text = input(f"{Fore.WHITE}Enter text to encrypt: {Style.RESET_ALL}").strip()
                password = input(f"{Fore.WHITE}Enter encryption password: {Style.RESET_ALL}").strip()
                
                if text and password:
                    result = encrypt_text(text, password)
                    if 'error' not in result:
                        print_colored("\n✅ ENCRYPTION SUCCESSFUL:", Fore.GREEN)
                        print_colored(f"Encrypted Data: {result['encrypted']}", Fore.CYAN)
                        print_colored(f"Salt: {result['salt']}", Fore.CYAN)
                        print_colored(f"Algorithm: {result['algorithm']}", Fore.CYAN)
                        
                        save = input(f"\n{Fore.WHITE}Save to file? (y/n): {Style.RESET_ALL}").strip().lower()
                        if save == 'y':
                            filename = "encrypted_data.json"
                            with open(filename, 'w') as f:
                                json.dump(result, f, indent=2)
                            print_colored(f"Saved to {filename}", Fore.GREEN)
                    else:
                        print_colored(f"❌ Encryption failed: {result['error']}", Fore.RED)
            
            elif sub_choice == '2':
                print_colored("1. Enter encrypted data manually", Fore.YELLOW)
                print_colored("2. Load from file", Fore.YELLOW)
                
                load_choice = input(f"{Fore.WHITE}Choose (1-2): {Style.RESET_ALL}").strip()
                
                encrypted_data = None
                
                if load_choice == '1':
                    encrypted = input(f"{Fore.WHITE}Enter encrypted data: {Style.RESET_ALL}").strip()
                    salt = input(f"{Fore.WHITE}Enter salt: {Style.RESET_ALL}").strip()
                    encrypted_data = {'encrypted': encrypted, 'salt': salt}
                
                elif load_choice == '2':
                    filename = input(f"{Fore.WHITE}Enter filename (default: encrypted_data.json): {Style.RESET_ALL}").strip()
                    if not filename:
                        filename = "encrypted_data.json"
                    
                    try:
                        with open(filename, 'r') as f:
                            encrypted_data = json.load(f)
                    except Exception as e:
                        print_colored(f"❌ Failed to load file: {str(e)}", Fore.RED)
                
                if encrypted_data:
                    password = input(f"{Fore.WHITE}Enter decryption password: {Style.RESET_ALL}").strip()
                    result = decrypt_text(encrypted_data, password)
                    
                    if not result.startswith("Decryption failed"):
                        print_colored(f"✅ DECRYPTED TEXT: {result}", Fore.GREEN)
                    else:
                        print_colored(f"❌ {result}", Fore.RED)
        
        elif choice == '5':
            print_colored("1. Encode to Base64", Fore.GREEN)
            print_colored("2. Decode from Base64", Fore.GREEN)
            
            sub_choice = input(f"{Fore.WHITE}Choose (1-2): {Style.RESET_ALL}").strip()
            text = input(f"{Fore.WHITE}Enter text: {Style.RESET_ALL}").strip()
            
            if sub_choice == '1':
                result = encode_decode_base64(text, 'encode')
                print_colored(f"Encoded: {result}", Fore.GREEN)
            elif sub_choice == '2':
                result = encode_decode_base64(text, 'decode')
                print_colored(f"Decoded: {result}", Fore.GREEN)
        
        elif choice == '6':
            print_colored("1. Hide message in text", Fore.GREEN)
            print_colored("2. Extract hidden message", Fore.GREEN)
            
            sub_choice = input(f"{Fore.WHITE}Choose (1-2): {Style.RESET_ALL}").strip()
            
            if sub_choice == '1':
                secret = input(f"{Fore.WHITE}Enter secret message: {Style.RESET_ALL}").strip()
                cover = input(f"{Fore.WHITE}Enter cover text: {Style.RESET_ALL}").strip()
                
                if secret and cover:
                    result = simple_steganography_encode(secret, cover)
                    print_colored(f"Steganographic text: {result}", Fore.GREEN)
            
            elif sub_choice == '2':
                stego_text = input(f"{Fore.WHITE}Enter steganographic text: {Style.RESET_ALL}").strip()
                if stego_text:
                    result = simple_steganography_decode(stego_text)
                    print_colored(f"Hidden message: {result}", Fore.GREEN)
        
        elif choice == '7':
            address = input(f"{Fore.WHITE}Enter Bitcoin address: {Style.RESET_ALL}").strip()
            if address:
                analyze_bitcoin_address(address)
        
        elif choice == '8':
            hash_string = input(f"{Fore.WHITE}Enter hash to identify: {Style.RESET_ALL}").strip()
            if hash_string:
                possible_types = hash_identifier(hash_string)
                print_colored(f"Hash length: {len(hash_string)} characters", Fore.CYAN)
                print_colored(f"Possible types: {', '.join(possible_types)}", Fore.GREEN)
        
        elif choice == '9':
            print_colored("Exiting crypto tools...", Fore.YELLOW)
            break
        
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
        
        if choice != '9':
            continue_choice = input(f"\n{Fore.WHITE}Continue using crypto tools? (y/n): {Style.RESET_ALL}").strip().lower()
            if continue_choice != 'y':
                break

if __name__ == "__main__":
    run_crypto_tools() 