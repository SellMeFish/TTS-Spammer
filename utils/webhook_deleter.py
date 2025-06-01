import requests

RESET = '\033[0m'
COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'GRAY': '\033[90m',
}

def color(text, c):
    return COLORS.get(c, '') + str(text) + COLORS['ENDC']

def pretty_print(text, color_key='OKCYAN', newline=True):
    out = color(text, color_key)
    if newline:
        print(out)
    else:
        print(out, end='')

def clean_singleline_input_left(prompt):
    raw = input(prompt)
    cleaned = "".join(raw.split())
    return cleaned

def delete_webhook():
    print(color("\n=== Webhook Deleter ===\n", 'HEADER'))
    webhook_url = clean_singleline_input_left("Enter Webhook URL to delete: ")
    if not webhook_url:
        pretty_print("No webhook URL entered!", 'WARNING')
        return
    try:
        resp = requests.delete(webhook_url)
        if resp.status_code in (200, 204):
            pretty_print("Webhook deleted successfully!", 'OKGREEN')
        elif resp.status_code == 404:
            pretty_print("Webhook not found (already deleted or invalid URL).", 'WARNING')
        else:
            pretty_print(f"Failed to delete webhook: {resp.status_code} {resp.text}", 'FAIL')
    except Exception as e:
        pretty_print(f"Error: {str(e)}", 'FAIL')

def main():
    delete_webhook()

if __name__ == "__main__":
    main() 