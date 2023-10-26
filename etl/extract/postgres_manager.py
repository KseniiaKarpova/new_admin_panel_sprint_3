from collections.abc import Generator
from typing import Dict, List

import psycopg2
from psycopg2.extras import DictCursor

from decorators import coroutine
from extract.scripts import SELECT_ALL, SELECT_LAST_UPDATE
from logger import logger
from settings import pg_settings


class PostgresConnector:

    settings = pg_settings.dict()

    def __init__(self):
        self.connection = None

    def open(self):
        logger.info('Open PG connection')
        self.connection = psycopg2.connect(**self.settings)
        return self.connection

    def close(self):
        logger.info('Close PG connection')
        if self.connection:
            self.connection.close()


class Postgres:

    def __init__(self, conn: PostgresConnector):
        self.conn = conn.open()

    def get_cursor_all(self):
        ''' Получение всех данных из Postgres '''
        logger.info('get_cursor_all')
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(SELECT_ALL)
        return cursor

    def get_cursor_last_update(self, last_updated):
        ''' Получение последних обновленнных данных '''
        logger.info(f'get_cursor_last_update = {last_updated}')
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(SELECT_LAST_UPDATE, (last_updated, last_updated, last_updated, last_updated, ))
        return cursor

    @coroutine
    def extract(self, next_node: Generator, cursor, size: int = 100) -> Generator[None, List[Dict], None]:
        while results := cursor.fetchmany(size=size):
            next_node.send(results)
