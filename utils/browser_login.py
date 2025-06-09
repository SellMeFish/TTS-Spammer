import webbrowser
import time
import os
import sys
import subprocess
from colorama import Fore, Style, init

init()

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

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

def pretty_print(text, color=(255,64,64)):
    ansi = rgb(*color)
    line = center(text)
    print(ansi + line + '\033[0m')

def open_in_new_terminal(token):
    """Open browser login in a new terminal window"""
    try:
        script_path = os.path.abspath(__file__)
        
        if os.name == 'nt':
            cmd = f'powershell -Command "Start-Process python -ArgumentList \\"{script_path}\\", \\"{token}\\" -WindowStyle Normal"'
            subprocess.Popen(cmd, shell=True)
            pretty_print("Browser login opened in new terminal window!", (0, 255, 0))
            return True
        else:
            terminals = ['gnome-terminal', 'xterm', 'konsole', 'terminal']
            for term in terminals:
                try:
                    if term == 'gnome-terminal':
                        subprocess.Popen([term, '--', 'python3', script_path, token])
                    else:
                        subprocess.Popen([term, '-e', f'python3 {script_path} {token}'])
                    pretty_print("Browser login opened in new terminal window!", (0, 255, 0))
                    return True
                except FileNotFoundError:
                    continue
            
            subprocess.Popen(['python3', script_path, token])
            pretty_print("Browser login started in background!", (255, 255, 0))
            return True
            
    except Exception as e:
        pretty_print(f"Error opening new terminal: {str(e)}", (255, 0, 0))
        pretty_print("Falling back to current terminal...", (255, 255, 0))
        return False

def inject_token_browser(token):
    try:
        import tempfile
        
        script_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discord Token Login</title>
            <style>
                body {{
                    background: #2c2f33;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #36393f;
                    padding: 30px;
                    border-radius: 10px;
                }}
                .button {{
                    background: #7289da;
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 10px;
                }}
                .button:hover {{
                    background: #677bc4;
                }}
                .status {{
                    margin: 20px 0;
                    padding: 10px;
                    border-radius: 5px;
                }}
                .success {{
                    background: #43b581;
                }}
                .error {{
                    background: #f04747;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Discord Token Login</h1>
                <p>Click the button below to inject your token and login to Discord.</p>
                <button class="button" onclick="injectToken()">Inject Token & Login</button>
                <div id="status"></div>
                <p><small>This will open Discord in a new tab and automatically log you in.</small></p>
            </div>
            
            <script>
                function injectToken() {{
                    const status = document.getElementById('status');
                    status.innerHTML = '<div class="status">Injecting token...</div>';
                    
                    try {{
                        // Open Discord
                        const discordWindow = window.open('https://discord.com/login', '_blank');
                        
                        setTimeout(() => {{
                            try {{
                                // Inject token
                                discordWindow.localStorage.setItem('token', '"{token}"');
                                
                                setTimeout(() => {{
                                    discordWindow.location.reload();
                                    status.innerHTML = '<div class="status success">Token injected successfully! Check the Discord tab.</div>';
                                }}, 1000);
                                
                            }} catch (e) {{
                                status.innerHTML = '<div class="status error">Injection failed. Please try manually.</div>';
                            }}
                        }}, 2000);
                        
                    }} catch (e) {{
                        status.innerHTML = '<div class="status error">Failed to open Discord. Please check your browser settings.</div>';
                    }}
                }}
                
                // Auto-inject after 3 seconds
                setTimeout(() => {{
                    injectToken();
                }}, 3000);
            </script>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(script_content)
            temp_file = f.name
        
        webbrowser.open(f'file://{temp_file}')
        return True
        
    except Exception as e:
        pretty_print(f"Error creating injection page: {str(e)}", (255, 0, 0))
        return False

def run_browser_login(token=None):
    """Browser Login Function"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pretty_print("Discord Browser Login", (255, 128, 0))
    print()
    
    if not token:
        token = input(rgb(255, 32, 32) + center("Enter Discord Token: ") + '\033[0m').strip()
        
    if not token:
        pretty_print("No token provided!", (255, 0, 0))
        return False
    
    pretty_print("This will open Discord in your browser with token injection", (255, 255, 0))
    confirm = input(rgb(255, 32, 32) + center("Continue? (y/n): ") + '\033[0m')
    
    if confirm.lower() != 'y':
        pretty_print("Cancelled!", (255, 0, 0))
        return False
    
    try:
        pretty_print("Opening browser with token injection...", (255, 128, 0))
        
        if inject_token_browser(token):
            pretty_print("Browser opened successfully!", (0, 255, 0))
            pretty_print("Token will be injected automatically", (255, 255, 0))
            pretty_print("Check your browser for Discord login", (255, 255, 0))
            return True
        else:
            return False
            
    except Exception as e:
        pretty_print(f"Error: {str(e)}", (255, 0, 0))
        return False

def run_browser_login_new_window(token):
    """Run browser login in a new terminal window"""
    try:
        if open_in_new_terminal(token):
            return True
        else:
            return run_browser_login(token)
    except Exception as e:
        pretty_print(f"Error: {str(e)}", (255, 0, 0))
        return False

def main():
    if len(sys.argv) > 1:
        token = sys.argv[1]
        run_browser_login(token)
    else:
        run_browser_login()
    
    input(rgb(255, 32, 32) + center("Press Enter to continue...") + '\033[0m')

if __name__ == "__main__":
    main()
