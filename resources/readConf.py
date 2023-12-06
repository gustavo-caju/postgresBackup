import yaml
from .log import logInfo, logRecord

class validateConfException(Exception):
    def __init__(self, message):
        super().__init__(message)


# first function to be executed
@logInfo
def readConf(confFile):
    return validateFile(confFile)

# second function to be executed
@logInfo
def validateFile(confFile):  # this functions validates the confFile
    try:
        with open(confFile, 'r') as yamlFile:
            conf = yaml.safe_load(yamlFile)
        return validateConf(confFile, conf)
    except yaml.YAMLError as e:
        message = f'Syntax error in {confFile} File - {e}'
        logRecord('critical', message)
        exit(1)

    except FileNotFoundError as e:
        message = f'Conf File not Found - {e}'
        logRecord('critical', message)
        exit(1)

    except Exception as e:
        message = f'An error occurred when open {confFile} file - {e}'
        logRecord('critical', message)
        exit(1)

# last function to be executed
@logInfo
def validateConf(confFile, conf):  # this functions validates each confFile parameters
    newConf = {}
    try:
        # configuration check - database
        db = conf.get('database')
        if db:
            dbParameters = ['host', 'port', 'user', 'pass']
            if all(key in db for key in dbParameters): newConf['database'] = db
            else: raise validateConfException(f'some parameter is missing in \'database\'')
        else: raise validateConfException('\'Database\' parameter is missing')

        # configuration check - zip
        zip = conf.get('zipPass')
        if zip:
            newConf['zipPass'] = zip
        else:
            message = f'\'zipPass\' parameter is not defined. Compression will not be performed'
            logRecord('warning', message)
            newConf['zipPass'] = ''

        # configuration check - Retention
        retention = conf.get('retention')
        if retention: newConf['retention'] = retention
        else:
            newConf['retention'] = 5
            message = f'Retention Time no defined. Default value set to 5'
            logRecord('warning', message)

        # configuration check - environment
        environment = conf.get('environment')
        if environment: newConf['environment'] = environment
        else: raise validateConfException('Environment parameter is missing')

        # configuration check - notifier  ### disabled for now
        notify = conf.get('notify')
        if notify:
            if notify.get('channel') and notify.get('token'): newConf['notify'] = notify
            else: raise validateConfException('notify: \'channel\' or \'token\' parameter is missing')
        else:
            message = f'Notify parameter is not defined'
            logRecord('warning', message)
            newConf['notify'] = None

        # configuration check - crypt
        crypt = conf.get('crypt')
        if crypt: newConf['crypt'] = crypt
        else:
            newConf['crypt'] = 'MmBH8#Xx'
            message = f'Crypt password is not defined. Default value was set'
            logRecord('warning', message)

        # configuration check - process
        process = conf.get('process')
        if process:
            newConf['process'] = int(process)
        else:
            newConf['process'] = 4
            message = f'NUmber of process was nor defined. Default value was set to 4'
            logRecord('warning', message)

        # configuration check - zabbix
        zabbix = conf.get('zabbix')
        if zabbix:
            parameters = ['server', 'host', 'port']
            if all(key in zabbix for key in parameters):
                newConf['zabbix'] = zabbix
            else:
                newConf['zabbix'] = None
                message = f'\'Zabbix\' some parameters are missing.'
                logRecord('warning', message)
        else:
            newConf['zabbix'] = None
            message = f'\'Zabbix\' was not defined.'
            logRecord('warning', message)

        return newConf
    except (Exception, validateConfException) as e:
        message = f'Wrong or missing Parameter in \'{confFile}\' - {e}'
        print(message)
        logRecord('critical', message)
        exit(1)



