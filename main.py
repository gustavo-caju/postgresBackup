from resources.log import logRecord
from resources.sqlCheckDatabase import checkDatabaseTable
from resources.sqlGetBackupBases import getBases
from resources.sqlRegisterBackup import registerBackup
from resources.sqlDeleteOldRecords import deleteOldRecords
from resources.deleteOldBackups import deleteOldBackups
from resources.performBackup import performBackup
from resources.performZip import performZip
from resources.sendZabbix import sendZabbix
from resources import confEnv, confZipPass, confProcess, confZabbix
from multiprocessing import Semaphore, Process, SimpleQueue


# To control the backup flow, a semaphore is used to limit the processes
def performBackup_semaphore(i, backups, resultQueue, semaphore):
    backup = backups[i] # the index to not lost sequences of backups
    with semaphore:
        result = performBackup(backup)
        resultQueue.put((i,result))

# To control the backup flow, a semaphore is used to limit the processes
def performZip_semaphore(i, file, resultQueue, confZipPass, semaphore):
    with semaphore:
        resultQueue.put((i, performZip(file, confZipPass)))



if __name__ == '__main__':
    message = f'Stating script of {confEnv}'
    logRecord('info', message)
    try:
        checkDatabaseTable() # check the database and its tables

        backups = []  # for each backup entry

        message = f'Stating dumping files'
        logRecord('info', message)
        for base in getBases():
            backupInfo = {}
            # below get each parameter from confFile
            backupInfo['base'] = base[0]
            backupInfo['host'] = base[1]
            backupInfo['port'] = base[2]
            backupInfo['user'] = base[3]
            backupInfo['pass'] = base[4]
            backupInfo['status'] = 0 if base[5] else None  # ignore table column
            backupInfo['zip'] = True if confZipPass else False
            backupInfo['path'] = None
            backupInfo['size'] = None
            backupInfo['date'] = None
            backups.append(backupInfo)

        resultQueue = SimpleQueue() # queue to control the processes
        semaphore = Semaphore(confProcess) # get limis from confFile
        processes = []  # to loop control of processes
        for i, backup in enumerate(backups):
            process = Process(target=performBackup_semaphore, args=(i,backups,resultQueue,semaphore))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        while not resultQueue.empty():   # goes through the entire queue to put the result in the backup list
            i, result = resultQueue.get()
            backup = backups[i]
            if isinstance(result, str):   # the function performBackup returns a string(path to backup) otherwise status
                backup['path'] = result
                backup['status'] = 1
            else: backup['status'] = result


        if confZipPass:  # if zip is set it will peform a compress
            processes = []
            resultQueue = SimpleQueue()
            for i, backup in enumerate(backups):
                if backup.get('status') == 1:
                    process = Process(target=performZip_semaphore, args=(i, backup.get('path'), resultQueue, confZipPass, semaphore))
                    processes.append(process)
                    process.start()
            for process in processes:
                process.join()
            while not resultQueue.empty():
                i, result = resultQueue.get()
                path = result
                if path: backups[i]['path'] = path
                else: backups[i]['status'] = 2


        for i, backupsToRegister in enumerate(backups):
            status = backupsToRegister.get('status')
            if status == 1 or status == 2:
                registerBackup(backupsToRegister)
                deletedRecords = deleteOldRecords(backupsToRegister.get('base'))  # delete records from database
                if deletedRecords:
                    deleteOldBackups(backupsToRegister.get('base'), deletedRecords)  # delete old backup files

        if confZabbix:
            sendZabbix(backups, confZabbix)

        message = f'Local\'Script is finished'
        logRecord('info', message)

    except Exception as e:
        message = f'An error occurred when execute main function - {e}'
        logRecord('critical', message)
        exit(1)
