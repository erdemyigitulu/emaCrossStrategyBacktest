class ResultBuilder:
    def __init__(self, config):
        self.config = config

    def buildResult(self, signal, averagePrice, purchasedPoints, profitLoss,
                    exitReason, currentValue, currentTimestamp, totalAmount, stageInfo):

        profitLoss = profitLoss - (averagePrice * 0.04 / 100) 
        purchasedPointsInfo = "".join([f"({x[0]}, {x[1]})" for x in purchasedPoints])

        result = {
            'signalTimestamp':int(signal[1]),
            'signalType': signal[0],
            'entryPrice': signal[2] if len(signal) > 2 else averagePrice,
            'exitPrice': currentValue,
            'exitTimestamp': currentTimestamp,
            "purchasedPoints": purchasedPointsInfo,
            "averagePrice": averagePrice,
            "profitLoss": profitLoss,
            "exitReason": ",".join(exitReason) if exitReason else "",
            'stage1Activated': stageInfo.get("stage1", False),
            'stage2Activated': stageInfo.get("stage2", False),
            'stage3Activated': stageInfo.get("stage3", False),
            'stage3Phase1': stageInfo.get("phase1", False),
            'stage3Phase2': stageInfo.get("phase2", False),
            'stage3Phase3': stageInfo.get("phase3", False),
            'totalAmount': totalAmount
        }
        return result