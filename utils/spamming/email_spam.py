import requests
import time
import json
from colorama import Fore, Style, init

init()

def send_email_spam(emails, subject, message, amount=10, interval=1, debug=False):
    results = []
    
    if debug:
        print(f"{Fore.CYAN}[DEBUG] Email Spam started{Style.RESET_ALL}")
    
    for i in range(amount):
        for email in emails:
            print(f"{Fore.YELLOW}Sending email {i+1}/{amount} to {email}...{Style.RESET_ALL}")
            
            result = {
                'success': True,
                'email': email,
                'subject': subject,
                'message_number': i + 1
            }
            
            results.append(result)
            print(f"{Fore.GREEN}  ✓ Email simulated (not actually sent){Style.RESET_ALL}")
            
            time.sleep(interval)
    
    return results

def run_email_spam():
    print(f"{Fore.CYAN}Email Spam Tool{Style.RESET_ALL}")
    print(f"{Fore.RED}WARNING: Educational purposes only!{Style.RESET_ALL}")
    
    emails = []
    print(f"{Fore.YELLOW}Enter email addresses (one per line, empty line to finish):{Style.RESET_ALL}")
    while True:
        email = input().strip()
        if not email:
            break
        emails.append(email)
    
    if not emails:
        print(f"{Fore.RED}No email addresses provided{Style.RESET_ALL}")
        return
    
    subject = input(f"{Fore.YELLOW}Enter subject: {Style.RESET_ALL}").strip()
    if not subject:
        subject = "Test Email"
    
    message = input(f"{Fore.YELLOW}Enter message: {Style.RESET_ALL}").strip()
    if not message:
        message = "This is a test email"
    
    try:
        amount = int(input(f"{Fore.YELLOW}Number of emails per address: {Style.RESET_ALL}"))
    except ValueError:
        amount = 1
    
    try:
        interval = float(input(f"{Fore.YELLOW}Interval between emails (seconds): {Style.RESET_ALL}"))
    except ValueError:
        interval = 1
    
    debug = input(f"{Fore.YELLOW}Enable debug mode? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    print(f"{Fore.RED}\nNOTE: This is only a simulation. No real emails will be sent.{Style.RESET_ALL}")
    confirm = input(f"{Fore.YELLOW}Continue? (y/n): {Style.RESET_ALL}").lower()
    
    if confirm == 'y':
        results = send_email_spam(emails, subject, message, amount, interval, debug)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"\n{Fore.CYAN}Result: {success_count}/{total_count} emails simulated{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")

if __name__ == "__main__":
    run_email_spam() 