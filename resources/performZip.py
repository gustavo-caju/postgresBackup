from .log import logRecord
from py7zr import SevenZipFile
from os import remove

def performZip(file, confZipPass):  # file is the path to backup file
    fileZip = f'{file}.7z'
    try:
        with SevenZipFile(fileZip, 'w', password=confZipPass) as archive:
            logRecord('debug', f'Starting compression of the file {file}')
            archive.write(file)
        remove(file)  # remove old file. keep zip file only
        return fileZip  # returns the new path to the backup file, zipped file
    except Exception as e:
        message = f'An error occurred when performing the \'{file}\' file compression - {e}'
        logRecord('error', message)
        return False
