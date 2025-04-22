from services.write_csv_data import WriteCsvData

class InformationService:
    def __init__(self):
        self.message = ""
        self.write_csv_data = WriteCsvData()

        self.totalPnL = 0
        self.totalProfitAmount = 0
        self.totalLossAmount = 0
        self.totalWinningTrades = 0
        self.totalLosingTrades = 0
        self.totalEntryStopTrades = 0

    def informationHead(self, exitReason):
        messages = {
            "stopLoss": "StopLoss has came true",
            "entryStop": "EntryStop has came true",
            "stage1": "Stage1 is done. Some profit is got",
            "stage2": "Stage2 is done. Some profit is got",
            "stage3": "Stage3 is done. Some profit is got",
            "increaseStopPoint1": "Stage3 is continuing and process is quitting in first upper entrystop point",
            "increaseStopPoint2": "Stage3 is continuing and process is quitting in second upper entrystop point",
            "increaseStopPoint3": "Stage3 is continuing and process is quitting in third upper entrystop point",
            "cameNewSignal": "New signal has came and process is quitting"
        }
        return messages.get(exitReason, f"Unknown reason: {exitReason}")

    def _updateStats(self, profitLoss):
        if profitLoss < 0:
            self.totalLossAmount += profitLoss
            self.totalLosingTrades += 1
        elif profitLoss > 0:
            self.totalProfitAmount += profitLoss
            self.totalWinningTrades += 1
        else:
            self.totalEntryStopTrades += 1

        self.totalPnL += profitLoss

    def _prepareMonthlyStats(self, resultData):
        resultData["totalPnL"] = self.totalPnL
        resultData["totalProfit"] = (self.totalProfitAmount, self.totalWinningTrades)
        resultData["totalLoss"] = (self.totalLossAmount, self.totalLosingTrades)
        resultData["totalEntryStop"] = self.totalEntryStopTrades
        return resultData

    def monthlyStats(self, resultData, profitLoss, month, year):
        self._updateStats(profitLoss)
        print(resultData)
        enrichedResult = self._prepareMonthlyStats(resultData)
        input(enrichedResult)
        self.write_csv_data.writeCsv(enrichedResult, month, year)