import os

from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    dbname: str = os.environ.get('PG_NAME')
    user: str = os.environ.get('PG_USER')
    password: str = os.environ.get('PG_PASSWORD')
    host: str = os.environ.get('PG_HOST')
    port: str = os.environ.get('PG_PORT')
    options: str = '-c search_path=content'


class ElasticsearchSettings(BaseSettings):
    host: str = os.environ.get('ES_HOST')
    port: str = os.environ.get('ES_PORT')


pg_settings = PostgresSettings()
es_settings = ElasticsearchSettings()
