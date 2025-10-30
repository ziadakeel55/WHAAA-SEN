#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import re
import sys
from datetime import datetime
from colorama import init, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

init(autoreset=True)

class WhatsAppSender:
    def __init__(self):
        self.phone_number = ""
        self.message = ""
        self.count = 0
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
        if headless:
            print(Fore.CYAN + "\n🚀 Starting sending process in headless mode...")
        else:
            print(Fore.CYAN + "\n🔍 Checking WhatsApp login status...")
        try:
            options = Options()
            options.add_argument('--user-data-dir=./User_Data')
            options.add_argument('--profile-directory=Default')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            if headless:
                options.add_argument('--headless=new')
                options.add_argument('--window-size=1920,1080')
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
            })
            return True
        except Exception as e:
            print(Fore.RED + f"❌ Error starting browser: {e}")
            return False

    def check_login(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='3'], div[title='Search input textbox']"))
            )
            print(Fore.GREEN + "✅ WhatsApp is logged in and ready")
            self.driver.quit()
            return True
        except:
            print(Fore.RED + "❌ Cannot proceed without WhatsApp login")
            try:
                self.driver.quit()
            except:
                pass
            return False

    def get_user_input(self):
        print(Fore.CYAN + "\n" + "═" * 68)
        print(Fore.WHITE + "           W H A T S A P P   S E N D E R")
        print(Fore.CYAN + "═" * 68 + "\n")
        print(Fore.CYAN + "──────────────────────────────────────────────────────────────")
        print(Fore.MAGENTA + "📝 ENTER REQUIRED INFORMATION:")
        print(Fore.CYAN + "──────────────────────────────────────────────────────────────\n")
        while True:
            phone_input = input(Fore.WHITE + "📱 Phone number (example: +20123456789): ").strip()
            self.phone_number = self.format_phone(phone_input)
            if self.validate_phone(self.phone_number):
                break
            else:
                print(Fore.RED + "❌ Invalid phone number format!")
        self.message = input(Fore.WHITE + "💬 Message: ").strip()
        while True:
            try:
                self.count = int(input(Fore.WHITE + "🔢 Number of messages: ").strip())
                if self.count > 0:
                    break
                print(Fore.RED + "❌ Number must be greater than zero!")
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid number!")

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
        print(Fore.BLUE + f"\n🚀 Starting to send {self.count} messages...")
        print(Fore.WHITE + f"⏰ Each message will be typed and sent individually")
        print(Fore.WHITE + f"⏳ Delay: 100ms between messages\n")

        for i in range(1, self.count + 1):
            try:
                print(Fore.CYAN + f"📤 Sending message {i}...")
                js_code = f"""
                const inputBox = document.querySelector('[contenteditable="true"][data-tab="10"], [contenteditable="true"][data-tab="6"]');
                const sendButtonSelector = () => 
                    document.querySelector('button span[data-icon="send"]')?.closest("button") ||
                    document.querySelector('div[aria-label="Send"][role="button"]') ||
                    document.querySelector('button[aria-label="Send"]');
                if (inputBox) {{
                    inputBox.focus();
                    inputBox.innerHTML = '';
                    document.execCommand("insertText", false, "{self.message.replace('"', '\\"')}");
                    const sendButton = sendButtonSelector();
                    if (sendButton) {{
                        ["mousedown", "mouseup", "click"].forEach(evt =>
                            sendButton.dispatchEvent(new MouseEvent(evt, {{ bubbles: true, cancelable: true }}))
                        );
                        return true;
                    }}
                }}
                return false;
                """
                result = self.driver.execute_script(js_code)
                if result:
                    print(Fore.GREEN + f"✅ Message {i} sent successfully!")
                else:
                    print(Fore.RED + f"❌ Failed to send message {i}")
                time.sleep(0.1)
            except Exception as e:
                print(Fore.RED + f"💥 Error sending message {i}: {e}")

        print(Fore.GREEN + f"\n🎉 Successfully sent {self.count} messages!\n")
        print(Fore.YELLOW + "💡 Browser will remain open (headless) for 5 seconds...")
        time.sleep(5)
        self.driver.quit()
        print(Fore.GREEN + "🔒 Headless browser closed.\n")
        print(Fore.GREEN + "✨ Process completed successfully!\n")

    def run(self):
        self.clear_screen()
        self.print_banner()
        if not self.setup_browser(headless=False):
            return
        if not self.check_login():
            return
        self.get_user_input()
        print(Fore.CYAN + "\n" + "═" * 68)
        print(Fore.WHITE + "📋 SENDING SUMMARY:")
        print(Fore.CYAN + "═" * 68)
        print(Fore.WHITE + f"   📱 Phone: {self.phone_number}")
        print(Fore.WHITE + f"   💬 Message: {self.message}")
        print(Fore.WHITE + f"   🔢 Count: {self.count}")
        print(Fore.CYAN + "═" * 68)
        confirm = input(Fore.YELLOW + "\n🎯 Start sending? (y/n): ").strip().lower()
        if confirm == 'y':
            if not self.setup_browser(headless=True):
                print(Fore.RED + "❌ Failed to start headless browser")
                return
            if self.open_chat():
                self.send_messages()
        else:
            print(Fore.RED + "\n❌ Operation cancelled")

if __name__ == "__main__":
    try:
        app = WhatsAppSender()
        app.run()
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Program stopped by user")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {e}")
        sys.exit(1)
