"""
-------------------------------------------------------
Python File: copy_files.py
Author     : Damien Keffyn
Company    : Sentinal IT
Date       : September 26, 2024
Description: 
    This script allows the user to select a source 
    and destination directory, and recursively copies 
    all files and folders from the source to the destination, 
    ignoring hidden files and folders, skipping files that result 
    in access errors, and excluding specified file types. It 
    also logs each file operation and provides a progress bar for 
    large copy operations.

Features:
    - Ignores hidden files and folders during the copy operation.
    - Allows the user to exclude specific file types from being copied.
    - Logs copied files, skipped files, and errors into 'copy_log.txt'.
    - Displays a progress bar to indicate the progress of large operations.
    - Skips files that cause access errors and continues copying.
    - Maintains the directory structure from the source to the destination.
    - Uses os.walk() to recursively walk through directories.
    - Cross-platform compatibility for Windows and Unix-like systems.

Requirements:
    - Install the 'tqdm' library for the progress bar:
        pip install tqdm

Usage:
    1. Run the script using Python.
    2. Enter the source and destination directories when prompted.
    3. Optionally, enter file types (extensions) to exclude from the copy.
    4. The script will display a progress bar and log each operation 
       to 'copy_log.txt'.

-------------------------------------------------------
"""

import os
import shutil
import fnmatch
import sys
import logging
from tqdm import tqdm  # Progress bar library

# Set up logging
logging.basicConfig(filename='copy_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check if a file or folder is hidden
def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    if sys.platform == 'win32':
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            return attrs & 2  # FILE_ATTRIBUTE_HIDDEN = 0x2
        except:
            return False
    else:
        return name.startswith('.')

# Function to copy files and folders, ignoring hidden files/folders, and excluding certain file types
def copy_files_and_folders(src, dst, exclude_extensions):
    total_files = sum([len(files) for _, _, files in os.walk(src)])
    copied_files = 0

    # Initialize progress bar
    with tqdm(total=total_files, unit="file") as progress_bar:
        for root, dirs, files in os.walk(src):
            # Remove hidden directories from the list so they are not traversed
            dirs[:] = [d for d in dirs if not is_hidden(os.path.join(root, d))]

            for file in files:
                # Skip hidden files
                if is_hidden(os.path.join(root, file)):
                    logging.info(f"Skipped hidden file: {os.path.join(root, file)}")
                    continue

                # Skip files with excluded extensions
                if any(fnmatch.fnmatch(file, f"*.{ext}") for ext in exclude_extensions):
                    logging.info(f"Skipped excluded file type: {os.path.join(root, file)}")
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
                    logging.info(f"Copied: {src_file} to {dest_dir}")
                    copied_files += 1
                except PermissionError:
                    logging.error(f"Access Denied: {src_file}. Skipping...")
                except Exception as e:
                    logging.error(f"Error copying {src_file}: {e}")

                # Update progress bar
                progress_bar.update(1)

    print(f"Copied {copied_files} files out of {total_files}. Check 'copy_log.txt' for details.")

# Main function to get user input and run the copy operation
def main():
    # Get source and destination from user
    src = input("Enter the source directory: ")
    dst = input("Enter the destination directory: ")

    # Check if source exists
    if not os.path.exists(src):
        print("Source directory does not exist.")
        return

    # Ask the user for file extensions to exclude
    exclude_extensions = input("Enter file extensions to exclude (comma-separated, e.g., 'exe,sys,tmp'): ")
    exclude_extensions = [ext.strip() for ext in exclude_extensions.split(',')]

    # Start the copying process
    print(f"Starting copy from {src} to {dst} (excluding hidden files and folders)...")
    logging.info(f"Starting copy operation from {src} to {dst}")
    copy_files_and_folders(src, dst, exclude_extensions)
    print("Copy operation completed.")

if __name__ == "__main__":
    main()
