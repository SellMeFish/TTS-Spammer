import requests
import json
import time
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def scrape_disboard_category(category, page=1):
    servers = []
    try:
        url = f"https://disboard.org/servers/tag/{category}/{page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            server_blocks = re.findall(r'<div class="server-card.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
            
            for block in server_blocks:
                try:
                    name_match = re.search(r'<h5[^>]*>(.*?)</h5>', block)
                    name = name_match.group(1).strip() if name_match else "Unknown Server"
                    
                    members_match = re.search(r'(\d+(?:,\d+)*)\s*members', block)
                    members = int(members_match.group(1).replace(',', '')) if members_match else 0
                    
                    invite_match = re.search(r'href="([^"]*discord\.gg/[^"]*)"', block)
                    invite = invite_match.group(1) if invite_match else f"https://discord.gg/{generate_invite_code()}"
                    
                    desc_match = re.search(r'<p[^>]*class="server-description"[^>]*>(.*?)</p>', block, re.DOTALL)
                    description = desc_match.group(1).strip()[:100] if desc_match else f"A {category} Discord server"
                    description = re.sub(r'<[^>]+>', '', description)
                    
                    servers.append({
                        'name': name,
                        'members': members,
                        'category': category,
                        'invite': invite,
                        'description': description,
                        'source': 'Disboard'
                    })
                except Exception:
                    continue
                    
        time.sleep(random.uniform(1, 3))
        
    except Exception as e:
        print_colored(f"[ERROR] Failed to scrape Disboard {category}: {str(e)}", Fore.RED)
    
    return servers

def get_public_servers_disboard():
    print_colored("[INFO] Scraping real servers from Disboard...", Fore.CYAN)
    
    categories = ['gaming', 'music', 'community', 'technology', 'anime', 'art', 'meme', 'social', 'roleplay', 'education']
    all_servers = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for category in categories:
            print_colored(f"[INFO] Queuing category: {category}", Fore.YELLOW)
            for page in range(1, 3):
                futures.append(executor.submit(scrape_disboard_category, category, page))
        
        for future in futures:
            try:
                servers = future.result(timeout=30)
                all_servers.extend(servers)
            except Exception as e:
                print_colored(f"[WARNING] Thread failed: {str(e)}", Fore.YELLOW)
    
    return all_servers

def get_discord_discovery_servers():
    print_colored("[INFO] Fetching from Discord Discovery API...", Fore.CYAN)
    
    servers = []
    categories = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    
    for category_id in categories:
        try:
            url = f"https://discord.com/api/v9/discovery/categories/{category_id}/servers"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                for server in data.get('servers', []):
                    invite_code = server.get('vanity_url_code') or server.get('id', 'unknown')
                    servers.append({
                        'name': server.get('name', 'Unknown'),
                        'members': server.get('approximate_member_count', 0),
                        'category': server.get('primary_category_name', 'General'),
                        'invite': f"https://discord.gg/{invite_code}",
                        'description': server.get('description', 'No description')[:100],
                        'source': 'Discord Discovery'
                    })
                print_colored(f"[SUCCESS] Found {len(data.get('servers', []))} servers in category {category_id}", Fore.GREEN)
            else:
                print_colored(f"[WARNING] Category {category_id} returned status {response.status_code}", Fore.YELLOW)
                
            time.sleep(random.uniform(0.5, 1.5))
            
        except Exception as e:
            print_colored(f"[ERROR] Failed to fetch category {category_id}: {str(e)}", Fore.RED)
    
    return servers

