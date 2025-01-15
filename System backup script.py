import os
import shutil
from datetime import datetime

def backup_folder(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join(destination, backup_name)
    
    shutil.make_archive(backup_path[:-4], 'zip', source)
    print(f"Backup created: {backup_path}")

source = input("Enter the folder path to back up: ")
destination = input("Enter the backup destination path: ")
backup_folder(source, destination)