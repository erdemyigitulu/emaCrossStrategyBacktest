

class PnLManager:
    def __init__(self):
        self.pnl = 0
        self.currentValue = 0
        self.currentTimestamp = 0

    def update(self, averagePrice, currentData, signalSide):
        self.currentTimestamp = int(currentData[0])
        self.currentValue = currentData[1]
        self.pnl = self.calculatePnL(averagePrice, self.currentValue, signalSide)

    def calculatePnL(self, entry, current, side):
        if entry == 0:
            return 0
        change = ((current - entry) / entry) * 100
        change = round(change, 4)
        if side == "short":
            change = -change
        return change