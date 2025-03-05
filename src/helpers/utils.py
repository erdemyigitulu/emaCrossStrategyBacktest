import pandas as pd
import os
import numpy as np


class Utils:
    def convertCsvToParquet(csv1s, parquet1s):
        if not os.path.exists(parquet1s):
            df = pd.read_csv(csv1s, usecols=[0, 1])
            df.to_parquet(parquet1s, index=False)
        else:
            df = pd.read_parquet(parquet1s)
        data1s = df.to_numpy()
        np.set_printoptions(
            formatter={
                "float_kind": lambda x: (
                    "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)
                )
            }
        )
        return data1s

    def arrangementOfEmaValues(emaValues, candles):
        ema5List = emaValues[0]
        ema8List = emaValues[1]
        ema13List = emaValues[2]
        print(len(ema13List), len(ema5List), len(ema8List))
        minSize = min(len(ema5List), len(ema8List), len(ema13List))
        ema5List = ema5List[-minSize:]
        ema8List = ema8List[-minSize:]
        ema13List = ema13List[-minSize:]
        zipList = zip(ema5List, ema8List, ema13List)
        lastTimeStamp = int(candles[-1][0])
        timeStampgap = int(candles[-1][0]) - int(candles[-2][0])
        firstTimeStamp = lastTimeStamp - ((minSize * timeStampgap) - timeStampgap)
        emaValues = []
        for arrange in zipList:
            emaData = {
                "timestamp": firstTimeStamp,
                "ema5": arrange[0],
                "ema8": arrange[1],
                "ema13": arrange[2],
            }
            firstTimeStamp = firstTimeStamp + timeStampgap
            emaValues.append(emaData)
        del emaValues[:50]
        return emaValues
