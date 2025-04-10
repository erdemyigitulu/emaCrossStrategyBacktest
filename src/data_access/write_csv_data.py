import json
import os
from data_access.candles_data_access import CandlesDataAccess

class WriteCsvData():
    def __init__(self):
        self.candles_data_access = CandlesDataAccess()

    def writeCsv(self, resultDatas, month, year):
        resultscsv = self.candles_data_access.getResultsPath(month, year)
        
        # Eğer dosya zaten varsa, mevcut verileri oku
        existing_data = []
        if os.path.exists(resultscsv):
            try:
                with open(resultscsv, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
            except json.JSONDecodeError:
                # Dosya boş veya geçersiz JSON formatında
                existing_data = []
        
        # Yeni verileri mevcut verilere ekle
        if isinstance(existing_data, list):
            existing_data.append(resultDatas)
        else:
            # Eğer mevcut veri bir liste değilse, yeni bir liste oluştur
            existing_data = [existing_data, resultDatas]
        
        # Tüm verileri dosyaya yaz
        with open(resultscsv, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)