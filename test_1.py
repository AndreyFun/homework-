import os
import fractions
import shutil
import re


def normalize(name):
    name = translit(name, 'ru', reversed=True)  # Транслітерація кирилиці
    name = re.sub(r'[^a-zA-Z0-9_.]', '_', name)  # Заміна всіх символів, крім літер та цифр, на підкреслення
    return name

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            normalized_file_name = normalize(file)
            
            # Визначаємо категорію файлу за розширенням
            extension = file.split('.')[-1].upper()

            if extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                category = 'images'
            elif extension in ['AVI', 'MP4', 'MOV', 'MKV']:
                category = 'video'
            elif extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                category = 'documents'
            elif extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                category = 'audio'
            elif extension in ['ZIP', 'GZ', 'TAR']:
                category = 'archives'
                # Розпаковуємо архів
                archive_path = os.path.join(root, file)
                extract_folder = os.path.join(folder_path, 'archives', normalized_file_name)
                shutil.unpack_archive(archive_path, extract_folder)
            else:
                category = 'unknown'

            # Створюємо папку для категорії, якщо вона не існує
            category_path = os.path.join(folder_path, category)
            os.makedirs(category_path, exist_ok=True)

            # Переміщуємо файл в відповідну категорію
            new_file_path = os.path.join(category_path, normalized_file_name)
            shutil.move(file_path, new_file_path)

    # Видаляємо порожні папки
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

def main():
    target_folder = '/your/target/folder/path'  # Шлях до цільової папки
    process_folder(target_folder)

if __name__ == "__main__":
    main()