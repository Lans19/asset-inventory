#!/usr/bin/env python3
"""
Python Asset Inventory Tool
============================
A command-line tool for recording devices, operating systems, assigned users,
and asset status in a structured CSV inventory.

Features:
- Add new assets with unique IDs
- View all inventory items
- Search by keyword
- Update asset status
- Export summary reports
- CSV-based storage (easy to edit in Excel)

Usage:
    python asset_inventory_tool.py

Author: Your Name
Date: 2026
"""

import csv
import os
from datetime import datetime

# Configuration
CSV_FILE = "asset_inventory.csv"

FIELDNAMES = [
    "asset_id",
    "device_type",
    "hostname",
    "operating_system",
    "assigned_user",
    "department",
    "location",
    "purchase_date",
    "warranty_expiry",
    "status",
    "notes",
    "last_updated"
]

def initialize_inventory():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"✓ Initialized new inventory file: {CSV_FILE}")
    else:
        print(f"✓ Using existing inventory file: {CSV_FILE}")

def generate_asset_id():
    """Generate a unique asset ID based on timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"AST-{timestamp}"

def add_asset():
    """Add a new asset to the inventory."""
    print("\n" + "=" * 50)
    print("ADD NEW ASSET")
    print("=" * 50)

    print("\nEnter asset details (press Enter to skip optional fields):")

    asset = {
        "asset_id": generate_asset_id(),
        "device_type": input("Device Type* (e.g., Laptop, Desktop, Server, Printer): ").strip(),
        "hostname": input("Hostname* (e.g., WIN-LP-001): ").strip(),
        "operating_system": input("Operating System* (e.g., Windows 11, Ubuntu 22.04): ").strip(),
        "assigned_user": input("Assigned User* (e.g., John Dlamini): ").strip(),
        "department": input("Department (e.g., IT, HR, Finance): ").strip(),
        "location": input("Location (e.g., Big Bend Office, Remote): ").strip(),
        "purchase_date": input("Purchase Date (YYYY-MM-DD): ").strip(),
        "warranty_expiry": input("Warranty Expiry (YYYY-MM-DD): ").strip(),
        "status": input("Status* (Active, In Storage, Retired, Repair): ").strip(),
        "notes": input("Notes (optional): ").strip(),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Validate required fields
    required = ["device_type", "hostname", "operating_system", "assigned_user", "status"]
    missing = [field for field in required if not asset[field]]

    if missing:
        print(f"\n✗ Error: Missing required fields: {', '.join(missing)}")
        print("Asset not added.")
        return None

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(asset)

    print(f"\n✓ Asset added successfully!")
    print(f"  Asset ID: {asset['asset_id']}")
    print(f"  Device: {asset['device_type']} ({asset['hostname']})")
    print(f"  Assigned to: {asset['assigned_user']}")
    print(f"  Status: {asset['status']}")

    return asset

def view_all_assets():
    """Display all assets in the inventory."""
    print("\n" + "=" * 50)
    print("ALL ASSETS")
    print("=" * 50)

    if not os.path.exists(CSV_FILE):
        print("✗ No inventory file found. Please add an asset first.")
        return []

    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        assets = list(reader)

    if not assets:
        print("No assets in inventory.")
        return []

    print(f"\nTotal Assets: {len(assets)}\n")
    print("-" * 50)

    for i, asset in enumerate(assets, 1):
        print(f"[{i}] {asset['asset_id']}")
        print(f"    Device: {asset['device_type']} | Hostname: {asset['hostname']}")
        print(f"    OS: {asset['operating_system']} | User: {asset['assigned_user']}")
        print(f"    Dept: {asset['department']} | Location: {asset['location']}")
        print(f"    Status: {asset['status']} | Updated: {asset['last_updated']}")
        print("-" * 50)

    return assets

def search_assets():
    """Search assets by keyword."""
    print("\n" + "=" * 50)
    print("SEARCH ASSETS")
    print("=" * 50)

    if not os.path.exists(CSV_FILE):
        print("✗ No inventory file found.")
        return []

    keyword = input("\nEnter search keyword (hostname, user, OS, device, etc.): ").strip().lower()

    if not keyword:
        print("✗ No keyword entered.")
        return []

    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        assets = list(reader)

    results = [
        asset for asset in assets
        if any(keyword in str(value).lower() for value in asset.values())
    ]

    if not results:
        print(f"\n✗ No matching assets found for '{keyword}'")
        return []

    print(f"\n✓ Found {len(results)} matching asset(s):\n")
    print("-" * 50)

    for i, asset in enumerate(results, 1):
        print(f"[{i}] {asset['asset_id']} - {asset['device_type']} ({asset['hostname']})")
        print(f"    OS: {asset['operating_system']} | User: {asset['assigned_user']}")
        print(f"    Status: {asset['status']} | Location: {asset['location']}")
        print("-" * 50)

    return results

def update_asset_status():
    """Update the status of an existing asset."""
    print("\n" + "=" * 50)
    print("UPDATE ASSET STATUS")
    print("=" * 50)

    if not os.path.exists(CSV_FILE):
        print("✗ No inventory file found.")
        return False

    asset_id = input("\nEnter Asset ID to update (e.g., AST-20261007...): ").strip()

    if not asset_id:
        print("✗ No Asset ID entered.")
        return False

    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        assets = list(reader)

    found = False
    for asset in assets:
        if asset['asset_id'] == asset_id:
            found = True
            print(f"\nCurrent details:")
            print(f"  Device: {asset['device_type']} ({asset['hostname']})")
            print(f"  Current Status: {asset['status']}")
            print(f"  Assigned User: {asset['assigned_user']}")

            new_status = input("\nEnter new status (Active, In Storage, Retired, Repair): ").strip()

            if not new_status:
                print("✗ No status entered. Update cancelled.")
                return False

            asset['status'] = new_status
            asset['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

    if not found:
        print(f"✗ Asset ID '{asset_id}' not found.")
        return False

    # Write back to CSV
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(assets)

    print(f"\n✓ Asset {asset_id} status updated to: {new_status}")
    return True

def export_report():
    """Export a summary report to a text file."""
    print("\n" + "=" * 50)
    print("EXPORT REPORT")
    print("=" * 50)

    if not os.path.exists(CSV_FILE):
        print("✗ No inventory file found.")
        return None

    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        assets = list(reader)

    if not assets:
        print("No assets to export.")
        return None

    report_file = f"asset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(report_file, mode='w', encoding='utf-8') as file:
        file.write("=" * 60 + "\n")
        file.write("ASSET INVENTORY REPORT\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 60 + "\n\n")

        # Summary statistics
        status_counts = {}
        dept_counts = {}
        device_counts = {}

        for asset in assets:
            status = asset['status']
            dept = asset['department']
            device = asset['device_type']

            status_counts[status] = status_counts.get(status, 0) + 1
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
            device_counts[device] = device_counts.get(device, 0) + 1

        file.write("SUMMARY STATISTICS\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Assets: {len(assets)}\n\n")

        file.write("By Status:\n")
        for status, count in sorted(status_counts.items()):
            file.write(f"  {status}: {count}\n")

        file.write("\nBy Department:\n")
        for dept, count in sorted(dept_counts.items()):
            file.write(f"  {dept}: {count}\n")

        file.write("\nBy Device Type:\n")
        for device, count in sorted(device_counts.items()):
            file.write(f"  {device}: {count}\n")

        file.write("\n" + "=" * 60 + "\n")
        file.write("FULL ASSET LISTING\n")
        file.write("=" * 60 + "\n\n")

        for asset in assets:
            file.write(f"Asset ID: {asset['asset_id']}\n")
            file.write(f"  Device Type: {asset['device_type']}\n")
            file.write(f"  Hostname: {asset['hostname']}\n")
            file.write(f"  Operating System: {asset['operating_system']}\n")
            file.write(f"  Assigned User: {asset['assigned_user']}\n")
            file.write(f"  Department: {asset['department']}\n")
            file.write(f"  Location: {asset['location']}\n")
            file.write(f"  Purchase Date: {asset['purchase_date']}\n")
            file.write(f"  Warranty Expiry: {asset['warranty_expiry']}\n")
            file.write(f"  Status: {asset['status']}\n")
            file.write(f"  Notes: {asset['notes']}\n")
            file.write(f"  Last Updated: {asset['last_updated']}\n")
            file.write("\n")

    print(f"✓ Report exported to: {report_file}")
    print(f"  Total assets in report: {len(assets)}")

    return report_file

def main_menu():
    """Display main menu and handle user input."""
    print("\n" + "=" * 50)
    print("PYTHON ASSET INVENTORY TOOL")
    print("=" * 50)
    print("Track devices, OS, users, and asset status")
    print("=" * 50)

    initialize_inventory()

    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Add New Asset")
        print("2. View All Assets")
        print("3. Search Assets")
        print("4. Update Asset Status")
        print("5. Export Report")
        print("6. Exit")
        print("=" * 50)

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == '1':
            add_asset()
        elif choice == '2':
            view_all_assets()
        elif choice == '3':
            search_assets()
        elif choice == '4':
            update_asset_status()
        elif choice == '5':
            export_report()
        elif choice == '6':
            print("\n✓ Exiting Asset Inventory Tool. Goodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n✓ Interrupted. Exiting...")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("Please check your inventory file and try again.")
