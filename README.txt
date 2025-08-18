╔════════════════════════════════════════════════════╗
║                      BrutalForex                   ║
╚════════════════════════════════════════════════════╝

=== Tool Overview ===
Name: BrutalForex
Version: 1.0
Author: voltsparx
Contact: voltsparx@gmail.com
License: GPL-3.0 (With Ethical Use Clause)

=== Description ===
A multi-threaded brute-forcing tool designed for authorized:
- Penetration testing
- Cybersecurity competitions
- Ethical hacking education

Supported Platforms:
- Instagram
- Facebook 
- Reddit
- Discord
- Telegram

=== Features ===
• Multi-threaded attacks (15 threads by default)
• Platform-specific attack methods
• Default wordlist support (sample_wordlist.txt)
• Session/cookie handling
• Rate-limiting avoidance
• Clean termination (Ctrl+C support)
• Detailed results logging

=== Requirements ===
• Python 3.6+
• Required modules:
  - requests
  - threading
  - queue
  - os/signal
  - time

=== Installation ===
1. Ensure Python 3.6+ is installed
2. Install dependencies:
   pip install requests
3. Create sample_wordlist.txt in same directory
4. Add passwords to test (one per line)

=== Usage Instructions ===
1. Run the script:
   python3 BrutalForex.py

2. Select target platform:
   Enter number (1-5) for desired platform

3. Enter target username

4. Provide wordlist path or press Enter to use default

5. Wait for results:
   - Successful attempts saved in /results/
   - Statistics shown in console

=== Default Wordlist ===
The tool will automatically use 'sample_wordlist.txt' if:
- No wordlist path is provided
- File exists in same directory

=== Modules Used ===
• requests       - HTTP requests handling
• threading     - Concurrent attacks
• queue         - Thread-safe results
• os/signal     - System integration
• time          - Rate control

=== Ethical Warning ===
❗❗ DISCLAIMER ❗❗

This tool is provided for LEGAL, AUTHORIZED testing ONLY including:
- Penetration testing with explicit permission
- Cybersecurity competitions
- Educational purposes under supervision

STRICTLY PROHIBITED:
- Unauthorized access to systems/accounts
- Any illegal hacking activities
- Violation of privacy laws

By using this tool, you AGREE:
- You have permission to test target systems
- You accept full legal responsibility for misuse
- The author is NOT LIABLE for any damages

USE AT YOUR OWN RISK. The author disclaims all responsibility for illegal use.

=== License ===
GNU GPLv3 with additional ethical restrictions:
- See included LICENSE file for full terms

=== Contact ===
Author: voltsparx
Email: voltsparx@gmail.com
GitHub: github.com/voltsparx

Report bugs/requests to the email above.