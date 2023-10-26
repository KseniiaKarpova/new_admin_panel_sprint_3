import uuid
from typing import List, Union

from pydantic import BaseModel


class Person(BaseModel):
    id: uuid.UUID
    name: str


class Movie(BaseModel):
    id: uuid.UUID
    imdb_rating: Union[float, None] = None
    genre: List
    title: str
    description: str
    director: str
    actors_names: str
    writers_names: str
    actors: List[Person]
    writers: List[Person]
