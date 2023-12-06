from .log import logInfo, logRecord
from . import confDatabase
from psycopg2 import connect, DatabaseError


def checkDatabaseTable():
    checkDatabase()
    checkTables()

# checks if the 'backup' database exists
@logInfo
def checkDatabase():
    try:
        conn = connect(
            host = confDatabase.get('host'),
            user = confDatabase.get('user'),
            password = confDatabase.get('pass'),
            port = confDatabase.get('port'))
        cur = conn.cursor()
        cur.execute('SELECT 1 FROM pg_database WHERE datname = \'backup\'')
        result = cur.fetchone() is None # if it doesn't return anything it will be True
        if result: raise Exception('Backup Base doesn\'t exist!')

    except Exception as e:
        message = f'An error occurred when test database - {e}'
        logRecord('critical', message)
        cur.close()
        conn.close()
        exit(1)
    finally:
        cur.close()
        conn.close()

@logInfo
def checkTables():
    try:
        conn = connect(
            host = confDatabase.get('host'),
            user = confDatabase.get('user'),
            password = confDatabase.get('pass'),
            port = confDatabase.get('port'),
            database = 'backup')
        sqlCheckBases = 'select exists (SELECT 1 FROM information_schema.tables WHERE table_name = \'bases\' )'
        sqlCheckBackups = 'select exists (SELECT 1 FROM information_schema.tables WHERE table_name = \'backups\' )'
        cur = conn.cursor()
        cur.execute(sqlCheckBases)
        if not cur.fetchone()[0]: raise Exception('The "bases" table doesn\'t exist!')
        cur.execute(sqlCheckBackups)
        if not cur.fetchone()[0]: raise Exception('The "backups" table doesn\'t exist!')

    except Exception as e:
        message = f'An error occurred while checking tables in the database - {e}'
        logRecord('warning', message)
        cur.close()
        conn.close()
        logRecord('info','Trying to create Tables')
        createTables()
    finally:
        cur.close()
        conn.close()

@logInfo
def createTables():
    try:
        conn = connect(
            host=confDatabase.get('host'),
            user=confDatabase.get('user'),
            database='backup',  # backup is the backup base
            password=confDatabase.get('pass'),
            port=confDatabase.get('port'))
        cur = conn.cursor()
        with open('resources/sql/createTables.sql', 'r') as sql:
            cur.execute(str(sql.read()))
        conn.commit()
    except (Exception, DatabaseError) as e:
        message = f'An error occurred while crating tables in the database - {e}'
        logRecord('critical', message)
        cur.close()
        conn.close()
        exit(1)
    finally:
        cur.close()
        conn.close()
