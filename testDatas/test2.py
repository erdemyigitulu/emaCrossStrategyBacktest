import csv
import json
import numpy as np
from main import calculateEma
from random import choice
import pandas as pd
import os

main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
signalscsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\signals.csv"
resultscsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\results.csv"

class Machine():
    def __init__(self):
        self.currentPnL = 0
        self.tradesList = []
        self.stage1Start = True
        self.stage2Start = False
        self.stage3Start = False
        self.stage1Phase1 = False
        self.stage3Phase1 = False
        self.stage3Phase2 = False
        self.stage3Phase3 = False
        self.entryStop = False
        self.stopLoss = False
        self.sellPoint1 = False
        self.sellPoint2 = False
        self.sellPoint3 = False
        self.protectProcess1 = False
        self.increaseStopPoint1 = False
        self.increaseStopPoint2 = False
        self.increaseStopPoint3 = False

    def stage1(self):
        if self.stage1Start :
            # if (self.currentPnL < 0.2) and not self.stage1Phase1 :
                self.stopLoss = True
                self.sellPoint1 = True
                self.protectProcess1 = True
            # else :
            #     self.stopLoss = False
            #     self.entryStop = True
            #     self.stage1Phase1 = True
  
    def stage2(self):
        self.stage1Start = False
        if self.stage2Start :
            self.entryStop = True
            self.sellPoint1 = False
            self.sellPoint2 = True

    def stage3(self):
        self.stage2Start = False
        if self.stage3Start:
            self.sellPoint2 = False
            self.sellPoint3 = True
            if (self.currentPnL < 0.65) and not self.stage3Phase1 :
                self.increaseStopPoint1 = True
                self.stage3Phase1 = True
            elif (0.65 <= self.currentPnL < 0.8) and not self.stage3Phase2 :
                self.increaseStopPoint1 = False
                self.increaseStopPoint2 = True
                self.stage3Phase2 = True
            elif(self.currentPnL >= 0.8) and not self.stage3Phase3:
                self.increaseStopPoint2 = False
                self.increaseStopPoint3 = True
                self.stage3Phase3 = True

def percentageIncrease (firstValue,SecondValue,signal):
        percentage = ((SecondValue - firstValue) / firstValue) * 100
        percentage = round(percentage,2)
        if signal == "short" :
            percentage = -(percentage)
        return percentage


