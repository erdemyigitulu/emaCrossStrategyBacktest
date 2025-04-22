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