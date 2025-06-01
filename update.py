import os
import sys
import requests
import zipfile
import io
import shutil

# === Konfiguration ===
GITHUB_REPO = "SellMeFish/TTS-Spammer"
RAW_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.txt"
ZIP_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = "version.txt"


def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_remote_version():
    try:
        resp = requests.get(RAW_VERSION_URL, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception:
        pass
    return None

def download_and_extract_zip():
    print("Downloading latest version from GitHub...")
    resp = requests.get(ZIP_URL, stream=True)
    if resp.status_code != 200:
        print("[ERROR] Could not download update from GitHub.")
        return False
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    temp_dir = "_update_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    z.extractall(temp_dir)
    # Finde den extrahierten Ordner
    extracted = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))][0]
    src_path = os.path.join(temp_dir, extracted)
    # Kopiere alle Dateien (außer .git, _update_temp, __pycache__)
    for root, dirs, files in os.walk(src_path):
        rel_path = os.path.relpath(root, src_path)
        for file in files:
            if file == "update.py": continue  # update.py nicht überschreiben
            src_file = os.path.join(root, file)
            dst_file = os.path.join(os.getcwd(), rel_path, file) if rel_path != "." else os.path.join(os.getcwd(), file)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
    shutil.rmtree(temp_dir)
    return True

def main():
    print("Checking for updates...")
    local_version = get_local_version()
    remote_version = get_remote_version()
    print(f"Local version:  {local_version}")
    print(f"Remote version: {remote_version}")
    if not remote_version:
        print("[ERROR] Could not fetch remote version. Please check your internet connection or the repo URL.")
        return
    if local_version == remote_version:
        print("You already have the latest version!")
        return
    print("A new version is available! Updating...")
    if download_and_extract_zip():
        print("Update successful! Please restart the tool.")
    else:
        print("Update failed.")

if __name__ == "__main__":
    main() 