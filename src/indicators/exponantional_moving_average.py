from indicators.base_indicator import BaseIndicator


class ExponentialMovingAverageIndicator(BaseIndicator):
    def __init__(self):
        super().__init__()
    
    def calculate(self):
        for period in self.config.daysOfEma:
            col_name = f"ema{period}"
            self.df[col_name] = self.df["Close"].ewm(span=period, adjust=False).mean()