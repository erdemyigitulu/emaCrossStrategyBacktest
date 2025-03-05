import pandas as pd
import os
import numpy as np
from calculations import getCloseTimes , calculateEmaValues , arrangementOfEmaValues , pullData15m, checkPositionSignal , getSignalsTime
from config import backtestConfigs

def extractSignals(datas15m):        
    data15m , candles= pullData15m(datas15m)
    closeTimes = getCloseTimes(data15m)
    emaValues = calculateEmaValues(closeTimes)
    organisedEmaValues = arrangementOfEmaValues(emaValues , candles)
    firstSignal , organisedEmaValues = checkPositionSignal(organisedEmaValues)
    signals = getSignalsTime(firstSignal , organisedEmaValues)
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

def extractPurchasedPoints (signal , data1s) :
    entryMoney = backtestConfigs()[4]
    startProcessTimeStamp = int(signal[1]) + 900000
    timestamp_column = data1s[:, 0]
    startIndex = np.argmax(timestamp_column >= startProcessTimeStamp)
    firstValue = data1s[startIndex][1]
    purchasePoints = findPurchasePoints(firstValue,signal[0])
    startProcessValue = (firstValue,entryMoney)
    purchasedPoints = []
    purchasedPoints.append(startProcessValue)
    return purchasePoints , purchasedPoints , startIndex , startProcessTimeStamp , firstValue

def improvingPurchasedPoints ( signal , purchasedPoints , purchasePoints , past , seperateMoney) :
                        currentValue = past[1]
                        currentTimeStamp =int(past[0]) 
                        for point in purchasePoints :
                            if currentValue <= point and signal[0] == "long" :
                                if not (point,seperateMoney) in purchasedPoints :
                                    purchasedPoints.append((point,seperateMoney))
                            elif currentValue >= point and signal[0] == "short" :
                                if not (point,seperateMoney) in purchasedPoints :
                                    purchasedPoints.append((point,seperateMoney))
                            return purchasedPoints , currentValue , currentTimeStamp