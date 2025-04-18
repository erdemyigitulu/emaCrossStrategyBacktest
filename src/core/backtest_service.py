from core.engine import Engine
from core.signal_service import SignalService
from services.information_service import InformationService
from services.data_converter import DataConverter
from config.config import Config

class BacktestService:
    def __init__(self):
        self.signal_service = SignalService()
        self.data_converter = DataConverter()
        self.config = Config()
        self.information_service = InformationService()

    def startBacktest(self):
        for year in self.config.years:
            for month in self.config.months:    
                signals = self.signal_service.extractSignals(month, year)
                data1s = self.data_converter.get1sData(month, year)

                for index, signal in enumerate(signals[1:]):
                    engine = Engine()
                    try:
                        nextSignalTimestamp = signals[index + 2][1]
                    except IndexError:
                        nextSignalTimestamp = float("inf")

                    engine.pushSignalData(signal, data1s)
                    engine.process(data1s, nextSignalTimestamp)

                    self.information_service.monthlyStats(engine.result, engine.result["profitLoss"], month, year)


