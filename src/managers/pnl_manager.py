class PnLManager:
    def __init__(self):
        self.currentPnL = 0
        self.currentValue = 0
        self.currentTimestamp = 0
        self.processPnL = 0  # tek seferlik işlem PnL’i
        self.pastPnL = 0     # toplam birikmiş PnL

    def updatePnL(self, averagePrice, currentData, signalType):
        self.currentTimestamp = int(currentData[0])
        self.currentValue = currentData[1]
        self.currentPnL = self._calculateCurrentPnL(averagePrice, self.currentValue, signalType)

    def _calculateCurrentPnL(self, entry, current, signalType):
        if entry == 0:
            return 0
        change = ((current - entry) / entry) * 100
        if signalType == "short":
            change = -change
        return round(change, 2)

    def calculateProcessPnL(self, entry, current, amount, portion, signalType):
        if entry == 0 or amount == 0:
            return 0

        if signalType == "short":
            rawPnL = (entry - current) / entry * amount
        else:
            rawPnL = (current - entry) / entry * amount

        currentProcessPnL = round(rawPnL * portion, 2)
        self.processPnL = currentProcessPnL
        return currentProcessPnL

    def registerPastPnL(self, entry, current, amount, portion, signalType):
        current = self.calculateProcessPnL(entry, current, amount, portion, signalType)
        self.pastPnL += current