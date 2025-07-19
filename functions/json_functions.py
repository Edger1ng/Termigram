import json
import os

SETTINGS_FILE = "settings.json"


if not os.path.exists(SETTINGS_FILE):
    default_settings = {
        "DEBUG": False,
        "BOT_TOKEN": "",
        "FIRST_START": True,
        "WAITING_FOR_ADMIN_IDS": False,
        "SUDO_USER": "",
        "SUDO_PASSWORD": "",
        "ADMIN_IDS": [],
        "FUNCTIONS_ALLOWED": []
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(default_settings, file, ensure_ascii=False, indent=4)
        
def load(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        if data.get("DEBUG") is True:
            print("JSON settings loaded")
        return data

def save(data, filename=SETTINGS_FILE):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        if data.get("DEBUG") is True:
            print("JSON settings saved")

def update_setting(key, value, filename=SETTINGS_FILE):
    data = load(filename)
    data[key] = value
    save(data, filename)
    if data.get("DEBUG") is True:
        print(f"Setting '{key}' updated to '{value}' in {filename}")