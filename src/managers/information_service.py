from services.write_csv_data import WriteCsvData


class InformationService:
    def __init__ (self):
        self.message = ""
        self.write_csv_data = WriteCsvData()
        self.totalpnL = 0
        self.totalProfitAmount = 0
        self.totalWinningTrades = 0
        self.totalLossAmount = 0
        self.totalLosingTrades = 0
        self.totalEntryStopTrades = 0

    def informationHead(self, informationOfStage):
        if informationOfStage == "stopLoss":
            self.message = "StopLoss has came true"
        if informationOfStage == "entryStop":
            self.message = "entryStop has came true"
        if informationOfStage == "stage1":
            self.message = f"Stage1 is done. Some profit is got"
        if informationOfStage == "stage2":
            self.message = f"Stage2 is done. Some profit is got"
        if informationOfStage == "stage3":
            self.message = f"Stage3 is done.Some profit is got"
        if informationOfStage == "increaseStopPoint1":
            self.message = f"Stage3 is continuing and process is quitting in first upper entrystop point"
        if informationOfStage == "increaseStopPoint2":
            self.message = f"Stage3 is continuing and process is quitting in second upper entrystop point"
        if informationOfStage == "increaseStopPoint3":
            self.message = f"Stage3 is continuing and process is quitting in third upper entrystop point"
        if informationOfStage == "cameNewSignal":
            self.message = f"New signal has came and process is quitting"
        return self.message
        
    def __createMonthlyStatsInfo(self,resultData, totalpnL, totalProfitAmount, totalWinningTrades, totalLossAmount, totalLosingTrade,totalEntryStopTrades ):
        resultData['totalPnL'] = totalpnL
        resultData['totalProfit'] = (totalProfitAmount, totalWinningTrades)
        resultData['totalLoss'] = (totalLossAmount, totalLosingTrade)
        resultData['totalEntryStop'] = totalEntryStopTrades
        return resultData
    
    def monthlyStats(self, resultDatas, profitLoss, month, year):
        if profitLoss < 0:
            self.totalLossAmount = self.totalLossAmount + profitLoss
            self.totalLosingTrades = self.totalLosingTrades + 1
        elif profitLoss > 0:
            self.totalProfitAmount = self.totalProfitAmount + profitLoss
            self.totalWinningTrades = self.totalWinningTrades + 1
        else:
            self.totalEntryStopTrades = self.totalEntryStopTrades + 1
        self.totalpnL = self.totalpnL + profitLoss
        self.resultDataMonthly = self.__createMonthlyStatsInfo(resultDatas, self.totalpnL, self.totalProfitAmount, self.totalWinningTrades, self.totalLossAmount, self.totalLosingTrades, self.totalEntryStopTrades)
        self.write_csv_data.writeCsv(self.resultDataMonthly, month, year)

        
        