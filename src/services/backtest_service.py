import json
from services.signal_service import SignalService
from helpers.utils import Utils      
from data_access.candles_data_access import CandlesDataAccess
from src.config import Config
from services.data_processor import DataProcessor
from services.engine import Engine



class BacktestService:
    def __init__(self):
        self.signal_service = SignalService()
        self.candles_data_access = CandlesDataAccess ()
        self.data_processor = DataProcessor()
        self.utils = Utils()
        self.config = Config()



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
                        break
                    engine.pushSignalData(signal , data1s)
                    for _1sdata in data1s[engine.startIndex:]:
                        engine.findpurhasedProcessesData()
                        engine.pushVariableValues(_1sdata)
                        engine.engineAlgoritm()
                        if engine.closeEngine :
                            break
                    engine.monthlyStats(month , year)

