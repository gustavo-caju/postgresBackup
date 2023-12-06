from .log import createLogFile, logRecord
from os import makedirs

# Creating folders and log files
bkpFolder = '/backups/dump'
logFolder = '/backups/log'
makedirs(bkpFolder, exist_ok=True)
makedirs(logFolder, exist_ok=True)
createLogFile(logFolder)

# Configuration File
from .readConf import readConf
logRecord('info', 'Reading conf file')
confFile = readConf('conf.yaml')
confDatabase = confFile.get('database')         # Database Connect Information dict
confNotify = confFile.get('notify')             # messenger to notify it
confZipPass = confFile.get('zipPass')           # information to zip
confRetention = confFile.get('retention')
confEnv = confFile.get('environment')
confCrypt = confFile.get('crypt')
confProcess = confFile.get('process')
confZabbix = confFile.get('zabbix')

# initializing the notifier instance
# disabled for now
# from .notify import notify
# notifier = notify(confNotify)
