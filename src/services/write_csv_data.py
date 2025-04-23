import json
import os
from data_paths.path_provider import PathProvider

class WriteCsvData:
    def __init__(self, path_provider:PathProvider):
        self.path_provider = path_provider()

    def writeCsv(self, resultData, month, year):
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

        existing_data.append(resultData)

        with open(result_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, separators=(',', ': '), ensure_ascii=False)