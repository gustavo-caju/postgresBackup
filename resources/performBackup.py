from .performDump import performDump
from .sqlCheckMigration import checkMigration
from .log import logRecord

def performBackup(base):  # base is dictionary
    '''
        status:
            0 - ignored
            1 - ok
            2 - Zip Failed
            3 - Locked - Migration
            4 - Dump Failed
    '''
    try:
        if base.get('status') == 0:
            message = f'the {base.get("base")} backup was ignored'
            logRecord('warning', message)
            return 0
        else:
            if checkMigration(base): # check if exists a migration, False means there is a locked
                backup = performDump(base) # performa a dump
                if backup:
                    return backup
                else:
                    message = f'the {base.get("base")} backup was not generated'
                    logRecord('error', message)
                    return 4 # dump failed
            else:
                message = f'\'{base.get("base")}\', skipping. There are migration in the database'
                logRecord('error', message)
                return 3 # Locked
    except (Exception) as e:
        message = f'An error occurred while performing Backup of {base.get("base")} - {e}'
        logRecord('critical', message)
        return False
