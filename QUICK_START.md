# 🚀 Poshmark Auto-Relister - Quick Start

## What You've Got

A complete automation system to relist your Poshmark items daily! This package includes:

✅ **Python automation script** - Does the actual relisting
✅ **Configuration file** - Customize settings
✅ **Automatic scheduling** - Runs at 9 AM and 4 PM daily
✅ **Manual run scripts** - Run anytime with a click
✅ **Full documentation** - Everything you need to know

---

## 🎯 Installation (5 minutes)

### Step 1: Install Python

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- ✅ Check "Add Python to PATH" during installation

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt install python3 python3-pip
```

### Step 2: Install Dependencies

Open terminal/command prompt in this folder and run:

**Windows:**
```bash
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

### Step 3: Test Run

**Windows:** Double-click `run_poshmark.bat`
**Mac/Linux:** Double-click `run_poshmark.sh` (or run `./run_poshmark.sh`)

OR run directly:
```bash
python3 poshmark_relister.py
```

**First Time:**
- Browser will open
- If not logged in, you have 60 seconds to log into Poshmark
- Script will then automatically relist all items
- Check the log file for results!

---

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
    "max_items": null,              // null = all items, or set a number
    "delay_between_items": 2,       // seconds between each relist
    "headless": false,              // true = invisible browser
    "chrome_profile": null          // path to Chrome profile (stay logged in)
}
```

### 💡 Pro Tip: Stay Logged In

To avoid logging in every time, set your Chrome profile:

**Find your Chrome profile path:**
- **Windows:** `C:\Users\YourName\AppData\Local\Google\Chrome\User Data`
- **Mac:** `/Users/YourName/Library/Application Support/Google/Chrome`
- **Linux:** `/home/yourname/.config/google-chrome`

Then update `config.json`:
```json
"chrome_profile": "YOUR_PATH_HERE"
```

⚠️ Close all Chrome windows before running with a profile!

---

## 📅 Automatic Scheduling

Your automation is already set to run:
- **9:00 AM** - Morning relist
- **4:00 PM** - Afternoon relist

This maximizes visibility on Poshmark!

### Check Schedule Status

The shortcut has been created for you. It will run automatically at the scheduled times.

### Manual Run Anytime

Just double-click:
- `run_poshmark.bat` (Windows)
- `run_poshmark.sh` (Mac/Linux)

Or run: `python3 poshmark_relister.py`

---

## 📊 Checking Results

After each run, check:
- **Log file:** `poshmark_relist_YYYYMMDD.log`
- **Poshmark:** Your items should be at the top of your closet

Example log:
```
2025-02-16 09:00:23 - INFO - Found 45 items. Will relist 45 items.
2025-02-16 09:15:42 - INFO - Successfully relisted: 45
2025-02-16 09:15:42 - INFO - Failed: 0
```

---

## 🎁 Bonus: Create Executable

Want a standalone app that doesn't require Python?

See **EXECUTABLE_GUIDE.md** for step-by-step instructions to create:
- Windows: `.exe` file
- Mac: Standalone app
- Linux: Binary executable

---

## 🐛 Troubleshooting

### "Could not find items"
- Make sure you're logged into Poshmark
- Check that you have items in your closet
- Review log file for specific errors

### "ChromeDriver error"
- Update: `pip install --upgrade selenium`
- Ensure Chrome browser is installed

### Still having issues?
1. Check log files
2. Run with visible browser (`"headless": false`)
3. Try increasing delays in config
4. See full README.md for detailed troubleshooting

---

## 📁 File Overview

```
📁 Your Folder/
├── poshmark_relister.py      ← Main script
├── config.json                ← Settings
├── requirements.txt           ← Dependencies
├── run_poshmark.bat          ← Windows runner
├── run_poshmark.sh           ← Mac/Linux runner
├── QUICK_START.md            ← This file
├── README.md                 ← Full documentation
├── EXECUTABLE_GUIDE.md       ← How to create .exe
└── poshmark_relist_*.log     ← Log files (created after runs)
```

---

## 🎉 You're All Set!

Your Poshmark items will now automatically relist twice daily to maximize visibility and sales!

**Next Steps:**
1. ✅ Test run to ensure everything works
2. ✅ Configure settings to your preference
3. ✅ Let it run automatically!
4. 📈 Watch your sales increase

---

**Need Help?**
Check README.md for detailed documentation and troubleshooting.

**Want More Control?**
You're advanced - feel free to modify the Python script to add custom features!

Happy Poshing! 🛍️
