from core.engine import Engine
from core.signal_service import SignalService
from services.information_service import InformationService
from services.data_converter import DataConverter
from managers.carry_over_manager import CarryOverManager
from config.config import Config

class BacktestService:
    def __init__(self):
        self.signal_service = SignalService()
        self.data_converter = DataConverter()
        self.config = Config()
        self.information_service = InformationService()
        self.carry_over_manager = CarryOverManager()
        self.signals = []
        self.isCarryOver = False
        self.carrySignal = []
        self.carryReason = ""
        self.isFirstMonth = True
        self.lastSignal = []


    def _getNextSignalTimeStamp(self,index):
        try:
            nextSignalTimestamp = self.signals[index + 2][1]
        except IndexError:
            nextSignalTimestamp  = float("inf")
            input("nextts deyim")
        return nextSignalTimestamp

    def _setCarryOverFlags(self, engine):
        self.isCarryOver = False
        self.carrySignal = engine.carrySignal
        self.carryReason = engine.carryReason

    def _prepareData1s(self, month, year):
        if self.isCarryOver:
            data1s = self._getCarryOverData1s(self.carryReason, month, year)
            self.carrySignal = self.lastSignal
            self._resetCarryOverVariables()
        else:
            data1s = self.data_converter.get1sData(month, year)
        return data1s
    
    def _getCarryOverData1s(self, reason, month, year):
        if reason == "late_entry":
            return self.data_converter.get1sData(month, year)
        elif reason == "unclosed_trade":
            return self.carry_over_manager.prepareCarryOverData(self.carrySignal, month, year)
    
    def _resetCarryOverVariables(self):
        self.carry_over_manager.isCarryOver = False
        self.isCarryOver = False

    def startBacktest(self):
        for year in self.config.years:
            for month in self.config.months:    
                data1s = self._prepareData1s(month, year)
                input(data1s[0])
                self.signals = self.signal_service.extractSignals(
                    self.lastSignal, 
                    self.isFirstMonth,
                    self.carrySignal, 
                    month, 
                    year
                )
                for index, signal in enumerate(self.signals[1:]):
                    engine = Engine()
                    nextSignalTimestamp = self._getNextSignalTimeStamp(index)
                    engine.pushSignalData(signal, data1s , nextSignalTimestamp)
                    self.lastSignal = self.signals[-1]
                    if engine.isCarryOver :
                       self._setCarryOverFlags(engine)
                       break
                    engine.process(data1s, nextSignalTimestamp)
                    self.information_service.monthlyStats(
                        engine.result, 
                        engine.result["profitLoss"],
                        month, 
                        year
                    )
                    

