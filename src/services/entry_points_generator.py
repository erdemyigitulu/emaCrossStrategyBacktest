from config.config import Config

class EntryPointGenerator :

    def __init__(self, config:Config):
        self.config = config
    
    def getBuyPoints (self, entryPrice, signalType):
        buyPoints = self.__findBuyPoints(entryPrice, signalType)
        return buyPoints

    def __findBuyPoints(self, entryPrice, signalType):
        valuesList = []
        nextPoint = entryPrice * self.config.buyPointsGap / 100
        testValue = entryPrice
        for _ in range(int(self.config.buyPointsCount)):
            if signalType == "long":                    
                pointValue = testValue - nextPoint
                valuesList.append(round(pointValue,2))
            else : 
                pointValue = testValue + nextPoint
                valuesList.append(round(pointValue,2))
            testValue = pointValue
        return valuesList