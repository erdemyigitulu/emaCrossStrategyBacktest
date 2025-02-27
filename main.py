from config import *
import requests
from urllib.parse import urljoin
import time
import json
import csv

baseUrl = "https://fapi.binance.com/"

def getCandles (symbol,interval,limit):
    params = {
        "symbol" : symbol,
        "interval" : interval,
        "limit" : limit,
    }
    url = urljoin(baseUrl,"fapi/v1/klines")
    response = requests.get(url, params).json()
    return response

def getCloseTimes (candles):
    data = []
    for candle in candles :
        datas = {"timeStamp":candle["timeStamp"], "closeTime" : candle["closeTime"]}
        data.append(datas)
    return data

def calculateEma(dataOfEma,day):

    data = []
    for closetime in dataOfEma :
        close = closetime["closeTime"]
        data.append(close)
    emaValues = []
    multiplier = 2 / (day + 1)
    initialEma = sum(data[:day]) / day
    emaValues.append(initialEma)
    for i in range(day, len(data)):
        ema = (data[i] - emaValues[-1]) * multiplier + emaValues[-1]
        emaValues.append(ema)
    return emaValues 

def calculateEmaValues (closeTimes) :
    dayOfEma = [5,8,13]
    emaDatasOfDays = []
    for day in dayOfEma :
        emaDataOfDay = calculateEma(closeTimes,day)
        emaDatasOfDays.append(emaDataOfDay)
    return emaDatasOfDays 

def arrangementOfEmaValues (emaValues , candles) :
    ema5List = emaValues[0]
    ema8List = emaValues[1]
    ema13List = emaValues[2]
    print(len(ema13List),len(ema5List),len(ema8List))
    minSize = min(len(ema5List), len(ema8List), len(ema13List))
    ema5List = ema5List[-minSize:]
    ema8List = ema8List[-minSize:]
    ema13List = ema13List[-minSize:]
    zipList = zip(ema5List, ema8List, ema13List)
    lastTimeStamp = int(candles[-1][0])
    timeStampgap = int(candles[-1][0]) - int(candles[-2][0])
    firstTimeStamp = lastTimeStamp - ((minSize * timeStampgap) - timeStampgap)
    emaValues = []
    for arrange in zipList :
        emaData = {"timestamp":firstTimeStamp , "ema5":arrange[0] , "ema8":arrange[1] , "ema13" : arrange[2]}
        firstTimeStamp = firstTimeStamp + timeStampgap
        emaValues.append(emaData)
    del emaValues[:50]
    return emaValues

def isCrossEmaValues (emaValues):
    emaLast = emaValues[-2]
    emaSecondLast = emaValues[-3]
    if emaSecondLast["ema5"] > emaSecondLast["ema8"] or emaSecondLast["ema5"] > emaSecondLast["ema13"]: 
        if emaLast["ema5"] < emaLast["ema8"] and emaLast["ema5"] < emaLast["ema13"]:
            print("SHORTLA ")
    elif emaSecondLast["ema5"] < emaSecondLast["ema8"] or emaSecondLast["ema5"] < emaSecondLast["ema13"] :
        if emaLast["ema5"] > emaLast["ema8"] and emaLast["ema5"] > emaLast["ema13"]:
            print("LONGLA")

def checkPositionSignal (emaValues) :
    for index , value in enumerate(emaValues) :
        ema5 = value["ema5"]
        ema8 = value["ema8"]
        ema13 = value["ema13"]
        emagap1 = ema8 - ema5 
        emagap2 = ema13 - ema5
        if emagap1 < 0 and emagap2 < 0 :
            whichSideOnSignal = ["long"]
            break
        elif emagap1 > 0 and emagap2 > 0 :
            whichSideOnSignal = ["short"]
            break
    if index != 0 :
        emaValues = emaValues[index:]
    return whichSideOnSignal , emaValues
   
def getSignalsTime (firstSide , emaValues , date) :
    signalDatas = []
    signalDatas.append(firstSide)
    try :
        for index, value in enumerate(emaValues):
            ema5First = value["ema5"]
            ema8First = value["ema8"]
            ema13First = value["ema13"]
            ema5Next = emaValues[index + 1]["ema5"]
            ema8Next = emaValues[index + 1]["ema8"]
            ema13Next = emaValues[index + 1]["ema13"]
            if (ema8First < ema5First < ema13First) or (ema13First < ema5First < ema8First):
                if ema5Next > ema8Next and ema5Next > ema13Next:
                    if signalDatas[-1][0] != "long":
                        lst = ["long", emaValues[index + 1]["timestamp"]]
                        signalDatas.append(lst)
                elif ema5Next < ema8Next and ema5Next < ema13Next:
                    if signalDatas[-1][0] != "short":
                        lst = ["short", emaValues[index + 1]["timestamp"]]
                        signalDatas.append(lst)
            elif ema5First > ema8First > ema13First:
                if ema5Next < ema8Next and ema5Next < ema13Next:
                    if signalDatas[-1][0] != "short":
                        lst = ["short", emaValues[index + 1]["timestamp"]]
                        signalDatas.append(lst)
            elif ema5First < ema8First < ema13First:
                if ema5Next > ema8Next and ema5Next > ema13Next :
                    if signalDatas[-1][0] != "long":
                        lst = ["long", emaValues[index + 1]["timestamp"]]
                        signalDatas.append(lst)
    except :
        pass

    return signalDatas
def getCandleDepo ():
    url = urljoin(baseUrl,"/fapi/v1/time")
    response = requests.get(url).json()
    currentTime = response["serverTime"]
    isRightNow = False
    startTime = 1698796830000
    while not isRightNow :
        endTime = startTime + (87000000)
        if (currentTime - endTime) < 0 :
            isRightNow = True
        params = {
            "symbol" : "btcusdt",
            "interval" : "1m",
            "startTime" : startTime,
            "endTime" : endTime
        }
        url = urljoin(baseUrl,"/fapi/v1/klines")
        response = requests.get(url, params).json()
        time.sleep(1)
        markPriceDepoJson2 = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\markPriceDepo2.json"
        with open(markPriceDepoJson2, encoding='utf-8') as f:
            markPriceDepo = json.load(f)
        for data in response :
            markPriceDepo.append(data)
        with open(markPriceDepoJson2, 'w' , encoding='utf-8' ) as json_file:
            json.dump(markPriceDepo, json_file, indent=4, separators=(',',': '),ensure_ascii=False)
        startTime = endTime + 87000000

# run = True
# while run :
#     print("şimdi")
#     candles = getCandles("BTCUSDT","15m",1000)
#     closeTimes = getCloseTimes (candles)
#     emaValues = calculateEmaValues(closeTimes)
#     liveEmaValues = { "ema5":emaValues[0][-1] , "ema8":emaValues[1][-1], "ema13":emaValues[2][-1]}
#     response2 = arrangementOfEmaValues(emaValues , candles)
#     print(liveEmaValues)
    

