from typing import List, Any
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import json
from backoff import on_exception, expo
from collections.abc import Generator
from decorators import coroutine, backoff_logger
from storage import STATE, KEY
from datetime import datetime


class ElasticConnection:

    def __init__(self):
        self.client = Elasticsearch(f"http://{os.environ.get('ES_HOST')}:{os.environ.get('ES_PORT')}/")

    def is_exist_index(self, index:str) -> bool:
        if self.client.indices.exists(index=index):
            return True
        else:
            return False

    def create_index(self, name, path_index) -> None:
        if not self.is_exist_index(index=name):
            path_index=os.path.join(os.path.dirname(os.path.abspath(__file__)), path_index)
            with open(path_index) as index_file:
                body = json.load(index_file)
                self.client.indices.create(index=name, body=body)


class ElasticExecutor:

    def __init__(self, client:ElasticConnection):
        self.client=client

    @on_exception(expo, Exception, logger=backoff_logger)
    @coroutine
    def insert_movies(self)-> Generator[None, List[Any], None]:
        while values := (yield):
            STATE.set_state(key=KEY, value=datetime.now().isoformat())
            print(STATE.get_state(KEY), len(values))
            bulk(self.client.client, values)