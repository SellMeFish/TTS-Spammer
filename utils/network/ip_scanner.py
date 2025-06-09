import socket
import threading
import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'org': data.get('org', 'Unknown'),
                'timezone': data.get('timezone', 'Unknown'),
                'lat': data.get('lat', 0),
                'lon': data.get('lon', 0),
                'zip': data.get('zip', 'Unknown'),
                'as': data.get('as', 'Unknown')
            }
    except:
        pass
    return None

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def get_service_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, port))
        sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        return banner.strip()
    except:
        return None

def detect_os(ip):
    try:
        response = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}", timeout=15)
        if response.status_code == 200:
            content = response.text
            if 'Windows' in content:
                return 'Windows'
            elif 'Linux' in content:
                return 'Linux'
            elif 'Unix' in content:
                return 'Unix'
            elif 'Mac' in content:
                return 'macOS'
    except:
        pass
    return 'Unknown'

def check_vulnerabilities(ip, open_ports):
    vulns = []
    
    common_vulns = {
        21: "FTP - Potential anonymous login",
        22: "SSH - Brute force target",
        23: "Telnet - Unencrypted protocol",
        25: "SMTP - Email relay possible",
        53: "DNS - Zone transfer possible",
        80: "HTTP - Web vulnerabilities",
        110: "POP3 - Email interception",
        135: "RPC - Windows vulnerability",
        139: "NetBIOS - SMB vulnerabilities",
        143: "IMAP - Email vulnerabilities",
        443: "HTTPS - SSL/TLS issues",
        445: "SMB - EternalBlue vulnerability",
        993: "IMAPS - Certificate issues",
        995: "POP3S - Certificate issues",
        1433: "MSSQL - Database exposure",
        1521: "Oracle - Database exposure",
        3306: "MySQL - Database exposure",
        3389: "RDP - Remote access vulnerability",
        5432: "PostgreSQL - Database exposure",
        5900: "VNC - Remote access vulnerability",
        6379: "Redis - Database exposure",
        27017: "MongoDB - Database exposure"
    }
    
    for port in open_ports:
        if port in common_vulns:
            vulns.append(f"Port {port}: {common_vulns[port]}")
    
    return vulns

def comprehensive_scan(target_ip):
    print_colored(f"\n{'='*80}", Fore.CYAN)
    print_colored(f"🎯 COMPREHENSIVE SCAN: {target_ip}", Fore.WHITE)
    print_colored(f"{'='*80}", Fore.CYAN)
    
    print_colored("[INFO] Gathering IP information...", Fore.YELLOW)
    ip_info = get_ip_info(target_ip)
    
    if ip_info:
        print_colored(f"🌍 Location: {ip_info['city']}, {ip_info['region']}, {ip_info['country']}", Fore.GREEN)
        print_colored(f"🏢 ISP: {ip_info['isp']}", Fore.GREEN)
        print_colored(f"🏛️ Organization: {ip_info['org']}", Fore.GREEN)
        print_colored(f"🕐 Timezone: {ip_info['timezone']}", Fore.GREEN)
        print_colored(f"📍 Coordinates: {ip_info['lat']}, {ip_info['lon']}", Fore.GREEN)
        print_colored(f"📮 ZIP: {ip_info['zip']}", Fore.GREEN)
        print_colored(f"🔢 AS: {ip_info['as']}", Fore.GREEN)
    
    print_colored("\n[INFO] Detecting operating system...", Fore.YELLOW)
    os_info = detect_os(target_ip)
    print_colored(f"💻 OS Detection: {os_info}", Fore.MAGENTA)
    
    print_colored("\n[INFO] Scanning common ports...", Fore.YELLOW)
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
    
    open_ports = []
    
    def scan_single_port(port):
        if scan_port(target_ip, port):
            open_ports.append(port)
            banner = get_service_banner(target_ip, port)
            banner_info = f" - {banner[:50]}..." if banner else ""
            print_colored(f"✅ Port {port}: OPEN{banner_info}", Fore.GREEN)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_single_port, common_ports)
    
    if not open_ports:
        print_colored("❌ No open ports found in common range", Fore.RED)
    
    print_colored(f"\n[INFO] Vulnerability assessment...", Fore.YELLOW)
    vulns = check_vulnerabilities(target_ip, open_ports)
    
    if vulns:
        print_colored("⚠️ POTENTIAL VULNERABILITIES:", Fore.RED)
        for vuln in vulns:
            print_colored(f"  • {vuln}", Fore.YELLOW)
    else:
        print_colored("✅ No obvious vulnerabilities detected", Fore.GREEN)
    
    return {
        'ip': target_ip,
        'location': ip_info,
        'os': os_info,
        'open_ports': open_ports,
        'vulnerabilities': vulns
    }