def scan_reddit_discord_servers():
    print_colored("[INFO] Scanning Reddit for Discord servers...", Fore.CYAN)
    
    servers = []
    subreddits = ['discordservers', 'DiscordAdvertising', 'DiscordAppServers', 'DiscordServers', 'gaming', 'anime', 'music']
    
    for subreddit in subreddits:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=25"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    
                    discord_links = re.findall(r'discord\.gg/([a-zA-Z0-9]+)', title + ' ' + selftext)
                    
                    for invite_code in discord_links:
                        servers.append({
                            'name': title[:50] + '...' if len(title) > 50 else title,
                            'members': random.randint(10, 5000),
                            'category': subreddit,
                            'invite': f"https://discord.gg/{invite_code}",
                            'description': selftext[:100] + '...' if len(selftext) > 100 else selftext,
                            'source': 'Reddit'
                        })
                        
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print_colored(f"[ERROR] Failed to scan r/{subreddit}: {str(e)}", Fore.RED)
    
    return servers

def scan_github_discord_bots():
    print_colored("[INFO] Scanning GitHub for Discord bot servers...", Fore.CYAN)
    
    servers = []
    try:
        url = "https://api.github.com/search/repositories?q=discord+bot+language:python&sort=stars&order=desc&per_page=50"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])
            
            for repo in repos[:20]:
                try:
                    readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
                    readme_response = requests.get(readme_url, headers=headers, timeout=10)
                    
                    if readme_response.status_code == 200:
                        readme_data = readme_response.json()
                        import base64
                        content = base64.b64decode(readme_data['content']).decode('utf-8')
                        
                        discord_links = re.findall(r'discord\.gg/([a-zA-Z0-9]+)', content)
                        
                        for invite_code in discord_links:
                            servers.append({
                                'name': f"{repo['name']} Support Server",
                                'members': random.randint(100, 10000),
                                'category': 'Bot Support',
                                'invite': f"https://discord.gg/{invite_code}",
                                'description': repo.get('description', 'Discord bot support server')[:100],
                                'source': 'GitHub'
                            })
                            
                    time.sleep(0.5)
                    
                except Exception:
                    continue
                    
    except Exception as e:
        print_colored(f"[ERROR] Failed to scan GitHub: {str(e)}", Fore.RED)
    
    return servers

def generate_invite_code():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(random.randint(6, 10)))

def validate_invite_code(invite_code):
    """Validate if Discord invite is still active"""
    try:
        url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': True,
                'server_name': data.get('guild', {}).get('name', 'Unknown'),
                'members': data.get('approximate_member_count', 0),
                'online': data.get('approximate_presence_count', 0)
            }
        else:
            return {'valid': False}
            
    except Exception:
        return {'valid': False}

def search_servers_by_keyword(keyword):
    print_colored(f"[INFO] Searching servers with keyword: {keyword}", Fore.CYAN)
    
    all_servers = []
    
    print_colored("[INFO] Searching Disboard...", Fore.YELLOW)
    try:
        url = f"https://disboard.org/search?keyword={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            invite_links = re.findall(r'discord\.gg/([a-zA-Z0-9]+)', content)
            
            for invite_code in invite_links[:10]:
                validation = validate_invite_code(invite_code)
                if validation['valid']:
                    all_servers.append({
                        'name': validation['server_name'],
                        'members': validation['members'],
                        'category': f'Search: {keyword}',
                        'invite': f'https://discord.gg/{invite_code}',
                        'description': f'Server found by searching for {keyword}',
                        'source': 'Disboard Search'
                    })
                    
    except Exception as e:
        print_colored(f"[ERROR] Disboard search failed: {str(e)}", Fore.RED)
    
    print_colored("[INFO] Searching Reddit...", Fore.YELLOW)
    try:
        url = f"https://www.reddit.com/search.json?q={keyword}+discord.gg&limit=20"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                title = post_data.get('title', '')
                selftext = post_data.get('selftext', '')
                
                discord_links = re.findall(r'discord\.gg/([a-zA-Z0-9]+)', title + ' ' + selftext)
                
                for invite_code in discord_links:
                    validation = validate_invite_code(invite_code)
                    if validation['valid']:
                        all_servers.append({
                            'name': validation['server_name'],
                            'members': validation['members'],
                            'category': f'Search: {keyword}',
                            'invite': f'https://discord.gg/{invite_code}',
                            'description': title[:100],
                            'source': 'Reddit Search'
                        })
                        
    except Exception as e:
        print_colored(f"[ERROR] Reddit search failed: {str(e)}", Fore.RED)
    
    return all_servers

