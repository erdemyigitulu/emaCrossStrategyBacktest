import pandas as pd
from pandas import DataFrame
from config.config import Config
from data_paths.path_provider import PathProvider 
from indicators.base_indicator import BaseIndicator

class SignalService:
    def __init__(self , config:Config, path_provider:PathProvider, base_indicator:BaseIndicator):
        self.config = config
        self.path_provider = path_provider
        self.base_indicator = base_indicator
        self.dataFrame = None

    def extractSignals(self,previous_month_last_signal,isFirstMonth, carrySignal, month, year):
        self._getDataFrame(month, year)
        self.dataFrameWithIndicators = self.base_indicator.applyIndicators(self.dataFrame)
        if isFirstMonth:
            firstSignalType = self._checkFirstSignalOfPosition(self.dataFrameWithIndicators)
        else:
            print("Previous month last signal:",  previous_month_last_signal)
            firstSignalType = previous_month_last_signal[0]['Type']
            raise ValueError("Initial signal direction could not be determined.")
        signals = self._getSignalsTime(carrySignal ,firstSignalType, self.dataFrameWithIndicators)
        return signals[1:]
    
    def _getDataFrame(self, month, year):
        path = self.path_provider.get15mCsvPath(month, year)
        self.dataFrame = pd.read_csv(path , names=self.config.COLUMN_NAMES)
        self.dataFrame[self.config.COLUMN_NAMES[0]] = self.dataFrame[self.config.COLUMN_NAMES[0]].astype("int64")
        return self.dataFrame
        
    def _getSignalsTime(self, carrySignal, firstSignalType, dataFrame: DataFrame):
        signalDatas = []
        if carrySignal:
            opposite = "short" if carrySignal["Type"] == "long" else "long"
            signalDatas.append({"Type": opposite})
            signalDatas.append(carrySignal)
        else:
            signalDatas.append({"Type": firstSignalType, "timestamp": 0})

        ema_periods = self.config.daysOfEma
        if len(ema_periods) < 3:
            raise ValueError("En az 3 EMA değeri olmalı")

        ema1_col = f"ema{ema_periods[0]}"
        ema2_col = f"ema{ema_periods[1]}"
        ema3_col = f"ema{ema_periods[2]}"

        try:
            rows = list((dataFrame[[ema1_col, ema2_col, ema3_col, "OpenTime"]]).itertuples(index=False))
            for current, next_row in zip(rows, rows[1:]):
                ema1_now, ema2_now, ema3_now, _ = current
                ema1_next, ema2_next, ema3_next, open_time_next = next_row

                if (ema2_now < ema1_now < ema3_now) or (ema3_now < ema1_now < ema2_now):
                    if ema1_next > ema2_next and ema1_next > ema3_next:
                        if signalDatas[-1]["Type"] != "long":
                            signalDatas.append({"Type": "long", "timestamp": open_time_next})
                    elif ema1_next < ema2_next and ema1_next < ema3_next:
                        if signalDatas[-1]["Type"] != "short":
                            signalDatas.append({"Type": "short", "timestamp": open_time_next})

                elif ema1_now > ema2_now > ema3_now:
                    if ema1_next < ema2_next and ema1_next < ema3_next:
                        if signalDatas[-1]["Type"] != "short":
                            signalDatas.append({"Type": "short", "timestamp": open_time_next})

                elif ema1_now < ema2_now < ema3_now:
                    if ema1_next > ema2_next and ema1_next > ema3_next:
                        if signalDatas[-1]["Type"] != "long":
                            signalDatas.append({"Type": "long", "timestamp": open_time_next})

        except KeyError as e:
            raise KeyError(f"DataFrame içinde beklenen EMA kolonları eksik: {e}")
        except Exception as e:
            raise RuntimeError(f"Beklenmeyen hata oluştu: {e}")

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
