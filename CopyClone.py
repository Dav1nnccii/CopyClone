"""
-------------------------------------------------------
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

-------------------------------------------------------
"""


import os
import shutil
import fnmatch
import sys

# Function to check if a file or folder is hidden
def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    # On Windows, hidden files/folders have the hidden attribute.
    if sys.platform == 'win32':
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            return attrs & 2  # FILE_ATTRIBUTE_HIDDEN = 0x2
        except:
            return False
    else:
        # On Unix-like systems, hidden files/folders start with a dot (.)
        return name.startswith('.')

# Function to copy files and folders, ignoring hidden files/folders
def copy_files_and_folders(src, dst):
    for root, dirs, files in os.walk(src):
        # Remove hidden directories from the list so they are not traversed
        dirs[:] = [d for d in dirs if not is_hidden(os.path.join(root, d))]
        
        for file in files:
            # Skip hidden files
            if is_hidden(os.path.join(root, file)):
                continue

            # Construct full file path
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(root, src)
            dest_dir = os.path.join(dst, rel_path)

            # Create the destination directory if it doesn't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Copy file, handling "Access Denied" or other errors
            try:
                shutil.copy2(src_file, dest_dir)
                print(f"Copied: {src_file} to {dest_dir}")
            except PermissionError:
                print(f"Access Denied: {src_file}. Skipping...")
            except Exception as e:
                print(f"Error copying {src_file}: {e}")

# Main function to get user input and run the copy operation
def main():
    # Get source and destination from user
    src = input("Enter the source directory: ")
    dst = input("Enter the destination directory: ")

    # Check if source exists
    if not os.path.exists(src):
        print("Source directory does not exist.")
        return

    # Start the copying process
    print(f"Starting copy from {src} to {dst} (excluding hidden files and folders)...")
    copy_files_and_folders(src, dst)
    print("Copy operation completed.")

if __name__ == "__main__":
    main()
