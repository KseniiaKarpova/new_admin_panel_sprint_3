import json
import os
from collections.abc import Generator
from datetime import datetime
from typing import Any, List

from backoff import expo, on_exception
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from decorators import coroutine
from settings import es_settings
from storage import KEY, STATE


class ElasticConnection:

    def __init__(self):
        self.client = Elasticsearch(f"http://{es_settings.host}:{es_settings.port}/")

    def is_exist_index(self, index: str) -> bool:
        if self.client.indices.exists(index=index):
            return True
        else:
            return False

    def create_index(self, name, path_index) -> None:
        if not self.is_exist_index(index=name):
            path_index = os.path.join(os.path.dirname(os.path.abspath(__file__)), path_index)
            with open(path_index) as index_file:
                body = json.load(index_file)
                self.client.indices.create(index=name, body=body)

    def close(self):
        self.client.transport.close()


class ElasticExecutor:

    def __init__(self, client: ElasticConnection):
        self.client = client

    @on_exception(expo, Exception)
    @coroutine
    def insert_movies(self) -> Generator[None, List[Any], None]:
        while values := (yield):
            STATE.set_state(key=KEY, value=datetime.now().isoformat())
            bulk(self.client.client, values)
