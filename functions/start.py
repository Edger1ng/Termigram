import json
from functions import json_functions as json_f
import os
import hashlib
import sys
from functions import arg_parse

settings = json_f.load(json_f.SETTINGS_FILE)
first = False

BASE_DIR = "in"
STORE_DIR = "sha_store"


def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_hashes():
    if arg_parse.override_security_check_integrity:
        print("Skipping integrity check due to override.")
        return
    print("Verifying file hashes...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    hash_file = os.path.join(base_dir, "checksums.json")

    with open(hash_file, "r") as f:
        hashes = json.load(f)

    for rel_path, expected_hash in hashes.items():
        # Skip settings.json from hash check
        if os.path.basename(rel_path) == "settings.json":
            continue
        abs_path = os.path.join(base_dir, rel_path)
        print(f"Checking {abs_path}...")
        if not os.path.exists(abs_path):
            print(f"File {abs_path} does not exist. Exiting.")
            sys.exit(1)
        actual_hash = get_file_hash(abs_path)
        if actual_hash != expected_hash:
            text = (
                f"\nHash mismatch for {abs_path}:\n"
                f"Expected: {expected_hash}\n"
                f"Actual: {actual_hash}\n"
                "Exiting due to hash mismatch.\n\n"
                "========\n"
                "This is a security check failure.\n"
                "It means that some files were changed or deleted.\n"
                "This is not a normal situation, and it can lead to unexpected behavior.\n"
                "Please, check your files and restore them if necessary.\n"
                "If you are sure that this is a false positive, you can override this check by starting the bot with '--exclude security_check_integrity' option.\n"
                "========"
            )
            print(
                text
            )
            print("Exiting due to hash mismatch.")
            sys.exit(1)


def first_start():
    print("This is the first start of the bot. If you did not set the bot token, please do so in settings.json.")
    print("Follow the instructions on the screen OR in Readme.md to setup me")

    if not settings.get("ADMIN_IDS"):
        text = (
            "========\n"
            "Hi! I am very happy to see you here.\n"
            "To gain access to admin panel id, you need to go to chat with me and click 'start' button.\n"
            "After that, you will be able to use admin panel.\n"
            "I would be waiting for you in chat.\n"
            "========"
        )
        print(text)
        settings["WAITING_FOR_ADMIN_IDS"] = True
        json_f.save(settings)
    else:
        print("Admin IDs are already set. Proceeding with bot startup.")

    settings["FIRST_START"] = False
    json_f.save(settings)


def security_check():
    if settings.get("DEBUG"):
        print("Security check is disabled in DEBUG mode.")
        return

    if settings.get("WAITING_FOR_ADMIN_IDS") and first != True and not arg_parse.override_security_check_wfa:
        text = (
            "========\n"
            "SECURITY WARN:\n"
            "Bot is now waiting for admin IDs adding by /start command, but it's not the first start.\n"
            "Using WAITING_FOR_ADMIN_IDS manual in settings.json is not recommended.\n"
            "Start of the bot is stopped.\n"
            "To override this, which is not reccommended, start the bot with '--exclude security_check_wfa' option.\n"
            "========"
        )
        print(text)
    if not arg_parse.override_security_check_integrity:
        verify_hashes()


def main_f():
    if settings.get("DEBUG"):
        print("Bot is starting with DEBUG mode enabled")
    else:
        print("Bot is starting in production mode")

    global first
    if not os.path.exists(json_f.SETTINGS_FILE):
        print("Settings file not found. Please create settings.json.")
        sys.exit(1)



    first = settings.get("FIRST_START", False)
    security_check()

    if first:
        first_start()
    
    else:
        print("Bot is already set up. Proceeding with normal startup.")
        print("You can change settings in settings.json file.")
