def backtestConfigs () :
    seperateMoney = 150
    profitLoss = 0
    portion = 1
    messages = []
    entryMoney = 12000
    return seperateMoney , profitLoss , portion , messages , entryMoney

years = [2020,2021,2022,2023,2024]
months = [1,2,3,4,5,6,7,8,9,10,11,12]

def fixedMonths(month,year) :
    if month < 10 :
        date = f"BTCUSDT-15m-{year}-0{month}"
        date1s = f"BTCUSDT-1s-{year}-0{month}"
    else :
        date = f"BTCUSDT-15m-{year}-{month}"  
        date1s = f"BTCUSDT-1s-{year}-{month}"
    datas15m = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\15m\\{date}\\{date}.csv"  
    resultscsv = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\results\\01results{date}.csv"
    csv1s = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\1s\\{date1s}\\{date1s}.csv"
    parquet1s = f"C:\\Users\\ERDO\\Desktop\\emaCrossStrategyBacktest\\backTestDatas\\datas\\BTC\\1s\\{date1s}\\{date1s}.parquet"

    return datas15m , resultscsv , csv1s , parquet1s
