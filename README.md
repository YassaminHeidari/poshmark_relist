# 🛍️ Poshmark Auto-Relister

Automate your Poshmark listings! This tool automatically relists all your items twice daily to maximize visibility and increase sales.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🤖 **Fully Automated** - Runs on schedule without manual intervention
- 🔐 **Automatic Login** - Saves credentials and stays logged in
- 👻 **Invisible Mode** - Runs headless in the background
- ⏰ **Scheduled Relisting** - Twice daily (9 AM & 4 PM) for maximum visibility
- 📊 **Detailed Logging** - Track every action and result
- 🌐 **Cross-Platform** - Works on Windows, Mac, and Linux
- ⚡ **Easy Setup** - 5-minute installation

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YassaminHeidari/poshmark_relist.git
cd poshmark_relist
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

```bash
# Copy the example config
cp config.example.json config.json

# Edit config.json and add your Poshmark credentials
nano config.json  # or use any text editor
```

### 4. Set Up Chrome Profile (Optional but Recommended)

```bash
python3 find_chrome_profile.py
```

This ensures you stay logged in between runs.

### 5. Run the Script

```bash
# Test run
python3 poshmark_relister.py

# Or use the launcher scripts
# Windows:
run_poshmark.bat

# Mac/Linux:
./run_poshmark.sh
```

---

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
    "poshmark_username": "your_email@example.com",
    "poshmark_password": "your_password",
    "max_items": null,              // null = all items, or set a number
    "delay_between_items": 2,       // seconds between each relist
    "headless": true,               // true = invisible, false = show browser
    "chrome_profile": null          // auto-filled by find_chrome_profile.py
}
```

---

## 📅 Scheduling

### Automatic (Twice Daily)

The shortcut system schedules automatic runs at:
- **9:00 AM** - Morning relist
- **4:00 PM** - Afternoon relist

### Manual Run

Run anytime:
```bash
python3 poshmark_relister.py
```

Or double-click the launcher:
- Windows: `run_poshmark.bat`
- Mac/Linux: `run_poshmark.sh`

---

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)** - Complete getting started guide
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup
- **[CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md)** - Login configuration
- **[HEADLESS_SETUP.md](HEADLESS_SETUP.md)** - Invisible operation
- **[EXECUTABLE_GUIDE.md](EXECUTABLE_GUIDE.md)** - Create standalone app
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Detailed project info
- **[WORKFLOW_DIAGRAM.txt](WORKFLOW_DIAGRAM.txt)** - Visual reference

---

## 🔐 Security

Your credentials are:
- ✅ Stored **only** on your computer in `config.json`
- ✅ Never transmitted to any third party
- ✅ Only used to log into Poshmark
- ✅ Protected by `.gitignore` (never committed to git)

**Recommendation:** Set file permissions:
```bash
# Mac/Linux
chmod 600 config.json
```

---

## 📊 How It Works

```
Script starts
    ↓
Opens Chrome (invisibly)
    ↓
Logs into Poshmark automatically
    ↓
Navigates to your closet
    ↓
For each item:
  • Click Edit
  • Click Next
  • Click List
    ↓
All items now at top of search!
    ↓
Creates log file with results
    ↓
Done! ✨
```

---

## 🛠️ Troubleshooting

### Login Failed
- Verify credentials in `config.json`
- Check for typos
- Ensure Poshmark account is active

### Items Not Relisting
- Check log files for specific errors
- Verify items exist in your closet
- Review Poshmark's daily relisting limits

### Chrome Issues
- Update: `pip install --upgrade selenium`
- Ensure Chrome browser is installed
- Close all Chrome windows before using Chrome profile

See [README.md](README.md) for detailed troubleshooting.

---

## 📦 Requirements

- Python 3.7+
- Chrome Browser
- Internet connection

Python packages (installed via `requirements.txt`):
- selenium >= 4.15.0
- webdriver-manager >= 4.0.0

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ⚠️ Disclaimer

This tool is for educational purposes. Use responsibly and in accordance with Poshmark's Terms of Service. Automated actions may be subject to Poshmark's policies. Use at your own risk.

---

## 🌟 Star This Repo

If this tool helps you, please ⭐ star this repository!

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/YassaminHeidari/poshmark_relist/issues)
- **Documentation:** See the [docs folder](.)

---

**Happy Poshing!** 🛍️💰

Made with ❤️ for automated Poshmark success
