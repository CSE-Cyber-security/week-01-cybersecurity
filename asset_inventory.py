"""
Cybersecurity Asset Inventory System
Weekly Mini Project - 01

A command-line tool for a security administrator to Add, Search, Update,
Delete, and Display IT assets, with basic risk/security classification
and a summary dashboard. Data is persisted to data/assets.json.
"""

import json
import os
import re

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "assets.json")

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
SECURITY_STATUSES = ["Secure", "Warning", "Vulnerable"]

IP_PATTERN = re.compile(
    r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
)


# ---------------------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------------------

def load_assets():
    """Load assets list from the JSON data file. Returns [] if missing/empty."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        print("Warning: could not read existing data file. Starting fresh.")
        return []


def save_assets(assets):
    """Save the current assets list to the JSON data file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(assets, f, indent=4)


# ---------------------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------------------

def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  -> This field cannot be empty. Please try again.")


def get_valid_ip(prompt):
    while True:
        ip = input(prompt).strip()
        match = IP_PATTERN.match(ip)
        if match and all(0 <= int(octet) <= 255 for octet in match.groups()):
            return ip
        print("  -> Invalid IP address format. Example: 192.168.1.10")


def get_choice(prompt, options):
    options_display = "/".join(options)
    while True:
        value = input(f"{prompt} ({options_display}): ").strip().title()
        if value in options:
            return value
        print(f"  -> Invalid choice. Please enter one of: {options_display}")


def get_unique_asset_id(prompt, assets, exclude_id=None):
    existing_ids = {a["asset_id"] for a in assets if a["asset_id"] != exclude_id}
    while True:
        asset_id = get_nonempty(prompt)
        if asset_id in existing_ids:
            print(f"  -> Asset ID '{asset_id}' already exists. Please enter a unique ID.")
        else:
            return asset_id


# ---------------------------------------------------------------------------
# Core features
# ---------------------------------------------------------------------------

def add_asset(assets):
    print("\n--- Add New Asset ---")
    asset_id = get_unique_asset_id("Asset ID: ", assets)
    asset = {
        "asset_id": asset_id,
        "asset_name": get_nonempty("Asset Name: "),
        "asset_type": get_choice("Asset Type", ASSET_TYPES),
        "ip_address": get_valid_ip("IP Address: "),
        "os": get_nonempty("Operating System: "),
        "department": get_nonempty("Owner/Department: "),
        "risk_level": get_choice("Risk Level", RISK_LEVELS),
        "security_status": get_choice("Security Status", SECURITY_STATUSES),
    }
    assets.append(asset)
    save_assets(assets)
    print(f"Asset '{asset_id}' added successfully.\n")


def display_assets(assets):
    print("\n" + "=" * 41)
    print(" CYBERSECURITY ASSET INVENTORY")
    print("=" * 41)
    if not assets:
        print("No assets found.")
    else:
        for i, a in enumerate(assets):
            print(f"Asset ID     : {a['asset_id']}")
            print(f"Asset Name   : {a['asset_name']}")
            print(f"Asset Type   : {a['asset_type']}")
            print(f"IP Address   : {a['ip_address']}")
            print(f"OS           : {a['os']}")
            print(f"Department   : {a['department']}")
            print(f"Risk Level   : {a['risk_level']}")
            print(f"Status       : {a['security_status']}")
            if i != len(assets) - 1:
                print("-" * 41)
    print("=" * 41)
    print_summary(assets)


def print_summary(assets):
    total = len(assets)
    critical = sum(1 for a in assets if a["risk_level"] == "Critical")
    high = sum(1 for a in assets if a["risk_level"] == "High")
    medium = sum(1 for a in assets if a["risk_level"] == "Medium")
    vulnerable = sum(1 for a in assets if a["security_status"] == "Vulnerable")

    print(f"Total Assets       : {total}")
    print(f"Critical Assets    : {critical}")
    print(f"High Risk Assets   : {high}")
    print(f"Medium Risk Assets : {medium}")
    print(f"Vulnerable Assets  : {vulnerable}")
    print("=" * 41 + "\n")


def find_asset(assets, asset_id):
    for a in assets:
        if a["asset_id"].lower() == asset_id.lower():
            return a
    return None


