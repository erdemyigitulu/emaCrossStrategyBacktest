import os
    
class CandlesDataAccess:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


    def getFileNamesWithDate(self, month, year):
        month_str = f"{month:02d}"
        date = f"{year}-{month_str}"
        return date

    def get15mCsvPath(self, month, year):
        date = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "15m", f"BTCUSDT-15m-{date}", f"BTCUSDT-15m-{date}.csv"
        )
    
    def get1sCsvPath(self, month, year):
        date = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "1s", f"BTCUSDT-1s-{date}", f"BTCUSDT-1s-{date}.csv"
        )

    def get1sParquetPath(self, month, year):
        date = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "datas", "BTC", "1s", f"BTCUSDT-1s-{date}", f"BTCUSDT-1s-{date}.parquet"
        )

    def getResultsPath(self, month, year):
        date = self.getFileNamesWithDate(month, year)
        return os.path.join(
            self.BASE_DIR,
            "backTestDatas", "results", f"BTCUSDT-1s-{date}.csv"
        )
