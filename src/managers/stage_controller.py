class StageController:
    def __init__(self, config):
        self.config = config
        self.stageControllerReset()

    def stageControllerReset(self):
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
        self.closeEngine = False

    def updateStages(self, pnl, nextSignalTimestamp, currentTimestamp):
        results = []

        print(currentTimestamp, nextSignalTimestamp, pnl,
              f"S1:{self.stage1Start} | S2:{self.stage2Start} | S3:{self.stage3Start} | "
              f"P1:{self.stage3Phase1} | P2:{self.stage3Phase2} | P3:{self.stage3Phase3} | "
              f"SL:{self.stopLoss} | ET:{self.entryStop} | CE:{self.closeEngine}")

        if not self.stage1isActivated and pnl >= self.config.stage1StartPnl and self.stage1Start:
            self.stage1isActivated = True
            self.stage1Start = False
            self.stage2Start = True
            self.stopLoss = False
            self.entryStop = True
            results.append("stage1")

        if not self.stage2isActivated and pnl >= self.config.stage2StartPnl and self.stage2Start:
            self.stage2isActivated = True
            self.stage2Start = False
            self.stage3Start = True
            self.entryStop = False
            results.append("stage2")

        if not self.stage3isActivated and pnl >= self.config.stage3StartPnl and self.stage3Start:
            self.stage3isActivated = True
            self.stage3Start = False
            self.closeEngine = True
            results.append("stage3")

        if self.stage3isActivated:
            if not self.stage3Phase1 and pnl < self.config.gap1:
                self.stage3Phase1 = True
                self.closeEngine = True
                results.append("phase1")

            elif not self.stage3Phase2 and self.config.gap1 <= pnl < self.config.gap2:
                self.stage3Phase2 = True
                self.closeEngine = True
                results.append("phase2")

            elif not self.stage3Phase3 and pnl >= self.config.gap2:
                self.stage3Phase3 = True
                self.closeEngine = True
                results.append("phase3")

        if self.stopLoss and pnl <= self.config.stopLossPnl:
            self.closeEngine = True
            results.append("stopLoss")

        if self.entryStop and pnl <= self.config.entryStopPnl:
            self.closeEngine = True
            results.append("entryStop")

        if currentTimestamp >= nextSignalTimestamp:
            self.closeEngine = True
            results.append("cameNewSignal")

        return results, self.closeEngine

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