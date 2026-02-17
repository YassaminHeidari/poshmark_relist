#!/usr/bin/env python3
"""
Poshmark Auto-Relister
Automates the process of relisting items on Poshmark by clicking Edit -> Next -> List
"""

import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'poshmark_relist_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

class PoshmarkRelister:
    def __init__(self, config_path='config.json'):
        """Initialize the Poshmark relister with configuration"""
        self.config = self.load_config(config_path)
        self.driver = None
        self.items_relisted = 0
        self.items_failed = 0

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "poshmark_url": "https://poshmark.com/closet",
                "poshmark_username": "",  # Your Poshmark username or email
                "poshmark_password": "",  # Your Poshmark password
                "max_items": None,  # None means all items
                "delay_between_items": 2,  # seconds
                "page_load_timeout": 10,
                "element_wait_timeout": 5,
                "headless": False,  # Set to True to run without opening browser window
                "chrome_profile": None  # Path to Chrome profile to stay logged in
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            logging.info(f"Created default config file: {config_path}")
            return default_config

    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()

        if self.config.get('headless', False):
            options.add_argument('--headless')

        # Use existing Chrome profile to stay logged in
        if self.config.get('chrome_profile'):
            options.add_argument(f"user-data-dir={self.config['chrome_profile']}")

        # Additional options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(self.config['page_load_timeout'])
        logging.info("WebDriver initialized successfully")

    def wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be present and clickable"""
        if timeout is None:
            timeout = self.config['element_wait_timeout']
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logging.warning(f"Timeout waiting for element: {value}")
            return None

    def automated_login(self):
        """Automatically log in using credentials from config"""
        logging.info("Checking login status...")
        self.driver.get("https://poshmark.com/login")
        time.sleep(3)

        # Check if we're already logged in
        current_url = self.driver.current_url
        if 'login' not in current_url.lower():
            logging.info("Already logged in!")
            return True

        # Get credentials from config
        username = self.config.get('poshmark_username', '')
        password = self.config.get('poshmark_password', '')

        if not username or not password:
            logging.error("No username/password found in config.json!")
            logging.info("Please add your credentials to config.json:")
            logging.info('  "poshmark_username": "your_email@example.com",')
            logging.info('  "poshmark_password": "your_password"')
            return False

        logging.info("Attempting automatic login...")

        try:
            # Find and fill username field
            username_selectors = [
                "input[name='login_form[username_email]']",
                "input[type='email']",
                "input[name='username']",
                "input[id='login_form_username_email']",
                "//input[@type='email' or @type='text']"
            ]

            username_field = None
            for selector in username_selectors:
                try:
                    if selector.startswith('//'):
                        username_field = self.driver.find_element(By.XPATH, selector)
                    else:
                        username_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if username_field:
                        break
                except:
                    continue

            if not username_field:
                logging.error("Could not find username field")
                self.driver.save_screenshot(f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False

            username_field.clear()
            username_field.send_keys(username)
            logging.info("Entered username")
            time.sleep(1)

            # Find and fill password field
            password_selectors = [
                "input[name='login_form[password]']",
                "input[type='password']",
                "input[name='password']",
                "input[id='login_form_password']"
            ]

            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if password_field:
                        break
                except:
                    continue

            if not password_field:
                logging.error("Could not find password field")
                self.driver.save_screenshot(f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False

            password_field.clear()
            password_field.send_keys(password)
            logging.info("Entered password")
            time.sleep(1)

            # Find and click login button
            login_button_selectors = [
                "button[type='submit']",
                "button[data-test='login-btn']",
                "input[type='submit']",
                "//button[contains(text(), 'Log In')]",
                "//button[contains(text(), 'Sign In')]"
            ]

            login_button = None
            for selector in login_button_selectors:
                try:
                    if selector.startswith('//'):
                        login_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if login_button:
                        break
                except:
                    continue

            if not login_button:
                logging.error("Could not find login button")
                self.driver.save_screenshot(f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False

            login_button.click()
            logging.info("Clicked login button")
            time.sleep(5)  # Wait for login to complete

            # Check if login was successful
            current_url = self.driver.current_url
            if 'login' in current_url.lower():
                logging.error("Login failed - still on login page")
                logging.error("Please check your username and password in config.json")
                self.driver.save_screenshot(f"login_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False

            logging.info("✅ Login successful!")
            return True

        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            self.driver.save_screenshot(f"login_exception_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False

    def get_closet_items(self):
        """Navigate to closet and get all items available for relisting"""
        logging.info("Navigating to your closet...")
        self.driver.get(self.config['poshmark_url'])
        time.sleep(3)

        # Find all listing items
        # Note: These selectors may need to be updated based on Poshmark's current HTML structure
        # Common selectors to try:
        selectors = [
            "div.tile",
            "div.card",
            "div.listing-item",
            "a[data-test='tile']",
            "div[data-test='closet-item']"
        ]

        items = []
        for selector in selectors:
            try:
                items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    logging.info(f"Found {len(items)} items using selector: {selector}")
                    break
            except NoSuchElementException:
                continue

        if not items:
            logging.error("Could not find any items in closet. Page structure may have changed.")
            logging.info("Current URL: " + self.driver.current_url)
            # Take screenshot for debugging
            self.driver.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

        return items

    def relist_item(self, item):
        """Relist a single item by clicking Edit -> Next -> List"""
        try:
            # Click on the item to open it
            item.click()
            time.sleep(2)

            # Click Edit button
            # Try multiple possible selectors
            edit_selectors = [
                "button:contains('Edit')",
                "a:contains('Edit')",
                "button[data-test*='edit']",
                "a[data-test*='edit']",
                "//button[contains(text(), 'Edit')]",
                "//a[contains(text(), 'Edit')]"
            ]

            edit_button = None
            for selector in edit_selectors:
                try:
                    if selector.startswith('//'):
                        edit_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        edit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if edit_button:
                        break
                except:
                    continue

            if not edit_button:
                logging.warning("Could not find Edit button")
                return False

            edit_button.click()
            logging.info("Clicked Edit button")
            time.sleep(2)

            # Click Next button (if it exists)
            try:
                next_selectors = [
                    "button:contains('Next')",
                    "button[data-test*='next']",
                    "//button[contains(text(), 'Next')]"
                ]

                for selector in next_selectors:
                    try:
                        if selector.startswith('//'):
                            next_button = self.driver.find_element(By.XPATH, selector)
                        else:
                            next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if next_button:
                            next_button.click()
                            logging.info("Clicked Next button")
                            time.sleep(2)
                            break
                    except:
                        continue
            except:
                logging.info("No Next button found, proceeding to List")

            # Click List button
            list_selectors = [
                "button:contains('List')",
                "button[data-test*='list']",
                "button[type='submit']",
                "//button[contains(text(), 'List')]",
                "//button[contains(text(), 'Publish')]"
            ]

            list_button = None
            for selector in list_selectors:
                try:
                    if selector.startswith('//'):
                        list_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        list_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if list_button:
                        break
                except:
                    continue

            if not list_button:
                logging.warning("Could not find List button")
                return False

            list_button.click()
            logging.info("Clicked List button - Item relisted!")
            time.sleep(2)

            return True

        except Exception as e:
            logging.error(f"Error relisting item: {str(e)}")
            return False

    def run(self):
        """Main execution function"""
        logging.info("=" * 50)
        logging.info("Starting Poshmark Auto-Relister")
        logging.info("=" * 50)

        try:
            # Setup browser
            self.setup_driver()

            # Automated login
            if not self.automated_login():
                logging.error("Login failed! Cannot proceed.")
                return

            # Get items from closet
            items = self.get_closet_items()

            if not items:
                logging.error("No items found to relist!")
                return

            # Determine how many items to relist
            max_items = self.config.get('max_items')
            items_to_process = items if max_items is None else items[:max_items]

            logging.info(f"Found {len(items)} items. Will relist {len(items_to_process)} items.")

            # Relist each item
            for idx, item in enumerate(items_to_process, 1):
                logging.info(f"\n--- Processing item {idx}/{len(items_to_process)} ---")

                success = self.relist_item(item)

                if success:
                    self.items_relisted += 1
                else:
                    self.items_failed += 1

                # Delay between items
                if idx < len(items_to_process):
                    delay = self.config['delay_between_items']
                    logging.info(f"Waiting {delay} seconds before next item...")
                    time.sleep(delay)

                # Navigate back to closet
                self.driver.get(self.config['poshmark_url'])
                time.sleep(2)

            # Summary
            logging.info("=" * 50)
            logging.info("Relisting Complete!")
            logging.info(f"Successfully relisted: {self.items_relisted}")
            logging.info(f"Failed: {self.items_failed}")
            logging.info("=" * 50)

        except Exception as e:
            logging.error(f"Fatal error: {str(e)}")
            raise
        finally:
            if self.driver:
                logging.info("Closing browser...")
                time.sleep(3)
                self.driver.quit()

def main():
    """Entry point for the script"""
    relister = PoshmarkRelister()
    relister.run()

if __name__ == "__main__":
    main()
