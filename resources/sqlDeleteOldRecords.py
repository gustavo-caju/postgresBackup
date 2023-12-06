from .log import logRecord
from psycopg2 import connect, DatabaseError
from . import confRetention, confDatabase


def deleteOldRecords(base):
    sqlFile = 'resources/sql/deleteOldRecords.sql'
    try:
        with open(sqlFile, 'r') as sql:
            sql = sql.read()
        substitutions = {
            '_base': base,
            '_retention': confRetention}
        for w, sub in substitutions.items():
            sql = sql.replace(str(w), str(sub))  # replace variables in the sql file

        try:
            conn = connect(
                host=confDatabase.get('host'),
                database='backup',
                user=confDatabase.get('user'),
                password=confDatabase.get('pass'),
                port=confDatabase.get('port'))
            cur = conn.cursor()
            logRecord('debug', f'\'{base}\' Delete Old Records')
            cur.execute(sql)
            conn.commit()
            deleted = [ record[3] for record in cur.fetchall()]  # get only database path column
            return deleted  # returns a paths list
        except (DatabaseError, Exception) as e:
            message = f'An error occurred when execute \'{sqlFile}\' sql file - {e}'
            logRecord('Error', message)
            cur.close()
            conn.close()
            return False
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        message = f'An error occurred when read \'{sqlFile}\' file - {e}'
        logRecord('error', message)
        return False
