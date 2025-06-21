from indicators.base_indicator import BaseIndicator
import ta

class AverageTrueRangeIndicator(BaseIndicator):
    def __init__(self,config, period=14):
        super().__init__(config)
        self.period = period
        self.tr = []
        self.atr = []

    def calculate(self):
        data = self.df
        atr_indicator = ta.volatility.AverageTrueRange(high=data['High'], low=data['Low'], close=data['Close'], window=14)
        data['ATR'] = atr_indicator.average_true_range()
        self.df = data

