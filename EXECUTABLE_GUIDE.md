# Creating a Standalone Executable

This guide will help you convert the Python script into a standalone executable that you can double-click to run without needing Python installed.

## Why Create an Executable?

- **No Python Required:** Run on any computer without installing Python
- **Easy Distribution:** Share with friends who also sell on Poshmark
- **One-Click Operation:** Just double-click the file to run
- **Portable:** Move it anywhere and it still works

## Prerequisites

You need Python installed **once** to create the executable. After that, the executable can run without Python.

## Method 1: Using PyInstaller (Recommended)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Create the Executable

**For Windows:**
```bash
pyinstaller --onefile --noconsole --add-data "config.json;." --icon=poshmark.ico poshmark_relister.py
```

**For Mac:**
```bash
pyinstaller --onefile --windowed --add-data "config.json:." poshmark_relister.py
```

**For Linux:**
```bash
pyinstaller --onefile --add-data "config.json:." poshmark_relister.py
```

### Step 3: Find Your Executable

After PyInstaller finishes:
- Your executable will be in the `dist/` folder
- **Windows:** `dist/poshmark_relister.exe`
- **Mac/Linux:** `dist/poshmark_relister`

### Step 4: Bundle Required Files

Create a folder with:
```
📁 PoshmarkRelister/
  ├── poshmark_relister.exe (or poshmark_relister on Mac/Linux)
  └── config.json
```

## Method 2: Using Auto-py-to-exe (GUI Tool)

For those who prefer a graphical interface:

### Step 1: Install Auto-py-to-exe

```bash
pip install auto-py-to-exe
```

### Step 2: Launch the GUI

```bash
auto-py-to-exe
```

### Step 3: Configure Settings

In the GUI:
1. **Script Location:** Browse to `poshmark_relister.py`
2. **Onefile:** Select "One File"
3. **Console Window:** Select "Window Based (hide console)" for cleaner experience
4. **Additional Files:** Add `config.json`
5. **Icon:** (Optional) Add a custom icon
6. Click **"CONVERT .PY TO .EXE"**

## Advanced PyInstaller Options

### Create Console Version (See Output/Errors)

```bash
pyinstaller --onefile --add-data "config.json;." poshmark_relister.py
```

This shows a console window with logs (helpful for debugging).

### Create Windowed Version (No Console)

```bash
pyinstaller --onefile --noconsole --add-data "config.json;." poshmark_relister.py
```

Runs silently in the background (best for scheduled tasks).

### Add Custom Icon

```bash
pyinstaller --onefile --icon=myicon.ico --add-data "config.json;." poshmark_relister.py
```

### Optimize File Size

```bash
pyinstaller --onefile --add-data "config.json;." --exclude-module matplotlib --exclude-module pandas poshmark_relister.py
```

## Creating a Spec File (Advanced)

For more control, create a `.spec` file:

```bash
# Generate spec file
pyi-makespec --onefile poshmark_relister.py

# Edit poshmark_relister.spec as needed

# Build from spec file
pyinstaller poshmark_relister.spec
```

Example `poshmark_relister.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['poshmark_relister.py'],
    pathex=[],
    binaries=[],
    datas=[('config.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PoshmarkRelister',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True to see console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='poshmark.ico'  # Optional custom icon
)
```

## Scheduling the Executable

### Windows Task Scheduler

1. Open **Task Scheduler**
2. Click **"Create Basic Task"**
3. Name: "Poshmark Morning Relist"
4. Trigger: **Daily** at **9:00 AM**
5. Action: **Start a program**
6. Program: Browse to your `.exe` file
7. Repeat for afternoon (4:00 PM)

### Mac (launchd)

Create: `~/Library/LaunchAgents/com.poshmark.relister.morning.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.poshmark.relister.morning</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/poshmark_relister</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.poshmark.relister.morning.plist
```

### Linux (cron)

```bash
crontab -e
```

Add:
```
0 9 * * * /path/to/poshmark_relister
0 16 * * * /path/to/poshmark_relister
```

## Troubleshooting Executable

### "Windows protected your PC" Warning

This is normal for unsigned executables:
1. Click **"More info"**
2. Click **"Run anyway"**

### Antivirus False Positives

Some antivirus software flags automation tools:
1. Add the executable to your antivirus exclusions
2. Or use the console version to see what's happening

### Executable Not Working

**Debug by creating console version:**
```bash
pyinstaller --onefile --add-data "config.json;." poshmark_relister.py
```

This will show error messages when you run it.

**Common Issues:**
- Missing `config.json` in same folder
- Chrome not installed
- Outdated ChromeDriver (should auto-update)

### File Size Too Large

Typical executable size: 50-100 MB (includes Python runtime + dependencies)

**To reduce size:**
1. Use UPX compression: `pyinstaller --onefile --upx-dir=/path/to/upx ...`
2. Exclude unused modules: `--exclude-module matplotlib`
3. Consider using a Python installer instead

## Testing Your Executable

Before scheduling:

1. **Test Run:** Double-click the executable manually
2. **Check Logs:** Verify log files are created
3. **Verify Relisting:** Check Poshmark to confirm items were relisted
4. **Test Schedule:** Set a test schedule 2 minutes in the future

## Distribution

If sharing with others:

**Package includes:**
```
📁 PoshmarkRelister_v1.0/
  ├── poshmark_relister.exe
  ├── config.json
  ├── README.txt (simplified instructions)
  └── LICENSE.txt (if applicable)
```

**Simple README.txt for users:**
```
Poshmark Auto-Relister

1. Keep this .exe and config.json together
2. Double-click poshmark_relister.exe to run
3. Edit config.json to customize settings
4. Logs are created in the same folder

First run: You may need to log into Poshmark manually.
```

## Security Note

- Executables created with PyInstaller can sometimes trigger antivirus warnings
- This is because they package Python + dependencies + script together
- Your executable is safe, but users should download from trusted sources only
- Consider code signing (advanced, requires certificate) for distribution

## Alternative: Python Installer

Instead of a single executable, you could create an installer:

**Using Inno Setup (Windows):**
1. Download Inno Setup
2. Create script that installs Python dependencies + your script
3. Users run installer once, then use your script

This approach:
- ✅ Smaller download size
- ✅ Easier to update
- ❌ More complex setup

---

**Recommendation:** Start with PyInstaller's one-file option for personal use. It's simple and works great!
