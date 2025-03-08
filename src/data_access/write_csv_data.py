
import json
from candles_data_access import CandlesDataAccess
class WriteCsvData() :
    def __init__(self) :
        self.candles_data_access = CandlesDataAccess()
        

    def writeCsv(self, resultDatas , month , year): 
        resultscsv = self.candles_data_access.getResultsPath (self , month , year)
        with open(resultscsv, "w", encoding="utf-8") as json_file:
            json.dump(
                resultDatas,
                json_file,
                indent=4,
                separators=(",", ": "),
                ensure_ascii=False,
            )