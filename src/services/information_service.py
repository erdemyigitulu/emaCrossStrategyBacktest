from services.result_logger import ResultLogger

class InformationService:
    def __init__(self, result_logger: ResultLogger):
        self.message = ""
        self.result_logger = result_logger

        self.totalPnL = 0
        self.totalProfitAmount = 0
        self.totalLossAmount = 0
        self.totalWinningTrades = 0
        self.totalLosingTrades = 0
        self.totalEntryStopTrades = 0

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

    def monthlyStats(self, resultData: dict, profitLoss: float, month: int, year: int):
        self._updateStats(profitLoss)
        enriched_result = self._prepareMonthlyStats(resultData)
        self.result_logger.save_to_json(enriched_result, month, year)