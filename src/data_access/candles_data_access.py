import time
import json
import csv


class CandlesDataAccess:
    def get15m(main15mcsv):
        with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            datas = []
            candleDatas = []
            for row in csv_reader:
                candle = row
                data = {
                    "timeStamp": int(row[0]),
                    "closeTime": float(row[4]),
                    "openTime": float(row[1]),
                }
                datas.append(data)
                candleDatas.append(candle)
            csv_file.close()
            return datas, candleDatas

    def getCloseTimes(candles):
        data = []
        for candle in candles:
            datas = {"timeStamp": candle["timeStamp"], "closeTime": candle["closeTime"]}
            data.append(datas)
        return data
