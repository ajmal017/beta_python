import os
import zipfile

def zip_file(directory_to_zip, zip_file):
    zf = zipfile.ZipFile(zip_file, "w")
    for dirname, subdirs, files in os.walk(directory_to_zip):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

def unzip_file(zip_file, extract_to):
    zf = zipfile.ZipFile(zip_file, 'r')
    zf.extractall(extract_to)
    zf.close()