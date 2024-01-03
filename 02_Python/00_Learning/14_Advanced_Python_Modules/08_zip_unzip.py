f = open("fileone.txt", "w+")
f.write('ONENENENENE')
f.close()

f = open("filetwo.txt", "w+")
f.write('TWOWOWOWOOWOW')
f.close()

# Method 1
# import zipfile

# # Create a zip file
# compress_file = zipfile.ZipFile('zip_comp.zip','w')
# compress_file.write('fileone.txt', compress_type = zipfile.ZIP_DEFLATED)
# compress_file.write('filetwo.txt', compress_type = zipfile.ZIP_DEFLATED)
# compress_file.close()

# # Unzip
# zip_object = zipfile.ZipFile('zip_comp.zip', 'r')
# zip_object.extractall('extracted_content') # Extract to folder extracted_content (create if does not exist)
# zip_object.close()

# Method 2
import shutil
output_file_name = 'example'
dir_to_zip = r'D:\\Libraries\\Documents\\Python\14_Advanced_Python_Modules\\extracted_content'
shutil.make_archive(output_file_name, 'zip', dir_to_zip)

shutil.unpack_archive('example.zip', 'final_unzip', 'zip') # can use path