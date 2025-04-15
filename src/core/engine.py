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
        self.sellPortion = 1
        self.shouldClose = True

    def pushSignalData(self, signal, data1s):
        self.signal = signal
        self.signalSide = signal[0]
        self.position_manager.initialize(signal, data1s)

    def process(self, data1s, nextSignalTimestamp):
        for data in data1s[self.position_manager.startIndex:]:
            currentTimestamp = data["OpenTime"]
            self.pnl_manager.update(
                averagePrice=self.position_manager.averagePrice,
                currentData=data,
                signalSide=self.signalSide
            )

            self.position_manager.update(
                currentValue=self.pnl_manager.currentValue,
                signalSide=self.signalSide
            )

            self._runStageLogic(nextSignalTimestamp,currentTimestamp)

            if self.closeEngine:
                break

    def _runStageLogic(self, nextSignalTimestamp , currentTimestamp):
        stageResults = self.stage_controller.updateStages(self.pnl_manager.pnl,nextSignalTimestamp , currentTimestamp )

        if "stage1" in stageResults:
            self.sellPortion = self.sellPortion - self.config.stage1SellPortion
            self._logExit("stage1")
            self.closeEngine = False

        if "stage2" in stageResults:
            self.sellPortion = self.sellPortion - self.config.stage2SellPortion
            self._logExit("stage2")
            self.closeEngine = False
            
        if "stage3" in stageResults:
            self._logExit("stage3")
            self.closeEngine = True

        if "phase1" in stageResults:
            self._logExit("increaseStopPoint1")
            self.closeEngine = True

        if "phase2" in stageResults:
            self._logExit("increaseStopPoint2")
            self.closeEngine = True

        if "phase3" in stageResults:
            self._logExit("increaseStopPoint3")
            self.closeEngine = True



    def _logExit(self, reason):

        stageInfo = self.stage_controller.getStageInfo()

        self.result = self.result_builder.buildResult(
            signal=self.signal,
            averagePrice=self.position_manager.averagePrice,
            purchasedPoints=self.position_manager.purchasedPoints,
            profitLoss=self._calculateMoneyPnL(),
            exitReason=reason,
            currentValue=self.pnl_manager.currentValue,
            currentTimestamp=self.pnl_manager.currentTimestamp,
            totalAmount=self.position_manager.totalAmount,
            stageInfo=stageInfo
        )

        print(f"🚪 EXIT: {reason} @ {self.pnl_manager.pnl:.2f}%")


    def _calculateMoneyPnL(self):
        entry = self.position_manager.averagePrice
        current = self.pnl_manager.currentValue
        total = self.position_manager.totalAmount
        pnl_percent = self.pnl_manager.pnl
        return ((current - entry) / entry) * total if total > 0 else 0


    

    
