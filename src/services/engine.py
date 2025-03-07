from src.config import Config
from data_processor import DataProcessor
from helpers.stage_controller import StageController
from calculator_service import CalculaterService
from information_service import InformationService

class Engine():
    def __init__ (self):
        self.__startProcessData() 
        self.__startVariables()
        self.__startStatsCount()
        self.__pushAlgoVariables()
        self.calculator_service = CalculaterService()
        self.data_processor = DataProcessor()
        self.config = Config()
        self.stage_controller = StageController()
        self.information_service = InformationService()

#-----------------------------------------------------------------------------------------------------------------------------
#Engine start configuration

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
        self.purchasedPoints = []

    def __startStatsCount(self):
        self.totalpnL = 0
        self.profit = 0
        self.loss = 0
        self.profitsCount = 0
        self.lossesCount = 0
        self.profitLoss = 0
        self.portion = 1
        self.resultDatas = []
        self.messages = []

    def pushSignalData(self ,signal , data1s):
        self.purchasedPoints = [()]
        self.signalSide = signal[0]
        self.signalData = signal
        self.data1s = data1s
        self.__createStartValues()

    def __createStartValues(self) :
        self.buyPoints , self.startIndex , self.entryPrice , self.startProcessTimestamp = self.data_processor.getBuyPoints(self.signalData , self.data1s)
        entryPoint = (self.entryPrice , self.config.totalEntryAmount)
        self.purchasedPoints.append(entryPoint)

    def __pushAlgoVariables (self):
        self.tradesList = []
        self.entryStopPoint = False
        self.stopLossPointPoint = False
        self.sellPoint1 = False
        self.sellPoint2 = False
        self.sellPoint3 = False
        self.protectProcess1 = False
        self.increaseStopPoint1 = False
        self.increaseStopPoint2 = False
        self.increaseStopPoint3 = False
        self.isEmaSideChange = False
        self.__stageInfo()

    def __stageInfo(self):
        self.stage1Start = True
        self.stage2Start = False
        self.stage3Start = False
        self.stage1Phase1 = False
        self.stage3Phase1 = False
        self.stage3Phase2 = False
        self.stage3Phase3 = False
# --------------------------------------------------------------------------------------------------------------------------
# While engine is working

    def findpurhasedProcessesData (self):
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
        
    def stage1(self):
        self.stopLossPoint = True
        self.sellPoint1 = True
        self.stage1Phase1 = True

    def stage2(self):
        self.stopLossPoint = False
        self.stage1Start = False
        self.entryStopPoint = True
        self.sellPoint1 = False
        self.sellPoint2 = True

    def stage3(self):
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
    
    def engineAlgoritm (self) :
        if self.stopLossPoint and self.pnL <= self.config.stopLossPnl:
            self.extractResultDatas ("stopLoss")
            self.closeEngine = True

        if self.entryStopPoint and self.pnL <= self.config.entryStopPnl:
            self.extractResultDatas ("entryStop")
            self.closeEngine = True
        
        if self.stage1Start and self.sellPoint1 and self.pnL >= self.config.stage1StartPnl:
           self.extractResultDatas ("stage1")

        if self.stage2Start and self.sellPoint2 and self.pnL >= self.config.stage2StartPnl:
            self.extractResultDatas ("stage2")
        
        if self.stage3Start and self.sellPoint3 and self.pnL >= self.config.stage3StartPnl:
            self.extractResultDatas ("stage3")
            self.closeEngine = True

        if self.increaseStopPoint1 and self.pnL == self.config.increaseStopPoint1Pnl:
            self.extractResultDatas ("increaseStopPoint1")
            self.closeEngine = True

        if self.increaseStopPoint2 and self.pnL <= self.config.increaseStopPoint2Pnl:
            self.extractResultDatas ("increaseStopPoint2")
            self.closeEngine = True

        if self.increaseStopPoint3 and self.pnL <= self.config.increaseStopPoint3Pnl:
            self.extractResultDatas ("increaseStopPoint3")
            self.closeEngine = True

    def extractResultDatas (self, message) :
        self.profitLoss = self.calculator_service.moneyProfitLossFunc(self.profitLoss, self.totalAmount, self.pnL, 0.25)
        self.resultDatas = self.information_service.createProcessInfo(message, self.signalSide, (self.signal)[1], self.startProcessTimestamp, self.profitLoss, self.totalAmount)
        