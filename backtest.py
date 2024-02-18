import csv
import json
import numpy as np
from main import calculatEmaValues , calculateEma
from experta import *
from random import choice


class TradeManagement(Fact):
    pass

class TradeEngine(KnowledgeEngine):
    def calculatingCurrentEma (timestamp , price):
        main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
        with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            datas = []
            for row in csv_reader:
                data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
                datas.append(data)
            csv_file.close()
        for index, data in enumerate(datas) :
            datatimestamp = timestamp - data['timeStamp']
            if datatimestamp < 0 :
                del datas[index - 1 :]
                break
        datas.append({"timeStamp":timestamp, "closeTime": price})
        emaDataOfDay = calculateEma(datas,5)
        return [emaDataOfDay[-1] , emaDataOfDay[-2]] 
    stopLossStage1 = False
    stopLossStage2 =False
    stopLossStage3 = False
    profitStage1 = False
    profitStage2 = False
    profitStage3 = False
    earlyClosePosition = False

    
    @Rule((TradeManagement(pnL=P(lambda x: x <= -0.2))))
    def StopLoss1(self):
        self.stopLossStage1 = True

    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)), NOT(TradeManagement(action="profitStage1")), NOT(TradeManagement(action2="profitStage2")), NOT(TradeManagement(action3="profitStage3"))))
    def profStage1(self):
        self.profitStage1 = True
        self.declare(TradeManagement(action="profitStage1"))

    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.5)), TradeManagement(action="profitStage1")), NOT(TradeManagement(action2="profitStage2")), NOT(TradeManagement(action3="profitStage3")))
    def profStage2(self):
        self.profitStage2= True
        self.declare(TradeManagement(action2="profitStage2"))

    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 1 )),  TradeManagement(action="profitStage1")), TradeManagement(action2="profitStage2"), NOT(TradeManagement(action3="profitStage3")))
    def profStage3(self):
        self.profitStage3 = True
        self.declare(TradeManagement(action3="profitStage3"))

    @Rule(TradeManagement(action2="profitStage2"))
    def stopLoss2(self):
        self.stopLossStage2 = True
    
    @Rule(TradeManagement(action3="profitStage3"))
    def stopLoss3(self):
        self.stopLossStage3 = True
    
    @Rule(TradeManagement(timeStamp=P(lambda x: x), price=P(lambda y: y)))
    def calculatingCurrentEma(self):
        tradeFacts = self.facts[1]
        timeStamp = tradeFacts['timeStamp']
        price = tradeFacts['price']
        signal = tradeFacts["signal"]
        main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
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
            self.earlyClosePosition = True
            print("İşlem ilk iki mumda terse hareket ettiği için erken kapatılıyor")

        



def backTestofMachine () :
    main1scsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main1s.csv"
    data1s = np.genfromtxt(main1scsv, delimiter=',', usecols=(0, 1))
    np.set_printoptions(formatter={'float_kind': lambda x: "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)})
    main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"

    def calculatingEma () :
        with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            datas = []
            for row in csv_reader:
                data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
                datas.append(data)
            csv_file.close()
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
                break
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
                print
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
    def percentageIncrease (firstValue,SecondValue):
        percentage = ((SecondValue - firstValue) / firstValue) * 100
        percentage = round(percentage,2)
        return percentage
    emaDatasOfDays , datas = calculatingEma()
    arrangementEma = arrangementOfEmaValues(emaDatasOfDays , datas)
    firstSignal , arrangementEmaFinal  = checkFirstSignal(arrangementEma)
    signals = getSignalsTime(firstSignal , arrangementEmaFinal)
    firstTimeStamp = 1698796800000
    money = 500
    margin = 30
    for index , signal in enumerate(signals[1:]):
        stage1Profit = False
        stage2Profit = False
        profitLoss = 0
        print(signal)
        input("işleme giriyorum")
        money = money - (money * 0.045 * 0.3)
        profitLoss = 0
        currentTimeStamp = int(signal[1])
        timeStampGap = int(((currentTimeStamp + 900000) - firstTimeStamp ) / 1000)
        firstValue = data1s[timeStampGap][1]
        engine = TradeEngine()
        engine.reset()
        for past in zip(range(timeStampGap, len(data1s)), data1s[(timeStampGap):]):
            currentValue = past[1][1]
            percentage = percentageIncrease(firstValue,currentValue)
            if signal[0] == "short" and percentage != 0 :
                percentage = -(percentage)
            if int(past[1][0]) - signal[1]  < 1800000 :
                engine.reset()
                engine.declare(TradeManagement(timeStamp = past[1][0] , price = past[1][1] , signal = signal[0]))
            engine.declare(TradeManagement(pnL=percentage))
            engine.run()
            if engine.earlyClosePosition :
                if profitLoss == 0 :
                    profitLoss = money * (percentage - 0.045) * margin / 100
                else :
                    profitLoss = profitLoss + money * (percentage - 0.045) * margin / 100
                break 
            if signals[index+2][1] <= int(past[1][0])  :
                print("işlem farklı sinyal aldığı için kapatıldı.")
                if profitLoss == 0 :
                    profitLoss = money * (percentage - 0.045) * margin / 100
                else :
                    profitLoss = profitLoss + money * (percentage - 0.045) * margin / 100
                break
            print( percentage , int(past[1][0]) , past[1][1] )
            
            if engine.stopLossStage1 :
                if profitLoss == 0 :
                    profitLoss = money * (percentage - 0.045) * margin / 100
                else :
                    profitLoss = profitLoss + money * (percentage - 0.045) * margin / 100 
                print("İşlem zararla stop oldu" , profitLoss )
                input("1")
                break
            if engine.profitStage1 and not stage1Profit :
                profitLoss = (money/2)* (percentage - 0.045) * margin / 100 
                print("İşlem 0.3 ten kar aldı devam ediyor" , profitLoss)
                stage1Profit = True
                input("2")
            if engine.profitStage2 and stage1Profit and not stage2Profit :
                profitLoss = profitLoss + (money/4 * (percentage - 0.045) * margin / 100) 
                print("İşlem 0.5 ten kar aldı devam ediyor" , profitLoss)
                stage2Profit = True
                input("3")
            if engine.profitStage3 and stage2Profit :
                profitLoss = profitLoss + (money/4) * (percentage - 0.045) * margin / 100 
                print("İşlem maksimum kar ederek kapandı" , profitLoss)
                input("4")
                break
            if engine.stopLossStage2 and stage1Profit and percentage == 0.1 :
                profitLoss = profitLoss + (money/4) * (percentage) * margin / 100 - (money/4 * margin / 100 * 0.045)
                print("İşlem 0.5 ten kar aldiktan sonra entry stop yaptı" , profitLoss)
                input("5")
                break
        money = money + profitLoss
        print(money)

             

    
backTestofMachine()
