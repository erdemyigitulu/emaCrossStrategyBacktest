import json
import os
from data_paths.candles_data_access import CandlesDataAccess

class WriteCsvData:
    def __init__(self):
        self.candles_data_access = CandlesDataAccess()

    def writeCsv(self, resultData, month, year):
        result_path = self.candles_data_access.getResultsPath(month, year)
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