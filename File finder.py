import os
from datetime import datetime


def find_files(folder_path, keyword):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if keyword.lower() in file.lower():
                file_path = os.path.join(root, file)
                print(f"Found: {file_path}")


folder_path = input("Enter the folder path: ")
keyword = input("Enter the keyword to search for: ")
find_files(folder_path, keyword)