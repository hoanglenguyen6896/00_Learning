#
import os
# Move file
import shutil

import send2trash

if __name__ == '__main__':

    os.system('dir')

    #f = open("practice.txt", "w+")
    #f.write("This is a test string")
    #f.close()

    print('>>>>>>>>>> Current working directory <<<<<<<<<<')
    print(os.getcwd())
    print('---------- Iten in current working directory: ')
    print(os.listdir())

    # Move file
    # shutil.move("src", "dest that you have permission")

    # shutil.move("practice.txt","D:\\Libraries\\Documents\\Python\\13_Generators\\")
    # shutil.move("D:\\Libraries\\Documents\\Python\\13_Generators\\practice.txt",
    #                                                       os.getcwd())

    # Delete a file
    """
    1. os.unlink("path of file") > Delete 1 file
    2. os.rmdir("path") > Delete 1 empty folder
    3. os.rmtree("path") > Delete all file and folder *CAN'T BE REVERSED*

    Use send to trash (pip install send2trash) to delete safer
    """

    # send2trash.send2trash('practice.txt')

    print('---------- Iten in current working directory: ')
    print(os.listdir())

    # os.walk("path"): show all file, sub-folder in file, sub-folder of path
    for folder, sub_folder, files in os.walk("D:\\Libraries\\Documents\\Python"):
        print(f"Currently looking at {folder}")
        print('\nThe sub-directories are: ')
        for sub_fold in sub_folder:
            print(f"\tSubfolder: {sub_fold}")
        print('\nThe files are: ')
        for f in files:
            print(f"\tSubfolder: {f}")