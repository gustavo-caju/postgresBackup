from os import remove
from .log import logRecord

def deleteOldBackups(base, backups):
    try:
        logRecord('debug', f'\'{base}\' Removing old backups')
        for backup in backups:  # backups is a list of files path
            remove(backup)
    except Exception as e:
        message = f'An error occurred while removing old backups = {e}'
        logRecord('error', message)