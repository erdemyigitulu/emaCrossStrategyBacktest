


class PositionManager:
    def __init__(self, config):
        self.config = config
        self.purchasedPoints = []
        self.buyPoints = []
        self.entryPrice = 0
        self.totalAmount = 0
        self.averagePrice = 0
        self.startIndex = 0
        self.startProcessTimestamp = 0

    def initialize(self, signal, data1s):
        signalSide = signal[0]
        signalTimestamp = signal[1]
        self.startProcessTimestamp = int(signalTimestamp) + 900000

        timestampColumn = data1s[:, 0]
        self.startIndex = int((timestampColumn >= self.startProcessTimestamp).nonzero()[0][0])
        self.entryPrice = data1s[self.startIndex][1]

        self.buyPoints = self.__findBuyPoints(self.entryPrice, signalSide)
        entry = (self.entryPrice, self.config.totalEntryAmount)
        self.purchasedPoints.append(entry)
        self._updateAveragePrice()

    def update(self, currentValue, signalSide):
        for point in self.buyPoints:
            if (point, self.config.seperatedMoneyAmount) in self.purchasedPoints:
                continue
            if signalSide == "long" and currentValue <= point:
                self.purchasedPoints.append((point, self.config.seperatedMoneyAmount))
            elif signalSide == "short" and currentValue >= point:
                self.purchasedPoints.append((point, self.config.seperatedMoneyAmount))
        self._updateAveragePrice()

    def __findBuyPoints(self, entryPrice, signalSide):
        valuesList = []
        nextPoint = entryPrice * self.config.buyPointsGap / 100
        testValue = entryPrice
        for _ in range(int(self.config.buyPointsCount)):
            if signalSide == "long":
                pointValue = testValue - nextPoint
            else:
                pointValue = testValue + nextPoint
            valuesList.append(round(pointValue, 2))
            testValue = pointValue
        return valuesList

    def _updateAveragePrice(self):
        totalCost = sum(price * amount for price, amount in self.purchasedPoints)
        self.totalAmount = sum(amount for _, amount in self.purchasedPoints)
        if self.totalAmount > 0:
            self.averagePrice = totalCost / self.totalAmount
