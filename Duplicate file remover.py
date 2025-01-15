import os
import hashlib

def calculate_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def remove_duplicates(folder_path):
    seen_hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)

            if file_hash in seen_hashes:
                os.remove(file_path)
                print(f"Removed duplicate: {file}")
            else:
                seen_hashes[file_hash] = file_path


folder_path = input("Enter the folder path: ")
remove_duplicates(folder_path)

#Modify to scan folders on pc not folder path

