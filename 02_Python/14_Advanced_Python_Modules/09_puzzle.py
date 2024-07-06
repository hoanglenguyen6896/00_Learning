import shutil
import os
'''
path = (r'C:\\Users\\hoangnl7\\Complete-Python-3-Bootcamp-master\\12-Advanced '
        r'Python Modules\\08-Advanced-Python-Module-Exercise\\'
        r'unzip_me_for_instructions.zip')
shutil.unpack_archive(path, 'puzzle_folder', 'zip') # can use path
'''
with open('puzzle_folder\\extracted_content\\Instructions.txt', 'r') as f:
    print(f.read())

import re

pattern_number = r'\d{3}-\d{3}-\d{4}'

print(re.search(pattern_number, '123-123-1423'))
print(re.search(pattern_number, '123-123-1423').group())

result = []

def search(file, pattern = pattern_number):
    f = open(file, 'r')
    text = f.read()
    if re.search(pattern, text):
        return re.search(pattern, text)
    else:
        return ''

for folder, sub_folder, files in os.walk(os.getcwd()
                                    + "\\puzzle_folder\\extracted_content"):
    for f in files:
        full_path = folder + '\\' + f

        result.append(search(full_path))

for r in result:
    if r != '':
        print(r.group())
    pass