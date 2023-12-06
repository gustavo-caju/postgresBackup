from subprocess import run, CalledProcessError
from .log import logRecord
from datetime import datetime
from . import bkpFolder, confDatabase, makedirs

date = datetime.now().strftime('%y-%m-%d--%H-%M')

# @logInfo
def performDump(base): # base is a dictionary with connect informations
    db = base.get('base')
    host = base.get('host')
    port = base.get('port')
    user = base.get('user')
    password = base.get('pass')

    makedirs(f'{bkpFolder}/{db}/', exist_ok=True)  # get backups folder from confFile. __init__ file
    backupFile = f'{bkpFolder}/{db}/{db}__{date}.backup'
    command = ['pg_dump', f'--dbname=postgresql://{user}:{password}@{host}:{port}/{db}', '-f', backupFile, '-Fc']

    try:
        message = f'\'{db}\' Starting dump'
        logRecord('debug', message)
        run(command, check=True, text=True, shell=False)
        return str(backupFile)  # it returns a path to the backup file
    except (Exception, CalledProcessError) as e:
        message = f'An error occurred while dumping the \'{db}\' base backup - {e}'
        logRecord('error', message)
        return False
