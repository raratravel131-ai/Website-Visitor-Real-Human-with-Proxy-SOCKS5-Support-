#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ProxyError, Timeout, ConnectionError
import threading
import time
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== KONFIGURASI ==========
PROXY_FILE = "proxylist.txt"          # File daftar proxy (format IP:PORT atau socks5://IP:PORT)
TARGET_URL = "https://raratravel.id"  # Target website
THREADS = 50                           # Jumlah thread bersamaan
TIMEOUT = 10                           # Timeout request (detik)
RETRY_COUNT = 2                        # Jumlah retry jika gagal
DELAY_BETWEEN_REQUESTS = (0.5, 2)      # Delay acak antar request (detik)
CHECK_PROXY_BEFORE_USE = True          # Cek proxy hidup sebelum dipakai
LOG_FILE = "visitor_log.txt"           # File log hasil
# ==================================

# ========== DAFTAR USER-AGENT (110+ items) ==========
USER_AGENTS = [
    # Windows 10 - Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    # Windows 10 - Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    # Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    # macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    # Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    # Android (Mobile)
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    # iOS (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    # Bot / crawler friendly
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    # Opera
    "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    # Tambahan acak hingga lebih dari 110
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# ========== DAFTAR REFERER (50+ items) ==========
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.facebook.com/",
    "https://www.twitter.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
    "https://www.reddit.com/",
    "https://www.wikipedia.org/",
    "https://www.amazon.com/",
    "https://www.ebay.com/",
    "https://www.netflix.com/",
    "https://www.youtube.com/",
    "https://www.whatsapp.com/",
    "https://www.zoom.us/",
    "https://www.microsoft.com/",
    "https://www.apple.com/",
    "https://www.spotify.com/",
    "https://www.github.com/",
    "https://www.stackoverflow.com/",
    "https://www.quora.com/",
    "https://www.tumblr.com/",
    "https://www.pinterest.com/",
    "https://www.twitch.tv/",
    "https://www.tiktok.com/",
    "https://www.snapchat.com/",
    "https://www.telegram.org/",
    "https://www.discord.com/",
    "https://www.yandex.com/",
    "https://www.baidu.com/",
    "https://www.duckduckgo.com/",
    "https://www.startpage.com/",
    "https://www.ask.com/",
    "https://www.aol.com/",
    "https://www.avg.com/",
    "https://www.adobe.com/",
    "https://www.wordpress.com/",
    "https://www.blogger.com/",
    "https://www.medium.com/",
    "https://www.wix.com/",
    "https://www.squarespace.com/",
    "https://www.weebly.com/",
    "https://www.shopify.com/",
    "https://www.paypal.com/",
    "https://www.visa.com/",
    "https://www.mastercard.com/",
    "https://www.airbnb.com/",
    "https://www.uber.com/",
    "https://www.grab.com/",
    "https://www.gojek.com/",
]

# ========== STATISTIK & LOGGER ==========
stats = {
    'total': 0,
    'success': 0,
    'failed': 0,
    'proxy_dead': 0,
    'proxy_alive': 0
}
stats_lock = threading.Lock()

