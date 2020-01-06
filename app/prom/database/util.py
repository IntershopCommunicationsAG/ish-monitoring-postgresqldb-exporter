import logging
import socket

from flask import current_app as app
from packaging import version
from pg8000 import connect, DatabaseError, InterfaceError, OperationalError


LOGGER = logging.getLogger(__name__)


def is_port_open():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((app.config["HOST"], int(app.config["PORT"])))
        s.shutdown(2)
        return True
    except:
        return False

def get_connection():
    database = app.config["DATABASE"]
    host = app.config["HOST"]
    port = app.config["PORT"]
    user = app.config["USERNAME"]
    password = app.config["PASSWORD"]
    ssl = app.config["SSL"]

    try:
        conn = connect(database=database, ssl=ssl, host=host, port=port, user=user, password=password)
    except OperationalError:
        raise InterfaceError
    return conn

def get_version():
    rows = get_query_result(get_connection(), 'SHOW server_version')
    version = next(rows)
    return version.get('server_version')

def dbVersionCompare(v1, v2):
    if version.parse(v1) >= version.parse(v2):
        return True
    elif version.parse(v1) < version.parse(v2):
        return False

def get_query_result(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_name = [column[0].decode('UTF-8') for column in cursor.description]
        for row in result:
            yield dict(zip(column_name, row))
    except DatabaseError as e:
        LOGGER.error("Query: %s has error: %s", query, str(e))
