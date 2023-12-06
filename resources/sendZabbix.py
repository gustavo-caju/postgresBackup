from pyzabbix import ZabbixMetric, ZabbixSender
from .log import logRecord
from json import dumps
from logging import getLogger

def sendZabbix(backups, confZabbix):  # backups is a backup list

    getLogger('pyzabbix').propagate = False  # Cancel logging from zabbix
    server = str(confZabbix.get('server'))
    port = int(confZabbix.get('port'))
    host = str(confZabbix.get('host'))

    message = f'Sending zabbix metric'
    logRecord('info', message)
    try:
        sender = ZabbixSender(server, port)
        metric = [ZabbixMetric(host, 'bkp.pg.backups', dumps(backups))]
        sender.send(metric)

    except Exception as e:
        message = f'An error occurred while sending zabbix metrics - {e}'
        logRecord('info', message)
