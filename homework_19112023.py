import os
import shutil
import unicodedata
import sys 


def my_normalize(s):
    # Транслітерація кириличних символів
    trans_table = {ord(c): None for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'}
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.translate(trans_table)
    # Заміна всіх символів, крім літер латинського алфавіту та цифр, на символ '_'
    s = ''.join([c if c.isalnum() or c.isspace() else '_' for c in s])
    return s


def get_file_extension(file_name):
    _, extension = os.path.splitext(file_name)
    return extension[1:].upper()  # Видаляємо крапку перед розширенням


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        # Ігноруємо папки archives, video, audio, documents, images
        dirs[:] = [d for d in dirs if d.lower() not in {'archives', 'video', 'audio', 'documents', 'images'}]

        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Перейменовуємо файли та папки
            normalized_name = my_normalize(file_name)
            os.rename(file_path, os.path.join(root, normalized_name))

            # Визначаємо розширення та обробляємо файл відповідно
            extension = get_file_extension(normalized_name)
            process_file(file_path, extension)


def process_file(file_path, extension):
    # Створюємо папки за категоріями, якщо їх не існує
    categories = {'JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                  'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR',
                  'ZIP', 'GZ', 'TAR'}
    if extension in categories:
        category_folder = extension.lower()
    else:
        category_folder = 'unknown'
    
    category_path = os.path.join(os.path.dirname(file_path), category_folder)
    os.makedirs(category_path, exist_ok=True)

    # Переміщуємо файли в категорії
    shutil.move(file_path, os.path.join(category_path, os.path.basename(file_path)))


def create_backup(path):
    archive_name = shutil.make_archive('backup_folder', 'zip', path)
    return archive_name


def unpack(archive_path, path_to_unpack):
    shutil.unpack_archive(archive_path, path_to_unpack)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)