def pullData15m ():
    with open(main15mcsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        datas = []
        for row in csv_reader:
            data = {"timeStamp":int(row[0] ), "closeTime": float(row[4]),"openTime": float(row[1])}
            datas.append(data)
        csv_file.close()
        return datas

def backTestofMachine () :
    resultscsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\results.csv"

    main1parquet = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main1s.parquet"
    df = pd.read_parquet(main1parquet)
    data1s = df.to_numpy()
    np.set_printoptions(formatter={'float_kind': lambda x: "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)})
    margin = 30
    datas = pullData15m()
    def calculateAvaregePrice(islemler):
        totalCost = sum(fiyat * miktar for fiyat, miktar in islemler)
        totalAmount = sum(miktar for _, miktar in islemler)
        ortalama = totalCost / totalAmount
        return ortalama , totalAmount
    def moneyProfitLossFunc(profitLoss , money , pnL , portion):
        print(profitLoss , money , pnL, portion )
        if profitLoss == 0 :
            profitLoss = ((money * (100 + pnL)/100 )- money) * portion
            print(profitLoss, "1") 
        else :
            profitLoss = profitLoss + ((money * (100 + pnL)/100 )- money) * portion
            print(profitLoss , "2")
        return profitLoss
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
    def calculatingEma () :
        dayOfEma = [5,8,13]
        emaDatasOfDays = []
        for day in dayOfEma :
            emaDataOfDay = calculateEma(datas,day)
            emaDatasOfDays.append(emaDataOfDay)
        return emaDatasOfDays , datas
    def arrangementOfEmaValues (emaValues,datas) :
        ema5List = emaValues[0]
        ema8List = emaValues[1]
        ema13List = emaValues[2]
        minSize = min(len(ema5List), len(ema8List), len(ema13List))
        ema5List = ema5List[-minSize:]
        ema8List = ema8List[-minSize:]
        ema13List = ema13List[-minSize:]
        zipList = zip(ema5List, ema8List, ema13List)
        lastTimeStamp = int(datas[-1]["timeStamp"])
        timeStampgap = int(datas[-1]["timeStamp"]) - int(datas[-2]["timeStamp"])
        firstTimeStamp = lastTimeStamp - ((minSize * timeStampgap) - timeStampgap)
        emaValues = []
        for arrange in zipList :
            emaData = {"timestamp":firstTimeStamp , "ema5":arrange[0] , "ema8":arrange[1] , "ema13" : arrange[2]}
            firstTimeStamp = firstTimeStamp + timeStampgap
            emaValues.append(emaData)
        del emaValues[:50]
        return emaValues
    def checkFirstSignal (arrangementEma):
        for index , value in enumerate(arrangementEma) :
            ema5 = value["ema5"]
            ema8 = value["ema8"]
            ema13 = value["ema13"]
            emagap1 = ema8 - ema5 
            emagap2 = ema13 - ema5
            if emagap1 < 0 and emagap2 < 0 :
                whichSideOnSignal = ["long"]
            elif emagap1 > 0 and emagap2 > 0 :
                whichSideOnSignal = ["short"]
            break
        if index != 0 :
            arrangementEma = arrangementEma[index:]
        return whichSideOnSignal , arrangementEma
    def getSignalsTime(firstSide,emaValues):
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
                elif (ema5First > ema8First > ema13First) or (ema5First > ema13First > ema8First):
                    if ema5Next < ema8Next and ema5Next < ema13Next:
                        if signalDatas[-1][0] != "short":
                            lst = ["short", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
                elif (ema5First < ema8First < ema13First) or (ema5First < ema13First < ema8First) :
                    if ema5Next > ema8Next and ema5Next > ema13Next :
                        if signalDatas[-1][0] != "long":
                            lst = ["long", emaValues[index + 1]["timestamp"]]
                            signalDatas.append(lst)
        except :
            pass
        return signalDatas
    def calculatingCurrentEma(timeStamp , price , signal ):
        with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            datas = []
            for row in csv_reader:
                data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
                datas.append(data)
            csv_file.close()
        for index, data in enumerate(datas) :
            datatimestamp = timeStamp - data['timeStamp']
            if datatimestamp < 0 :
                del datas[index - 1 :]
                break
        datas.append({"timeStamp":timeStamp, "closeTime": price})
        emaDataOfDay = calculateEma(datas,5)
        emaDatas = [emaDataOfDay[-2],emaDataOfDay[-1]]
        if signal == "short" :
            emaDatas = list(map(lambda x: -1 * x, emaDatas))
        if emaDatas [-1] < emaDatas[-2] :
            protectProcess = True
        return protectProcess
    emaDatasOfDays , datas = calculatingEma()
    arrangementEma = arrangementOfEmaValues(emaDatasOfDays , datas)
    firstSignal , arrangementEmaFinal  = checkFirstSignal(arrangementEma)
    signals = getSignalsTime(firstSignal , arrangementEmaFinal)
    firstTimeStamp = 1698796800000
    resultDatas = []
    totalpnL = 0
    profit = 0
    loss = 0
    profits = 0
    losss = 0
    entryStops = 0
    for index , signal in enumerate(signals[1:]) :
        print(signal)
        nextSignal = signals[(index + 2)][1]
        startProcessTimeStamp = signal[1]
        timeStampGap = int(((startProcessTimeStamp + 909000) - firstTimeStamp ) / 1000)
        firstValue = data1s[timeStampGap][1]
        purchasePoints = findPurchasePoints(firstValue,signal[0])
        startProcessValue = (firstValue,5000)
        seperateMoney = 500
        purchasedPoints = []
        messages = []
        purchasedPoints.append(startProcessValue)
        profitLoss = 0
        portion = 1
        a = True
        b = True
        c = True
        aa = True
        bb = True
        machine = Machine()
        for past in zip(range((timeStampGap + 9000), len(data1s)), data1s[(timeStampGap):]):
            currentValue = past[1][1]
            currentTimeStamp =int(past[1][0]) - 9000
            # print(currentTimeStamp , past)
            for point in purchasePoints :
                if currentValue <= point and signal[0] == "long" :
                    if not (point,seperateMoney) in purchasedPoints :
                        purchasedPoints.append((point,seperateMoney))
                elif currentValue >= point and signal[0] == "short" :
                    if not (point,seperateMoney) in purchasedPoints :
                        purchasedPoints.append((point,seperateMoney))
            avaregePrice , totalAmount = calculateAvaregePrice(purchasedPoints)
            pnL = percentageIncrease(avaregePrice , currentValue , signal[0] )
            # print(pnL,currentTimeStamp,currentValue,firstValue,signal[0], machine.increaseStopPoint1,machine.increaseStopPoint2,machine.increaseStopPoint3,machine.stage3Phase2,machine.stage3Phase1)
            print(pnL,firstValue,avaregePrice,f"SL:{machine.stopLoss}" ,f"ET:{machine.entryStop}",f"S1:{machine.stage1Start}" ,f"S2:{machine.stage2Start}",f"S3:{machine.stage3Start}",f"SP1:{machine.sellPoint1}" ,f"SP2:{machine.sellPoint2}",f"SP3:{machine.sellPoint3}",f"IP1:{machine.increaseStopPoint1}" ,f"IP2:{machine.increaseStopPoint2}",f"IP3:{machine.increaseStopPoint3}")
            machine.currentPnL = pnL
            if machine.stage1Start :
                machine.stage1()
            if machine.stage2Start :
                machine.stage2()
            if machine.stage3Start :
                machine.stage3()
            if machine.stopLoss and pnL <= -0.2:
                profitLoss = moneyProfitLossFunc(0 , totalAmount , pnL , portion)
                message = "STOPKE"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("STOPKE")
                break
            if machine.entryStop and pnL <= 0.04 :
                if machine.stage1Start :
                    message = "Stage 1 de entry stop yaptım kanks"
                    messages.append(message)
                    print("Stage 1 de entry stop yaptım kanks")
                else:
                    portion = portion - 0.5
                    profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion)
                    message = "Stage 2 de entry stop yaptım kanks"
                    messages.append(message)
                    print("Stage 2 de entry stop yaptım kanks")
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                break
            if machine.stage1Start and machine.sellPoint1 and pnL >= 0.3 and aa:
                portion = portion - 0.5
                profitLoss = moneyProfitLossFunc(0 , totalAmount , pnL , portion )
                message = "stage1 bitti kar aldım devamke"
                messages.append(message)
                print("stage1 bitti kar aldım devamke")
                aa = False
            if machine.stage2Start and machine.sellPoint2 and pnL >= 0.5 and bb :
                portion = portion - 0.25
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "stage2 bitti kar aldım devamke"
                messages.append(message)
                bb = False
            if machine.stage3Start and machine.sellPoint3 and pnL >= 1 :
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "işlem tam karla kapatılıyor"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("işlem tam karla kapatılıyor")
                break
            if machine.increaseStopPoint1 and pnL == 0.19:
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "stage2 de 0.5 den kar aldım 0.15 de stop oluyorum"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("stage2 de 0.5 den kar aldım 0.15 de stop oluyorum ")
                break
            if machine.increaseStopPoint2 and pnL <= 0.34 :
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "stage3 de 0.65 e kadar yükselip 0.3 de stop oldum"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("stage3 de 0.65 e kadar yükselip 0.3 de stop oldum")
                break
            if machine.increaseStopPoint3 and pnL <= 0.54:
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "stage 3 de 0.8 e gelip 0.5 de stop oluyorum"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("stage 3 de 0.8 e gelip 0.5 de stop oluyorum")
                break
            if currentTimeStamp > nextSignal + 900000 :
                profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                message = "yeni sinyal geldiği için işlemi kapatıyorumke"
                messages.append(message)
                resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss })
                print("yeni sinyal geldiği için işlemi kapatıyorumke")
                break
            if a :
                print("Stage1 başladı")
                a = False
            if pnL >= 0.3 and b :
                machine.stage2Start = True
                print("Stage2 başladı")
                b = False
            if pnL >= 0.5 and c :
                machine.stage3Start = True
                print("Stage3 başladı")
                c = False        
        
        if profitLoss < 0:
            loss = loss + profitLoss
            losss = losss + 1
        elif profitLoss > 0:
            profit = profit + profitLoss
            profits = profits + 1
        else :
            entryStops = entryStops + 1
        
        totalpnL = totalpnL + profitLoss
        purchasedPoints = ''.join([f"({x[0]}, {x[1]})" for x in purchasedPoints])
        resultDatas[-1]["purchasedPoints"] = purchasedPoints
        resultDatas[-1]["situationOfProcess"] = messages
        resultDatas[-1]["totalPnL"] = totalpnL
        resultDatas[-1]["totalProfit"] = (profit,profits)
        resultDatas[-1]["totalLoss"] = (loss,losss)
        resultDatas[-1]["totalEntryStop"] = entryStops
        
        with open(resultscsv, 'w' , encoding='utf-8' ) as json_file:
            json.dump(resultDatas, json_file, indent=4, separators=(',',': '),ensure_ascii=False)
    


backTestofMachine ()


