# 🚫 No Chrome Window Setup

## ✅ Done! Headless Mode Enabled

I've already set `"headless": true` in your config.json. Chrome will now run invisibly!

---

## 🎯 Complete Invisible Setup (Recommended)

For **fully automatic, invisible operation** with no login needed:

### Step 1: Find Your Chrome Profile (One-Time Setup)

Run this command in the PoshmarkAutoRelister folder:

```bash
python3 find_chrome_profile.py
```

**What it does:**
- Automatically finds your Chrome profile path
- Updates config.json for you
- Enables persistent login

### Step 2: First Login (One-Time)

**Temporarily set headless to false** for the first run:

Edit `config.json`:
```json
"headless": false
```

**Run the script once:**
```bash
python3 poshmark_relister.py
```

- Browser will open (last time you'll see it!)
- Log into Poshmark
- Let the script complete

### Step 3: Enable Headless Forever

Edit `config.json` back:
```json
"headless": true
```

**Done!** From now on:
- ✅ No Chrome window opens
- ✅ No login needed
- ✅ Runs completely invisibly
- ✅ Perfect for scheduled automation

---

## 🔍 How to Know It's Working

Since you won't see Chrome, check these:

### 1. Log Files
After each run, check: `poshmark_relist_YYYYMMDD.log`

Example:
```
2025-02-16 09:00:23 - INFO - Found 45 items. Will relist 45 items.
2025-02-16 09:15:42 - INFO - Successfully relisted: 45
```

### 2. Poshmark Closet
- Visit your Poshmark closet
- Your items should be at the top with fresh timestamps

### 3. Process Monitor (Optional)

**Windows:**
- Task Manager → Look for "chrome.exe" and "python.exe" processes while running

**Mac:**
- Activity Monitor → Look for "Google Chrome" and "Python" processes

**Linux:**
```bash
ps aux | grep chrome
```

---

## ⚙️ Current Configuration

Your `config.json` now has:

```json
{
    "headless": true,           ← Chrome runs invisibly
    "chrome_profile": null      ← Run find_chrome_profile.py to set this
}
```

**After running find_chrome_profile.py:**

```json
{
    "headless": true,           ← Chrome runs invisibly
    "chrome_profile": "/path"   ← Stays logged in
}
```

---

## 🎛️ Quick Toggle

Need to see Chrome for debugging?

**Show Chrome:**
```json
"headless": false
```

**Hide Chrome:**
```json
"headless": true
```

---

## 🚀 Scheduled Runs (9 AM & 4 PM)

With headless mode + Chrome profile:
- Script runs automatically at 9 AM
- Chrome opens invisibly in background
- Relists all items
- Closes silently
- You never see anything!
- Repeats at 4 PM

**You'll only know it ran by checking:**
- Log files
- Poshmark closet timestamps

---

## 💡 Pro Tips

1. **First time?** Run visible (`headless: false`) to verify everything works
2. **Set up Chrome profile** for best experience (no login needed)
3. **Check logs regularly** first week to ensure smooth operation
4. **Close Chrome** when first setting up Chrome profile
5. **Trust the process** - if logs show success, it worked!

---

## ⚠️ Troubleshooting Headless Mode

### "Script seems stuck"
- Check log file - it's probably working
- Headless mode is slower (no visual feedback)
- Be patient, it takes 5-10 minutes for 50 items

### "No log file created"
- Script might have crashed
- Run with `headless: false` to see what's happening
- Check for Chrome/ChromeDriver updates

### "Items not relisting"
- Check log for specific errors
- Verify Chrome profile is set correctly
- Try running visible first to debug

---

## 🎉 Summary

**Before:** Chrome opens → You see everything → Distracting

**After:**
- Chrome runs invisibly
- No windows pop up
- No login needed (with profile)
- Perfect for automatic scheduling
- Silent operation

**You'll only notice:**
- ✅ Log files appearing
- ✅ Items at top of your closet
- ✅ More sales! 💰

---

**Ready?** Run `python3 find_chrome_profile.py` to complete the setup!
