from services.signal_service import SignalService
from helpers.utils import Utils      
from data_access.candles_data_access import CandlesDataAccess
from config import Config
from services.data_processor import DataProcessor
from services.engine import Engine
from services.information_service import InformationService


class BacktestService:
    def __init__(self):
        self.signal_service = SignalService()
        self.candles_data_access = CandlesDataAccess ()
        self.data_processor = DataProcessor()
        self.utils = Utils()
        self.config = Config()
        self.information_service = InformationService()
        self.totalPnL = 0
        self.totalProfit = 0
        self.totalLoss = 0
        self.totalEntryStop = 0



    def startBacktest(self):
        years = self.config.years
        months = self.config.months
        for year in years:
            for month in months:
                signals = self.signal_service.extractSignals(month, year)
                data1s = self.utils.get1sData(month, year)
                for index, signal in enumerate(signals[1:]):
                    engine = Engine()
                    try:
                        engine.nextSignal = signals[(index + 2)][1]
                    except:
                        print("Error in nextSignal")
                        break
                    engine.pushSignalData(signal , data1s)
                    for dataOf1s in data1s[engine.startIndex:]:
                        engine.findpurhasedProcessesData()
                        engine.pushVariableValues(dataOf1s)
                        engine.engineAlgoritm()
                        if engine.closeEngine :
                            break
                    self.information_service.monthlyStats(engine.resultDatas, engine.profitLoss, month , year)

