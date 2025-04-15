from core.data_processor import DataProcessor
from config.config import Config

class SignalService:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.config = Config()
    def __getSignalsTime(self, firstSignalSide, df):
        signalDatas = []
        signalDatas.append(firstSignalSide)

        ema_periods = self.config.daysOfEma  # Örneğin: [5, 8, 13]
        if len(ema_periods) < 3:
            raise ValueError("En az 3 EMA değeri olmalı")

        ema1_col = f"ema{ema_periods[0]}"
        ema2_col = f"ema{ema_periods[1]}"
        ema3_col = f"ema{ema_periods[2]}"

        try:
            for index in range(len(df) - 1):
                row_now = df.iloc[index]
                row_next = df.iloc[index + 1]

                ema1_now = row_now[ema1_col]
                ema2_now = row_now[ema2_col]
                ema3_now = row_now[ema3_col]

                ema1_next = row_next[ema1_col]
                ema2_next = row_next[ema2_col]
                ema3_next = row_next[ema3_col]

                if (ema2_now < ema1_now < ema3_now) or (ema3_now < ema1_now < ema2_now):
                    if ema1_next > ema2_next and ema1_next > ema3_next:
                        if signalDatas[-1][0] != "long":
                            signalDatas.append(["long", row_next["OpenTime"]])
                    elif ema1_next < ema2_next and ema1_next < ema3_next:
                        if signalDatas[-1][0] != "short":
                            signalDatas.append(["short", row_next["OpenTime"]])
                elif ema1_now > ema2_now > ema3_now:
                    if ema1_next < ema2_next and ema1_next < ema3_next:
                        if signalDatas[-1][0] != "short":
                            signalDatas.append(["short", row_next["OpenTime"]])
                elif ema1_now < ema2_now < ema3_now:
                    if ema1_next > ema2_next and ema1_next > ema3_next:
                        if signalDatas[-1][0] != "long":
                            signalDatas.append(["long", row_next["OpenTime"]])

        except Exception as e:
            print("Error in getSignalsTime:", e)

        return signalDatas  

    def extractSignals(self, month, year):
        organisedDataFrame = self.data_processor.addIndicators(month, year)
        firstSignalSide = self.data_processor.checkFirstSignalOfPosition(organisedDataFrame)
        signals = self.__getSignalsTime(firstSignalSide, organisedDataFrame)
        return signals