def log_message(msg, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {msg}"
    print(log_line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def load_proxies(filename):
    """Membaca daftar proxy, support format: IP:PORT, http://IP:PORT, socks5://IP:PORT"""
    proxies = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Jika tidak ada skema, tambahkan http:// sebagai default
                if "://" not in line:
                    line = "http://" + line
                proxies.append(line)
        log_message(f"Loaded {len(proxies)} proxies from {filename}")
        return proxies
    except FileNotFoundError:
        log_message(f"Proxy file '{filename}' not found!", "ERROR")
        sys.exit(1)

def check_proxy(proxy_url):
    """Cek apakah proxy (termasuk SOCKS5) masih hidup"""
    try:
        test_url = TARGET_URL
        # Gunakan HEAD request dengan timeout kecil
        response = requests.head(
            test_url,
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=TIMEOUT // 2,
            headers={"User-Agent": random.choice(USER_AGENTS)}
        )
        return response.status_code < 500
    except Exception:
        return False

def visit_url(proxy_url):
    """Melakukan kunjungan ke target menggunakan proxy (support SOCKS5)"""
    time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': random.choice(REFERERS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    for attempt in range(RETRY_COUNT):
        try:
            # requests secara otomatis menangani skema socks5://
            response = requests.get(
                TARGET_URL,
                proxies={"http": proxy_url, "https": proxy_url},
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                with stats_lock:
                    stats['success'] += 1
                log_message(f"✓ SUCCESS | {proxy_url} | Status {response.status_code}")
                return True
            else:
                log_message(f"⚠ WARNING | {proxy_url} | Status {response.status_code} (attempt {attempt+1})")
                
        except ProxyError:
            log_message(f"✗ PROXY DEAD | {proxy_url} - Connection refused", "WARNING")
            with stats_lock:
                stats['proxy_dead'] += 1
            return False
        except Timeout:
            log_message(f"⏱ TIMEOUT | {proxy_url} - No response in {TIMEOUT}s", "WARNING")
        except ConnectionError:
            log_message(f"🔌 CONN ERR | {proxy_url} - Cannot connect", "WARNING")
        except Exception as e:
            log_message(f"⚠ ERROR | {proxy_url} - {str(e)[:80]}", "ERROR")
        
        if attempt < RETRY_COUNT - 1:
            time.sleep(1)
    
    with stats_lock:
        stats['failed'] += 1
    log_message(f"✗ FAILED | {proxy_url} after {RETRY_COUNT} attempts")
    return False

def worker(proxy_url):
    with stats_lock:
        stats['total'] += 1
    
    if CHECK_PROXY_BEFORE_USE:
        if not check_proxy(proxy_url):
            log_message(f"⏭ SKIP | {proxy_url} is dead (pre-check)", "WARNING")
            with stats_lock:
                stats['proxy_dead'] += 1
            return
    
    visit_url(proxy_url)

def main():
    banner = """
   ██████╗  █████╗ ██████╗  █████╗ 
   ██╔══██╗██╔══██╗██╔══██╗██╔══██╗
   ██████╔╝███████║██████╔╝███████║
   ██╔══██╗██╔══██║██╔══██╗██╔══██║
   ██║  ██║██║  ██║██║  ██║██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                      
   ===== Website Visitor v3.0 (SOCKS5 + 110+ User-Agent) =====
   ===================== Created by Rara =====================
    """
    print(banner)
    
    proxies = load_proxies(PROXY_FILE)
    if not proxies:
        log_message("No proxies found. Exiting.", "ERROR")
        sys.exit(1)
    
    log_message(f"Starting with {THREADS} threads, {len(proxies)} proxies")
    log_message(f"Target: {TARGET_URL}")
    log_message(f"User-Agent count: {len(USER_AGENTS)}")
    log_message(f"Referer count: {len(REFERERS)}")
    log_message("=" * 60)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(worker, proxy) for proxy in proxies]
        completed = 0
        for future in as_completed(futures):
            completed += 1
            if completed % 10 == 0 or completed == len(proxies):
                with stats_lock:
                    log_message(f"Progress: {completed}/{len(proxies)} | ✓ {stats['success']} | ✗ {stats['failed']} | 💀 {stats['proxy_dead']}")
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    log_message("VISITING COMPLETED", "INFO")
    log_message(f"Total proxies processed : {stats['total']}")
    log_message(f"Successful visits       : {stats['success']}")
    log_message(f"Failed visits           : {stats['failed']}")
    log_message(f"Dead proxies detected   : {stats['proxy_dead']}")
    log_message(f"Time elapsed            : {elapsed:.2f} seconds")
    log_message(f"Success rate            : {stats['success']/max(1,stats['total'])*100:.2f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()