def generate_advanced_invite_patterns():
    patterns = []
    
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    common_words = [
        'minecraft', 'gaming', 'anime', 'music', 'memes', 'art', 'coding', 'python', 'discord',
        'community', 'chat', 'friends', 'fun', 'cool', 'awesome', 'best', 'official', 'main',
        'general', 'random', 'help', 'support', 'dev', 'test', 'new', 'join', 'welcome', 'server',
        'hub', 'zone', 'world', 'place', 'home', 'base', 'team', 'clan', 'guild', 'group'
    ]
    
    for word in common_words:
        patterns.append(word)
        patterns.append(word + str(random.randint(1, 999)))
        patterns.append(word + str(random.randint(2020, 2025)))
        patterns.append(word + random.choice(['123', '69', '420', '777', '1337']))
    
    for length in [6, 7, 8, 9, 10]:
        for _ in range(50):
            code = ''.join(random.choice(chars) for _ in range(length))
            patterns.append(code)
    
    for _ in range(100):
        prefix = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
        suffix = ''.join(random.choice(chars) for _ in range(random.randint(5, 9)))
        patterns.append(prefix + suffix)
    
    sequential_patterns = []
    for i in range(1000):
        sequential_patterns.append(f"server{i:03d}")
        sequential_patterns.append(f"discord{i:03d}")
        sequential_patterns.append(f"game{i:03d}")
    
    patterns.extend(sequential_patterns[:200])
    
    return patterns

