from collections.abc import Generator
from typing import Dict, List

from decorators import coroutine
from entities import Movie, Person


@coroutine
def transform_movies(next_node: Generator) -> Generator[None, List[Dict], None]:
    while movie_dicts := (yield):
        data = []
        # Преобразование данных
        for temp in movie_dicts:
            item = dict_to_movie(dict(temp))
            item = movie_to_es_data(item)
            data.append(item)
        next_node.send(data)


def dict_to_movie(temp: Dict) -> Movie:
    actors = [Person(id=x.get('person_id'), name=x.get('person_name')) for x in temp.get('persons') if
              x.get('person_role') == 'actor']
    writers = [Person(id=x.get('person_id'), name=x.get('person_name')) for x in temp.get('persons') if
               x.get('person_role') == 'writer']
    director = " ".join([x.get('person_name') for x in temp.get('persons') if x.get('person_role') == 'director'])
    item = Movie(
        id=temp.get('id'),
        title=temp.get('title'),
        description=temp.get('description') or '',
        imdb_rating=temp.get('rating'),
        genre=temp.get('genres'),
        director=director.strip(),
        actors_names=" ".join([person.name for person in actors]),
        writers_names=" ".join([person.name for person in writers]),
        actors=actors,
        writers=writers,
    )

    return item


def movie_to_es_data(movie: Movie, index='movies') -> Dict:
    es_data = {
        "_index": index,
        "_id": movie.id,
        "_source": {
            "id": movie.id,
            "imdb_rating": movie.imdb_rating,
            "title": movie.title,
            "description": movie.description,
            "genre": movie.genre,
            "director": movie.director,
            "actors_names": movie.actors_names,
            "writers_names": movie.writers_names,
            "actors": [dict(p) for p in movie.actors],
            "writers": [dict(p) for p in movie.writers],
        }
    }
    return es_data
