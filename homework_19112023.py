import os
import shutil
import sys

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            normalized_name = normalize(file)
            new_path = os.path.join(root, normalized_name)
            os.rename(file_path, new_path)

        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

def sort_files(folder_path):
    
    categories = ['images', 'documents', 'audio', 'video', 'archives']
    for category in categories:
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = file.split('.')[-1].upper()

            
            if file_extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                shutil.move(file_path, os.path.join(folder_path, 'images', file))
            elif file_extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                shutil.move(file_path, os.path.join(folder_path, 'documents', file))
            elif file_extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                shutil.move(file_path, os.path.join(folder_path, 'audio', file))
            elif file_extension in ['AVI', 'MP4', 'MOV', 'MKV']:
                shutil.move(file_path, os.path.join(folder_path, 'video', file))
            elif file_extension in ['ZIP', 'GZ', 'TAR']:
                
                archive_folder_path = os.path.join(folder_path, 'archives', file.replace('.', '_'))
                os.makedirs(archive_folder_path, exist_ok=True)
                shutil.unpack_archive(file_path, archive_folder_path)
                os.remove(file_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        return

    folder_path = sys.argv[1]

    process_folder(folder_path)
    sort_files(folder_path)

if __name__ == "__main__":
    main()