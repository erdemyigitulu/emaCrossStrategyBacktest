import csv
import json
import numpy as np
from main import calculatEmaValues , calculateEma
from experta import *
from random import choice
import pandas as pd

main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
signalscsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\signals.csv"

class TradeManagement(Fact):
    isMachineActivated =  False

class TradeEngine(KnowledgeEngine):
    isMachineActivated = False
    stopLoss = False #İşlemin direkt stop olması
    wrongSignal =False #İşlem açılmadan kar noktasına ulaştı ve sinyal başarılı gerçekleşmedi
    protectProcess1 = False #İşlem kar almaya çok yaklaştıktan sonra terse harekette sinyal kapatılır.
    protectProcess2  = False #Ema ters yöne hareket başladığı için sinyal kapatılır 
    profit03 = False #Kar noktaları
    profit05 = False #Kar noktaları
    profit1 = False #Kar noktaları
    entryStop03 = False #Kar alındıktan sonra fiyat düşerse entry stop yapılır
    entryStop05 = False #Kar alındıktan sonra fiyat düşerse entry stop yapılır

    #MACHINE IS ACTIVATED
    @Rule(TradeManagement(isMachineActivated = True))
    def activatedMachine(self) :
        self.isMachineActivated= True

    #WRONG SİGNAL 
    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)) , TradeManagement(isMachineActivated = False)))
    def wrongSignalFunc(self):
        self.wrongSignal = True

    #STOPLOSS
    @Rule(AND(TradeManagement(pnL=P(lambda x: x <= -0.2)) , TradeManagement(isMachineActivated = True) , NOT(TradeManagement(profit03 = "active"))))
    def stopLossFunc(self) :
        self.stopLoss = True

    #PROFİT 1
    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)) , TradeManagement(isMachineActivated = True)))
    def profit03Func(self) :
        self.profit03 = True
        self.entryStop03 = True
        self.declare(TradeManagement(profit03 = "active"))

    #PROFİT 2
    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.5)) , TradeManagement(profit03 = "active")))
    def profit05Func(self) :
        self.profit05 = True
        self.entryStop05 = True
        self.declare(TradeManagement(profit05 = "active"))

    #PROFİT 3
    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 1)) , TradeManagement(profit05 = "active")))
    def profit1Func(self) :
        self.profit1 = True

    #PROTECTPROCESS 1
    @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.2)) , NOT(TradeManagement(profit03 = "active")) , (TradeManagement(isMachineActivated = True)) , NOT(TradeManagement(protectProcess1 = "active"))))
    def protectProcess1Func1(self) :
        self.declare(TradeManagement(protectProcess1 = "active"))
        self.protectProcess1 = True

def percentageIncrease (firstValue,SecondValue):
        percentage = ((SecondValue - firstValue) / firstValue) * 100
        percentage = round(percentage,2)
        return percentage

