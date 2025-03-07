


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
        if infoStage == "self.increaseStopPoint2":
            self.message = f"Stage3 is continuing and process is quitting in second upper entrystop point"
        if infoStage == "increaseStopPoint3":
            self.message = f"Stage3 is continuing and process is quitting in third upper entrystop point"
        

    def createProcessInfo(self,infoStage,signalSide,signalTimeStamp,startProcessTimestamp,profitLoss,totalAmount):
        self.__informationHead(self, infoStage)
        self.resultDatas = []
        self.resultDatas.append(
                {
                    "signal": signalSide,
                    "signalTimeStamp": signalTimeStamp,
                    "startProcessTimestamp": startProcessTimestamp,
                    "profitLoss": profitLoss,
                    "totalAmount": totalAmount,
                }
            )
        return resultDatas
    
    def createMonthlyStatsInfo(self,currentTimeStamp, purchasedPoints, messages , totalpnL, profit, profitsCount, loss, lossesCount,entryStopsCount ):
        purchasedPoints = "".join(
                        [f"({x[0]}, {x[1]})" for x in purchasedPoints]
                    )
        self.resultDatas[-1]["processEndTimeStamp"] = currentTimeStamp
        self.resultDatas[-1]["purchasedPoints"] = purchasedPoints
        self.resultDatas[-1]["situationOfProcess"] = messages
        self.resultDatas[-1]["totalPnL"] = totalpnL
        self.resultDatas[-1]["totalProfit"] = (profit, profitsCount)
        self.resultDatas[-1]["totalLoss"] = (loss, lossesCount)
        self.resultDatas[-1]["totalEntryStop"] = entryStopsCount

        
        