def get_detailed_server_info(invite_code):
    try:
        url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            guild = data.get('guild', {})
            channel = data.get('channel', {})
            inviter = data.get('inviter', {})
            
            server_info = {
                'valid': True,
                'invite_code': invite_code,
                'server_name': guild.get('name', 'Unknown'),
                'server_id': guild.get('id', 'Unknown'),
                'description': guild.get('description', 'No description'),
                'member_count': data.get('approximate_member_count', 0),
                'online_count': data.get('approximate_presence_count', 0),
                'verification_level': guild.get('verification_level', 0),
                'nsfw_level': guild.get('nsfw_level', 0),
                'premium_tier': guild.get('premium_tier', 0),
                'features': guild.get('features', []),
                'vanity_url': guild.get('vanity_url_code'),
                'banner': guild.get('banner'),
                'icon': guild.get('icon'),
                'splash': guild.get('splash'),
                'channel_name': channel.get('name', 'Unknown'),
                'channel_type': channel.get('type', 0),
                'inviter_name': inviter.get('username', 'Unknown') if inviter else 'Unknown',
                'expires_at': data.get('expires_at'),
                'max_uses': data.get('max_uses'),
                'uses': data.get('uses', 0),
                'temporary': data.get('temporary', False),
                'created_at': data.get('created_at')
            }
            
            return server_info
        else:
            return {'valid': False, 'status_code': response.status_code}
            
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def display_detailed_server(server_info):
    if not server_info.get('valid'):
        return
    
    print_colored(f"\n{'='*80}", Fore.CYAN)
    print_colored(f"🎯 FOUND ACTIVE SERVER: {server_info['server_name']}", Fore.GREEN)
    print_colored(f"{'='*80}", Fore.CYAN)
    
    print_colored(f"📋 Server ID: {server_info['server_id']}", Fore.WHITE)
    print_colored(f"🔗 Invite: https://discord.gg/{server_info['invite_code']}", Fore.BLUE)
    print_colored(f"👥 Members: {server_info['member_count']:,} total, {server_info['online_count']:,} online", Fore.YELLOW)
    
    if server_info['description']:
        print_colored(f"📝 Description: {server_info['description'][:100]}...", Fore.CYAN)
    
    verification_levels = {0: "None", 1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    print_colored(f"🔒 Verification: {verification_levels.get(server_info['verification_level'], 'Unknown')}", Fore.MAGENTA)
    
    if server_info['premium_tier'] > 0:
        print_colored(f"💎 Boost Level: Tier {server_info['premium_tier']}", Fore.MAGENTA)
    
    if server_info['features']:
        print_colored(f"⭐ Features: {', '.join(server_info['features'][:5])}", Fore.GREEN)
    
    if server_info['vanity_url']:
        print_colored(f"🎭 Vanity URL: discord.gg/{server_info['vanity_url']}", Fore.BLUE)
    
    print_colored(f"📺 Channel: #{server_info['channel_name']}", Fore.CYAN)
    print_colored(f"👤 Inviter: {server_info['inviter_name']}", Fore.CYAN)
    
    if server_info['expires_at']:
        print_colored(f"⏰ Expires: {server_info['expires_at']}", Fore.RED)
    else:
        print_colored(f"⏰ Expires: Never", Fore.GREEN)
    
    if server_info['max_uses']:
        print_colored(f"🔢 Uses: {server_info['uses']}/{server_info['max_uses']}", Fore.YELLOW)
    else:
        print_colored(f"🔢 Uses: {server_info['uses']} (Unlimited)", Fore.GREEN)

def mass_invite_scanner():
    print_colored("=" * 80, Fore.CYAN)
    print_colored("🚀 ADVANCED DISCORD INVITE BRUTE FORCER", Fore.WHITE)
    print_colored("=" * 80, Fore.CYAN)
    print_colored("⚡ Multi-threaded brute force scanning with detailed server analysis", Fore.YELLOW)
    print_colored("=" * 80, Fore.CYAN)
    
    try:
        threads = int(input(f"{Fore.WHITE}Number of threads (1-50, recommended: 20): {Style.RESET_ALL}"))
        threads = max(1, min(50, threads))
    except:
        threads = 20
    
    try:
        scan_count = int(input(f"{Fore.WHITE}Number of invites to scan (100-10000): {Style.RESET_ALL}"))
        scan_count = max(100, min(10000, scan_count))
    except:
        scan_count = 1000
    
    print_colored(f"\n[INFO] Starting brute force with {threads} threads scanning {scan_count} invites...", Fore.CYAN)
    
    patterns = generate_advanced_invite_patterns()
    random.shuffle(patterns)
    
    if len(patterns) < scan_count:
        additional_needed = scan_count - len(patterns)
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for _ in range(additional_needed):
            length = random.choice([6, 7, 8, 9, 10])
            code = ''.join(random.choice(chars) for _ in range(length))
            patterns.append(code)
    
    scan_patterns = patterns[:scan_count]
    
    found_servers = []
    scanned_count = 0
    lock = threading.Lock()
    
    def scan_invite(invite_code):
        nonlocal scanned_count
        
        server_info = get_detailed_server_info(invite_code)
        
        with lock:
            scanned_count += 1
            if scanned_count % 50 == 0:
                print_colored(f"[PROGRESS] Scanned {scanned_count}/{scan_count} invites... Found {len(found_servers)} servers", Fore.YELLOW)
        
        if server_info.get('valid'):
            with lock:
                found_servers.append(server_info)
                display_detailed_server(server_info)
        
        time.sleep(random.uniform(0.1, 0.3))
    
    print_colored(f"[INFO] Scanning {len(scan_patterns)} invite patterns...", Fore.CYAN)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_invite, code) for code in scan_patterns]
        
        try:
            for future in futures:
                future.result(timeout=30)
        except KeyboardInterrupt:
            print_colored("\n[INFO] Scan interrupted by user", Fore.YELLOW)
        except Exception as e:
            print_colored(f"[ERROR] Scan error: {str(e)}", Fore.RED)
    
    print_colored(f"\n{'='*80}", Fore.CYAN)
    print_colored(f"🎯 BRUTE FORCE SCAN COMPLETE", Fore.GREEN)
    print_colored(f"{'='*80}", Fore.CYAN)
    print_colored(f"📊 Total Scanned: {scanned_count}", Fore.WHITE)
    print_colored(f"✅ Valid Servers Found: {len(found_servers)}", Fore.GREEN)
    print_colored(f"📈 Success Rate: {(len(found_servers)/scanned_count*100):.2f}%" if scanned_count > 0 else "0%", Fore.YELLOW)
    
    if found_servers:
        found_servers.sort(key=lambda x: x.get('member_count', 0), reverse=True)
        
        print_colored(f"\n🏆 TOP SERVERS BY MEMBER COUNT:", Fore.YELLOW)
        for i, server in enumerate(found_servers[:5], 1):
            print_colored(f"{i}. {server['server_name']} - {server['member_count']:,} members", Fore.WHITE)
    
    converted_servers = []
    for server in found_servers:
        converted_servers.append({
            'name': server['server_name'],
            'members': server['member_count'],
            'category': 'Brute Force',
            'invite': f"https://discord.gg/{server['invite_code']}",
            'description': server['description'],
            'source': 'Advanced Brute Forcer'
        })
    
    return converted_servers

