# Test Cases — Cybersecurity Asset Inventory System

| # | Test Case | Input | Expected Output | Result |
|---|-----------|-------|------------------|--------|
| 1 | Add a valid asset | Menu 1 → A101, HR-PC-01, Workstation, 192.168.1.10, Windows 11, HR, Medium, Secure | "Asset 'A101' added successfully." | Pass |
| 2 | Add asset with duplicate Asset ID | Menu 1 → A101 (already exists) | Error: "Asset ID 'A101' already exists. Please enter a unique ID." — re-prompts | Pass |
| 3 | Add asset with invalid IP address | IP Address → 999.999.1.1 | Error: "Invalid IP address format." — re-prompts | Pass |
| 4 | Add asset with invalid Asset Type | Asset Type → "Laptop" | Error listing valid options — re-prompts | Pass |
| 5 | Add asset with empty required field | Asset Name → "" (blank) | Error: "This field cannot be empty." — re-prompts | Pass |
| 6 | Display all assets | Menu 5 | Formatted list of all assets + summary counts | Pass |
| 7 | Display with no assets | Menu 5 (empty inventory) | "No assets found." + summary showing all zeros | Pass |
| 8 | Search for existing Asset ID | Menu 2 → A102 | Displays matching asset's full details | Pass |
| 9 | Search for non-existent Asset ID | Menu 2 → A999 | "No asset found with ID 'A999'." | Pass |
| 10 | Update an existing asset (change one field) | Menu 3 → A102, new Security Status = Warning, rest blank | "Asset 'A102' updated successfully." Only status changes | Pass |
| 11 | Update non-existent asset | Menu 3 → A999 | "No asset found with ID 'A999'." | Pass |
| 12 | Delete an existing asset with confirmation | Menu 4 → A102 → y | "Asset 'A102' deleted successfully." | Pass |
| 13 | Delete cancelled by user | Menu 4 → A102 → n | "Delete cancelled." — asset remains | Pass |
| 14 | Delete non-existent asset | Menu 4 → A999 | "No asset found with ID 'A999'." | Pass |
| 15 | Invalid menu choice | Menu → 9 | "Invalid input. Please enter a number between 1 and 6." — re-prompts | Pass |
| 16 | Data persistence across runs | Add asset → exit → relaunch program | Previously added asset still present (loaded from assets.json) | Pass |
| 17 | Summary counts accuracy | 3 assets: 1 Critical, 1 High, 1 Medium, 1 Vulnerable | Summary line counts match exactly | Pass |

## How these were tested
Each test case was run manually via the terminal by launching `python3 src/asset_inventory.py`
and entering the inputs listed above, then comparing the printed output against the
"Expected Output" column. Screenshots of each core feature are in the `screenshots/` folder.
