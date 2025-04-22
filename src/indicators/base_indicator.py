from data_paths.candles_data_access import CandlesDataAccess
from config.config import Config


class BaseIndicator():
    def __init__(self):
        self.config = Config()
        self.candles_data_access = CandlesDataAccess()
        self.df = None
        self.indicators = []

    def _addIndicator(self, indicator):
        self.indicators.append(indicator)

    def _importIndicatorsFromConfig(self):
        for className in self.config.USED_INDICATORS:
            modulePath = self.config.INDICATOR_MAP[className]
            module = __import__(modulePath, fromlist=[className])
            indicatorModule = getattr(module, className)
            self._addIndicator(indicatorModule())

    def _calculateAll(self):
        for indicator in self.indicators:
            indicator.df = self.df
            indicator.calculate()
        self.df = self.df.iloc[self.config.cleanRowCount:].copy()
        return self.df
    
    def applyIndicators(self, df):
        self.df = df
        self._importIndicatorsFromConfig()
        return self._calculateAll()



        

