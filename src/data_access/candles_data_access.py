
class CandlesDataAccess:

    def getFileNamesWithDate(self , month, year):
        if month < 10:
            date = f"BTCUSDT-15m-{year}-0{month}"
            date1s = f"BTCUSDT-1s-{year}-0{month}"
        else:
            date = f"BTCUSDT-15m-{year}-{month}"
            date1s = f"BTCUSDT-1s-{year}-{month}"
        return date , date1s
        
    def get15mCsvPath(self , month , year):
        date , _ = self.getFileNamesWithDate(month , year)
        _15mCsvPath = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\15m\\{date}\\{date}.csv"
        return _15mCsvPath
    
    def get1sCsvPath(self , month , year) :
        print(month, year)
        _ , date1s = self.getFileNamesWithDate(month , year)
        _1sCsvPath = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\1s\\{date1s}\\{date1s}.csv"
        return _1sCsvPath
    
    def get1sParquetPath (self , month , year):
        _ , date1s = self.getFileNamesWithDate(month , year)
        _1sParquetPath = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\1s\\{date1s}\\{date1s}.parquet"
        return _1sParquetPath
    
    def getResultsPath (self , month , year):
        date , _ = self.getFileNamesWithDate(month , year)
        resultsCsvPath = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\results\\01results{date}.csv"
        return resultsCsvPath
    
    
    