def pullData15m ():
    with open(main15mcsv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            datas = []
            for row in csv_reader:
                data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
                datas.append(data)
            csv_file.close()


def backTestofMachine () :
    main1scsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main1s.csv"
    resultscsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\results.csv"
    data1s = np.genfromtxt(main1scsv, delimiter=',', usecols=(0, 1))
    np.set_printoptions(formatter={'float_kind': lambda x: "{:.2f}".format(x) if x % 1 else "{:.0f}".format(x)})
    margin = 30
    def moneyProfitLossFunc(profitLoss , money , percentage , portion):
        if profitLoss == 0 :
            profitLoss = money/portion * (percentage - 0.018) * margin / 100
        else :
            profitLoss = profitLoss + money/portion * (percentage - 0.018) * margin / 100
        return profitLoss
    def calculatingEma () :
        datas = pullData15m ()
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
        protectProcess = False
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
            protectProcess = True
        return protectProcess
    emaDatasOfDays , datas = calculatingEma()
    arrangementEma = arrangementOfEmaValues(emaDatasOfDays , datas)
    firstSignal , arrangementEmaFinal  = checkFirstSignal(arrangementEma)
    signals = getSignalsTime(firstSignal , arrangementEmaFinal)
    firstTimeStamp = 1698796800000
    resultDatas = []
    totalMoney = 0
    for index , signal in enumerate(signals[1:]) :
        money = 500
        isPriceCame = False
        profit0point3 = False
        profit0point5 = False
        profitLoss = 0
        counter = 0
        nextSignalTimestamp = signals[index+2][1]
        fee = (money * 0.018 * 0.3)
        money = money - fee
        startProcessTimeStamp = signal[1]
        timeStampGap = int(((startProcessTimeStamp + 900000) - firstTimeStamp ) / 1000)
        firstValue = data1s[timeStampGap][1]
        if signal[0] == "short" :
            targetValue = firstValue + (firstValue * 0.05 / 100)
            comparisonValue = targetValue
        else :
            targetValue = firstValue - (firstValue * 0.1 / 100)
            comparisonValue = -(targetValue)
        engine = TradeEngine()
        engine.reset()
        for past in zip(range(timeStampGap, len(data1s)), data1s[(timeStampGap):]):
            currentValue = past[1][1]
            currentTimeStamp =past[1][0]
            if signal[0] == "long" :
                currentValue = -(currentValue)
            if currentValue >= comparisonValue :
                isPriceCame = True
            if isPriceCame :
                if counter == 0 :
                    startProcessTimeStamp = past[1][0] 
                    engine.declare(TradeManagement(isMachineActivated= True))
                if currentValue < 0 :
                    currentValue = -(currentValue)
                percentage = percentageIncrease(targetValue,currentValue)
                if signal[0] == "short" and percentage != 0 :
                    percentage = -(percentage)
                print(percentage , targetValue , currentValue , int(past[1][0]))
                engine.declare(TradeManagement(pnL = percentage))
                engine.run()
                if currentTimeStamp - startProcessTimeStamp < 1800000 :
                    earlyClosePosition = calculatingCurrentEma(currentTimeStamp ,currentValue , signal[0] )
                if engine.protectProcess1 and percentage < 0.05 and (currentTimeStamp - startProcessTimeStamp > 2700000) and not profit0point3 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 1)
                    message = "işlem açıldı ve alım noktasına çok yaklaştı ancak geri düştü ve işlem kapandı."
                    print(message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if engine.stopLoss :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 1)
                    message = "işlem zarar ederek kapandı"
                    print( message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if engine.profit03 and not profit0point3 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 2)
                    message = "işlem 0,3 den kar alarak devam ediyor."
                    print( message , profitLoss)
                    profit0point3 = True
                if engine.profit05 and not profit0point5 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 4)
                    message = "işlem 0,5 ten kar alarak devam ediyor."
                    print( message , profitLoss)
                    profit0point5 = True
                if engine.profit1 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 4)
                    message = "işlem 1 den kar alarak maksimum seviyeye geldi ve kapandı"
                    print(message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if engine.entryStop03 and percentage < -0.1 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 2)
                    message = "işlem 0.3 den kar aldıktan sonra entry stop yaptı"
                    print(message ,profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if engine.entryStop05 and percentage < 0.1 :
                    profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 4)
                    message = "işlem 0.5 den kar aldıktan sonra entry stop yaptı"
                    print(message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if ((nextSignalTimestamp + 900000) <= currentTimeStamp) and nextSignalTimestamp - startProcessTimeStamp > 900000 :
                    if not engine.profit03 and not profit0point5 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 1)
                    elif engine.profit03 and not engine.profit05 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 2)
                    elif engine.profit03 and engine.profit05 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 4)
                    message = "işlem farklı sinyal aldığı için kapatıldı."
                    print(message, profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if earlyClosePosition :
                    if not engine.profit03 and not profit0point5 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 1)
                    elif engine.profit03 and not engine.profit05 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 2)
                    elif engine.profit03 and engine.profit05 :
                        profitLoss = moneyProfitLossFunc(profitLoss , money , percentage , 4)
                    message = "İşlem ilk iki mumda terse hareket ettiği için erken kapatılıyor"
                    print(message, profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                counter +=1
            else :
                print(currentValue , currentTimeStamp , comparisonValue)
                if engine.wrongSignal and not engine.isMachineActivated :
                    message = "İşlem açılamadan kar noktasına ulaştı yeni sinyale geçiliyor"
                    profitLoss = 0
                    print(message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
                if nextSignalTimestamp <= currentTimeStamp and not engine.isMachineActivated and nextSignalTimestamp - startProcessTimeStamp > 900000 :
                    message = "işlem açılamadan diğer sinyal geldi.Diğerine geçildi"
                    profitLoss = 0
                    print(message , profitLoss)
                    resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":past[1][0] , "profitLoss":profitLoss , "situationOfProcess":message})
                    break
        totalMoney = totalMoney + profitLoss
        resultDatas.append({"totalMoney":totalMoney})
        with open(resultscsv, 'w' , encoding='utf-8' ) as json_file:
            json.dump(resultDatas, json_file, indent=4, separators=(',',': '),ensure_ascii=False)
        money = money + profitLoss
        print(money)
            
            

            

def howMachineStartPosition () :
    with open(main15mcsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        main15m = []
        for row in csv_reader:
            data1 = [row[0],row[1],row[2],row[3],row[4]]
            main15m.append(data1)
        csv_file.close()
    with open(signalscsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        signals = []
        for row in csv_reader:
            try :
                data2 = [row[0],row[1]]
                signals.append(data2)
            except :
                pass
        csv_file.close()
    datas = []
    for signal in signals :
        data = []
        for index , candle in enumerate(main15m) :
            if int(candle[0]) == int(signal[1]):
                if signal[0] == "long" :
                    variant = 3
                else :
                    variant = 2
                signalsTimeClose = candle[4]
                enterenceSignalLow = main15m[index + 1][variant]
                percentageOfClosetoLow = percentageIncrease(float(signalsTimeClose) , float(enterenceSignalLow))
                if signal[0] == "long" :
                    percentageOfClosetoLow = -(percentageOfClosetoLow)
                data = {"signalTimeStamp": candle[0] , "signalsTimeClose" : candle[4] , "enterenceSignalLow": enterenceSignalLow , "percentageIncrease" : percentageOfClosetoLow }
                datas.append(data)
                break
    percanteges = []
    sorted_datas = sorted(datas, key=lambda x: x["percentageIncrease"])  
    for data in datas :
        percentage = data['percentageIncrease']
        percanteges.append(percentage)

    df = pd.DataFrame(sorted_datas)
    pd.set_option('display.max_rows', None)
    print(df)
                
        
            
        
        
backTestofMachine()


        
    



    
    
            


    
# backTestofMachine()


# class TradeManagement(Fact):
#     pass

# class TradeEngine(KnowledgeEngine):
#     def calculatingCurrentEma (timestamp , price):
#         main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
#         with open(main15mcsv) as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
#             datas = []
#             for row in csv_reader:
#                 data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
#                 datas.append(data)
#             csv_file.close()
#         for index, data in enumerate(datas) :
#             datatimestamp = timestamp - data['timeStamp']
#             if datatimestamp < 0 :
#                 del datas[index - 1 :]
#                 break
#         datas.append({"timeStamp":timestamp, "closeTime": price})
#         emaDataOfDay = calculateEma(datas,5)
#         return [emaDataOfDay[-1] , emaDataOfDay[-2]] 
#     stopLossStage1 = False
#     stopLossStage2 =False
#     stopLossStage3 = False
#     profitStage1 = False
#     profitStage2 = False
#     profitStage3 = False
#     earlyClosePosition = False

    
#     @Rule((TradeManagement(pnL=P(lambda x: x <= -0.2))))
#     def StopLoss1(self):
#         self.stopLossStage1 = True

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)), NOT(TradeManagement(action="profitStage1")), NOT(TradeManagement(action2="profitStage2")), NOT(TradeManagement(action3="profitStage3"))))
#     def profStage1(self):
#         self.profitStage1 = True
#         self.declare(TradeManagement(action="profitStage1"))

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.5)), TradeManagement(action="profitStage1")), NOT(TradeManagement(action2="profitStage2")), NOT(TradeManagement(action3="profitStage3")))
#     def profStage2(self):
#         self.profitStage2= True
#         self.declare(TradeManagement(action2="profitStage2"))

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 1 )),  TradeManagement(action="profitStage1")), TradeManagement(action2="profitStage2"), NOT(TradeManagement(action3="profitStage3")))
#     def profStage3(self):
#         self.profitStage3 = True
#         self.declare(TradeManagement(action3="profitStage3"))

    

