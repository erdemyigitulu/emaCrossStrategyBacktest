from experta import *


class TradeManagement(Fact):
    pass
class EmaValuesProcess(Fact) :
    pass
class TradeEngine(KnowledgeEngine):
    @Rule(TradeManagement(aa="aa"))
    def func(self):
        print("tamam")


def engineer () :
    engine = TradeEngine()
    engine.reset()
    trade_management_aa = TradeManagement(aa="aaa" , bb= "bbb")
    trade_management_cc = TradeManagement(cc = "cc")
    print(trade_management_aa["aa"], trade_management_aa["bb"])
    if trade_management_aa


engineer()











#ikinci kods
# for index , signal in enumerate(signals[1:]):
#         profit0point3 = False
#         profit0point5 = False
#         isPriceCame = False
#         isMachineActivated = False
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
#             targetValue = firstValue - (firstValue * 0.1 / 100)
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
#                 engine.declare(TradeStart(start= "start"))
#                 isMachineActivated = True
#                 if counter == 0 :
#                     input("THE MACHINE IS ACTIVATED") 
#                 if currentValue < 0 :
#                     currentValue = -(currentValue)
#                 percentage = percentageIncrease(targetValue,currentValue)
#                 if signal[0] == "short" and percentage != 0 :
#                     percentage = -(percentage)
#                 print(percentage , targetValue , currentValue , int(past[1][0]))
#                 if int(past[1][0]) - signal[1]  < 1800000 :
#                     engine.declare(TradeManagement(timeStamp = past[1][0] , price = past[1][1] , signal = signal[0]))
#                 engine.declare(TradeManagement(pnL=percentage))
#                 engine.run()
#                 if engine.entryStop03  and percentage <= -0.1:
#                     profitLoss = after03MoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem 0.3 den kar aldıktan sonra -0.1 de entry stop oldu",profitLoss)
#                     input()
#                     break
#                 if engine.entryStop05 and percentage <= 0.1  :
#                     profitLoss = after05MoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem 0.5 den kar aldıktan sonra 0.1 de entry stop oldu",profitLoss)
#                     input()
#                     break
#                 if engine.stopLoss and isMachineActivated :
#                     profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem zararla stop oldu" , profitLoss )
#                     input()
#                     break
#                 if engine.protectProcess1 :
#                     if engine.profit03 :
#                         profitLoss = after03MoneyProfitLossFunc(profitLoss , money , percentage)
#                     if engine.profit05 :
#                         profitLoss = after05MoneyProfitLossFunc(profitLoss , money , percentage)
#                     else :
#                         profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem ilk iki mumda terse hareket ettiği için erken kapatılıyor", profitLoss)
#                     input()
#                     break
#                 if engine.protectProcess2 and percentage <= 0.05:
#                     profitLoss = allMoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem ilk alım noktasına yaklaşmasına rağmen geri hareket sonrası kapatılıyor",profitLoss)
#                     input()
#                     break
#                 if engine.profit03 and isMachineActivated and not profit0point3 :
#                     profitLoss = after03MoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem 0.3 ten kar alarak devam ediyor",profitLoss)
#                     input()
#                     profit0point3 = True
#                 if engine.profit05 and not profit0point5:
#                     profitLoss = after05MoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem 0.5 ten kar alarak devam ediyor",profitLoss)
#                     input()
#                     profit0point5 = True
#                 if engine.profit1 :
#                     profitLoss = after05MoneyProfitLossFunc(profitLoss , money , percentage)
#                     print("İşlem 1 den kar alarak kapanıyor",profitLoss)
#                     input()
#                     break
#                 counter += 1 
#             else :
#                 engine.declare(TradeStart(start= "notstart"))
#                 print( currentValue ,comparisonValue ,  int(past[1][0]) , past[1][1] ) 
#                 if signals[index+3][1] <= int(past[1][0]) :
#                     print("işlem açılmadan yeni sinyal geldi" , signals[index+2][1] , int(past[1][0]) )
#                     money = money + fee
#                     input()
#                     break
#                 if engine.wrongSignal :
#                     print("İşlem açılmadan sinyal alım bölgesine geldi. Yeni sinyale geçiliyor ")
#                     input()
#                     break
#         money = money + profitLoss
#         print(money)




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
    
#     machineIsActivated = False
#     stopLoss = False #İşlemin direkt stop olması
#     wrongSignal =False #İşlem açılmadan kar noktasına ulaştı ve sinyal başarılı gerçekleşmedi
#     protectProcess1 = False # Ema ters yöne hareket başladığı için sinyal kapatılır
#     protectProcess2  = False # İşlem kar almaya çok yaklaştıktan sonra terse harekette sinyal kapatılır.
#     profit03 = False #Kar noktaları
#     profit05 = False #Kar noktaları
#     profit1 = False #Kar noktaları
#     entryStop03 = False #Kar alındıktan sonra fiyat düşerse entry stop yapılır
#     entryStop05 = False #Kar alındıktan sonra fiyat düşerse entry stop yapılır

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)) , TradeManagement(start = "notstart")))
#     def wrongSignalFunc(self):
#         self.wrongSignal = True

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x <= -0.2))) , (TradeManagement(start="start")))
#     def stopLoss1(self):
#         self.stopLoss = True

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.2)) , NOT(TradeManagement(profit03="active"))))
#     def protectProcess(self):
#         self.protectProcess2 = True

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.3)) , NOT(TradeManagement(profit03="active"))))
#     def profit03Func(self):
#         self.profit03 = True
#         self.profit03 = "active"

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 0.5))) , TradeManagement(profit03="active") , NOT(TradeManagement(profit05="active")))
#     def profit05Func(self):
#         self.profit05 = True
#         self.declare(TradeManagement(profit05="active"))
#         self.declare(TradeManagement(profit03="active"))

#     @Rule(AND(TradeManagement(pnL=P(lambda x: x >= 1 )),  TradeManagement(profit05="active") , NOT(TradeManagement(profit1="active"))))
#     def profit1Func(self):
#         self.profit1 = True

#     @Rule(AND(TradeManagement(profit03="active")  , NOT(TradeManagement(profit05 = "active"))))
#     def stopLoss2(self):
#         self.entryStop03 = True

#     @Rule(AND(TradeManagement(profit05="active")  , NOT(TradeManagement(profit1 = "active"))))
#     def stopLoss4(self):
#         print("buradayım")
#         self.entryStop05 = True
    
#     @Rule(EmaValuesProcess(timeStamp=P(lambda x: x) , price=P(lambda y: y) , signal=P(lambda z: z)))
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
#             self.protectProcess1 = True