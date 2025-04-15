import os
    
class CandlesDataAccess:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    def getFileNamesWithDate(self, month, year):
        month_str = f"{month:02d}"
        date = f"BTCUSDT-15m-{year}-{month_str}"
        return date

    def get15mCsvPath(self, month, year):
        date = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "15m", date, f"{date}.csv"
        )
    
    def get1sCsvPath(self, month, year):
        _, date1s = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "1s", date1s, f"{date1s}.csv"
        )

    def get1sParquetPath(self, month, year):
        _, date1s = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "1s", date1s, f"{date1s}.parquet"
        )

    def getResultsPath(self, month, year):
        date, _ = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "results", f"01results{date}.csv"
        )
