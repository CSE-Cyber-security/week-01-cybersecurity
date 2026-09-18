# Week 01 — Cybersecurity Asset Inventory System

## Overview
A command-line Python application that lets a security administrator manage an
organization's IT assets (workstations, servers, routers, switches, and applications).
It supports adding, searching, updating, deleting, and displaying assets, classifies
each one by risk level and security status, and prints a summary dashboard.

## Features
- **Add Asset** — Enter details for a new asset, with input validation on every field
  (unique Asset ID, valid IP address format, and restricted choices for Asset Type,
  Risk Level, and Security Status).
- **Search Asset** — Look up a single asset by Asset ID.
- **Update Asset** — Edit any field of an existing asset (press Enter to keep the
  current value for a field).
- **Delete Asset** — Remove an asset, with a y/n confirmation prompt.
- **Display All Assets** — Prints every asset in a formatted report, followed by a
  summary (total assets, critical assets, high-risk assets, medium-risk assets,
  vulnerable assets).
- **Data Persistence** — All changes are saved to `data/assets.json` immediately, so
  data survives across program runs.

## Folder Structure
```
Week-01-Cybersecurity-Asset-Inventory/
├── src/
│   └── asset_inventory.py     # Main program
├── data/
│   └── assets.json            # Stored asset data (sample data included)
├── tests/
│   └── test_cases.md          # Manual test cases and results
├── screenshots/                # Screenshots of each feature (add yours here)
└── README.md
```

## How to Run
1. Make sure Python 3 is installed (`python3 --version`).
2. Open a terminal in the project folder.
3. Run:
   ```
   python3 src/asset_inventory.py
   ```
4. Use the on-screen menu (1–6) to Add, Search, Update, Delete, Display, or Exit.

## Input Validation Rules
- **Asset ID**: required, and must be unique among existing assets.
- **Asset Name / OS / Department**: required, cannot be blank.
- **IP Address**: must match a valid `x.x.x.x` format (each octet 0–255).
- **Asset Type**: must be one of Workstation, Server, Router, Switch, Application.
- **Risk Level**: must be one of Low, Medium, High, Critical.
- **Security Status**: must be one of Secure, Warning, Vulnerable.

## Sample Data
`data/assets.json` is pre-loaded with the 3 sample assets from the assignment
(A101 – HR-PC-01, A102 – Web-Server, A103 – Core-Router) so the Display and
Search features can be demonstrated immediately.

## Author
Rupesh Rakesh — Second-year Cyber Security, S.A. Engineering College
