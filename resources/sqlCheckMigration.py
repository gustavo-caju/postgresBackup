from .log import logInfo, logRecord
from . import confDatabase
from psycopg2 import connect, DatabaseError
from time import sleep


def checkMigration(base):
    _base = base.get('base')
    _host = base.get('host')
    _port = base.get('port')
    _user = base.get('user')
    _pass = base.get('pass')
    try:
        conn = connect(
            host = _host,
            user = _user,
            password = _pass,
            port = _port,
            database = _base)
        cur = conn.cursor()
        # check if this base has a 'changelock'
        cur.execute('SELECT exists(SELECT * FROM pg_tables WHERE schemaname=\'public\' AND tablename=\'databasechangeloglock\');')
        tableLock = cur.fetchone()[0]

        if tableLock:
            conn = connect(
                host=_host,
                user=_user,
                password=_pass,
                port=_port,
                database=_base)
            cur = conn.cursor()
            counter = 1
            while counter < 6:  # if lock exists it going to try six times
                cur.execute('SELECT locked FROM databasechangeloglock;')
                result = cur.fetchone()[0]
                if result:
                    message = f'\'{_base}\' is locked. Attempt {counter} Waiting 60s...'
                    logRecord('warning', message)
                    sleep(60)
                    counter += 1
                else: return True
            return False

        # there is no tableLock
        else: return True

    except Exception as e:
        message = f'An error occurred when verify if Migration exists - {e}'
        logRecord('critical', message)
        cur.close()
        conn.close()
        return False
    finally:
        cur.close()
        conn.close()
