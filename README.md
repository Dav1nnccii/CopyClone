Python File: copy_files.py
Author     : Damien Keffyn
Company    : Sentinal IT
Date       : September 26, 2024

Description: This script allows the user to select a source 
             and destination directory, and recursively copies 
             all files and folders from the source to the destination, 
             ignoring hidden files and folders. It also skips files 
             that result in access errors (e.g., Access Denied).

Features:
    - Ignores hidden files and folders during the copy operation.
    - Skips files that cause access errors and continues copying.
    - Maintains the directory structure from the source to the destination.
    - Uses os.walk() to recursively walk through directories.
    - Cross-platform compatibility for Windows and Unix-like systems.

Usage:
    1. Run the script using Python.
    2. Enter the source and destination directories when prompted.
    3. The script will display the status of each file being copied.