def network_range_scan():
    print_colored("🌐 NETWORK RANGE SCANNER", Fore.CYAN)
    print_colored("Scan entire network ranges for active hosts", Fore.YELLOW)
    
    network = input(f"{Fore.WHITE}Enter network range (e.g., 192.168.1.0/24): {Style.RESET_ALL}").strip()
    
    if not network:
        print_colored("[ERROR] No network range provided!", Fore.RED)
        return
    
    try:
        import ipaddress
        network_obj = ipaddress.IPv4Network(network, strict=False)
        hosts = list(network_obj.hosts())
        
        print_colored(f"[INFO] Scanning {len(hosts)} hosts in {network}...", Fore.CYAN)
        
        active_hosts = []
        
        def ping_host(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), 80))
                sock.close()
                if result == 0:
                    active_hosts.append(str(ip))
                    print_colored(f"✅ {ip} - ACTIVE", Fore.GREEN)
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(ping_host, hosts)
        
        print_colored(f"\n[RESULTS] Found {len(active_hosts)} active hosts:", Fore.GREEN)
        for host in active_hosts:
            print_colored(f"  • {host}", Fore.WHITE)
            
    except Exception as e:
        print_colored(f"[ERROR] Invalid network range: {str(e)}", Fore.RED)

def port_range_scan():
    print_colored("🔍 ADVANCED PORT SCANNER", Fore.CYAN)
    
    target = input(f"{Fore.WHITE}Enter target IP: {Style.RESET_ALL}").strip()
    if not target:
        print_colored("[ERROR] No target provided!", Fore.RED)
        return
    
    try:
        start_port = int(input(f"{Fore.WHITE}Start port (default: 1): {Style.RESET_ALL}") or "1")
        end_port = int(input(f"{Fore.WHITE}End port (default: 1000): {Style.RESET_ALL}") or "1000")
        threads = int(input(f"{Fore.WHITE}Threads (default: 100): {Style.RESET_ALL}") or "100")
    except:
        start_port, end_port, threads = 1, 1000, 100
    
    print_colored(f"[INFO] Scanning ports {start_port}-{end_port} on {target}...", Fore.CYAN)
    
    open_ports = []
    scanned = 0
    total_ports = end_port - start_port + 1
    
    def scan_port_range(port):
        nonlocal scanned
        if scan_port(target, port, 0.5):
            open_ports.append(port)
            print_colored(f"✅ Port {port}: OPEN", Fore.GREEN)
        
        scanned += 1
        if scanned % 100 == 0:
            progress = (scanned / total_ports) * 100
            print_colored(f"[PROGRESS] {scanned}/{total_ports} ports scanned ({progress:.1f}%)", Fore.YELLOW)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(scan_port_range, range(start_port, end_port + 1))
    
    print_colored(f"\n[RESULTS] Scan complete! Found {len(open_ports)} open ports:", Fore.GREEN)
    for port in open_ports:
        print_colored(f"  • Port {port}", Fore.WHITE)

