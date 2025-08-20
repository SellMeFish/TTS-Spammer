

try:
    from .strings_config import (
        CHANGELOG, MENU_HEADERS, MENU_CHOICES,
        PROMPTS, STATUS_MESSAGES, MESSAGES, UI_ELEMENTS, COLORS
    )
except ImportError:
    CHANGELOG = ["v0.4.5 - Latest Update:", "✓ Configuration system added"]
    MENU_HEADERS = {}
    MENU_CHOICES = {}
    PROMPTS = {}
    STATUS_MESSAGES = {}
    MESSAGES = {"success": {}, "error": {}, "info": {}}
    UI_ELEMENTS = {}
    COLORS = {}

try:
    from . import config
except ImportError:
    pass

try:
    from . import update
except ImportError:
    pass

__all__ = [
    'CHANGELOG', 'MENU_HEADERS', 'MENU_CHOICES',
    'PROMPTS', 'STATUS_MESSAGES', 'MESSAGES', 'UI_ELEMENTS', 'COLORS'
]
