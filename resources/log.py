import logging as log
from datetime import datetime

def createLogFile(logFolder):
    date = datetime.now().strftime('%Y-%m-%d--%H-%M')   # set time format
    logFile = f'{logFolder}/{date}.log'                 # create logfile
    try:
        log.basicConfig(
            # filename=str(logFile),
            level=log.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[log.StreamHandler(), log.FileHandler(logFile, encoding='UTF-8')])  # it sends logs to output and file
    except Exception as e:
        print(f'An error occurred while creating log file\n{e}')
        exit(1)

def logInfo(func):     # this function sends logs as INFO for default
    def wrapper(*args, **kwargs):
        log.info(f'Starting the {func.__name__} function')
        result = func(*args, **kwargs)
        log.info(f'Function {func.__name__} finished')
        return result
    return wrapper


def logRecord(level, message):   # this function sends logs to the previously defined logger
    logger = log.getLogger()
    level = str(level).lower()
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