#     @Rule(TradeManagement(action2="profitStage2"))
#     def stopLoss2(self):
#         self.stopLossStage2 = True

#     @Rule(TradeManagement(action1="profitStage1"))
#     def stopLoss4(self):
#         self.stopLossStage3 = True
    
    
#     @Rule(TradeManagement(timeStamp=P(lambda x: x), price=P(lambda y: y)))
#     def calculatingCurrentEma(self):
#         tradeFacts = self.facts[1]
#         timeStamp = tradeFacts['timeStamp']
#         price = tradeFacts['price']
#         signal = tradeFacts["signal"]
#         main15mcsv = "C:\\Users\\ERDO\\Desktop\\moneyMachine\\backTestDatas\\main15m.csv"
#         with open(main15mcsv) as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
#             datas = []
#             for row in csv_reader:
#                 data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
#                 datas.append(data)
#             csv_file.close()
#         for index, data in enumerate(datas) :
#             datatimestamp = timeStamp - data['timeStamp']
#             if datatimestamp < 0 :
#                 del datas[index - 1 :]
#                 break
#         datas.append({"timeStamp":timeStamp, "closeTime": price})
#         emaDataOfDay = calculateEma(datas,5)
#         emaDatas = [emaDataOfDay[-2],emaDataOfDay[-1]]
#         if signal == "short" :
#             emaDatas = list(map(lambda x: -1 * x, emaDatas))
#         if emaDatas [-1] < emaDatas[-2] :
#             self.earlyClosePosition = True
#             print("İşlem ilk iki mumda terse hareket ettiği için erken kapatılıyor")




