import unicodedata
import os
import shutil
import sys

def normalize(s):
    # Транслітерація кириличних символів
    trans_table = {ord(c): None for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'}
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.translate(trans_table)
    # Заміна всіх символів, крім літер латинського алфавіту та цифр, на символ '_'
    s = ''.join([c if c.isalnum() or c.isspace() else '_' for c in s])
    return s


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            normalized_name = normalize(file)
            new_path = os.path.join(root, normalized_name)
            os.rename(file_path, new_path)

        # Видалення порожніх папок
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        return

    folder_path = sys.argv[1]
    
    # Додаткові операції можна розширити тут, наприклад, розпізнавання розширень та перенесення файлів у відповідні папки.
    # Реалізація цих операцій буде залежати від конкретних вимог.

    process_folder(folder_path)

if __name__ == "__main__":
    main()                