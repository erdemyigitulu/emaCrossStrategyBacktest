


class InformationService ():
    def __init__ (self):
        pass

    def __informationHead(self, infoStage):
        if infoStage == "stopLoss":
            self.message = "StopLoss has came true"
        if infoStage == "entryStop":
            self.message = "entryStop has came true"
        if infoStage == "stage1":
            self.message = f"Stage1 is done. Some profit is got {"aa"}"
        if infoStage == "stage2":
            self.message = f"Stage2 is done. Some profit is got {"aa"}"
        if infoStage == "stage3":
            self.message = f"Stage3 is done.Some profit is got {"aa"}"
        if infoStage == "increaseStopPoint1":
            self.message = f"Stage3 is continuing and process is quitting in first upper entrystop point"
        if infoStage == "increaseStopPoint2":
            self.message = f"Stage3 is continuing and process is quitting in second upper entrystop point"
        if infoStage == "increaseStopPoint3":
            self.message = f"Stage3 is continuing and process is quitting in third upper entrystop point"
        if infoStage == "cameNewSignal":
            self.message = f"New signal has came and process is quitting"
        
    def createProcessInfo(self,infoStage,signalSide,signalTimeStamp,startProcessTimestamp,profitLoss,totalAmount,currentTimeStamp, purchasedPoints, messages):
        self.__informationHead(self, infoStage)
        self.resultDatas = []
        purchasedPoints = "".join(
                        [f"({x[0]}, {x[1]})" for x in purchasedPoints]
                    )
        self.resultDatas.append(
                {
                    "signal": signalSide,
                    "signalTimeStamp": signalTimeStamp,
                    "startProcessTimestamp": startProcessTimestamp,
                    "profitLoss": profitLoss,
                    "totalAmount": totalAmount,
                    "processEndTimeStamp" : currentTimeStamp,
                    "purchasedPoints" : purchasedPoints,
                    "situationOfProcess" : messages
                }
            )
        return self.resultDatas
    
    def createMonthlyStatsInfo(self,resultData, totalpnL, profit, profitsCount, loss, lossesCount,entryStopsCount ):
        resultData[-1]["totalPnL"] = totalpnL
        resultData[-1]["totalProfit"] = (profit, profitsCount)
        resultData[-1]["totalLoss"] = (loss, lossesCount)
        resultData[-1]["totalEntryStop"] = entryStopsCount
        return resultData

        
        