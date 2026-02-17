# 🎯 START HERE - Poshmark Auto-Relister

## Welcome! 👋

You've got a **complete automation system** to relist your Poshmark items twice daily (9 AM & 4 PM).

---

## 🚀 Get Started in 3 Steps

### 1️⃣ Install Python Dependencies (2 minutes)

Open terminal/command prompt in this folder:

```bash
pip install -r requirements.txt
```

### 2️⃣ Run Your First Test (1 minute)

**Option A - Easy way (recommended):**
- **Windows:** Double-click `run_poshmark.bat`
- **Mac/Linux:** Double-click `run_poshmark.sh`

**Option B - Command line:**
```bash
python3 poshmark_relister.py
```

### 3️⃣ Log into Poshmark if needed

- Browser will open automatically
- If not logged in, you have 60 seconds to log in
- After that, it runs on autopilot!

---

## 📚 Documentation Guide

### 🏃 Quick Start
**→ Read first:** [`QUICK_START.md`](QUICK_START.md)
- 5-minute setup guide
- Installation steps
- Basic configuration
- Troubleshooting

### 📖 Complete Reference
**→ For details:** [`README.md`](README.md)
- Full documentation
- Advanced configuration
- Comprehensive troubleshooting
- Scheduling details
- Log file examples

### 🗺️ Project Overview
**→ For understanding:** [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md)
- What's included
- Key features
- Expected results
- Customization options

### 📊 Workflow Diagram
**→ Visual learner?** [`WORKFLOW_DIAGRAM.txt`](WORKFLOW_DIAGRAM.txt)
- Visual flow charts
- Step-by-step process
- Timeline examples
- File interactions

### 📦 Create Executable
**→ Want standalone app?** [`EXECUTABLE_GUIDE.md`](EXECUTABLE_GUIDE.md)
- Step-by-step PyInstaller guide
- GUI tool option
- Distribution instructions

---

## 📁 What's in This Package?

### 🔧 Core Files (Run these)
- `poshmark_relister.py` - Main automation script
- `run_poshmark.bat` - Windows quick launcher
- `run_poshmark.sh` - Mac/Linux quick launcher

### ⚙️ Configuration
- `config.json` - Settings (edit this to customize)
- `requirements.txt` - Python dependencies

### 🛠️ Utilities
- `find_chrome_profile.py` - Find Chrome path for auto-login

### 📚 Documentation (Read these)
- `START_HERE.md` - This file
- `QUICK_START.md` - Fast setup
- `README.md` - Complete guide
- `PROJECT_OVERVIEW.md` - Project details
- `WORKFLOW_DIAGRAM.txt` - Visual reference
- `EXECUTABLE_GUIDE.md` - Standalone app

---

## ⚙️ Quick Configuration

### Stay Logged In (Recommended!)

Run this to find your Chrome profile:
```bash
python3 find_chrome_profile.py
```

It will automatically update your `config.json` so you never have to log in again!

### Customize Behavior

Edit `config.json`:

```json
{
    "max_items": null,           ← null = all items, or set a number
    "delay_between_items": 2,    ← seconds between each relist
    "headless": false,           ← true = invisible browser
    "chrome_profile": null       ← auto-filled by find_chrome_profile.py
}
```

---

## 🎯 How It Works

```
9:00 AM Daily                           4:00 PM Daily
    ↓                                        ↓
Script Starts                           Script Starts
    ↓                                        ↓
Opens Chrome                            Opens Chrome
    ↓                                        ↓
Logs into Poshmark (if needed)         Already logged in
    ↓                                        ↓
Finds all your items                    Finds all your items
    ↓                                        ↓
For each item:                          For each item:
  • Click Edit                            • Click Edit
  • Click Next                            • Click Next
  • Click List                            • Click List
    ↓                                        ↓
All items now at top of closet!        All items now at top of closet!
    ↓                                        ↓
Creates log file                        Creates log file
    ↓                                        ↓
Done! ✨                                Done! ✨
```

---

## 📊 Check Your Results

After running, look for:

1. **Log file:** `poshmark_relist_YYYYMMDD.log`
   - Shows what happened
   - Number of items relisted
   - Any errors encountered

2. **Your Poshmark closet:**
   - All items should be at the top
   - Fresh listing timestamps
   - Increased visibility in search

---

## ❓ Common Questions

### Q: Will this work on my computer?
**A:** Yes! Works on Windows, Mac, and Linux.

### Q: Do I need to stay logged into Poshmark?
**A:** No, but it's easier. Run `find_chrome_profile.py` to set up auto-login.

### Q: How do I schedule it to run automatically?
**A:** It's already scheduled for 9 AM and 4 PM daily via the shortcut system!

### Q: Can I run it manually anytime?
**A:** Absolutely! Just double-click the run script or execute the Python file.

### Q: What if Poshmark's website changes?
**A:** You may need to update selectors in the Python script. Since you're advanced, this should be straightforward.

### Q: Is this safe?
**A:** Yes! Everything runs locally. No data is sent anywhere except to Poshmark through your browser.

### Q: Can I create a .exe file?
**A:** Yes! See `EXECUTABLE_GUIDE.md` for step-by-step instructions.

---

## 🐛 Quick Troubleshooting

### Script won't start
- Make sure Python is installed
- Run: `pip install -r requirements.txt`

### "Could not find items"
- Check that you're logged into Poshmark
- Verify you have items in your closet
- Review the log file for details

### Chrome won't open
- Make sure Chrome browser is installed
- Update selenium: `pip install --upgrade selenium`

### Need more help?
- Check `README.md` for detailed troubleshooting
- Review log files for specific errors
- Screenshot any errors you see

---

## 💡 Pro Tips

1. **First time?** Run with `"headless": false` to see what's happening
2. **Set up Chrome profile** for seamless operation
3. **Check logs after first run** to verify everything worked
4. **Start with defaults** then customize as needed
5. **Close Chrome** when using Chrome profile

---

## 🎉 You're All Set!

Your Poshmark automation is ready to go. Here's what happens next:

✅ **Today:** Test run to make sure everything works
✅ **Tomorrow:** Wakes up at 9 AM and relists your items
✅ **Every day:** Automatic relisting at 9 AM and 4 PM
✅ **Result:** Maximum visibility and more sales!

---

## 📖 Recommended Reading Order

1. **This file** ← You are here
2. **QUICK_START.md** ← Set up and run first test
3. **README.md** ← Learn advanced features
4. **PROJECT_OVERVIEW.md** ← Understand the system
5. **WORKFLOW_DIAGRAM.txt** ← Visual reference
6. **EXECUTABLE_GUIDE.md** ← Optional: Create .exe

---

## 📦 Package Information

- **Total Files:** 11
- **Package Size:** 88 KB
- **Setup Time:** ~5 minutes
- **Daily Time Saved:** 10-20 minutes
- **Supported OS:** Windows, Mac, Linux

---

## 🚀 Ready? Let's Go!

1. Open **QUICK_START.md** for setup instructions
2. Run your first test
3. Customize as needed
4. Enjoy automated relisting!

---

**Questions?** Check the documentation files above.
**Problems?** See README.md troubleshooting section.
**Want to customize?** You're advanced - dive into the code!

**Happy Poshing! 🛍️💰**

---

*Created with ❤️ for automated Poshmark success*
