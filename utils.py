import pandas as pd
import os
import numpy as np
from calculations import getCloseTimes , calculateEmaValues , arrangementOfEmaValues , pullData15m, checkPositionSignal , getSignalsTime


def extractSignals(datas15m , date):        
    data15m , candles= pullData15m(datas15m)
    closeTimes = getCloseTimes(data15m)
    emaValues = calculateEmaValues(closeTimes)
    organisedEmaValues = arrangementOfEmaValues(emaValues , candles)
    firstSignal , organisedEmaValues = checkPositionSignal(organisedEmaValues)
    signals = getSignalsTime(firstSignal , organisedEmaValues )
    return signals

def convertCsvToParquet(csv1s,parquet1s) :

    if not os.path.exists(parquet1s):
        df = pd.read_csv(csv1s, usecols=[0, 1])
        df.to_parquet(parquet1s, index=False)
    else:
        df = pd.read_parquet(parquet1s)
    data1s = df.to_numpy()
    np.set_printoptions(formatter={'float_kind': lambda x: "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)})
    return data1s

def findPurchasePoints(currentValue,signal):
    valuesList = []
    testValue = currentValue
    for _ in range(20):
        accumulateProcessPointValue = currentValue * 0.005 / 100
        if signal == "long":                    
            pointValue = testValue - accumulateProcessPointValue
            valuesList.append(round(pointValue,2))
        else : 
            pointValue = testValue + accumulateProcessPointValue
            valuesList.append(round(pointValue,2))
        testValue = pointValue
    return valuesList