def search_asset(assets):
    print("\n--- Search Asset ---")
    if not assets:
        print("No assets to search.\n")
        return
    asset_id = get_nonempty("Enter Asset ID to search: ")
    asset = find_asset(assets, asset_id)
    if asset:
        display_assets([asset])
    else:
        print(f"No asset found with ID '{asset_id}'.\n")


def update_asset(assets):
    print("\n--- Update Asset ---")
    if not assets:
        print("No assets to update.\n")
        return
    asset_id = get_nonempty("Enter Asset ID to update: ")
    asset = find_asset(assets, asset_id)
    if not asset:
        print(f"No asset found with ID '{asset_id}'.\n")
        return

    print("Leave a field blank to keep its current value.")
    new_name = input(f"Asset Name [{asset['asset_name']}]: ").strip()
    if new_name:
        asset["asset_name"] = new_name

    new_type = input(f"Asset Type [{asset['asset_type']}] ({'/'.join(ASSET_TYPES)}): ").strip().title()
    if new_type:
        while new_type not in ASSET_TYPES:
            print(f"  -> Invalid choice. Options: {'/'.join(ASSET_TYPES)}")
            new_type = input("Asset Type: ").strip().title()
        asset["asset_type"] = new_type

    new_ip = input(f"IP Address [{asset['ip_address']}]: ").strip()
    if new_ip:
        while not (IP_PATTERN.match(new_ip) and all(0 <= int(o) <= 255 for o in IP_PATTERN.match(new_ip).groups())):
            print("  -> Invalid IP address format.")
            new_ip = input("IP Address: ").strip()
        asset["ip_address"] = new_ip

    new_os = input(f"Operating System [{asset['os']}]: ").strip()
    if new_os:
        asset["os"] = new_os

    new_dept = input(f"Department [{asset['department']}]: ").strip()
    if new_dept:
        asset["department"] = new_dept

    new_risk = input(f"Risk Level [{asset['risk_level']}] ({'/'.join(RISK_LEVELS)}): ").strip().title()
    if new_risk:
        while new_risk not in RISK_LEVELS:
            print(f"  -> Invalid choice. Options: {'/'.join(RISK_LEVELS)}")
            new_risk = input("Risk Level: ").strip().title()
        asset["risk_level"] = new_risk

    new_status = input(f"Security Status [{asset['security_status']}] ({'/'.join(SECURITY_STATUSES)}): ").strip().title()
    if new_status:
        while new_status not in SECURITY_STATUSES:
            print(f"  -> Invalid choice. Options: {'/'.join(SECURITY_STATUSES)}")
            new_status = input("Security Status: ").strip().title()
        asset["security_status"] = new_status

    save_assets(assets)
    print(f"Asset '{asset_id}' updated successfully.\n")


def delete_asset(assets):
    print("\n--- Delete Asset ---")
    if not assets:
        print("No assets to delete.\n")
        return
    asset_id = get_nonempty("Enter Asset ID to delete: ")
    asset = find_asset(assets, asset_id)
    if not asset:
        print(f"No asset found with ID '{asset_id}'.\n")
        return
    confirm = input(f"Are you sure you want to delete '{asset_id}'? (y/n): ").strip().lower()
    if confirm == "y":
        assets.remove(asset)
        save_assets(assets)
        print(f"Asset '{asset_id}' deleted successfully.\n")
    else:
        print("Delete cancelled.\n")


# ---------------------------------------------------------------------------
# Menu / main loop
# ---------------------------------------------------------------------------

def print_menu():
    print("\n========= CYBERSECURITY ASSET INVENTORY SYSTEM =========")
    print("1. Add Asset")
    print("2. Search Asset")
    print("3. Update Asset")
    print("4. Delete Asset")
    print("5. Display All Assets")
    print("6. Exit")
    print("==========================================================")


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-6): ").strip()
        if choice in {"1", "2", "3", "4", "5", "6"}:
            return choice
        print("  -> Invalid input. Please enter a number between 1 and 6.")


def main():
    assets = load_assets()
    print("Welcome to the Cybersecurity Asset Inventory System.")

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_asset(assets)
        elif choice == "2":
            search_asset(assets)
        elif choice == "3":
            update_asset(assets)
        elif choice == "4":
            delete_asset(assets)
        elif choice == "5":
            display_assets(assets)
        elif choice == "6":
            print("Exiting. All data has been saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
