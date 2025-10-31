#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import re
import sys
import io
import json
from colorama import init, Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Fix UTF-8 encoding for input/output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

init(autoreset=True)

class WhatsAppSender:
    def __init__(self):
        self.phone_number = ""
        self.message = ""
        self.count = 0
        self.mode = 2
        self.driver = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = Fore.CYAN + r"""
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ██████╗ ██╗███████╗ █████╗  █████╗  █████╗ ██████╗        │
│  ██╔══██╗██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗       │
│  ██║  ██║██║  ███╔╝ ███████║███████║███████║██████╔╝       │
│  ██║  ██║██║ ███╔╝  ██╔══██║██╔══██║██╔══██║██╔══██╗       │
│  ██████╔╝██║███████╗██║  ██║██║  ██║██║  ██║██║  ██║       │
│  ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""
        print(banner)

    def setup_browser(self, headless=False):
        options = Options()
        options.add_argument('--user-data-dir=./User_Data')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Ensure UTF-8 encoding in browser
        options.add_argument('--lang=en-US,en')
        options.add_argument('--accept-lang=en-US,en')
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
        })

    def wait_for_login(self):
        print(Fore.CYAN + "\n🔍 Checking WhatsApp login status...")
        print(Fore.YELLOW + "🕒 Waiting for WhatsApp login... (Scan QR Code if required)")
        self.driver.get("https://web.whatsapp.com")
        try:
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='3'], div[title='Search input textbox']"))
            )
            print(Fore.GREEN + "✅ WhatsApp logged in successfully!")
            self.driver.quit()
            return True
        except:
            print(Fore.RED + "❌ Login not detected within 3 minutes.")
            self.driver.quit()
            return False

    def get_user_input(self):
        print(Fore.CYAN + "\n" + "═" * 68)
        print(Fore.WHITE + "           W H A T S A P P   S E N D E R")
        print(Fore.CYAN + "═" * 68 + "\n")
        print(Fore.MAGENTA + "📝 ENTER REQUIRED INFORMATION:\n")

        while True:
            phone_input = input(Fore.WHITE + "📱 Phone number (example: +20123456789): ").strip()
            self.phone_number = self.format_phone(phone_input)
            if self.validate_phone(self.phone_number):
                break
            else:
                print(Fore.RED + "❌ Invalid phone number format!")

        self.message = input(Fore.WHITE + "💬 Message: ").strip()

        print(Fore.YELLOW + "\n🔘 Choose sending mode:")
        print(Fore.WHITE + "   1️⃣  Send one message containing multiple lines")
        print(Fore.WHITE + "   2️⃣  Send multiple separate messages")

        while True:
            choice = input(Fore.CYAN + "👉 Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                self.mode = int(choice)
                break
            else:
                print(Fore.RED + "❌ Invalid choice! Please enter 1 or 2")

        while True:
            try:
                self.count = int(input(Fore.WHITE + "🔢 Number of messages/lines: ").strip())
                if self.count > 0:
                    break
                print(Fore.RED + "❌ Number must be greater than zero!")
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid number!")

        if self.mode == 1:
            self.message = "\n".join([self.message for _ in range(self.count)])
            self.count = 1

    def format_phone(self, phone):
        phone = re.sub(r'[^\d+]', '', phone)
        if not phone.startswith('+'):
            if phone.startswith('0'):
                phone = '+20' + phone[1:]
            elif len(phone) == 10:
                phone = '+20' + phone
            elif len(phone) == 11 and phone.startswith('20'):
                phone = '+' + phone
            else:
                phone = '+' + phone
        return phone

    def validate_phone(self, phone):
        return re.match(r'^\+\d{10,15}$', phone)

    def open_chat(self):
        print(Fore.BLUE + f"👤 Opening chat with: {self.phone_number}")
        try:
            chat_url = f"https://web.whatsapp.com/send?phone={self.phone_number[1:]}"
            self.driver.get(chat_url)
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='10'], div[data-tab='6']"))
            )
            print(Fore.GREEN + "✅ Chat opened successfully")
            return True
        except:
            print(Fore.RED + "❌ Failed to open chat")
            return False

    def send_messages(self):
        print(Fore.BLUE + f"\n🚀 Starting to send {self.count} message(s)...")
        print(Fore.WHITE + "⏰ Each message will be typed and sent individually")
        print(Fore.WHITE + "⏳ Delay: 100ms between messages\n")

        # Escape the message for JavaScript - this is the key fix
        escaped_message = json.dumps(self.message, ensure_ascii=False)[1:-1]
        
        js_code = f"""
        const message = `{escaped_message}`;
        const times = {self.count};
        const delay = 100;
        const inputBox = document.querySelector('[contenteditable="true"][data-tab="10"], [contenteditable="true"][data-tab="6"]');
        if (!inputBox) return 0;
        const sendButtonSelector = () => 
            document.querySelector('button span[data-icon="send"]')?.closest("button") ||
            document.querySelector('div[aria-label="Send"][role="button"]') ||
            document.querySelector('button[aria-label="Send"]');
        const delayMs = ms => new Promise(r => setTimeout(r, ms));
        let successCount = 0;
        const sendAll = async () => {{
            for (let i = 0; i < times; i++) {{
                inputBox.focus();
                inputBox.innerHTML = '';
                const lines = message.split('\\n');
                for (const [index, line] of lines.entries()) {{
                    document.execCommand("insertText", false, line);
                    if (index < lines.length - 1) {{
                        const shiftEnterEvent = new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', shiftKey: true, bubbles: true }});
                        inputBox.dispatchEvent(shiftEnterEvent);
                    }}
                }}
                await delayMs(50);
                const sendButton = sendButtonSelector();
                if (sendButton) {{
                    ["mousedown", "mouseup", "click"].forEach(evt =>
                        sendButton.dispatchEvent(new MouseEvent(evt, {{ bubbles: true, cancelable: true }}))
                    );
                    successCount++;
                    console.log(`✅ Message ${{i+1}} sent successfully!`);
                }} else {{
                    console.log(`❌ Failed to send message ${{i+1}}`);
                }}
                await delayMs(delay);
            }}
            return successCount;
        }};
        return sendAll();
        """

        self.driver.set_script_timeout(600)
        try:
            result = self.driver.execute_script(js_code)
            print(Fore.GREEN + f"\n🎉 Successfully sent {result} message(s)!\n")
            print(Fore.YELLOW + "💡 Browser will stay open. Press Ctrl+C to stop manually.\n")
            while True:
                time.sleep(1)
        except Exception as e:
            print(Fore.RED + f"\n💥 Process completed with errors: {e}")
            while True:
                time.sleep(1)

    def run(self):
        self.clear_screen()
        self.print_banner()
        self.setup_browser(headless=False)
        if not self.wait_for_login():
            return
        self.get_user_input()
        print(Fore.CYAN + "\n📋 SENDING SUMMARY:")
        print(Fore.WHITE + f"   📱 Phone: {self.phone_number}")
        print(Fore.WHITE + f"   💬 Message: {self.message[:50]}{'...' if len(self.message) > 50 else ''}")
        print(Fore.WHITE + f"   🔢 Count: {self.count}")

        while True:
            confirm = input(Fore.YELLOW + "\n🎯 Start sending? (y/n): ").strip().lower()
            if confirm in ['y', 'n']:
                break
            print(Fore.RED + "❌ Invalid input! Please enter only 'y' or 'n'.")

        if confirm == 'y':
            self.setup_browser(headless=True)
            if self.open_chat():
                self.send_messages()
        else:
            print(Fore.RED + "\n❌ Operation cancelled")

if __name__ == "__main__":
    try:
        app = WhatsAppSender()
        app.run()
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Script stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {e}")
        sys.exit(1)
