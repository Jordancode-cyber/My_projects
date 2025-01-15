import os
import shutil

def clean_temp_folder():
    temp_folder = os.environ.get('TEMP')
    if temp_folder:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def clean_recycle_bin():
    recycle_bin = os.path.expandvars(r'$Recycle.Bin')
    for root, dirs, _ in os.walk(recycle_bin):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(dir_path, ignore_errors=True)
                print(f"Cleared: {dir_path}")
            except Exception as e:
                print(f"Error clearing {dir_path}: {e}")

print("Cleaning temporary files...")
clean_temp_folder()
print("Cleaning Recycle Bin...")
clean_recycle_bin()
print("Cleanup complete!")