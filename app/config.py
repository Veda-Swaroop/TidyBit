# Reading and writing JSON file

import json
import platform
from pathlib import Path
from app.file_extns import file_extensions as DEFAULT_EXTENSIONS


APP_NAME = "TidyBit"

if platform.system() == "Windows":
    CONFIG_DIR = Path.home() / "AppData" / "Local" / APP_NAME
else:
    CONFIG_DIR = Path.home() / ".config" / APP_NAME


SETTINGS_FILE = CONFIG_DIR / "settings.json"


# Function to write to JSON file
def save_settings(data):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(SETTINGS_FILE, mode="w", encoding="utf-8") as write_file:
            json.dump(data, write_file, indent=4)
        return True
    except(OSError, TypeError) as e:
        print(f"Error writing to {SETTINGS_FILE}: {e}")
        return False

# Function to read from JSON file
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, mode="r", encoding="utf-8") as read_file:
                data = json.load(read_file)
                if isinstance(data, dict):
                    return data
                
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {SETTINGS_FILE}: {e}")


    return DEFAULT_EXTENSIONS.copy()

# Function to restore default extensions
def get_defaults():
    # If extensions are deleted accidentally, this will reset 
    return DEFAULT_EXTENSIONS.copy()

