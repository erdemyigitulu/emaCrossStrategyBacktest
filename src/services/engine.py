from src.config import Config
from data_processor import DataProcessor
from calculator_service import CalculaterService
from information_service import InformationService
from data_access.write_csv_data import WriteCsvData

class Engine():
    def __init__ (self):
        self.__startProcessData() 
        self.__startVariables()
        self.__startStatsCount()
        self.__pushAlgoVariables()
        self.calculator_service = CalculaterService()
        self.data_processor = DataProcessor()
        self.config = Config()
        self.information_service = InformationService()
        self.write_csv_data = WriteCsvData()

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
        self.entryStopsCount = 0
        self.profitsCount = 0
        self.lossesCount = 0
        self.profitLoss = 0
        self.portion = 1
        self.nextSignal = 0
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
        self.stage1isActivated = False
        self.stage2isActivated = False
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
        
    def __stage1(self):
        self.stopLossPoint = True
        self.sellPoint1 = True
        self.stage1Phase1 = True

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
    
    def engineAlgoritm (self) :
        self.__stageController()
        if self.stopLossPoint and self.pnL <= self.config.stopLossPnl:
            self.__extractResultDatas ("stopLoss")
            self.closeEngine = True

        if self.entryStopPoint and self.pnL <= self.config.entryStopPnl:
            self.__extractResultDatas ("entryStop")
            self.closeEngine = True
        
        if self.stage1Start and self.sellPoint1 and self.pnL >= self.config.stage1StartPnl and not self.stage1isActivated:
           self.__extractResultDatas ("stage1")
           self.stage1isActivated = False

        if self.stage2Start and self.sellPoint2 and self.pnL >= self.config.stage2StartPnl and not self.stage2isActivated:
            self.__extractResultDatas ("stage2")
            self.stage2isActivated = False
        
        if self.stage3Start and self.sellPoint3 and self.pnL >= self.config.stage3StartPnl:
            self.__extractResultDatas ("stage3")
            self.closeEngine = True

        if self.increaseStopPoint1 and self.pnL == self.config.increaseStopPoint1Pnl:
            self.__extractResultDatas ("increaseStopPoint1")
            self.closeEngine = True

        if self.increaseStopPoint2 and self.pnL <= self.config.increaseStopPoint2Pnl:
            self.__extractResultDatas ("increaseStopPoint2")
            self.closeEngine = True

        if self.increaseStopPoint3 and self.pnL <= self.config.increaseStopPoint3Pnl:
            self.__extractResultDatas ("increaseStopPoint3")
            self.closeEngine = True

        if self.currentTimeStamp > self.nextSignal + 900000:
            self.__extractResultDatas ("cameNewSignal")
            self.closeEngine = True

    def __stageController(self):
        if self.stage1Start:
            self.__stage1()
        elif self.stage2Start :
            self.__stage2()
        elif self.stage3Start:
            self.__stage3()
        else :
            print("not active stage")

# --------------------------------------------------------------------------------------------------------------------------
# Engine's work is done

    def __extractResultDatas (self, message) :
        self.profitLoss = self.calculator_service.moneyProfitLossFunc(self.profitLoss, self.totalAmount, self.pnL, 0.25)
        self.resultDatas = self.information_service.createProcessInfo(message, self.signalSide, (self.signal)[1], self.startProcessTimestamp, self.profitLoss, self.totalAmount, self.currentTimestamp, self.purchasedPoints, self.messages)

    def monthlyStats(self , month , year):
        if self.profitLoss < 0:
            self.loss = self.loss + self.profitLoss
            self.lossesCount = self.lossesCount + 1
        elif self.profitLoss > 0:
            profit = profit + self.profitLoss
            profitsCount = profitsCount + 1
        else:
            self.entryStopsCount = self.entryStopsCount + 1
        totalpnL = totalpnL + self.profitLoss
        resultData=[]
        self.resultDatas = resultData
        self.resultDatas = self.information_service.createMonthlyStatsInfo(resultData , self.totalpnL, self.profit, self.profitsCount, self.loss, self.lossesCount, self.entryStopsCount)
        self.write_csv_data.writeCsv(self.resultDatas, month, year)