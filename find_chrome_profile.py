#!/usr/bin/env python3
"""
Chrome Profile Finder
Helps you locate your Chrome profile path for the config.json file
"""

import os
import platform
import json

def find_chrome_profile():
    """Find Chrome profile path based on operating system"""
    system = platform.system()

    if system == "Windows":
        paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Google', 'Chrome', 'User Data'),
        ]
    elif system == "Darwin":  # macOS
        paths = [
            os.path.expanduser('~/Library/Application Support/Google/Chrome'),
        ]
    elif system == "Linux":
        paths = [
            os.path.expanduser('~/.config/google-chrome'),
            os.path.expanduser('~/.config/chromium'),
        ]
    else:
        print(f"Unknown operating system: {system}")
        return None

    # Check which path exists
    for path in paths:
        if os.path.exists(path):
            return path

    return None

def main():
    print("=" * 60)
    print("Chrome Profile Finder")
    print("=" * 60)
    print()

    profile_path = find_chrome_profile()

    if profile_path:
        print("✅ Found Chrome profile at:")
        print(f"   {profile_path}")
        print()
        print("📝 To use this in your automation:")
        print()
        print("1. Open config.json")
        print("2. Find the line: \"chrome_profile\": null")
        print("3. Change it to:")
        print(f"   \"chrome_profile\": \"{profile_path}\"")
        print()

        # Offer to update config automatically
        response = input("Would you like to automatically update config.json? (y/n): ")

        if response.lower() == 'y':
            try:
                # Read current config
                with open('config.json', 'r') as f:
                    config = json.load(f)

                # Update profile path
                config['chrome_profile'] = profile_path

                # Write back
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)

                print()
                print("✅ config.json has been updated!")
                print()
            except Exception as e:
                print()
                print(f"❌ Error updating config.json: {e}")
                print("Please update it manually.")
                print()
        else:
            print()
            print("Please update config.json manually with the path above.")
            print()

        print("⚠️  IMPORTANT:")
        print("   Close ALL Chrome windows before running the automation")
        print("   when using a Chrome profile.")
        print()

    else:
        print("❌ Could not find Chrome profile automatically.")
        print()
        print("Please locate it manually:")
        print()
        print("Windows: C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data")
        print("Mac: /Users/YourName/Library/Application Support/Google/Chrome")
        print("Linux: /home/yourname/.config/google-chrome")
        print()

    print("=" * 60)

if __name__ == "__main__":
    main()
