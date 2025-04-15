import pandas as pd
from data_paths.candles_data_access import CandlesDataAccess
from config.config import Config
import ta


class BaseIndicator():
    def __init__(self):
        self.config = Config()
        self.candles_data_access = CandlesDataAccess()
        self.df = None
        self.indicators = []

    def addIndicator(self, indicator):
        self.indicators.append(indicator)

    def addIndicatorDatas(self, month, year):
        path = self.candles_data_access.get15mCsvPath(month, year)
        self.df = pd.read_csv(path , names=self.config.COLUMN_NAMES)

    def calculateAll(self):
        for indicator in self.indicators:
            indicator.df = self.df
            indicator.calculate()
        self.df = self.df.iloc[self.config.cleanRowCount:].copy()
        return self.df


        

