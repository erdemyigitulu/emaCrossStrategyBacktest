import importlib
from config.config import Config


class BaseIndicator():
    def __init__(self,config:Config):
        self.config = config
        self.df = None
        self.indicators = []

    def _addIndicator(self, indicator):
        self.indicators.append(indicator)

    def _importIndicatorsFromConfig(self):
        for className in self.config.USED_INDICATORS:
            modulePath = self.config.INDICATOR_MAP[className]
            module = importlib.import_module(modulePath)
            indicatorClass = getattr(module, className) 
            self._addIndicator(indicatorClass(self.config))

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



        

