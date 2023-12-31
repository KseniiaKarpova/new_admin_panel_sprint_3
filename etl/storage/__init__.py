import os

from storage.base import State
from storage.json import JsonFileStorage

KEY = "LAST_DATE_UPDATED"

STORAGE = JsonFileStorage(file_path=os.environ.get('PATH_JsonFileStorage'))
STATE = State(storage=STORAGE)
