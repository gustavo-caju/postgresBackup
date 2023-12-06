from .log import logInfo, logRecord
from . import confDatabase, confCrypt
from psycopg2 import connect, DatabaseError

@logInfo
def getBases():  # get information about backups from database
    try:
        conn = connect(
            host = confDatabase.get('host'),
            database = 'backup',
            user = confDatabase.get('user'),
            password = confDatabase.get('pass'),
            port = confDatabase.get('port'))
        cur = conn.cursor()
        # decrypt password
        cur.execute(f'select base, host, port, user, pgp_sym_decrypt(pass::BYTEA, \'{confCrypt}\', \'compress-algo=aes256\') as pass, ignore from bases order by base asc')
        return cur.fetchall()
    except (Exception, DatabaseError) as e:
        message = f'An error occurred while getting bases for backup - {e}'
        logRecord('critical', message)
        cur.close()
        conn.close()
        exit(1)
    finally:
        cur.close()
        conn.close()