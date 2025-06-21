import os
import json
from data_paths.path_provider import PathProvider

class ResultLogger:
    def __init__(self, path_provider: PathProvider):
        self.path_provider = path_provider

    def save_to_json(self, result_data: dict, month: int, year: int):
        result_path = self.path_provider.getResultsPath(month, year)
        existing_data = []

        if os.path.exists(result_path):
            try:
                with open(result_path, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []

        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        existing_data.append(result_data)

        with open(result_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, separators=(',', ': '), ensure_ascii=False)