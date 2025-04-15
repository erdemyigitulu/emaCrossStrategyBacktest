import csv
import numpy as np
from data_paths.candles_data_access import CandlesDataAccess
from config.config import Config
from indicators.base_indicator import BaseIndicator
from indicators.exponantional_moving_average import ExponentialMovingAverageIndicator
from indicators.average_true_range import AverageTrueRangeIndicator


class DataProcessor :

    def __init__(self):
        self.candles_data_access = CandlesDataAccess()
        self.config = Config()

    def addIndicators(self, month, year):
        baseIndicator = BaseIndicator()
        emaIndicator = ExponentialMovingAverageIndicator()
        atrIndicator = AverageTrueRangeIndicator()
        baseIndicator.addIndicator(emaIndicator)
        baseIndicator.addIndicator(atrIndicator)
        baseIndicator.addIndicatorDatas(month, year)
        df = baseIndicator.calculateAll()
        return df

    def checkFirstSignalOfPosition(self, df):
        row = df.iloc[0]

        ema_periods = self.config.daysOfEma
        ema0 = row[f"ema{ema_periods[0]}"]
        ema1 = row[f"ema{ema_periods[1]}"]
        ema2 = row[f"ema{ema_periods[2]}"]
        gap1 = ema1 - ema0
        gap2 = ema2 - ema0

        if gap1 < 0 and gap2 < 0:
            return "long"
        elif gap1 > 0 and gap2 > 0:
            return "short"
        else:
            raise ValueError("İlk satırda sinyal yok ama olmalıydı.")
    
    def getBuyPoints (self , signal , data1s):
        startProcessTimestamp = int(signal[1]) + 900000
        timestampColumn = data1s[:, 0]
        startIndex = np.argmax(timestampColumn >= startProcessTimestamp)
        entryPrice = data1s[startIndex][1]
        buyPoints = self.__findBuyPoints(entryPrice, signal[0])
        return buyPoints , startIndex , entryPrice , startProcessTimestamp

    def __findBuyPoints(self, entryPrice, signal):
        valuesList = []
        nextPoint = entryPrice * self.config.buyPointsGap / 100
        testValue = entryPrice
        for _ in range(int(self.config.buyPointsCount)):
            if signal == "long":                    
                pointValue = testValue - nextPoint
                valuesList.append(round(pointValue,2))
            else : 
                pointValue = testValue + nextPoint
                valuesList.append(round(pointValue,2))
            testValue = pointValue
        return valuesList