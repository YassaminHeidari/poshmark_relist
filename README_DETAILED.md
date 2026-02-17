# Poshmark Auto-Relister

Automate the process of relisting your Poshmark items daily to increase visibility and sales. This tool uses browser automation to click through Edit → Next → List for each item in your closet.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

### 2. First Run (Manual)

```bash
# Run the script manually to test
python3 poshmark_relister.py
```

On the first run:
- The browser will open and navigate to Poshmark
- If you're not logged in, you'll have 60 seconds to log in manually
- The script will then automatically relist all your items
- A log file will be created with the results

### 3. Schedule Automatic Runs

The script is configured to run automatically at **9:00 AM** and **4:00 PM** every day (via the shortcut created in your system).

You can also run it manually anytime by executing:
```bash
python3 poshmark_relister.py
```

## ⚙️ Configuration

Edit `config.json` to customize behavior:

```json
{
    "poshmark_url": "https://poshmark.com/closet",
    "max_items": null,                    // null = all items, or set a number
    "delay_between_items": 2,             // seconds between each relist
    "page_load_timeout": 10,              // seconds to wait for pages
    "element_wait_timeout": 5,            // seconds to wait for buttons
    "headless": false,                    // true = invisible, false = show browser
    "chrome_profile": null                // path to Chrome profile (stay logged in)
}
```

### Staying Logged In (Recommended)

To avoid logging in every time, set your Chrome profile path:

**Windows:**
```json
"chrome_profile": "C:/Users/YourName/AppData/Local/Google/Chrome/User Data"
```

**Mac:**
```json
"chrome_profile": "/Users/YourName/Library/Application Support/Google/Chrome"
```

**Linux:**
```json
"chrome_profile": "/home/yourname/.config/google-chrome"
```

⚠️ **Note:** When using a Chrome profile, close all Chrome windows before running the script.

## 📊 Logs

Each run creates a log file: `poshmark_relist_YYYYMMDD.log`

Example log output:
```
2025-02-16 09:00:15 - INFO - Starting Poshmark Auto-Relister
2025-02-16 09:00:18 - INFO - WebDriver initialized successfully
2025-02-16 09:00:20 - INFO - Already logged in!
2025-02-16 09:00:23 - INFO - Found 45 items. Will relist 45 items.
2025-02-16 09:00:25 - INFO - Processing item 1/45
2025-02-16 09:00:27 - INFO - Clicked Edit button
2025-02-16 09:00:29 - INFO - Clicked List button - Item relisted!
...
2025-02-16 09:15:42 - INFO - Successfully relisted: 45
2025-02-16 09:15:42 - INFO - Failed: 0
```

## 🛠️ Advanced Usage

### Running Headless (Invisible Browser)

For scheduled runs where you don't want to see the browser:
```json
"headless": true
```

### Limiting Items Per Session

To relist only the first 20 items:
```json
"max_items": 20
```

### Custom Delays

If Poshmark is rate-limiting you, increase delays:
```json
"delay_between_items": 5
```

## 🐛 Troubleshooting

### "Could not find Edit button"
- Poshmark may have changed their HTML structure
- Check `error_screenshot_*.png` files for visual debugging
- The script may need selector updates

### "Not logged in"
- Set up Chrome profile in config to stay logged in
- Or manually log in during the 60-second wait window

### ChromeDriver Issues
- The script auto-downloads the correct ChromeDriver
- Ensure you have Chrome browser installed
- Update selenium: `pip install --upgrade selenium`

### Items Not Relisting
- Check Poshmark's daily relisting limits
- Verify you have items in your closet
- Review log files for specific errors

## 📦 Creating a Standalone Executable (Optional)

To create a double-click executable that doesn't require Python:

### Windows

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --add-data "config.json;." poshmark_relister.py

# Your .exe will be in the dist/ folder
```

### Mac/Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --add-data "config.json:." poshmark_relister.py

# Your executable will be in the dist/ folder
```

**Note:** When using the executable:
1. Keep `config.json` in the same folder as the executable
2. The executable will be larger (~50-100 MB) but won't require Python
3. Antivirus software may flag it initially (it's safe, just automation)

## 🔒 Privacy & Security

- Your credentials are never stored or transmitted by this script
- The script only interacts with Poshmark through your browser
- All automation happens locally on your computer
- No data is sent to third parties

## 📝 Poshmark Terms of Service

Be aware of Poshmark's terms regarding automation. This tool is designed to automate a repetitive task (relisting) that you would normally do manually. Use responsibly and at your own discretion.

## 🤝 Support

If you encounter issues:
1. Check the log files for error messages
2. Take screenshots of any errors
3. Verify your Python and Chrome versions are up to date
4. Try running manually first before troubleshooting scheduled runs

## 📅 Schedule Details

The shortcut is configured to run automatically:
- **Morning:** 9:00 AM (catch early shoppers)
- **Afternoon:** 4:00 PM (peak browsing time)

This twice-daily schedule maximizes your items' visibility on Poshmark!

---

**Created with:** Python, Selenium WebDriver, Chrome Automation
**Compatible with:** Windows, Mac, Linux
