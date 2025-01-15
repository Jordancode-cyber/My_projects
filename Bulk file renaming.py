import os

def rename_files(folder_path, prefix):
    for count, filename in enumerate(os.listdir(folder_path), start = 1):
        old_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_path):
            extension = os.path.splitext(filename)[1]
            new_filename = f"{prefix}_{count}{extension}"
            new_path = os.path.join(folder_path, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed {filename} to {new_filename}")


folder_path = input("Enter the folder path: ")
prefix = input("Enter the prefix for renaming: ")
rename_files(folder_path, prefix)