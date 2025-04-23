import pandas as pd
from config.config import Config
from data_paths.path_provider import PathProvider 
from indicators.base_indicator import BaseIndicator
from services.entry_points_generator import EntryPointGenerator

class SignalService:
    def __init__(self , config:Config, path_provider:PathProvider, base_indicator:BaseIndicator, entry_point_generator:EntryPointGenerator):
        self.config = config
        entry_point_generator
        self.path_provider = path_provider
        self.base_indicator = base_indicator
        self.dataFrame = None

    def extractSignals(self,previousSignal,isFirstMonth, carrySignal, month, year):
        self._getDataFrame(month, year)
        self.dataFrameWithIndicators = self.base_indicator.applyIndicators(self.dataFrame)
        if isFirstMonth:
            firstSignalSide = self._checkFirstSignalOfPosition(self.dataFrameWithIndicators)
        else:
            firstSignalSide = previousSignal[0]
            raise ValueError("Initial signal direction could not be determined.")
        signals = self._getSignalsTime(carrySignal ,firstSignalSide, self.dataFrameWithIndicators)
        return signals[1:]
    
    def _getDataFrame(self, month, year):
        path = self.path_provider.get15mCsvPath(month, year)
        self.dataFrame = pd.read_csv(path , names=self.config.COLUMN_NAMES)
        self.dataFrame[self.config.COLUMN_NAMES[0]] = self.dataFrame[self.config.COLUMN_NAMES[0]].astype("int64")
        return self.dataFrame
        
    def _getSignalsTime(self, carrySignal, firstSignalSide, dataFrame):
        signalDatas = []
        if not carrySignal == []:
            opposite = "short" if carrySignal["side"] == "long" else "long"
            signalDatas.append({"side": opposite, "timestamp": carrySignal["timestamp"]})
            signalDatas.append(carrySignal)
        else:
            signalDatas.append({"side": firstSignalSide, "timestamp": 0})
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
                    if signalDatas[-1]["side"] != "long":
                        signalDatas.append({"side": "long", "timestamp": row_next["OpenTime"]})
                elif ema1_next < ema2_next and ema1_next < ema3_next:
                    if signalDatas[-1]["side"] != "short":
                        signalDatas.append({"side": "short", "timestamp": row_next["OpenTime"]})

            elif ema1_now > ema2_now > ema3_now:
                if ema1_next < ema2_next and ema1_next < ema3_next:
                    if signalDatas[-1]["side"] != "short":
                        signalDatas.append({"side": "short", "timestamp": row_next["OpenTime"]})

            elif ema1_now < ema2_now < ema3_now:
                if ema1_next > ema2_next and ema1_next > ema3_next:
                    if signalDatas[-1]["side"] != "long":
                        signalDatas.append({"side": "long", "timestamp": row_next["OpenTime"]})

        except Exception as e:
            print("Error in getSignalsTime:", e)
        input(signalDatas)
        return signalDatas  

    def _checkFirstSignalOfPosition(self, dataFrame):
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
