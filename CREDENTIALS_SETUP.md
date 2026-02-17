# 🔐 Automatic Login Setup

## ✅ Updated! Now with Automated Login

Your script now **automatically logs in** using credentials you provide once, and then **stays logged in** forever!

---

## 🚀 Quick Setup (2 Steps)

### Step 1: Add Your Credentials

Open `config.json` and add your Poshmark login details:

```json
{
    "poshmark_url": "https://poshmark.com/closet",
    "poshmark_username": "your_email@example.com",
    "poshmark_password": "your_password",
    "max_items": null,
    "delay_between_items": 2,
    "page_load_timeout": 10,
    "element_wait_timeout": 5,
    "headless": true,
    "chrome_profile": null
}
```

**Replace:**
- `"your_email@example.com"` with your actual Poshmark email/username
- `"your_password"` with your actual Poshmark password

### Step 2: Set Up Chrome Profile (Stay Logged In)

Run this command once:

```bash
python3 find_chrome_profile.py
```

This automatically configures Chrome to remember your login session.

**That's it!** Your script will now:
- ✅ Log in automatically on first run
- ✅ Stay logged in forever (using Chrome profile)
- ✅ Run completely invisibly (headless mode already enabled)

---

## 🎯 How It Works

### First Run:
```
Script starts
    ↓
Opens Chrome (invisibly)
    ↓
Navigates to Poshmark login page
    ↓
Automatically enters your username
    ↓
Automatically enters your password
    ↓
Clicks "Log In" button
    ↓
Chrome profile saves the session
    ↓
Proceeds to relist items
```

### Every Run After:
```
Script starts
    ↓
Opens Chrome (invisibly)
    ↓
Chrome says "Already logged in!"
    ↓
Proceeds directly to relisting
    ↓
No login needed! ✨
```

---

## 🔐 Security Information

### Where Are Credentials Stored?

Your credentials are stored **ONLY** in `config.json` on **your computer**.

**Security features:**
- ✅ File is local on your machine
- ✅ Never transmitted anywhere except to Poshmark
- ✅ No third-party servers involved
- ✅ You control the file

### Best Practices:

1. **Keep config.json secure**
   - Don't share it with anyone
   - Don't commit it to GitHub/Git
   - Keep it in a secure folder

2. **File Permissions (Optional but Recommended)**

   **Mac/Linux:**
   ```bash
   chmod 600 config.json
   ```
   This makes the file readable only by you.

   **Windows:**
   - Right-click config.json
   - Properties → Security → Advanced
   - Remove all users except yourself

3. **Use Strong Password**
   - Enable 2FA on your Poshmark account
   - Use a unique password

4. **Alternative: Environment Variables (Advanced)**

   Instead of storing in config.json, use environment variables:

   **Set environment variables:**
   ```bash
   # Mac/Linux
   export POSHMARK_USERNAME="your_email@example.com"
   export POSHMARK_PASSWORD="your_password"

   # Windows (PowerShell)
   $env:POSHMARK_USERNAME="your_email@example.com"
   $env:POSHMARK_PASSWORD="your_password"
   ```

   Then leave config.json empty - the script will check environment variables first.

---

## 🛠️ Troubleshooting

### "Login failed - still on login page"

**Possible causes:**
1. **Wrong credentials** - Double-check username/password in config.json
2. **Poshmark changed login page** - Selectors may need updating
3. **2FA enabled** - Script can't handle 2FA automatically

**Solutions:**
- Verify credentials are correct
- Check for typos in config.json
- Try logging in manually first to verify credentials work
- Temporarily disable 2FA (not recommended) or use Chrome profile method

### "Could not find username field"

Poshmark's login page structure changed. The script includes multiple selector fallbacks, but you may need to:
- Take a screenshot (auto-saved as `login_error_*.png`)
- Update selectors in the script if you're comfortable with code

### Chrome Profile Not Working

Make sure:
1. You ran `find_chrome_profile.py` successfully
2. Chrome is **completely closed** before running the script
3. The path in config.json is correct

---

## 🎛️ Configuration Options

### Current Settings (Already Optimized):

```json
{
    "headless": true,           ← Chrome runs invisibly
    "chrome_profile": null      ← Run find_chrome_profile.py to set
}
```

### Want to See What's Happening?

For debugging, temporarily set:
```json
"headless": false
```

You'll see Chrome open and watch the login happen. Once verified, set back to `true`.

---

## 📊 Complete Flow After Setup

### Daily Automatic Runs (9 AM & 4 PM):

```
⏰ Schedule triggers at 9:00 AM
    ↓
🤖 Script starts silently
    ↓
🌐 Chrome opens invisibly
    ↓
🔐 Checks if logged in
    ↓
✅ Already logged in (thanks to Chrome profile!)
    ↓
📦 Finds all your closet items
    ↓
🔄 Relists each item (Edit → Next → List)
    ↓
📝 Creates log file with results
    ↓
🚪 Closes Chrome
    ↓
✨ Done! (You never saw anything)
    ↓
⏰ Repeats at 4:00 PM
```

**You only notice:**
- Log files appearing
- Items at top of your Poshmark closet
- More sales! 💰

---

## 🔒 Two-Factor Authentication (2FA)

If you have 2FA enabled on Poshmark:

### Option 1: Chrome Profile (Recommended)
1. Set `"headless": false` temporarily
2. Run script once
3. Complete 2FA manually when prompted
4. Chrome profile saves the authenticated session
5. Set `"headless": true` again
6. Future runs won't need 2FA!

### Option 2: Disable 2FA (Not Recommended)
Only if you're comfortable with the security trade-off.

---

## 🎉 You're All Set!

After following the setup:

✅ **Credentials added** to config.json
✅ **Chrome profile configured** (stay logged in)
✅ **Headless mode enabled** (invisible operation)
✅ **Scheduled** for 9 AM & 4 PM
✅ **Completely automated** - no intervention needed!

---

## 📝 Example config.json (Complete)

```json
{
    "poshmark_url": "https://poshmark.com/closet",
    "poshmark_username": "seller@example.com",
    "poshmark_password": "MySecurePassword123!",
    "max_items": null,
    "delay_between_items": 2,
    "page_load_timeout": 10,
    "element_wait_timeout": 5,
    "headless": true,
    "chrome_profile": "/Users/yourname/Library/Application Support/Google/Chrome"
}
```

---

## 🚀 Next Steps

1. **Add credentials** to config.json
2. **Run:** `python3 find_chrome_profile.py`
3. **Test:** `python3 poshmark_relister.py`
4. **Verify** in log file that login succeeded
5. **Relax** - automation handles everything now! 🎉

---

**Questions?**
- Check log files for detailed execution info
- Screenshots saved on errors for debugging
- All runs are logged with timestamps

**Happy automated Poshing!** 🛍️💰
