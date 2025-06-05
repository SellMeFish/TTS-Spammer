# Discord AIO Tool

![Preview](spammer1.png)

A modern, versatile Discord tool packed with powerful features.

##  Features

### Token Management
- **Token Info**
  - Get detailed insights into any Discord token
  - View username, ID, creation date, language, and badges
  - See avatar URL and token details
  - Check 2FA status, email, phone, and verification status
  - Monitor Nitro status with remaining days
  - View all payment methods (credit card/PayPal) with full details

- **Token Login**
  - Quick and easy token-based login
  - Smart token validation

- **Token Generator**
  - Generate and validate Discord tokens
  - Multi-threaded validation for speed

- **Nitro Generator & Checker**
  - Generate and check Discord Nitro codes
  - Configurable thread count and speed

### Token Grabber
- **Advanced Token Grabber**
  - Collect Discord tokens from multiple browsers and profiles
  - Extract browser passwords from 35+ different browsers (Chrome, Edge, Brave, Opera, Vivaldi, Yandex, Firefox)
  - Capture browser history from all major browsers
  - Extract autofill data (profiles, form data, addresses)
  - Capture screenshots of user's screens
  - Gather detailed system information and geolocation
  - Collect cookies from important domains (Discord, Google, PayPal, etc.)
  - Extract Discord login credentials from local storage
  - Automatic startup persistence
  - **NEW: GoFile Integration**
    - Creates organized local data folders in AppData
    - Packages all captured data into ZIP archives
    - Uploads to GoFile for easy download
    - Clean, formatted text files without failed decryptions
    - Simple Discord webhook notifications with download links
  - Compile as standalone executable

### Server Management
- **Server Cloner**
  - Clone entire server structures
  - Copy roles, channels (including categories)
  - Transfer server icon, name, and description
  - Clone all emojis
  - Clean target server before cloning

- **Delete/Leave All Servers**
  - Leave or delete all servers
  - Safety confirmation before execution

### Friend Management
- **Unfriend All Friends**
  - Remove all friends
  - Confirmation prompt

- **DM All Friends**
  - Send messages to all friends
  - Support for mass messaging

### Webhook Tools
- **Webhook Spammer**
  - Send messages through webhooks
  - Support for various message formats
  - Customizable delays
  - TTS message support

- **Webhook Deleter**
  - Delete webhooks via URL
  - Confirmation before deletion

### Additional Features
- **Close All DMs**
  - Close all open DMs

- **Theme Spammer**
  - Spam theme messages
  - Customizable settings

##  Getting Started

1. Make sure you have Python 3.8 or higher installed
2. Clone the repository:
```bash
git clone https://github.com/SellMeFish/TTS-Spammer.git
cd TTS-Spammer
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

##  Usage

1. Start the tool:
```bash
python tts_spammer.py
```

2. Choose your desired function from the main menu
3. Follow the on-screen instructions

##  Dependencies

The tool requires the following key dependencies:
- **Core Libraries**: requests, urllib3, discord-webhook
- **UI & Display**: colorama, inquirer, art, tqdm
- **Audio**: pyttsx3
- **System**: psutil, setuptools
- **Cryptography**: pycryptodome
- **Image Processing**: pillow
- **Windows Support**: pywin32, pypiwin32 (Windows only)
- **Browser Automation**: selenium, webdriver-manager
- **Packaging**: pyinstaller
- **Date/Time**: python-dateutil
- **Web Parsing**: beautifulsoup4
- **File Compression**: zipfile (built-in)

For a complete list, see the requirements.txt file.

##  Important Notes

- This tool is intended for educational purposes only
- Please use responsibly and in accordance with Discord's Terms of Service
- The author is not responsible for any misuse of this tool
- **Data Security**: All captured data is temporarily stored locally and uploaded to GoFile
- **Privacy**: Ensure you have proper authorization before using the grabber functionality
- **Compatibility**: Optimized for Windows systems with support for major browsers

##  Latest Updates

### Recent Improvements
- **Major Token Grabber Overhaul**
  - Added browser history and autofill data extraction
  - Implemented GoFile cloud storage integration
  - Organized data collection into structured ZIP archives
  - Enhanced data filtering (only valid passwords, no failed decryptions)
  - Improved local file management with AppData storage
  - Streamlined Discord notifications with single download links
- Added advanced Token Grabber with browser password extraction
- Added Token Generator and Nitro Generator & Checker
- Added TTS (Text-to-Speech) message support for webhook spammer
- Enhanced token validation and Firefox password support
- Optimized Nitro days calculation
- Modernized user interface with comment-free codebase
- Improved error handling and startup persistence
- New webhook deleter feature
- Extended server cloner functionality
- Support for multiple screen captures
- More browser support (35+ browsers including Firefox variants)

##  Contributing

Feel free to contribute! Whether it's bug reports, feature requests, or pull requests - every contribution is welcome. Just make sure to:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

##  Author

Created by cyberseall

---
