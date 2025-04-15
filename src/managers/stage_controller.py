

class StageController:
    def __init__(self, config):
        self.config = config
        self._reset()

    def _reset(self):
        self.stage1Start = True
        self.stage2Start = False
        self.stage3Start = False
        self.stage1isActivated = False
        self.stage2isActivated = False
        self.stage3isActivated = False
        self.stage3Phase1 = False
        self.stage3Phase2 = False
        self.stage3Phase3 = False
        self.stopLoss = True
        self.entryStop = False
        self.newSignalHasCame = False
        self.results = []

    def updateStages(self, pnl, currentTimestamp, nextSignalTimestamp):

        if not self.stage1isActivated and pnl >= self.config.stage1StartPnl and self.stage1Start:
            self.stage1isActivated = True
            self.stage1Start = False
            self.stage2Start = True
            self.stopLoss = False
            self.entryStop = True
            self.results.append("stage1")

        if not self.stage2isActivated and not self.stage2isActivated and pnl >= self.config.stage2StartPnl and self.stage2Start:
            self.stage2isActivated = True   
            self.stage2Start = False
            self.stage3Start = True
            self.entryStop = False
            self.results.append("stage2")

        if not self.stage3isActivated and pnl >= self.config.stage3StartPnl and self.stage3Start:
            self.stage3Start = False
            self.stage3isActivated = False
            self.results.append("stage3")

        if not self.stage3Phase1 and pnl < self.config.gap1 and self.stage3isActivated:
            self.stage3Phase1 = True
            self.results.append("phase1")

        if not self.stage3Phase2 and self.config.gap1 <= pnl < self.config.gap2 and self.stage3isActivated:
            self.stage3Phase2 = True
            self.results.append("phase2")

        if not self.stage3Phase3 and pnl >= self.config.gap2 and self.stage3isActivated:
            self.stage3Phase3 = True
            self.results.append("phase3")

        if pnl <= self.config.stopLossPnl and self.stopLoss:
            self.results.append("stopLoss")
            self.closeEngine = True

        if  pnl <= self.config.entryStopPnl and self.entryStop:
            self.results.append("entryStop")
            self.closeEngine = True

        if currentTimestamp >= nextSignalTimestamp:
            self.results.append("cameNewSignal")
            self.closeEngine = True
        return self.results
    
    def isStopLossActive(self):
        return self.stopLoss

    def isEntryStopActive(self):
        return self.entryStop

    def getStageInfo(self):
        return {
            "stage1": self.stage1Start,
            "stage2": self.stage2Start,
            "stage3": self.stage3Start,
            "phase1": self.stage3Phase1,
            "phase2": self.stage3Phase2,
            "phase3": self.stage3Phase3,
            "stopLoss": self.stopLoss,
            "entryStop": self.entryStop

        }