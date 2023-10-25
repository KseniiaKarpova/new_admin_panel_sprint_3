from extract.postgres_manager import Postgres, PostgresConnector
from storage import STATE, KEY
from dotenv import load_dotenv
from transform import transform_movies
from load.elasticsearch.manager import ElasticExecutor, ElasticConnection


load_dotenv()

if __name__ == '__main__':
    # получаем дату, когда послений раз загружалии в ElasticSearch
    last_date = STATE.get_state(KEY)

    # Подключение к базе данных Postgres
    con = PostgresConnector()
    pg = Postgres(conn=con)
    es_conn = ElasticConnection()

    # Подлкючение к базе данных ElasticSearch
    es_conn.create_index('movies', 'movies.json')
    elactic = ElasticExecutor(client=es_conn)

    print('last_date = ', last_date)
    if last_date is None:
        # получаем все данные
        cursor = pg.get_cursor_all()
    else:
        # ищем последние обновленния
        cursor = pg.get_cursor_last_update(last_date)

    while True:
        load_coro = elactic.insert_movies()
        transformer_coro = transform_movies(next_node=load_coro)
        extract_coro = pg.extract(transformer_coro, cursor)