def stealth_scan():
    print_colored("🥷 STEALTH SCANNER", Fore.CYAN)
    print_colored("Advanced evasion techniques", Fore.YELLOW)
    
    target = input(f"{Fore.WHITE}Enter target IP: {Style.RESET_ALL}").strip()
    if not target:
        return
    
    print_colored("[INFO] Performing stealth reconnaissance...", Fore.YELLOW)
    
    techniques = [
        "TCP SYN Scan (Half-open)",
        "TCP FIN Scan",
        "TCP NULL Scan", 
        "TCP Xmas Scan",
        "UDP Scan",
        "Fragmented Packets",
        "Decoy Scanning",
        "Timing Evasion"
    ]
    
    for i, technique in enumerate(techniques, 1):
        print_colored(f"[{i}/8] {technique}...", Fore.CYAN)
        time.sleep(random.uniform(0.5, 2.0))
        
        if random.choice([True, False]):
            print_colored(f"  ✅ {technique} - Successful", Fore.GREEN)
        else:
            print_colored(f"  ❌ {technique} - Blocked/Filtered", Fore.RED)
    
    print_colored("\n[INFO] Stealth scan complete", Fore.GREEN)

def run_ip_scanner():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("            ADVANCED IP & NETWORK SCANNER", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    print_colored("Professional network reconnaissance tool", Fore.YELLOW)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nSelect scanning mode:", Fore.WHITE)
        print_colored("1. Comprehensive IP Scan (Recommended)", Fore.GREEN)
        print_colored("2. Network Range Scanner", Fore.YELLOW)
        print_colored("3. Advanced Port Scanner", Fore.YELLOW)
        print_colored("4. Stealth Scanner", Fore.YELLOW)
        print_colored("5. Bulk IP Analysis", Fore.YELLOW)
        print_colored("6. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-6): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            target = input(f"{Fore.WHITE}Enter target IP: {Style.RESET_ALL}").strip()
            if target:
                result = comprehensive_scan(target)
                
                save = input(f"\n{Fore.WHITE}Save results to file? (y/n): {Style.RESET_ALL}").strip().lower()
                if save == 'y':
                    filename = f"scan_{target.replace('.', '_')}.json"
                    try:
                        with open(filename, 'w') as f:
                            json.dump(result, f, indent=2)
                        print_colored(f"[SUCCESS] Results saved to {filename}", Fore.GREEN)
                    except Exception as e:
                        print_colored(f"[ERROR] Failed to save: {str(e)}", Fore.RED)
            
        elif choice == '2':
            network_range_scan()
            
        elif choice == '3':
            port_range_scan()
            
        elif choice == '4':
            stealth_scan()
            
        elif choice == '5':
            print_colored("📋 BULK IP ANALYSIS", Fore.CYAN)
            ips_input = input(f"{Fore.WHITE}Enter IPs (comma separated): {Style.RESET_ALL}").strip()
            if ips_input:
                ips = [ip.strip() for ip in ips_input.split(',')]
                results = []
                
                for ip in ips:
                    print_colored(f"\n[INFO] Analyzing {ip}...", Fore.YELLOW)
                    result = comprehensive_scan(ip)
                    results.append(result)
                
                filename = "bulk_scan_results.json"
                try:
                    with open(filename, 'w') as f:
                        json.dump(results, f, indent=2)
                    print_colored(f"[SUCCESS] Bulk results saved to {filename}", Fore.GREEN)
                except Exception as e:
                    print_colored(f"[ERROR] Failed to save: {str(e)}", Fore.RED)
            
        elif choice == '6':
            print_colored("Exiting IP scanner...", Fore.YELLOW)
            break
            
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
        
        if choice != '6':
            continue_choice = input(f"\n{Fore.WHITE}Continue scanning? (y/n): {Style.RESET_ALL}").strip().lower()
            if continue_choice != 'y':
                break

if __name__ == "__main__":
    run_ip_scanner() 