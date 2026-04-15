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
import glob
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
                "chrome_profile": None,  # Path to Chrome profile to stay logged in
                "restart_every": 15  # Restart browser every N items to prevent memory crashes
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

        # Use a dedicated Chrome profile for automation (separate from your main Chrome).
        # Sharing your main profile with an already-running Chrome causes an instant crash.
        chrome_profile = self.config.get('chrome_profile')
        main_profile = os.path.expanduser('~/Library/Application Support/Google/Chrome')
        auto_profile = os.path.expanduser('~/Library/Application Support/Google/ChromeAutomation')

        if chrome_profile and os.path.normpath(chrome_profile) == os.path.normpath(main_profile):
            logging.warning(
                "chrome_profile points to your main Chrome profile — switching to a "
                "dedicated automation profile to avoid conflicts with running Chrome."
            )
            chrome_profile = auto_profile

        if not chrome_profile:
            chrome_profile = auto_profile

        os.makedirs(chrome_profile, exist_ok=True)
        options.add_argument(f'--user-data-dir={chrome_profile}')
        options.add_argument('--profile-directory=Default')
        logging.info(f"Using Chrome profile: {chrome_profile}")

        # Additional options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Auto-detect ChromeDriver — picks the highest cached version automatically
        chromedriver_path = self.config.get('chromedriver_path')
        if not chromedriver_path:
            pattern = os.path.expanduser(
                '~/.wdm/drivers/chromedriver/mac64/*/chromedriver-mac-x64/chromedriver'
            )
            matches = sorted(glob.glob(pattern))
            if matches:
                chromedriver_path = matches[-1]
                os.system(f'xattr -d com.apple.quarantine "{chromedriver_path}" 2>/dev/null')
                logging.info(f"Using ChromeDriver: {chromedriver_path}")
            else:
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    chromedriver_path = ChromeDriverManager().install()
                    logging.info(f"Downloaded ChromeDriver: {chromedriver_path}")
                except Exception as e:
                    raise RuntimeError(f"ChromeDriver not found. Run: pip install --upgrade webdriver-manager. Error: {e}")
        service = Service(chromedriver_path)
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
            time.sleep(5)  # Wait for login / 2FA page to load

            # Poll until we leave the login flow, waiting up to 120s for manual 2FA entry
            login_keywords = ['login', 'signin', 'sign-in', 'security', 'verify',
                              'verification', 'challenge', 'confirm', 'two-factor', 'captcha']
            max_wait = 120
            waited = 0
            interval = 3
            notified = False

            while waited < max_wait:
                current_url = self.driver.current_url.lower()
                logging.info(f"Current URL: {current_url}")

                # Success — navigated to feed or closet (even with ?login=true query param)
                if '/feed' in current_url or '/closet' in current_url:
                    break
                # Success — navigated away from all login/verification pages
                if not any(k in current_url for k in login_keywords):
                    break

                if not notified:
                    logging.info("⏳ Still in login/verification flow.")
                    logging.info("   If a security code was texted to you, enter it in the browser now.")
                    logging.info(f"   Waiting up to {max_wait} seconds...")
                    notified = True

                time.sleep(interval)
                waited += interval
            else:
                logging.error(f"Login timed out after {max_wait}s. Final URL: {self.driver.current_url}")
                self.driver.save_screenshot(f"login_timeout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False

            logging.info(f"✅ Login successful! Landed on: {self.driver.current_url}")
            return True

        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            self.driver.save_screenshot(f"login_exception_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return False

    def get_closet_items(self):
        """Navigate to closet and get all items available for relisting"""
        logging.info("Navigating to your closet...")

        # Auto-detect the correct closet URL (format: /closet/<username>)
        closet_url = self.config.get('poshmark_url', 'https://poshmark.com/closet')
        if closet_url.rstrip('/') == 'https://poshmark.com/closet':
            try:
                self.driver.get('https://poshmark.com/feed')
                time.sleep(3)
                profile_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/closet/']")
                for link in profile_links:
                    href = link.get_attribute('href') or ''
                    if '/closet/' in href:
                        slug = href.split('/closet/')[-1].rstrip('/')
                        if slug:
                            closet_url = f"https://poshmark.com/closet/{slug}"
                            logging.info(f"Auto-detected closet URL: {closet_url}")
                            break
            except Exception as e:
                logging.warning(f"Could not auto-detect closet URL: {e}")

        self.closet_url = closet_url
        self.driver.get(closet_url)
        time.sleep(4)
        logging.info(f"Closet page URL: {self.driver.current_url}")

        # Wait up to 10s for items to initially appear before trying selectors
        import time as _time
        for _ in range(10):
            for sel in ["div.tile", "[data-et-element-type='listing']", "a[href*='/listing/']"]:
                if self.driver.find_elements(By.CSS_SELECTOR, sel):
                    break
            else:
                _time.sleep(1)
                continue
            break

        # Try multiple selectors to find the right one for current Poshmark version
        tile_selectors = [
            "div.tile",
            "[data-et-element-type='listing']",
            "div[class*='listing-card']",
            "div[class*='tile']",
            "li[class*='listing']",
            "a[href*='/listing/']",
        ]

        tile_selector = None
        logging.info("Detecting item selector...")
        for sel in tile_selectors:
            found = self.driver.find_elements(By.CSS_SELECTOR, sel)
            if found:
                tile_selector = sel
                logging.info(f"Using selector: {tile_selector!r} (found {len(found)} initially)")
                break

        if not tile_selector:
            logging.error("Could not detect item selector — saving page source for inspection")
            with open('closet_page_dump.html', 'w') as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            return []

        # Scroll down to load ALL items (Poshmark uses infinite scroll)
        logging.info("Scrolling to load all closet items...")
        last_count = 0
        no_change_rounds = 0
        while no_change_rounds < 3:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            current_count = len(self.driver.find_elements(By.CSS_SELECTOR, tile_selector))
            if current_count == last_count:
                no_change_rounds += 1
            else:
                no_change_rounds = 0
                logging.info(f"Loaded {current_count} items so far...")
            last_count = current_count

        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Store tile_selector for use in get_listing_urls
        self._tile_selector = tile_selector
        items = self.driver.find_elements(By.CSS_SELECTOR, tile_selector)
        logging.info(f"Found {len(items)} total items after full scroll")

        if not items:
            logging.error("Could not find any items in closet.")
            with open('closet_page_dump.html', 'w') as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

        return items

    def click_element(self, element):
        """Click an element, scrolling it into view first and falling back to JS click"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def find_button_by_text(self, *texts, timeout=5):
        """Find a button or link by text — tries exact match then partial match"""
        xpath_exact = " | ".join(
            f"//button[normalize-space()='{t}'] | //a[normalize-space()='{t}']"
            for t in texts
        )
        xpath_partial = " | ".join(
            f"//button[contains(., '{t}')] | //a[contains(., '{t}')]"
            for t in texts
        )
        for xpath in [xpath_exact, xpath_partial]:
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            except Exception:
                continue
        return None

    def get_listing_urls(self):
        """Scrape all available (non-sold) listing URLs, deduplicating across scroll loads"""
        seen = set()
        urls = []
        skipped_sold = 0
        tile_selector = getattr(self, '_tile_selector', 'div.tile')
        tiles = self.driver.find_elements(By.CSS_SELECTOR, tile_selector)
        for tile in tiles:
            try:
                # Skip sold, sold-out, or not-for-sale items
                tile_html = tile.get_attribute('innerHTML') or ''
                if any(cls in tile_html for cls in ['sold-tag', 'sold-out-tag', 'not-for-sale-tag']):
                    skipped_sold += 1
                    continue

                anchor = tile.find_element(By.CSS_SELECTOR, "a[href*='/listing/']")
                href = anchor.get_attribute('href')
                if href:
                    clean = href.split('?')[0]
                    if clean not in seen:
                        seen.add(clean)
                        urls.append(clean)
            except Exception:
                continue
        logging.info(f"Collected {len(urls)} available listings (skipped {skipped_sold} sold items)")
        return urls

    def wait_for_page_load(self, marker_text, timeout=15):
        """Wait until a specific text appears anywhere on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: marker_text.lower() in d.page_source.lower()
            )
            return True
        except Exception:
            return False

    def scroll_and_dump_buttons(self, label=""):
        """Scroll through the full page and collect all button/link texts"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        last_height = 0
        for _ in range(10):
            self.driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(0.5)
            new_height = self.driver.execute_script("return window.scrollY")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        all_btns = self.driver.find_elements(By.XPATH, "//button | //a[@href]")
        btn_texts = [b.text.strip() for b in all_btns if b.text.strip()]
        if label:
            logging.info(f"Buttons [{label}]: {btn_texts[:40]}")
        return btn_texts

    def get_draft_urls(self):
        """Get all draft listing URLs from /drafts page"""
        self.driver.get("https://poshmark.com/drafts")
        self.wait_for_page_load("draft", timeout=10)
        time.sleep(3)
        anchors = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/edit-listing/']")
        urls = list(dict.fromkeys([  # dedupe while preserving order
            a.get_attribute('href').split('?')[0]
            for a in anchors if a.get_attribute('href')
        ]))
        logging.info(f"Found {len(urls)} drafts: {urls[:5]}")
        return urls

    def publish_listing(self, new_edit_url, original_listing_id, original_edit_url):
        """Navigate to a listing draft, clean title, publish it, then delete original"""
        self.wait_for_page_load("Update", timeout=15)
        time.sleep(3)

        # Clean "Copy of" from title
        try:
            title_field = WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located((By.XPATH,
                    "//input[contains(@placeholder,'title') or contains(@placeholder,'Title') or contains(@name,'title')] | //textarea[contains(@placeholder,'title') or contains(@name,'title')]"
                ))
            )
            current_title = title_field.get_attribute('value') or ''
            logging.info(f"Draft title: {current_title!r}")
            for prefix in ['Copy of ', 'copy of ', 'COPY OF ']:
                if current_title.startswith(prefix):
                    new_title = current_title[len(prefix):]
                    self.driver.execute_script("arguments[0].value = '';", title_field)
                    title_field.send_keys(new_title)
                    logging.info(f"Cleaned title to: {new_title!r}")
                    break
        except Exception as e:
            logging.warning(f"Could not clean title: {e}")

        # Click Next through steps
        for step in range(5):
            next_btn = self.find_button_by_text("Next", "NEXT", timeout=3)
            if not next_btn:
                break
            self.click_element(next_btn)
            logging.info(f"Clicked Next (step {step + 1})")
            time.sleep(2)

        # Click List to publish
        list_btn = self.find_button_by_text("List", "Publish", "LIST", "PUBLISH", timeout=8)
        if not list_btn:
            btn_texts = self.scroll_and_dump_buttons("before List click")
            logging.warning(f"No List button. Buttons: {btn_texts[:30]}")
            return False
        self.click_element(list_btn)
        logging.info("✅ New listing published!")
        time.sleep(3)

        # Delete original
        logging.info(f"Deleting original: {original_edit_url}")
        self.driver.get(original_edit_url)
        self.wait_for_page_load("Delete", timeout=10)
        time.sleep(2)

        delete_btn = None
        for xpath in [
            "//a[.//h4[contains(text(),'Delete Listing')]]",
            "//a[@data-et-name='delete']",
            "//h4[contains(text(),'Delete Listing')]/..",
        ]:
            try:
                delete_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                if delete_btn:
                    break
            except Exception:
                continue

        if delete_btn:
            self.click_element(delete_btn)
            time.sleep(2)
            yes_btn = self.find_button_by_text("Yes", "YES", timeout=6)
            if not yes_btn:
                try:
                    yes_btn = self.driver.find_element(
                        By.XPATH, "//*[self::button or self::a][normalize-space(text())='Yes']"
                    )
                except Exception:
                    pass
            if yes_btn:
                self.click_element(yes_btn)
                logging.info("Original deleted ✅")
                time.sleep(3)
        else:
            logging.warning("No Delete button found on original")

        return True

    def relist_item(self, listing_url):
        """
        Relist flow (confirmed working):
          1. Go to edit page -> Update -> Copy Listing
          2. Click Yes (btn--tertiary) on copy tooltip
          3. Click List This Item — this publishes the copy and replaces the original in-place
             No separate delete needed: count stays the same, but listing date is refreshed.
        """
        try:
            logging.info(f"Relisting: {listing_url}")
            listing_id = listing_url.rstrip('/').split('-')[-1]
            edit_url = f"https://poshmark.com/edit-listing/{listing_id}"

            # Step 1: Open edit page
            self.driver.get(edit_url)
            self.wait_for_page_load("Update", timeout=20)
            time.sleep(4)

            # Click Update to clear Vue dirty state
            update_btn = self.find_button_by_text("Update", timeout=6)
            if update_btn:
                self.click_element(update_btn)
                logging.info("Clicked Update")
                time.sleep(3)

            # Step 2: Click Copy Listing
            copy_btn = None
            for xpath in [
                "//a[.//h4[contains(text(),'Copy Listing')]]",
                "//a[@data-et-name='copy_listing']",
            ]:
                try:
                    copy_btn = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    if copy_btn:
                        break
                except Exception:
                    continue

            if not copy_btn:
                logging.warning("No Copy Listing button found")
                return False

            self.click_element(copy_btn)
            logging.info("Clicked Copy Listing")
            time.sleep(3)

            # Step 3: Click Yes on copy tooltip (btn--tertiary)
            yes_btn = None
            for xpath in [
                "//button[contains(@class,'btn--tertiary') and normalize-space(text())='Yes']",
                "//button[normalize-space(text())='Yes']",
            ]:
                try:
                    yes_btn = self.driver.find_element(By.XPATH, xpath)
                    if yes_btn:
                        logging.info(f"Found Yes via: {xpath}")
                        break
                except Exception:
                    continue

            if not yes_btn:
                logging.warning("No Yes button on copy confirmation")
                return False
            self.driver.execute_script("arguments[0].click();", yes_btn)
            logging.info("Clicked Yes on copy confirmation")
            time.sleep(6)

            # Step 4: Click Next if present, then List This Item
            next_btn = self.find_button_by_text("Next", "NEXT", timeout=5)
            if next_btn:
                self.click_element(next_btn)
                logging.info("Clicked Next")
                time.sleep(3)

            list_btn = self.find_button_by_text("List This Item", "List this item", timeout=15)
            if not list_btn:
                logging.warning("No List This Item button found")
                return False
            self.click_element(list_btn)
            logging.info("Clicked List This Item")
            time.sleep(5)

            # Verify: URL should return to the listing page (not an error page)
            final_url = self.driver.current_url
            if 'listing' in final_url or 'closet' in final_url or 'feed' in final_url:
                logging.info(f"✅ Item relisted successfully! URL: {final_url}")
                return True
            else:
                logging.warning(f"Unexpected URL after List This Item: {final_url}")
                return False

        except Exception as e:
            logging.error(f"Error relisting item: {str(e)}")
            return False

    def run(self):
        """Main execution function"""
        logging.info("=" * 50)
        logging.info("Starting Poshmark Auto-Relister")
        logging.info("=" * 50)

        try:
            self.setup_driver()

            if not self.automated_login():
                logging.error("Login failed! Cannot proceed.")
                return

            self.get_closet_items()
            listing_urls = self.get_listing_urls()

            if not listing_urls:
                logging.error("No items found to relist!")
                return

            max_items = self.config.get('max_items')
            if max_items is not None:
                max_items = int(max_items)
            urls_to_process = listing_urls if max_items is None else listing_urls[:max_items]
            logging.info(f"Found {len(listing_urls)} items. Will relist {len(urls_to_process)} items.")

            # Restart browser every 15 items to prevent Chrome tab crashes from memory exhaustion
            restart_every = self.config.get('restart_every', 15)

            for idx, url in enumerate(urls_to_process, 1):
                logging.info(f"\n--- Processing item {idx}/{len(urls_to_process)} ---")

                # Periodic browser restart to clear memory
                if idx > 1 and (idx - 1) % restart_every == 0:
                    logging.info(f"Restarting browser to clear memory (every {restart_every} items)...")
                    try:
                        self.driver.quit()
                    except Exception:
                        pass
                    time.sleep(3)
                    self.setup_driver()
                    self.automated_login()
                    logging.info("Browser restarted successfully")

                success = self.relist_item(url)

                if success:
                    self.items_relisted += 1
                else:
                    self.items_failed += 1

                if idx < len(urls_to_process):
                    delay = self.config['delay_between_items']
                    logging.info(f"Waiting {delay} seconds before next item...")
                    time.sleep(delay)

                # Navigate back to closet with retry on timeout
                for attempt in range(3):
                    try:
                        self.driver.get(self.closet_url)
                        time.sleep(2)
                        break
                    except Exception as nav_err:
                        logging.warning(f"Navigation to closet failed (attempt {attempt+1}): {nav_err}")
                        time.sleep(3)
                        if attempt == 2:
                            # Last resort: restart browser and try again
                            logging.warning("Restarting browser after navigation failure...")
                            try:
                                self.driver.quit()
                            except Exception:
                                pass
                            time.sleep(3)
                            self.setup_driver()
                            self.automated_login()
                            self.driver.get(self.closet_url)
                            time.sleep(2)

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