# for index , signal in enumerate(signals[1:]):
#         stage1Profit = False
#         stage2Profit = False
#         isMachineActive = False
#         isPriceCame = False
#         entryStopPosition  = False
#         profitLoss = 0
#         counter = 0
#         input(signal)
#         fee = (money * 0.045 * 0.3)
#         money = money - fee
#         currentTimeStamp = int(signal[1])
#         timeStampGap = int(((currentTimeStamp + 900000) - firstTimeStamp ) / 1000)
#         firstValue = data1s[timeStampGap][1]
#         if signal[0] == "short" :
#             targetValue = firstValue + (firstValue * 0.05 / 100)
#             comparisonValue = targetValue
#         else :
#             targetValue = firstValue - (firstValue * 0.05 / 100)
#             comparisonValue = -(targetValue)
#         engine = TradeEngine()
#         engine.reset()
#         for past in zip(range(timeStampGap, len(data1s)), data1s[(timeStampGap):]):
#             currentValue = past[1][1]
#             if signal[0] == "long" :
#                 currentValue = -(currentValue)
#             if currentValue >= comparisonValue :
#                 isPriceCame = True
#             if isPriceCame :
#                 if currentValue < 0 :
#                     currentValue = -(currentValue)
#                 if counter == 0 :
#                     input("THE MACHINE IS ACTIVATED")
#                 isMachineActive = True
#                 percentage = percentageIncrease(targetValue,currentValue)  
#                 if signal[0] == "short" and percentage != 0 :
#                     percentage = -(percentage)
#                 print( percentage , int(past[1][0]) , past[1][1] , comparisonValue) 
#                 if int(past[1][0]) - signal[1]  < 1800000 :
#                     engine.reset()
#                     engine.declare(TradeManagement(timeStamp = past[1][0] , price = past[1][1] , signal = signal[0]))
#                 engine.declare(TradeManagement(pnL=percentage))
#                 engine.run()
#                 if percentage >= 0.2 :
#                     entryStopPosition = True
#                 if entryStopPosition and not stage1Profit and not stage2Profit and percentage <= -0.05 :
#                     print("işlem biraz yükseldikten sonra ilk kar payına gelemedi ve stop oldu.")
#                     profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     break
#                 if engine.earlyClosePosition :
#                     profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     break
#                 if signals[index+3][1] <= int(past[1][0])  :
#                     if stage1Profit and not stage2Profit :
#                        profitLoss = (money/2)* (percentage - 0.045) * margin / 100 
#                     elif stage2Profit and stage1Profit :
#                        profitLoss = (money/4)* (percentage - 0.045) * margin / 100 
#                     print("işlem farklı sinyal aldığı için kapatıldı." , profitLoss)
#                     break
#                 if engine.stopLossStage1 :
#                     profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem zararla stop oldu" , profitLoss )
#                     input("1")
#                     break
#                 if engine.profitStage1 and not stage1Profit :
#                     profitLoss = (money/2)* (percentage - 0.045) * margin / 100 
#                     print("İşlem 0.3 ten kar aldı devam ediyor" , profitLoss)
#                     stage1Profit = True
#                     input("2")
#                 if engine.profitStage2 and stage1Profit and not stage2Profit :
#                     profitLoss = profitLoss + (money/4 * (percentage - 0.045) * margin / 100) 
#                     print("İşlem 0.5 ten kar aldı devam ediyor" , profitLoss)
#                     stage2Profit = True
#                     input("3")
#                 if engine.profitStage3 and stage2Profit :
#                     profitLoss = profitLoss + (money/4) * (percentage - 0.045) * margin / 100 
#                     print("İşlem maksimum kar ederek kapandı" , profitLoss)
#                     input("4")
#                     break
#                 if engine.stopLossStage2 and stage1Profit and percentage <= 0.1 :
#                     profitLoss = profitLoss + (money/4) * (percentage -  0.045) * margin / 100 
#                     print("İşlem 0.5 ten kar aldiktan sonra entry stop yaptı" , profitLoss)
#                     input("5")
#                     break
#                 if engine.stopLossStage3 and stage1Profit and not stage2Profit and percentage <= -0.1 :
#                     profitLoss = profitLoss + (money/2) * (percentage -  0.045) * margin / 100 
#                     print("İşlem 0.3 ten kar aldiktan sonra az zararla kapattı" , profitLoss)
#                     input("6")
#                     break
#                 counter += 1
#             if signals[index+3][1] <= int(past[1][0]) and not isMachineActive :
#                 print("işlem açılmadan yeni sinyal geldi" , signals[index+2][1] , int(past[1][0]) )
#                 money = money + fee
#                 break
#         money = money + profitLoss
#         print(money)