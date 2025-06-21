
class TradeAggregator:
    def __init__(self):
        self.purchasedPoints = []
        self.buyPoints = []
        self.totalAmount = 0
        self.averagePrice = 0

    def calculateAverageAndTotal(self, purchasedPoints):
        totalCost = sum(price * amount for price, amount in purchasedPoints)
        totalAmount = sum(amount for _, amount in purchasedPoints)

        if totalAmount > 0:
            averagePrice = totalCost / totalAmount
        else:
            averagePrice = 0
        self.averagePrice = averagePrice
        return totalAmount, averagePrice

