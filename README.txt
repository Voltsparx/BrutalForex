========================================================================
                      BrutalForex v6.3 - README
========================================================================

[Description]
BrutalForex is an advanced multi-platform bruteforce tool designed for 
ethical penetration testing and cybersecurity research. It supports 
targeted attacks against Instagram, Facebook, Discord, Reddit, GitHub, 
and Roblox with platform-specific handling for each service.

[Legal Warning]
⚠️ WARNING: Unauthorized access to computer systems is illegal. 
This tool is for LEGAL penetration testing ONLY. Use only on accounts 
you own or have explicit permission to test. By using this software, 
you agree to use it ethically and legally.

[Features]
✔️ Multi-platform support (6 major social platforms)
✔️ Tor and proxy anonymity options
✔️ Platform-specific attack methods
✔️ Intelligent rate limiting
✔️ Session management
✔️ Detailed result logging
✔️ Threaded execution (50+ threads)
✔️ User-agent rotation
✔️ CSRF/fingerprint handling

[Supported Platforms]
• Instagram - Encrypted password handling
• Facebook - Form-based authentication
• Discord - API with fingerprint collection  
• Reddit - JSON response validation
• GitHub - Cookie-based sessions
• Roblox - JSON API authentication

[Requirements]
▫️ Python 3.8+
▫️ Required Libraries:
   - requests
   (Install with: pip install requests)

▫️ For Tor support:
   - Tor service installed and running
   - sudo apt install tor (Linux)
   - brew install tor (macOS)

▫️ For proxy support:
   - proxies.txt file with one proxy per line:
     socks5://ip:port
     http://ip:port

[Installation]
1. Clone the repository:
   git clone https://github.com/voltsparx/BrutalForex.git
2. Navigate to directory:
   cd BrutalForex
3. Install dependencies:
   pip install -r requirements.txt

[Usage]
Basic command:
python3 brutalforex.py -p <platform> -u <username> -w <wordlist> [options]

Required Arguments:
  -p, --platform    Target platform (instagram, facebook, discord, etc.)
  -u, --username    Target username/email
  -w, --wordlist    Path to password wordlist

Optional Arguments:
  -t, --threads     Number of threads (default: 50)
  --tor             Use Tor for anonymity
  --proxies         Use proxies from proxies.txt

Examples:
1. Attack Instagram with Tor:
   python3 brutalforex.py -p instagram -u testuser -w passwords.txt --tor -t 30

2. Attack Discord with proxies:
   python3 brutalforex.py -p discord -u user@domain.com -w rockyou.txt --proxies

3. Attack Roblox (clearnet):
   python3 brutalforex.py -p roblox -u player123 -w wordlist.txt -t 20

[Wordlist Format]
• One password per line
• UTF-8 encoding recommended
• Common wordlists: rockyou.txt, crackstation.txt

Sample wordlist:
password123
qwerty
letmein
<...>

[Result Saving]
Successful attempts are saved to:
./results/<platform>_<username>.txt

File contains:
• Platform name
• Username
• Found password  
• Attempt count
• Timestamp

[Anonymity Options]
1. Tor (Recommended):
   - Routes all traffic through Tor network
   - Enable with --tor flag
   - Requires Tor service running

2. Proxies:
   - Rotates through proxies from proxies.txt
   - Enable with --proxies flag
   - Format: socks5://ip:port or http://ip:port

[Rate Limiting]
Each platform has customized delays:
• Instagram: 0.5-2.0s between attempts
• GitHub: 1.0-4.0s (strict rate limits)
• Others: Balanced values for stealth

[Warning Messages]
❌ "Wordlist not found" - Check file path/permissions
❌ "Tor connection failed" - Verify Tor service is running
❌ "No valid passwords" - Wordlist is empty or malformed
❌ "Platform not supported" - Check -p argument

[Disclaimer]
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. 
THE AUTHOR IS NOT RESPONSIBLE FOR ANY ILLEGAL USE OF THIS TOOL. 
USERS ASSUME ALL RISK AND LIABILITY.

[Ethical Guidelines]
✔ Only test systems you own/have permission to test
✔ Respect all applicable laws
✔ Do not disrupt production systems
✔ Report vulnerabilities responsibly

[Author]
voltsparx
Contact: voltsparx@gmail.com
Repository: https://github.com/voltsparx/BrutalForex

[License]
GPL-3.0 License - See LICENSE file for details

========================================================================
