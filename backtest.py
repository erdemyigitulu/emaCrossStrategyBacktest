import csv
import json
import numpy as np
from calculations import calculateEma
from config import fixedMonths, main15mcsv , years , months
from utils import convertCsvToParquet , extractSignals , findPurchasePoints 

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
        self.isEmaSideChange = False

    def stage1(self):
        if self.stage1Start :
            self.stopLoss = True
            self.sellPoint1 = True
            self.stage1Phase1 = True          
  
    def stage2(self):
        self.stopLoss = False
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

def calculateAvaregePrice(islemler):
    totalCost = sum(fiyat * miktar for fiyat, miktar in islemler)
    totalAmount = sum(miktar for _, miktar in islemler)
    ortalama = totalCost / totalAmount
    return ortalama , totalAmount
def moneyProfitLossFunc(profitLoss , money , pnL , portion):
    if profitLoss == 0 :
        profitLoss = ((money * (100 + pnL)/100 )- money) * portion
        print(profitLoss)
    else :
        profitLoss = profitLoss + ((money * (100 + pnL)/100 )- money) * portion
        print(profitLoss)
    print(profitLoss , money , pnL, portion )
    return profitLoss

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
def updateEma(newPrice , signal , organisedEmaValues ):
    for values in organisedEmaValues :
        result = False
        if values["timestamp"] == signal[1] :
            previousEma = values["ema5"]
            break
    multiplier = 2 / (15 + 1)
    updatedEma = (newPrice - previousEma) * multiplier + previousEma
    if signal[0] == "short" :
        updatedEma = - updatedEma
        previousEma = - previousEma
    if updatedEma < previousEma :
        result = True

    return result
def backTestofMachine () :
   
    for year in years :
        for month in months :
            datas15m , resultscsv , csv1s , parquet1s , date  = fixedMonths(month,year)
            signals = extractSignals(datas15m , date)
            data1s = convertCsvToParquet(csv1s,parquet1s) 
            resultDatas = []
            totalpnL = 0
            profit = 0
            loss = 0
            profits = 0
            losss = 0
            entryStops = 0
            for index , signal in enumerate(signals[1:]) :
                try :
                    nextSignal = signals[(index + 2)][1]
                except :
                    break
                startProcessTimeStamp = int(signal[1]) + 900000
                timestamp_column = data1s[:, 0]
                start_index = np.argmax(timestamp_column >= startProcessTimeStamp)
                firstValue = data1s[start_index][1]
                purchasePoints = findPurchasePoints(firstValue,signal[0])
                startProcessValue = (firstValue,12000)
                seperateMoney = 150
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
                for past in data1s[start_index:]:
                    currentValue = past[1]
                    currentTimeStamp =int(past[0]) 
                    for point in purchasePoints :
                        if currentValue <= point and signal[0] == "long" :
                            if not (point,seperateMoney) in purchasedPoints :
                                purchasedPoints.append((point,seperateMoney))
                        elif currentValue >= point and signal[0] == "short" :
                            if not (point,seperateMoney) in purchasedPoints :
                                purchasedPoints.append((point,seperateMoney))
                    avaregePrice , totalAmount = calculateAvaregePrice(purchasedPoints)
                    pnL = percentageIncrease(avaregePrice , currentValue , signal[0] )
                   
                    print(pnL,currentTimeStamp,currentValue,firstValue)
                    machine.currentPnL = pnL
                    if machine.stage1Start :
                        machine.stage1()
                    if machine.stage2Start :
                        machine.stage2()
                    if machine.stage3Start :
                        machine.stage3()
                    if machine.stopLoss and pnL <= -0.2:
                        print("STOPKE")
                        message = "STOPKE"
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 1)
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        
                        break
                    if machine.entryStop and pnL <= 0.04 :
                        message = "Stage 2 de 0.3 den kar alıp entry stop"
                        messages.append(message)
                        print("Stage 2 de entry stop")
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if machine.stage1Start and machine.sellPoint1 and pnL >= 0.2 and aa:
                        portion = portion - 0.5
                        print("stage1 bitti kar aldım")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.5 )
                        message = "stage1 bitti 0.3 den kar aldım"
                        messages.append(message)
                        
                        aa = False
                    if machine.stage2Start and machine.sellPoint2 and pnL >= 0.5 and bb :
                        portion = portion - 0.25
                        print("stage2 bitti kar aldım")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.25 )
                        message = "stage2 bitti 0.5 den kar aldım"
                        messages.append(message)
                        bb = False
                    if machine.stage3Start and machine.sellPoint3 and pnL >= 1 :
                        print("işlem tam karla kapatılıyor")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.25 )
                        message = "işlem tam karla kapatılıyor"
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if machine.increaseStopPoint1 and pnL == 0.19:
                        print("stage3 de 0.5 den kar aldım 0.15 de stop oluyorum ")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.25 )
                        message = "stage3 de 0.5 den kar aldım 0.15 de stop oluyorum"
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if machine.increaseStopPoint2 and pnL <= 0.34 :
                        print("stage3 de 0.65 e kadar yükselip 0.3 de stop oldum")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.25 )
                        message = "stage3 de 0.65 e kadar yükselip 0.3 de stop oldum"
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if machine.increaseStopPoint3 and pnL <= 0.54:
                        print("stage 3 de 0.8 e gelip 0.5 de stop oluyorum")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , 0.25 )
                        message = "stage 3 de 0.8 e gelip 0.5 de stop oluyorum"
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if currentTimeStamp > nextSignal + 900000 :
                        print("yeni sinyal geldiği için işlemi kapatıyorumke")
                        profitLoss = moneyProfitLossFunc(profitLoss , totalAmount , pnL , portion )
                        message = "yeni sinyal geldiği için işlemi kapatıyorumke"
                        messages.append(message)
                        resultDatas.append({"signal":signal[0] , "signalTimeStamp":signal[1] , "startProcessTimeStamp":startProcessTimeStamp , "profitLoss":profitLoss, "totalAmount" : totalAmount })
                        break
                    if a :
                        print("Stage1 başladı")
                        a = False
                    if pnL >= 0.2 and b :
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
                resultDatas[-1]["processEndTimeStamp"] = currentTimeStamp
                resultDatas[-1]["purchasedPoints"] = purchasedPoints
                resultDatas[-1]["situationOfProcess"] = messages
                resultDatas[-1]["totalPnL"] = totalpnL
                resultDatas[-1]["totalProfit"] = (profit,profits)
                resultDatas[-1]["totalLoss"] = (loss,losss)
                resultDatas[-1]["totalEntryStop"] = entryStops
               

                with open(resultscsv, 'w' , encoding='utf-8' ) as json_file:
                    json.dump(resultDatas, json_file, indent=4, separators=(',',': '),ensure_ascii=False)
    


backTestofMachine ()


