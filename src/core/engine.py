from config.config import Config
from managers.position_manager import PositionManager
from managers.pnl_manager import PnLManager
from managers.result_builder import ResultBuilder
from managers.stage_controller import StageController

class Engine:
    def __init__(self):
        self.config = Config()
        self.stage_controller = StageController(self.config)
        self.position_manager = PositionManager(self.config)
        self.result_builder = ResultBuilder(self.config)
        self.pnl_manager = PnLManager()
        self.closeEngine = False
        self.signal = None
        self.signalSide = None
        self.result = None
        self.triggeredReasons = []
        self.pastpnL = 0
        self.pnL = 0
        self.sellPortion = 1

    def pushSignalData(self, signal, data1s,nextSignalTimestamp):
        self.signal = signal
        self.signalSide = signal[0]
        self.position_manager.initialize(signal, data1s, nextSignalTimestamp)
        self.isCarryOver = self.position_manager.isCarryOver
        if self.isCarryOver :
            self.carrySignal = signal
            self.carryReason = "late_entry"
            input("push data içindeyim")

    def process(self, data1s, nextSignalTimestamp):
        self.stage_controller.stageControllerReset()
        for data in data1s[self.position_manager.startIndex:]:
            currentTimestamp = int(data[0])
            self.pnl_manager.updatePnL(
                averagePrice=self.position_manager.averagePrice,
                currentData=data,
                signalType=self.signalSide
            )
            self.pnL = self.pnl_manager.currentPnL
            self.position_manager.totalAmount -= self.position_manager.totalAmount * self.sellPortion

            self.position_manager.updatePurchasedPoints(
                currentValue=self.pnl_manager.currentValue,
                signalSide=self.signalSide
            )
            self._runStageLogic(nextSignalTimestamp,currentTimestamp)
            if self.closeEngine :
                break
        else:
            if not self.closeEngine:
                self.isCarryOver = True
                self.carrySignal = self.signal
                self.carryReason = "unclosed_trade"

    def _runStageLogic(self, nextSignalTimestamp, currentTimestamp):
        stageResults, self.closeEngine = self.stage_controller.updateStages(
            self.pnl_manager.currentPnL,
            nextSignalTimestamp,
            currentTimestamp
        )

        for reason in [
            "stopLoss", "entryStop", "cameNewSignal",
            "stage1", "stage2", "stage3",
            "phase1", "phase2", "phase3"
        ]:
            if reason in stageResults:
                if reason == "stage1":
                    self.sellPortion = max(0, self.sellPortion - self.config.stage1SellPortion)
                elif reason == "stage2":
                    self.sellPortion = max(0, self.sellPortion - self.config.stage2SellPortion)
                self.triggeredReasons.append(reason)
                self._logExit(self.triggeredReasons)
                break

    def _logExit(self, allReasons):
        stageInfo = self.stage_controller.getStageInfo()

        self.pnl_manager.registerPastPnL(
            self.position_manager.averagePrice,
            self.pnl_manager.currentValue,
            self.position_manager.totalAmount,
            self.sellPortion,
            self.signalSide
        )

        self.result = self.result_builder.buildResult(
            signal=self.signal,
            averagePrice=self.position_manager.averagePrice,
            purchasedPoints=self.position_manager.purchasedPoints,
            profitLoss=self.pnl_manager.pastPnL,  # toplam PnL
            exitReason=allReasons,
            currentValue=self.pnl_manager.currentValue,
            currentTimestamp=self.pnl_manager.currentTimestamp,
            totalAmount=self.position_manager.totalAmount,
            stageInfo=stageInfo,
        )
        self.pnl_manager.pastPnL += self.pnl_manager.processPnL


    

    
