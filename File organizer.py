import os
import shutil

def organize_files(folder_path):
    extensions = {
        'Images':['.jpg','.jpeg','.png','.gif'],
        'Documents':['.docx','.xlsx','.pdf','.txt','.pptx'],
        'Videos':['.mp4','.mkv','.avi'],
        'Audio':['.mp3','.wav'],
        'Archives':['.zip','.rar','.7z'],
        }

    for category, exts in extensions.items():
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok = True)

        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path)):
                if any(file.lower().endswitch(ext) for ext in exts):
                    shutil.move(os.path.join(folder_path, file), os.path.join(category_folder, file))
                    print(f"Moved {file} to {category}")

folder_path = input("Enter the folder path to organize: ")
organize_files(folder_path)