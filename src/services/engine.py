from config import Config
from services.data_processor import DataProcessor
from services.calculator_service import CalculaterService
from services.information_service import InformationService
from data_access.write_csv_data import WriteCsvData

class Engine():
    def __init__(self):
        self.__startProcessData() 
        self.__startVariables()
        self.__startStatsCount()
        self.__pushAlgoVariables()
        self.calculator_service = CalculaterService()
        self.data_processor = DataProcessor()
        self.config = Config()
        self.information_service = InformationService()
        self.write_csv_data = WriteCsvData()
        #self.database_service = DatabaseService()
        #self.experimentId = self.database_service.saveExperimentParameters()

    def __startProcessData(self):
        self.buyPoints = []
        self.startIndex = 0
        self.entryPrice = 0
        self.startProcessTimestamp = 0

    def __startVariables(self):
        self.currentTimestamp = 0
        self.currentValue = 0
        self.pnL = 0
        self.avaregePrice = 0
        self.portion = 1
        self.purchasedPoints = []

    def __startStatsCount(self):
        self.totalpnL = 0
        self.totalProfitAmount = 0
        self.totalLossAmount = 0
        self.totalEntryStopTrades = 0
        self.totalWinningTrades = 0
        self.totalLosingTrades = 0
        self.profitLoss = 0
        self.portion = 1
        self.nextSignal = 0
        self.resultDatas = {}
        self.resultDataMonthly = {}
        self.messages = []

    def __pushAlgoVariables(self):
        self.tradesList = []
        self.entryStopPoint = False
        self.stopLossPointPoint = False
        self.sellPoint1 = False
        self.sellPoint2 = False
        self.sellPoint3 = False
        self.protectProcess1  = False
        self.increaseStopPoint1 = False
        self.increaseStopPoint2 = False
        self.increaseStopPoint3 = False
        self.isEmaSideChange = False
        self.closeEngine = False
        self.__stageInfo()

    def __stageInfo(self):
        self.stage1Start = True
        self.stage2Start = False
        self.stage3Start = False
        self.stage3Phase1 = False
        self.stage3Phase2 = False
        self.stage3Phase3 = False
        self.stage1isActivated = False
        self.stage2isActivated = False

    def pushSignalData(self, signal, data1s):

        self.signalSide = signal[0]
        self.signalTimestamp = signal[1]
        self.signalData = signal
        self.data1s = data1s
        self.__createStartValues()

    def __createStartValues(self):
        self.buyPoints, self.startIndex, self.entryPrice, self.startProcessTimestamp = self.data_processor.getBuyPoints(self.signalData, self.data1s)
        entryPoint = (self.entryPrice, self.config.totalEntryAmount)
        self.purchasedPoints.append(entryPoint)

    def findpurhasedProcessesData(self):
        for point in self.buyPoints:
            if not (point, self.config.seperatedMoneyAmount) in self.purchasedPoints:
                if self.currentValue <= point and self.signalSide == "long":
                    self.purchasedPoints.append((point, self.config.seperatedMoneyAmount))
                elif self.currentValue >= point and self.signalSide == "short":
                    self.purchasedPoints.append((point, self.config.seperatedMoneyAmount))
                self.avaregePrice, self.totalAmount = self.calculator_service.calculateAvaregePrice(self.purchasedPoints)
    
    def pushVariableValues(self, past):
        self.currentValue = past[1]
        self.currentTimestamp = int(past[0])
        self.pnL = self.calculator_service.percentageIncrease(self.avaregePrice, self.currentValue, self.signalSide)
        print(self.pnL, self.currentTimestamp, self.currentValue, self.entryPrice)
        
    def __stage1(self):
        self.stopLossPoint = True
        self.sellPoint1 = True

    def __stage2(self):
        self.stopLossPoint = False
        self.stage1Start = False
        self.entryStopPoint = True
        self.sellPoint1 = False
        self.sellPoint2 = True

    def __stage3(self):
        self.stage2Start = False
        self.sellPoint2 = False
        self.sellPoint3 = True
        if (self.pnL < self.config.gap1) and not self.stage3Phase1:
            self.increaseStopPoint1 = True
            self.stage3Phase1 = True
        elif (self.config.gap1 <= self.pnL < self.config.gap2) and not self.stage3Phase2:
            self.increaseStopPoint1 = False
            self.increaseStopPoint2 = True
            self.stage3Phase2 = True
        elif (self.pnL >= self.config.gap2) and not self.stage3Phase3:
            self.increaseStopPoint2 = False
            self.increaseStopPoint3 = True
            self.stage3Phase3 = True
    
    def engineAlgoritm(self):
        self.__stageController()
        if self.stopLossPoint and self.pnL <= self.config.stopLossPnl:
            self.__extractResultDatas("stopLoss")
            self.closeEngine = True

        if self.entryStopPoint and self.pnL <= self.config.entryStopPnl:
            self.__extractResultDatas("entryStop")
            if not self.portion == 1:
                self.portion = self.portion - self.config.stage1SellPortion
            self.closeEngine = True
                  
        if self.stage1Start and self.sellPoint1 and self.pnL >= self.config.stage1StartPnl and not self.stage1isActivated:
            self.__extractResultDatas("stage1")
            self.portion = self.portion - self.config.stage1SellPortion
            self.stage1isActivated = True

        if self.stage2Start and self.sellPoint2 and self.pnL >= self.config.stage2StartPnl and not self.stage2isActivated:
            self.__extractResultDatas("stage2")
            self.portion = self.portion - self.config.stage2SellPortion
            self.stage2isActivated = True
        
        if self.stage3Start and self.sellPoint3 and self.pnL >= self.config.stage3StartPnl:
            self.__extractResultDatas("stage3")
            self.portion = self.portion - self.config.stage3SellPortion
            self.closeEngine = True

        if self.increaseStopPoint1 and self.pnL == self.config.increaseStopPoint1Pnl:
            self.__extractResultDatas("increaseStopPoint1")
            self.portion = self.portion - self.config.stage3SellPortion
            self.closeEngine = True

        if self.increaseStopPoint2 and self.pnL <= self.config.increaseStopPoint2Pnl:
            self.__extractResultDatas("increaseStopPoint2")
            self.portion = self.portion - self.config.stage3SellPortion
            self.closeEngine = True

        if self.increaseStopPoint3 and self.pnL <= self.config.increaseStopPoint3Pnl:
            self.__extractResultDatas("increaseStopPoint3")
            self.portion = self.portion - self.config.stage3SellPortion
            self.closeEngine = True

        if self.currentTimestamp > self.nextSignal + 900000:
            self.__extractResultDatas("cameNewSignal")
            self.closeEngine = True

    def __stageController(self):
        if self.stage1Start:
            self.__stage1()
        elif self.stage2Start:
            self.__stage2()
        elif self.stage3Start:
            self.__stage3()
        else:
            print("not active stage")

    def __extractResultDatas(self, informationOfStage):
        self.profitLoss = self.calculator_service.moneyProfitLossFunc(self.profitLoss, self.totalAmount, self.pnL, self.portion)
        message = self.information_service.informationHead(informationOfStage)
        self.messages.append(message)
        purchasedPointsInfo = "".join(
                        [f"({x[0]}, {x[1]})" for x in self.purchasedPoints]
                    )
        
        # Save signal result to database
        self.resultDatas = {
            'signalTimestamp': self.signalTimestamp,
            'signalType': self.signalSide,
            'entryPrice': self.entryPrice,
            'exitPrice': self.currentValue,
            "purchasedPoints": purchasedPointsInfo,
            'profitLoss': self.profitLoss,
            'exitReason': self.messages,
            'stage1Activated': self.stage1Start,
            'stage2Activated': self.stage2Start,
            'stage3Activated': self.stage3Start,
            'stage3Phase1': self.stage3Phase1,
            'stage3Phase2': self.stage3Phase2,
            'stage3Phase3': self.stage3Phase3,
            'totalAmount': self.totalAmount
        }
        #self.database_service.saveSignalResult(self.experimentId, self.resultDatas )
        
        # Save monthly stats to database
        #statsData = {
        #    'year': year,
        #    'month': month,
        #    'totalPnl': self.totalpnL,
        #    'totalProfitAmount': self.totalProfitAmount,
        #    'totalLossAmount': self.totalLossAmount,
        #    'profitCount': self.totalWinningTrades,
        #    'lossCount': self.totalLosingTrade,
        #    'entryStopCount': self.totalEntryStopTrades
        #}
        #self.database_service.saveMonthlyStats(self.experimentId, statsData)

    #def __del__(self):
    #    self.database_service.close()