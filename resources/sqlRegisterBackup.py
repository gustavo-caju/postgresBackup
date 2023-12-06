from .log import logInfo, logRecord
from psycopg2 import connect, DatabaseError
from . import confDatabase
def registerBackup(backup):
    sqlFile = 'resources/sql/registerBackup.sql'
    try:
        with open(sqlFile, 'r') as sql:
            sql = sql.read()
        sql = sql.replace('_base', backup.get('base'))
        sql = sql.replace('_host', backup.get('host'))
        sql = sql.replace('_port', backup.get('port'))
        sql = sql.replace('_path', backup.get('path'))
        try:
            conn = connect(
                host=confDatabase.get('host'),
                database='backup',
                user=confDatabase.get('user'),
                password=confDatabase.get('pass'),
                port=confDatabase.get('port'))
            cur = conn.cursor()
            cur.execute(sql)
            message = f'\'{backup.get("base")}\' Registering Backup'
            logRecord('Debug', message)
            conn.commit()
        except (DatabaseError, Exception) as e:
            message = f'An error occurred when execute \'{sqlFile}\' sql file - {e}'
            logRecord('Error', message)
            cur.close()
            conn.close()
    except Exception as e:
        message = f'An error occurred when read \'{sqlFile}\' file - {e}'
        logRecord('error', message)
    finally:
        cur.close()
        conn.close()
