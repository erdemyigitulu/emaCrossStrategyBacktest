import csv
import numpy as np
from data_access.candles_data_access import CandlesDataAccess
from services.calculator_service import CalculaterService
from config import Config


class DataProcessor :

    def __init__(self):
        self.candles_data_access = CandlesDataAccess()
        self.config = Config()
        self.calculator_service = CalculaterService

    def getData(self , month , year):
        path15m = self.candles_data_access.get15mCsvPath(month , year)
        with open(path15m) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=",")
            closeTimeDatas = []
            openTimeDatas = []
            candleDatas = []
            for row in csvReader:
                candle = row
               # openTimeData = {
               #     "timeStamp": int(row[0]),
               #     "openTime": float(row[1])
               # }
                closeTimeData = {
                    "timeStamp": int(row[0]),
                    "closeTime": float(row[4])
                }
                closeTimeDatas.append(closeTimeData)
                #openTimeDatas.append(openTimeData)
                candleDatas.append(candle)
            csv_file.close()
            return openTimeDatas, candleDatas , closeTimeDatas
    
    def __getEmaValues (self , closeTimeDatas):
        emaDatasOfDays = []
        daysOfEma = self.config.daysOfEma
        for day in daysOfEma:
            emaDataOfDay = self.calculator_service.calculateEma(closeTimeDatas, day)
            emaDatasOfDays.append(emaDataOfDay)
        return emaDatasOfDays
    
    def datasOfEmaValues(self, closeTimeDatas, candles):
        emaValues = self.__getEmaValues(closeTimeDatas)
        ema5List = emaValues[0]
        ema8List = emaValues[1]
        ema13List = emaValues[2]
        minSize = min(len(ema5List), len(ema8List), len(ema13List))
        ema5List = ema5List[-minSize:]
        ema8List = ema8List[-minSize:]
        ema13List = ema13List[-minSize:]
        zipList = zip(ema5List, ema8List, ema13List)
        lastTimeStamp = int(candles[-1][0])
        timeStampgap = int(candles[-1][0]) - int(candles[-2][0])
        firstTimeStamp = lastTimeStamp - ((minSize * timeStampgap) - timeStampgap)
        emaValues = []
        for arrange in zipList:
            emaData = {
                "timestamp": firstTimeStamp,
                "ema5": arrange[0],
                "ema8": arrange[1],
                "ema13": arrange[2],
            }
            firstTimeStamp = firstTimeStamp + timeStampgap
            emaValues.append(emaData)
        del emaValues[:50]
        return emaValues
    
    def checkFirstSignalOfPosition (self , emaValues ) :
        for index , value in enumerate(emaValues) :
            ema5 = value["ema5"]
            ema8 = value["ema8"]
            ema13 = value["ema13"]
            emagap1 = ema8 - ema5 
            emagap2 = ema13 - ema5
            if emagap1 < 0 and emagap2 < 0 :
                whichSideOnSignal = ["long"]
                break
            elif emagap1 > 0 and emagap2 > 0 :
                whichSideOnSignal = ["short"]
                break
        if index != 0 :
            emaValues = emaValues[index:]
        return whichSideOnSignal , emaValues
    
    def getBuyPoints (self , signal , data1s):
        startProcessTimestamp = int(signal[1]) + 900000
        timestampColumn = data1s[:, 0]
        startIndex = np.argmax(timestampColumn >= startProcessTimestamp)
        entryPrice = data1s[startIndex][1]
        buyPoints = self.__findPurchasePoints(entryPrice, signal[0])
        return buyPoints , startIndex , entryPrice , startProcessTimestamp

    def __findPurchasePoints(self, entryPrice, signal):
        valuesList = []
        testValue = entryPrice
        buyCount = self.config.buyPointsCount
        for _ in range(int(buyCount)):
            nextPoint = entryPrice * int(self.config.buyPointsGap) / 100
            if signal == "long":                    
                pointValue = testValue - nextPoint
                valuesList.append(round(pointValue,2))
            else : 
                pointValue = testValue + nextPoint
                valuesList.append(round(pointValue,2))
            testValue = pointValue
        return valuesList