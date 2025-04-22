import pandas as pd
from core.data_processor import DataProcessor
from config.config import Config
from data_paths.candles_data_access import CandlesDataAccess
from indicators.base_indicator import BaseIndicator

class SignalService:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.config = Config()
        self.candles_data_access = CandlesDataAccess()
        self.base_indicator = BaseIndicator()
        self.dataFrame = None
        
    def getDataFrame(self, month, year):
        path = self.candles_data_access.get15mCsvPath(month, year)
        self.dataFrame = pd.read_csv(path , names=self.config.COLUMN_NAMES)
        self.dataFrame[self.config.COLUMN_NAMES[0]] = self.dataFrame[self.config.COLUMN_NAMES[0]].astype("int64")
        return self.dataFrame
        
    def _getSignalsTime(self, carrySignal, firstSignalSide, dataFrame):
        signalDatas = []
        print(carrySignal)
        if not carrySignal == []:
            if carrySignal[0] == "short":
                referenceSignal = "long"
            else :
                referenceSignal[0] = "short"
            signalDatas.append(referenceSignal)
            signalDatas.append(carrySignal)
        else :
            signalDatas.append(firstSignalSide)
        ema_periods = self.config.daysOfEma 
        if len(ema_periods) < 3:
            raise ValueError("En az 3 EMA değeri olmalı")

        ema1_col = f"ema{ema_periods[0]}"
        ema2_col = f"ema{ema_periods[1]}"
        ema3_col = f"ema{ema_periods[2]}"

        try:
            for index in range(len(dataFrame) - 1):
                row_now = dataFrame.iloc[index]
                row_next = dataFrame.iloc[index + 1]

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
        input(signalDatas)
        return signalDatas  

    def extractSignals(self,previousSignal,isFirstMonth, carrySignal, month, year):
        self.getDataFrame(month, year)
        self.dataFrameWithIndicators = self.base_indicator.applyIndicators(self.dataFrame)
        if isFirstMonth:
            firstSignalSide = self.checkFirstSignalOfPosition(self.dataFrameWithIndicators)
        else:
            firstSignalSide = previousSignal[0]
            raise ValueError("İlk sinyal yönü belirlenemedi.")
        signals = self._getSignalsTime(carrySignal ,firstSignalSide, self.dataFrameWithIndicators)
        return signals
    
    def checkFirstSignalOfPosition(self, dataFrame):
        row = dataFrame.iloc[0]

        ema_periods = self.config.daysOfEma
        ema0 = row[f"ema{ema_periods[0]}"]
        ema1 = row[f"ema{ema_periods[1]}"]
        ema2 = row[f"ema{ema_periods[2]}"]
        gap1 = ema1 - ema0
        gap2 = ema2 - ema0

        if gap1 < 0 and gap2 < 0:
            return "long"
        elif gap1 > 0 and gap2 > 0:
            return "short"
        #else:
        #    raise ValueError("There is no signal in the first line, but there should be")
