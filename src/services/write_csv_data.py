import json
import os
from data_paths.candles_data_access import CandlesDataAccess

class WriteCsvData():
    def __init__(self):
        self.candles_data_access = CandlesDataAccess()

    def writeCsv(self, resultDatas, month, year):
        resultscsv = self.candles_data_access.getResultsPath(month, year)
        existing_data = []
        if os.path.exists(resultscsv):
            try:
                with open(resultscsv, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
        if isinstance(existing_data, list):
            existing_data.append(resultDatas)
        else:
            existing_data = [existing_data, resultDatas]
        with open(resultscsv, 'w', encoding='utf-8') as json_file:
            json.dump(resultDatas, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)
