FROM python
RUN apt update && \
    apt install --autoremove postgresql-client -y && \
    mkdir -p /backups/resources

COPY resources/ /backups/resources/
COPY main.py /backups

WORKDIR /backups
RUN pip install pyyaml psycopg2 slack_sdk py7zr py-zabbix
VOLUME /backups

CMD ["python3", "main.py"]