import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size +=  os.path.getsize(file_path)
    return total_size

def analyze_sizes(folder_path):
    for folder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(subfolder_path):
            size_in_mb = get_folder_size(subfolder_path) / (1024 * 1024)
            print(f"Folder: {folder_name} - Size: {size_in_mb:.2f} MB")

folder_path = input(f"Enter the folder path: ")
analyze_sizes(folder_path)