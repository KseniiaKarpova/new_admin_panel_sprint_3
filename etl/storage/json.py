import json
import os
from typing import Any, Dict

from storage.base import BaseStorage


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        # сравниваем с текущим состоянием
        current_state = self.retrieve_state()
        if json.dumps(current_state) == json.dumps(state):
            pass
        else:
            # сохраняем новое соостояние
            with open(self.file_path, 'w') as f:
                json.dump(state, f)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as myfile:
                data = myfile.read()
            return json.loads(data)
        return {}
