from config.config import Config

class BuyPointsGenerator:

    def __init__(self, config:Config):
        self.config = config
        self.buyPoints = []
    
    def getBuyPoints (self, entry_position, signal):
        self.buyPoints.append(entry_position)
        buyPoints = self._findBuyPoints(entry_position[0], signal)
        return buyPoints

    def _findBuyPoints(self, entry_position, signal):
        valuesList = []
        nextPoint = entry_position * self.config.buyPointsGap / 100
        testValue = entry_position
        for _ in range(int(self.config.buyPointsCount)):
            if signal["Type"] == "long":                    
                pointValue = testValue - nextPoint
            else : 
                pointValue = testValue + nextPoint
            testValue = pointValue
            valuesList.append((round(pointValue,2), self.config.seperatedMoneyAmount))
        return valuesList