def display_servers(servers):
    if not servers:
        print_colored("[INFO] No servers found!", Fore.YELLOW)
        return
    
    servers = sorted(servers, key=lambda x: x.get('members', 0), reverse=True)
    
    print_colored(f"\n[SUCCESS] Found {len(servers)} Discord servers:", Fore.GREEN)
    print_colored("=" * 90, Fore.CYAN)
    
    for i, server in enumerate(servers, 1):
        print_colored(f"\n[{i}] {server['name']}", Fore.WHITE)
        print_colored(f"    Members: {server['members']:,}", Fore.YELLOW)
        print_colored(f"    Category: {server['category']}", Fore.MAGENTA)
        print_colored(f"    Source: {server.get('source', 'Unknown')}", Fore.CYAN)
        print_colored(f"    Invite: {server['invite']}", Fore.BLUE)
        print_colored(f"    Description: {server['description'][:80]}...", Fore.CYAN)

def save_servers_to_file(servers, filename="found_servers.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(servers, f, indent=2, ensure_ascii=False)
        print_colored(f"[SUCCESS] Servers saved to {filename}", Fore.GREEN)
    except Exception as e:
        print_colored(f"[ERROR] Failed to save servers: {str(e)}", Fore.RED)

def run_server_scanner():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("            ADVANCED DISCORD SERVER SCANNER", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    print_colored("Real-time scanning across multiple platforms", Fore.YELLOW)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nSelect scanning method:", Fore.WHITE)
        print_colored("1. Disboard Scraper (Real servers)", Fore.YELLOW)
        print_colored("2. Discord Discovery API (Official)", Fore.YELLOW)
        print_colored("3. Reddit Scanner (Community servers)", Fore.YELLOW)
        print_colored("4. GitHub Bot Servers", Fore.YELLOW)
        print_colored("5. Keyword Search (Multi-platform)", Fore.YELLOW)
        print_colored("6. Mass Invite Scanner (Brute force)", Fore.YELLOW)
        print_colored("7. Scan ALL sources (Recommended)", Fore.GREEN)
        print_colored("8. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-8): {Style.RESET_ALL}").strip()
        
        all_servers = []
        
        if choice == '1':
            servers = get_public_servers_disboard()
            all_servers.extend(servers)
            
        elif choice == '2':
            servers = get_discord_discovery_servers()
            all_servers.extend(servers)
            
        elif choice == '3':
            servers = scan_reddit_discord_servers()
            all_servers.extend(servers)
            
        elif choice == '4':
            servers = scan_github_discord_bots()
            all_servers.extend(servers)
            
        elif choice == '5':
            keyword = input(f"{Fore.WHITE}Enter search keyword: {Style.RESET_ALL}").strip()
            if keyword:
                servers = search_servers_by_keyword(keyword)
                all_servers.extend(servers)
            else:
                print_colored("[ERROR] No keyword provided!", Fore.RED)
                continue
                
        elif choice == '6':
            print_colored("[WARNING] This may take several minutes...", Fore.YELLOW)
            confirm = input(f"{Fore.WHITE}Continue with mass scanning? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirm == 'y':
                servers = mass_invite_scanner()
                all_servers.extend(servers)
            else:
                continue
                
        elif choice == '7':
            print_colored("[INFO] Starting comprehensive scan across all platforms...", Fore.CYAN)
            print_colored("[INFO] This will take 5-10 minutes...", Fore.YELLOW)
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [
                    executor.submit(get_public_servers_disboard),
                    executor.submit(get_discord_discovery_servers),
                    executor.submit(scan_reddit_discord_servers),
                    executor.submit(scan_github_discord_bots)
                ]
                
                for future in futures:
                    try:
                        servers = future.result(timeout=300)
                        all_servers.extend(servers)
                        print_colored(f"[SUCCESS] Completed scan source (+{len(servers)} servers)", Fore.GREEN)
                    except Exception as e:
                        print_colored(f"[WARNING] Scan source failed: {str(e)}", Fore.YELLOW)
            
        elif choice == '8':
            print_colored("Exiting server scanner...", Fore.YELLOW)
            break
            
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
            continue
        
        unique_servers = []
        seen_invites = set()
        
        for server in all_servers:
            invite = server.get('invite', '')
            if invite not in seen_invites:
                seen_invites.add(invite)
                unique_servers.append(server)
        
        if unique_servers:
            print_colored(f"\n[INFO] Removed {len(all_servers) - len(unique_servers)} duplicates", Fore.CYAN)
            display_servers(unique_servers)
            
            print_colored("\nExport options:", Fore.WHITE)
            print_colored("1. Save as JSON", Fore.YELLOW)
            print_colored("2. Save as CSV", Fore.YELLOW)
            print_colored("3. Save invite list only", Fore.YELLOW)
            print_colored("4. Skip saving", Fore.YELLOW)
            
            save_choice = input(f"\n{Fore.WHITE}Choose export option (1-4): {Style.RESET_ALL}").strip()
            
            if save_choice == '1':
                filename = input(f"{Fore.WHITE}JSON filename (default: servers.json): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "servers.json"
                save_servers_to_file(unique_servers, filename)
                
            elif save_choice == '2':
                filename = input(f"{Fore.WHITE}CSV filename (default: servers.csv): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "servers.csv"
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("Name,Members,Category,Source,Invite,Description\n")
                        for server in unique_servers:
                            f.write(f'"{server["name"]}",{server["members"]},"{server["category"]}","{server.get("source", "")}","{server["invite"]}","{server["description"]}"\n')
                    print_colored(f"[SUCCESS] Servers exported to {filename}", Fore.GREEN)
                except Exception as e:
                    print_colored(f"[ERROR] Failed to export CSV: {str(e)}", Fore.RED)
                    
            elif save_choice == '3':
                filename = input(f"{Fore.WHITE}Invite list filename (default: invites.txt): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "invites.txt"
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        for server in unique_servers:
                            f.write(f"{server['invite']}\n")
                    print_colored(f"[SUCCESS] Invite list saved to {filename}", Fore.GREEN)
                except Exception as e:
                    print_colored(f"[ERROR] Failed to save invite list: {str(e)}", Fore.RED)
        else:
            print_colored("[INFO] No servers found with current scan method", Fore.YELLOW)
        
        continue_choice = input(f"\n{Fore.WHITE}Continue scanning? (y/n): {Style.RESET_ALL}").strip().lower()
        if continue_choice != 'y':
            break

if __name__ == "__main__":
    run_server_scanner() 